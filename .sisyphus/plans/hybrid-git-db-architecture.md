# Hybrid Git + DB Architecture: Skills as Code

## Philosophy

**Git is the source of truth. The database is a build artifact.**

We keep canonical skills in Git (provenance, history, diffability). The database is generated from Git on-demand. Small deployments use JSON. Large deployments use DB. Both point to the same Git files.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     SOURCE OF TRUTH                          │
│                      (Git Repository)                        │
├─────────────────────────────────────────────────────────────┤
│ skills/                                                      │
│ ├── canonical/           ← Actual skill content (SSoT)    │
│ │   ├── typescript-expert/SKILL.md                         │
│ │   ├── scientific-writing/SKILL.md                        │
│ │   └── ...                                                │
│ ├── domain/              ← Navigation tree (pointers)      │
│ │   ├── science/                                           │
│ │   └── development/                                         │
│ ├── bundles/             ← Role-based collections          │
│ └── _core/               ← Always-loaded foundation        │
│                                                            │
│ INDEX.json               ← Generated (jq-compatible)       │
│ INDEX.db                 ← Generated (SQLite/PostgreSQL)     │
│ .db-version              ← Tracks which Git commit built DB│
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   GENERATED ARTIFACTS                        │
│              (Rebuilt from Git when stale)                   │
├─────────────────────────────────────────────────────────────┤
│ Small Scale (< 10K skills):                                 │
│   - Use INDEX.json directly                                 │
│   - jq-based queries                                        │
│   - No DB required                                          │
│                                                             │
│ Large Scale (10K+ skills):                                  │
│   - Generate INDEX.db from canonical skills                 │
│   - Query DB for speed                                      │
│   - Still reference canonical files by path                 │
└─────────────────────────────────────────────────────────────┘
```

---

## Directory Structure

```
skills/
├── canonical/                    ← SOURCE OF TRUTH
│   ├── markdown-mermaid-writing/
│   │   ├── SKILL.md             ← Content lives here
│   │   ├── assets/
│   │   └── references/
│   ├── typescript-expert/
│   ├── scientific-writing/
│   └── ... (1M+ skills here)
│
├── domain/                       ← Navigation (pointers)
│   └── science/
│       └── writing/
│           └── markdown-mermaid-writing.pointer.md
│
├── bundles/                      ← Role collections
│   └── scientist.md
│
├── _core/                        ← Foundation
│   ├── alignment.md
│   └── documentation.md
│
├── INDEX.json                    ← GENERATED (from canonical/)
├── INDEX.db                      ← GENERATED (SQLite/PostgreSQL)
└── .db-version                   ← Tracks Git commit hash
```

**Key Principle**: `canonical/` is the only place with actual skill content. Everything else (domain/, bundles/, INDEX.json, INDEX.db) is derived from `canonical/`.

---

## Build System

### Build Scripts

```bash
# scripts/build-index.sh
# Current: Generates INDEX.json
# Future: Also generates INDEX.db for large scale

# scripts/build-db.sh
# New: Generate SQLite/PostgreSQL from canonical/

# scripts/check-db-stale.sh
# New: Check if DB needs rebuild (compare .db-version to HEAD)
```

### Makefile

```makefile
# Makefile
.PHONY: all index db clean

all: index db

# Generate JSON index (always)
index:
	./scripts/build-index.sh

# Generate DB only if needed (checks .db-version)
db:
	./scripts/build-db.sh --if-stale

# Force rebuild DB
db-force:
	./scripts/build-db.sh --force

# Clean generated files
clean:
	rm -f skills/INDEX.json skills/INDEX.db skills/.db-version
```

### build-db.sh Logic

```bash
#!/usr/bin/env bash
# scripts/build-db.sh

DB_PATH="skills/INDEX.db"
VERSION_FILE="skills/.db-version"
CANONICAL_DIR="skills/canonical/"

# Get current Git commit
CURRENT_COMMIT=$(git rev-parse HEAD)

# Check if DB is stale
if [[ -f "$VERSION_FILE" && -f "$DB_PATH" ]]; then
    BUILT_COMMIT=$(cat "$VERSION_FILE")
    if [[ "$BUILT_COMMIT" == "$CURRENT_COMMIT" ]]; then
        echo "DB is up to date (commit: ${CURRENT_COMMIT:0:8})"
        exit 0
    fi
fi

echo "Building DB from canonical skills..."

