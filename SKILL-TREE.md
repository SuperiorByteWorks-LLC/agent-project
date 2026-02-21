# SKILL-TREE — Hierarchical Skill Repository Design

> **This is the canonical design document for the `agents-skills-tree` project.** Agents and humans working on this repo read this first. It defines the loading protocol, pointer format, index schema, inheritance model, and import strategy.

---

## 🗺️ What This Is

A personal skill repository that supercharges any AI agent platform through three mechanisms:

1. **Yahoo Directory navigation** — agents drill down through a category tree to reach exactly the skill they need, loading no extra context
2. **Grep-index fallback** — `skills/INDEX.json` is always the fast path when the domain is uncertain; search it with `jq` or `grep` in milliseconds
3. **Pointer-based SSoT** — every skill lives at exactly one canonical path; taxonomy nodes are navigation aids with zero content

The target: 500–1000 skills, all findable in under 3 seconds, none ever duplicated.

---

## 🧭 Directory Map

```
skills/
├── AGENTS.md              ← YOU ARE HERE if you're an agent. Read this first.
├── INDEX.json             ← Machine-generated. Grep this when uncertain.
├── CATALOG.md             ← Human-readable. Browse by domain.
│
├── _core/                 ← Always-loaded foundation (alignment + docs)
│   ├── alignment.md       ← Core values, operating principles
│   └── documentation.md   ← Points to canonical/markdown-mermaid-writing/
│
├── canonical/             ← ALL skill content lives here. SSoT.
│   ├── <skill-name>/
│   │   ├── SKILL.md       ← The skill (YAML frontmatter + content)
│   │   └── ...            ← Any skill-specific assets (refs, templates)
│   └── ...
│
├── domain/                ← Navigation tree. Pointers and READMEs only.
│   ├── science/
│   │   ├── README.md      ← Directory listing: what lives here
│   │   ├── writing/
│   │   │   ├── README.md
│   │   │   ├── scientific-writing.pointer.md
│   │   │   └── markdown-mermaid-writing.pointer.md
│   │   ├── analysis/
│   │   │   ├── README.md
│   │   │   └── statistical-analysis.pointer.md
│   │   └── databases/
│   │       ├── README.md
│   │       └── pubmed.pointer.md
│   ├── development/
│   │   ├── README.md
│   │   ├── languages/
│   │   │   ├── python.pointer.md
│   │   │   ├── typescript-expert.pointer.md
│   │   │   └── go.pointer.md
│   │   ├── frameworks/
│   │   │   └── react-patterns.pointer.md
│   │   ├── architecture/
│   │   │   └── senior-architect.pointer.md
│   │   └── testing/
│   │       └── test-driven-development.pointer.md
│   ├── security/
│   │   ├── README.md
│   │   ├── appsec/
│   │   │   ├── ghost-scan-code.pointer.md
│   │   │   ├── ghost-scan-deps.pointer.md
│   │   │   └── ghost-scan-secrets.pointer.md
│   │   └── pentesting/
│   │       └── ...
│   ├── data/
│   │   ├── README.md
│   │   ├── ml/
│   │   ├── analysis/
│   │   └── visualization/
│   ├── documents/
│   │   ├── README.md
│   │   ├── pdf.pointer.md
│   │   ├── docx.pointer.md
│   │   └── pptx.pointer.md
│   └── research/
│       ├── README.md
│       ├── literature-review.pointer.md
│       ├── citation-management.pointer.md
│       └── hypothesis-generation.pointer.md
│
├── bundles/               ← Role-based ordered pointer lists. No content.
│   ├── scientist.md
│   ├── developer.md
│   ├── security-engineer.md
│   ├── data-scientist.md
│   └── writer.md
│
└── prompts/               ← Persona layer. Role activation templates, NOT skills.
    ├── README.md          ← Usage guide, synergy combos, MCP integration
    ├── catalog.csv        ← prompts.chat full dataset (CC0, periodically updated)
    └── custom/            ← Original prompts with skill-synergies frontmatter
```

---

## 🤖 Loading Protocol (for agents)

### Path 1 — You know the domain

1. Read `skills/domain/<domain>/README.md` — this is the "Yahoo directory page" for that domain
2. Navigate down the subtree if needed: read the subdomain README
3. Find the `.pointer.md` file for the skill you want
4. Read the `canonical:` field from the pointer frontmatter
5. Load `<canonical-path>/SKILL.md`

**Token cost**: 2–3 small README files + 1 pointer file + 1 SKILL.md. Total: ~5–15KB depending on skill depth.

### Path 2 — You're uncertain (grep the index)

```bash
# Find all skills tagged "writing"
jq '.[] | select(.tags[] | contains("writing")) | {skill, canonical, description}' skills/INDEX.json

# Find skills in the science domain
jq '.[] | select(.domain[] | contains("science"))' skills/INDEX.json

# Full-text search by description keyword
jq '.[] | select(.description | contains("protein"))' skills/INDEX.json

# Find all high-frequency skills
jq '.[] | select(.load_frequency == "high") | .skill' skills/INDEX.json
```

