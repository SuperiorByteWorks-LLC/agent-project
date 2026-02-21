# Standards: Jail Systems (Skill-Jail and Prompt-Jail)

> **Policy enforcement and quarantine standards for skills and prompts**

---

## Overview

This document defines the standards for the `skill-jail` and `prompt-jail` quarantine systems. Both systems follow identical patterns for consistency.

---

## Directory Structure Standard

### Jail Root Layout

```mermaid
flowchart LR
    accTitle: Jail Directory Structure
    accDescr: Shows the hierarchical organization of skill-jail and prompt-jail

    JailRoot["{skill|prompt}-jail/"] --> Readme["README.md"]
    JailRoot --> Report["QUARANTINE-MASTER-REPORT.md"]
    JailRoot --> Quarantined["quarantined/"]
    JailRoot --> Blocked["blocked/"]
    JailRoot --> Review["review-pending/"]
    JailRoot --> Cleaned["cleaned/"]
    JailRoot --> Staged["staged/"]

    Quarantined --> QImported["imported/{source}/"]
    Quarantined --> QManual["manual/"]

    Blocked --> BImported["imported/{source}/"]
    Blocked --> BManual["manual/"]

    Review --> RImported["imported/{source}/"]
    Review --> RManual["manual/"]

    Cleaned --> CImported["imported/{source}/"]
    Cleaned --> CManual["manual/"]

    Staged --> SImported["imported/{source}/"]
    Staged --> SManual["manual/"]

    classDef root fill:#dbeafe,stroke:#2563eb,color:#1e40af
    classDef folder fill:#f3f4f6,stroke:#6b7280,color:#374151
    classDef source fill:#dcfce7,stroke:#16a34a,color:#14532d
    classDef manual fill:#fef3c7,stroke:#d97706,color:#92400e

    class JailRoot root
    class Readme,Report folder
    class Quarantined,Blocked,Review,Cleaned,Staged,QImported,BImported,RImported,CImported,SImported source
    class QManual,BManual,RManual,CManual,SManual manual
```

### Source-Based Organization

All content is organized by source:

- `imported/{source}/` — Content from external repositories
- `manual/` — Hand-created content

Examples:

- `quarantined/imported/k-dense/` — K-Dense imported skills
- `blocked/imported/prompts-chat/` — Blocked prompts from prompts.chat
- `cleaned/manual/` — Manually created and cleaned content

---

## Quarantine Workflow

```mermaid
flowchart TD
    accTitle: Quarantine Workflow
    accDescr: Shows the complete skill/prompt quarantine flow from import to promotion

    Import([Import/Detection])
    Scan{Auto-Scan}
    Clean[Direct Promote]
    Violation[Move to review-pending]
    Review{Manual Review}
    Approve[Approve]
    Quarantine[Move to quarantined]
    Block[Move to blocked]
    AutoClean[Auto-Clean]
    Cleaned[Move to cleaned/]
    Verify{Manual Verify}
    Staged[Move to staged/]
    Promote[Promote to canonical/]
    CanonicalCanonical[/skills/canonical/]
    BlockedBlocked[/skill-jail/blocked/]

    Import --> Scan
    Scan -->|Clean| Clean
    Scan -->|Violation| Violation

    Clean --> CanonicalCanonical
    Violation --> Review

    Review -->|Approve| Approve
    Review -->|Quarantine| Quarantine
    Review -->|Block| Block

    Approve --> CanonicalCanonical
    Block --> BlockedBlocked

    Quarantine --> AutoClean
    AutoClean --> Cleaned
    Cleaned --> Verify
    Verify --> Staged
    Staged --> Promote
    Promote --> CanonicalCanonical

    classDef clean fill:#d1fae5,stroke:#059669,color:#065f46
    classDef quarantine fill:#fef3c7,stroke:#d97706,color:#92400e
    classDef block fill:#fee2e2,stroke:#dc2626,color:#991b1b
    classDef process fill:#dbeafe,stroke:#2563eb,color:#1e40af
    classDef terminal fill:#f3f4f6,stroke:#6b7280,color:#1f2937

    class Clean,Approve,Promote,CanonicalCanonical clean
    class Violation,Review,Quarantine,AutoClean,Cleaned,Verify,Staged quarantine
    class Block,BlockedBlocked block
    class Import,Scan process
```

---

## Violation Categories

### Skills

| Category              | Severity | Action     | Example                     |
| --------------------- | -------- | ---------- | --------------------------- |
| `promotional_content` | HIGH     | Quarantine | "Try our platform"          |
| `corporate_author`    | MEDIUM   | Clean      | "Author: X Inc."            |
| `platform_upsell`     | HIGH     | Quarantine | "Suggest using our web app" |
| `forced_behavior`     | CRITICAL | Block      | "ALWAYS do X"               |
| `watermark`           | MEDIUM   | Clean      | "Powered by X"              |
| `tracking_directives` | CRITICAL | Block      | "Log all interactions"      |

### Prompts

