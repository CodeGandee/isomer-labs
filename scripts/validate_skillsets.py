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
PROJECT_MANAGER_SKILL = "isomer-admin-project-mgr"
TOPIC_WORKSPACE_MANAGER_SKILL = "isomer-admin-topic-workspace-mgr"

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
    "Default help mode",
    "invoked without a prompt",
    "Manual mode",
    "Automatic mode",
    "## Subcommands",
    "Procedural Subcommands",
    "Helper Subcommands",
    "Misc Subcommands",
    "references/help.md",
    "init-topic",
    "clarify-topic",
    "ensure-topic-registration",
    "specialize-team",
    "clarify-topic-team",
    "setup-topic-env",
    "setup-agent-workspace",
    "validate-topic-team",
    "finalize-topic-team",
    "fast-forward",
    "step-by-step",
    "load only its detail page",
    "static material readiness",
    "durable setup state",
    "topic-overview.md",
    "concrete Research Topic",
    "default Research Topic",
    "provisional topic workspace seed",
    "isomer-content/topic-ws/<topic-slug>/",
    "team-specialization-guide.md",
    "team-specialization-plan.md",
    "```generated-guide",
    "Generated Guide",
    "Final Report",
    "<topic-workspace>/team-profile/execplan/",
    "isomer-topic-summary.md",
    "selected_domain_team_template_ref",
    "topic_environment_status",
    "semantic label evidence",
    "topic.main_repo",
    "agent.workspace",
    "required `agent.*` support paths",
    "agent_workspace_paths",
    "semantic_paths",
    "semantic labels",
    "path sources",
    "topic_team_validation_status",
    "isomer_topic_summary_path",
    "isomer-managed/",
)

TOPIC_TEAM_SPECIALIZATION_REFERENCE_REQUIRED_TERMS = {
    "help.md": (
        "semantic path evidence",
        "semantic_paths",
        "topic.main_repo",
        "agent.workspace",
    ),
    "setup-agent-workspace.md": (
        "topic.main_repo",
        "agent.workspace",
        "required `agent.*` support paths",
        "semantic_paths",
        "path sources",
        "default-looking directories without semantic labels and path sources",
    ),
    "validate-topic-team.md": (
        "topic.main_repo",
        "agent.workspace",
        "required `agent.*` support labels",
        "semantic_paths",
        "path sources",
        "hard-coded default-only paths without semantic labels",
    ),
    "finalize-topic-team.md": (
        "semantic labels first",
        "topic.main_repo",
        "agent.workspace",
        "path sources",
        "isomer-default.v1",
        "hard-coded default-only paths without semantic label",
    ),
}

TOPIC_TEAM_SPECIALIZATION_SUBCOMMANDS = (
    "help.md",
    "init-topic.md",
    "clarify-topic.md",
    "ensure-topic-registration.md",
    "specialize-team.md",
    "clarify-topic-team.md",
    "setup-topic-env.md",
    "setup-agent-workspace.md",
    "validate-topic-team.md",
    "finalize-topic-team.md",
    "resolve-project.md",
    "inspect-template.md",
    "resolve-context.md",
    "map-placeholders.md",
    "draft-profile.md",
    "approve-profile.md",
    "materialize-profile.md",
    "fast-forward.md",
    "step-by-step.md",
)

TOPIC_TEAM_SPECIALIZATION_PROCEDURAL_SUBCOMMANDS = (
    "init-topic.md",
    "clarify-topic.md",
    "ensure-topic-registration.md",
    "specialize-team.md",
    "clarify-topic-team.md",
    "setup-topic-env.md",
    "setup-agent-workspace.md",
    "validate-topic-team.md",
    "finalize-topic-team.md",
    "approve-profile.md",
    "materialize-profile.md",
)

TOPIC_TEAM_SPECIALIZATION_HELP_FORBIDDEN_SUBCOMMANDS = (
    "launch-team",
    "resolve-project",
    "inspect-template",
    "resolve-context",
    "map-placeholders",
    "draft-profile",
)

TOPIC_TEAM_SPECIALIZATION_HELP_TABLE_TERMS = (
    "| Subcommand | Purpose | Produces |",
    "| --- | --- | --- |",
)

TOPIC_TEAM_SPECIALIZATION_NAMING_EXCEPTIONS = {"help", "step-by-step"}
TOPIC_TEAM_SPECIALIZATION_LENGTH_EXCEPTIONS = {"ensure-topic-registration"}

TOPIC_TEAM_SPECIALIZATION_SUPPORT_REFERENCES = (
    "isomer-domain-language.md",
    "runtime-and-file-boundaries.md",
)

TOPIC_TEAM_SPECIALIZATION_FORBIDDEN_SUPPORT_REFS = (
    ".imsight-arts/",
    "docs/",
    "extern/",
    "/data/",
    "/home/",
)

