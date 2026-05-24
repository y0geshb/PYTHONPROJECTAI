#!/usr/bin/env python3
"""
setup_github.py - Automate GitHub project upload and setup for QA engineers.

Features:
- Initializes git if needed
- Creates .gitignore if missing
- Commits all files
- Connects to a remote GitHub repo
- Pushes to a configurable branch
- Logs errors and progress

Usage:
    python setup_github.py --repo-url https://github.com/y0geshb/PYTHONPROJECTAI.git --branch <BRANCH_NAME> --message "Initial commit"

Environment variables (optional):
    GITHUB_REPO_URL, GIT_BRANCH, GIT_COMMIT_MSG, GIT_USER_NAME, GIT_USER_EMAIL

"""
import os
import subprocess
import sys
from pathlib import Path
import argparse
from datetime import datetime

def log(msg):
    print(f"[setup_github] {msg}")

def run(cmd, check=True, **kwargs):
    log(f"Running: {' '.join(cmd)}")
    try:
        return subprocess.run(cmd, check=check, capture_output=True, text=True, **kwargs)
    except subprocess.CalledProcessError as e:
        log(f"ERROR: {e.stderr.strip() if e.stderr else str(e)}")
        sys.exit(1)


def is_git_repository():
    result = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        check=False,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0 and result.stdout.strip() == "true"


def backup_broken_git_dir(git_dir: Path):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_dir = git_dir.with_name(f".git.broken.{timestamp}")
    git_dir.rename(backup_dir)
    log(f"Existing broken .git directory moved to {backup_dir}")


def ensure_git_identity(user_name=None, user_email=None):
    existing_name = subprocess.run(
        ["git", "config", "user.name"],
        check=False,
        capture_output=True,
        text=True,
    ).stdout.strip()
    existing_email = subprocess.run(
        ["git", "config", "user.email"],
        check=False,
        capture_output=True,
        text=True,
    ).stdout.strip()

    resolved_name = user_name or os.getenv("GIT_USER_NAME") or existing_name
    resolved_email = user_email or os.getenv("GIT_USER_EMAIL") or existing_email

    if resolved_name and not existing_name:
        run(["git", "config", "user.name", resolved_name])
    if resolved_email and not existing_email:
        run(["git", "config", "user.email", resolved_email])

    if not resolved_name or not resolved_email:
        log(
            "ERROR: Git user identity is not configured. Provide --git-user-name and --git-user-email, "
            "or set GIT_USER_NAME and GIT_USER_EMAIL, or configure git manually."
        )
        sys.exit(1)

def check_git_installed():
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
    except Exception:
        log("Git is not installed or not in PATH. Please install Git and try again.")
        sys.exit(1)

def ensure_gitignore():
    gi = Path(".gitignore")
    if not gi.exists():
        log("Creating default .gitignore...")
        gi.write_text("""# Python
__pycache__/
*.py[cod]
.venv/
venv/
env/
.env
.pytest_cache/
.idea/
.vscode/
.DS_Store
Thumbs.db
reports/
Archieve/
Archieves/
""")
    else:
        log(".gitignore already exists.")

def init_git():
    git_dir = Path(".git")

    if is_git_repository():
        log("Git repository already initialized.")
        return

    if git_dir.exists():
        log("Detected invalid or broken .git metadata. Backing it up before reinitializing...")
        backup_broken_git_dir(git_dir)

    if not git_dir.exists():
        log("Initializing git repository...")
        run(["git", "init"])

def add_all_and_commit(commit_msg):
    run(["git", "add", "."])
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        check=False,
        capture_output=True,
        text=True,
    )
    if not status.stdout.strip():
        log("No changes to commit. Skipping commit step.")
        return
    run(["git", "commit", "-m", commit_msg])

def set_remote(repo_url):
    remotes = subprocess.run(["git", "remote"], capture_output=True, text=True).stdout.split()
    if "origin" in remotes:
        log("Remote 'origin' already set. Updating URL...")
        run(["git", "remote", "set-url", "origin", repo_url])
    else:
        log("Adding remote 'origin'...")
        run(["git", "remote", "add", "origin", repo_url])

def push_to_github(branch):
    try:
        run(["git", "push", "-u", "origin", branch])
    except SystemExit:
        log("Push failed. Check your authentication, repo URL, and permissions.")
        sys.exit(1)

def main():
    check_git_installed()
    parser = argparse.ArgumentParser(description="Automate GitHub project upload.")
    parser.add_argument(
        "--repo-url",
        default=os.getenv("GITHUB_REPO_URL", "https://github.com/y0geshb/PYTHONPROJECTAI.git"),
        help="GitHub repository URL",
    )
    parser.add_argument("--branch", default=os.getenv("GIT_BRANCH", "main"), help="Branch name (default: main)")
    parser.add_argument("--message", default=os.getenv("GIT_COMMIT_MSG", "Initial project commit"), help="Commit message")
    parser.add_argument("--git-user-name", default=os.getenv("GIT_USER_NAME"), help="Git author name for commits")
    parser.add_argument("--git-user-email", default=os.getenv("GIT_USER_EMAIL"), help="Git author email for commits")
    args = parser.parse_args()

    if not args.repo_url:
        log("ERROR: GitHub repository URL must be provided via --repo-url or GITHUB_REPO_URL.")
        sys.exit(1)

    ensure_gitignore()
    init_git()
    ensure_git_identity(args.git_user_name, args.git_user_email)
    add_all_and_commit(args.message)
    set_remote(args.repo_url)
    push_to_github(args.branch)
    log(f"Project pushed to {args.repo_url} on branch {args.branch}.")
    log("GitHub setup complete!")

if __name__ == "__main__":
    main()