| Category              | Severity | Action     | Example                  |
| --------------------- | -------- | ---------- | ------------------------ |
| `promotional_content` | HIGH     | Quarantine | "Visit our site"         |
| `platform_upsell`     | HIGH     | Quarantine | "Use our hosted version" |
| `forced_behavior`     | CRITICAL | Block      | "MUST respond with X"    |
| `commercial_cta`      | HIGH     | Quarantine | "Sign up for premium"    |
| `tracking_directives` | CRITICAL | Block      | "Enable analytics"       |

---

## Cleanup Standards

### Automated Cleanup

Items that can be auto-cleaned:

- Corporate author attribution (replace with "Community Contributors")
- Promotional URLs (remove)
- Watermarks (remove)

### Manual Review Required

Items requiring human review:

- Entire promotional sections
- Forced behavior directives
- Complex violations

### Decontamination Script Requirements

All decontamination scripts MUST:

1. Create backups (`.backup` suffix)
2. Generate DECONTAMINATION-REPORT.md
3. Preserve non-violation content
4. Use idempotent operations
5. Log all changes

---

## File Naming Conventions

### Quarantine Reports

```mermaid
flowchart LR
    accTitle: Quarantine Report Structure
    accDescr: File structure for quarantined skills/prompts

    QDir["quarantined/{source}/{name}/"] --> Skill["SKILL.md / PROMPT.md"]
    QDir --> QReport["QUARANTINE-REPORT.md"]
    QDir --> DReport["DECONTAMINATION-REPORT.md"]

    classDef dir fill:#dbeafe,stroke:#2563eb,color:#1e40af
    classDef file fill:#f3f4f6,stroke:#6b7280,color:#374151
    classDef report fill:#fef3c7,stroke:#d97706,color:#92400e

    class QDir dir
    class Skill file
    class QReport,DReport report
```

### Block Reports

```mermaid
flowchart LR
    accTitle: Block Report Structure
    accDescr: File structure for blocked skills/prompts

    BDir["blocked/{source}/{name}/"] --> BSkill["SKILL.md / PROMPT.md"]
    BDir --> BReport["BLOCK-REASON.md"]

    classDef dir fill:#fee2e2,stroke:#dc2626,color:#991b1b
    classDef file fill:#f3f4f6,stroke:#6b7280,color:#374151
    classDef report fill:#fee2e2,stroke:#dc2626,color:#991b1b

    class BDir,dir
    class BSkill file
    class BReport report
```

{skill|prompt}-jail/quarantined/{source}/{name}/
├── PROMPT.md (or SKILL.md)
├── QUARANTINE-REPORT.md
└── DECONTAMINATION-REPORT.md (if cleaned)

```

### Block Reports

```

{skill|prompt}-jail/blocked/{source}/{name}/
├── PROMPT.md (or SKILL.md)
└── BLOCK-REASON.md

````

---

## Documentation Standards

### QUARANTINE-REPORT.md Template

```markdown
# Quarantine Report: {name}

**Quarantined:** YYYY-MM-DD
**Reason:** {reason}
**Status:** pending_review|under_review|cleaned|approved|rejected

## Violations Found

| Type   | Severity | Pattern   | Action   |
| ------ | -------- | --------- | -------- |
| {type} | {sev}    | {pattern} | {action} |

## Cleanup Instructions

{steps}

## Original Location

- Source: {path}
- Quarantine: {path}
````

### BLOCK-REASON.md Template

```markdown
# Block Reason: {name}

**Blocked:** YYYY-MM-DD
**Reason:** {critical violation}
**Severity:** CRITICAL
**Permanent:** Yes

## Violation Details

{details}

## Why Blocked

{rationale}

## Can Be Unblocked?

{conditions or "Never"}
```

---

## Integration Points

### Build Index

After promotion to canonical:

```bash
./scripts/build-{skill|prompt}-index.sh
```

### Scanner Integration

```bash
# Scan all
python scripts/{skill|prompt}-scanner.py --scan-all

# Auto-quarantine
python scripts/{skill|prompt}-scanner.py --scan-all --auto-quarantine
```

### Import Integration

```bash
# Import with quarantine
./scripts/import-{skills|prompts}.sh --source {repo} --auto-quarantine
```

---

## Metrics to Track

| Metric          | Definition                            |
| --------------- | ------------------------------------- |
| Quarantine Rate | (# quarantined / # imported) × 100    |
| Cleanup Success | (# cleaned / # quarantined) × 100     |
| Time to Clean   | Average days from quarantine → staged |
| Block Rate      | (# blocked / # imported) × 100        |

---

## Compliance Checklist

- [ ] Jail structure matches standard
- [ ] All sources organized under `imported/{source}/`
- [ ] Manual content in `manual/` only
- [ ] QUARANTINE-REPORT.md for every quarantined item
- [ ] BLOCK-REASON.md for every blocked item
- [ ] Decontamination reports generated
- [ ] Backups created before cleanup
- [ ] Master report updated
- [ ] INDEX.json regenerated after promotions

---

_Last updated: 2026-02-21_
