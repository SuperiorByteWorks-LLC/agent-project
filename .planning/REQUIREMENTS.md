# Requirements: GSD + Agent-Project Template Integration

**Defined:** 2026-02-19
**Core Value:** Unified planning and execution framework combining GSD's hierarchical planning with template's rigorous documentation and agent workflow

## v1 Requirements

Requirements for initial integration release. Each maps to roadmap phases.

### Planning Layer Integration

- [ ] **PLAN-01**: GSD `.planning/` directory structure integrates cleanly with existing repo layout
- [ ] **PLAN-02**: PROJECT.md captures integration vision and preserves template's existing validated capabilities
- [ ] **PLAN-03**: REQUIREMENTS.md defines REQ-ID traceability aligned with template conventions
- [ ] **PLAN-04**: ROADMAP.md phases map to incremental integration milestones
- [ ] **PLAN-05**: STATE.md tracks project memory and decision history

### Documentation Standards Alignment

- [ ] **DOC-01**: Template's Mermaid style guide (23 diagram types) takes precedence over GSD defaults
- [ ] **DOC-02**: Markdown style guide applies to all `.planning/` artifacts
- [ ] **DOC-03**: ADR format maintained for integration architecture decisions
- [ ] **DOC-04**: All diagrams follow accessibility standards (accTitle, accDescr, classDef)

### Execution Layer Integration

- [ ] **EXEC-01**: GSD phases spawn template 14-step workflow agents
- [ ] **EXEC-02**: AGENTS.md remains canonical entrypoint for all agent work
- [ ] **EXEC-03**: Local CI runner (`./scripts/ci-local.sh`) validates phase deliverables
- [ ] **EXEC-04**: CrewAI review system processes phase outputs

### Project Tracking Integration

- [ ] **TRACK-01**: Kanban boards reference active GSD phase and REQ-IDs
- [ ] **TRACK-02**: PR records document phase deliverables with traceability
- [ ] **TRACK-03**: Issue records track blockers and decisions
- [ ] **TRACK-04**: Source-of-truth sync updates both `.planning/` and `docs/project/`

### Verification and Guide

- [ ] **VERIFY-01**: Integration tested end-to-end on experimental branch
- [ ] **VERIFY-02**: Comprehensive integration guide created with examples
- [ ] **VERIFY-03**: All v1 requirements mapped to phases with success criteria
- [ ] **VERIFY-04**: ADR-009 documents architecture decision and consequences

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

| Requirement | Phase   | Status  |
| ----------- | ------- | ------- |
| PLAN-01     | Phase 1 | Pending |
| PLAN-02     | Phase 1 | Pending |
| PLAN-03     | Phase 1 | Pending |
| PLAN-04     | Phase 1 | Pending |
| PLAN-05     | Phase 1 | Pending |
| DOC-01      | Phase 2 | Pending |
| DOC-02      | Phase 2 | Pending |
| DOC-03      | Phase 1 | Pending |
| DOC-04      | Phase 2 | Pending |
| EXEC-01     | Phase 2 | Pending |
| EXEC-02     | Phase 2 | Pending |
| EXEC-03     | Phase 3 | Pending |
| EXEC-04     | Phase 3 | Pending |
| TRACK-01    | Phase 2 | Pending |
| TRACK-02    | Phase 2 | Pending |
| TRACK-03    | Phase 2 | Pending |
| TRACK-04    | Phase 3 | Pending |
| VERIFY-01   | Phase 3 | Pending |
| VERIFY-02   | Phase 3 | Pending |
| VERIFY-03   | Phase 3 | Pending |
| VERIFY-04   | Phase 1 | Pending |

**Coverage:**

- v1 requirements: 21 total
- Mapped to phases: 21
- Unmapped: 0 ✓

---

_Requirements defined: 2026-02-19_
_Last updated: 2026-02-19 after initial definition_
