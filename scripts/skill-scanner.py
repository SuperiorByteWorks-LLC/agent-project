#!/usr/bin/env python3
"""
Skill Scanner - Detects policy violations in skills using blocklist patterns.

This script scans skills for violations defined in blocklist.yaml and generates
quarantine recommendations. It can also auto-clean skills using blocklist rules.

Usage:
    python skill-scanner.py --skill skills/canonical/example/
    python skill-scanner.py --scan-all
    python skill-scanner.py --skill skills/canonical/example/ --auto-clean
    python skill-scanner.py --scan-all --output report.json
"""

import argparse
import json
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

# Configuration
DEFAULT_BLOCKLIST_PATH = Path(__file__).parent / "blocklist.yaml"
SKILL_JAIL_PATH = Path(__file__).parent.parent / "skills" / "skill-jail"
CANONICAL_PATH = Path(__file__).parent.parent / "skills" / "canonical"


def load_blocklist(blocklist_path: Path) -> dict:
    """Load the blocklist configuration from YAML file."""
    try:
        with open(blocklist_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Blocklist file not found: {blocklist_path}", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML in blocklist: {e}", file=sys.stderr)
        sys.exit(1)


def compile_patterns(blocklist: dict) -> dict:
    """Compile regex patterns from blocklist configuration."""
    compiled = {}

    for category, config in blocklist.items():
        if not isinstance(config, dict):
            continue

        if "patterns" in config:
            compiled[category] = {
                "severity": config.get("severity", "medium"),
                "action": config.get("action", "quarantine"),
                "description": config.get("description", ""),
                "patterns": [],
            }

            for pattern in config["patterns"]:
                if isinstance(pattern, str):
                    if pattern.startswith("regex: "):
                        # Extract regex pattern
                        regex_str = pattern[7:]
                        try:
                            compiled[category]["patterns"].append(
                                re.compile(regex_str, re.IGNORECASE)
                            )
                        except re.error as e:
                            print(
                                f"Warning: Invalid regex in {category}: {e}",
                                file=sys.stderr,
                            )
                    else:
                        # Simple string match (case-insensitive)
                        compiled[category]["patterns"].append(
                            re.compile(re.escape(pattern), re.IGNORECASE)
                        )

    return compiled


def scan_file(file_path: Path, compiled_patterns: dict) -> list[dict]:
    """Scan a single file for violations."""
    violations = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            lines = content.split("\n")
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}", file=sys.stderr)
        return violations

    for category, config in compiled_patterns.items():
        for pattern in config["patterns"]:
            for match in pattern.finditer(content):
                # Find line number
                line_num = content[: match.start()].count("\n") + 1
                line_content = lines[line_num - 1] if line_num <= len(lines) else ""

                violation = {
                    "category": category,
                    "severity": config["severity"],
                    "action": config["action"],
                    "description": config["description"],
                    "file": str(file_path),
                    "line": line_num,
                    "column": match.start() - content.rfind("\n", 0, match.start()),
                    "matched_text": match.group(),
                    "line_content": line_content.strip(),
                    "pattern": pattern.pattern,
                }
                violations.append(violation)

    return violations


