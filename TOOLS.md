# TOOLS.md — Tool Inventory

> **WHAT I Can Execute — Layer 3 of the Agent OS Stack**
>
> This file declares available tools: MCP servers, CLI tools, and environment capabilities.

---

## 🖥️ Environment

| Property | Value |
|----------|-------|
| Platform | Linux (Ubuntu / Debian-based) |
| Shell | bash |
| Working directory | `/home/clay/dev` |
| Python | `python3` (3.11+) |
| Node.js | Available via `node` / `npx` |
| Package manager | `pnpm` (preferred), `npm`, `pip`, `uv` |

---

## 🔌 MCP Servers

MCP (Model Context Protocol) servers extend capabilities beyond file system access.

| Server | Config key | Purpose |
|--------|-----------|---------|
| **Filesystem** | `filesystem` | Read/write files within permitted directories |
| **Bash** | `bash` | Execute shell commands in persistent session |
| **Web search** | `exa` | Search web via Exa API |
| **Web fetch** | `webfetch` | Fetch and convert web pages to markdown |
| **Context7** | `context7` | Resolve library IDs, query official docs |
| **AST Grep** | `ast-grep` | Pattern-based code search and rewrite |
| **LSP** | `lsp` | Language server protocol operations |

### External MCP

**Prompts.chat MCP**: `https://prompts.chat/api/mcp` — Query role prompts by keyword

---

## 💻 CLI Tools

### Core Development

| Tool | Binary | Purpose |
|------|--------|---------|
| **git** | `git` | Version control |
| **jq** | `jq` | JSON query — INDEX.json search |
| **yq** | `yq` | YAML query |
| **python3** | `python3` | Python runtime with PyYAML |
| **node** | `node` | JavaScript runtime |
| **pnpm** | `pnpm` | Node package manager |
| **uv** | `uv` | Fast Python package installer |

### Documentation

| Tool | Binary | Purpose |
|------|--------|---------|
| **pandoc** | `pandoc` | Markdown ↔ PDF/DOCX/HTML |
| **mermaid-cli** | `mmdc` | Render Mermaid to PNG/SVG |

### Search

| Tool | Binary | Purpose |
|------|--------|---------|
| **ripgrep** | `rg` | Fast content search |
| **fd** | `fd` | Fast file finder |
| **fzf** | `fzf` | Fuzzy finder |

---

## 🗂️ Permitted Paths

| Path | Access | Purpose |
|------|--------|---------|
| `/home/clay/dev/` | Read/Write | All projects and repos |
| `/tmp/` | Read/Write | Temporary files |

> **Not permitted**: `/etc/`, `/usr/`, system paths. Ask if system-level access needed.

---

## 🔗 Stack Position

| Layer | File | Purpose |
|-------|------|---------|
| 1 — Identity | `SOUL.md` | WHO I am |
| 2 — Behavior | `AGENTS.md` | HOW I use tools |
| 4 — Knowledge | `skills/` | Technique and best practices |

---

_This file is environment-specific. Customize for your actual setup._
