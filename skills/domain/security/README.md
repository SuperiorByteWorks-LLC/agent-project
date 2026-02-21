# Security Domain

> **Navigation**: You are in `skills/domain/security/`.
> - To browse subdirectories: read a subdirectory README below
> - To load a skill: find its `.pointer.md`, follow the `canonical:` path
> - Uncertain? Search: `jq '.[] | select(.domain[] | contains("security"))' skills/INDEX.json`

---

## Subdirectories

| Directory | Skills | Focus |
|-----------|--------|-------|
| [appsec/](appsec/README.md) | 7 | AI-powered application security scanning |
| [pentesting/](pentesting/README.md) | ~3 | Penetration testing patterns _(pending)_ |

## Ghost Security AppSec suite

All 7 ghostsecurity/skills — ready to import (Apache-2.0, compatible):

| Skill | What it does |
|-------|-------------|
| ghost-repo-context | Build shared repository context (criticality, sensitive data, component map) |
| ghost-scan-code | AI-powered detection of code security issues (SAST) |
| ghost-scan-deps | Exploitability analysis of dependency vulnerabilities (SCA) |
| ghost-scan-secrets | Context assessment of detected secrets and credentials |
| ghost-report | Combined security report across all scan results |
| ghost-validate | Dynamic validation of findings against live application (DAST) |
| ghost-proxy | HTTP proxy for the ghost-validate skill |

## Import status

Source: https://github.com/ghostsecurity/skills (Apache-2.0)
Status: **Pending import** — 7 skills, high priority
