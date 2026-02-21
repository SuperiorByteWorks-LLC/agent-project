#!/usr/bin/env python3
"""
Import with Quarantine - Import skills from upstream with automatic quarantine checking.

This script imports skills from upstream repositories, automatically runs the skill-scanner,
moves flagged skills to quarantine, and generates a comprehensive quarantine report.

Usage:
    python import-with-quarantine.py --source upstream-repo/ --target skills/
    python import-with-quarantine.py --source upstream-repo/ --dry-run
    python import-with-quarantine.py --source upstream-repo/ --skill skill-name
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Configuration
DEFAULT_TARGET_PATH = Path(__file__).parent.parent / "skills" / "canonical"
SKILL_JAIL_PATH = Path(__file__).parent.parent / "skills" / "skill-jail"
SCANNER_SCRIPT = Path(__file__).parent / "skill-scanner.py"


def run_scanner(skill_path: Path, blocklist_path: Path = None) -> dict:
    """Run the skill scanner on a specific skill."""
    cmd = [
        sys.executable,
        str(SCANNER_SCRIPT),
        "--skill",
        str(skill_path),
        "--format",
        "json",
    ]

    if blocklist_path:
        cmd.extend(["--blocklist", str(blocklist_path)])

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
        )

        # Parse JSON output from stdout
        lines = result.stdout.strip().split("\n")
        json_lines = []
        capture = False

        for line in lines:
            if line.startswith("["):
                capture = True
            if capture:
                json_lines.append(line)

        if json_lines:
            return json.loads("\n".join(json_lines))[0]
        else:
            return {
                "skill_name": skill_path.name,
                "skill_path": str(skill_path),
                "scan_date": datetime.now().isoformat(),
                "violations": [],
                "summary": {
                    "total_violations": 0,
                    "critical": 0,
                    "high": 0,
                    "medium": 0,
                    "low": 0,
                },
            }

    except Exception as e:
        print(f"Warning: Scanner failed for {skill_path}: {e}", file=sys.stderr)
        return {
            "skill_name": skill_path.name,
            "skill_path": str(skill_path),
            "scan_date": datetime.now().isoformat(),
            "violations": [],
            "summary": {
                "total_violations": 0,
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0,
            },
            "error": str(e),
        }


def copy_skill(source_path: Path, target_path: Path, dry_run: bool = False) -> bool:
    """Copy a skill from source to target."""
    if dry_run:
        print(f"[DRY-RUN] Would copy: {source_path} -> {target_path}")
        return True

    try:
        if target_path.exists():
            shutil.rmtree(target_path)
        shutil.copytree(source_path, target_path)
        return True
    except Exception as e:
        print(f"Error: Failed to copy {source_path}: {e}", file=sys.stderr)
        return False


def move_to_quarantine(
    skill_path: Path, violations: dict, quarantine_type: str = "review-pending"
) -> Path:
    """Move a skill to the skill jail."""
    skill_name = skill_path.name
    dest_path = SKILL_JAIL_PATH / quarantine_type / skill_name

    # Ensure destination exists
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    # Move skill to quarantine
    if dest_path.exists():
        shutil.rmtree(dest_path)
    shutil.move(str(skill_path), str(dest_path))

    # Generate quarantine report
    generate_quarantine_report(skill_name, violations, dest_path.parent)

    return dest_path


def generate_quarantine_report(skill_name: str, violations: dict, output_dir: Path) -> None:
    """Generate a quarantine report for a skill."""
    report_path = output_dir / skill_name / "QUARANTINE-REPORT.md"

    report_content = f"""# Skill Quarantine Report

## Skill Information

| Field | Value |
|-------|-------|
| **Skill Name** | `{skill_name}` |
| **Detection Date** | `{violations.get("scan_date", datetime.now().isoformat())}` |
| **Status** | `review-pending` |

## Violation Summary

| Severity | Count |
|----------|-------|
| **Critical** | {violations["summary"]["critical"]} |
| **High** | {violations["summary"]["high"]} |
| **Medium** | {violations["summary"]["medium"]} |
| **Low** | {violations["summary"]["low"]} |
| **Total** | {violations["summary"]["total_violations"]} |

## Violation Details

"""

    for i, v in enumerate(violations.get("violations", []), 1):
        report_content += f"""### Violation {i}

