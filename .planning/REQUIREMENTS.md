# Requirements: GSD + Agent-Project Template Integration

**Defined:** 2026-02-19
**Core Value:** Unified planning and execution framework combining GSD's hierarchical planning with template's rigorous documentation and agent workflow

## v1 Requirements

Requirements for initial integration release. Each maps to roadmap phases.

### Planning Layer Integration

- [x] **PLAN-01**: GSD `.planning/` directory structure integrates cleanly with existing repo layout
- [x] **PLAN-02**: PROJECT.md captures integration vision and preserves template's existing validated capabilities
- [x] **PLAN-03**: REQUIREMENTS.md defines REQ-ID traceability aligned with template conventions
- [x] **PLAN-04**: ROADMAP.md phases map to incremental integration milestones
- [x] **PLAN-05**: STATE.md tracks project memory and decision history

### Documentation Standards Alignment

- [x] **DOC-01**: Template's Mermaid style guide (23 diagram types) takes precedence over GSD defaults
- [x] **DOC-02**: Markdown style guide applies to all `.planning/` artifacts
- [x] **DOC-03**: ADR format maintained for integration architecture decisions
- [x] **DOC-04**: All diagrams follow accessibility standards (accTitle, accDescr, classDef)

### Execution Layer Integration

- [x] **EXEC-01**: GSD phases spawn template 14-step workflow agents
- [x] **EXEC-02**: AGENTS.md remains canonical entrypoint for all agent work
- [x] **EXEC-03**: Local CI runner (`./scripts/ci-local.sh`) validates phase deliverables
- [x] **EXEC-04**: CrewAI review system processes phase outputs

### Project Tracking Integration

- [x] **TRACK-01**: Kanban boards reference active GSD phase and REQ-IDs
- [x] **TRACK-02**: PR records document phase deliverables with traceability
- [x] **TRACK-03**: Issue records track blockers and decisions (demonstrated)
- [x] **TRACK-04**: Source-of-truth sync updates both `.planning/` and `docs/project/`

### Verification and Guide

- [x] **VERIFY-01**: Integration tested end-to-end on experimental branch
- [x] **VERIFY-02**: Comprehensive integration guide created with examples
- [x] **VERIFY-03**: All v1 requirements mapped to phases with success criteria
- [x] **VERIFY-04**: ADR-009 documents architecture decision and consequences

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Automation

- **AUTO-01**: `./scripts/ci-local.sh` validates GSD phase alignment
- **AUTO-02**: Git hooks prevent commits that break planning/tracking sync
- **AUTO-03**: Automated REQ-ID consistency checker

### Template Enhancements

- **TMPL-01**: Kanban template includes GSD phase reference section
- **TMPL-02**: PR template includes REQ-ID traceability fields
- **TMPL-03**: Issue template includes phase blocker tracking

## Out of Scope

| Feature                              | Reason                                                                              |
| ------------------------------------ | ----------------------------------------------------------------------------------- |
| Replacing template Mermaid standards | Template has 23 diagram type guides; GSD has minimal approach; template is superior |
| Modifying CrewAI review architecture | Integration at orchestration layer only; review system remains unchanged            |
| GitHub Actions workflow changes      | Focus is local development experience; CI/CD remains separate concern               |
| Non-markdown project tracking        | Everything-is-code principle is non-negotiable; no external PM tools                |
| GSD cloud/sync features              | Local-first approach maintained; no external dependencies                           |

## Traceability

| Requirement | Phase   | Status   |
| ----------- | ------- | -------- |
| PLAN-01     | Phase 1 | Complete |
| PLAN-02     | Phase 1 | Complete |
| PLAN-03     | Phase 1 | Complete |
| PLAN-04     | Phase 1 | Complete |
| PLAN-05     | Phase 1 | Complete |
| DOC-01      | Phase 2 | Complete |
| DOC-02      | Phase 2 | Complete |
| DOC-03      | Phase 1 | Complete |
| DOC-04      | Phase 2 | Complete |
| EXEC-01     | Phase 2 | Complete |
| EXEC-02     | Phase 2 | Complete |
| EXEC-03     | Phase 3 | Complete |
| EXEC-04     | Phase 3 | Complete |
| TRACK-01    | Phase 2 | Complete |
| TRACK-02    | Phase 2 | Complete |
| TRACK-03    | Phase 2 | Complete |
| TRACK-04    | Phase 3 | Complete |
| VERIFY-01   | Phase 3 | Complete |
| VERIFY-02   | Phase 3 | Complete |
| VERIFY-03   | Phase 1 | Complete |
| VERIFY-04   | Phase 1 | Complete |

**Coverage:**

- v1 requirements: 21 total
- Mapped to phases: 21
- Unmapped: 0 ✓

---

_Requirements defined: 2026-02-19_
_Last updated: 2026-02-19 — All 21 v1 requirements complete_
