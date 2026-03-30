# Claude Code — Project Instructions

> Full shared rules are in [AGENTS.md](AGENTS.md). This file adds Claude Code-specific settings.

## Security Rules

- **NEVER read, open, display, or output the contents of `.env` files.** These contain student API keys.
- **NEVER include API keys, tokens, or secrets in code suggestions.** Use `os.environ.get()` instead.
- **NEVER commit `.env` files** or suggest disabling the pre-commit hook.
- When students ask about API keys, point them to `.env.example` and README.
- If you see a hardcoded secret, flag it immediately.

## Project Context

GitHub Classroom tutorial repo — MCP and AI Agent Skills.
See [AGENTS.md](AGENTS.md) for full project context, structure, and code guidelines.

## Claude Code Specific

- Do not add or modify `CLAUDE.md` unless asked.
- Read `AGENTS.md` for the complete list of rules before making any changes to this repo.
