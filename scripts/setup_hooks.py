#!/usr/bin/env python3
"""
Setup script to install git hooks for the MCP & Skills tutorial.

Installs:
  - pre-commit hook: Scans for leaked API keys and secrets before every commit

Usage:
  python scripts/setup_hooks.py
"""

import shutil
import stat
import subprocess
import sys
from pathlib import Path


def main():
    repo_root = Path(__file__).parent.parent

    # Ensure we're in a git repo
    git_dir = repo_root / ".git"
    if not git_dir.exists():
        print("Initialising git repository...")
        subprocess.run(["git", "init"], cwd=str(repo_root), check=True)
        git_dir = repo_root / ".git"

    hooks_dir = git_dir / "hooks"
    hooks_dir.mkdir(exist_ok=True)

    # Install pre-commit hook
    source = repo_root / "scripts" / "pre-commit-secrets-scan.sh"
    target = hooks_dir / "pre-commit"

    if target.exists():
        print(f"Backing up existing pre-commit hook to {target}.bak")
        shutil.copy2(str(target), str(target) + ".bak")

    shutil.copy2(str(source), str(target))

    # Make executable
    target.chmod(target.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)

    print(f"Installed pre-commit hook: {target}")
    print()
    print("The hook will scan for leaked API keys and secrets before every commit.")
    print("To bypass in emergencies: git commit --no-verify")
    print()
    print("Setup complete!")


if __name__ == "__main__":
    main()
