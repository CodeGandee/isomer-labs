#!/usr/bin/env python3
"""Validate the research-paradigm skill bundle."""

from __future__ import annotations

import argparse
import fnmatch
import re
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


SKILL_NAME_RE = re.compile(r"^isomer-rsch-[a-z0-9]+(?:-[a-z0-9]+)*$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
FRONTMATTER_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*?)\s*$")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
CODE_SPAN_RE = re.compile(r"`([^`]+)`")
TBD_PLACEHOLDER_RE = re.compile(r"\[\[tbd-surface:([a-z0-9][a-z0-9-]*)\]\]")
RSCH_OBJECT_PLACEHOLDER_RE = re.compile(r"\[\[rsch-object:([a-z0-9][a-z0-9-]*)\]\]")
MIGRATION_PLACEHOLDER_RE = re.compile(r"<([A-Z][A-Z0-9_]*)>")
MIGRATION_PLACEHOLDER_CELL_RE = re.compile(r"^<?([A-Z][A-Z0-9_]*)>?$")
PLACEHOLDER_PATH_SEGMENT_RE = re.compile(r"<[A-Za-z0-9_-]+>")
REGISTRY_ROW_ID_RE = re.compile(r"^(?:path|api|schema|policy|provider)-[a-z0-9-]+$")
SEMANTIC_PLACEHOLDER_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
FORBIDDEN_REPO_LOCAL_ISOMER_CLI = "pixi run isomer-cli"
ACTIVE_REF_SUFFIXES = {".md", ".toml", ".yaml", ".yml", ".py", ".json"}

EXPECTED_V1_SKILLS = frozenset(
    {
        "isomer-rsch-analysis-v1",
        "isomer-rsch-baseline-v1",
        "isomer-rsch-decision-v1",
        "isomer-rsch-experiment-v1",
        "isomer-rsch-figure-polish-v1",
        "isomer-rsch-finalize-v1",
        "isomer-rsch-idea-v1",
        "isomer-rsch-intake-v1",
        "isomer-rsch-optimize-v1",
        "isomer-rsch-paper-outline-v1",
        "isomer-rsch-paper-plot-v1",
        "isomer-rsch-rebuttal-v1",
        "isomer-rsch-review-v1",
        "isomer-rsch-science-v1",
        "isomer-rsch-scout-v1",
        "isomer-rsch-shared-v1",
        "isomer-rsch-write-v1",
    }
)

EXPECTED_V2_SKILLS = frozenset(
    {
        "isomer-rsch-analysis-v2",
        "isomer-rsch-baseline-v2",
        "isomer-rsch-decision-v2",
        "isomer-rsch-experiment-v2",
        "isomer-rsch-figure-polish-v2",
        "isomer-rsch-finalize-v2",
        "isomer-rsch-idea-v2",
        "isomer-rsch-nature-data-v2",
        "isomer-rsch-nature-figure-v2",
        "isomer-rsch-nature-paper2ppt-v2",
        "isomer-rsch-nature-polishing-v2",
        "isomer-rsch-optimize-v2",
        "isomer-rsch-paper-outline-v2",
        "isomer-rsch-paper-plot-v2",
        "isomer-rsch-rebuttal-v2",
        "isomer-rsch-review-v2",
        "isomer-rsch-science-v2",
        "isomer-rsch-scout-v2",
        "isomer-rsch-shared-v2",
        "isomer-rsch-workspace-mgr-v2",
        "isomer-rsch-write-v2",
    }
)

STALE_TERMS = {
    "Research Goal": "Research Topic",
    "Research Thread": "Research Inquiry",
    "Research Branch": "Research Inquiry Relationship",
    "Isomer Workspace": "Topic Workspace",
}

RESOLVED_TBD_IDS = frozenset(
    {
        "path-isomer-workspace",
        "path-topic-workspace",
        "path-workspace-runtime",
        "path-agent-workspace",
        "path-artifact-layout",
        "path-run-logs",
        "path-experiment-output",
        "path-analysis-output",
        "path-paper-layout",
        "path-figure-output",
        "api-artifact-record",
        "api-finding-query",
        "api-gate",
        "schema-decision-record",
        "schema-evidence-item",
        "schema-research-claim",
        "schema-gate",
        "schema-stage-cursor",
        "schema-agent-team-state",
        "policy-branching",
        "api-execution-command",
        "provider-literature-search",
        "schema-skill-binding",
        "policy-scheduler",
        "policy-baseline-waiver",
        "policy-cost-privacy-gate",
    }
)

