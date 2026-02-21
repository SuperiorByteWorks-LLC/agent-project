# Developer Bundle

> Role-based skill loading sequence for software engineering workflows.
> Load in order. All paths relative to `skills/` root.

## Loading sequence

1. `_core/alignment.md` — always first
2. `_core/documentation.md` — formatting baseline
3. `canonical/typescript-expert/SKILL.md` — TypeScript patterns (or substitute python-patterns / go-patterns)
4. `canonical/senior-architect/SKILL.md` — system design, C4 diagrams, ADRs
5. `canonical/test-driven-development/SKILL.md` — TDD red/green/refactor

## When to use this bundle

Load when the primary task is software engineering: coding, architecture, refactoring, or system design.

## Extending

| Extension | Skill | When |
|-----------|-------|------|
| React/Frontend | `canonical/react-patterns/SKILL.md` | UI components, hooks |
| Python | `canonical/python-patterns/SKILL.md` | Python-first projects |
| DevOps | `canonical/docker-expert/SKILL.md` | Containers and deployment |
| Security review | `canonical/ghost-scan-code/SKILL.md` | Code security scanning |

## Status

Pending import from antigravity-awesome-skills (MIT). Curation in progress.
