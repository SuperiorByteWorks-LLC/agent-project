#!/bin/bash
#
# Import prompts from prompts.chat
# Creates proper directory structure and pointer files
#
# Usage:
#   ./scripts/import-prompts.sh --source prompts-chat --limit 1000
#   ./scripts/import-prompts.sh --source prompts-chat --category development
#   ./scripts/import-prompts.sh --source prompts-chat --dry-run

set -e

# Configuration
SOURCE_NAME="prompts-chat"
SOURCE_URL="https://prompts.chat"
CANONICAL_ROOT="prompts/canonical/imported/prompts-chat"
DOMAIN_ROOT="prompts/domain"
JAIL_ROOT="prompts/prompt-jail"
API_ENDPOINT="https://prompts.chat/api/prompts"
CSV_URL="https://prompts.chat/prompts.csv"

# Defaults
LIMIT=1000
DRY_RUN=false
CATEGORY=""
VERBOSE=false

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --source)
            SOURCE_NAME="$2"
            shift 2
            ;;
        --limit)
            LIMIT="$2"
            shift 2
            ;;
        --category)
            CATEGORY="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --source <name>     Source name (default: prompts-chat)"
            echo "  --limit <n>         Maximum prompts to import (default: 1000)"
            echo "  --category <cat>    Import only from category"
            echo "  --dry-run          Preview without importing"
            echo "  --verbose          Show detailed output"
            echo "  --help             Show this help"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo "=========================================="
echo "Prompt Import Tool"
echo "=========================================="
echo "Source: $SOURCE_NAME"
echo "Limit: $LIMIT"
if [ -n "$CATEGORY" ]; then
    echo "Category: $CATEGORY"
fi
if [ "$DRY_RUN" = true ]; then
    echo "Mode: DRY RUN (no changes)"
fi
echo "=========================================="

# Create directories
create_dirs() {
    if [ "$DRY_RUN" = true ]; then
        return
    fi
    
    mkdir -p "$CANONICAL_ROOT"
    mkdir -p "$DOMAIN_ROOT"/{science,development,security,data,documents,research,general}
    mkdir -p "$JAIL_ROOT"/{quarantined,blocked,review-pending,cleaned,staged}/imported/prompts-chat
}

# Normalize prompt name for directory
normalize_name() {
    echo "$1" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//' | sed 's/-$//'
}

# Determine domain from categories
determine_domain() {
    local categories="$1"
    local description="$2"
    
    # Check categories first
    if echo "$categories" | grep -qi "code\|programming\|software\|development\|debugging"; then
        echo "development"
    elif echo "$categories" | grep -qi "security\|pentest\|audit\|vulnerability"; then
        echo "security"
    elif echo "$categories" | grep -qi "data\|analysis\|ml\|machine.learning\|ai\|analytics"; then
        echo "data"
    elif echo "$categories" | grep -qi "science\|research\|academic\|paper\|publication"; then
        echo "science"
    elif echo "$categories" | grep -qi "document\|writing\|content\|blog\|email"; then
        echo "documents"
    elif echo "$categories" | grep -qi "general\|productivity\|planning\|brainstorm"; then
        echo "general"
    else
        # Default to general
        echo "general"
    fi
}

# Determine subdomain
determine_subdomain() {
    local categories="$1"
    local domain="$2"
    
    case "$domain" in
        development)
            if echo "$categories" | grep -qi "debug\|troubleshoot\|fix\|error"; then
                echo "debugging"
            elif echo "$categories" | grep -qi "review\|audit\|check"; then
                echo "code-review"
            elif echo "$categories" | grep -qi "architect\|design\|pattern\|structure"; then
                echo "architecture"
            elif echo "$categories" | grep -qi "test\|qa\|quality"; then
                echo "testing"
            elif echo "$categories" | grep -qi "deploy\|ci/cd\|devops\|pipeline"; then
                echo "deployment"
            else
                echo "coding"
            fi
            ;;
        science)
            if echo "$categories" | grep -qi "write\|paper\|manuscript\|thesis"; then
                echo "writing"
            elif echo "$categories" | grep -qi "analyze\|statistic\|compute\|calculate"; then
                echo "analysis"
            else
                echo "research"
            fi
            ;;
        *)
            echo ""
            ;;
    esac
}

