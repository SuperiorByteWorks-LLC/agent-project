# Development Domain — Prompts

> **Code, debug, architect, ship.**

This directory contains prompts for software development tasks.

---

## Subdomains

| Subdomain                               | Description                    | Prompt Count |
| --------------------------------------- | ------------------------------ | ------------ |
| [coding/](coding/README.md)             | Write, refactor, optimize code | ~100         |
| [debugging/](debugging/README.md)       | Find and fix bugs              | ~50          |
| [code-review/](code-review/README.md)   | Review and improve code        | ~50          |
| [architecture/](architecture/README.md) | Design systems and patterns    | ~50          |
| [testing/](testing/README.md)           | Write tests, QA                | ~30          |
| [deployment/](deployment/README.md)     | CI/CD, DevOps                  | ~20          |

---

## Quick Access

### Most Used

- [expert-debugger](coding/expert-debugger.pointer.md) — Systematic debugging approach
- [code-reviewer](code-review/code-reviewer.pointer.md) — Thorough code review
- [architect-decisions](architecture/architect-decisions.pointer.md) — Architecture decision making

### By Language

- [python-expert](coding/python-expert.pointer.md)
- [typescript-expert](coding/typescript-expert.pointer.md)
- [rust-expert](coding/rust-expert.pointer.md)

---

## Pointer Format

Each `.pointer.md` file contains:

```yaml
---
prompt: expert-debugger
canonical: prompts/canonical/imported/prompts-chat/expert-debugger/PROMPT.md
description: Systematic debugging approach for any language
tags: [debugging, troubleshooting, problem-solving]
source: prompts-chat
---

# expert-debugger

**Domain:** development/debugging
**Source:** [prompts.chat](https://prompts.chat)

Navigate to: `prompts/canonical/imported/prompts-chat/expert-debugger/PROMPT.md`
```

---

## Adding New Prompts

1. Import to `prompts/canonical/imported/<source>/`
2. Create pointer file in appropriate subdomain
3. Run `scripts/build-prompt-index.sh`

---

_See [PROMPT-TREE.md](../../PROMPT-TREE.md) for full documentation._
