#!/usr/bin/env python3
"""Import ghostsecurity skills into canonical/."""

import shutil
import subprocess
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).parent.parent.resolve()
SKILLS_DIR = REPO_ROOT / "skills" / "canonical"
GHOST_DIR = Path("/tmp/ghostsecurity-skills")


def import_ghostsecurity():
    """Import ghostsecurity skills."""
    skills_root = GHOST_DIR / "plugins" / "ghost" / "skills"
    upstream_url = "https://github.com/ghostsecurity/skills"

    if not skills_root.exists():
        print(f"ERROR: Ghostsecurity skills directory not found: {skills_root}")
        return 0, 0

    imported = 0
    failed = 0

    for skill_path in skills_root.iterdir():
        if not skill_path.is_dir():
            continue

        skill_name = f"ghost-{skill_path.name}"  # Prefix to avoid conflicts
        target_path = SKILLS_DIR / skill_name

        if target_path.exists():
            print(f"SKIP: {skill_name} (already exists)")
            continue

        try:
            shutil.copytree(skill_path, target_path)
            imported += 1
            print(f"IMPORT: {skill_name}")
        except Exception as e:
            failed += 1
            print(f"FAIL: {skill_name} - {e}")

    return imported, failed


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
    print("Importing ghostsecurity skills...\n")
    imported, failed = import_ghostsecurity()

    print(f"\nImport complete:")
    print(f"  Imported: {imported}")
    print(f"  Failed: {failed}")

    if imported > 0:
        regenerate_index()
