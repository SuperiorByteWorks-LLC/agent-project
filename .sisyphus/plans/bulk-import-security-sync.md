# Bulk Import + Security Sandbox + Upstream Sync System

## TL;DR

Import **ALL 1,050+ skills** from upstream (882 antigravity + 143 K-Dense scientific + 25 K-Dense writer + 7 ghostsecurity) with a **zero-trust security sandbox** and **automated upstream sync** capability.

**Key innovation**: Every skill carries `what_it_does` array for grepability, ultra-clear file paths for discoverability-by-design, and complete upstream provenance for automated refresh.

---

## Current State

| Source | Skills | Status | Location |
|--------|--------|--------|----------|
| markdown-mermaid-writing | 1 | ✅ Imported | `canonical/markdown-mermaid-writing/` |
| K-Dense scientific-skills | 143 | 📦 Ready | `~/dev/claude-scientific-skills/` (local) |
| K-Dense scientific-writer | ~25 | 🔗 Remote | https://github.com/K-Dense-AI/claude-scientific-writer |
| antigravity-awesome-skills | 882 | 🔗 Remote | https://github.com/sickn33/antigravity-awesome-skills |
| ghostsecurity/skills | 7 | 🔗 Remote | https://github.com/ghostsecurity/skills |
| **Total** | **~1,058** | | |

---

## Part 1: Enhanced Metadata Schema (for grepability)

### SKILL.md frontmatter additions

```yaml
---
name: typescript-expert
description: >
  TypeScript deep-dive: strict config, generics mastery, type guards, and idiomatic patterns.

# NEW: "What it does" — grep-friendly capability list
what_it_does:
  - "Configures strict TypeScript with noImplicitAny"
  - "Teaches generic constraints and conditional types"
  - "Explains type guards (typeof, instanceof, custom)"
  - "Patterns for discriminated unions and branded types"

# NEW: Decision aid — when to load this
typical_use_cases:
  - "Starting TypeScript project from scratch"
  - "Migrating JavaScript to TypeScript"
  - "Debugging complex generic errors"

# Navigation (enables discoverability-by-design)
domain: development
subdomain: languages
tags: [typescript, javascript, generics, types, strict-mode]

# Tool compatibility
compatible_with:
  - opencode
  - claude-code
  - cursor
  - codex

# License and attribution
license: MIT
metadata:
  # Original creation
  skill-author: "John Doe"
  skill-source: "https://github.com/original/ts-skills"
  created-date: "2025-06-15"

  # Import tracking (for upstream sync)
  imported-from: "https://github.com/sickn33/antigravity-awesome-skills"
  imported-by: "Clayton Young"
  import-date: "2026-02-20"
  import-commit: "a1b2c3d4e5f6789..."
  upstream-version: "v5.4.0"
  upstream-branch: "main"

  # Sync state
  last-sync-check: "2026-02-20"
  sync-status: current  # current | behind | diverged | conflict

  # Validation
  validation:
    last-validated: "2026-02-20"
    status: pass
    checksum: "sha256:abc123..."
---
```

### Grep-friendly design

| Use case | Command |
|----------|---------|
| Find skills that "configure TypeScript" | `grep -r "Configures strict TypeScript" skills/canonical/*/SKILL.md` |
| Find skills with "generics" capability | `grep -r "generics" skills/canonical/*/SKILL.md` |
| Find all Python skills | `jq '.[] | select(.tags | contains("python"))' skills/INDEX.json` |
| Find skills imported from antigravity | `jq '.[] | select(.upstream | contains("antigravity"))' skills/INDEX.json` |
| Find outdated skills | `jq '.[] | select(.sync-status == "behind")' skills/INDEX.json` |

---

## Part 2: Directory Structure (discoverability-by-design)

### Canonical structure (flat — SSoT)

```
skills/canonical/
├── typescript-expert/              # name = directory name
│   ├── SKILL.md                    # skill definition
│   ├── assets/                     # diagrams, examples (optional)
│   └── references/                 # templates, guides (optional)
├── python-patterns/
├── react-hooks-mastery/
└── ... 1050+ directories
```

### Domain tree (navigation — discoverable)

