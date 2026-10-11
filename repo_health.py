import subprocess
from datetime import datetime

def git_command(*args):
    """Run a Git command safely."""
    result = subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return None, result.stderr.strip()

    return result.stdout.strip(), None

def check_repository():
    print("\n" + "=" * 45)
    print("  REPOSITORY HEALTH CHECK")
    print("=" * 45)

    #1. Check current branch
    branch, error = git_command(
        "branch", "--show-current"
    )

    if error:
        print("Git error:", error)
        return

    print(f"\n Current branch: {branch}")

    #Checking working tree
    status, errror = git_command("status", "--short")

    if error:
        print("Could not check working tree:", error)
        return

    if status:
        print("\n Uncommited changes detected:")
        print(status)

    else:
        print("\n Working Tree is clean.")

    #3. Check latest commit
    latest, error = git_command(
        "log",
        "-1",
        "--format=%h|%s|%cI",
    )

    if error:
        print("\n Could not retreive latest commit.")
    elif latest:
        commit_hash, message, timestamp = latest.split("|", 2)

        commit_date = datetime.fromisoformat(timestamp)
        age = datetime.now(commit_date.tzinfo) - commit_date

        print("\n Latest commit:")
        print(f" Hash: {commit_hash}")
        print(f" Message: {message}")
        print(f" Date: {timestamp}")
        print(f" Age: {age.days} day(s)")

    else:
        print("\n No commits found.")

    #4. Check remote synchronisation
    upstream, error = git_command(
        "rev-parse",
        "--abbrev-ref",
        "--symbolic-full-name",
        "@{u}",

    )
    if error:
        print("\n No upstream branch configured.")
        return

    counts, error = git_command(
        "rev-list",
        "--left-right",
        "--count",
        f"HEAD..{upstream}",
    )

    if error:
        print("\n could not compare with remote.")
        return

    ahead, behind = map(int, counts.split())

    print("\n Remote synchronisations:")
    print(f" Local commits not pushed: {ahead}")
    print(f" Remote commits not pulled: {behind}")

    if ahead == 0 and behind == 0:
        print(" Loacl and remote branches match.")
    elif ahead > 0 and behind > 0:
        print(" Branches have diverged.")
    elif ahead > 0:
        print(" Push may be needed.")
    else:
        print(" Pull may be needed.")

    print("\n" + "=" * 45)
    print("  HEALTH CHECK COMPLETE")
    print("=" * 45)

if __name__ == "__main__":
    check_repository()
    
    
    