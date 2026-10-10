import subprocess
from datetime import datetime

def  run_git(*args):
    """Run a Git command and return its output."""
    try:
        result = subprocess.run(
            ["git", *args],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as error:
        return f"Error: {error.stderr.strip()}"
    except FileNotFoundError:
        return "Error: Git is not installed or unavailable."

def show_repository_status():
    print("\n=== REPOSITORY STATUS ===")

    branch = run_git("branch", "--show-current")
    print("fBranch: {branch}")

    status = run_git("status", "--short")

    if status.startswith("Error:"):
        print(status)
    elif status:
        print("\nFiles needing attention:")
        print(status)
    else:
        print("Working tree is clean:")

def show_recent_commits():
    print("\n=== RECENT COMMITS ===")


    commits = run_git(
        "log",
        "-5",
        "--date=short",
        "--pretty=format:%h | %ad | %s",
    )

    if commits.startswith("Error:"):
        print(commits)
    elif commits:
        print(commits)
    else:
        print("No commits found.")

def show_sync_status():
    print("\n=== GITHUB SYNC STATUS ===")

    upstream = run_git(
        "rev-parse",
        "--abbrev-ref",
        "--symbolic-full-name",
        "@{u}",
    )

    if upstream.startswith("Error:"):
        print("No upstream branch configured.")
        return

    counts = run_git(
        "rev-list",
        "--left-right",
        "--count",
        f"HEAD...{upstream}",
        
    )

    if counts.startswith("Error:"):
        print(counts)
        return

    ahead, behind = map(int, counts.split())

    print(f"Remote branch: {upstream}")
    print(f"Local commits not pushed: {ahead}")
    print(f"Remote commits not pulled: {behind}")

    if ahead == 0 and behind == 0:
        print("Your branch is synchronised.")
    elif ahead > 0 and behind > 0:
        print("Your branch has diverged from the remote.")
    elif ahead > 0:
        print("You have commits waiting to be pushed.")
    else:
        print("Updates are available from GitHub.")

def show_report():
    print("=" * 40)
    print("     GITHUB CONTRIBUTION ASSISTANT ")
    print("=" * 40)
    print("Report generated:", datetime.now().strftime("%Y-%m-%d %H:%M"))

    show_repository_status()
    show_recent_commits()
    show_sync_status()

    print("\nReport complete. No files were modified.")

if __name__ == "__main__":
    show_report()
    

                      
                      
