#!/usr/bin/env bash
# build-index.sh — Regenerate skills/INDEX.json from canonical/ SKILL.md frontmatter
#
# Usage:  ./scripts/build-index.sh
#         ./scripts/build-index.sh --dry-run   (print to stdout, don't write)
#
# Idempotent: safe to run multiple times.
# Requires: python3, PyYAML (pip install pyyaml)
#
# AGENTS.md invariant: INDEX.json is always machine-generated, never hand-edited.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CANONICAL_DIR="$REPO_ROOT/skills/canonical"
OUTPUT="$REPO_ROOT/skills/INDEX.json"
DRY_RUN=false

# Parse flags
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=true ;;
    *) echo "Unknown flag: $arg"; exit 1 ;;
  esac
done

# Require python3 and PyYAML
if ! command -v python3 &>/dev/null; then
  echo "ERROR: python3 is required. Install it and retry." >&2
  exit 1
fi
if ! python3 -c "import yaml" 2>/dev/null; then
  echo "ERROR: PyYAML is required. Run: pip install pyyaml" >&2
  exit 1
fi

# Build index via Python (handles YAML frontmatter reliably)
python3 - <<'PYTHON' "$CANONICAL_DIR" "$OUTPUT" "$DRY_RUN"
import sys
import json
import os
import yaml
import re
from pathlib import Path

canonical_dir = Path(sys.argv[1])
output_path = Path(sys.argv[2])
dry_run = sys.argv[3] == "true"
repo_root = output_path.parent.parent  # skills/ -> repo root

skills = []

def extract_frontmatter(filepath: Path) -> dict:
    """Extract YAML frontmatter from a markdown file."""
    content = filepath.read_text(encoding="utf-8")
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}
    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}

def get_pointer_domains(skill_name: str, skills_dir: Path) -> list[str]:
    """Find all domain paths that point to this skill."""
    domain_dir = skills_dir / "domain"
    domains = []
    for ptr in domain_dir.rglob(f"{skill_name}.pointer.md"):
        # Convert path to domain notation: domain/science/writing
        rel = ptr.relative_to(domain_dir)
        domain_path = str(rel.parent)
        if domain_path not in domains:
            domains.append(domain_path)
    return domains

def get_bundle_memberships(skill_name: str, skills_dir: Path) -> list[str]:
    """Find all bundles that reference this skill."""
    bundles_dir = skills_dir / "bundles"
    memberships = []
    for bundle_file in bundles_dir.glob("*.md"):
        content = bundle_file.read_text(encoding="utf-8")
        if f"/{skill_name}/SKILL.md" in content:
            memberships.append(bundle_file.stem)
    return memberships

skills_dir = canonical_dir.parent  # skills/

# Walk canonical/
for skill_dir in sorted(canonical_dir.iterdir()):
    if not skill_dir.is_dir():
        continue
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        continue

    fm = extract_frontmatter(skill_file)
    skill_name = skill_dir.name

    # Canonical path relative to repo root
    canonical_path = str(skill_file.relative_to(repo_root))

    entry = {
        "skill": skill_name,
        "canonical": canonical_path,
        "description": str(fm.get("description", "")).strip(),
        "tags": fm.get("tags", []) or [],
        "domain": get_pointer_domains(skill_name, skills_dir),
        "bundles": get_bundle_memberships(skill_name, skills_dir),
        "upstream": fm.get("metadata", {}).get("skill-source", "") if fm.get("metadata") else "",
        "license": str(fm.get("license", "")).strip(),
        "load_frequency": str(fm.get("load_frequency", "medium")).strip(),
        "skill_author": fm.get("metadata", {}).get("skill-author", "") if fm.get("metadata") else "",
    }

    # Clean empty strings
    entry = {k: v for k, v in entry.items() if v != "" and v != []}
    skills.append(entry)

output_json = json.dumps(skills, indent=2)

if dry_run:
    print(output_json)
else:
    output_path.write_text(output_json + "\n", encoding="utf-8")
    print(f"INDEX.json regenerated: {len(skills)} skills")
PYTHON

if [ "$DRY_RUN" = "false" ]; then
  # Validate the output
  if ! python3 -c "import json; json.load(open('$OUTPUT'))" 2>/dev/null; then
    echo "ERROR: Generated INDEX.json is invalid. Check canonical/ SKILL.md frontmatter." >&2
    exit 1
  fi
  echo "Validation passed."
fi
