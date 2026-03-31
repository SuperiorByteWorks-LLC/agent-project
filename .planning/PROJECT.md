# GSD + Agent-Project Template Integration

## What This Is

A unified agentic development framework that combines GSD's hierarchical planning and phase-based execution with the agent-project template's rigorous documentation standards, Mermaid diagram conventions, and "Everything is Code" project tracking. This integration creates a comprehensive system for managing complex projects from high-level vision through implementation and verification.

## Core Value

Developers can plan projects with GSD's structured phases while maintaining the template's superior documentation quality and agent-optimized workflow — getting both systematic planning and execution excellence in one cohesive system.

## Requirements

### Validated

- ✓ AGENTS.md entrypoint system — existing
- ✓ 14-step agent workflow with human checkpoints — existing
- ✓ Mermaid diagram standards (23 types) — existing
- ✓ Everything-is-code tracking (PRs/issues/kanban as files) — existing
- ✓ CrewAI review system with memory — existing
- ✓ Local CI runner (`./scripts/ci-local.sh`) — existing

### Active

- [ ] Integrate GSD `.planning/` hierarchy with existing project structure
- [ ] Create unified workflow: GSD phases drive template execution
- [ ] Align kanban boards with GSD phase tracking
- [ ] Merge Mermaid standards into GSD documentation
- [ ] Create ADRs for integration architecture decisions
- [ ] Build comprehensive integration guide

### Out of Scope

- Replacing template's Mermaid standards with GSD's simpler versions — template standards are superior and will be preserved
- Modifying CrewAI review system architecture — integration at orchestration layer only
- Changing GitHub Actions workflows — focus is on local development experience
- Supporting non-markdown project tracking — everything-is-code principle is non-negotiable

## Context

This project emerges from the recognition that GSD provides excellent high-level planning and phase orchestration, while the agent-project template provides superior documentation standards and agent workflow patterns. Rather than choosing one, we're integrating both to create a best-of-both-worlds solution.

The agent-project template has invested heavily in:

- Mermaid diagram accessibility and styling standards
- Document templates for PRs, issues, kanban, ADRs
- Idempotent script patterns for CI
- Token management and context budget guides

GSD provides:

- Hierarchical project planning (PROJECT → REQUIREMENTS → ROADMAP)
- Phase-based execution with parallel agent orchestration
- Milestone management and audit workflows
- Research agents for domain exploration

## Constraints

- **Tech Stack**: Must work with existing Node.js/pnpm ecosystem
- **Compatibility**: Cannot break existing `./scripts/ci-local.sh` usage
- **Documentation**: Must follow existing markdown and Mermaid style guides
- **Git**: All planning artifacts committed (config.commit_docs: true)
- **Timeline**: Single-session implementation on experimental branch

## Key Decisions

| Decision                            | Rationale                                                                                                       | Outcome   |
| ----------------------------------- | --------------------------------------------------------------------------------------------------------------- | --------- |
| Use GSD as orchestrator             | GSD provides planning layer that template lacks; template provides execution layer that GSD delegates to agents | — Pending |
| Preserve template Mermaid standards | Template has 23 diagram type guides vs GSD's minimal approach; quality advantage clear                          | — Pending |
| Keep docs/project/ tracking         | Everything-is-code principle proven valuable; GSD's .planning/ complementary (planning vs execution tracking)   | — Pending |
| YOLO mode for integration           | User explicitly wants "just get shit done"; checkpoints at phase boundaries sufficient                          | — Pending |

---

_Last updated: 2026-02-19 after initialization_