COUPLING_PATTERNS = (
    ("DeepScientist source reference", re.compile(r"\bDeepScientist\b")),
    (
        "local absolute path",
        re.compile(
            r"(?<![A-Za-z0-9])/(?:data|home|Users|tmp|var/folders|mnt|scratch|workspace)/[^\s)`\"']+"
        ),
    ),
    ("source-analysis path", re.compile(r"\bsource-analysis(?:/|\b)")),
    ("archived OpenSpec change path", re.compile(r"\bopenspec/changes/archive/[^\s)`\"']+")),
    ("extern/orphan path", re.compile(r"\bextern/orphan(?:/|\b)")),
    ("DeepScientist runtime path", re.compile(r"(?:~|/[^\s]*)?\.deepscientist(?:/|\b)|\bDEEPSCIENTIST_HOME\b", re.I)),
    ("source runtime API", re.compile(r"\bartifact\.science(?:\(|\b)|\bhoumao-memo\b")),
    ("command wrapper", re.compile(r"`?(?:pixi run ds|ds-[a-z0-9-]+|deepscientist(?:\s|$)|deep-scientist)`?", re.I)),
    ("runner home", re.compile(r"\b(?:RUNNER_HOME|AGENT_HOME|~/\.runner|/runner/home)\b")),
    (
        "source runtime term",
        re.compile(
            r"\b(?:workspace_mode|continuation_policy|auto_continue|wait_for_user_or_resume|"
            r"continuation_anchor|continuation_reason)\b"
        ),
    ),
)

DEFAULT_ALLOW_ZONES = {
    "stale_terms_file_globs": (
        "PROVENANCE.md",
        "licenses/*.md",
        "deepscientist-migration-guide.md",
        "ds-analysis/**",
        "*/migrate/**",
        "*/org/**",
        "*/templates/**",
        "*/references/provenance.md",
        "*/references/source-term-mapping.md",
    ),
    "stale_terms_section_headings": (
        "Source-Term Mapping",
        "Source-Term Mappings",
    ),
    "runtime_coupling_file_globs": (
        "PROVENANCE.md",
        "licenses/*.md",
        "deepscientist-migration-guide.md",
        "ds-analysis/**",
        "*/migrate/**",
        "*/org/**",
        "*/templates/**",
        "*/references/provenance.md",
        "*/references/source-term-mapping.md",
        "*/references/deferred-resources.md",
        "*/references/deferred-venue-templates.md",
        "*/references/package-index-decision.md",
    ),
    "runtime_coupling_section_headings": (
        "Source-Term Mapping",
        "Source-Term Mappings",
        "Rejected Source Runtime Concepts",
        "Rejected Runtime Concepts",
        "Runtime Boundary",
        "Source Lineage",
    ),
    "resolved_id_file_globs": (
        "v1/isomer-rsch-shared-v1/references/tbd-surface-registry.md",
        "deepscientist-migration-guide.md",
        "ds-analysis/**",
        "*/migrate/**",
        "*/org/**",
        "*/templates/**",
    ),
    "resolved_id_section_headings": (
        "Research Recording Contracts",
        "Research Lifecycle State",
        "Research Execution and Extension Contract",
        "TBD Surface Registry",
        "Resolved Workspace Path Surfaces",
        "Resolved Research Recording Surfaces",
        "Resolved Research Lifecycle Surfaces",
        "Resolved Research Execution Extension Surfaces",
        "Resolved Surfaces",
        "Resolved Extension Surfaces",
    ),
    "v2_storage_binding_file_globs": (
        "v2/isomer-rsch-shared-v2/references/semantic-placeholders.md",
        "*/placeholder-bindings.md",
        "*/migrate/**",
        "*/org/**",
        "*/templates/**",
    ),
    "v2_storage_binding_section_headings": (
        "Source Lineage",
        "Placeholder Rule",
        "Storage Binding Status",
    ),
}

DEFAULT_FILE_ROLES = {
    "migration_file_globs": (
        "deepscientist-migration-guide.md",
        "*/migrate/**",
    ),
    "source_analysis_file_globs": (
        "ds-analysis/**",
        "*/org/analysis/**",
    ),
    "source_copy_file_globs": (
        "*/org/**",
    ),
    "passive_template_file_globs": (
        "*/templates/**",
    ),
}

NON_ACTIVE_ROLES = frozenset(
    {
        "canonical-registry",
        "deferred-resource",
        "license",
        "migration",
        "passive-template",
        "provenance",
        "semantic-placeholder-registry",
        "source-analysis",
        "source-copy",
        "source-term-mapping",
    }
)

LOCAL_REFERENCE_PREFIXES = ("references/", "assets/", "scripts/")

V2_STORAGE_BINDING_PATTERNS = (
    (
        "storage-bound research record",
        re.compile(r"\b(?:Artifact|Evidence Item|Gate|Decision Record|Provenance Record)s?\b|\bRun records?\b"),
    ),
    (
        "storage or runtime implementation binding",
        re.compile(
            r"\b(?:Topic Workspace records?|lifecycle rows?|database schemas?|database rows?|"
            r"storage labels?|concrete paths?|scheduler fields?)\b",
            re.I,
        ),
    ),
)

V2_STORAGE_BINDING_VERB_RE = re.compile(
    r"\b(?:create|emit|persist|register|store|submit|update|write)\b",
    re.I,
)

