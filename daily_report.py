import subprocess
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def get_commits(days=7):
    """Get commits from the last few days."""
    result = subprocess.run(
        [
            "git",
            "log",
            f"--since={days} days ago",
            "--date=short",
            "--pretty=format:%ad|%h|%s",
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())

    commits = []

    for line in result.stdout.splitlines():
        if not line:
            continue

        date, commit_hash, message = line.split("|", 2)

        commits.append({
            "date": date,
            "hash": commit_hash,
            "message": message,
        })

    return commits


def create_report(commits, days):
    """Create a Markdown activity report."""
    grouped = defaultdict(list)

    for commit in commits:
        grouped[commit["date"]].append(commit)

    report = [
        "# GitHub Coding Activity Report",
        "",
        f"Generated: {datetime.now():%Y-%m-%d %H:%M}",
        f"Period: Last {days} days",
        f"Total commits: {len(commits)}",
        "",
    ]

    if not commits:
        report.append("No commits found during this period.")
    else:
        for date in sorted(grouped, reverse=True):
            report.extend([f"## {date}", ""])

            for commit in grouped[date]:
                report.append(
                    f"- `{commit['hash']}` — {commit['message']}"
                )

            report.append("")

    return "\n".join(report)


def main():
    print("=== DAILY CODING REPORT ===")

    try:
        days = int(input("How many days should be included? (default 7): ") or "7")

        if days < 1:
            print("Please enter a number greater than zero.")
            return

        commits = get_commits(days)
        report = create_report(commits, days)

        output_file = Path("daily_coding_report.md")
        output_file.write_text(report + "\n", encoding="utf-8")

        print(f"\nCommits found: {len(commits)}")
        print(f"Report saved to: {output_file.resolve()}")
        print("\n--- REPORT PREVIEW ---\n")
        print(report)

    except ValueError:
        print("Please enter a valid whole number.")
    except (RuntimeError, OSError) as error:
        print(f"Could not create report: {error}")


if __name__ == "__main__":
    main()