# AGENTS.md

> **You are an AI agent working in this repository.** This file is your entry point. Follow the instructions below before doing any work.

---

## Before you do anything

### 0. Load the Agent OS stack (do this first, always)

This repo uses a 5-layer Agent OS stack. Load in this order:

| # | File | What it is | Always load? |
|---|------|-----------|-------------|
| 1 | [`SOUL.md`](SOUL.md) | WHO you are — identity and values | ✅ Yes |
| 2 | `AGENTS.md` (this file) | HOW you work — behavioral rules | ✅ Yes (you're reading it) |
| 3 | [`TOOLS.md`](TOOLS.md) | WHAT you can execute — tool inventory | ✅ Yes |
| 4 | [`skills/_core/`](skills/_core/) | Foundation alignment + docs standard | ✅ Yes |
| 5 | [`skills/`](skills/) | What you know — on-demand by task | On demand |

Full stack design: **[`AGENT-OS.md`](AGENT-OS.md)**

### 1. Read your operating instructions

Open **[agentic/instructions.md](agentic/instructions.md)** — it tells you what files to load, in what order, and based on what task type.

### 2. Before writing ANY documentation or diagrams

You **MUST** read and follow the style guides. These are not optional — they define formatting, structure, citations, accessibility, and visual standards for every document and diagram in this project.

| What you're creating       | Read FIRST                                                         | Then                                                                                            |
| -------------------------- | ------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------- |
| **Any `.md` file**         | [agentic/markdown_style_guide.md](agentic/markdown_style_guide.md) | Check [templates](agentic/markdown_templates/) for your doc type                                |
| **Any Mermaid diagram**    | [agentic/mermaid_style_guide.md](agentic/mermaid_style_guide.md)   | Open the [specific diagram type file](agentic/mermaid_diagrams/)                                |
| **A PR record**            | [agentic/markdown_style_guide.md](agentic/markdown_style_guide.md) | Use [PR template](agentic/markdown_templates/pull_request.md) → save to `docs/pr/`              |
| **An issue record**        | [agentic/markdown_style_guide.md](agentic/markdown_style_guide.md) | Use [issue template](agentic/markdown_templates/issue.md) → save to `docs/issues/`              |
| **A kanban board**         | [agentic/markdown_style_guide.md](agentic/markdown_style_guide.md) | Use [kanban template](agentic/markdown_templates/kanban.md) → save to `docs/kanban/`            |
| **An ADR/decision record** | [agentic/markdown_style_guide.md](agentic/markdown_style_guide.md) | Use [decision template](agentic/markdown_templates/decision_record.md) → save to `agentic/adr/` |

### 3. Key rules you must follow

**Documentation:**

- **One H1 per document.** Emoji on H2 headings only (one per H2). No emoji on H3/H4. No H5+.
- **Cite everything.** Every external claim gets a footnote citation with full URL.
- **Diagrams over prose.** If content describes flow, structure, or relationships — add a Mermaid diagram.
- **`accTitle` + `accDescr`** on every Mermaid diagram. `classDef` color classes only — no inline `style`, no `%%{init}`.
- **Horizontal rule after every `</details>` block.**

**Code:**

- **Scoped Conventional Commits** for all commit messages — `type(scope): description` (e.g., `feat(auth): add OAuth2 flow`, `fix(api): handle timeout`). Scope is strongly recommended; see [contribute_standards.md](agentic/contribute_standards.md) for full format including body, footers, and breaking change conventions.
- **Multi-line commit bodies are required** for non-trivial changes. The body must explain **why** the change was made, **what** key files were touched, and **how** behavior differs. The commit history is the authoritative record of the project — someone reading `git log` alone should fully understand every change.
- **Draft PR first** → design checkpoint → implement → code review → human marks Ready
- **PR records are files** in `docs/pr/pr-NNNNNNNN.md` — not GitHub UI data
- **Never** merge, deploy, access secrets, force-push, or approve your own PR

**Everything is Code:**

- PRs, issues, and kanban boards are **markdown files in `docs/`**, not data locked in GitHub's UI
- The file is the source of truth. GitHub is the comment/review layer.
- See [ADR-003](agentic/adr/ADR-003-everything-is-code.md) for the full rationale.

---

## Quick reference

| Need                                  | File                                                                           |
| ------------------------------------- | ------------------------------------------------------------------------------ |
| Full stack design (5 layers)          | [AGENT-OS.md](AGENT-OS.md)                                                     |
| Who I am / my values | [SOUL.md](SOUL.md) |
| What tools I can use | [TOOLS.md](TOOLS.md) |
| Skill tree navigation                 | [skills/AGENTS.md](skills/AGENTS.md)                                           |
| What can I do? What must I ask about? | [agentic/agentic_coding.md](agentic/agentic_coding.md)                         |
| Step-by-step workflow                 | [agentic/workflow_guide.md](agentic/workflow_guide.md)                         |
| Code style, commits, PRs              | [agentic/contribute_standards.md](agentic/contribute_standards.md)             |
| Project-specific rules                | [agentic/custom-instructions.md](agentic/custom-instructions.md)               |
| Markdown formatting                   | [agentic/markdown_style_guide.md](agentic/markdown_style_guide.md)             |
| Mermaid diagrams                      | [agentic/mermaid_style_guide.md](agentic/mermaid_style_guide.md)               |
| Document templates                    | [agentic/markdown_templates/](agentic/markdown_templates/)                     |
| Diagram type guides                   | [agentic/mermaid_diagrams/](agentic/mermaid_diagrams/)                         |
| System constraints                    | [agentic/operational_readiness.md](agentic/operational_readiness.md)           |
| Token management                      | [agentic/context_budget_guide.md](agentic/context_budget_guide.md)             |
| Error recovery                        | [agentic/agent_error_recovery.md](agentic/agent_error_recovery.md)             |
| Idempotent script standards           | [agentic/idempotent_design_patterns.md](agentic/idempotent_design_patterns.md) |
| File locations                        | [agentic/file_organization.md](agentic/file_organization.md)                   |
| Architecture decisions                | [agentic/adr/](agentic/adr/)                                                   |

---

## Directory overview

```text
soul.md                         → Layer 1: Agent identity and values (WHO)
AGENTS.md                       → Layer 2: Behavioral rules (HOW) ← you are here
tools.md                        → Layer 3: Tool inventory (WHAT can execute)
AGENT-OS.md                     → Full 5-layer stack design
SKILL-TREE.md                   → Skill tree architecture design
skills/                         → Layer 4+5: Knowledge and persona (on-demand)
agentic/                        → Agent instructions, style guides, templates, ADRs
docs/pr/                        → Pull request records (pr-NNNNNNNN.md)
docs/issues/                    → Issue records (issue-NNNNNNNN.md)
docs/kanban/                    → Sprint/project boards
notebooks/                      → Jupyter notebooks, prototypes, analysis
src/                            → Python apps, libraries, and utilities
```

---

**Start here → [agentic/instructions.md](agentic/instructions.md)**
