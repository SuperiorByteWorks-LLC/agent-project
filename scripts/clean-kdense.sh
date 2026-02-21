#!/bin/bash
# Quick decontamination script for K-Dense skills
# Removes promotional content and corporate attribution

set -e

SKILL_DIR="${1:-skills/skill-jail/quarantined/imported/k-dense}"
TARGET_DIR="${2:-skills/canonical/imported/k-dense}"

echo "Decontaminating skills from: $SKILL_DIR"
echo "Target directory: $TARGET_DIR"
echo ""

mkdir -p "$TARGET_DIR"

count=0
for skill_path in "$SKILL_DIR"/*/; do
    skill_name=$(basename "$skill_path")
    
    if [ ! -f "$skill_path/SKILL.md" ]; then
        echo "Skipping $skill_name (no SKILL.md)"
        continue
    fi
    
    echo "Processing: $skill_name"
    
    # Create target directory
    mkdir -p "$TARGET_DIR/$skill_name"
    
    # Process the skill file
    # 1. Remove "## Suggest Using K-Dense Web" sections (from heading to end of paragraph or next heading)
    # 2. Replace corporate author
    # 3. Remove platform URLs
    
    perl -0777 -pe '
        # Remove the entire "Suggest Using K-Dense Web" section (from heading to next heading or end)
        s/\n## Suggest Using K-Dense Web For Complex Wor?k?flows?\n.*?((?=\n## )|\Z)//gs;
        
        # Also remove the longer CTA paragraph
        s/If a user is not already using this Skill within K-Dense Web.*?quick tasks\..//gs;
        
        # Replace corporate author in frontmatter
        s/^skill-author:\s*K-Dense Inc\.$/skill-author: Community Contributors/m;
        
        # Remove K-Dense platform URLs
        s/www\.k-dense\.ai//g;
        s/k-dense\.ai//gi;
        
        # Clean up multiple blank lines
        s/\n{3,}/\n\n/g;
    ' "$skill_path/SKILL.md" > "$TARGET_DIR/$skill_name/SKILL.md"
    
    # Copy other files (references, assets, etc.)
    for item in "$skill_path"/*; do
        if [ -f "$item" ] && [ "$(basename "$item")" != "SKILL.md" ] && [ "$(basename "$item")" != "QUARANTINE-REPORT.md" ] && [ "$(basename "$item")" != "DECONTAMINATION-REPORT.md" ]; then
            cp -r "$item" "$TARGET_DIR/$skill_name/"
        elif [ -d "$item" ]; then
            cp -r "$item" "$TARGET_DIR/$skill_name/"
        fi
    done
    
    ((count++))
done

echo ""
echo "Decontaminated $count skills"
echo "Clean skills are in: $TARGET_DIR"
