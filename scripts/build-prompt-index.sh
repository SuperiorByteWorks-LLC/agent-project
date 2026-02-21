#!/bin/bash
#
# Build Prompt Index
# Generates INDEX.json from canonical/ frontmatter
#
# Usage:
#   ./scripts/build-prompt-index.sh
#   ./scripts/build-prompt-index.sh --watch

set -e

PROMPTS_ROOT="prompts"
CANONICAL_ROOT="$PROMPTS_ROOT/canonical"
INDEX_FILE="$PROMPTS_ROOT/INDEX.json"

echo "Building prompt index..."

# Create temporary file
TEMP_FILE=$(mktemp)

# Start JSON array
echo "[" > "$TEMP_FILE"

FIRST=true

# Find all PROMPT.md files in canonical/
find "$CANONICAL_ROOT" -name "PROMPT.md" -type f | while read -r prompt_file; do
    # Get relative path from prompts/
    rel_path="${prompt_file#$PROMPTS_ROOT/}"
    
    # Extract frontmatter
    frontmatter=$(sed -n '/^---$/,/^---$/p' "$prompt_file" | sed '1d;$d')
    
    # Parse name
    name=$(echo "$frontmatter" | grep "^name:" | cut -d: -f2- | sed 's/^[[:space:]]*//')
    
    # Parse description
    description=$(echo "$frontmatter" | grep "^description:" | cut -d: -f2- | sed 's/^[[:space:]]*//')
    
    # Parse domain
    domain=$(echo "$frontmatter" | grep "^domain:" | cut -d: -f2- | sed 's/^[[:space:]]*//')
    
    # Parse tags
    tags=$(echo "$frontmatter" | grep "^tags:" | cut -d: -f2- | sed 's/^[[:space:]]*//')
    
    # Parse source
    source=$(echo "$frontmatter" | grep "^source:" | cut -d: -f2- | sed 's/^[[:space:]]*//')
    
    # Add comma if not first
    if [ "$FIRST" = true ]; then
        FIRST=false
    else
        echo "," >> "$TEMP_FILE"
    fi
    
    # Write JSON entry
    cat >> "$TEMP_FILE" << ENTRY
  {
    "prompt": "$name",
    "canonical": "$rel_path",
    "description": "${description//"/\\"}",
    "domain": "$domain",
    "tags": [$tags],
    "source": "$source"
  }
ENTRY
done

# Close JSON array
echo "" >> "$TEMP_FILE"
echo "]" >> "$TEMP_FILE"

# Move to final location
mv "$TEMP_FILE" "$INDEX_FILE"

echo "Index built: $INDEX_FILE"
echo "Total prompts: $(grep -c '"prompt":' "$INDEX_FILE" 2>/dev/null || echo "0")"
