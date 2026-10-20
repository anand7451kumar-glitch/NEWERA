
import json
import sqlite3
from datetime import date, timedelta
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "focusflow.db"


def connect_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db


def init_db():
    with connect_db() as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                priority TEXT NOT NULL DEFAULT 'Normal',
                due_date TEXT,
                completed INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT (datetime('now','localtime')),
                completed_at TEXT
            );

            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mode TEXT NOT NULL,
                minutes INTEGER NOT NULL,
                completed_at TEXT NOT NULL DEFAULT (datetime('now','localtime'))
            );
        """)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        if length > 100_000:
            raise ValueError("Request too large")
        raw = self.rfile.read(length)
        return json.loads(raw or b"{}")

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/api/tasks":
            with connect_db() as db:
                rows = db.execute("""
                    SELECT * FROM tasks
                    ORDER BY completed ASC, id DESC
                """).fetchall()
            return self.send_json([dict(row) for row in rows])

        if path == "/api/stats":
            today = date.today().isoformat()
            week_start = (date.today() - timedelta(days=6)).isoformat()

            with connect_db() as db:
                focus = db.execute("""
                    SELECT COALESCE(SUM(minutes), 0) AS total,
                           COUNT(*) AS sessions
                    FROM sessions
                    WHERE mode = 'focus'
                      AND date(completed_at) = ?
                """, (today,)).fetchone()

                tasks_done = db.execute("""
                    SELECT COUNT(*) AS total FROM tasks
                    WHERE completed = 1
                      AND date(completed_at) = ?
                """, (today,)).fetchone()

                week = db.execute("""
                    SELECT date(completed_at) AS day,
                           SUM(minutes) AS minutes
                    FROM sessions
                    WHERE mode = 'focus'
                      AND date(completed_at) BETWEEN ? AND ?
                    GROUP BY date(completed_at)
                """, (week_start, today)).fetchall()

            return self.send_json({
                "focusMinutes": focus["total"],
                "sessionCount": focus["sessions"],
                "taskCount": tasks_done["total"],
                "week": [dict(row) for row in week]
            })

        if path.startswith("/api/"):
            return self.send_json({"error": "Not found"}, 404)

        return super().do_GET()

    def do_POST(self):
        path = urlparse(self.path).path

        try:
            data = self.read_json()
        except (ValueError, json.JSONDecodeError):
            return self.send_json({"error": "Invalid JSON"}, 400)

        if path == "/api/tasks":
            title = str(data.get("title", "")).strip()
            priority = data.get("priority", "Normal")
            due_date = data.get("dueDate") or None

            if not title or len(title) > 160:
                return self.send_json({"error": "Task title must be 1–160 characters"}, 400)
            if priority not in ("Low", "Normal", "High"):
                return self.send_json({"error": "Invalid priority"}, 400)
            if due_date and (not isinstance(due_date, str) or len(due_date) != 10):
                return self.send_json({"error": "Invalid due date"}, 400)

            with connect_db() as db:
                cursor = db.execute("""
                    INSERT INTO tasks (title, priority, due_date)
                    VALUES (?, ?, ?)
                """, (title, priority, due_date))
                task_id = cursor.lastrowid
                row = db.execute(
                    "SELECT * FROM tasks WHERE id = ?", (task_id,)
                ).fetchone()

            return self.send_json(dict(row), 201)

        if path == "/api/sessions":
            mode = data.get("mode")
            minutes = data.get("minutes")

            if mode not in ("focus", "short", "long"):
                return self.send_json({"error": "Invalid session mode"}, 400)
            if type(minutes) is not int or not 1 <= minutes <= 180:
                return self.send_json({"error": "Invalid session length"}, 400)

            with connect_db() as db:
                cursor = db.execute("""
                    INSERT INTO sessions (mode, minutes)
                    VALUES (?, ?)
                """, (mode, minutes))
                session_id = cursor.lastrowid

            return self.send_json({"id": session_id}, 201)

        return self.send_json({"error": "Not found"}, 404)

    def do_PATCH(self):
        path = urlparse(self.path).path
        parts = path.strip("/").split("/")

        if len(parts) != 3 or parts[:2] != ["api", "tasks"]:
            return self.send_json({"error": "Not found"}, 404)

        try:
            task_id = int(parts[2])
            data = self.read_json()
        except (ValueError, json.JSONDecodeError):
            return self.send_json({"error": "Invalid request"}, 400)

        if not isinstance(data.get("completed"), bool):
            return self.send_json({"error": "Expected completed true or false"}, 400)

        with connect_db() as db:
            cursor = db.execute("""
                UPDATE tasks
                SET completed = ?,
                    completed_at = CASE WHEN ? = 1
                        THEN datetime('now','localtime')
                        ELSE NULL END
                WHERE id = ?
            """, (int(data["completed"]), int(data["completed"]), task_id))

            if cursor.rowcount == 0:
                return self.send_json({"error": "Task not found"}, 404)

        return self.send_json({"success": True})

    def do_DELETE(self):
        path = urlparse(self.path).path
        parts = path.strip("/").split("/")

        if len(parts) != 3 or parts[:2] != ["api", "tasks"]:
            return self.send_json({"error": "Not found"}, 404)

        try:
            task_id = int(parts[2])
        except ValueError:
            return self.send_json({"error": "Invalid task ID"}, 400)

        with connect_db() as db:
            cursor = db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            if cursor.rowcount == 0:
                return self.send_json({"error": "Task not found"}, 404)

        return self.send_json({"success": True})

    def log_message(self, format, *args):
        print(f"[FocusFlow] {args[0]}")


if __name__ == "__main__":
    init_db()
    server = ThreadingHTTPServer(("127.0.0.1", 8000), Handler)
    print("FocusFlow running at http://127.0.0.1:8000")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nFocusFlow stopped.")
    finally:
        server.server_close()