V2_SUPPORT_SECTION_HEADINGS = frozenset(
    {
        "Guidance",
        "Preferences",
        "Constraints",
        "Quality Gates",
        "Cross-Step Guidance",
        "Cross-Step Preferences",
        "Cross-Step Constraints",
        "Cross-Step Quality Gates",
    }
)
SUPPORT_INTRO_DISALLOWED_PREFIXES = tuple(f"{number}. " for number in range(1, 10)) + ("- ", "##", "###")
SENTENCE_END_RE = re.compile(r"[.!?](?:\s|$)")


@dataclass(frozen=True, order=True)
class Diagnostic:
    path: str
    line: int
    code: str
    message: str

    def render(self) -> str:
        return f"{self.path}:{self.line}: {self.code} {self.message}"


@dataclass(frozen=True)
class RegistryRow:
    resolution: str
    line: int


@dataclass(frozen=True)
class Document:
    path: Path
    rel_repo: str
    rel_target: str
    lines: tuple[str, ...]
    sections_by_line: tuple[tuple[str, ...], ...]
    roles: frozenset[str]


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


def normalize_heading(raw: str) -> str:
    return raw.strip().strip("#").strip()


def section_stack(lines: tuple[str, ...]) -> tuple[tuple[str, ...], ...]:
    active: list[tuple[int, str]] = []
    result: list[tuple[str, ...]] = []
    for line in lines:
        match = HEADING_RE.match(line)
        if match:
            level = len(match.group(1))
            heading = normalize_heading(match.group(2))
            active = [(item_level, item_heading) for item_level, item_heading in active if item_level < level]
            active.append((level, heading))
        result.append(tuple(heading for _, heading in active))
    return tuple(result)


def classify_document(
    rel_target: str,
    lines: tuple[str, ...],
    file_roles: dict[str, tuple[str, ...]],
) -> frozenset[str]:
    roles: set[str] = set()
    if rel_target.startswith("v1/"):
        roles.add("v1")
    if rel_target.startswith("v2/"):
        roles.add("v2")
    for role_key, role_name in (
        ("migration_file_globs", "migration"),
        ("source_analysis_file_globs", "source-analysis"),
        ("source_copy_file_globs", "source-copy"),
        ("passive_template_file_globs", "passive-template"),
    ):
        if any(fnmatch.fnmatch(rel_target, pattern) for pattern in file_roles.get(role_key, ())):
            roles.add(role_name)
    if rel_target == "PROVENANCE.md" or fnmatch.fnmatch(rel_target, "*/references/provenance.md"):
        roles.add("provenance")
    if rel_target.endswith("/PROVENANCE.md"):
        roles.add("provenance")
    if fnmatch.fnmatch(rel_target, "licenses/*.md"):
        roles.add("license")
    if fnmatch.fnmatch(rel_target, "*/references/deferred-*.md") or rel_target.endswith(
        "references/package-index-decision.md"
    ):
        roles.add("deferred-resource")
    if rel_target.endswith("references/source-term-mapping.md"):
        roles.add("source-term-mapping")
    if rel_target == "v1/isomer-rsch-shared-v1/references/tbd-surface-registry.md":
        roles.add("canonical-registry")
    if rel_target == "v2/isomer-rsch-shared-v2/references/semantic-placeholders.md":
        roles.add("semantic-placeholder-registry")
    if rel_target.endswith("/placeholder-bindings.md"):
        roles.add("placeholder-binding")
    if any(normalize_heading(line.removeprefix("##")) == "TBD Surface Registry" for line in lines if line.startswith("##")):
        roles.add("registry-mirror")
    if not (roles & NON_ACTIVE_ROLES):
        roles.add("active")
    return frozenset(roles)


def load_allow_zones(target: Path) -> dict[str, tuple[str, ...]]:
    config = {key: tuple(value) for key, value in DEFAULT_ALLOW_ZONES.items()}
    config_path = target / "validation.toml"
    if not config_path.exists():
        return config
    data = tomllib.loads(config_path.read_text(encoding="utf-8"))
    allow_zones = data.get("allow_zones", {})
    for key in config:
        value = allow_zones.get(key)
        if isinstance(value, list) and all(isinstance(item, str) for item in value):
            config[key] = tuple(value)
    return config


def load_file_roles(target: Path) -> dict[str, tuple[str, ...]]:
    config = {key: tuple(value) for key, value in DEFAULT_FILE_ROLES.items()}
    config_path = target / "validation.toml"
    if not config_path.exists():
        return config
    data = tomllib.loads(config_path.read_text(encoding="utf-8"))
    file_roles = data.get("file_roles", {})
    for key in config:
        value = file_roles.get(key)
        if isinstance(value, list) and all(isinstance(item, str) for item in value):
            config[key] = tuple(value)
    return config


def is_active_guidance(document: Document) -> bool:
    return "active" in document.roles


def allowed_by_rule(rule: str, document: Document, line_index: int, allow_zones: dict[str, tuple[str, ...]]) -> bool:
    file_globs = allow_zones.get(f"{rule}_file_globs", ())
    if any(fnmatch.fnmatch(document.rel_target, pattern) for pattern in file_globs):
        return True
    headings = {heading.casefold() for heading in allow_zones.get(f"{rule}_section_headings", ())}
    return any(heading.casefold() in headings for heading in document.sections_by_line[line_index])


