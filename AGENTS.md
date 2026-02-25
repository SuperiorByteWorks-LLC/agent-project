# AGENTS.md

> **You are an AI agent working in this repository.** This file is your entry point. Follow the instructions below before doing any work.

---

## Before you do anything

### 1. Read your operating instructions

Open **[agentic/instructions.md](agentic/instructions.md)** — it tells you what files to load, in what order, and based on what task type.

### 2. Before writing ANY documentation or diagrams

You **MUST** read and follow the style guides. These are not optional — they define formatting, structure, citations, accessibility, and visual standards for every document and diagram in this project.

| What you're creating       | Read FIRST                                                         | Then                                                                                                                                                      |
| -------------------------- | ------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Any `.md` file**         | [agentic/markdown_style_guide.md](agentic/markdown_style_guide.md) | Check [templates](agentic/markdown_templates/) for your doc type                                                                                          |
| **Any Mermaid diagram**    | [agentic/mermaid_style_guide.md](agentic/mermaid_style_guide.md)   | Open the [specific diagram type file](agentic/mermaid_diagrams/)                                                                                          |
| **A PR record**            | [agentic/markdown_style_guide.md](agentic/markdown_style_guide.md) | Use [PR template](agentic/markdown_templates/pull_request.md) → save to `docs/project/pr/`                                                                |
| **An issue record**        | [agentic/markdown_style_guide.md](agentic/markdown_style_guide.md) | Use [issue template](agentic/markdown_templates/issue.md) → save to `docs/project/issues/`                                                                |
| **A kanban board**         | [agentic/markdown_style_guide.md](agentic/markdown_style_guide.md) | Use [kanban template](agentic/markdown_templates/kanban.md) → save to `docs/project/kanban/`                                                              |
| **An ADR/decision record** | [agentic/markdown_style_guide.md](agentic/markdown_style_guide.md) | Use [decision template](agentic/markdown_templates/decision_record.md) → save to `agentic/adr/` (global) or subsystem `adr/` (for example `.crewai/adr/`) |

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
- **License and attribution are mandatory in redistributions** — this repo is Apache-2.0. Keep `LICENSE` and `NOTICE` when redistributing derivative works, and preserve attribution to Superior Byte Works, LLC / Clayton Young (Boreal Bytes).
- **No warranty / no liability** — do not add language in docs or code comments that contradicts Apache-2.0 warranty and liability disclaimers.
- **Example secret placeholders are acceptable** — `*.env.example` may contain clearly fake sample values; flag only real credential leakage or unsafe secret handling.
- **Run local CI before commit/push when possible** — run `./scripts/ci-local.sh` (or `./scripts/ci-local.sh --review` when review behavior changed) before committing/pushing unless the user explicitly says not to.
- **If local CI cannot run in this environment** (missing local secrets/tools, hosted remote runner), document the skip reason in PR/issue records and proceed with available checks.
- **Draft PR first** → design checkpoint → implement → code review → human marks Ready
- **PR records are files** in `docs/project/pr/pr-NNNNNNNN-short-description.md` — not GitHub UI data
- **GitHub PR body must contain only the full branch URL to the PR record file** (for example, `https://github.com/<org>/<repo>/blob/<branch>/docs/project/pr/pr-NNNNNNNN-short-description.md`)
- **Never** merge, deploy, access secrets, force-push, or approve your own PR

**Everything is Code:**

- PRs, issues, and kanban boards are **markdown files in `docs/`**, not data locked in GitHub's UI
- The file is the source of truth. GitHub is the comment/review layer.
- See [ADR-003](agentic/adr/ADR-003-everything-is-code.md) for the full rationale.

---

## Quick reference

| Need                                  | File                                                                                              |
| ------------------------------------- | ------------------------------------------------------------------------------------------------- |
| What can I do? What must I ask about? | [agentic/agentic_coding.md](agentic/agentic_coding.md)                                            |
| Step-by-step workflow                 | [agentic/workflow_guide.md](agentic/workflow_guide.md)                                            |
| Code style, commits, PRs              | [agentic/contribute_standards.md](agentic/contribute_standards.md)                                |
| Project-specific rules                | [agentic/custom-instructions.md](agentic/custom-instructions.md)                                  |
| Markdown formatting                   | [agentic/markdown_style_guide.md](agentic/markdown_style_guide.md)                                |
| Mermaid diagrams                      | [agentic/mermaid_style_guide.md](agentic/mermaid_style_guide.md)                                  |
| Document templates                    | [agentic/markdown_templates/](agentic/markdown_templates/)                                        |
| Diagram type guides                   | [agentic/mermaid_diagrams/](agentic/mermaid_diagrams/)                                            |
| System constraints                    | [agentic/operational_readiness.md](agentic/operational_readiness.md)                              |
| Token management                      | [agentic/context_budget_guide.md](agentic/context_budget_guide.md)                                |
| Error recovery                        | [agentic/agent_error_recovery.md](agentic/agent_error_recovery.md)                                |
| Idempotent script standards           | [agentic/idempotent_design_patterns.md](agentic/idempotent_design_patterns.md)                    |
| Local CI runner                       | [`scripts/ci-local.sh`](scripts/ci-local.sh)                                                      |
| License and attribution               | [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE)                                                       |
| File locations                        | [agentic/file_organization.md](agentic/file_organization.md)                                      |
| Architecture decisions                | [agentic/adr/](agentic/adr/) (global) + subsystem `adr/` directories (for example `.crewai/adr/`) |

