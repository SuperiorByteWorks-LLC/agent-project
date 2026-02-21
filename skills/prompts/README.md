# Prompts — Role Activation Layer

> **This is not the `domain/` taxonomy tree.** Prompts are a distinct layer from skills.
>
> **Skills** = capability tools an agent uses (what it _does_)
> **Prompts** = role/persona activation frames (what it _is_ while working)
>
> The power is in combining them. See [Synergy Combos](#synergy-combos) below.

---

## What this directory contains

Curated, validated role-activation prompt templates sourced from:

- **prompts.chat** (f/prompts.chat) — 200+ community-validated system prompts, CC0 Public Domain[^1]
- Custom-authored templates adapted for our skill tree

These are battle-tested role persona prompts (e.g., "Act as a Cyber Security Specialist") that establish working context before skills load capabilities on top.

---

## How to use

### Step 1 — Pick a role prompt

Browse the catalog below or search:

```bash
# Find prompts tagged for developers
grep "TRUE" skills/prompts/catalog.csv | head -20

# Find prompts by keyword
grep -i "security" skills/prompts/catalog.csv
```

### Step 2 — Stack skills on top

Load the matching skill bundle after the role prompt activates:

| Role prompt | Recommended skill bundle |
|-------------|--------------------------|
| Cyber Security Specialist | `bundles/security-engineer.md` |
| Statistician | `domain/science/analysis/` |
| IT Architect | `domain/development/architecture/` |
| AI Writing Tutor / Academician | `bundles/scientist.md` |
| Developer Relations Consultant | `domain/development/` |
| Journal Reviewer | `domain/science/writing/` |

### Step 3 — Customize variables

Many prompts use `${Variable:Default}` syntax. Replace before using:

```
"I want you to act as an interviewer for the ${Position:Software Developer} position."
→
"I want you to act as an interviewer for the Machine Learning Engineer position."
```

---

## Synergy combos

The highest-value combinations — where a role prompt + skills create something greater than either alone:

### Security audit

```
Prompt:  "Cyber Security Specialist" (prompts.chat)
Skills:  canonical/ghost-repo-context + canonical/ghost-scan-code +
         canonical/ghost-scan-deps + canonical/ghost-scan-secrets
Result:  A security specialist with AI-powered SAST, SCA, and secret scanning
```

### Scientific manuscript review

```
Prompt:  "Journal Reviewer" (prompts.chat)
Skills:  canonical/scientific-writing + canonical/peer-review +
         canonical/citation-management
Result:  A journal reviewer that enforces CONSORT/STROBE and validates citations
```

### Architecture consultation

```
Prompt:  "IT Architect" (prompts.chat)
Skills:  canonical/senior-architect + canonical/markdown-mermaid-writing
Result:  An IT architect that produces C4 diagrams and ADR documents by default
```

### Statistical analysis

```
Prompt:  "Statistician" (prompts.chat)
Skills:  canonical/statistical-analysis + canonical/scientific-visualization
Result:  A statistician that produces properly-cited analysis with Mermaid charts
```

### Code education

```
Prompt:  "Instructor in a School" (prompts.chat, Python algorithms variant)
Skills:  canonical/python-patterns + canonical/test-driven-development
Result:  An instructor who teaches patterns with tests and ASCII visualizations
```

---

## MCP integration (live query)

prompts.chat ships an MCP server — query it directly for real-time access to the full 200+ prompt library without loading the CSV:

```json
{
  "mcpServers": {
    "prompts.chat": {
      "url": "https://prompts.chat/api/mcp"
    }
  }
}
```

Or via Claude Code plugin:
```
/plugin marketplace add f/prompts.chat
/plugin install prompts.chat@prompts.chat
```

The MCP approach is preferred over the static CSV when you need to search/filter at runtime.[^1]

---

## Catalog

`skills/prompts/catalog.csv` — the full prompts.chat dataset (CC0, updated periodically from upstream).

Columns: `act, prompt, for_devs, type, contributor`

- `for_devs=TRUE` — prompts especially useful in technical/development contexts
- `type=TEXT` — all current prompts are text format

Quick counts (from upstream as of 2026-02-20):
- Total prompts: ~200+
- Developer-relevant (`for_devs=TRUE`): ~40
- Contributors: 100+

---

## Contributing custom prompts

Custom prompts that aren't from upstream go in `skills/prompts/custom/` as markdown files:

```markdown
---
name: scientific-data-analyst
act: Scientific Data Analyst
source: original
license: Apache-2.0
skill-synergies:
  - canonical/statistical-analysis
  - canonical/scientific-visualization
  - canonical/agentic-data-scientist
tags: [science, data, analysis]
---

I want you to act as a scientific data analyst...
```

---

## 🔗 References

[^1]: f/prompts.chat — CC0 Public Domain, 146k stars: https://github.com/f/prompts.chat
     MCP server docs: https://prompts.chat/docs/api
     Claude plugin: https://github.com/f/prompts.chat/blob/main/CLAUDE-PLUGIN.md

- [SKILL-TREE.md](../../SKILL-TREE.md) — full design doc
- [skills/AGENTS.md](../AGENTS.md) — overall loading protocol
- [skills/bundles/](../bundles/) — role-based skill stacks to pair with prompts
