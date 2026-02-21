# Prompts — Agent Loading Protocol

> **You are an agent reading this file.** This is the entry point for the prompt tree. Read it once at session start, then follow the protocol below.

---

## What this prompt tree is

A hierarchical repository of agent prompts organized by domain. Prompts live at exactly one canonical path (`canonical/<source>/<prompt-name>/PROMPT.md`). Everything else in this tree is navigation — directory listings and pointers.

Two invariants that never break:

1. **Zero content duplication** — a prompt's content lives in exactly one place
2. **INDEX.json is always the grep target** — search it when you're uncertain; never load it whole

---

## Loading protocol

### If you know the domain

```
prompts/domain/<domain>/README.md ← read this (directory listing)
→ prompts/domain/<domain>/<sub>/README.md ← drill down if needed
→ prompts/domain/<domain>/<sub>/<prompt>.pointer.md ← get canonical path
→ prompts/canonical/<source>/<prompt>/PROMPT.md ← load this
```

**Example:**

> I need a prompt for code review.

1. Read `prompts/domain/development/README.md` — see "code-review" subdirectory listed
2. Read `prompts/domain/development/code-review/README.md` — see `expert-code-reviewer` listed
3. Read `prompts/domain/development/code-review/expert-code-reviewer.pointer.md` — get canonical path
4. Load `prompts/canonical/imported/prompts-chat/expert-code-reviewer/PROMPT.md`

### If you are uncertain (grep the index)

```bash
# Find by tag
jq '.[] | select(.tags[] | contains("code-review")) | {prompt, canonical, description}' prompts/INDEX.json

# Find by domain
jq '.[] | select(.domain[] | contains("development")) | .prompt' prompts/INDEX.json

# Find by keyword in description
jq '.[] | select(.description | ascii_downcase | contains("debugging")) | {prompt, canonical}' prompts/INDEX.json
```

The `canonical` field in the jq output gives you the exact path. Load that file.

### Core prompts (always loaded — no action needed)

These load automatically at session start:

- `_core/alignment.md` — operating principles, values
- `_core/documentation.md` — links to formatting and standards

---

## Domain map

| Domain                                       | Subdirectories                        | Prompt count | Focus                        |
| -------------------------------------------- | ------------------------------------- | ------------ | ---------------------------- |
| [science/](domain/science/README.md)         | research, writing, analysis           | ~150         | Scientific research prompts  |
| [development/](domain/development/README.md) | coding, debugging, architecture       | ~300         | Software engineering prompts |
| [security/](domain/security/README.md)       | pentesting, audit, compliance         | ~100         | Security prompts             |
| [data/](domain/data/README.md)               | analysis, visualization, ml           | ~150         | Data science prompts         |
| [documents/](domain/documents/README.md)     | writing, editing, formatting          | ~100         | Document prompts             |
| [research/](domain/research/README.md)       | literature, citations, synthesis      | ~100         | Research prompts             |
| [general/](domain/general/README.md)         | brainstorming, planning, productivity | ~100         | General purpose prompts      |

## Prompt Jail

Prompts with policy violations (promotional content, forced behavior, etc.) are quarantined in `prompt-jail/`.

See [prompt-jail/README.md](prompt-jail/README.md) for details.

---

## What NOT to do

- **Do not load `INDEX.json` into context** — it is grep-only
- **Do not load all prompts in a domain** — load exactly what you need
- **Do not create new prompt content in `domain/`** — all content goes to `canonical/`
- **Do not edit `INDEX.json` by hand** — run `scripts/build-prompt-index.sh` to regenerate

---

_See [PROMPT-TREE.md](../PROMPT-TREE.md) for the complete design document._