---

## Directory overview

```text
agentic/                        → Agent instructions, style guides, templates, ADRs
docs/project/pr/                → Pull request records (pr-NNNNNNNN-short-description.md)
docs/project/issues/            → Issue records (issue-NNNNNNNN-short-description.md)
docs/project/kanban/            → Sprint/project boards ({scope}-{identifier}-short-description.md)
.crewai/adr/                    → CrewAI subsystem architecture decisions
apps/                           → Deployable apps (web, api, cli, mobile)
services/                       → Long-running backend services and workers
packages/                       → Shared libraries/modules across runtimes
data/sql/                       → SQL schemas, migrations, seed assets
notebooks/                      → Jupyter notebooks, prototypes, analysis
src/                            → Language-focused source workspace (Python-first)
src/ → Language-focused source workspace (Python-first)
skills/ → Agent Skills for agricultural data analysis (see below)
```

---

## Available Skills

This repository includes Agent Skills for agricultural data analysis. These skills provide high-level interfaces to common data sources and should be used by default when working with agricultural data.

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| **field-boundaries** | Access USDA field boundary data | When you need field polygons, crop boundaries, or field-level spatial analysis |
| **ssurgo-soil** | Access USDA NRCS SSURGO soil data | When analyzing soil conditions, pH, organic matter, texture, or drainage |
| **nasa-power-weather** | Access NASA POWER weather data | When you need historical weather, temperature, precipitation, or solar radiation |
| **cdl-cropland** | Access USDA Cropland Data Layer | When identifying crop types, analyzing land use, or studying crop rotations |
| **sentinel2-imagery** | Access Sentinel-2 satellite imagery | When analyzing crop health, NDVI, or vegetation indices |
| **landsat-imagery** | Access Landsat 8/9 satellite imagery | When analyzing long-term trends or historical field conditions |

### Using Skills

Skills are located in `skills/<skill-name>/` directories. Each skill contains:
- `SKILL.md` - Documentation and usage instructions
- `scripts/` - Python implementation

Import and use skills like this:

```python
from skills.field-boundaries.scripts.field_boundaries import FieldBoundariesSkill

skill = FieldBoundariesSkill()
fields = skill.download(count=50, regions=['corn_belt'])
```

**Note:** Skills are automatically discovered by compatible agents. When working with agricultural data, these skills provide the standard patterns and should be preferred over writing custom data access code.

---

## Repo entrypoint map

Use this map when a task is focused on one subsystem.

| Area                     | Start here                                                 | Why                                                           |
| ------------------------ | ---------------------------------------------------------- | ------------------------------------------------------------- |
| Core agent workflow      | [agentic/instructions.md](agentic/instructions.md)         | Required read order, escalation rules, and task-based loading |
| CrewAI review system     | [.crewai/README.md](.crewai/README.md)                     | Review architecture, crews, outputs, and local run model      |
| GitHub Actions/CI        | [.github/workflows/README.md](.github/workflows/README.md) | CI phases, reusable workflow layout, and troubleshooting      |
| App workspace            | [apps/README.md](apps/README.md)                           | Deployable app layout (`apps/web`, `apps/api`, etc.)          |
| Service workspace        | [services/README.md](services/README.md)                   | Background services/workers organization                      |
| Shared package workspace | [packages/README.md](packages/README.md)                   | Reusable library/module conventions                           |
| SQL/data workspace       | [data/sql/README.md](data/sql/README.md)                   | SQL schemas, migrations, and seed conventions                 |
| Language workspace       | [src/README.md](src/README.md)                             | Language-focused code organization                            |
| Notebook workspace       | [notebooks/README.md](notebooks/README.md)                 | Prototyping conventions and graduation path to `src/`         |

---

## Progress sync loop (mandatory)

Use this loop so humans can monitor work in real time from repo files.

1. **Before implementation starts**: update the active PR file, issue file(s), and kanban board with scope, plan, and `in progress` status.
2. **Before touching real implementation files**: ensure PR/issue/kanban reflect exactly what you are about to change and why.
3. **After each logical milestone** (not just at the end): update PR/issue/kanban with progress, decisions, blockers, and changed scope.
4. **Before running verification/tests**: update PR/issue/kanban with expected validation steps and current status, then run `./scripts/ci-local.sh` when local environment supports it.
5. **After verification/tests**: update PR/issue/kanban with pass/fail evidence and next actions.

Do not treat tracking files as end-of-task paperwork; they are live operational status for humans.

---

## Task completion gate (mandatory final step)

Before declaring any task complete, update the repo's source-of-truth records.

1. **Update PR record** in `docs/project/pr/pr-NNNNNNNN-short-description.md` to reflect what changed and what remains.
2. **Update issue record(s)** in `docs/project/issues/` when status, scope, root cause, or verification changes.
3. **Update kanban board** in `docs/project/kanban/` for movement across backlog/in-progress/review/done.
4. **Create or update ADRs** in the correct decision log when a change introduces a durable decision:
   - `agentic/adr/` for repo-wide or cross-subsystem decisions,
   - subsystem `adr/` directories for local implementation decisions (for example `.crewai/adr/`),
   - cross-cutting decisions discovered in a subsystem must also be mirrored in `agentic/adr/`.

If no ADR is needed, explicitly state `No ADR required` in the PR record rationale.

This enforces **single source of truth**: GitHub is the review surface; repository files are the authoritative record.

---

**Start here → [agentic/instructions.md](agentic/instructions.md)**
