# Security Engineer Bundle

> Role-based skill loading sequence for application security workflows.
> Load in order. All paths relative to `skills/` root.

## Loading sequence

1. `_core/alignment.md` — always first
2. `canonical/ghost-repo-context/SKILL.md` — build repository security context first
3. `canonical/ghost-scan-code/SKILL.md` — SAST code scanning
4. `canonical/ghost-scan-deps/SKILL.md` — SCA dependency scanning
5. `canonical/ghost-scan-secrets/SKILL.md` — secret detection
6. `canonical/ghost-report/SKILL.md` — combined security report generation

## When to use

Load when performing security review, code audit, dependency analysis, or generating security reports.

## Extending

| Extension | Skill | When |
|-----------|-------|------|
| DAST | `canonical/ghost-validate/SKILL.md` + `canonical/ghost-proxy/SKILL.md` | Live app validation |

## Status

All 7 ghostsecurity skills pending import from https://github.com/ghostsecurity/skills (Apache-2.0).