```
skills/domain/
├── development/
│   ├── README.md                   # "You are here" + skill listing
│   ├── languages/
│   │   ├── README.md
│   │   ├── typescript-expert.pointer.md
│   │   ├── python-patterns.pointer.md
│   │   └── go-idioms.pointer.md
│   ├── frameworks/
│   │   ├── react-hooks-mastery.pointer.md
│   │   └── vue-patterns.pointer.md
│   └── architecture/
│       └── senior-architect.pointer.md
├── science/
│   ├── README.md
│   ├── writing/
│   │   ├── README.md
│   │   ├── markdown-mermaid-writing.pointer.md  ✅
│   │   ├── scientific-writing.pointer.md
│   │   └── literature-review.pointer.md
│   └── databases/
│       ├── pubmed.pointer.md
│       └── chembl.pointer.md
└── security/
    ├── README.md
    ├── appsec/
    │   ├── ghost-scan-code.pointer.md
│   └── pentesting/
└── ...
```

### File naming rules (MUST follow)

| Rule | Example | Why |
|------|---------|-----|
| `kebab-case` | `typescript-expert` | grep-friendly, URL-safe |
| Match `name:` field exactly | `name: typescript-expert` ↔ `typescript-expert/` | consistency |
| No version numbers in path | ❌ `typescript-expert-v2/` | versions in metadata |
| Domain + subdomain in pointer path | `domain/development/languages/` | browseable |
| Pointer files end in `.pointer.md` | `typescript-expert.pointer.md` | clear intent |

---

## Part 3: Security Sandbox Pipeline (Zero-Trust)

### Branch strategy

```
main                              ← production (validated only)
├── staging/                      ← integration testing
│   └── import-batch-2026-02-20/
└── sandbox/                      ← unvalidated imports
    ├── import-antigravity-2026-02-20/
    ├── import-kdense-scientific-2026-02-20/
    └── import-kdense-writer-2026-02-20/
```

### Validation stages

#### Stage 1: Static Analysis (`validate-static.sh`)

```bash
#!/usr/bin/env bash
# validates static code, structure, and content

SKILL_FILE=$1
ERRORS=0

# Check 1: No invisible Unicode
echo "Checking for invisible Unicode..."
if grep -P '[\x{200B}-\x{200D}\x{FEFF}\x{2060}-\x{206F}]' "$SKILL_FILE"; then
    echo "ERROR: Invisible Unicode detected"
    ((ERRORS++))
fi

# Check 2: No bidirectional text overrides (Trojan Source)
echo "Checking for bidirectional overrides..."
if grep -P '[\x{202A}-\x{202E}\x{2066}-\x{2069}]' "$SKILL_FILE"; then
    echo "ERROR: Bidirectional text detected (Trojan Source risk)"
    ((ERRORS++))
fi

# Check 3: Safe YAML (no anchors, no references)
echo "Checking YAML safety..."
if grep -E '^\s*\*\w+:' "$SKILL_FILE"; then
    echo "ERROR: YAML anchor/reference detected (injection risk)"
    ((ERRORS++))
fi

# Check 4: No suspicious shell patterns
echo "Checking for shell execution..."
if grep -E '(eval\s*\(|exec\s*\(|system\s*\(|`[^`]*`)' "$SKILL_FILE"; then
    echo "ERROR: Suspicious shell execution detected"
    ((ERRORS++))
fi

# Check 5: No external scripts
echo "Checking for external script references..."
if grep -E '(<script|javascript:|data:text/javascript)' "$SKILL_FILE"; then
    echo "ERROR: External script reference detected"
    ((ERRORS++))
fi

# Check 6: Valid markdown structure
echo "Checking markdown structure..."
if ! grep -q "^# " "$SKILL_FILE"; then
    echo "ERROR: No H1 found"
    ((ERRORS++))
fi

# Check 7: Required frontmatter fields
echo "Checking required fields..."
for field in "name" "description" "what_it_does" "domain" "tags" "license"; do
    if ! grep -q "^${field}:" "$SKILL_FILE"; then
        echo "ERROR: Missing required field: $field"
        ((ERRORS++))
    fi
done

