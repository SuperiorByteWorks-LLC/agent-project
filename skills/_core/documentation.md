---
name: documentation
description: >
  Core documentation standard loaded at every session start. Establishes
  markdown + Mermaid as the canonical output format for all documents.
  This is a thin pointer to the full markdown-mermaid-writing skill —
  load that skill when producing actual documents.
allowed-tools: [Read]
load-trigger: always
metadata:
  skill-author: Clayton Young / Superior Byte Works, LLC (@borealBytes)
  skill-source: original
  skill-version: "1.0.0"
---

# Documentation — Core Standard

All output defaults to markdown with embedded Mermaid diagrams as the source of truth.

**Full skill**: When producing documents, diagrams, or reports, load:
→ `skills/canonical/markdown-mermaid-writing/SKILL.md`

That skill contains the complete markdown style guide, Mermaid diagram standards, 24 diagram type references, and 9 document templates.

## Quick rules (always apply)

- Markdown is the source format — not Word, not PDF, not Python-generated images
- Mermaid diagrams are text — diffable, versionable, renderable without build steps
- AI-generated or Python-generated images are downstream artifacts, never the source
- `accTitle` + `accDescr` on every diagram (accessibility)
- `classDef` color classes only — no `%%{init}`, no inline `style`

## When to load the full skill

Load `canonical/markdown-mermaid-writing/SKILL.md` when:
- Writing any report, manuscript, or structured document
- Creating diagrams (need diagram type selection guidance)
- Using document templates
- Unsure which Mermaid diagram type to use

## Status

`canonical/markdown-mermaid-writing/` — pending import from `~/dev/claude-scientific-skills/scientific-skills/markdown-mermaid-writing/`