def scan_skill(skill_path: Path, compiled_patterns: dict) -> dict:
    """Scan an entire skill directory for violations."""
    skill_violations = {
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

    # Find all markdown files in the skill directory
    for md_file in skill_path.rglob("*.md"):
        violations = scan_file(md_file, compiled_patterns)
        for v in violations:
            v["relative_path"] = str(md_file.relative_to(skill_path))
        skill_violations["violations"].extend(violations)

    # Update summary
    skill_violations["summary"]["total_violations"] = len(skill_violations["violations"])
    for v in skill_violations["violations"]:
        severity = v["severity"]
        if severity in skill_violations["summary"]:
            skill_violations["summary"][severity] += 1

    return skill_violations


def scan_all_skills(canonical_path: Path, compiled_patterns: dict) -> list[dict]:
    """Scan all skills in the canonical directory."""
    results = []

    if not canonical_path.exists():
        print(f"Warning: Canonical path does not exist: {canonical_path}", file=sys.stderr)
        return results

    for skill_dir in canonical_path.iterdir():
        if skill_dir.is_dir():
            result = scan_skill(skill_dir, compiled_patterns)
            results.append(result)

    return results


def auto_clean_skill(skill_path: Path, violations: list[dict], blocklist: dict) -> dict:
    """Auto-clean a skill by removing violations that can be auto-cleaned."""
    cleanup_results = {
        "skill_name": skill_path.name,
        "cleaned": False,
        "modifications": [],
        "remaining_violations": [],
    }

    # Get auto-cleanup rules
    auto_cleanup_categories = set()
    if "auto_cleanup_rules" in blocklist:
        auto_cleanup_categories = set(blocklist["auto_cleanup_rules"].get("can_auto_clean", []))

    # Separate auto-cleanable from manual review violations
    auto_cleanable = [v for v in violations if v["category"] in auto_cleanup_categories]
    manual_review = [v for v in violations if v["category"] not in auto_cleanup_categories]

    cleanup_results["remaining_violations"] = manual_review

    if not auto_cleanable:
        return cleanup_results

    # Read skill files and apply cleanup
    for md_file in skill_path.rglob("*.md"):
        try:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()

            original_content = content
            modifications = []

            for violation in auto_cleanable:
                if violation["relative_path"] != str(md_file.relative_to(skill_path)):
                    continue

                # Apply cleanup based on category
                if violation["category"] == "author_replacements":
                    replacements = blocklist.get("author_replacements", {}).get("replacements", {})
                    for old, new in replacements.items():
                        if old in content:
                            content = content.replace(old, new)
                            modifications.append(f"Replaced '{old}' with '{new}'")

                elif violation["category"] == "watermark_patterns":
                    # Remove watermarks
                    matched = violation["matched_text"]
                    if matched in content:
                        content = content.replace(matched, "")
                        modifications.append(f"Removed watermark: '{matched}'")

                elif violation["category"] == "blocked_emails":
                    # Remove email addresses
                    matched = violation["matched_text"]
                    if matched in content:
                        content = content.replace(matched, "")
                        modifications.append(f"Removed email: '{matched}'")

                elif violation["category"] == "blocked_phones":
                    # Remove phone numbers
                    matched = violation["matched_text"]
                    if matched in content:
                        content = content.replace(matched, "")
                        modifications.append(f"Removed phone: '{matched}'")

                elif violation["category"] == "metadata_injection":
                    # Remove metadata injection patterns
                    matched = violation["matched_text"]
                    if matched in content:
                        content = content.replace(matched, "")
                        modifications.append(f"Removed metadata: '{matched}'")

            if content != original_content:
                with open(md_file, "w", encoding="utf-8") as f:
                    f.write(content)
                cleanup_results["modifications"].extend(modifications)

        except Exception as e:
            print(f"Warning: Could not clean {md_file}: {e}", file=sys.stderr)

    cleanup_results["cleaned"] = len(cleanup_results["modifications"]) > 0
    return cleanup_results


def generate_quarantine_report(skill_violations: dict, output_path: Path) -> None:
    """Generate a quarantine report for a skill."""
    skill_name = skill_violations["skill_name"]
    report_path = output_path / skill_name / "QUARANTINE-REPORT.md"

    # Ensure directory exists
    report_path.parent.mkdir(parents=True, exist_ok=True)

    report_content = f"""# Skill Quarantine Report

## Skill Information

| Field | Value |
|-------|-------|
| **Skill Name** | `{skill_name}` |
| **Detection Date** | `{skill_violations["scan_date"]}` |
| **Status** | `quarantined` |

## Violation Summary

| Severity | Count |
|----------|-------|
| **Critical** | {skill_violations["summary"]["critical"]} |
| **High** | {skill_violations["summary"]["high"]} |
| **Medium** | {skill_violations["summary"]["medium"]} |
| **Low** | {skill_violations["summary"]["low"]} |
| **Total** | {skill_violations["summary"]["total_violations"]} |

## Violation Details

"""

    for i, v in enumerate(skill_violations["violations"], 1):
        report_content += f"""### Violation {i}

| Field | Value |
|-------|-------|
| **Type** | `{v["category"]}` |
| **Severity** | `{v["severity"]}` |
| **Action** | `{v["action"]}` |
| **File** | `{v["relative_path"]}` |
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

- [ ] `pending_review`
- [x] `quarantined`
- [ ] `approved_cleaned`
- [ ] `rejected`

### Reviewer Notes

<!-- Add reviewer notes here -->

### Cleanup Instructions

<!-- Add cleanup instructions here -->

---

*Generated by skill-scanner.py on {datetime.now().isoformat()}*
"""

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)


def move_to_quarantine(
    skill_path: Path, violations: dict, quarantine_type: str = "quarantined"
) -> Path:
    """Move a skill to the skill jail."""
    skill_name = skill_path.name
    dest_path = SKILL_JAIL_PATH / quarantine_type / skill_name

    # Ensure destination exists
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    # Copy skill to quarantine (don't move, keep original for reference)
    if dest_path.exists():
        shutil.rmtree(dest_path)
    shutil.copytree(skill_path, dest_path)

    # Generate quarantine report
    generate_quarantine_report(violations, SKILL_JAIL_PATH / quarantine_type)

    return dest_path


