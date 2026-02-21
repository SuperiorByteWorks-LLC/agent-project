# ADR-004: Skill Tree Architecture — Pointer-Index Pattern

| Field | Value |
|-------|-------|
| **Status** | Accepted |
| **Date** | 2026-02-20 |
| **Author** | Clayton Young ([@borealBytes](https://github.com/borealBytes)) |
| **Supersedes** | None |
| **Related** | [ADR-003: Everything is Code](ADR-003-everything-is-code.md) |

---

## 🎯 Context

The 2026 agentic coding ecosystem has produced dozens of skill repositories, the largest having 868 skills.[^1] Every one of them uses a flat directory structure: one folder per skill, all at the same level. This is fine for small collections. It breaks down at scale:

- An agent cannot selectively load "writing skills" without either loading the entire repo or maintaining an external, hand-curated list.
- Skills that fit multiple domains get copied into each relevant location, creating duplicate content with no single source of truth.
- Context windows are finite. Loading 20 irrelevant skills to get to the 1 relevant one is a real cost.
- There is no mechanism for a subdomain to inherit shared behavior (alignment, formatting) from a parent. Every skill must re-state conventions that should be implicit.

The question: how should a large personal skill repository (target: 500–1000 skills) be organized so that agents can load exactly what they need, find anything quickly even when uncertain, and never encounter duplicated content?

---

## 🔍 Decision Drivers

1. **Selective loading** — agents load ≤ 10 skills for most tasks (not 100+)
2. **Single source of truth** — zero content duplication across the skill set
3. **Fast uncertainty resolution** — when an agent doesn't know if a skill exists or where it lives, resolution must take seconds not minutes
4. **Alignment inheritance** — core values and formatting standards propagate down the tree without repetition
5. **Provenance and attribution** — imported skills must retain original authorship and license
6. **Operator-friendly** — the system must be maintainable by one person and a few agents over time

---

## 🗺️ Considered Options

### Option A — Flat with tags

Keep the flat structure; add YAML frontmatter tags to each skill; build a tag-based search tool.

**Problems**: Still loads everything to build tag index. No navigation structure. Duplication when a skill fits two categories — either copy or lose the cross-domain membership.

### Option B — Multi-root domain directories

Organize by domain at the top level (`science/`, `development/`, etc.); skills live in their primary domain directory. Cross-domain skills are symlinked.

**Problems**: Symlinks break on Windows without Git config flags.[^2] Skills still duplicated conceptually when symlinks aren't available. No root-level search fallback.

### Option C — Pointer-Index Tree (chosen)

- All skill content lives at exactly one canonical path (`skills/canonical/<skill-name>/SKILL.md`).
- A taxonomy tree (`skills/domain/`) contains only pointer files and README directory listings — zero skill content.
- A machine-generated `skills/INDEX.json` provides the grep fallback for uncertainty.
- A `skills/_core/` directory holds always-loaded alignment and documentation foundation skills.
- Bundle files (`skills/bundles/`) are ordered pointer lists for role-specific loading — zero content.

---

## ✅ Decision

**Adopt the Pointer-Index Tree pattern (Option C).**

### Three invariants — never violated

1. **One canonical path per skill**: skills live at `skills/canonical/<skill-name>/SKILL.md`. This is the only copy of any skill content.
2. **Taxonomy nodes contain pointers only**: `skills/domain/` nodes hold `.pointer.md` files and `README.md` directory listings. No skill content anywhere in the taxonomy tree.
3. **INDEX.json is machine-generated**: `scripts/build-index.sh` regenerates the index from canonical frontmatter. It is never edited by hand. It is the single grep target for uncertainty resolution.

### Navigation model

The model is deliberately modeled on the Yahoo Directory[^3] — the classic pre-search web navigation paradigm. Before search engines, humans navigated by category drill-down. The same pattern is optimal for agents:

```
Known domain → read domain README → read subdomain README → follow pointer → load SKILL.md
Unknown location → grep INDEX.json → get canonical path → load SKILL.md
```

Two paths, both terminate at a single canonical file. No path requires loading more than one skill's content.

### Inheritance model

```
skills/_core/           ← always loaded (root of inheritance tree)
skills/domain/*/AGENTS.md  ← domain-level loading rules (extend root)
skills/canonical/*/SKILL.md  ← skill content (leaf nodes)
```

Core skills (alignment, documentation standards) define the baseline behavior inherited by all skills. Domain AGENTS.md files specify which skills auto-load when the agent is operating in that domain. Leaf skills never need to re-state core conventions.

### Pointer file format

```markdown
---
skill: scientific-writing
canonical: ../../../canonical/scientific-writing/SKILL.md
description: >
  Write scientific manuscripts in full paragraphs using IMRAD structure,
  citations, figures, and reporting guidelines.
tags: [science, writing, manuscripts]
upstream: https://github.com/K-Dense-AI/claude-scientific-skills
license: MIT
---
```

Zero prose. Zero skill content. Navigation metadata only.

### INDEX.json schema

```json
{
  "skill": "scientific-writing",
  "canonical": "skills/canonical/scientific-writing/SKILL.md",
  "description": "...",
  "tags": ["science", "writing", "manuscripts"],
  "domain": ["science/writing"],
  "bundles": ["scientist", "researcher"],
  "upstream": "https://github.com/K-Dense-AI/claude-scientific-skills",
  "license": "MIT",
  "load_frequency": "high"
}
```

The `load_frequency` field (`high`, `medium`, `low`) reflects observed usage and guides bundle curation. It is set by the maintainer, not auto-generated.

---

## 📊 Consequences

**Positive:**

- Context efficiency: a scientist agent loads 5–8 skills vs 143+ in flat repos
- Zero duplication: `find skills/canonical -name "SKILL.md" | wc -l` equals `jq '. | length' skills/INDEX.json` by construction
- Platform-agnostic: no symlinks, no tool-specific features — plain text files on any OS
- Grep-searchable: `jq '.[] | select(.tags[] | contains("X"))' skills/INDEX.json` resolves any uncertainty instantly
- Provenance preserved: every imported skill retains `upstream` URL, `license`, and attribution in frontmatter

**Negative / Tradeoffs:**

- Pointer files add a navigation layer — agents must follow one redirect per skill (acceptable: pointer files are tiny, resolution is trivial)
- Index requires manual regeneration after skill additions (`scripts/build-index.sh`) — mitigated by keeping the script idempotent and fast
- Cross-domain membership (skill in two domains) requires two pointer files — acceptable; content remains single-source

**Neutral:**

- Bundle files are ordering abstractions — they define role-appropriate loading sequences, not content. Curating them is subjective and intentional.

---

## 🔗 References

[^1]: antigravity-awesome-skills — 868 skills in flat directory: https://github.com/sickn33/antigravity-awesome-skills
[^2]: Git symlinks on Windows: https://git-scm.com/docs/git-config#Documentation/git-config.txt-coresymlinks
[^3]: Yahoo Directory model: https://en.wikipedia.org/wiki/Yahoo!_Directory

- [Issue-#2](../../docs/issues/issue-00000002-agents-skills-tree.md)
- [PR-#2](../../docs/pr/pr-00000002-agents-skills-tree.md)
- [SKILL-TREE.md](../../SKILL-TREE.md)
- [ADR-003: Everything is Code](ADR-003-everything-is-code.md)

---

_Last updated: 2026-02-20_