exit $ERRORS
```

#### Stage 2: Content Validation (`validate-content.sh`)

- Mermaid syntax validation (if diagrams present)
- Link validation (no broken internal refs)
- Image source validation (only whitelisted domains)
- No executable file attachments

#### Stage 3: Sandbox Execution (`validate-sandbox.sh`)

```bash
#!/usr/bin/env bash
# Execute skill in isolated environment to detect unexpected behavior

SKILL_FILE=$1
SKILL_NAME=$(basename $(dirname $SKILL_FILE))
SANDBOX_DIR=$(mktemp -d)

echo "Creating sandbox in $SANDBOX_DIR..."

# Copy skill to sandbox
cp "$SKILL_FILE" "$SANDBOX_DIR/"

# Create isolated environment:
# - chroot jail or container (if available)
# - Network disabled
# - Read-only filesystem except sandbox dir
# - Limited resource quotas

echo "Running skill in sandbox..."
# This would use a container or restricted subprocess
# For now, we simulate with strict timeouts and monitoring

timeout 30s bash -c "
    cd $SANDBOX_DIR
    # Simulate skill loading and basic execution
    # Check for any file system access outside sandbox
    # Check for network attempts
    # Check for process spawning
" 2>&1 | tee "$SANDBOX_DIR/execution.log"

# Analyze logs for violations
echo "Analyzing execution logs..."
# Check for:
# - File system access outside sandbox
# - Network connections
# - Process execution
# - Suspicious patterns

# Cleanup
rm -rf "$SANDBOX_DIR"
```

#### Stage 4: Human Review

For **first-time imports** from new upstreams:
- Full diff review
- Security checklist completion
- Maintainer approval required

For **updates** to existing skills:
- Diff-only review
- Automated validation must pass
- Single maintainer approval OK

### Validation results storage

```json
{
  "skill": "typescript-expert",
  "validation": {
    "date": "2026-02-20",
    "validator": "v1.0.0",
    "stages": {
      "static": "pass",
      "content": "pass",
      "sandbox": "pass",
      "human_review": "approved"
    },
    "violations": [],
    "checksum": "sha256:abc123..."
  }
}
```

---

## Part 4: Upstream Sync System

### `upstream-registry.json` (central registry)

```json
{
  "version": "1.0.0",
  "updated": "2026-02-20",
  "upstreams": [
    {
      "id": "antigravity",
      "name": "Antigravity Awesome Skills",
      "url": "https://github.com/sickn33/antigravity-awesome-skills",
      "license": "MIT",
      "tracked_branch": "main",
      "last_fetch": "2026-02-20T18:00:00Z",
      "last_commit": "a1b2c3d4e5f6789...",
      "skills_count": 882,
      "local_vendor_path": "vendor/antigrawesome-skills",
      "sync_frequency": "weekly",
      "auto_pr": false,
      "maintainer": "sickn33",
      "categories": ["development", "security", "data", "infrastructure"]
    },
    {
      "id": "kdense-scientific",
      "name": "K-Dense Scientific Skills",
      "url": "https://github.com/K-Dense-AI/claude-scientific-skills",
      "license": "MIT",
      "tracked_branch": "main",
      "last_fetch": "2026-02-20T18:00:00Z",
      "last_commit": "b2c3d4e5f678901...",
      "skills_count": 143,
      "local_vendor_path": "~/dev/claude-scientific-skills",
      "sync_frequency": "daily",
      "auto_pr": false,
      "maintainer": "K-Dense-AI",
      "categories": ["science"]
    },
    {
      "id": "kdense-writer",
      "name": "K-Dense Scientific Writer",
      "url": "https://github.com/K-Dense-AI/claude-scientific-writer",
      "license": "MIT",
      "tracked_branch": "main",
      "skills_count": 25,
      "local_vendor_path": "vendor/kdense-writer",
      "sync_frequency": "weekly",
      "auto_pr": false
    },
    {
      "id": "ghostsecurity",
      "name": "Ghost Security Skills",
      "url": "https://github.com/ghostsecurity/skills",
      "license": "Apache-2.0",
      "tracked_branch": "main",
      "skills_count": 7,
      "local_vendor_path": "vendor/ghostsecurity-skills",
      "sync_frequency": "monthly",
      "auto_pr": false
    }
  ]
}
```

### Sync scripts

#### `scripts/skills-sync/check-updates.sh`

```bash
#!/usr/bin/env bash
# Check all upstreams for changes

