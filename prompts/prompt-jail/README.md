# Prompt Jail System

_Quarantine and review system for managing prompts with policy violations_

---

## 📋 Overview

The prompt jail is a quarantine system that identifies, isolates, and manages prompts that violate repository policies. It ensures the prompt tree maintains high quality standards and remains free from promotional content, forced behavior directives, and other undesirable elements.

**Structure mirrors skill-jail exactly.**

---

## 🏗️ Directory Structure

```text
prompts/prompt-jail/
├── README.md              # This file
├── quarantined/           # Prompts with confirmed violations
│   └── imported/
│       └── prompts-chat/
│           └── {prompt-name}/
│               ├── PROMPT.md
│               └── QUARANTINE-REPORT.md
├── review-pending/        # Prompts awaiting manual review
├── blocked/               # Permanently blocked prompts
├── cleaned/               # Prompts that passed review after cleanup
└── staged/                # Ready for promotion to canonical
```

---

## 🔍 How Prompts Get Here

### Automatic Detection

The `prompt-scanner.py` script automatically detects violations during:

- **Import workflows** — when importing prompts from external sources
- **CI/CD pipelines** — automated scanning on pull requests
- **Manual scans** — ad-hoc scanning of the prompt tree

### Detection Categories

| Category              | Description                        | Example                     |
| --------------------- | ---------------------------------- | --------------------------- |
| `promotional_content` | Advertising for external platforms | "Try our premium service"   |
| `forced_behavior`     | Mandates specific AI behavior      | "ALWAYS respond with X"     |
| `commercial_cta`      | Calls to action for paid services  | "Sign up at example.com"    |
| `platform_upsell`     | Pushes users to external platforms | "Use our hosted version"    |
| `tracking_directives` | Prompts that enable tracking       | "Log all user interactions" |

---

## 📖 Review and Approval Workflow

### Step 1: Detection

When a violation is detected, the prompt is moved to `review-pending/` with an initial assessment.

### Step 2: Manual Review

A maintainer reviews the prompt and determines:

- **Severity**: `critical`, `high`, `medium`, `low`
- **Action**: `approve`, `quarantine`, `block`, `clean`

### Step 3: Resolution

| Action       | Destination                | Description                          |
| ------------ | -------------------------- | ------------------------------------ |
| `approve`    | `prompts/canonical/`       | Prompt is clean, moved to canonical  |
| `quarantine` | `prompt-jail/quarantined/` | Has fixable issues, awaiting cleanup |
| `block`      | `prompt-jail/blocked/`     | Permanently rejected                 |
| `clean`      | `prompts/canonical/`       | Auto-cleaned and approved            |

### Step 4: Documentation

Every action is documented in a quarantine report.

---

## 🛠️ Tools

### prompt-scanner.py

Scans prompts for blocklist patterns and generates quarantine recommendations.

```bash
# Scan a specific prompt
python scripts/prompt-scanner.py --prompt prompts/canonical/example/

# Scan entire prompt tree
python scripts/prompt-scanner.py --scan-all

# Auto-clean detected violations
python scripts/prompt-scanner.py --prompt prompts/canonical/example/ --auto-clean
```

### import-prompts.sh

Imports prompts from prompts.chat with automatic quarantine checking.

```bash
# Import from prompts.chat
./scripts/import-prompts.sh --source prompts-chat --limit 100

# Import with dry-run
./scripts/import-prompts.sh --source prompts-chat --dry-run
```

---

## 📝 Blocklist Configuration

The `prompt-blocklist.yaml` file defines patterns to detect violations.

---

## 📊 Status Tracking

Prompts in quarantine are tracked with:

- **QUARANTINE-REPORT.md**: Detailed violation report
- **INDEX.json**: Not indexed until approved
- **Git history**: All actions tracked in git

---

## 🚫 Permanently Blocked Prompts

Prompts in `blocked/` are permanently rejected. Reasons include:

- Malicious content
- Severe policy violations
- Repeated violations after cleanup
- Legal or compliance issues

---

## 💡 Best Practices

1. **Review promptly** — Don't let prompts languish in review-pending
2. **Document thoroughly** — Every quarantine needs a clear report
3. **Clean before approve** — Remove violations, don't just ignore them
4. **Update blocklist** — Add new patterns as violations are discovered

---

## 🔗 Related Documentation

- [PROMPT-TREE.md](../../PROMPT-TREE.md) — Prompt tree architecture
- [AGENTS.md](../AGENTS.md) — Prompt loading protocol
- [QUARANTINE_REPORT.md](QUARANTINE_REPORT.md) — Template for reports

---

_Last updated: 2026-02-21_
