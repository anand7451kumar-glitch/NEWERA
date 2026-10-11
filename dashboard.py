import subprocess
from pathlib import Path
from datetime import datetime


def run_command(command):
    """Run a command and return its output."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=15,
        )

        if result.returncode != 0:
            return f"Error: {result.stderr.strip()}"

        return result.stdout.strip()

    except FileNotFoundError:
        return "Error: Command not found."

    except subprocess.TimeoutExpired:
        return "Error: Command timed out."


def repository_overview():
    print("\n--- REPOSITORY OVERVIEW ---")

    root = run_command(["git", "rev-parse", "--show-toplevel"])
    branch = run_command(["git", "branch", "--show-current"])
    status = run_command(["git", "status", "--short"])

    print("Repository:", root)
    print("Branch:", branch)

    if status.startswith("Error:"):
        print(status)
    elif status:
        print("\nFiles with changes:")
        print(status)
    else:
        print("Working tree: Clean")


def recent_commits():
    print("\n--- LAST 10 COMMITS ---")

    output = run_command([
        "git",
        "log",
        "-10",
        "--date=short",
        "--pretty=format:%h | %ad | %s",
    ])

    print(output or "No commits found.")


def contribution_summary():
    print("\n--- CONTRIBUTION SUMMARY ---")

    today = datetime.now().date()
    output = run_command([
        "git",
        "log",
        "--since=30 days ago",
        "--format=%ad",
        "--date=short",
    ])

    if output.startswith("Error:"):
        print(output)
        return

    dates = output.splitlines() if output else []
    total = len(dates)
    active_days = len(set(dates))

    print("Commits in the last 30 days:", total)
    print("Days with commits:", active_days)

    if dates:
        print("Most recent commit date:", max(dates))
    else:
        print("No commits found in the last 30 days.")


def sync_status():
    print("\n--- GITHUB SYNCHRONIZATION ---")

    upstream = run_command([
        "git",
        "rev-parse",
        "--abbrev-ref",
        "--symbolic-full-name",
        "@{u}",
    ])

    if upstream.startswith("Error:"):
        print("No upstream branch configured.")
        return

    fetch = input("Fetch latest remote changes first? (y/N): ").strip().lower()

    if fetch == "y":
        output = run_command(["git", "fetch", "--prune"])

        if output.startswith("Error:"):
            print(output)
            return

        print("Remote information updated.")

    counts = run_command([
        "git",
        "rev-list",
        "--left-right",
        "--count",
        f"HEAD...{upstream}",
    ])

    if counts.startswith("Error:"):
        print(counts)
        return

    ahead, behind = map(int, counts.split())

    print("Remote branch:", upstream)
    print("Commits waiting to be pushed:", ahead)
    print("Remote commits not present locally:", behind)

    if ahead == 0 and behind == 0:
        print("Local and remote branches match.")
    elif ahead and behind:
        print("Branches have diverged.")
    elif ahead:
        print("Local commits are waiting to be pushed.")
    else:
        print("Remote changes are available to pull.")


def generate_report():
    print("\n--- GENERATE MARKDOWN REPORT ---")

    commits = run_command([
        "git",
        "log",
        "-7 days ago",
        "--format=%ad|%h|%s",
        "--date=short",
    ])

    # Use the correct Git time filter.
    commits = run_command([
        "git",
        "log",
        "--since=7 days ago",
        "--format=%ad|%h|%s",
        "--date=short",
    ])

    if commits.startswith("Error:"):
        print(commits)
        return

    report = [
        "# GitHub Coding Activity",
        "",
        f"Generated: {datetime.now():%Y-%m-%d %H:%M}",
        "",
    ]

    if commits:
        for line in commits.splitlines():
            date, commit_hash, message = line.split("|", 2)
            report.append(f"- **{date}** — `{commit_hash}` — {message}")
    else:
        report.append("No commits found in the last seven days.")

    output = Path("dashboard_report.md")
    output.write_text("\n".join(report) + "\n", encoding="utf-8")

    print("Report saved to:", output.resolve())


def main():
    while True:
        print("\n" + "=" * 38)
        print("     GITHUB CONTRIBUTION DASHBOARD")
        print("=" * 38)
        print("1. Repository overview")
        print("2. Recent commits")
        print("3. Contribution summary")
        print("4. GitHub synchronization")
        print("5. Generate Markdown report")
        print("6. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            repository_overview()
        elif choice == "2":
            recent_commits()
        elif choice == "3":
            contribution_summary()
        elif choice == "4":
            sync_status()
        elif choice == "5":
            generate_report()
        elif choice == "6":
            print("Dashboard closed.")
            break
        else:
            print("Invalid choice. Enter 1–6.")


if __name__ == "__main__":
    main()