#!/usr/bin/env python3
"""
Prompt Scanner - Detects policy violations in prompts using blocklist patterns.

Usage:
    python prompt-scanner.py --prompt prompts/canonical/example/
    python prompt-scanner.py --scan-all
    python prompt-scanner.py --prompt prompts/canonical/example/ --auto-clean
    python prompt-scanner.py --scan-all --output report.json
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
DEFAULT_BLOCKLIST_PATH = Path(__file__).parent / "prompt-blocklist.yaml"
PROMPT_JAIL_PATH = Path(__file__).parent.parent / "prompts" / "prompt-jail"
CANONICAL_PATH = Path(__file__).parent.parent / "prompts" / "canonical"


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
        if isinstance(config, dict) and "patterns" in config:
            compiled[category] = {
                "severity": config.get("severity", "medium"),
                "action": config.get("action", "quarantine"),
                "patterns": [],
            }

            for pattern in config["patterns"]:
                if pattern.startswith("regex:"):
                    regex = pattern[6:]
                    compiled[category]["patterns"].append(re.compile(regex, re.IGNORECASE))
                else:
                    compiled[category]["patterns"].append(
                        re.compile(re.escape(pattern), re.IGNORECASE)
                    )

    return compiled


def scan_prompt(prompt_path: Path, compiled_patterns: dict) -> list:
    """Scan a single prompt file for violations."""
    violations = []

    prompt_file = prompt_path / "PROMPT.md"
    if not prompt_file.exists():
        return violations

    try:
        with open(prompt_file, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Warning: Could not read {prompt_file}: {e}", file=sys.stderr)
        return violations

    lines = content.split("\n")

    for category, config in compiled_patterns.items():
        for pattern in config["patterns"]:
            for i, line in enumerate(lines, 1):
                if pattern.search(line):
                    violations.append(
                        {
                            "category": category,
                            "severity": config["severity"],
                            "action": config["action"],
                            "line": i,
                            "content": line.strip()[:100],
                            "pattern": pattern.pattern,
                        }
                    )

    return violations


def scan_all(compiled_patterns: dict) -> dict:
    """Scan all prompts in the canonical directory."""
    results = {}

    if not CANONICAL_PATH.exists():
        print(f"Error: Canonical path not found: {CANONICAL_PATH}", file=sys.stderr)
        return results

    for source_dir in CANONICAL_PATH.iterdir():
        if source_dir.is_dir():
            for prompt_dir in source_dir.iterdir():
                if prompt_dir.is_dir():
                    prompt_name = f"{source_dir.name}/{prompt_dir.name}"
                    violations = scan_prompt(prompt_dir, compiled_patterns)
                    if violations:
                        results[prompt_name] = violations

    return results


def generate_report(results: dict) -> str:
    """Generate a summary report of all violations."""
    report = f"""# Prompt Scan Report

**Generated:** {datetime.now().isoformat()}
**Total Prompts with Violations:** {len(results)}

## Summary by Severity

"""

    severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for prompt, violations in results.items():
        for v in violations:
            severity_counts[v["severity"]] = severity_counts.get(v["severity"], 0) + 1

    for sev, count in severity_counts.items():
        if count > 0:
            report += f"- **{sev.upper()}:** {count} violations\n"

    report += "\n## Detailed List\n\n"
    report += "| Prompt | Violations | Categories |\n"
    report += "|--------|-----------|------------|\n"

    for prompt, violations in sorted(results.items()):
        categories = ", ".join(set(v["category"] for v in violations))
        report += f"| {prompt} | {len(violations)} | {categories} |\n"

    return report


def move_to_jail(prompt_path: Path, reason: str, violations: list, dry_run: bool = True) -> bool:
    """Move a prompt to the quarantine directory."""
    prompt_name = prompt_path.name
    source = prompt_path.parent.name

    target = PROMPT_JAIL_PATH / "quarantined" / "imported" / source / prompt_name

    if dry_run:
        print(f"[DRY-RUN] Would move {prompt_path} -> {target}")
        return True

    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(prompt_path), str(target))

        # Create quarantine report
        report_file = target / "QUARANTINE-REPORT.md"
        report_content = f"""# Quarantine Report: {prompt_name}

**Quarantined:** {datetime.now().isoformat()}
**Reason:** {reason}
**Status:** quarantined

## Violations Found

"""
        for v in violations:
            report_content += f"- [{v['severity'].upper()}] {v['category']}: Line {v['line']}\n"

        report_content += f"""
## Cleanup Instructions

Review and remove violations before promoting to canonical.

## Original Location

- Source: {prompt_path}
- Quarantine: {target}
"""

        report_file.write_text(report_content)
        print(f"Moved {prompt_name} to quarantine")
        return True
    except Exception as e:
        print(f"Error moving {prompt_name}: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Scan prompts for policy violations")

    parser.add_argument("--prompt", type=Path, help="Scan a specific prompt directory")
    parser.add_argument("--scan-all", action="store_true", help="Scan all prompts")
    parser.add_argument(
        "--blocklist", type=Path, default=DEFAULT_BLOCKLIST_PATH, help="Path to blocklist YAML"
    )
    parser.add_argument("--output", type=Path, help="Output report to file")
    parser.add_argument(
        "--auto-quarantine", action="store_true", help="Auto-quarantine prompts with violations"
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without applying")

    args = parser.parse_args()

    # Load and compile blocklist
    blocklist = load_blocklist(args.blocklist)
    compiled_patterns = compile_patterns(blocklist)

    if args.prompt:
        # Scan single prompt
        violations = scan_prompt(args.prompt, compiled_patterns)

        print(f"\nScanning: {args.prompt}")
        print("=" * 60)

        if violations:
            print(f"\n⚠️  Found {len(violations)} violation(s):\n")
            for v in violations:
                print(f"  [{v['severity'].upper()}] {v['category']}")
                print(f"    Line {v['line']}: {v['content'][:60]}...")
                print(f"    Action: {v['action']}")
                print()
        else:
            print("✓ No violations found")

    elif args.scan_all:
        # Scan all prompts
        print("Scanning all prompts...")
        results = scan_all(compiled_patterns)

        print(f"\n{'=' * 60}")
        print(f"Scan complete. Found {len(results)} prompts with violations.")
        print(f"{'=' * 60}\n")

        if results:
            report = generate_report(results)
            print(report)

            if args.output:
                args.output.write_text(report)
                print(f"\nReport saved to: {args.output}")

            # Auto-quarantine if requested
            if args.auto_quarantine:
                print(f"\n{'=' * 60}")
                print("Auto-quarantining prompts with violations...")
                print(f"{'=' * 60}\n")

                for prompt_name, violations in results.items():
                    source, name = prompt_name.split("/", 1)
                    prompt_path = CANONICAL_PATH / source / name
                    move_to_jail(
                        prompt_path, "Violations detected", violations, dry_run=args.dry_run
                    )
        else:
            print("✓ No violations found across all prompts")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