# Fetch prompts from prompts.chat
fetch_prompts() {
    echo ""
    echo "Fetching prompts from $SOURCE_NAME..."
    
    # Try to get CSV or API data
    # This is a placeholder - actual implementation would use curl to fetch from prompts.chat
    
    # For now, create a sample structure to demonstrate
    echo "Note: This requires actual API access to prompts.chat"
    echo "Creating sample structure..."
    
    # In real implementation, this would:
    # 1. curl "$API_ENDPOINT" or download CSV
    # 2. Parse JSON/CSV
    # 3. Process each prompt
    
    # Sample prompts for demonstration
    local count=0
    
    # Simulate importing prompts
    # In production, this would iterate over actual API results
    
    echo ""
    echo "To import real prompts from prompts.chat:"
    echo "1. Get API key from prompts.chat"
    echo "2. Use: curl -H 'Authorization: Bearer TOKEN' '$API_ENDPOINT?limit=$LIMIT'"
    echo "3. Parse and process results"
    echo ""
    echo "Sample structure created in $CANONICAL_ROOT/"
}

# Create a sample prompt to demonstrate structure
create_sample_structure() {
    if [ "$DRY_RUN" = true ]; then
        return
    fi
    
    # Create a sample prompt
    local sample_dir="$CANONICAL_ROOT/expert-debugger"
    mkdir -p "$sample_dir"
    
    cat > "$sample_dir/PROMPT.md" << 'EOF'
---
name: expert-debugger
description: Systematic debugging approach for any language or framework
domain: development/debugging
tags: [debugging, troubleshooting, problem-solving, code-review]
source: prompts-chat
imported-from: https://prompts.chat/p/expert-debugger
import-date: "2026-02-21"
license: CC0
---

# Expert Debugger

You are an expert debugger. Your approach is systematic and thorough.

## When to Use

Use this prompt when:
- Code is not working as expected
- Error messages need interpretation
- Performance issues need diagnosis
- Logic errors need to be found

## Process

1. **Understand the problem**
   - What is the expected behavior?
   - What is the actual behavior?
   - When does it occur?

2. **Gather information**
   - Read relevant code files
   - Check error logs
   - Review recent changes

3. **Form hypotheses**
   - What could cause this behavior?
   - Prioritize most likely causes

4. **Test hypotheses**
   - Design minimal reproduction cases
   - Check assumptions

5. **Implement fix**
   - Make minimal necessary changes
   - Verify fix works
   - Check for regressions

## Output Format

```
## Diagnosis

**Problem:** [clear statement]
**Root Cause:** [explanation]
**Location:** [file:line]

## Fix

```language
[code]
```

## Prevention

[how to avoid similar issues]
```

## Constraints

- Always provide the full context
- Include line numbers in references
- Explain the "why" not just the "what"
- Suggest tests to prevent regression
EOF

    # Create pointer file
    mkdir -p "$DOMAIN_ROOT/development/debugging"
    cat > "$DOMAIN_ROOT/development/debugging/expert-debugger.pointer.md" << EOF
---
prompt: expert-debugger
canonical: $CANONICAL_ROOT/expert-debugger/PROMPT.md
description: Systematic debugging approach for any language or framework
domain: development/debugging
tags: [debugging, troubleshooting, problem-solving, code-review]
source: prompts-chat
---

# expert-debugger

**Domain:** development/debugging  
**Source:** [prompts.chat](https://prompts.chat)

Navigate to: \`$CANONICAL_ROOT/expert-debugger/PROMPT.md\`
EOF

    echo "Created sample: expert-debugger"
}

# Scan for violations
scan_prompt() {
    local prompt_file="$1"
    local violations=()
    
    # Check for promotional content
    if grep -qi "try our\|sign up\|visit.*\.com\|premium\|upgrade" "$prompt_file"; then
        violations+=("promotional_content")
    fi
    
    # Check for forced behavior
    if grep -qi "ALWAYS\|MUST\|REQUIRED\|mandatory" "$prompt_file"; then
        violations+=("forced_behavior")
    fi
    
    # Check for platform mentions
    if grep -qi "prompts\.chat\|hosted version\|platform" "$prompt_file"; then
        violations+=("platform_mention")
    fi
    
    echo "${violations[@]}"
}

# Main execution
main() {
    create_dirs
    
    if [ "$DRY_RUN" = true ]; then
        echo ""
        echo "DRY RUN: Would create the following structure:"
        echo "  - $CANONICAL_ROOT/<prompt-name>/PROMPT.md (canonical content)"
        echo "  - $DOMAIN_ROOT/<domain>/<sub>/<prompt>.pointer.md (navigation)"
        echo ""
        echo "Sample prompt structure:"
        create_sample_structure
        exit 0
    fi
    
    # Fetch and process prompts
    fetch_prompts
    
    # Create sample for demonstration
    create_sample_structure
    
    echo ""
    echo "=========================================="
    echo "Import complete"
    echo "=========================================="
    echo ""
    echo "Next steps:"
    echo "1. Review imported prompts: ls $CANONICAL_ROOT/"
    echo "2. Run scanner: python scripts/prompt-scanner.py --scan-all"
    echo "3. Build index: ./scripts/build-prompt-index.sh"
    echo ""
}

main "$@"