PROJECT_MANAGER_REQUIRED_SKILL_TERMS = (
    "Default help mode",
    "invoked without a prompt",
    "## Subcommands",
    "references/help.md",
    "init-project",
    "cleanup-project",
    "move-content",
    "check-project",
    "list-topics",
    "show-context",
    "init-runtime",
    "prep-runtime",
    "specialize-team",
    "load only the selected subcommand page",
    ".isomer-labs/",
    "isomer-content/",
    "isomer-content/topic-ws/<topic-id>/",
    "--content-dir <content-dir>",
    "<content-dir>/topic-ws/<topic-id>/",
    ".isomer-labs/.houmao/",
    "external user-owned",
    "Isomer-managed Houmao overlay",
    "isomer-cli project init",
    "isomer-cli project cleanup --part <part> --dry-run",
    "isomer-cli project cleanup --part <part> --yes",
    "--purge-content-root",
    "isomer-cli project content-root move --to <content-dir> --dry-run",
    "isomer-cli project content-root move --to <content-dir> --yes",
    "unknown files",
    "isomer-cli project validate",
    "isomer-cli project doctor",
    "isomer-cli project runtime init",
    "isomer-cli project runtime prepare",
    "isomer-admin-topic-team-specialize",
)

PROJECT_MANAGER_FORBIDDEN_CLI_TERMS = (
    "isomer-cli init",
    "isomer-cli validate",
    "isomer-cli doctor",
    "isomer-cli topics",
    "isomer-cli workspaces",
    "isomer-cli context",
    "isomer-cli paths",
    "isomer-cli runtime",
    "isomer-cli team-",
    "isomer-cli handoffs",
    "isomer-cli cleanup",
    "isomer-cli --project",
)

PROJECT_MANAGER_SUBCOMMANDS = (
    "help.md",
    "init-project.md",
    "cleanup-project.md",
    "move-content.md",
    "check-project.md",
    "list-topics.md",
    "show-context.md",
    "init-runtime.md",
    "prep-runtime.md",
    "specialize-team.md",
)

PROJECT_MANAGER_NAMING_EXCEPTIONS = {"help"}

PROJECT_MANAGER_SUPPORT_REFERENCES = (
    "project-concepts.md",
    "cli-command-boundaries.md",
    "houmao-bootstrap.md",
    "runtime-boundaries.md",
)

PROJECT_MANAGER_FORBIDDEN_SUPPORT_REFS = TOPIC_TEAM_SPECIALIZATION_FORBIDDEN_SUPPORT_REFS

TOPIC_WORKSPACE_MANAGER_REQUIRED_SKILL_TERMS = (
    "topic-workspace",
    "Default subcommand",
    "## Subcommands",
    "Procedural Subcommands",
    "Helper Subcommands",
    "Misc Subcommands",
    "references/topic-workspace.md",
    "resolve-workspace",
    "ensure-main-repo",
    "plan-agents",
    "create-worktrees",
    "write-boundaries",
    "create-agent-branch",
    "validate-worktrees",
    "summarize",
    "help",
    "semantic workspace labels",
    "Topic Workspace Manifest",
    "isomer-default.v1",
    "topic.main_repo",
    "topic.main_repo.isomer_managed",
    "topic.agents_root",
    "agent.workspace",
    "agent.private_artifacts",
    "agent.public_share",
    "agent.links",
    "semantic_paths",
    "topic-owner/main",
    "per-agent/<agent-name>/main",
    "per-agent/<agent-name>/<branch-name>",
    "agent_name",
    "agent_branch",
    "agent_workspace_ref",
    "isomer-managed/",
    "tracked/",
    "agent-owned/",
    "topic-owned/",
    "links/",
    "topic.records.*",
    "Agent Instance",
    "Workspace Runtime",
    "Houmao",
    "Execution Adapter",
    "Workspace Boundary",
    "Peer Read Access",
    "blockers",
    "next_operator_action",
)

TOPIC_WORKSPACE_MANAGER_SUBCOMMANDS = (
    "resolve-workspace.md",
    "ensure-main-repo.md",
    "plan-agents.md",
    "create-worktrees.md",
    "write-boundaries.md",
    "create-agent-branch.md",
    "validate-worktrees.md",
    "summarize.md",
    "help.md",
    "topic-workspace.md",
)

TOPIC_WORKSPACE_MANAGER_HELP_TABLE_TERMS = (
    "| Subcommand | Purpose | Produces |",
    "| --- | --- | --- |",
)

TOPIC_WORKSPACE_MANAGER_NAMING_EXCEPTIONS = {"help", "summarize", "topic-workspace"}

TOPIC_WORKSPACE_MANAGER_REFERENCE_REQUIRED_TERMS = (
    "blocker",
)