# Create schema
sqlite3 "$DB_PATH" < scripts/db-schema.sql

# Import all canonical skills
python3 scripts/import-skills-to-db.py \
    --source "$CANONICAL_DIR" \
    --db "$DB_PATH"

# Create indices
echo "CREATE INDEX idx_name ON skills(name);" | sqlite3 "$DB_PATH"
echo "CREATE INDEX idx_domain ON skills(domain);" | sqlite3 "$DB_PATH"
echo "CREATE INDEX idx_tags ON skills(tags);" | sqlite3 "$DB_PATH"

# Track version
echo "$CURRENT_COMMIT" > "$VERSION_FILE"

echo "DB built: $DB_PATH"
echo "Skills indexed: $(sqlite3 $DB_PATH 'SELECT COUNT(*) FROM skills;')"
```

---

## Database Schema (SQLite for simplicity)

```sql
-- scripts/db-schema.sql
-- Minimal schema - just what's needed for fast queries

-- Skills table (metadata only, content read from disk)
CREATE TABLE skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(64) UNIQUE NOT NULL,
    canonical_path VARCHAR(512) NOT NULL,
    description TEXT,
    domain VARCHAR(64),
    subdomain VARCHAR(64),
    -- Arrays stored as JSON strings
    tags JSON,
    bundles JSON,
    -- Source tracking
    upstream_url VARCHAR(512),
    license VARCHAR(32),
    import_date TIMESTAMP,
    import_commit VARCHAR(40),
    -- For change detection
    content_hash VARCHAR(64),
    -- Search
    search_text TEXT  -- Concatenated fields for full-text search
);

-- Full-text search using FTS5
CREATE VIRTUAL TABLE skills_fts USING fts5(
    name,
    description,
    search_text,
    content='skills',
    content_rowid='id'
);

-- Pointers table (for domain navigation)
CREATE TABLE pointers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill_id INTEGER REFERENCES skills(id),
    domain VARCHAR(64),
    subdomain VARCHAR(64),
    pointer_path VARCHAR(512)
);

-- Keep it simple - no complex relations
-- Just what's needed for fast lookup
```

---

## Hybrid Query API

### Query Router (Python)

```python
# skills/query.py

import json
import sqlite3
import subprocess
from pathlib import Path

