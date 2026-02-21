# Prompt Tree — Hierarchical Prompt Repository

> **This is the canonical design document for the `prompts` directory.**

---

## What This Is

A personal prompt repository organized like the Yahoo Directory with three navigation mechanisms:

1. **Yahoo Directory navigation** — agents drill down through a category tree to reach exactly the prompt they need
2. **Grep-index fallback** — `prompts/INDEX.json` is always the fast path when the domain is uncertain
3. **Pointer-based SSoT** — every prompt lives at exactly one canonical path; taxonomy nodes are navigation aids with zero content

The target: 1000+ prompts, all findable in under 3 seconds, none ever duplicated.

---

## Directory Map

```
prompts/
├── AGENTS.md              ← YOU ARE HERE if you're an agent. Read this first.
├── INDEX.json             ← Machine-generated. Grep this when uncertain.
├── CATALOG.md             ← Human-readable. Browse by domain.
│
├── canonical/             ← SSoT location for all prompt content
│   ├── imported/         ← Prompts imported from external sources
│   │   └── prompts-chat/  ← From prompts.chat
│   └── manual/           ← Hand-written prompts
│
├── domain/              ← Navigation tree. Pointers and READMEs only.
│   ├── science/
│   │   ├── README.md
│   │   └── research/
│   │       ├── README.md
│   │       └── systematic-review.pointer.md
│   ├── development/
│   │   ├── README.md
│   │   ├── debugging/
│   │   ├── code-review/
│   │   └── architecture/
│   ├── security/
│   ├── data/
│   ├── documents/
│   ├── research/
│   └── general/
│
└── prompt-jail/         ← Quarantine for prompts with violations
    ├── README.md
    ├── quarantined/
    ├── blocked/
    ├── review-pending/
    └── cleaned/
```

---

## Loading Protocol

### If you know the domain

```
prompts/domain/<domain>/README.md ← read this
→ prompts/domain/<domain>/<sub>/README.md ← drill down
→ prompts/domain/<domain>/<sub>/<prompt>.pointer.md ← get path
→ prompts/canonical/<source>/<prompt>/PROMPT.md ← load this
```

**Example:**

> I need a prompt for debugging Python.

1. Read `prompts/domain/development/README.md` — see "debugging" subdirectory
2. Read `prompts/domain/development/debugging/README.md` — see `python-debugging-expert`
3. Read pointer — get `prompts/canonical/imported/prompts-chat/python-debugging-expert/PROMPT.md`
4. Load that file

### If you are uncertain (grep the index)

```bash
# Find by tag
jq '.[] | select(.tags[] | contains("debugging")) | {prompt, canonical}' prompts/INDEX.json

# Find by domain
jq '.[] | select(.domain == "development") | .prompt' prompts/INDEX.json

# Find by keyword
jq '.[] | select(.description | ascii_downcase | contains("python")) | {prompt, canonical}' prompts/INDEX.json
```

---

## Three Invariants

1. **One canonical path per prompt** — never duplicated
2. **Taxonomy nodes contain pointers only** — never content
3. **INDEX.json is machine-generated** — always the grep target

---

## Import Strategy

All prompts from prompts.chat and other sources are imported to `canonical/imported/<source>/`.

Before promotion to active use:

1. Scan for violations (promotional content, forced behavior)
2. Quarantine if violations found
3. Clean and approve
4. Move to `canonical/imported/<source>/`

---

## Prompt Jail

Prompts with policy violations are quarantined in `prompt-jail/`.

See [prompt-jail/README.md](prompt-jail/README.md) for details.

---

## Tools

- `scripts/import-prompts.sh` — Import from prompts.chat
- `scripts/prompt-scanner.py` — Detect violations
- `scripts/build-prompt-index.sh` — Regenerate INDEX.json

---

## Standards

See [docs/standards/jail-systems.md](docs/standards/jail-systems.md) for:

- Directory structure standards
- Quarantine workflow
- Violation categories
- File naming conventions

---

_Last updated: 2026-02-21_
