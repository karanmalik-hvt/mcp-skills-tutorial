#!/usr/bin/env python3
"""
Setup script for the MCP & Skills tutorial.

Installs:
  - pre-commit hook: Scans for leaked API keys and secrets before every commit
  - Claude Code skills link: Makes skills/ discoverable at .claude/skills/

Usage:
  python scripts/setup_hooks.py
"""

import os
import platform
import shutil
import stat
import subprocess
import sys
from pathlib import Path


def install_pre_commit_hook(repo_root: Path):
    """Install the secrets-scanning pre-commit hook."""
    git_dir = repo_root / ".git"
    if not git_dir.exists():
        print("Initialising git repository...")
        subprocess.run(["git", "init"], cwd=str(repo_root), check=True)

    hooks_dir = git_dir / "hooks"
    hooks_dir.mkdir(exist_ok=True)

    source = repo_root / "scripts" / "pre-commit-secrets-scan.sh"
    target = hooks_dir / "pre-commit"

    if target.exists():
        print(f"  Backing up existing pre-commit hook to {target}.bak")
        shutil.copy2(str(target), str(target) + ".bak")

    shutil.copy2(str(source), str(target))
    target.chmod(target.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    print(f"  Installed pre-commit hook: {target}")


def link_skills_for_claude(repo_root: Path):
    """Link skills/ to .claude/skills/ so Claude Code auto-discovers them."""
    claude_dir = repo_root / ".claude"
    claude_dir.mkdir(exist_ok=True)

    skills_source = repo_root / "skills"
    skills_target = claude_dir / "skills"

    if not skills_source.exists():
        print("  Skipped — skills/ directory not found")
        return

    if skills_target.exists() or skills_target.is_symlink():
        print(f"  .claude/skills/ already exists — skipping")
        return

    system = platform.system()
    if system == "Windows":
        # Use a junction on Windows (no admin required)
        subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(skills_target), str(skills_source)],
            check=True, capture_output=True
        )
        print(f"  Created junction: .claude/skills/ -> skills/")
    else:
        # Use a relative symlink on macOS/Linux
        os.symlink(
            os.path.relpath(skills_source, claude_dir),
            skills_target
        )
        print(f"  Created symlink: .claude/skills/ -> skills/")


def main():
    repo_root = Path(__file__).parent.parent

    print("Setting up MCP & Skills tutorial...\n")

    print("[1/2] Installing pre-commit hook...")
    install_pre_commit_hook(repo_root)

    print("\n[2/2] Linking skills for Claude Code...")
    link_skills_for_claude(repo_root)

    print()
    print("Setup complete!")
    print()
    print("  Pre-commit hook: scans for leaked API keys before every commit")
    print("  Skills linked:   skills/ discoverable by all agents")
    print("                   .claude/skills/ linked for Claude Code auto-discovery")
    print()
    print("To bypass hook in emergencies: git commit --no-verify")


if __name__ == "__main__":
    main()