REGISTRY="skills/upstream-registry.json"
REPORT="skills/sync-report-$(date +%Y-%m-%d).md"

echo "# Sync Report: $(date)" > "$REPORT"

for upstream in $(jq -r '.upstreams[] | .id' "$REGISTRY"); do
    echo "Checking $upstream..."

    URL=$(jq -r ".upstreams[] | select(.id == \"$upstream\") | .url" "$REGISTRY")
    BRANCH=$(jq -r ".upstreams[] | select(.id == \"$upstream\") | .tracked_branch" "$REGISTRY")
    LAST_COMMIT=$(jq -r ".upstreams[] | select(.id == \"$upstream\") | .last_commit" "$REGISTRY")

    # Fetch latest commit via GitHub API
    LATEST=$(curl -s "https://api.github.com/repos/$URL/commits/$BRANCH" | jq -r '.sha')

    if [ "$LATEST" != "$LAST_COMMIT" ]; then
        echo "- **$upstream**: NEW CHANGES detected" >> "$REPORT"
        echo "  - Last known: ${LAST_COMMIT:0:8}" >> "$REPORT"
        echo "  - Latest: ${LATEST:0:8}" >> "$REPORT"

        # List changed skills
        # This would need git fetch + diff, simplified here
    else
        echo "- $upstream: Up to date" >> "$REPORT"
    fi
done

echo "Report saved to $REPORT"
```

#### `scripts/skills-sync/skill-diff.sh`

```bash
#!/usr/bin/env bash
# Show diff between our copy and upstream

SKILL_NAME=$1
UPSTREAM=$2

# Find skill in our tree
SKILL_PATH="skills/canonical/$SKILL_NAME/SKILL.md"

# Find upstream source
UPSTREAM_URL=$(jq -r ".upstreams[] | select(.id == \"$UPSTREAM\") | .url" skills/upstream-registry.json)

# Fetch upstream version
UPSTREAM_SKILL=$(curl -s "https://raw.githubusercontent.com/$UPSTREAM_URL/main/skills/$SKILL_NAME/SKILL.md")

# Show diff
echo "=== Diff: $SKILL_NAME ==="
echo "Upstream: $UPSTREAM_URL"
echo ""
diff -u "$SKILL_PATH" <(echo "$UPSTREAM_SKILL")
```

#### `scripts/skills-sync/bulk-refresh.sh`

```bash
#!/usr/bin/env bash
# Bulk refresh skills from upstream

UPSTREAM=$1
MODE=${2:-dry-run}  # dry-run | validate | import

REGISTRY="skills/upstream-registry.json"
VENDOR_PATH=$(jq -r ".upstreams[] | select(.id == \"$UPSTREAM\") | .local_vendor_path" "$REGISTRY")

echo "Bulk refresh from $UPSTREAM..."
echo "Mode: $MODE"
echo "Source: $VENDOR_PATH"

# Clone or pull latest
if [ -d "$VENDOR_PATH" ]; then
    git -C "$VENDOR_PATH" pull
else
    git clone "$UPSTREAM_URL" "$VENDOR_PATH"
fi

