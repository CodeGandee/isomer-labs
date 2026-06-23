#!/usr/bin/env python3
"""
Quick validation script for agent skills.

Checks that a skill directory contains SKILL.md with valid YAML frontmatter
and required fields. Does not require PyYAML; it parses the small subset of
YAML used in skill frontmatter.
"""

import re
import sys
from pathlib import Path


# Top-level keys allowed in skill frontmatter.
ALLOWED_PROPERTIES = {"name", "description", "license", "compatibility", "metadata"}


def _parse_frontmatter(frontmatter_text: str) -> dict[str, str]:
    """Parse a small YAML frontmatter block into a flat string dictionary.

    Supports simple `key: value` lines and folded (`>`) / literal (`|`)
    multiline scalars indented by two or more spaces.
    """
    result: dict[str, str] = {}
    lines = frontmatter_text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.strip().startswith("#"):
            i += 1
            continue

        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not match:
            i += 1
            continue

        key = match.group(1)
        value = match.group(2).strip()

        if value in (">", "|", ">-", "|-"):
            # Folded/literal multiline scalar
            continuation_lines: list[str] = []
            i += 1
            while i < len(lines) and (
                lines[i].startswith("  ") or lines[i].startswith("\t") or not lines[i].strip()
            ):
                if lines[i].strip():
                    continuation_lines.append(lines[i].strip())
                i += 1
            result[key] = " ".join(continuation_lines)
            continue

        result[key] = value.strip('"').strip("'")
        i += 1

    return result


def validate_skill(skill_path: Path) -> tuple[bool, str]:
    """Basic validation of a skill."""
    skill_path = Path(skill_path)

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    content = skill_md.read_text()
    if not content.startswith("---"):
        return False, "No YAML frontmatter found"

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    try:
        frontmatter = _parse_frontmatter(frontmatter_text)
    except Exception as e:
        return False, f"Invalid frontmatter: {e}"

    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, (
            f"Unexpected key(s) in SKILL.md frontmatter: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed properties are: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    if "name" not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if "description" not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    name = frontmatter.get("name", "")
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"
    name = name.strip()
    if name:
        if not re.match(r"^[a-z0-9-]+$", name):
            return False, f"Name '{name}' should be kebab-case (lowercase letters, digits, and hyphens only)"
        if name.startswith("-") or name.endswith("-") or "--" in name:
            return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
        if len(name) > 64:
            return False, f"Name is too long ({len(name)} characters). Maximum is 64 characters."

    description = frontmatter.get("description", "")
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"
    description = description.strip()
    if description:
        if "<" in description or ">" in description:
            return False, "Description cannot contain angle brackets (< or >)"
        if len(description) > 1024:
            return False, f"Description is too long ({len(description)} characters). Maximum is 1024 characters."

    compatibility = frontmatter.get("compatibility", "")
    if compatibility:
        if not isinstance(compatibility, str):
            return False, f"Compatibility must be a string, got {type(compatibility).__name__}"
        if len(compatibility) > 500:
            return False, f"Compatibility is too long ({len(compatibility)} characters). Maximum is 500 characters."

    return True, "Skill is valid!"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)

    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