def print_report(results: list[dict], output_format: str = "text") -> None:
    """Print scan results in the specified format."""
    if output_format == "json":
        print(json.dumps(results, indent=2))
    else:
        # Text format
        total_violations = sum(r["summary"]["total_violations"] for r in results)
        skills_with_violations = sum(1 for r in results if r["summary"]["total_violations"] > 0)

        print("\n" + "=" * 80)
        print("SKILL SCANNER REPORT")
        print("=" * 80)
        print(f"\nTotal skills scanned: {len(results)}")
        print(f"Skills with violations: {skills_with_violations}")
        print(f"Total violations found: {total_violations}")
        print()

        for result in results:
            if result["summary"]["total_violations"] == 0:
                continue

            print(f"\n{'─' * 80}")
            print(f"Skill: {result['skill_name']}")
            print(f"Path: {result['skill_path']}")
            print(
                f"Violations: {result['summary']['total_violations']} "
                f"(Critical: {result['summary']['critical']}, "
                f"High: {result['summary']['high']}, "
                f"Medium: {result['summary']['medium']}, "
                f"Low: {result['summary']['low']})"
            )
            print()

            for v in result["violations"]:
                severity_emoji = {
                    "critical": "🔴",
                    "high": "🟠",
                    "medium": "🟡",
                    "low": "🔵",
                }.get(v["severity"], "⚪")

                print(f"  {severity_emoji} [{v['severity'].upper()}] {v['category']}")
                print(f"     File: {v['relative_path']}:{v['line']}:{v['column']}")
                print(f'     Match: "{v["matched_text"]}"')
                print(f"     Action: {v['action']}")
                print()

        print("=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description="Scan skills for policy violations using blocklist patterns.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --skill skills/canonical/example/
  %(prog)s --scan-all
  %(prog)s --skill skills/canonical/example/ --auto-clean
  %(prog)s --scan-all --output report.json
        """,
    )

    parser.add_argument(
        "--skill",
        type=Path,
        help="Path to a specific skill to scan",
    )

    parser.add_argument(
        "--scan-all",
        action="store_true",
        help="Scan all skills in the canonical directory",
    )

    parser.add_argument(
        "--auto-clean",
        action="store_true",
        help="Automatically clean violations that can be auto-fixed",
    )

    parser.add_argument(
        "--quarantine",
        action="store_true",
        help="Move skills with violations to quarantine",
    )

    parser.add_argument(
        "--blocklist",
        type=Path,
        default=DEFAULT_BLOCKLIST_PATH,
        help=f"Path to blocklist YAML file (default: {DEFAULT_BLOCKLIST_PATH})",
    )

    parser.add_argument(
        "--output",
        type=Path,
        help="Output file for JSON report",
    )

    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.skill and not args.scan_all:
        parser.error("Must specify either --skill or --scan-all")

    # Load blocklist
    blocklist = load_blocklist(args.blocklist)
    compiled_patterns = compile_patterns(blocklist)

    # Scan skills
    if args.skill:
        if not args.skill.exists():
            print(f"Error: Skill path does not exist: {args.skill}", file=sys.stderr)
            sys.exit(1)

        results = [scan_skill(args.skill, compiled_patterns)]

        # Auto-clean if requested
        if args.auto_clean:
            cleanup_result = auto_clean_skill(args.skill, results[0]["violations"], blocklist)
            print(f"\nAuto-cleanup results for {args.skill.name}:")
            print(f"  Cleaned: {cleanup_result['cleaned']}")
            print(f"  Modifications: {len(cleanup_result['modifications'])}")
            if cleanup_result["modifications"]:
                for mod in cleanup_result["modifications"]:
                    print(f"    - {mod}")

            # Re-scan after cleanup
            results = [scan_skill(args.skill, compiled_patterns)]

        # Quarantine if requested and violations remain
        if args.quarantine and results[0]["summary"]["total_violations"] > 0:
            dest = move_to_quarantine(args.skill, results[0])
            print(f"\nSkill moved to quarantine: {dest}")

    else:
        results = scan_all_skills(CANONICAL_PATH, compiled_patterns)

        # Quarantine skills with violations if requested
        if args.quarantine:
            for result in results:
                if result["summary"]["total_violations"] > 0:
                    skill_path = Path(result["skill_path"])
                    dest = move_to_quarantine(skill_path, result)
                    print(f"Quarantined: {result['skill_name']} -> {dest}")

    # Print report
    print_report(results, args.format)

    # Save JSON output if requested
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"\nReport saved to: {args.output}")

    # Exit with error code if violations found
    total_violations = sum(r["summary"]["total_violations"] for r in results)
    if total_violations > 0:
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
