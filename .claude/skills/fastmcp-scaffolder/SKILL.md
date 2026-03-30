---
name: fastmcp-scaffolder
description: >
  Generate correct Python MCP server boilerplate using the FastMCP SDK.
  Produces properly structured servers with tools, resources, and prompts
  including type hints, docstrings, safe_path() security, and logging best practices.
  Use when creating a new MCP server, scaffolding FastMCP tools, or when the user
  asks to "build an MCP server" or "create a tool".
  Do NOT use for TypeScript/Node.js MCP servers or for editing existing servers.
license: Proprietary
metadata:
  author: hexaview-ai-team
  version: "1.0"
  skill-type: creation
---

# FastMCP Server Scaffolder

## When to use this skill
Activate when:
- User asks to "create an MCP server" or "build a new server"
- User asks to "scaffold a tool" or "generate MCP boilerplate"
- User needs a new FastMCP server from scratch
- User is working on MCP exercises and needs a starting point

Do NOT use when:
- The user wants a TypeScript/Node.js server (different SDK entirely)
- The user wants to modify an existing server (just edit it directly)
- The user asks about MCP concepts without needing code

## How to generate a server

### Step 1: Gather requirements
Ask the user (or infer from context):
1. Server name (lowercase-with-hyphens)
2. What tools it needs (actions the AI can perform)
3. What resources it needs (data the AI can read)
4. What prompts it needs (reusable templates)
5. Whether it needs file system access (triggers safe_path pattern)
6. Transport: stdio (default/local) or HTTP+SSE (remote)

### Step 2: Generate using the template
Use `assets/server-template.py` as the base. Fill in:
- Server name
- Tool functions with type hints and docstrings
- Resource functions with URIs
- Prompt functions
- safe_path() if file access is needed
- Correct transport in the `if __name__` block

### Step 3: Apply these rules (NEVER skip)
1. **Every tool function** must have:
   - Type hints on all parameters AND return type
   - A docstring (this becomes the tool description the AI reads)
   - Error handling that returns error text (not raises exceptions)
2. **NEVER use print()** — use `logging.info()` or `logging.error()` instead.
   The stdio channel is reserved for MCP protocol messages. Any print() call
   will corrupt the stream and crash the connection.
3. **File access tools MUST include safe_path()** — validates that requested
   paths stay within ALLOWED_ROOT. Without this, an AI could read /etc/passwd
   or private keys.
4. **Wrap tool logic in try/except** and return errors as text content, not
   exceptions. This lets the AI read and explain the error to the user.

## Output format

ALWAYS generate servers following the template in `assets/server-template.py`.

Key structure:
```python
# Imports
from mcp.server.fastmcp import FastMCP
import logging

# Logging (NEVER print)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

# Server
mcp = FastMCP("server-name")

# Tools with @mcp.tool()
# Resources with @mcp.resource("uri://...")
# Prompts with @mcp.prompt()

# Entry point
if __name__ == "__main__":
    mcp.run()  # stdio by default
```

## Gotchas
- `print()` with stdio transport is the #1 cause of "connection crashed" errors.
  Use `logging.info()` which writes to stderr, not stdout.
- Type hints are NOT optional — FastMCP uses them to auto-generate the JSON schema.
  Without hints, the AI won't know what arguments to send.
- Docstrings are NOT optional — they become the tool description. Without a docstring,
  the AI has no idea what the tool does and will skip it.
- `safe_path()` must use `str(resolved).startswith(str(ALLOWED_ROOT))` — do NOT use
  `Path.is_relative_to()` as it behaves differently on Windows.
- The `@mcp.resource()` decorator takes a URI string argument, unlike `@mcp.tool()`
  and `@mcp.prompt()` which take no arguments.
- For HTTP+SSE transport, change `mcp.run()` to `mcp.run(transport="sse", host="0.0.0.0", port=3000)`.