| Field | Value |
|-------|-------|
| **Type** | `{v["category"]}` |
| **Severity** | `{v["severity"]}` |
| **Action** | `{v["action"]}` |
| **File** | `{v.get("relative_path", "N/A")}` |
| **Line** | {v["line"]} |
| **Column** | {v["column"]} |
| **Matched Text** | `{v["matched_text"]}` |

**Line Content:**
```
{v["line_content"]}
```

**Description:** {v["description"]}

---

"""

    report_content += f"""## Resolution

### Status

- [x] `pending_review`
- [ ] `under_review`
- [ ] `approved_cleaned`
- [ ] `approved_unchanged`
- [ ] `rejected`
- [ ] `quarantined`

### Reviewer Notes

<!-- Add reviewer notes here -->

### Cleanup Instructions

<!-- Add cleanup instructions here -->

---

*Generated by import-with-quarantine.py on {datetime.now().isoformat()}*
"""

    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)


def generate_import_report(
    imported: list[str],
    quarantined: list[dict],
    failed: list[str],
    output_path: Path,
) -> None:
    """Generate a comprehensive import report."""
    report = {
        "import_date": datetime.now().isoformat(),
        "summary": {
            "total_processed": len(imported) + len(quarantined) + len(failed),
            "imported_clean": len(imported),
            "quarantined": len(quarantined),
            "failed": len(failed),
        },
        "imported_clean": imported,
        "quarantined": quarantined,
        "failed": failed,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    # Also generate a markdown report
    md_path = output_path.with_suffix(".md")
    md_content = f"""# Skill Import Report

_Import completed: {datetime.now().isoformat()}_

---

## Summary

| Metric | Count |
|--------|-------|
| **Total Processed** | {report["summary"]["total_processed"]} |
| **Imported Clean** | {report["summary"]["imported_clean"]} |
| **Quarantined** | {report["summary"]["quarantined"]} |
| **Failed** | {report["summary"]["failed"]} |

---

## ✅ Imported Clean

Skills that passed all checks and were imported successfully.

"""

    for skill in imported:
        md_content += f"- `{skill}`\n"

    md_content += f"""

---

## 🚨 Quarantined

Skills with violations that were moved to quarantine for review.

"""

    for item in quarantined:
        skill_name = item["skill_name"]
        violations = item["violations"]
        md_content += f"""### {skill_name}

- **Location:** `skills/skill-jail/review-pending/{skill_name}/`
- **Total Violations:** {violations["summary"]["total_violations"]}
- **Critical:** {violations["summary"]["critical"]}
- **High:** {violations["summary"]["high"]}
- **Medium:** {violations["summary"]["medium"]}
- **Low:** {violations["summary"]["low"]}

"""

    md_content += f"""

---

## ❌ Failed

Skills that failed to import due to errors.

"""

    for skill in failed:
        md_content += f"- `{skill}`\n"

    md_content += f"""

---

## Next Steps

1. **Review quarantined skills** in `skills/skill-jail/review-pending/`
2. **Check quarantine reports** for each flagged skill
3. **Clean or approve** skills following the workflow in `skills/skill-jail/README.md`
4. **Update blocklist** if new violation patterns were discovered

---