**Token cost**: Zero — `INDEX.json` is grep-only, never loaded into context. The jq output gives you the canonical path, then you load that one file.

### Path 3 — Core skills (always loaded)

`skills/_core/` loads automatically at session start. These are:

- `alignment.md` — core values and operating principles that apply to all work
- `documentation.md` — pointer to the markdown-mermaid-writing canonical skill (formatting foundation)

You do not need to explicitly load core skills. They are the implicit inheritance root.

---

## 📌 Pointer File Format

Every taxonomy leaf is a `.pointer.md` file. Strict format — no exceptions:

```markdown
---
skill: <skill-name>
canonical: <relative-path-from-skills-root>/SKILL.md
description: >
  One to three sentences describing what this skill does and when to use it.
  This is the text that appears in domain README listings.
tags: [tag1, tag2, tag3]
domain: [primary/domain, optional/secondary/domain]
upstream: <source-repo-url>
license: <SPDX-identifier>
load_frequency: high | medium | low
---
```

**Rules:**
- No prose below the frontmatter. The `---` closing the frontmatter is the end of the file.
- `canonical` is always relative to `skills/` root, using `../` to navigate up from the pointer's location
- `tags` must include at minimum the primary domain name (e.g., `science`)
- `load_frequency` is set by the maintainer based on observed usage; defaults to `medium`

---

## 📄 SKILL.md Canonical Format

Skills in `skills/canonical/<skill-name>/SKILL.md` use this frontmatter:

```yaml
---
name: <skill-name>
description: >
  Detailed description of what the skill provides and when to load it.
  This is the text loaded into agent context.
allowed-tools: [Read, Write, Edit, Bash, ...]
license: <SPDX-identifier>
metadata:
  skill-author: <Original author>
  skill-source: <upstream repo URL or "original">
  skill-version: "1.0.0"
  imported-from: <upstream repo URL if imported>
  import-date: <YYYY-MM-DD>
  skill-contributors:
    - name: <name>
      org: <org>
      role: <Author | Importer | Contributor>
---

# <Skill Title>

<skill content>
```

**Attribution rule**: If imported from an upstream repo, `imported-from` and `import-date` are required. The original `skill-author` and `skill-source` are preserved unchanged. Adding import metadata does not replace original attribution.

---

## 🗂️ INDEX.json Schema

`skills/INDEX.json` is the root-level grep target. Never edit by hand. Always regenerate with `scripts/build-index.sh`.

```json
[
  {
    "skill": "scientific-writing",
    "canonical": "skills/canonical/scientific-writing/SKILL.md",
    "description": "Write scientific manuscripts in full paragraphs using IMRAD structure, citations, and reporting guidelines (CONSORT/STROBE/PRISMA).",
    "tags": ["science", "writing", "manuscripts", "citations", "IMRAD"],
    "domain": ["science/writing"],
    "bundles": ["scientist", "researcher"],
    "upstream": "https://github.com/K-Dense-AI/claude-scientific-skills",
    "license": "MIT",
    "load_frequency": "high",
    "skill-author": "K-Dense Team"
  }
]
```

**Schema fields:**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `skill` | string | Yes | Matches directory name in `canonical/` |
| `canonical` | string | Yes | Full relative path from repo root |
| `description` | string | Yes | From SKILL.md frontmatter, max 3 sentences |
| `tags` | string[] | Yes | From SKILL.md frontmatter |
| `domain` | string[] | Yes | Derived from pointer file locations |
| `bundles` | string[] | No | Derived from bundle files |
| `upstream` | string | No | From SKILL.md metadata |
| `license` | string | Yes | From SKILL.md metadata |
| `load_frequency` | string | Yes | `high`, `medium`, or `low` |
| `skill-author` | string | No | From SKILL.md metadata |

---

## 🌲 Domain README Format

Every directory node in `skills/domain/` must have a `README.md` in this format:

```markdown
# <Domain> Skills

> **Navigation**: You are in `skills/domain/<domain>/`. This is a directory listing.
> - To browse subdirectories, read the subdirectory README.
> - To load a specific skill, find its `.pointer.md` and follow the `canonical:` path.
> - To search all skills, grep `skills/INDEX.json`.

## Skills in this domain

| Skill | Description | Canonical path |
|-------|-------------|----------------|
| [scientific-writing](writing/scientific-writing.pointer.md) | Write manuscripts with IMRAD, citations, reporting guidelines | `canonical/scientific-writing/` |
| [literature-review](writing/literature-review.pointer.md) | Conduct systematic literature reviews across databases | `canonical/literature-review/` |

## Subdirectories

| Directory | Skills | Focus |
|-----------|--------|-------|
| [writing/](writing/README.md) | 8 | Scientific manuscripts, style guides, diagrams |
| [analysis/](analysis/README.md) | 12 | Statistical methods, data interpretation |
| [databases/](databases/README.md) | 15 | PubMed, ChEMBL, UniProt, and other scientific DBs |
```