def is_rejection_line(line: str) -> bool:
    lowered = line.casefold()
    return any(
        marker in lowered
        for marker in (
            "do not",
            "does not",
            "must not",
            "should not",
            "not import",
            "not define",
            "remain outside",
            "outside generic",
            "rejected",
        )
    )


def collect_documents(target: Path, repo_root: Path, file_roles: dict[str, tuple[str, ...]]) -> list[Document]:
    documents: list[Document] = []
    for path in sorted(target.rglob("*")):
        if path.suffix not in {".md", ".yaml", ".yml"} or not path.is_file():
            continue
        lines = read_lines(path)
        rel_target = relpath(path, target)
        documents.append(
            Document(
                path=path,
                rel_repo=relpath(path, repo_root),
                rel_target=rel_target,
                lines=lines,
                sections_by_line=section_stack(lines),
                roles=classify_document(rel_target, lines, file_roles),
            )
        )
    return documents


def add(
    diagnostics: list[Diagnostic],
    repo_root: Path,
    path: Path,
    line: int,
    code: str,
    message: str,
) -> None:
    diagnostics.append(Diagnostic(relpath(path, repo_root), max(line, 1), code, message))


def find_h2(lines: tuple[str, ...], title: str) -> int | None:
    expected = title.casefold()
    for line_number, line in enumerate(lines, start=1):
        match = HEADING_RE.match(line)
        if match and len(match.group(1)) == 2 and normalize_heading(match.group(2)).casefold() == expected:
            return line_number
    return None


def workflow_step_numbers(lines: tuple[str, ...], workflow_line: int) -> list[int]:
    numbers: list[int] = []
    for line in lines[workflow_line:]:
        match = HEADING_RE.match(line)
        if match and len(match.group(1)) <= 2:
            break
        number_match = re.match(r"^(\d+)\.\s+", line)
        if number_match:
            numbers.append(int(number_match.group(1)))
    return numbers


def validate_skill_layout(skill_dir: Path, repo_root: Path, diagnostics: list[Diagnostic], generation: str | None) -> None:
    skill_name = skill_dir.name
    if not SKILL_NAME_RE.match(skill_name):
        add(diagnostics, repo_root, skill_dir, 1, "RPS007", f"skill folder '{skill_name}' must match isomer-rsch-*")
    if generation in {"v1", "v2"} and not skill_name.endswith(f"-{generation}"):
        add(
            diagnostics,
            repo_root,
            skill_dir,
            1,
            "RPS007",
            f"skill folder '{skill_name}' must end with -{generation}",
        )

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        add(diagnostics, repo_root, skill_dir, 1, "RPS007", "skill folder is missing SKILL.md")
        return

    lines = read_lines(skill_md)
    frontmatter = parse_frontmatter(lines)
    if frontmatter.get("name") != skill_name:
        add(diagnostics, repo_root, skill_md, 2, "RPS007", "frontmatter name must match the skill folder")
    if not frontmatter.get("description"):
        add(diagnostics, repo_root, skill_md, 3, "RPS007", "frontmatter description is required")

    workflow_line = find_h2(lines, "Workflow")
    if workflow_line is None:
        add(diagnostics, repo_root, skill_md, 1, "RPS007", "SKILL.md must contain ## Workflow")
    else:
        if workflow_line > 40:
            add(diagnostics, repo_root, skill_md, workflow_line, "RPS007", "## Workflow must appear near the top")
        numbers = workflow_step_numbers(lines, workflow_line)
        if len(numbers) < 2 or numbers[0] != 1:
            add(diagnostics, repo_root, skill_md, workflow_line, "RPS007", "## Workflow must contain numbered steps")

    if find_h2(lines, "Reference Routing") is None:
        add(diagnostics, repo_root, skill_md, 1, "RPS007", "SKILL.md must contain ## Reference Routing")

    if not any("does not map cleanly" in line for line in lines):
        add(diagnostics, repo_root, skill_md, 1, "RPS007", "SKILL.md must include fallback guidance")


def validate_manifest(skill_dir: Path, repo_root: Path, diagnostics: list[Diagnostic]) -> None:
    skill_name = skill_dir.name
    manifest = skill_dir / "agents" / "openai.yaml"
    if not manifest.exists():
        add(diagnostics, repo_root, skill_dir, 1, "RPS006", "agents/openai.yaml is required")
        return
    fields = parse_interface_fields(read_lines(manifest))
    display_name = fields.get("display_name")
    if display_name is None:
        add(diagnostics, repo_root, manifest, 1, "RPS006", "interface.display_name is required")
    elif display_name[0] != skill_name:
        add(
            diagnostics,
            repo_root,
            manifest,
            display_name[1],
            "RPS006",
            f"interface.display_name must be '{skill_name}'",
        )

    default_prompt = fields.get("default_prompt")
    if default_prompt is None:
        add(diagnostics, repo_root, manifest, 1, "RPS006", "interface.default_prompt is required")
    elif f"${skill_name}" not in default_prompt[0]:
        add(
            diagnostics,
            repo_root,
            manifest,
            default_prompt[1],
            "RPS006",
            f"interface.default_prompt must invoke ${skill_name}",
        )


