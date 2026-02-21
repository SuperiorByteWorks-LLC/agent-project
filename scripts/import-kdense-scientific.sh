#!/usr/bin/env bash
# Import K-Dense scientific-skills into canonical/

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SOURCE_DIR="$HOME/dev/claude-scientific-skills/scientific-skills"
TARGET_DIR="$REPO_ROOT/skills/canonical"
DOMAIN_DIR="$REPO_ROOT/skills/domain/science"

UPSTREAM_URL="https://github.com/K-Dense-AI/claude-scientific-skills"
IMPORT_DATE="2026-02-20"
IMPORT_COMMIT=$(cd "$SOURCE_DIR" && git rev-parse HEAD 2>/dev/null || echo "unknown")

echo "Importing K-Dense scientific-skills..."
echo "Source: $SOURCE_DIR"
echo "Target: $TARGET_DIR"
echo "Upstream: $UPSTREAM_URL"
echo "Import commit: ${IMPORT_COMMIT:0:8}"
echo ""

# Counters
IMPORTED=0
FAILED=0

# Process each skill
for skill_dir in "$SOURCE_DIR"/*/; do
    skill_name=$(basename "$skill_dir")
    target_skill_dir="$TARGET_DIR/$skill_name"
    
    echo -n "Importing: $skill_name... "
    
    # Skip if already exists
    if [[ -d "$target_skill_dir" ]]; then
        echo "SKIPPED (already exists)"
        continue
    fi
    
    # Copy skill directory
    if cp -r "$skill_dir" "$target_skill_dir"; then
        # Add import metadata to SKILL.md if it exists
        if [[ -f "$target_skill_dir/SKILL.md" ]]; then
            # Check if already has import metadata
            if ! grep -q "imported-from:" "$target_skill_dir/SKILL.md"; then
                # Add import metadata after license line or at end of frontmatter
                sed -i '/^---$/{
                    N
                    /license:/a\  imported-from: '"$UPSTREAM_URL"'\n  import-date: '"$IMPORT_DATE"'\n  import-commit: '"$IMPORT_COMMIT"'
                }' "$target_skill_dir/SKILL.md" 2>/dev/null || true
            fi
        fi
        
        ((IMPORTED++))
        echo "OK"
    else
        ((FAILED++))
        echo "FAILED"
    fi
done

echo ""
echo "Import complete:"
echo "  Imported: $IMPORTED"
echo "  Failed: $FAILED"
echo ""

# Regenerate index
echo "Regenerating INDEX.json..."
cd /home/clay/dev/opencode-worktrees/agents-skills-tree
./scripts/build-index.sh

echo "Done!"