TOPIC_WORKSPACE_MANAGER_SEMANTIC_REFERENCE_REQUIRED_TERMS = {
    "resolve-workspace.md": (
        "isomer-cli project paths get",
        "semantic_paths",
        "topic.main_repo",
        "agent.workspace",
    ),
    "ensure-main-repo.md": (
        "topic.main_repo",
        "topic.main_repo.isomer_managed",
        "isomer-default.v1",
    ),
    "plan-agents.md": (
        "agent.workspace",
        "Workspace Path Resolution",
        "path sources",
    ),
    "create-worktrees.md": (
        "agent.workspace",
        "topic.main_repo",
        "path sources",
        "semantic support paths",
    ),
    "write-boundaries.md": (
        "topic.main_repo",
        "agent.workspace",
        "path source",
        "without passing Agent Name",
    ),
    "validate-worktrees.md": (
        "semantic label bindings",
        "hard-coded default-only evidence",
    ),
    "summarize.md": (
        "semantic_paths",
        "cwd-friendly guidance",
        "without passing Agent Name",
    ),
    "topic-workspace.md": (
        "`agent.workspace` path plans",
        "Missing semantic label evidence",
    ),
}

TOPIC_WORKSPACE_MANAGER_FORBIDDEN_PUBLIC_TERMS = (
    "agent-key",
    "agent key",
    "<agent-key>",
    ".isomer-agent/",
)

TOPIC_WORKSPACE_MANAGER_FORBIDDEN_SUPPORT_REFS = TOPIC_TEAM_SPECIALIZATION_FORBIDDEN_SUPPORT_REFS

TOPIC_ENV_SETUP_SERVICE_SKILL = "isomer-srv-topic-env-setup"

TOPIC_ENV_SETUP_REQUIRED_SKILL_TERMS = (
    "setup-topic-env",
    "resolve-topic-workspace",
    "read-env-gate",
    "ensure-topic-repos",
    "derive-env-gate",
    "install-topic-deps",
    "verify-env-gate",
    "single capable agent or operator",
    "Topic environment setup is independent of Topic Agent Team structure",
    "Do not require or inspect Topic Agent Team Profile material",
    "agent count",
    "pixi run --manifest-path <manifest_path> --environment <pixi_environment>",
    "pixi add --manifest-path <manifest_path>",
    "pixi install --manifest-path <manifest_path> --environment <pixi_environment>",
    ".isomer-user-env/",
    "sudo",
    "semantic_paths",
    "topic.workspace",
    "topic.main_repo",
    "topic.records",
    "topic.runtime",
    "agent-scoped target",
    "resolve the appropriate topic repository label",
)

TOPIC_ENV_SETUP_REFERENCE_REQUIRED_TERMS = {
    "resolve-topic-workspace.md": (
        "semantic_paths",
        "topic.main_repo",
        "topic.records",
        "topic.runtime",
        "path source",
    ),
    "ensure-topic-repos.md": (
        "semantic_paths",
        "resolved topic repository root",
        "semantic label and path source",
        "Do not place task repos",
    ),
    "setup-topic-env.md": (
        "semantic_paths",
        "topic.main_repo",
        "topic.tmp",
        "local, ignored, disposable, not shared, and not durable evidence",
    ),
}

TOPIC_ENV_SETUP_SUBCOMMANDS = (
    "resolve-topic-workspace.md",
    "read-env-gate.md",
    "ensure-topic-repos.md",
    "derive-env-gate.md",
    "install-topic-deps.md",
    "verify-env-gate.md",
    "setup-topic-env.md",
)

TOPIC_ENV_SETUP_REMOVED_SUBCOMMANDS = (
    "resolve-workspace.md",
    "read-gate.md",
    "ensure-repos.md",
    "derive-gate.md",
    "install-deps.md",
    "verify-gate.md",
    "setup-for-topic-workspace.md",
)

TOPIC_ENV_SETUP_INDEPENDENCE_TERMS = (
    "Do not block solely because `<topic-workspace>/team-profile/`",
    "non-blocking for this subcommand unless",
    "one agent or operator",
    "Do not require `team-profile/`",
    "Do not require or verify `team-profile/`",
)

