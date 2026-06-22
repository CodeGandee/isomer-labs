#!/usr/bin/env python3
"""Repository-local documentation validation for Isomer Labs."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


REQUIRED_PAGES = [
    "docs/index.md",
    "docs/getting-started.md",
    "docs/concepts.md",
    "docs/system-design.md",
    "docs/isomer-cli.md",
    "docs/workflows.md",
    "docs/houmao-adapter.md",
    "docs/runtime-and-files.md",
    "docs/assumptions-and-roadmap.md",
    "docs/troubleshooting.md",
    "docs/contributing-docs.md",
]

FORBIDDEN_TERMS: list[tuple[str, str]] = [
    ("quest", r"\bquest\b"),
    ("state of the art", r"state of the art"),
    ("research goal", r"research goal"),
    ("control plane", r"control plane"),
]

README_LINK_TARGETS = ["docs/index.md", "docs/getting-started.md", "docs/isomer-cli.md"]
STALE_ISOMER_JSON_PATTERNS = [
    re.compile(r"\bisomer-cli\b[^\n]*\s--json\b"),
    re.compile(r"\bisomer-cli\b[^\n]*\s--format(?:=|\s+)json\b"),
    re.compile(r"^\s*--json\s*$"),
]


def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def run_cli_help(args: list[str]) -> str:
    argv = [sys.executable, "-m", "isomer_labs", *args, "--help"]
    completed = subprocess.run(argv, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        return ""
    return completed.stdout


def _command_name(line: str) -> str | None:
    match = re.match(r"^  (\S+)", line)
    return match.group(1) if match else None


def collect_cli_commands(base_args: list[str], help_text: str) -> list[str]:
    commands: list[str] = []
    in_commands = False
    for line in help_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("Commands:"):
            in_commands = True
            continue
        if in_commands:
            if not stripped or stripped.startswith("Options:"):
                break
            name = _command_name(line)
            if name is None:
                continue
            sub_args = base_args + [name]
            sub_help = run_cli_help(sub_args)
            if "Commands:" in sub_help:
                commands.extend(collect_cli_commands(sub_args, sub_help))
            else:
                commands.append(" ".join(sub_args))
    return commands


def get_public_commands() -> list[str]:
    top_help = run_cli_help([])
    if not top_help:
        return []
    return collect_cli_commands([], top_help)


def check_required_pages(repo_root: Path) -> list[str]:
    issues: list[str] = []
    for relative in REQUIRED_PAGES:
        path = repo_root / relative
        if not path.is_file():
            issues.append(f"Missing required docs page: {relative}")
    return issues


def check_readme_links(repo_root: Path) -> list[str]:
    readme = repo_root / "README.md"
    if not readme.is_file():
        return ["README.md is missing"]
    content = readme.read_text(encoding="utf-8")
    if not any(target in content for target in README_LINK_TARGETS):
        return ["README.md does not link to docs/index.md, docs/getting-started.md, or docs/isomer-cli.md"]
    return []


def check_cli_coverage(repo_root: Path, commands: list[str]) -> list[str]:
    cli_doc = repo_root / "docs" / "isomer-cli.md"
    if not cli_doc.is_file():
        return ["docs/isomer-cli.md is missing"]
    content = cli_doc.read_text(encoding="utf-8")
    issues: list[str] = []
    for command in commands:
        if command not in content:
            issues.append(f"docs/isomer-cli.md missing command: {command}")
    return issues


def _without_inline_code(content: str) -> str:
    """Return content with inline code spans replaced by spaces of equal length."""
    return re.sub(r"`[^`]*`", lambda match: " " * len(match.group(0)), content)


def check_forbidden_terms(repo_root: Path) -> list[str]:
    issues: list[str] = []
    docs_dir = repo_root / "docs"
    for path in sorted(docs_dir.glob("*.md")):
        content = path.read_text(encoding="utf-8")
        searchable = _without_inline_code(content)
        for label, pattern in FORBIDDEN_TERMS:
            for match in re.finditer(pattern, searchable, flags=re.IGNORECASE):
                line_number = content[: match.start()].count("\n") + 1
                issues.append(f"{path.name}:{line_number}: forbidden term '{label}'")
    return issues


def check_stale_isomer_cli_json_examples(repo_root: Path) -> list[str]:
    issues: list[str] = []
    paths = [repo_root / "README.md", *sorted((repo_root / "docs").glob("*.md"))]
    for path in paths:
        if not path.is_file():
            continue
        content = path.read_text(encoding="utf-8")
        for line_number, line in enumerate(content.splitlines(), start=1):
            if any(pattern.search(line) for pattern in STALE_ISOMER_JSON_PATTERNS):
                issues.append(
                    f"{path.relative_to(repo_root)}:{line_number}: use root-level isomer-cli --print-json instead of command-local JSON flags"
                )
    return issues


def validate_docs(repo_root: Path) -> list[str]:
    issues: list[str] = []
    issues.extend(check_required_pages(repo_root))
    issues.extend(check_readme_links(repo_root))
    commands = get_public_commands()
    if not commands:
        issues.append("Could not discover public isomer-cli commands")
    else:
        issues.extend(check_cli_coverage(repo_root, commands))
    issues.extend(check_stale_isomer_cli_json_examples(repo_root))
    issues.extend(check_forbidden_terms(repo_root))
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=get_repo_root(),
        help="Repository root to validate.",
    )
    args = parser.parse_args()

    issues = validate_docs(args.repo_root)
    if issues:
        print("Documentation validation failed:", file=sys.stderr)
        for issue in issues:
            print(f"  - {issue}", file=sys.stderr)
        return 1

    print("Documentation validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
