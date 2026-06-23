#!/usr/bin/env python3
"""Validate Isomer skillset namespaces."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import validate_research_paradigm_skillset as research_validator


FRONTMATTER_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*?)\s*$")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
CODE_SPAN_RE = re.compile(r"`([^`]+)`")
LOCAL_REFERENCE_PREFIXES = ("references/", "assets/", "scripts/", "subcommands/")
TOPIC_TEAM_SPECIALIZATION_SKILL = "isomer-admin-topic-team-specialize"

MIGRATED_OPERATOR_SKILLS = (
    "isomer-rsch-project-aware",
    "isomer-rsch-service-request-route",
    "isomer-rsch-template-inspect",
    "isomer-rsch-topic-context-resolve",
    "isomer-rsch-placeholder-reconcile",
    "isomer-rsch-topic-profile-draft",
    "isomer-rsch-profile-review-approval",
    "isomer-rsch-profile-materialize",
    "isomer-rsch-team-launch-orchestrate",
    "isomer-rsch-topic-service-agent-support",
)

ACTIVE_REF_ROOTS = (
    ".imsight-arts",
    "docs",
    "openspec/specs",
    "skillset",
    "src",
    "teams",
    "tests",
)
ACTIVE_REF_FILES = ("AGENTS.md", "ROADMAP.md", "pyproject.toml")
ACTIVE_REF_SUFFIXES = {".md", ".toml", ".yaml", ".yml", ".py", ".json"}

TOPIC_TEAM_SPECIALIZATION_REQUIRED_SKILL_TERMS = (
    "## Subskills",
    "team-specialization-guide.md",
    "team-specialization-plan.md",
    "Generated Guide",
    "Final Report",
    "<topic-workspace>/team-profile/execplan/",
)

TOPIC_TEAM_SPECIALIZATION_SUBSKILLS = (
    "project-awareness.md",
    "template-inspection.md",
    "topic-context-resolution.md",
    "service-request-routing.md",
    "placeholder-reconciliation.md",
    "topic-profile-drafting.md",
    "profile-review-approval.md",
    "profile-materialization.md",
    "team-launch-orchestration.md",
)

INCORPORATED_OPERATOR_SKILLS = (
    "isomer-admin-project-aware",
    "isomer-admin-template-inspect",
    "isomer-admin-topic-context-resolve",
    "isomer-admin-service-request-route",
    "isomer-admin-placeholder-reconcile",
    "isomer-admin-topic-profile-draft",
    "isomer-admin-profile-review-approval",
    "isomer-admin-profile-materialize",
    "isomer-admin-team-launch-orchestrate",
)

DEEPSCI_MINI_GUIDE_REQUIRED_TERMS = (
    "placeholder",
    "assumption",
    "workflow",
    "contract",
    "cooperation example",
    "deepsci-mini-lead",
    "deepsci-mini-scout",
    "deepsci-mini-synth-reviewer",
    "<topic-workspace>/team-profile/execplan/",
)


@dataclass(frozen=True, order=True)
class Diagnostic:
    path: str
    line: int
    code: str
    message: str

    def render(self) -> str:
        return f"{self.path}:{self.line}: {self.code} {self.message}"


def find_repo_root(start: Path) -> Path:
    current = start.resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / "pyproject.toml").exists() and (candidate / "skillset").exists():
            return candidate
        if (candidate / ".git").exists():
            return candidate
    return current


def relpath(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def read_lines(path: Path) -> tuple[str, ...]:
    return tuple(path.read_text(encoding="utf-8").splitlines())


def first_line_containing(lines: tuple[str, ...], term: str) -> int:
    for line_number, line in enumerate(lines, start=1):
        if term in line:
            return line_number
    return 1


def line_index_containing(lines: tuple[str, ...], term: str) -> int | None:
    for index, line in enumerate(lines):
        if term in line:
            return index
    return None


def has_numbered_step_after(lines: tuple[str, ...], start_index: int) -> bool:
    for line in lines[start_index + 1 :]:
        if line.startswith("## ") and line.strip() != "## Workflow":
            return False
        if re.match(r"^\d+\.\s+", line):
            return True
    return False


def strip_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_frontmatter(lines: tuple[str, ...]) -> dict[str, str]:
    if not lines or lines[0].strip() != "---":
        return {}
    end = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end = index
            break
    if end is None:
        return {}
    fields: dict[str, str] = {}
    for line in lines[1:end]:
        match = FRONTMATTER_RE.match(line)
        if match:
            fields[match.group(1)] = strip_scalar(match.group(2))
    return fields


def parse_interface_fields(lines: tuple[str, ...]) -> dict[str, tuple[str, int]]:
    fields: dict[str, tuple[str, int]] = {}
    in_interface = False
    for line_number, line in enumerate(lines, start=1):
        if re.match(r"^interface:\s*$", line):
            in_interface = True
            continue
        if in_interface and line and not line.startswith((" ", "\t")):
            in_interface = False
        if not in_interface:
            continue
        match = re.match(r"^\s+([A-Za-z0-9_-]+):\s*(.*?)\s*$", line)
        if match:
            fields[match.group(1)] = (strip_scalar(match.group(2)), line_number)
    return fields


def add(
    diagnostics: list[Diagnostic],
    repo_root: Path,
    path: Path,
    line: int,
    code: str,
    message: str,
) -> None:
    diagnostics.append(Diagnostic(relpath(path, repo_root), max(line, 1), code, message))


def clean_reference(raw: str) -> str | None:
    value = raw.strip().strip("<>").strip()
    if "://" in value or value.startswith("#"):
        return None
    value = value.split("#", 1)[0].strip()
    value = value.strip(".,;:)")
    if any(value.startswith(prefix) for prefix in LOCAL_REFERENCE_PREFIXES):
        return value
    return None


def local_references_from_line(line: str) -> Iterable[str]:
    for match in CODE_SPAN_RE.finditer(line):
        cleaned = clean_reference(match.group(1))
        if cleaned:
            yield cleaned
    for match in MARKDOWN_LINK_RE.finditer(line):
        destination = match.group(1).split()[0]
        cleaned = clean_reference(destination)
        if cleaned:
            yield cleaned


def validate_simple_skill_layout(
    target: Path,
    repo_root: Path,
    *,
    prefix: str,
    code: str,
    manifest_required: bool,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if not target.exists():
        add(diagnostics, repo_root, target, 1, code, "skillset path does not exist")
        return diagnostics

    skill_dirs = sorted(path for path in target.iterdir() if path.is_dir() and path.name.startswith(prefix))
    if not skill_dirs:
        add(diagnostics, repo_root, target, 1, code, f"no {prefix}* skill folders were found")
    for skill_dir in skill_dirs:
        skill_name = skill_dir.name
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            add(diagnostics, repo_root, skill_dir, 1, code, "skill folder is missing SKILL.md")
            continue
        frontmatter = parse_frontmatter(read_lines(skill_md))
        if frontmatter.get("name") != skill_name:
            add(diagnostics, repo_root, skill_md, 2, code, "frontmatter name must match the skill folder")
        if not frontmatter.get("description"):
            add(diagnostics, repo_root, skill_md, 3, code, "frontmatter description is required")
        validate_local_references(skill_dir, repo_root, diagnostics, code)
        validate_manifest(skill_dir, repo_root, diagnostics, code, manifest_required=manifest_required)
    return diagnostics


def validate_manifest(
    skill_dir: Path,
    repo_root: Path,
    diagnostics: list[Diagnostic],
    code: str,
    *,
    manifest_required: bool,
) -> None:
    skill_name = skill_dir.name
    manifest = skill_dir / "agents" / "openai.yaml"
    if not manifest.exists():
        if manifest_required:
            add(diagnostics, repo_root, skill_dir, 1, code, "agents/openai.yaml is required")
        return
    fields = parse_interface_fields(read_lines(manifest))
    display_name = fields.get("display_name")
    if display_name is None:
        add(diagnostics, repo_root, manifest, 1, code, "interface.display_name is required")
    elif display_name[0] != skill_name:
        add(diagnostics, repo_root, manifest, display_name[1], code, f"interface.display_name must be '{skill_name}'")
    default_prompt = fields.get("default_prompt")
    if default_prompt is None:
        add(diagnostics, repo_root, manifest, 1, code, "interface.default_prompt is required")
    elif f"${skill_name}" not in default_prompt[0]:
        add(diagnostics, repo_root, manifest, default_prompt[1], code, f"interface.default_prompt must invoke ${skill_name}")


def validate_local_references(skill_dir: Path, repo_root: Path, diagnostics: list[Diagnostic], code: str) -> None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return
    skill_root = skill_dir.resolve()
    for line_number, line in enumerate(read_lines(skill_md), start=1):
        for reference in local_references_from_line(line):
            target = (skill_dir / reference).resolve()
            if not target.is_relative_to(skill_root) or not target.exists():
                add(diagnostics, repo_root, skill_md, line_number, code, f"local reference '{reference}' does not exist inside {skill_dir.name}")


def iter_active_ref_files(repo_root: Path) -> Iterable[Path]:
    for root_name in ACTIVE_REF_ROOTS:
        root = repo_root / root_name
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.suffix in ACTIVE_REF_SUFFIXES:
                yield path
    for file_name in ACTIVE_REF_FILES:
        path = repo_root / file_name
        if path.exists():
            yield path


def validate_migrated_operator_refs(repo_root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    pattern = re.compile("|".join(re.escape(name) for name in MIGRATED_OPERATOR_SKILLS))
    for path in sorted(set(iter_active_ref_files(repo_root))):
        lines = read_lines(path)
        for line_number, line in enumerate(lines, start=1):
            match = pattern.search(line)
            if match:
                add(
                    diagnostics,
                    repo_root,
                    path,
                    line_number,
                    "OPS002",
                    f"migrated operator skill '{match.group(0)}' must use the new operator or service skill name",
                )
    return diagnostics


def validate_topic_team_specialization_module(repo_root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    skill_dir = repo_root / "skillset" / "operator" / TOPIC_TEAM_SPECIALIZATION_SKILL
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        add(diagnostics, repo_root, skill_md, 1, "OPS003", f"{TOPIC_TEAM_SPECIALIZATION_SKILL} is required")
        return diagnostics
    if (skill_dir / "evals").exists():
        add(diagnostics, repo_root, skill_dir / "evals", 1, "OPS003", f"{TOPIC_TEAM_SPECIALIZATION_SKILL} must not contain evals/")
    for incorporated_skill in INCORPORATED_OPERATOR_SKILLS:
        incorporated_path = repo_root / "skillset" / "operator" / incorporated_skill
        if incorporated_path.exists():
            add(
                diagnostics,
                repo_root,
                incorporated_path,
                1,
                "OPS003",
                f"{incorporated_skill} has been incorporated into {TOPIC_TEAM_SPECIALIZATION_SKILL} and must not be a standalone skill",
            )
    lines = read_lines(skill_md)
    text = "\n".join(lines)
    for term in TOPIC_TEAM_SPECIALIZATION_REQUIRED_SKILL_TERMS:
        if term not in text:
            add(
                diagnostics,
                repo_root,
                skill_md,
                first_line_containing(lines, "# Isomer"),
                "OPS003",
                f"{TOPIC_TEAM_SPECIALIZATION_SKILL} must document '{term}'",
            )
    references_dir = skill_dir / "references"
    for subskill_file_name in TOPIC_TEAM_SPECIALIZATION_SUBSKILLS:
        subskill_path = references_dir / subskill_file_name
        if not subskill_path.exists():
            add(diagnostics, repo_root, subskill_path, 1, "OPS003", f"{TOPIC_TEAM_SPECIALIZATION_SKILL} must include references/{subskill_file_name}")
            continue
        if f"references/{subskill_file_name}" not in text:
            add(diagnostics, repo_root, skill_md, first_line_containing(lines, "## Subskills"), "OPS003", f"{TOPIC_TEAM_SPECIALIZATION_SKILL} must link references/{subskill_file_name}")
        subskill_lines = read_lines(subskill_path)
        workflow_index = line_index_containing(subskill_lines, "## Workflow")
        if workflow_index is None:
            add(diagnostics, repo_root, subskill_path, 1, "OPS003", f"references/{subskill_file_name} must include a ## Workflow section")
            continue
        if workflow_index > 8:
            add(diagnostics, repo_root, subskill_path, workflow_index + 1, "OPS003", f"references/{subskill_file_name} must place ## Workflow near the top")
        if not has_numbered_step_after(subskill_lines, workflow_index):
            add(diagnostics, repo_root, subskill_path, workflow_index + 1, "OPS003", f"references/{subskill_file_name} workflow must use numbered steps")
        if "does not map cleanly" not in "\n".join(subskill_lines):
            add(diagnostics, repo_root, subskill_path, workflow_index + 1, "OPS003", f"references/{subskill_file_name} must include a freeform fallback")
    return diagnostics


def validate_deepsci_mini_specialization_guide(repo_root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    guide = repo_root / "teams" / "deepsci-mini" / "execplan" / "team-specialization-guide.md"
    if not guide.exists():
        add(diagnostics, repo_root, guide, 1, "OPS004", "deepsci-mini must include team-specialization-guide.md")
        return diagnostics
    lines = read_lines(guide)
    text = "\n".join(lines).lower()
    for term in DEEPSCI_MINI_GUIDE_REQUIRED_TERMS:
        if term.lower() not in text:
            add(
                diagnostics,
                repo_root,
                guide,
                first_line_containing(lines, "# deepsci-mini"),
                "OPS004",
                f"deepsci-mini specialization guide must describe '{term}'",
            )
    return diagnostics


def validate_operator_skillset(repo_root: Path) -> list[Diagnostic]:
    diagnostics = validate_simple_skill_layout(
        repo_root / "skillset" / "operator",
        repo_root,
        prefix="isomer-admin-",
        code="OPS001",
        manifest_required=True,
    )
    diagnostics.extend(validate_migrated_operator_refs(repo_root))
    diagnostics.extend(validate_topic_team_specialization_module(repo_root))
    diagnostics.extend(validate_deepsci_mini_specialization_guide(repo_root))
    return sorted(set(diagnostics))


def validate_service_skillset(repo_root: Path) -> list[Diagnostic]:
    return sorted(
        set(
            validate_simple_skill_layout(
                repo_root / "skillset" / "service",
                repo_root,
                prefix="isomer-srv-",
                code="SVS001",
                manifest_required=False,
            )
        )
    )


def validate_all(repo_root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    diagnostics.extend(
        Diagnostic(item.path, item.line, item.code, item.message)
        for item in research_validator.validate_skillset(repo_root / "skillset" / "research-paradigm", repo_root)
    )
    diagnostics.extend(validate_operator_skillset(repo_root))
    diagnostics.extend(validate_service_skillset(repo_root))
    return sorted(set(diagnostics))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate Isomer skillset namespaces.")
    parser.add_argument(
        "--scope",
        choices=("all", "research", "operator", "service"),
        default="all",
        help="Skillset validation scope.",
    )
    parser.add_argument("--repo-root", type=Path, default=None, help="Repository root for diagnostic paths.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    repo_root = args.repo_root.resolve() if args.repo_root else find_repo_root(Path.cwd())
    if args.scope == "research":
        diagnostics = [
            Diagnostic(item.path, item.line, item.code, item.message)
            for item in research_validator.validate_skillset(repo_root / "skillset" / "research-paradigm", repo_root)
        ]
    elif args.scope == "operator":
        diagnostics = validate_operator_skillset(repo_root)
    elif args.scope == "service":
        diagnostics = validate_service_skillset(repo_root)
    else:
        diagnostics = validate_all(repo_root)
    for diagnostic in diagnostics:
        print(diagnostic.render())
    return 1 if diagnostics else 0


if __name__ == "__main__":
    sys.exit(main())