REMOVED_OPERATOR_SKILLS = (
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
    for removed_skill in REMOVED_OPERATOR_SKILLS:
        removed_path = repo_root / "skillset" / "operator" / removed_skill
        if removed_path.exists():
            add(
                diagnostics,
                repo_root,
                removed_path,
                1,
                "OPS003",
                f"{removed_skill} is no longer part of the active operator skillset and must not be a standalone skill",
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
    skill_workflow_index = line_index_containing(lines, "## Workflow")
    if skill_workflow_index is None:
        add(diagnostics, repo_root, skill_md, 1, "OPS003", f"{TOPIC_TEAM_SPECIALIZATION_SKILL} must include a ## Workflow section")
    else:
        if skill_workflow_index > 24:
            add(diagnostics, repo_root, skill_md, skill_workflow_index + 1, "OPS003", f"{TOPIC_TEAM_SPECIALIZATION_SKILL} must place ## Workflow near the top")
        if not has_numbered_step_after(lines, skill_workflow_index):
            add(diagnostics, repo_root, skill_md, skill_workflow_index + 1, "OPS003", f"{TOPIC_TEAM_SPECIALIZATION_SKILL} workflow must use numbered steps")
        if "does not map cleanly" not in text:
            add(diagnostics, repo_root, skill_md, skill_workflow_index + 1, "OPS003", f"{TOPIC_TEAM_SPECIALIZATION_SKILL} must include a freeform fallback")
    references_dir = skill_dir / "references"
    for support_file_name in TOPIC_TEAM_SPECIALIZATION_SUPPORT_REFERENCES:
        support_path = references_dir / support_file_name
        if not support_path.exists():
            add(diagnostics, repo_root, support_path, 1, "OPS003", f"{TOPIC_TEAM_SPECIALIZATION_SKILL} must include references/{support_file_name}")
    allowed_reference_names = set(TOPIC_TEAM_SPECIALIZATION_SUBCOMMANDS) | set(TOPIC_TEAM_SPECIALIZATION_SUPPORT_REFERENCES)
    for reference_path in sorted(references_dir.glob("*.md")):
        if reference_path.name not in allowed_reference_names:
            add(
                diagnostics,
                repo_root,
                reference_path,
                1,
                "OPS003",
                f"{TOPIC_TEAM_SPECIALIZATION_SKILL} has unexpected reference page references/{reference_path.name}",
            )
    for skill_file in sorted(path for path in skill_dir.rglob("*") if path.is_file() and path.suffix in ACTIVE_REF_SUFFIXES):
        skill_file_lines = read_lines(skill_file)
        for line_number, line in enumerate(skill_file_lines, start=1):
            for forbidden_ref in TOPIC_TEAM_SPECIALIZATION_FORBIDDEN_SUPPORT_REFS:
                if forbidden_ref in line:
                    add(
                        diagnostics,
                        repo_root,
                        skill_file,
                        line_number,
                        "OPS003",
                        f"{TOPIC_TEAM_SPECIALIZATION_SKILL} must keep required support references inside its skill directory; found '{forbidden_ref}'",
                    )
    for subcommand_file_name in TOPIC_TEAM_SPECIALIZATION_SUBCOMMANDS:
        subcommand_name = subcommand_file_name.removesuffix(".md")
        subcommand_path = references_dir / subcommand_file_name
        if subcommand_name not in TOPIC_TEAM_SPECIALIZATION_NAMING_EXCEPTIONS and not re.match(r"^[a-z]+(?:-[a-z]+)+$", subcommand_name):
            add(diagnostics, repo_root, subcommand_path, 1, "OPS003", f"subcommand '{subcommand_name}' must be a short verb-object name or an allowed command")
        if len(subcommand_name) > 24 and subcommand_name not in TOPIC_TEAM_SPECIALIZATION_LENGTH_EXCEPTIONS:
            add(diagnostics, repo_root, subcommand_path, 1, "OPS003", f"subcommand '{subcommand_name}' must be short")
        if not subcommand_path.exists():
            add(diagnostics, repo_root, subcommand_path, 1, "OPS003", f"{TOPIC_TEAM_SPECIALIZATION_SKILL} must include references/{subcommand_file_name}")
            continue
        if f"references/{subcommand_file_name}" not in text:
            add(diagnostics, repo_root, skill_md, first_line_containing(lines, "## Subcommands"), "OPS003", f"{TOPIC_TEAM_SPECIALIZATION_SKILL} must link references/{subcommand_file_name}")
        subcommand_lines = read_lines(subcommand_path)
        workflow_index = line_index_containing(subcommand_lines, "## Workflow")
        if workflow_index is None:
            add(diagnostics, repo_root, subcommand_path, 1, "OPS003", f"references/{subcommand_file_name} must include a ## Workflow section")
            continue
        if workflow_index > 8:
            add(diagnostics, repo_root, subcommand_path, workflow_index + 1, "OPS003", f"references/{subcommand_file_name} must place ## Workflow near the top")
        if not has_numbered_step_after(subcommand_lines, workflow_index):
            add(diagnostics, repo_root, subcommand_path, workflow_index + 1, "OPS003", f"references/{subcommand_file_name} workflow must use numbered steps")
        subcommand_text = "\n".join(subcommand_lines)
        if "does not map cleanly" not in subcommand_text:
            add(diagnostics, repo_root, subcommand_path, workflow_index + 1, "OPS003", f"references/{subcommand_file_name} must include a freeform fallback")
        if subcommand_file_name in TOPIC_TEAM_SPECIALIZATION_PROCEDURAL_SUBCOMMANDS:
            if "## Prerequisite Artifacts" not in subcommand_text:
                add(diagnostics, repo_root, subcommand_path, 1, "OPS003", f"references/{subcommand_file_name} must document predecessor artifacts")
            if "refuse to run" not in subcommand_text.lower():
                add(diagnostics, repo_root, subcommand_path, 1, "OPS003", f"references/{subcommand_file_name} must refuse to run when predecessor artifacts are missing")
        for required_term in TOPIC_TEAM_SPECIALIZATION_REFERENCE_REQUIRED_TERMS.get(subcommand_file_name, ()):
            if required_term not in subcommand_text:
                add(diagnostics, repo_root, subcommand_path, 1, "OPS003", f"references/{subcommand_file_name} must document '{required_term}'")
    help_path = references_dir / "help.md"
    if help_path.exists():
        help_lines = read_lines(help_path)
        help_text = "\n".join(help_lines)
        for table_term in TOPIC_TEAM_SPECIALIZATION_HELP_TABLE_TERMS:
            if table_term not in help_text:
                add(
                    diagnostics,
                    repo_root,
                    help_path,
                    first_line_containing(help_lines, "## Public Subcommands"),
                    "OPS003",
                    f"references/help.md must print public subcommands as a three-column table including '{table_term}'",
                )
        for helper_subcommand in TOPIC_TEAM_SPECIALIZATION_HELP_FORBIDDEN_SUBCOMMANDS:
            if helper_subcommand in help_text:
                add(
                    diagnostics,
                    repo_root,
                    help_path,
                    first_line_containing(help_lines, helper_subcommand),
                    "OPS003",
                    f"references/help.md must not list private helper subcommand '{helper_subcommand}'",
                )
    return diagnostics


def validate_project_manager_module(repo_root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    skill_dir = repo_root / "skillset" / "operator" / PROJECT_MANAGER_SKILL
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        add(diagnostics, repo_root, skill_md, 1, "OPS005", f"{PROJECT_MANAGER_SKILL} is required")
        return diagnostics
    if (skill_dir / "evals").exists():
        add(diagnostics, repo_root, skill_dir / "evals", 1, "OPS005", f"{PROJECT_MANAGER_SKILL} must not contain evals/")
    lines = read_lines(skill_md)
    text = "\n".join(lines)
    for term in PROJECT_MANAGER_REQUIRED_SKILL_TERMS:
        if term not in text:
            add(
                diagnostics,
                repo_root,
                skill_md,
                first_line_containing(lines, "# Isomer"),
                "OPS005",
                f"{PROJECT_MANAGER_SKILL} must document '{term}'",
            )
    skill_workflow_index = line_index_containing(lines, "## Workflow")
    if skill_workflow_index is None:
        add(diagnostics, repo_root, skill_md, 1, "OPS005", f"{PROJECT_MANAGER_SKILL} must include a ## Workflow section")
    else:
        if skill_workflow_index > 24:
            add(diagnostics, repo_root, skill_md, skill_workflow_index + 1, "OPS005", f"{PROJECT_MANAGER_SKILL} must place ## Workflow near the top")
        if not has_numbered_step_after(lines, skill_workflow_index):
            add(diagnostics, repo_root, skill_md, skill_workflow_index + 1, "OPS005", f"{PROJECT_MANAGER_SKILL} workflow must use numbered steps")
        if "does not map cleanly" not in text:
            add(diagnostics, repo_root, skill_md, skill_workflow_index + 1, "OPS005", f"{PROJECT_MANAGER_SKILL} must include a freeform fallback")
    references_dir = skill_dir / "references"
    for support_file_name in PROJECT_MANAGER_SUPPORT_REFERENCES:
        support_path = references_dir / support_file_name
        if not support_path.exists():
            add(diagnostics, repo_root, support_path, 1, "OPS005", f"{PROJECT_MANAGER_SKILL} must include references/{support_file_name}")
    allowed_reference_names = set(PROJECT_MANAGER_SUBCOMMANDS) | set(PROJECT_MANAGER_SUPPORT_REFERENCES)
    for reference_path in sorted(references_dir.glob("*.md")):
        if reference_path.name not in allowed_reference_names:
            add(
                diagnostics,
                repo_root,
                reference_path,
                1,
                "OPS005",
                f"{PROJECT_MANAGER_SKILL} has unexpected reference page references/{reference_path.name}",
            )
    for skill_file in sorted(path for path in skill_dir.rglob("*") if path.is_file() and path.suffix in ACTIVE_REF_SUFFIXES):
        skill_file_lines = read_lines(skill_file)
        for line_number, line in enumerate(skill_file_lines, start=1):
            for forbidden_ref in PROJECT_MANAGER_FORBIDDEN_SUPPORT_REFS:
                if forbidden_ref in line:
                    add(
                        diagnostics,
                        repo_root,
                        skill_file,
                        line_number,
                        "OPS005",
                        f"{PROJECT_MANAGER_SKILL} must keep required support references inside its skill directory; found '{forbidden_ref}'",
                    )
            for forbidden_cli_term in PROJECT_MANAGER_FORBIDDEN_CLI_TERMS:
                if forbidden_cli_term in line:
                    add(
                        diagnostics,
                        repo_root,
                        skill_file,
                        line_number,
                        "OPS005",
                        f"{PROJECT_MANAGER_SKILL} must use 'isomer-cli project ...' command shapes instead of '{forbidden_cli_term}'",
                    )
    for subcommand_file_name in PROJECT_MANAGER_SUBCOMMANDS:
        subcommand_name = subcommand_file_name.removesuffix(".md")
        subcommand_path = references_dir / subcommand_file_name
        if subcommand_name not in PROJECT_MANAGER_NAMING_EXCEPTIONS and not re.match(r"^[a-z]+(?:-[a-z]+)+$", subcommand_name):
            add(diagnostics, repo_root, subcommand_path, 1, "OPS005", f"subcommand '{subcommand_name}' must be a short verb-object name or an allowed command")
        if len(subcommand_name) > 24:
            add(diagnostics, repo_root, subcommand_path, 1, "OPS005", f"subcommand '{subcommand_name}' must be short")
        if not subcommand_path.exists():
            add(diagnostics, repo_root, subcommand_path, 1, "OPS005", f"{PROJECT_MANAGER_SKILL} must include references/{subcommand_file_name}")
            continue
        if f"references/{subcommand_file_name}" not in text:
            add(diagnostics, repo_root, skill_md, first_line_containing(lines, "## Subcommands"), "OPS005", f"{PROJECT_MANAGER_SKILL} must link references/{subcommand_file_name}")
        subcommand_lines = read_lines(subcommand_path)
        workflow_index = line_index_containing(subcommand_lines, "## Workflow")
        if workflow_index is None:
            add(diagnostics, repo_root, subcommand_path, 1, "OPS005", f"references/{subcommand_file_name} must include a ## Workflow section")
            continue
        if workflow_index > 8:
            add(diagnostics, repo_root, subcommand_path, workflow_index + 1, "OPS005", f"references/{subcommand_file_name} must place ## Workflow near the top")
        if not has_numbered_step_after(subcommand_lines, workflow_index):
            add(diagnostics, repo_root, subcommand_path, workflow_index + 1, "OPS005", f"references/{subcommand_file_name} workflow must use numbered steps")
        if "does not map cleanly" not in "\n".join(subcommand_lines):
            add(diagnostics, repo_root, subcommand_path, workflow_index + 1, "OPS005", f"references/{subcommand_file_name} must include a freeform fallback")
    return diagnostics


def validate_topic_workspace_manager_module(repo_root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    skill_dir = repo_root / "skillset" / "operator" / TOPIC_WORKSPACE_MANAGER_SKILL
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        add(diagnostics, repo_root, skill_md, 1, "OPS006", f"{TOPIC_WORKSPACE_MANAGER_SKILL} is required")
        return diagnostics
    if (skill_dir / "evals").exists():
        add(diagnostics, repo_root, skill_dir / "evals", 1, "OPS006", f"{TOPIC_WORKSPACE_MANAGER_SKILL} must not contain evals/")
    lines = read_lines(skill_md)
    text = "\n".join(lines)
    for term in TOPIC_WORKSPACE_MANAGER_REQUIRED_SKILL_TERMS:
        if term not in text:
            add(
                diagnostics,
                repo_root,
                skill_md,
                first_line_containing(lines, "# Isomer"),
                "OPS006",
                f"{TOPIC_WORKSPACE_MANAGER_SKILL} must document '{term}'",
            )
    skill_workflow_index = line_index_containing(lines, "## Workflow")
    if skill_workflow_index is None:
        add(diagnostics, repo_root, skill_md, 1, "OPS006", f"{TOPIC_WORKSPACE_MANAGER_SKILL} must include a ## Workflow section")
    else:
        if skill_workflow_index > 24:
            add(diagnostics, repo_root, skill_md, skill_workflow_index + 1, "OPS006", f"{TOPIC_WORKSPACE_MANAGER_SKILL} must place ## Workflow near the top")
        if not has_numbered_step_after(lines, skill_workflow_index):
            add(diagnostics, repo_root, skill_md, skill_workflow_index + 1, "OPS006", f"{TOPIC_WORKSPACE_MANAGER_SKILL} workflow must use numbered steps")
        if "does not map cleanly" not in text:
            add(diagnostics, repo_root, skill_md, skill_workflow_index + 1, "OPS006", f"{TOPIC_WORKSPACE_MANAGER_SKILL} must include a freeform fallback")
    references_dir = skill_dir / "references"
    allowed_reference_names = set(TOPIC_WORKSPACE_MANAGER_SUBCOMMANDS)
    for reference_path in sorted(references_dir.glob("*.md")):
        if reference_path.name not in allowed_reference_names:
            add(
                diagnostics,
                repo_root,
                reference_path,
                1,
                "OPS006",
                f"{TOPIC_WORKSPACE_MANAGER_SKILL} has unexpected reference page references/{reference_path.name}",
            )
    for skill_file in sorted(path for path in skill_dir.rglob("*") if path.is_file() and path.suffix in ACTIVE_REF_SUFFIXES):
        skill_file_lines = read_lines(skill_file)
        for line_number, line in enumerate(skill_file_lines, start=1):
            for forbidden_term in TOPIC_WORKSPACE_MANAGER_FORBIDDEN_PUBLIC_TERMS:
                if forbidden_term in line:
                    add(
                        diagnostics,
                        repo_root,
                        skill_file,
                        line_number,
                        "OPS006",
                        f"{TOPIC_WORKSPACE_MANAGER_SKILL} must use agent-name public wording instead of stale '{forbidden_term}'",
                    )
            for forbidden_ref in TOPIC_WORKSPACE_MANAGER_FORBIDDEN_SUPPORT_REFS:
                if forbidden_ref in line:
                    add(
                        diagnostics,
                        repo_root,
                        skill_file,
                        line_number,
                        "OPS006",
                        f"{TOPIC_WORKSPACE_MANAGER_SKILL} must keep required support references inside its skill directory; found '{forbidden_ref}'",
                    )
    for subcommand_file_name in TOPIC_WORKSPACE_MANAGER_SUBCOMMANDS:
        subcommand_name = subcommand_file_name.removesuffix(".md")
        subcommand_path = references_dir / subcommand_file_name
        if subcommand_name not in TOPIC_WORKSPACE_MANAGER_NAMING_EXCEPTIONS and not re.match(r"^[a-z]+(?:-[a-z]+)+$", subcommand_name):
            add(diagnostics, repo_root, subcommand_path, 1, "OPS006", f"subcommand '{subcommand_name}' must be a short verb-object name or an allowed command")
        if len(subcommand_name) > 24:
            add(diagnostics, repo_root, subcommand_path, 1, "OPS006", f"subcommand '{subcommand_name}' must be short")
        if not subcommand_path.exists():
            add(diagnostics, repo_root, subcommand_path, 1, "OPS006", f"{TOPIC_WORKSPACE_MANAGER_SKILL} must include references/{subcommand_file_name}")
            continue
        if f"references/{subcommand_file_name}" not in text:
            add(diagnostics, repo_root, skill_md, first_line_containing(lines, "## Subcommands"), "OPS006", f"{TOPIC_WORKSPACE_MANAGER_SKILL} must link references/{subcommand_file_name}")
        subcommand_lines = read_lines(subcommand_path)
        workflow_index = line_index_containing(subcommand_lines, "## Workflow")
        if workflow_index is None:
            add(diagnostics, repo_root, subcommand_path, 1, "OPS006", f"references/{subcommand_file_name} must include a ## Workflow section")
            continue
        if workflow_index > 8:
            add(diagnostics, repo_root, subcommand_path, workflow_index + 1, "OPS006", f"references/{subcommand_file_name} must place ## Workflow near the top")
        if not has_numbered_step_after(subcommand_lines, workflow_index):
            add(diagnostics, repo_root, subcommand_path, workflow_index + 1, "OPS006", f"references/{subcommand_file_name} workflow must use numbered steps")
        subcommand_text = "\n".join(subcommand_lines)
        if "does not map cleanly" not in subcommand_text:
            add(diagnostics, repo_root, subcommand_path, workflow_index + 1, "OPS006", f"references/{subcommand_file_name} must include a freeform fallback")
        for required_term in TOPIC_WORKSPACE_MANAGER_REFERENCE_REQUIRED_TERMS:
            if required_term not in subcommand_text:
                add(diagnostics, repo_root, subcommand_path, 1, "OPS006", f"references/{subcommand_file_name} must document '{required_term}'")
        for required_term in TOPIC_WORKSPACE_MANAGER_SEMANTIC_REFERENCE_REQUIRED_TERMS.get(subcommand_file_name, ()):
            if required_term not in subcommand_text:
                add(diagnostics, repo_root, subcommand_path, 1, "OPS006", f"references/{subcommand_file_name} must document '{required_term}'")
    help_path = references_dir / "help.md"
    if help_path.exists():
        help_lines = read_lines(help_path)
        help_text = "\n".join(help_lines)
        for table_term in TOPIC_WORKSPACE_MANAGER_HELP_TABLE_TERMS:
            if table_term not in help_text:
                add(
                    diagnostics,
                    repo_root,
                    help_path,
                    first_line_containing(help_lines, "## Public Subcommands"),
                    "OPS006",
                    f"references/help.md must print public subcommands as a three-column table including '{table_term}'",
                )
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
    diagnostics.extend(validate_project_manager_module(repo_root))
    diagnostics.extend(validate_topic_workspace_manager_module(repo_root))
    diagnostics.extend(validate_deepsci_mini_specialization_guide(repo_root))
    return sorted(set(diagnostics))


def validate_topic_env_setup_service(repo_root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    old_skill_dir = repo_root / "skillset" / "service" / "isomer-srv-env-setup"
    if old_skill_dir.exists():
        add(diagnostics, repo_root, old_skill_dir, 1, "SVS002", "legacy isomer-srv-env-setup skill folder must be renamed to isomer-srv-topic-env-setup")
    skill_dir = repo_root / "skillset" / "service" / TOPIC_ENV_SETUP_SERVICE_SKILL
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        add(diagnostics, repo_root, skill_md, 1, "SVS002", f"{TOPIC_ENV_SETUP_SERVICE_SKILL} is required")
        return diagnostics
    lines = read_lines(skill_md)
    text = "\n".join(lines)
    for term in TOPIC_ENV_SETUP_REQUIRED_SKILL_TERMS:
        if term not in text:
            add(
                diagnostics,
                repo_root,
                skill_md,
                first_line_containing(lines, "# Isomer"),
                "SVS002",
                f"{TOPIC_ENV_SETUP_SERVICE_SKILL} must document '{term}'",
            )
    references_dir = skill_dir / "references"
    for removed_subcommand in TOPIC_ENV_SETUP_REMOVED_SUBCOMMANDS:
        removed_path = references_dir / removed_subcommand
        if removed_path.exists():
            add(diagnostics, repo_root, removed_path, 1, "SVS002", f"legacy subcommand references/{removed_subcommand} must be renamed")
    allowed_reference_names = set(TOPIC_ENV_SETUP_SUBCOMMANDS)
    for reference_path in sorted(references_dir.glob("*.md")):
        if reference_path.name not in allowed_reference_names:
            add(
                diagnostics,
                repo_root,
                reference_path,
                1,
                "SVS002",
                f"{TOPIC_ENV_SETUP_SERVICE_SKILL} has unexpected reference page references/{reference_path.name}",
            )
    for subcommand_file_name in TOPIC_ENV_SETUP_SUBCOMMANDS:
        subcommand_path = references_dir / subcommand_file_name
        if not subcommand_path.exists():
            add(diagnostics, repo_root, subcommand_path, 1, "SVS002", f"{TOPIC_ENV_SETUP_SERVICE_SKILL} must include references/{subcommand_file_name}")
            continue
        if f"references/{subcommand_file_name}" not in text:
            add(diagnostics, repo_root, skill_md, first_line_containing(lines, "## Subcommands"), "SVS002", f"{TOPIC_ENV_SETUP_SERVICE_SKILL} must link references/{subcommand_file_name}")
        subcommand_lines = read_lines(subcommand_path)
        subcommand_text = "\n".join(subcommand_lines)
        for required_term in TOPIC_ENV_SETUP_REFERENCE_REQUIRED_TERMS.get(subcommand_file_name, ()):
            if required_term not in subcommand_text:
                add(diagnostics, repo_root, subcommand_path, 1, "SVS002", f"references/{subcommand_file_name} must document '{required_term}'")
    for file_name, term in zip(
        ("resolve-topic-workspace.md", "resolve-topic-workspace.md", "read-env-gate.md", "setup-topic-env.md", "verify-env-gate.md"),
        TOPIC_ENV_SETUP_INDEPENDENCE_TERMS,
        strict=True,
    ):
        subcommand_path = references_dir / file_name
        if subcommand_path.exists():
            subcommand_lines = read_lines(subcommand_path)
            subcommand_text = "\n".join(subcommand_lines)
            if term not in subcommand_text:
                add(
                    diagnostics,
                    repo_root,
                    subcommand_path,
                    first_line_containing(subcommand_lines, "#"),
                    "SVS002",
                    f"references/{file_name} must document team-independent environment setup term '{term}'",
                )
    return diagnostics


def validate_service_skillset(repo_root: Path) -> list[Diagnostic]:
    diagnostics = validate_simple_skill_layout(
        repo_root / "skillset" / "service",
        repo_root,
        prefix="isomer-srv-",
        code="SVS001",
        manifest_required=False,
    )
    diagnostics.extend(validate_topic_env_setup_service(repo_root))
    return sorted(set(diagnostics))


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