**Rules:**
- Header: one H1 with domain name
- Navigation hint at top: always the same three-option pattern
- Skills table: links to pointer files, not canonical files directly
- Subdirectory table: links to subdomain READMEs

---

## 📦 Bundle File Format

Bundle files describe an ordered skill loading sequence for a role. No content — only ordered pointer references.

```markdown
# Scientist Bundle

> Role-based skill sequence for scientific research workflows.
> Load in order — earlier skills establish context for later ones.

## Loading sequence

1. `_core/alignment.md` — always first
2. `_core/documentation.md` — formatting foundation
3. `canonical/scientific-writing/SKILL.md` — primary writing skill
4. `canonical/literature-review/SKILL.md` — research retrieval
5. `canonical/citation-management/SKILL.md` — reference management
6. `canonical/markdown-mermaid-writing/SKILL.md` — diagram standards
7. `canonical/statistical-analysis/SKILL.md` — when data is involved
8. `canonical/hypothesis-generation/SKILL.md` — when formulating research questions

## When to use this bundle

Load this bundle at session start when the primary task is scientific research, manuscript writing, literature review, or hypothesis generation.

## Extending this bundle

For specialized domains, add after step 8:
- Clinical work: `canonical/clinical-reports/SKILL.md`
- Data analysis: `canonical/agentic-data-scientist/SKILL.md`
```

---

## 🔧 Index Build Script

`scripts/build-index.sh` regenerates `INDEX.json` atomically. Run after any skill addition or modification.

```bash
#!/usr/bin/env bash
# build-index.sh — Regenerate skills/INDEX.json from canonical/ frontmatter
# Idempotent: safe to run multiple times.

set -euo pipefail

SKILLS_DIR="skills/canonical"
OUTPUT="skills/INDEX.json"
TEMP="$(mktemp)"

echo "[" > "$TEMP"
first=true

for skill_dir in "$SKILLS_DIR"/*/; do
  skill_file="$skill_dir/SKILL.md"
  [ -f "$skill_file" ] || continue

  skill_name="$(basename "$skill_dir")"
  # Extract YAML frontmatter and convert to JSON entry
  # (implementation: use yq or python-frontmatter)
  # Append to TEMP with comma handling

  if [ "$first" = true ]; then
    first=false
  else
    echo "," >> "$TEMP"
  fi
  # ... yq/python extraction logic ...
done

echo "]" >> "$TEMP"

# Validate JSON before overwriting
jq '.' "$TEMP" > /dev/null || { echo "ERROR: Generated invalid JSON"; exit 1; }
mv "$TEMP" "$OUTPUT"
echo "INDEX.json regenerated: $(jq '. | length' "$OUTPUT") skills"
```

---

## 🏗️ Upstream Import Plan

### Priority 1 — K-Dense claude-scientific-skills

- Source: `~/dev/claude-scientific-skills/scientific-skills/`
- 143 skills, MIT license
- Import ALL into `canonical/`; create science domain pointers for relevant ones
- Already local — no clone needed

### Priority 2 — sickn33/antigravity-awesome-skills

- Source: https://github.com/sickn33/antigravity-awesome-skills
- 868 skills, MIT license — **do NOT import all**
- Curate top ~50 by: (a) quality, (b) domain coverage gap-filling, (c) official sources (Anthropic, Vercel, Supabase official skills)
- Focus domains: architecture, testing, DevOps, infrastructure

### Priority 3 — ghostsecurity/skills

- Source: https://github.com/ghostsecurity/skills
- 7 skills, Apache-2.0
- Import all 7 into `canonical/security/`; create security/appsec pointers

### Priority 4 — K-Dense agentic-data-scientist + claude-scientific-writer

- Source: https://github.com/K-Dense-AI/agentic-data-scientist
- Import into data/ domain

### Already available (local)

- `~/dev/claude-scientific-skills/scientific-skills/markdown-mermaid-writing/` — import immediately as first canonical skill (PR-50 from K-Dense)

---

## 🔗 References

- [Issue-#2](docs/issues/issue-00000002-agents-skills-tree.md)
- [PR-#2](docs/pr/pr-00000002-agents-skills-tree.md)
- [ADR-004: Skill Tree Architecture](agentic/adr/ADR-004-skill-tree-architecture.md)
- [skills/AGENTS.md](skills/AGENTS.md)
- antigravity-awesome-skills (868 skills, MIT): https://github.com/sickn33/antigravity-awesome-skills
- K-Dense claude-scientific-skills (143 skills, MIT): https://github.com/K-Dense-AI/claude-scientific-skills
- ghostsecurity/skills (7 skills, Apache-2.0): https://github.com/ghostsecurity/skills
- OpenCode skills documentation: https://opencode.ai/docs/skills/

---

_Last updated: 2026-02-20_