def clean_reference(raw: str) -> str | None:
    value = raw.strip().strip("<>").strip()
    if "://" in value or value.startswith("#"):
        return None
    value = value.split("#", 1)[0].strip()
    value = value.strip(".,;:)")
    if any(value.startswith(prefix) for prefix in LOCAL_REFERENCE_PREFIXES):
        return value
    return None


def is_placeholder_reference(reference: str) -> bool:
    return bool(PLACEHOLDER_PATH_SEGMENT_RE.search(reference))


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


def validate_local_references(skill_dir: Path, repo_root: Path, diagnostics: list[Diagnostic]) -> None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return
    skill_root = skill_dir.resolve()
    for line_number, line in enumerate(read_lines(skill_md), start=1):
        for reference in local_references_from_line(line):
            if is_placeholder_reference(reference):
                continue
            target = (skill_dir / reference).resolve()
            if not target.is_relative_to(skill_root) or not target.exists():
                add(
                    diagnostics,
                    repo_root,
                    skill_md,
                    line_number,
                    "RPS005",
                    f"local reference '{reference}' does not exist inside {skill_dir.name}",
                )


def parse_registry_rows(lines: tuple[str, ...]) -> dict[str, RegistryRow]:
    rows: dict[str, RegistryRow] = {}
    for line_number, line in enumerate(lines, start=1):
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        row_id = cells[0]
        if row_id.casefold() in {"former id", "id", "---"} or set(row_id) <= {"-"}:
            continue
        if REGISTRY_ROW_ID_RE.match(row_id):
            rows[row_id] = RegistryRow(cells[1], line_number)
    return rows


def parse_semantic_placeholder_ids(lines: tuple[str, ...]) -> dict[str, int]:
    ids: dict[str, int] = {}
    for line_number, line in enumerate(lines, start=1):
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        raw_id = cells[0].strip("`")
        if raw_id.casefold() in {"id", "---"} or set(raw_id) <= {"-"}:
            continue
        if SEMANTIC_PLACEHOLDER_ID_RE.match(raw_id):
            ids[raw_id] = line_number
    return ids


def parse_migration_placeholder_ids(lines: tuple[str, ...]) -> dict[str, int]:
    ids: dict[str, int] = {}
    for line_number, line in enumerate(lines, start=1):
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells:
            continue
        raw_id = cells[0].strip("`")
        if raw_id.casefold() in {"placeholder", "---"} or set(raw_id) <= {"-"}:
            continue
        match = MIGRATION_PLACEHOLDER_CELL_RE.match(raw_id)
        if match:
            ids[match.group(1)] = line_number
    return ids


def parse_placeholder_binding_ids(lines: tuple[str, ...]) -> dict[str, int]:
    ids: dict[str, int] = {}
    for line_number, line in enumerate(lines, start=1):
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells:
            continue
        raw_id = cells[0].strip("`")
        if raw_id.casefold() in {"placeholder", "---"} or set(raw_id) <= {"-"}:
            continue
        match = MIGRATION_PLACEHOLDER_CELL_RE.match(raw_id)
        if match:
            ids[match.group(1)] = line_number
    return ids


