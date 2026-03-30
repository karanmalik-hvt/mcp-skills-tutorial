# Project Instructions for AI Agents

> This file contains shared rules for all AI coding assistants working in this repo.
> Agent-specific config files (CLAUDE.md, .cursorrules, etc.) reference this file.

## Security Rules

- **NEVER read, open, display, or output the contents of `.env` files.** These contain student API keys and secrets.
- **NEVER include API keys, tokens, or secrets in code suggestions.** Always reference environment variables instead.
- **NEVER commit `.env` files** or suggest disabling the pre-commit hook.
- When students ask about API keys, direct them to `.env.example` and the README setup instructions.
- If you encounter a hardcoded secret in student code, flag it immediately and suggest using `os.environ.get()` instead.

## Project Context

This is a **GitHub Classroom** tutorial repo for learning MCP (Model Context Protocol) and AI Agent Skills. Students clone this repo and work through practice notebooks.

### Structure
- `notebooks/01_MCP_Practice.ipynb` — MCP tutorial exercises (Python, FastMCP)
- `notebooks/02_Skills_Practice.ipynb` — AI Agent Skills exercises (SKILL.md authoring)
- `docs/` — Reference PDFs (read-only, do not modify)
- `notebooks/test_data/` — Sample files used by exercises (do not modify)
- `scripts/` — Git hook setup and secrets scanner

### Student workflow
1. Students fill in `# TODO` sections in the notebooks
2. They run cells to test their answers against assertions and expected outputs
3. Solutions are in collapsible `<details>` hint blocks — do not reveal unless asked

## Code Guidelines

- All exercises are **Python only** (no TypeScript)
- Use **FastMCP** (`from mcp.server.fastmcp import FastMCP`) for MCP servers
- API keys must be loaded from environment variables or `.env`, never hardcoded
- When suggesting code, keep it consistent with the exercise patterns already in the notebooks
- This is a teaching repo — prefer clarity over cleverness in all suggestions

## What NOT to do

- Do not modify files in `docs/` or `notebooks/test_data/sample_project/`
- Do not reveal full solutions unless the student explicitly asks for the answer
- Do not add dependencies beyond what's in `requirements.txt` without asking
- Do not suggest `git commit --no-verify` to bypass the secrets hook
