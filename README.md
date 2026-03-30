# MCP & AI Agent Skills — Practice Tutorial

**Hexaview Technologies | AI Engineering Series**

Hands-on practice notebooks for learning **Model Context Protocol (MCP)** and **AI Agent Skills** — two foundational technologies for building tool-using AI agents.

## What You'll Learn

| Notebook | Topics | Time |
|----------|--------|------|
| **01 — MCP Practice** | Build MCP servers in Python (FastMCP), tools/resources/prompts, file explorer with security, HTTP+SSE transport, LLM integration | ~4-5 hrs |
| **02 — Skills Practice** | SKILL.md format & validation, description quality, Creation/Automation/MCP Enhancement skills, progressive disclosure, MCP+Skills capstone | ~4-5 hrs |

Both notebooks are completable in **one day**.

## Prerequisites

- Python 3.10+
- Basic Python knowledge
- No prior MCP or Skills experience required
- (Optional) OpenAI API key — only needed for the bonus exercise in Notebook 1

## Getting Started

### 1. Clone the repo

```bash
git clone <repo-url>
cd mcp-skills-tutorial
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your OpenAI API key (only needed for Bonus Exercise 8)
# The .env file is gitignored — your key will never be committed
```

> **Important:** NEVER hardcode API keys in notebooks or Python files. Always load them from the `.env` file using `os.environ.get("OPENAI_API_KEY")`. The pre-commit hook will block any commit containing leaked keys.

### 5. Install git hooks (required)

```bash
python scripts/setup_hooks.py
```

This installs a **pre-commit hook** that:
- Blocks `.env` files from being accidentally committed
- Scans all staged files for API key patterns (OpenAI, AWS, GitHub, Slack, Google, private keys)
- Rejects the commit if any secrets are detected

### 6. Launch Jupyter

```bash
jupyter notebook notebooks/
```

## Repository Structure

```
mcp-skills-tutorial/
├── README.md
├── requirements.txt
├── .env.example                          # Template — copy to .env and fill in
├── .env                                  # Your secrets (gitignored, never committed)
├── .gitignore
│
├── AGENTS.md                             # Shared AI agent rules (all agents read this)
├── CLAUDE.md                             # Claude Code project config
├── .cursorrules                          # Cursor project config
├── .windsurfrules                        # Windsurf (Codeium) project config
├── .github/
│   └── copilot-instructions.md           # GitHub Copilot project config
├── .antigravity/
│   └── instructions.md                   # Antigravity project config
│
├── scripts/
│   ├── setup_hooks.py                    # Installs git pre-commit hook
│   └── pre-commit-secrets-scan.sh        # Scans for leaked API keys
├── docs/
│   ├── MCP_Tutorial_Hexaview.pdf         # Reference tutorial — MCP
│   └── AI_Agent_Skills_Hexaview.pdf      # Reference tutorial — Skills
└── notebooks/
    ├── 01_MCP_Practice.ipynb             # MCP practice notebook
    ├── 02_Skills_Practice.ipynb          # Skills practice notebook
    └── test_data/
        └── sample_project/              # Sample files for file explorer exercise
            ├── README.md
            ├── src/
            │   ├── main.py
            │   └── utils.py
            └── docs/
                └── guide.txt
```

## How the Notebooks Work

- Each exercise has **skeleton code** with `# TODO` comments — fill them in
- Expand the **Hint** dropdowns if you get stuck (click the triangle)
- Compare your output against the **Expected Output** sections
- Exercises are progressive — complete them in order
- Assertions verify your answers where possible

## Exercise Overview

### Notebook 1: MCP Practice