class SkillQuery:
    def __init__(self, skills_root: Path):
        self.skills_root = skills_root
        self.json_path = skills_root / "INDEX.json"
        self.db_path = skills_root / "INDEX.db"
        
    def query(self, q: str, limit: int = 10) -> List[SkillResult]:
        """Route to appropriate backend based on scale."""
        
        # Check if DB exists and is fresh
        if self._should_use_db():
            return self._query_db(q, limit)
        else:
            return self._query_json(q, limit)
    
    def _should_use_db(self) -> bool:
        """Use DB if: exists, is fresh, and scale > threshold."""
        if not self.db_path.exists():
            return False
            
        # Check if DB is stale
        version_file = self.skills_root / ".db-version"
        if not version_file.exists():
            return False
            
        built_commit = version_file.read_text().strip()
        current_commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True
        ).stdout.strip()
        
        if built_commit != current_commit:
            print("Warning: DB is stale. Run: make db")
            return False
        
        # Count skills - use DB if > 10K
        skill_count = self._count_skills()
        return skill_count > 10000
    
    def _query_json(self, q: str, limit: int) -> List[SkillResult]:
        """Use jq for small scale."""
        import subprocess
        
        jq_query = f'''
            .[] | select(
                (.name | contains("{q}")) or
                (.description | contains("{q}")) or
                (.tags | contains(["{q}"]))
            ) | {{name, description, canonical}}
        '''
        
        result = subprocess.run(
            ["jq", "-c", jq_query, str(self.json_path)],
            capture_output=True, text=True
        )
        
        return [json.loads(line) for line in result.stdout.strip().split('\n')][:limit]
    
    def _query_db(self, q: str, limit: int) -> List[SkillResult]:
        """Use SQLite FTS for large scale."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        
        # Use FTS5 for fast full-text search
        cursor = conn.execute("""
            SELECT s.name, s.description, s.canonical_path
            FROM skills_fts
            JOIN skills s ON skills_fts.rowid = s.id
            WHERE skills_fts MATCH ?
            ORDER BY rank
            LIMIT ?
        """, (q, limit))
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results
```

---

## Git Workflows

### Development Workflow

```bash
# 1. Add/modify skill in canonical/
vim skills/canonical/new-skill/SKILL.md

# 2. Rebuild indices
make all

# 3. Check what changed
git diff skills/INDEX.json

# 4. Commit both skill + generated index
git add skills/canonical/new-skill/
git add skills/INDEX.json
# DB is gitignored - generated on deploy
git commit -m "feat(skills): add new-skill"
```

### Deployment Workflow

```bash
# On target machine:
git clone <repo>
cd agents-skills-tree

# Build indices from canonical skills
make all

# Now ready to serve
./scripts/serve.sh  # Uses JSON if < 10K skills, DB if >= 10K
```

### CI/CD

```yaml
# .github/workflows/build-db.yml
name: Build Skill Indices

on:
  push:
    paths:
      - 'skills/canonical/**'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Build indices
        run: make all
      
      - name: Verify DB is fresh
        run: ./scripts/check-db-stale.sh
      
      - name: Commit generated files
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add skills/INDEX.json
          git commit -m "chore(build): regenerate indices" || echo "No changes"
          git push
```

---

## Scale Thresholds

| Scale | Mode | Latency | When to Switch |
|-------|------|---------|----------------|
| < 1K | JSON + jq | ~200ms | Default |
| 1K - 10K | JSON + jq | ~1s | Still fine |
| 10K - 100K | DB required | ~50ms | Auto-detect |
| 100K+ | DB + caching | ~20ms | Must use DB |

**Auto-detection**:
```python
# Automatically choose backend
def auto_select_backend(skill_count: int) -> str:
    if skill_count < 10000:
        return "json"  # Simple, no dependencies
    else:
        return "db"    # Required for performance
```

---

## Provenance Tracking

### Git Commit in Metadata

Every skill has:
```yaml
---
name: typescript-expert
metadata:
  imported-from: "https://github.com/sickn33/antigravity-awesome-skills"
  import-commit: "a1b2c3d4e5f6789..."
  import-date: "2026-02-20"
  # DB tracks: db-built-from-commit: "f2g3h4i5..."
---
```

### DB Version Tracking

```bash
# skills/.db-version
cat skills/.db-version
# Output: f2g3h4i5j6k7l8m9n0o1p2q3r4s5t6u7v8w9x0y1z2

# Compare to current Git HEAD
git rev-parse HEAD
# Output: f2g3h4i5j6k7l8m9n0o1p2q3r4s5t6u7v8w9x0y1z2

# If different, DB is stale
```

---

## CLI Tool

```bash
# skills query tool
skill-query "typescript authentication"
# Output: json array of matching skills

# Force specific backend
skill-query "python" --backend=json
skill-query "python" --backend=db

# Rebuild indices
skill-query --rebuild

# Check staleness
skill-query --check-stale

# Export skill
skill-query export typescript-expert --output=./my-skill.md
```

---

## Migration from Current

```bash
# 1. Current state: 1 skill in JSON
ls skills/INDEX.json  # exists
ls skills/INDEX.db    # doesn't exist

# 2. Add more skills to canonical/
cp -r ~/dev/claude-scientific-skills/scientific-skills/*/ skills/canonical/

# 3. Rebuild indices
make all

# 4. Now we have:
# - skills/canonical/ (100+ skills)
# - skills/INDEX.json (rebuilt)
# - skills/INDEX.db (new, if > 10K skills)

# 5. Git commit
git add skills/canonical/ skills/INDEX.json
git commit -m "feat(skills): import 143 K-Dense scientific skills"

# Note: INDEX.db is in .gitignore - generated on deploy
```

---

## Summary

**Git = Source of Truth**
- `skills/canonical/` - actual skill content
- `skills/domain/` - navigation pointers
- `skills/bundles/` - role collections

**Generated = Fast Query**
- `skills/INDEX.json` - jq-compatible (small scale)
- `skills/INDEX.db` - SQLite/PostgreSQL (large scale)

**Workflow**
1. Edit skills in Git
2. Run `make all` to rebuild indices
3. Commit Git changes (includes INDEX.json)
4. DB is regenerated on deployment

**Benefits**
- ✅ Full provenance in Git
- ✅ Fast queries via DB (when needed)
- ✅ Simple JSON fallback (small scale)
- ✅ Scales from 1 to 1M+ skills
- ✅ No DB vendor lock-in
- ✅ Skills remain "code" (diffable, reviewable)

---

_This architecture keeps skills as code while enabling massive scale._
