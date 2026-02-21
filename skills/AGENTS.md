# Skills — Agent Loading Protocol

> **You are an agent reading this file.** This is the entry point for the skill tree. Read it once at session start, then follow the protocol below.

---

## What this skill tree is

A hierarchical repository of agent skills organized by domain. Skills live at exactly one canonical path (`canonical/<skill-name>/SKILL.md`). Everything else in this tree is navigation — directory listings and pointers.

Two invariants that never break:
1. **Zero content duplication** — a skill's content lives in exactly one place
2. **INDEX.json is always the grep target** — search it when you're uncertain; never load it whole

---

## Loading protocol

### If you know the domain

```
skills/domain/<domain>/README.md     ← read this (directory listing)
  → skills/domain/<domain>/<sub>/README.md   ← drill down if needed
    → skills/domain/<domain>/<sub>/<skill>.pointer.md   ← get canonical path
      → skills/canonical/<skill>/SKILL.md   ← load this
```

**Example:**
> I need a skill for writing scientific manuscripts.

1. Read `skills/domain/science/README.md` — see "writing" subdirectory listed
2. Read `skills/domain/science/writing/README.md` — see `scientific-writing` listed
3. Read `skills/domain/science/writing/scientific-writing.pointer.md` — get canonical path
4. Load `skills/canonical/scientific-writing/SKILL.md`

### If you are uncertain (grep the index)

```bash
# Find by tag
jq '.[] | select(.tags[] | contains("writing")) | {skill, canonical, description}' skills/INDEX.json

# Find by domain
jq '.[] | select(.domain[] | contains("science")) | .skill' skills/INDEX.json

# Find by keyword in description
jq '.[] | select(.description | ascii_downcase | contains("protein")) | {skill, canonical}' skills/INDEX.json

# List all high-frequency skills
jq '.[] | select(.load_frequency == "high") | .skill' skills/INDEX.json
```

The `canonical` field in the jq output gives you the exact path. Load that file.

### Core skills (always loaded — no action needed)

These load automatically at session start:

- `_core/alignment.md` — operating principles, values
- `_core/documentation.md` — links to formatting and diagram standards

---

## Domain map

| Domain | Subdirectories | Skill count | Focus |
|--------|---------------|-------------|-------|
| [science/](domain/science/README.md) | writing, analysis, databases, visualization | ~80 | Scientific research workflows |
| [development/](domain/development/README.md) | languages, frameworks, architecture, testing | ~40 | Software engineering |
| [security/](domain/security/README.md) | appsec, pentesting | ~10 | Application security |
| [data/](domain/data/README.md) | ml, analysis, visualization | ~20 | Data science |
| [documents/](domain/documents/README.md) | — | ~5 | Document production (PDF, DOCX, PPTX) |
| [research/](domain/research/README.md) | — | ~10 | Research tools (lit review, citations) |

## Prompts layer (separate from domain/)

`skills/prompts/` is a distinct layer — **role activation templates**, not skill capabilities.

| What | Where | Use it when |
|------|-------|-------------|
| Browse 200+ role prompts | [prompts/README.md](prompts/README.md) | You want to activate a persona before loading skills |
| Power combos | [prompts/README.md#synergy-combos](prompts/README.md#synergy-combos) | Prompt + skill stack for maximum alignment |
| Live query (MCP) | `https://prompts.chat/api/mcp` | Real-time search without loading the CSV |

**Pattern**: load a role prompt first, then load the matching skill bundle. The role prompt sets _what the agent is_; skills set _what it can do_.

---

## Bundle shortcuts

Bundles are pre-curated ordered loading sequences for common roles:

| Bundle | File | When to use |
|--------|------|-------------|
| Scientist | [bundles/scientist.md](bundles/scientist.md) | Scientific research, manuscript writing |
| Developer | [bundles/developer.md](bundles/developer.md) | Software engineering tasks |
| Security engineer | [bundles/security-engineer.md](bundles/security-engineer.md) | AppSec reviews, security audits |
| Data scientist | [bundles/data-scientist.md](bundles/data-scientist.md) | ML, data analysis, visualization |
| Writer | [bundles/writer.md](bundles/writer.md) | Documentation, technical writing |

---

## What NOT to do

- **Do not load `INDEX.json` into context** — it is grep-only
- **Do not load all skills in a domain** — load exactly what you need
- **Do not create new skill content in `domain/`** — all content goes to `canonical/`
- **Do not edit `INDEX.json` by hand** — run `scripts/build-index.sh` to regenerate

---

_See [SKILL-TREE.md](../SKILL-TREE.md) for the complete design document._
