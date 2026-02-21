#!/usr/bin/env python3
"""Populate domain/ tree with pointers to canonical skills."""

import json
import os
from pathlib import Path
from datetime import datetime
import yaml

REPO_ROOT = Path(__file__).parent.parent.resolve()
CANONICAL_DIR = REPO_ROOT / "skills" / "canonical"
DOMAIN_DIR = REPO_ROOT / "skills" / "domain"

# Domain mapping rules
DOMAIN_MAP = {
    # Science domains
    "science": "science",
    "scientific": "science",
    "biology": "science",
    "chemistry": "science",
    "physics": "science",
    "medical": "science",
    "clinical": "science",
    "bioinformatics": "science",
    "genomics": "science",
    "proteomics": "science",
    "metabolomics": "science",
    "drug": "science",
    "pharma": "science",
    # Development domains
    "development": "development",
    "programming": "development",
    "coding": "development",
    "software": "development",
    "typescript": "development/languages",
    "python": "development/languages",
    "javascript": "development/languages",
    "react": "development/frameworks",
    "vue": "development/frameworks",
    "angular": "development/frameworks",
    "node": "development/frameworks",
    "testing": "development/testing",
    "architecture": "development/architecture",
    "infrastructure": "development/infrastructure",
    "devops": "development/infrastructure",
    "docker": "development/infrastructure",
    "kubernetes": "development/infrastructure",
    # Security domains
    "security": "security",
    "appsec": "security/appsec",
    "pentesting": "security/pentesting",
    "vulnerability": "security/appsec",
    "scan": "security/appsec",
    # Data domains
    "data": "data",
    "ml": "data/ml",
    "machine learning": "data/ml",
    "ai": "data/ml",
    "analytics": "data/analysis",
    "visualization": "data/visualization",
    # Documents
    "documents": "documents",
    "pdf": "documents",
    "docx": "documents",
    "pptx": "documents",
    "xlsx": "documents",
    # Research
    "research": "research",
    "literature": "research",
    "citation": "research",
    "grant": "research",
    "peer review": "research",
}

SUBDOMAIN_DEFAULTS = {
    "science": "analysis",
    "development": "languages",
    "security": "appsec",
    "data": "analysis",
    "documents": "conversion",
    "research": "writing",
}


def infer_domain(skill_name, tags, description):
    """Infer domain from skill metadata."""
    search_text = (
        f"{skill_name} {' '.join(tags) if isinstance(tags, list) else tags} {description}".lower()
    )

    for keyword, domain in DOMAIN_MAP.items():
        if keyword in search_text:
            return domain

    return "general"


def parse_frontmatter(skill_md_path):
    """Parse YAML frontmatter from SKILL.md."""
    try:
        content = skill_md_path.read_text()
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                return yaml.safe_load(parts[1]) or {}
    except Exception:
        pass
    return {}


def create_pointer(skill_name, skill_data, domain_path):
    """Create pointer file for a skill."""
    pointer_dir = DOMAIN_DIR / domain_path
    pointer_dir.mkdir(parents=True, exist_ok=True)

    pointer_file = pointer_dir / f"{skill_name}.pointer.md"

    # Calculate relative path to canonical
    depth = len(domain_path.split("/"))
    canonical_rel = "../" * (depth + 1) + f"canonical/{skill_name}/SKILL.md"

    # Build pointer content
    tags = skill_data.get("tags", [])
    if isinstance(tags, str):
        tags = [tags]

    tags_yaml = "\n".join(f"  - {tag}" for tag in tags[:10])  # Limit to 10 tags

    content = f"""---
skill: {skill_name}
canonical: {canonical_rel}
description: >
  {skill_data.get("description", "")[:200]}
tags:
{tags_yaml or "  - skill"}
domain: [{domain_path}]
upstream: {skill_data.get("upstream", "") or skill_data.get("metadata", {}).get("imported-from", "")}
license: {skill_data.get("license", "MIT")}
load_frequency: {skill_data.get("load_frequency", "medium")}
---
"""

    pointer_file.write_text(content)
    return pointer_file


def update_domain_readme(domain_path, skill_count):
    """Update domain README with skill count."""
    readme_file = DOMAIN_DIR / domain_path / "README.md"

    if not readme_file.exists():
        # Create basic README
        domain_name = domain_path.split("/")[-1].replace("-", " ").title()
        readme_content = f"""# {domain_name}

> Skills for {domain_name.lower()}

## Skills

| Skill | Description | Pointer |
|-------|-------------|---------|

_Auto-generated. {skill_count} skills in this domain._
"""
        readme_file.write_text(readme_content)
    else:
        # Update existing README
        content = readme_file.read_text()
        # Update count in footer
        import re

        content = re.sub(
            r"_Auto-generated\. \d+ skills in this domain\._",
            f"_Auto-generated. {skill_count} skills in this domain._",
            content,
        )
        readme_file.write_text(content)


def populate_pointers():
    """Populate domain tree with pointers."""
    print("Populating domain pointers...")
    print(f"Source: {CANONICAL_DIR}")
    print(f"Target: {DOMAIN_DIR}")
    print()

    created = 0
    skipped = 0
    domain_counts = {}

    for skill_dir in CANONICAL_DIR.iterdir():
        if not skill_dir.is_dir():
            continue

        skill_name = skill_dir.name
        skill_md = skill_dir / "SKILL.md"

        if not skill_md.exists():
            print(f"Skip: {skill_name} (no SKILL.md)")
            continue

        # Parse frontmatter
        fm = parse_frontmatter(skill_md)
        if not fm:
            fm = {}

        # Get domain
        domain = fm.get("domain", "")
        if isinstance(domain, list) and domain:
            domain = domain[0]
        elif not domain:
            # Infer from tags/description/name
            tags = fm.get("tags", [])
            description = fm.get("description", "")
            domain = infer_domain(skill_name, tags, description)

        # Clean domain path
        domain = domain.strip("/")
        if not domain:
            domain = "general"

        # Create pointer
        try:
            pointer_file = create_pointer(skill_name, fm, domain)
            created += 1

            # Track domain counts
            domain_counts[domain] = domain_counts.get(domain, 0) + 1

            if created % 100 == 0:
                print(f"  Created {created} pointers...")

        except Exception as e:
            print(f"  Error: {skill_name} - {e}")
            skipped += 1

    print(f"\nPointer creation complete:")
    print(f"  Created: {created}")
    print(f"  Skipped: {skipped}")
    print(f"\nDomain distribution:")
    for domain, count in sorted(domain_counts.items(), key=lambda x: -x[1])[:20]:
        print(f"  {domain}: {count}")

    # Update READMEs
    print("\nUpdating domain READMEs...")
    for domain, count in domain_counts.items():
        update_domain_readme(domain, count)

    print("Done!")


if __name__ == "__main__":
    populate_pointers()
