#!/usr/bin/env python3
"""Import skills from upstream sources into canonical/."""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).parent.parent.resolve()
SKILLS_DIR = REPO_ROOT / "skills" / "canonical"


def import_kdense_scientific():
    """Import K-Dense scientific-skills."""
    source_dir = Path.home() / "dev" / "claude-scientific-skills" / "scientific-skills"
    upstream_url = "https://github.com/K-Dense-AI/claude-scientific-skills"

    if not source_dir.exists():
        print(f"ERROR: Source directory not found: {source_dir}")
        return 0, 0

    # Get commit hash
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=source_dir, capture_output=True, text=True
        )
        import_commit = result.stdout.strip()[:8]
    except Exception:
        import_commit = "unknown"

    imported = 0
    failed = 0

    for skill_path in source_dir.iterdir():
        if not skill_path.is_dir():
            continue

        skill_name = skill_path.name
        target_path = SKILLS_DIR / skill_name

        if target_path.exists():
            print(f"SKIP: {skill_name} (already exists)")
            continue

        try:
            shutil.copytree(skill_path, target_path)

            # Add import metadata
            skill_md = target_path / "SKILL.md"
            if skill_md.exists():
                content = skill_md.read_text()
                if "imported-from:" not in content:
                    # Add metadata after frontmatter
                    lines = content.split("\n")
                    frontmatter_end = lines.index("---", 1) if "---" in lines[1:] else len(lines)

                    import_meta = f"""  imported-from: {upstream_url}
  import-date: "{datetime.now().strftime("%Y-%m-%d")}"
  import-commit: "{import_commit}"
---"""

                    lines.insert(frontmatter_end, import_meta)
                    skill_md.write_text("\n".join(lines))

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
    print("Importing K-Dense scientific-skills...\n")
    imported, failed = import_kdense_scientific()

    print(f"\nImport complete:")
    print(f"  Imported: {imported}")
    print(f"  Failed: {failed}")

    if imported > 0:
        regenerate_index()