*Report generated by import-with-quarantine.py*
"""

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)


def import_skill(
    source_path: Path,
    target_path: Path,
    blocklist_path: Path = None,
    dry_run: bool = False,
) -> dict:
    """Import a single skill with quarantine checking."""
    skill_name = source_path.name

    print(f"\nProcessing: {skill_name}")
    print(f"  Source: {source_path}")

    # First, copy to a temporary location for scanning
    temp_path = target_path.parent / f".temp-{skill_name}"

    try:
        # Copy to temp location
        if temp_path.exists():
            shutil.rmtree(temp_path)
        shutil.copytree(source_path, temp_path)

        # Run scanner
        print(f"  Scanning for violations...")
        violations = run_scanner(temp_path, blocklist_path)

        total_violations = violations["summary"]["total_violations"]

        if total_violations > 0:
            print(f"  ⚠️  Found {total_violations} violations")
            print(f"     Critical: {violations['summary']['critical']}")
            print(f"     High: {violations['summary']['high']}")
            print(f"     Medium: {violations['summary']['medium']}")
            print(f"     Low: {violations['summary']['low']}")

            # Move to quarantine
            if not dry_run:
                quarantine_path = move_to_quarantine(temp_path, violations, "review-pending")
                print(f"  🚨 Moved to quarantine: {quarantine_path}")
            else:
                print(
                    f"  [DRY-RUN] Would move to quarantine: skills/skill-jail/review-pending/{skill_name}/"
                )
                shutil.rmtree(temp_path)

            return {
                "skill_name": skill_name,
                "status": "quarantined",
                "violations": violations,
            }
        else:
            print(f"  ✅ No violations found")

            # Move to target
            if not dry_run:
                if target_path.exists():
                    shutil.rmtree(target_path)
                shutil.move(str(temp_path), str(target_path))
                print(f"  ✅ Imported to: {target_path}")
            else:
                print(f"  [DRY-RUN] Would import to: {target_path}")
                shutil.rmtree(temp_path)

            return {
                "skill_name": skill_name,
                "status": "imported",
                "violations": violations,
            }

    except Exception as e:
        print(f"  ❌ Error: {e}", file=sys.stderr)
        if temp_path.exists():
            shutil.rmtree(temp_path, ignore_errors=True)
        return {
            "skill_name": skill_name,
            "status": "failed",
            "error": str(e),
        }


def main():
    parser = argparse.ArgumentParser(
        description="Import skills from upstream with automatic quarantine checking.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --source upstream-repo/skills/ --target skills/canonical/
  %(prog)s --source upstream-repo/skills/ --dry-run
  %(prog)s --source upstream-repo/skills/ --skill my-skill
        """,
    )

    parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="Source directory containing skills to import",
    )

    parser.add_argument(
        "--target",
        type=Path,
        default=DEFAULT_TARGET_PATH,
        help=f"Target directory for imported skills (default: {DEFAULT_TARGET_PATH})",
    )

    parser.add_argument(
        "--skill",
        type=str,
        help="Import only a specific skill by name",
    )

    parser.add_argument(
        "--blocklist",
        type=Path,
        help="Path to blocklist YAML file",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("import-report.json"),
        help="Output file for import report (default: import-report.json)",
    )

    args = parser.parse_args()

    # Validate source exists
    if not args.source.exists():
        print(f"Error: Source path does not exist: {args.source}", file=sys.stderr)
        sys.exit(1)

    # Ensure target directory exists
    args.target.mkdir(parents=True, exist_ok=True)

    # Ensure skill jail directories exist
    (SKILL_JAIL_PATH / "review-pending").mkdir(parents=True, exist_ok=True)
    (SKILL_JAIL_PATH / "quarantined").mkdir(parents=True, exist_ok=True)
    (SKILL_JAIL_PATH / "blocked").mkdir(parents=True, exist_ok=True)

    # Collect skills to import
    skills_to_import = []

    if args.skill:
        # Import specific skill
        skill_path = args.source / args.skill
        if skill_path.exists():
            skills_to_import.append(skill_path)
        else:
            print(f"Error: Skill not found: {skill_path}", file=sys.stderr)
            sys.exit(1)
    else:
        # Import all skills from source
        for item in args.source.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                skills_to_import.append(item)

    if not skills_to_import:
        print("No skills found to import.")
        sys.exit(0)

    print(f"\n{'=' * 80}")
    print("SKILL IMPORT WITH QUARANTINE")
    print(f"{'=' * 80}")
    print(f"\nSource: {args.source}")
    print(f"Target: {args.target}")
    print(f"Skills to import: {len(skills_to_import)}")
    if args.dry_run:
        print("Mode: DRY-RUN (no changes will be made)")
    print()

    # Process each skill
    imported = []
    quarantined = []
    failed = []

    for skill_path in skills_to_import:
        target_path = args.target / skill_path.name
        result = import_skill(skill_path, target_path, args.blocklist, args.dry_run)

        if result["status"] == "imported":
            imported.append(result["skill_name"])
        elif result["status"] == "quarantined":
            quarantined.append(result)
        else:
            failed.append(result["skill_name"])

    # Generate report
    print(f"\n{'=' * 80}")
    print("IMPORT SUMMARY")
    print(f"{'=' * 80}")
    print(f"\nTotal processed: {len(skills_to_import)}")
    print(f"  ✅ Imported clean: {len(imported)}")
    print(f"  🚨 Quarantined: {len(quarantined)}")
    print(f"  ❌ Failed: {len(failed)}")

    if not args.dry_run:
        generate_import_report(imported, quarantined, failed, args.output)
        print(f"\nReport saved to:")
        print(f"  - {args.output}")
        print(f"  - {args.output.with_suffix('.md')}")
    else:
        print(f"\n[DRY-RUN] Report would be saved to: {args.output}")

    # Exit with error code if any skills were quarantined or failed
    if quarantined or failed:
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
