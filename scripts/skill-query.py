#!/usr/bin/env python3
"""Query skills using JSON or DB backend based on scale."""

import json
import sqlite3
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
JSON_PATH = REPO_ROOT / "skills" / "INDEX.json"
DB_PATH = REPO_ROOT / "skills" / "INDEX.db"


def get_skill_count():
    """Count skills in canonical directory."""
    canonical = REPO_ROOT / "skills" / "canonical"
    return len([d for d in canonical.iterdir() if d.is_dir()])


def should_use_db():
    """Auto-select backend based on skill count."""
    if not DB_PATH.exists():
        return False

    count = get_skill_count()
    return count >= 1000  # Switch to DB at 1000+ skills


def query_json(q, limit=10):
    """Query using jq (JSON backend)."""
    start = time.time()

    # Build jq query
    jq_filter = f'''
        .[] | select(
            (.name | ascii_downcase | contains("{q.lower()}")) or
            (.description | ascii_downcase | contains("{q.lower()}")) or
            (.tags | map(ascii_downcase) | contains(["{q.lower()}"]))
        ) | {{
            name: .name,
            description: (.description | split(" ")[:20] | join(" ")),
            canonical: .canonical,
            upstream: .upstream
        }}
    '''

    result = subprocess.run(["jq", "-c", jq_filter, str(JSON_PATH)], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"jq error: {result.stderr}")
        return []

    lines = [l for l in result.stdout.strip().split("\n") if l]
    results = [json.loads(line) for line in lines[:limit]]

    elapsed = time.time() - start
    return results, elapsed


def query_db(q, limit=10):
    """Query using SQLite (DB backend)."""
    start = time.time()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Use LIKE for now - FTS needs population
    like_q = f"%{q}%"
    cursor.execute(
        """
        SELECT name, description, canonical_path, upstream_url
        FROM skills
        WHERE name LIKE ? OR description LIKE ? OR tags LIKE ?
        LIMIT ?
    """,
        (like_q, like_q, like_q, limit),
    )

    results = [dict(row) for row in cursor.fetchall()]
    conn.close()

    elapsed = time.time() - start
    return results, elapsed


def query_hybrid(q, limit=10):
    """Auto-select and query."""
    if should_use_db():
        print(f"[Using DB backend - {get_skill_count()} skills]")
        return query_db(q, limit)
    else:
        print(f"[Using JSON backend - {get_skill_count()} skills]")
        return query_json(q, limit)


def main():
    if len(sys.argv) < 2:
        print("Usage: skill-query.py <query> [--limit=N]")
        print("Examples:")
        print("  skill-query.py typescript")
        print("  skill-query.py 'scientific writing' --limit=5")
        sys.exit(1)

    q = sys.argv[1]
    limit = 10

    for arg in sys.argv[2:]:
        if arg.startswith("--limit="):
            limit = int(arg.split("=")[1])

    results, elapsed = query_hybrid(q, limit)

    print(f"\nFound {len(results)} results in {elapsed:.3f}s:\n")

    for i, r in enumerate(results, 1):
        name = r.get("name", "unknown")
        desc = r.get("description", "")[:80]
        upstream = r.get("upstream", r.get("upstream_url", ""))
        print(f"{i}. {name}")
        print(f"   {desc}..." if len(desc) >= 80 else f"   {desc}")
        if upstream:
            print(f"   Source: {upstream[:50]}...")
        print()


if __name__ == "__main__":
    main()