# For each skill in upstream
for skill_dir in "$VENDOR_PATH"/skills/*/; do
    skill_name=$(basename "$skill_dir")

    echo "Processing $skill_name..."

    case $MODE in
        dry-run)
            echo "  Would import: $skill_name"
            ;;
        validate)
            # Copy to sandbox and validate
            cp -r "$skill_dir" "sandbox/import-$UPSTREAM/"
            scripts/validate/validate-static.sh "sandbox/import-$UPSTREAM/$skill_name/SKILL.md"
            ;;
        import)
            # Full import pipeline
            scripts/import/skill-import.sh "$skill_dir" "$UPSTREAM"
            ;;
    esac
done
```

### Sync automation (CI/CD)

```yaml
# .github/workflows/skills-sync.yml
name: Skills Sync

on:
  schedule:
    - cron: '0 6 * * *'  # Daily at 6am
  workflow_dispatch:

jobs:
  check-updates:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check upstreams for updates
        run: |
          ./scripts/skills-sync/check-updates.sh

      - name: Create PR if changes detected
        run: |
          # Create PR from sandbox branch to staging
          # Include sync report in PR body
```

---

## Part 5: Import Execution Plan

### Phase 1: Security Infrastructure (PRIORITY)

**Before any bulk imports:**

1. Create sandbox branch
2. Implement `validate-static.sh` (Stage 1)
3. Implement `validate-content.sh` (Stage 2)
4. Test on markdown-mermaid-writing (already imported)
5. Create import PR template with security checklist

### Phase 2: Bulk Import (by source)

#### Step 2.1: K-Dense Scientific (143 skills)

**Why first**: Already local, trusted source, good test case

```bash
# Import script
for skill in ~/dev/claude-scientific-skills/scientific-skills/*/; do
    ./scripts/import/skill-import.sh "$skill" kdense-scientific
done
```

- Map to `domain/science/*` subdirectories
- Create pointers
- Validate each
- PR to sandbox → staging → main

#### Step 2.2: K-Dense Writer (~25 skills)

- Clone repo
- Extract from `skills/` subdirectory
- Import to `domain/science/writing/`

#### Step 2.3: Ghostsecurity (7 skills)

- Clone repo
- Import to `domain/security/appsec/`
- Validate (Apache-2.0 OK)

#### Step 2.4: Antigravity (882 skills)

**Why last**: Largest batch, validates infrastructure at scale

```bash
# Category mapping
declare -A CATEGORY_MAP=(
    ["architecture"]="development/architecture"
    ["business"]="business"
    ["data-ai"]="data/ai"
    ["development"]="development/languages"
    ["general"]="general"
    ["infrastructure"]="development/infrastructure"
    ["security"]="security"
    ["testing"]="development/testing"
    ["workflow"]="workflow"
)

# Import with category mapping
for category in "${!CATEGORY_MAP[@]}"; do
    for skill in vendor/antigravity-awesome-skills/skills/$category/*/; do
        ./scripts/import/skill-import.sh "$skill" antigravity "${CATEGORY_MAP[$category]}"
    done
done
```

---

## Part 6: Maintenance Dashboard

### Auto-generated `skills/MAINTENANCE.md`

```markdown
# Skill Maintenance Dashboard

_Generated: 2026-02-20_

## Upstream Health

| Upstream | Skills | Last Sync | Status | Behind By | Action |
|----------|--------|-----------|--------|-----------|--------|
| antigravity | 882 | 2026-02-20 | ✅ Current | — | — |
| kdense-scientific | 143 | 2026-02-20 | ⚠️ Behind | 3 commits | [Review changes](#) |
| kdense-writer | 25 | 2026-02-20 | ✅ Current | — | — |
| ghostsecurity | 7 | 2026-02-20 | ✅ Current | — | — |

## Validation Status

| Status | Count | Percentage |
|--------|-------|------------|
| ✅ Validated | 1,050 | 100% |
| ⏳ Pending | 0 | 0% |
| ❌ Failed | 0 | 0% |

## Recent Activity

- **2026-02-20**: Imported antigravity batch (882 skills)
- **2026-02-20**: Imported kdense-scientific (143 skills)
- **2026-02-20**: Implemented security validation pipeline
```

---

## Success Criteria

- [ ] All 1,050+ skills imported and validated
- [ ] Security sandbox blocks 100% of malicious patterns
n- [ ] Upstream sync detects changes within 24 hours
- [ ] Grep `what_it_does` works for all skills
- [ ] INDEX.json regenerates in < 5 seconds
- [ ] Domain tree browsable without loading canonical content

---

## Next Steps

1. **Approve this plan** — Review security model, metadata schema
2. **Implement security pipeline** — Stage 1 validation scripts
3. **Test on single skill** — Validate workflow with markdown-mermaid-writing
4. **Bulk import K-Dense** — 143 skills (trusted source)
5. **Scale to antigravity** — 882 skills (infrastructure test)

**Estimated effort**: 2-3 sessions for full implementation

---

_Plan created: 2026-02-20_
_Ready for execution via /start-work_