def normalize_resolution(text: str) -> str:
    text = re.sub(r"[`*_]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip().casefold()


def validate_registry_mirrors(
    documents: list[Document],
    canonical_rows: dict[str, RegistryRow],
    repo_root: Path,
    diagnostics: list[Diagnostic],
) -> None:
    expected = {row_id: row for row_id, row in canonical_rows.items() if row_id in RESOLVED_TBD_IDS}
    canonical_path = "v1/isomer-rsch-shared-v1/references/tbd-surface-registry.md"
    for document in documents:
        if document.rel_target == canonical_path or "registry-mirror" not in document.roles:
            continue
        rows = parse_registry_rows(document.lines)
        heading_line = find_h2(document.lines, "TBD Surface Registry") or 1
        missing = sorted(set(expected) - set(rows))
        extra = sorted(set(rows) - set(expected))
        for row_id in missing:
            add(
                diagnostics,
                repo_root,
                document.path,
                heading_line,
                "RPS008",
                f"local TBD registry mirror is missing resolved id '{row_id}'",
            )
        for row_id in extra:
            add(
                diagnostics,
                repo_root,
                document.path,
                rows[row_id].line,
                "RPS008",
                f"local TBD registry mirror has extra id '{row_id}'",
            )
        for row_id in sorted(set(expected) & set(rows)):
            if normalize_resolution(expected[row_id].resolution) != normalize_resolution(rows[row_id].resolution):
                add(
                    diagnostics,
                    repo_root,
                    document.path,
                    rows[row_id].line,
                    "RPS008",
                    f"local TBD registry mirror changes resolution text for '{row_id}'",
                )


def validate_tbd_placeholders(
    document: Document,
    repo_root: Path,
    diagnostics: list[Diagnostic],
    registered_ids: set[str],
) -> None:
    if not is_active_guidance(document):
        return
    for line_number, line in enumerate(document.lines, start=1):
        for match in TBD_PLACEHOLDER_RE.finditer(line):
            tbd_id = match.group(1)
            if tbd_id in RESOLVED_TBD_IDS:
                add(
                    diagnostics,
                    repo_root,
                    document.path,
                    line_number,
                    "RPS002",
                    f"resolved TBD id '{tbd_id}' must not be emitted as a placeholder",
                )
            elif tbd_id not in registered_ids:
                add(
                    diagnostics,
                    repo_root,
                    document.path,
                    line_number,
                    "RPS003",
                    f"TBD surface id '{tbd_id}' is not registered in the shared registry",
                )


def validate_rsch_object_placeholders(
    document: Document,
    repo_root: Path,
    diagnostics: list[Diagnostic],
    registered_ids: set[str],
) -> None:
    if "v2" not in document.roles or not is_active_guidance(document):
        return
    for line_number, line in enumerate(document.lines, start=1):
        for match in RSCH_OBJECT_PLACEHOLDER_RE.finditer(line):
            placeholder_id = match.group(1)
            if placeholder_id not in registered_ids:
                add(
                    diagnostics,
                    repo_root,
                    document.path,
                    line_number,
                    "RPS009",
                    f"research object placeholder '{placeholder_id}' is not registered in the v2 semantic-placeholder registry",
                )


def validate_migration_placeholders(
    document: Document,
    repo_root: Path,
    diagnostics: list[Diagnostic],
    registered_by_skill: dict[str, set[str]],
) -> None:
    if not is_active_guidance(document):
        return
    if "placeholder-binding" in document.roles:
        return
    parts = document.rel_target.split("/")
    if len(parts) < 3 or parts[0] not in {"v1", "v2"}:
        return
    skill_rel = "/".join(parts[:2])
    registered_ids = registered_by_skill.get(skill_rel, set())
    for line_number, line in enumerate(document.lines, start=1):
        for match in MIGRATION_PLACEHOLDER_RE.finditer(line):
            placeholder_id = match.group(1)
            if placeholder_id not in registered_ids:
                add(
                    diagnostics,
                    repo_root,
                    document.path,
                    line_number,
                    "RPS009",
                    f"migration placeholder '{placeholder_id}' is not registered in migrate/placeholders.md",
                )


def validate_v2_placeholder_bindings(
    skill_dirs: list[tuple[Path, str]],
    repo_root: Path,
    diagnostics: list[Diagnostic],
) -> None:
    for skill_dir, generation in skill_dirs:
        if generation != "v2":
            continue
        placeholder_path = skill_dir / "migrate" / "placeholders.md"
        if not placeholder_path.exists():
            continue
        expected = parse_migration_placeholder_ids(read_lines(placeholder_path))
        binding_path = skill_dir / "placeholder-bindings.md"
        if not binding_path.exists():
            add(
                diagnostics,
                repo_root,
                skill_dir,
                1,
                "RPS012",
                "v2 skill with migrate/placeholders.md must include placeholder-bindings.md",
            )
            continue
        actual = parse_placeholder_binding_ids(read_lines(binding_path))
        heading_line = find_h2(read_lines(binding_path), "Placeholder Bindings") or 1
        for placeholder_id in sorted(set(expected) - set(actual)):
            add(
                diagnostics,
                repo_root,
                binding_path,
                heading_line,
                "RPS012",
                f"placeholder-bindings.md is missing migration placeholder '<{placeholder_id}>'",
            )
        for placeholder_id in sorted(set(actual) - set(expected)):
            add(
                diagnostics,
                repo_root,
                binding_path,
                actual[placeholder_id],
                "RPS012",
                f"placeholder-bindings.md has extra migration placeholder '<{placeholder_id}>'",
            )


def validate_v2_storage_binding(
    document: Document,
    repo_root: Path,
    diagnostics: list[Diagnostic],
    allow_zones: dict[str, tuple[str, ...]],
) -> None:
    if "v2" not in document.roles or not is_active_guidance(document):
        return
    for line_index, line in enumerate(document.lines):
        if allowed_by_rule("v2_storage_binding", document, line_index, allow_zones):
            continue
        lowered = line.casefold()
        if (
            is_rejection_line(line)
            or "not storage-bound" in lowered
            or "storage binding is deferred" in lowered
            or "source-compatible" in lowered
            or "placeholder" in lowered
        ):
            continue
        for label, pattern in V2_STORAGE_BINDING_PATTERNS:
            if pattern.search(line):
                if label == "storage-bound research record" and not V2_STORAGE_BINDING_VERB_RE.search(line):
                    continue
                add(
                    diagnostics,
                    repo_root,
                    document.path,
                    line_index + 1,
                    "RPS010",
                    f"active v2 guidance contains {label}",
                )


def validate_v2_support_section_intros(
    document: Document,
    repo_root: Path,
    diagnostics: list[Diagnostic],
) -> None:
    if "v2" not in document.roles or not is_active_guidance(document):
        return
    for line_index, line in enumerate(document.lines):
        match = HEADING_RE.match(line)
        if not match:
            continue
        heading = normalize_heading(match.group(2))
        if heading not in V2_SUPPORT_SECTION_HEADINGS:
            continue
        content_index = line_index + 1
        while content_index < len(document.lines) and not document.lines[content_index].strip():
            content_index += 1
        if content_index >= len(document.lines):
            add(
                diagnostics,
                repo_root,
                document.path,
                line_index + 1,
                "RPS011",
                f"active v2 {heading} section must start with a one-to-three-sentence interpretive paragraph",
            )
            continue
        first_content = document.lines[content_index].strip()
        if first_content == "None" or first_content.startswith(SUPPORT_INTRO_DISALLOWED_PREFIXES):
            add(
                diagnostics,
                repo_root,
                document.path,
                content_index + 1,
                "RPS011",
                f"active v2 {heading} section must start with a one-to-three-sentence interpretive paragraph",
            )
            continue
        paragraph_lines: list[str] = []
        paragraph_end = content_index
        while paragraph_end < len(document.lines):
            current = document.lines[paragraph_end].strip()
            if not current or current == "None" or current.startswith(SUPPORT_INTRO_DISALLOWED_PREFIXES):
                break
            paragraph_lines.append(current)
            paragraph_end += 1
        sentence_count = len(SENTENCE_END_RE.findall(" ".join(paragraph_lines)))
        if sentence_count < 1 or sentence_count > 3:
            add(
                diagnostics,
                repo_root,
                document.path,
                content_index + 1,
                "RPS011",
                f"active v2 {heading} section intro must be one to three sentences",
            )
        if paragraph_end < len(document.lines):
            next_line = document.lines[paragraph_end].strip()
            if next_line and next_line.startswith(SUPPORT_INTRO_DISALLOWED_PREFIXES):
                add(
                    diagnostics,
                    repo_root,
                    document.path,
                    paragraph_end + 1,
                    "RPS011",
                    f"active v2 {heading} section intro must be separated from following content by a blank line",
                )


def validate_resolved_id_text(
    document: Document,
    repo_root: Path,
    diagnostics: list[Diagnostic],
    allow_zones: dict[str, tuple[str, ...]],
) -> None:
    if not is_active_guidance(document):
        return
    for line_index, line in enumerate(document.lines):
        if allowed_by_rule("resolved_id", document, line_index, allow_zones):
            continue
        for row_id in sorted(RESOLVED_TBD_IDS):
            if re.search(rf"(?<![A-Za-z0-9-]){re.escape(row_id)}(?![A-Za-z0-9-])", line):
                add(
                    diagnostics,
                    repo_root,
                    document.path,
                    line_index + 1,
                    "RPS002",
                    f"resolved TBD id '{row_id}' appears in active guidance",
                )


def validate_stale_terms(
    document: Document,
    repo_root: Path,
    diagnostics: list[Diagnostic],
    allow_zones: dict[str, tuple[str, ...]],
) -> None:
    if not is_active_guidance(document):
        return
    for line_index, line in enumerate(document.lines):
        if allowed_by_rule("stale_terms", document, line_index, allow_zones):
            continue
        for term, replacement in STALE_TERMS.items():
            if term in line:
                add(
                    diagnostics,
                    repo_root,
                    document.path,
                    line_index + 1,
                    "RPS001",
                    f"stale term '{term}' should use '{replacement}' in active guidance",
                )


def validate_coupling_patterns(
    document: Document,
    repo_root: Path,
    diagnostics: list[Diagnostic],
    allow_zones: dict[str, tuple[str, ...]],
) -> None:
    if not is_active_guidance(document):
        return
    for line_index, line in enumerate(document.lines):
        if allowed_by_rule("runtime_coupling", document, line_index, allow_zones):
            continue
        for label, pattern in COUPLING_PATTERNS:
            if pattern.search(line):
                if is_rejection_line(line):
                    continue
                add(
                    diagnostics,
                    repo_root,
                    document.path,
                    line_index + 1,
                    "RPS004",
                    f"active guidance contains {label}",
                )


def validate_global_isomer_cli_invocation(target: Path, repo_root: Path, diagnostics: list[Diagnostic]) -> None:
    for path in sorted(candidate for candidate in target.rglob("*") if candidate.is_file() and candidate.suffix in ACTIVE_REF_SUFFIXES):
        for line_number, line in enumerate(read_lines(path), start=1):
            if FORBIDDEN_REPO_LOCAL_ISOMER_CLI in line:
                add(
                    diagnostics,
                    repo_root,
                    path,
                    line_number,
                    "RPS013",
                    "research skills must call global isomer-cli directly instead of 'pixi run isomer-cli'",
                )


def validate_skillset(target: Path, repo_root: Path | None = None) -> list[Diagnostic]:
    target = target.resolve()
    repo_root = (repo_root or find_repo_root(target)).resolve()
    diagnostics: list[Diagnostic] = []
    if not target.exists():
        diagnostics.append(Diagnostic(relpath(target, repo_root), 1, "RPS000", "skillset path does not exist"))
        return diagnostics

    allow_zones = load_allow_zones(target)
    file_roles = load_file_roles(target)
    flat_skill_dirs = sorted(path for path in target.iterdir() if path.is_dir() and path.name.startswith("isomer-rsch-"))
    for skill_dir in flat_skill_dirs:
        add(
            diagnostics,
            repo_root,
            skill_dir,
            1,
            "RPS007",
            "active flat root research skill folders are not allowed; use v1/ or v2/",
        )

    skill_dirs: list[tuple[Path, str]] = []
    for generation, expected in (("v1", EXPECTED_V1_SKILLS), ("v2", EXPECTED_V2_SKILLS)):
        generation_root = target / generation
        if not generation_root.exists():
            add(diagnostics, repo_root, generation_root, 1, "RPS007", f"{generation}/ generation directory is missing")
            continue
        generation_skill_dirs = sorted(
            path for path in generation_root.iterdir() if path.is_dir() and path.name.startswith("isomer-rsch-")
        )
        actual_names = {path.name for path in generation_skill_dirs}
        for missing in sorted(expected - actual_names):
            add(diagnostics, repo_root, generation_root / missing, 1, "RPS007", f"expected {generation} skill is missing")
        for skill_dir in generation_skill_dirs:
            skill_dirs.append((skill_dir, generation))

    if not skill_dirs:
        add(diagnostics, repo_root, target, 1, "RPS007", "no generationed isomer-rsch-* skill folders were found")
    for skill_dir, generation in skill_dirs:
        validate_skill_layout(skill_dir, repo_root, diagnostics, generation)
        validate_manifest(skill_dir, repo_root, diagnostics)
        validate_local_references(skill_dir, repo_root, diagnostics)

    documents = collect_documents(target, repo_root, file_roles)
    registry_path = target / "v1" / "isomer-rsch-shared-v1" / "references" / "tbd-surface-registry.md"
    if registry_path.exists():
        canonical_rows = parse_registry_rows(read_lines(registry_path))
    else:
        canonical_rows = {}
        add(diagnostics, repo_root, registry_path, 1, "RPS003", "canonical v1 shared TBD registry is missing")
    registered_ids = set(canonical_rows)

    semantic_registry_path = target / "v2" / "isomer-rsch-shared-v2" / "references" / "semantic-placeholders.md"
    if semantic_registry_path.exists():
        semantic_placeholder_ids = set(parse_semantic_placeholder_ids(read_lines(semantic_registry_path)))
    else:
        semantic_placeholder_ids = set()
        add(diagnostics, repo_root, semantic_registry_path, 1, "RPS009", "v2 semantic-placeholder registry is missing")

    migration_placeholder_ids_by_skill: dict[str, set[str]] = {}
    for skill_dir, _generation in skill_dirs:
        rel_skill_dir = relpath(skill_dir, target)
        placeholder_path = skill_dir / "migrate" / "placeholders.md"
        if placeholder_path.exists():
            migration_placeholder_ids_by_skill[rel_skill_dir] = set(
                parse_migration_placeholder_ids(read_lines(placeholder_path))
            )

    for document in documents:
        validate_tbd_placeholders(document, repo_root, diagnostics, registered_ids)
        validate_rsch_object_placeholders(document, repo_root, diagnostics, semantic_placeholder_ids)
        validate_migration_placeholders(document, repo_root, diagnostics, migration_placeholder_ids_by_skill)
        validate_resolved_id_text(document, repo_root, diagnostics, allow_zones)
        validate_stale_terms(document, repo_root, diagnostics, allow_zones)
        validate_coupling_patterns(document, repo_root, diagnostics, allow_zones)
        validate_v2_storage_binding(document, repo_root, diagnostics, allow_zones)
        validate_v2_support_section_intros(document, repo_root, diagnostics)
    validate_v2_placeholder_bindings(skill_dirs, repo_root, diagnostics)
    validate_registry_mirrors(documents, canonical_rows, repo_root, diagnostics)
    validate_global_isomer_cli_invocation(target, repo_root, diagnostics)
    return sorted(set(diagnostics))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate the research-paradigm skillset.")
    parser.add_argument(
        "skillset",
        nargs="?",
        default="skillset/research-paradigm",
        help="Path to the research-paradigm skillset root.",
    )
    parser.add_argument("--repo-root", type=Path, default=None, help="Repository root for diagnostic paths.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    repo_root = args.repo_root.resolve() if args.repo_root else find_repo_root(Path.cwd())
    target = Path(args.skillset)
    if not target.is_absolute():
        target = repo_root / target
    diagnostics = validate_skillset(target, repo_root)
    for diagnostic in diagnostics:
        print(diagnostic.render())
    return 1 if diagnostics else 0


if __name__ == "__main__":
    sys.exit(main())
