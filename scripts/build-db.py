#!/usr/bin/env python3
"""Build SQLite database from canonical skills."""

import json
import sqlite3
import subprocess
import sys
from pathlib import Path
import yaml

REPO_ROOT = Path(__file__).parent.parent.resolve()
CANONICAL_DIR = REPO_ROOT / "skills" / "canonical"
DB_PATH = REPO_ROOT / "skills" / "INDEX.db"
SCHEMA_PATH = REPO_ROOT / "scripts" / "db-schema.sql"


def get_git_commit():
    """Get current Git commit hash."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, capture_output=True, text=True
        )
        return result.stdout.strip()
    except Exception:
        return "unknown"


def parse_frontmatter(skill_md_path):
    """Parse YAML frontmatter from SKILL.md."""
    try:
        content = skill_md_path.read_text()
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = yaml.safe_load(parts[1])
                return frontmatter
    except Exception as e:
        print(f"Warning: Failed to parse {skill_md_path}: {e}")
    return {}


def build_database():
    """Build SQLite database from canonical skills."""
    print("Building skill database...")
    print(f"Source: {CANONICAL_DIR}")
    print(f"Target: {DB_PATH}")

    # Remove old DB
    if DB_PATH.exists():
        DB_PATH.unlink()

    # Create new DB
    conn = sqlite3.connect(DB_PATH)

    # Load schema
    schema = SCHEMA_PATH.read_text()
    conn.executescript(schema)

    cursor = conn.cursor()

    # Process each skill
    imported = 0
    for skill_dir in CANONICAL_DIR.iterdir():
        if not skill_dir.is_dir():
            continue

        skill_name = skill_dir.name
        skill_md = skill_dir / "SKILL.md"

        if not skill_md.exists():
            print(f"Warning: No SKILL.md for {skill_name}")
            continue

        # Parse frontmatter
        fm = parse_frontmatter(skill_md)
        if not fm:
            continue

        # Extract fields
        if not fm:
            continue

        canonical_path = f"skills/canonical/{skill_name}/SKILL.md"
        description = fm.get("description", "")
        domain = (
            ",".join(fm.get("domain", []))
            if isinstance(fm.get("domain"), list)
            else fm.get("domain", "")
        )
        tags = (
            ",".join(fm.get("tags", []))
            if isinstance(fm.get("tags"), list)
            else str(fm.get("tags", ""))
        )
        bundles = ",".join(fm.get("bundles", [])) if isinstance(fm.get("bundles"), list) else ""
        metadata = fm.get("metadata", {}) or {}
        upstream = fm.get("upstream", "") or metadata.get("imported-from", "")
        license_field = fm.get("license", "")
        load_frequency = fm.get("load_frequency", "medium")
        skill_author = fm.get("skill-author", "")

        # Create search text
        search_text = f"{skill_name} {description} {tags} {domain}"

        # Insert into skills table
        cursor.execute(
            """
            INSERT INTO skills 
            (name, canonical_path, description, domain, tags, bundles, 
             upstream_url, license, load_frequency, skill_author, search_text)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                skill_name,
                canonical_path,
                description,
                domain,
                tags,
                bundles,
                upstream,
                license_field,
                load_frequency,
                skill_author,
                search_text,
            ),
        )

        imported += 1
        if imported % 100 == 0:
            print(f"  Processed {imported} skills...")

    # Track version
    commit_hash = get_git_commit()
    cursor.execute(
        """
        INSERT INTO db_version (commit_hash, built_at, skill_count)
        VALUES (?, datetime('now'), ?)
    """,
        (commit_hash, imported),
    )

    conn.commit()
    conn.close()

    print(f"\nDatabase built successfully:")
    print(f"  Skills indexed: {imported}")
    print(f"  Database: {DB_PATH}")
    print(f"  Commit: {commit_hash[:8]}")


if __name__ == "__main__":
    build_database()
