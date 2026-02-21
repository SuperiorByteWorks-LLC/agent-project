# Scientist Bundle

> Role-based skill loading sequence for scientific research workflows.
> Load in order — earlier skills establish context for later ones.
> All paths are relative to the `skills/` root.

## Loading sequence

1. `_core/alignment.md` — always first; core values and operating principles
2. `_core/documentation.md` — formatting baseline
3. `canonical/markdown-mermaid-writing/SKILL.md` — full style guide, 24 diagram types, 9 templates
4. `canonical/scientific-writing/SKILL.md` — IMRAD manuscripts, citations, reporting guidelines
5. `canonical/literature-review/SKILL.md` — systematic reviews across PubMed, arXiv, bioRxiv
6. `canonical/citation-management/SKILL.md` — search, validate, BibTeX generation
7. `canonical/statistical-analysis/SKILL.md` — statistical methods and interpretation
8. `canonical/hypothesis-generation/SKILL.md` — structured hypothesis formulation

## When to use this bundle

Load this bundle at session start when the primary task is:
- Scientific research or manuscript writing
- Literature review or systematic review
- Hypothesis formulation from observations
- Clinical or biomedical data analysis

## Extending this bundle

Add after step 8 based on specific need:

| Extension | Skill | When |
|-----------|-------|------|
| Clinical reports | `canonical/clinical-reports/SKILL.md` | Clinical case reports, diagnostic reports |
| Clinical decisions | `canonical/clinical-decision-support/SKILL.md` | Drug development, evidence synthesis |
| Data science | `canonical/agentic-data-scientist/SKILL.md` | Heavy data analysis |
| Schematics | `canonical/scientific-schematics/SKILL.md` | Neural networks, pathways, system diagrams |
| Slides | `canonical/scientific-slides/SKILL.md` | Conference presentations |
| Grants | `canonical/research-grants/SKILL.md` | NSF, NIH, DOE proposals |
| Infographics | `canonical/infographics/SKILL.md` | Visual summaries |
| Venue templates | `canonical/venue-templates/SKILL.md` | Journal/conference submission formatting |

## Status

Skills pending import from `~/dev/claude-scientific-skills/`. Paths will be active after import.
