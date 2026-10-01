#!/usr/bin/env python3
"""A tiny local task manager. Uses only the Python standard library."""

from __future__ import annotations

import argparse
import os
import sqlite3
import sys
from datetime import date
from pathlib import Path


def database_path() -> Path:
    """Choose a persistent per-user location, respecting the XDG convention."""
    base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    return base / "taskflow" / "tasks.sqlite3"


def connect() -> sqlite3.Connection:
    path = database_path()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        db = sqlite3.connect(path)
    except (OSError, sqlite3.Error):
        # Restricted environments may block the normal per-user data folder.
        # Keep the database beside the script as a practical fallback.
        path = Path(__file__).with_name("taskflow.sqlite3")
        db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.execute("""CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        due TEXT,
        priority INTEGER NOT NULL DEFAULT 2,
        created TEXT NOT NULL,
        done INTEGER NOT NULL DEFAULT 0
    )""")
    return db


def parse_date(value: str | None) -> str | None:
    if value is None:
        return None
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Use a date in YYYY-MM-DD format.") from exc


def add_task(args: argparse.Namespace) -> None:
    due = parse_date(args.due)
    with connect() as db:
        cur = db.execute(
            "INSERT INTO tasks(title, due, priority, created) VALUES (?, ?, ?, ?)",
            (args.title, due, args.priority, date.today().isoformat()),
        )
    print(f"Added task #{cur.lastrowid}: {args.title}")


def display(tasks: list[sqlite3.Row]) -> None:
    if not tasks:
        print("No tasks here. You're all caught up.")
        return
    labels = {1: "HIGH", 2: "MED ", 3: "LOW "}
    today = date.today().isoformat()
    for task in tasks:
        due = task["due"] or "no due date"
        if task["due"] and task["due"] < today:
            due += " (overdue)"
        mark = "x" if task["done"] else " "
        print(f"[{mark}] #{task['id']:<4} {labels[task['priority']]}  {due:<24} {task['title']}")


def list_tasks(args: argparse.Namespace) -> None:
    clauses = ["done = 0"] if not args.all else []
    params: list[object] = []
    if args.today:
        clauses.append("(due IS NULL OR due <= ?)")
        params.append(date.today().isoformat())
    where = " WHERE " + " AND ".join(clauses) if clauses else ""
    with connect() as db:
        rows = db.execute(
            f"SELECT * FROM tasks{where} ORDER BY done, CASE WHEN due IS NULL THEN 1 ELSE 0 END, due, priority, id",
            params,
        ).fetchall()
    display(rows)


def set_done(args: argparse.Namespace) -> None:
    with connect() as db:
        cur = db.execute("UPDATE tasks SET done = 1 WHERE id = ? AND done = 0", (args.id,))
    if cur.rowcount:
        print(f"Completed task #{args.id}.")
    else:
        print(f"No open task found with ID #{args.id}.", file=sys.stderr)
        raise SystemExit(1)


def remove_task(args: argparse.Namespace) -> None:
    with connect() as db:
        cur = db.execute("DELETE FROM tasks WHERE id = ?", (args.id,))
    if cur.rowcount:
        print(f"Deleted task #{args.id}.")
    else:
        print(f"No task found with ID #{args.id}.", file=sys.stderr)
        raise SystemExit(1)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="taskflow",
        description="A simple local task list with due dates and priorities.",
        epilog="Examples: taskflow add 'Pay rent' --due 2026-10-05 --priority 1; taskflow today",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    add = commands.add_parser("add", help="Add a task")
    add.add_argument("title", help="Task description")
    add.add_argument("--due", help="Due date (YYYY-MM-DD)")
    add.add_argument("--priority", type=int, choices=(1, 2, 3), default=2,
                     help="1 = high, 2 = medium (default), 3 = low")
    add.set_defaults(run=add_task)

    listing = commands.add_parser("list", help="Show open tasks")
    listing.add_argument("--all", action="store_true", help="Include completed tasks")
    listing.set_defaults(run=list_tasks, today=False)

    today = commands.add_parser("today", help="Show tasks due today, overdue, or without a due date")
    today.set_defaults(run=list_tasks, today=True, all=False)

    done = commands.add_parser("done", help="Mark a task complete")
    done.add_argument("id", type=int, help="Task ID shown by list")
    done.set_defaults(run=set_done)

    delete = commands.add_parser("delete", help="Delete a task")
    delete.add_argument("id", type=int, help="Task ID shown by list")
    delete.set_defaults(run=remove_task)
    return parser


def main() -> None:
    parser = build_parser()
    # Running the file with no arguments should still be useful: show the list.
    args = parser.parse_args(sys.argv[1:] or ["list"])
    try:
        args.run(args)
    except argparse.ArgumentTypeError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
