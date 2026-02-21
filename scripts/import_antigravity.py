#!/usr/bin/env python3
"""Import ALL antigravity-awesome-skills into canonical/."""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).parent.parent.resolve()
SKILLS_DIR = REPO_ROOT / "skills" / "canonical"
ANTIGRAVITY_DIR = Path("/tmp/antigravity-awesome-skills")

CATEGORY_MAP = {
    "architecture": "development/architecture",
    "business": "business",
    "data-ai": "data/ai",
    "development": "development/languages",
    "general": "general",
    "infrastructure": "development/infrastructure",
    "security": "security",
    "testing": "development/testing",
    "workflow": "workflow",
}


def import_antigravity_skills():
    """Import all antigravity skills (flat structure)."""
    skills_root = ANTIGRAVITY_DIR / "skills"
    upstream_url = "https://github.com/sickn33/antigravity-awesome-skills"

    if not skills_root.exists():
        print(f"ERROR: Antigravity skills directory not found: {skills_root}")
        return 0, 0, 0

    imported = 0
    failed = 0
    skipped = 0

    # Antigravity has flat structure: skills/<skill-name>/
    for skill_path in skills_root.iterdir():
        if not skill_path.is_dir():
            continue

        skill_name = skill_path.name
        target_path = SKILLS_DIR / skill_name

        if target_path.exists():
            skipped += 1
            continue

        try:
            shutil.copytree(skill_path, target_path)
            imported += 1

            if imported % 100 == 0:
                print(f"Progress: {imported} imported...")

        except Exception as e:
            failed += 1
            print(f"FAIL: {skill_name} - {e}")

    return imported, failed, skipped


def regenerate_index():
    """Run build-index.sh to regenerate INDEX.json."""
    print("\nRegenerating INDEX.json...")
    result = subprocess.run(
        ["bash", "scripts/build-index.sh"], cwd=REPO_ROOT, capture_output=True, text=True
    )
    if result.returncode == 0:
        print("Index regenerated successfully")
    else:
        print(f"Index regeneration failed: {result.stderr}")


if __name__ == "__main__":
    print("Importing ALL antigravity-awesome-skills...\n")
    imported, failed, skipped = import_antigravity_skills()

    print(f"\nImport complete:")
    print(f"  Imported: {imported}")
    print(f"  Failed: {failed}")
    print(f"  Skipped (already exists): {skipped}")

    if imported > 0:
        regenerate_index()