| # | Exercise | Difficulty | Key Concept |
|---|----------|-----------|-------------|
| 1 | Conceptual Understanding | Easy | MCP architecture, primitives |
| 2 | Greeter Server | Easy | `@mcp.tool()`, type hints, docstrings |
| 3 | Adding Resources | Easy | `@mcp.resource()`, URIs |
| 4 | Adding Prompts | Easy | `@mcp.prompt()`, templates |
| 5 | File Explorer | Medium | `safe_path()` security, real-world server |
| 6 | Task Manager | Medium | Multi-tool server from scratch |
| 7 | HTTP+SSE Transport | Easy | Remote deployment configuration |
| 8 | LLM Integration (Bonus) | Hard | OpenAI function calling + MCP bridge |

### Notebook 2: Skills Practice

| # | Exercise | Difficulty | Key Concept |
|---|----------|-----------|-------------|
| 1 | Conceptual Understanding | Easy | Skills lifecycle, types |
| 2 | Frontmatter Validator | Medium | SKILL.md spec rules, regex validation |
| 3 | Write Your First SKILL.md | Medium | Frontmatter, body structure, triggers |
| 4 | Description Quality Scorer | Medium | Activation triggers, keyword analysis |
| 5 | Creation Skill | Medium | Output templates, assets, references |
| 6 | Automation Skill | Hard | Plan-Validate-Execute, validation scripts |
| 7 | Progressive Disclosure | Medium | Refactoring, token budget management |
| 8 | MCP + Skills Capstone | Hard | MCP Enhancement Skill design |

## Reference Materials

The `docs/` folder contains the full tutorial PDFs. Use them as reference while working through the exercises:

- **MCP Tutorial** — Covers what MCP is, how it works, building servers in Python and TypeScript, transport layers, debugging
- **Skills Tutorial** — Covers what Skills are, the SKILL.md format, skill types, building and testing skills, progressive disclosure

## Security

This repo includes multiple layers of protection against accidental secret exposure:

| Layer | What it does |
|-------|-------------|
| `.gitignore` | Prevents `.env`, `.key`, `.pem` files from being tracked by git |
| **Pre-commit hook** | Scans every commit for API key patterns and blocks if found |
| **AI agent configs** | Instructs all AI assistants to never read `.env` files (see table below) |
| `.env.example` | Provides a safe template so students never hardcode keys |

### AI agent configuration (agent-agnostic)

All agent rules live in a shared `AGENTS.md` file. Each agent also has its own config that references it:

| Agent | Config file | Reads from |
|-------|------------|------------|
| Claude Code | `CLAUDE.md` | `AGENTS.md` |
| Cursor | `.cursorrules` | `AGENTS.md` |
| GitHub Copilot | `.github/copilot-instructions.md` | `AGENTS.md` |
| Windsurf (Codeium) | `.windsurfrules` | `AGENTS.md` |
| Antigravity | `.antigravity/instructions.md` | `AGENTS.md` |

To add support for a new agent, create its config file and have it reference `AGENTS.md`.

### API key patterns detected by the pre-commit hook

- OpenAI keys (`sk-...`, `sk-proj-...`)
- Anthropic keys (`sk-ant-...`)
- AWS Access Key IDs (`AKIA...`)
- GitHub tokens (`ghp_...`, `gho_...`)
- Slack tokens (`xox...`)
- Google API keys (`AIza...`)
- Private keys (`-----BEGIN PRIVATE KEY`)

### If the hook blocks your commit

1. Remove the secret from the file
2. Use `os.environ.get("KEY_NAME")` and put the value in `.env`
3. If it's a false positive: `git commit --no-verify` (use sparingly)

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: mcp` | Run `pip install mcp` |
| `ModuleNotFoundError: yaml` | Run `pip install pyyaml` |
| Notebook kernel not found | Select your virtual environment as the kernel |
| OpenAI exercises fail | Add your key to `.env` file (see step 4 above), or skip (it's optional) |
| Pre-commit hook not running | Run `python scripts/setup_hooks.py` to reinstall |
| Commit blocked by secrets scan | Remove the secret and use `.env` instead (see Security section) |

## License

Internal learning material — Hexaview Technologies.
