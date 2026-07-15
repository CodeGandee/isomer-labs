#!/usr/bin/env python3
"""Validate the research-paradigm skill bundle."""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sys
import tomllib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from packaging.version import InvalidVersion, Version
import yaml

from isomer_labs.core.artifact_identity import (
    ArtifactIdentityError,
    packaged_extension_ids,
    parse_artifact_identity,
)
from isomer_labs.kaoju.contracts import (
    load_binding_registry,
    load_contract,
    load_semantic_registry,
    resource_coverage_diagnostics,
)


@dataclass(frozen=True)
class FamilyConfig:
    key: str
    root_name: str
    name_pattern: re.Pattern[str]
    name_shape: str
    expected_skills: frozenset[str]
    max_workflow_line: int
    required: bool
    semantic_registry: str | None = None
    semantic_id_pattern: re.Pattern[str] | None = None
    binding_filename: str | None = None
    profile_namespace: str | None = None
    binding_owners: frozenset[str] = frozenset()
    required_binding_fields: tuple[str, ...] = ()


SKILL_NAME_RE = re.compile(r"^isomer-deepsci-[a-z0-9]+(?:-[a-z0-9]+)*$")
KAOJU_SKILL_NAME_RE = re.compile(r"^isomer-kaoju-[a-z0-9]+(?:-[a-z0-9]+)*$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
FRONTMATTER_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*?)\s*$")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
CODE_SPAN_RE = re.compile(r"`([^`]+)`")
TBD_PLACEHOLDER_RE = re.compile(r"\[\[tbd-surface:([a-z0-9][a-z0-9-]*)\]\]")
RSCH_OBJECT_PLACEHOLDER_RE = re.compile(r"\[\[rsch-object:([^\]]+)\]\]")
MIGRATION_PLACEHOLDER_RE = re.compile(r"(?<![A-Z0-9:-])(DEEPSCI:[A-Z0-9]+(?:-[A-Z0-9]+)*)(?![A-Z0-9:-])")
MIGRATION_PLACEHOLDER_CELL_RE = re.compile(r"^(DEEPSCI:[A-Z0-9]+(?:-[A-Z0-9]+)*)$")
PLACEHOLDER_PATH_SEGMENT_RE = re.compile(r"<[A-Za-z0-9_-]+>")
REGISTRY_ROW_ID_RE = re.compile(r"^(?:path|api|schema|policy|provider)-[a-z0-9-]+$")
SEMANTIC_PLACEHOLDER_ID_RE = re.compile(r"^DEEPSCI:[A-Z0-9]+(?:-[A-Z0-9]+)*$")
CANONICAL_IDENTITY_TOKEN_RE = re.compile(r"(?<![A-Za-z0-9-])([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*:[A-Z0-9]+(?:-[A-Z0-9]+)*)(?![A-Za-z0-9-])")
NONCANONICAL_EXTENSION_ID_RE = re.compile(r"(?<![A-Za-z0-9-])((?:deepsci|kaoju|DeepSci|Kaoju):[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*)(?![A-Za-z0-9-])")
WRAPPED_IDENTITY_RE = re.compile(r"<([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*:[A-Z0-9]+(?:-[A-Z0-9]+)*)>")
LEGACY_ANGLE_ARTIFACT_RE = re.compile(r"<([A-Z][A-Z0-9]+(?:_[A-Z0-9]+)+)>")
DOUBLE_BRACKET_ARTIFACT_RE = re.compile(r"\[\[(?:rsch-object|artifact|placeholder):[^\]]+\]\]", re.I)
FORBIDDEN_REPO_LOCAL_ISOMER_CLI = "pixi run isomer-cli"
ACTIVE_REF_SUFFIXES = {".md", ".toml", ".yaml", ".yml", ".py", ".json"}
MAX_DEEPSCI_WORKFLOW_LINE = 45

EXPECTED_DEEPSCI_SKILLS = frozenset(
    {
        "isomer-deepsci-analysis",
        "isomer-deepsci-baseline",
        "isomer-deepsci-decision",
        "isomer-deepsci-experiment",
        "isomer-deepsci-figure-polish",
        "isomer-deepsci-finalize",
        "isomer-deepsci-idea",
        "isomer-deepsci-nature-data",
        "isomer-deepsci-nature-figure",
        "isomer-deepsci-nature-paper2ppt",
        "isomer-deepsci-nature-polishing",
        "isomer-deepsci-optimize",
        "isomer-deepsci-paper-outline",
        "isomer-deepsci-paper-plot",
        "isomer-deepsci-rebuttal",
        "isomer-deepsci-review",
        "isomer-deepsci-science",
        "isomer-deepsci-scout",
        "isomer-deepsci-shared",
        "isomer-deepsci-workspace-mgr",
        "isomer-deepsci-write",
    }
)

EXPECTED_KAOJU_SKILLS = frozenset(
    {
        "isomer-kaoju-acquire",
        "isomer-kaoju-audit",
        "isomer-kaoju-compare",
        "isomer-kaoju-discover",
        "isomer-kaoju-examine",
        "isomer-kaoju-frame",
        "isomer-kaoju-pipeline",
        "isomer-kaoju-reproduce",
        "isomer-kaoju-shared",
        "isomer-kaoju-synthesize",
        "isomer-kaoju-trial",
        "isomer-kaoju-workspace-mgr",
        "isomer-kaoju-write",
        "isomer-kaoju-export",
    }
)

FAMILY_CONFIGS = (
    FamilyConfig(
        key="deepsci",
        root_name="deepsci",
        name_pattern=SKILL_NAME_RE,
        name_shape="isomer-deepsci-*",
        expected_skills=EXPECTED_DEEPSCI_SKILLS,
        max_workflow_line=MAX_DEEPSCI_WORKFLOW_LINE,
        required=True,
    ),
    FamilyConfig(
        key="kaoju",
        root_name="kaoju",
        name_pattern=KAOJU_SKILL_NAME_RE,
        name_shape="isomer-kaoju-*",
        expected_skills=EXPECTED_KAOJU_SKILLS,
        max_workflow_line=40,
        required=False,
        semantic_registry="isomer-kaoju-shared/references/artifact-semantics.md",
        semantic_id_pattern=re.compile(r"^KAOJU:[A-Z0-9]+(?:-[A-Z0-9]+)*$"),
        binding_filename="artifact-bindings.md",
        profile_namespace="isomer:research/record-format/profile/kaoju/",
        binding_owners=frozenset(
            {
                "isomer-kaoju-acquire",
                "isomer-kaoju-audit",
                "isomer-kaoju-compare",
                "isomer-kaoju-discover",
                "isomer-kaoju-examine",
                "isomer-kaoju-frame",
                "isomer-kaoju-pipeline",
                "isomer-kaoju-reproduce",
                "isomer-kaoju-synthesize",
                "isomer-kaoju-workspace-mgr",
                "isomer-kaoju-write",
            }
        ),
        required_binding_fields=(
            "Semantic id",
            "Storage item",
            "Record kind",
            "Semantic label",
            "Neutral profile",
            "Producer",
            "Consumers",
            "Payload role",
            "Lineage policy",
            "Revision policy",
            "Query metadata",
        ),
    ),
)

EXPECTED_KAOJU_COMMANDS = frozenset(
    {
        "audit-survey-pass",
        "build-paper-pdf",
        "build-reading-list",
        "choose-directions",
        "comparative-pass",
        "create-paper-template",
        "curated-intake-pass",
        "direction-expansion-pass",
        "draft-paper",
        "export-survey-wiki",
        "ingest-reading-item",
        "ingest-source-code",
        "landscape-pass",
        "manage-dataset",
        "manage-paper-template",
        "manage-survey",
        "method-trial-pass",
        "paper-pass",
        "prepare-code-run",
        "run-code-trial",
        "theory-comparison-pass",
    }
)

EXPECTED_KAOJU_PROCEDURES = frozenset(
    {
        "audit-survey-pass",
        "comparative-pass",
        "create-paper-template",
        "curated-intake-pass",
        "direction-expansion-pass",
        "landscape-pass",
        "method-trial-pass",
        "paper-pass",
        "theory-comparison-pass",
    }
)

FORBIDDEN_KAOJU_PROCEDURES = frozenset(
    {
        "environment-repair",
        "full-kaoju",
        "list-passes",
        "refresh",
        "repository-refresh",
        "reproduction",
        "resume",
        "source-audit",
    }
)

EXPECTED_KAOJU_SHARED_REFERENCES = frozenset(
    {
        "evidence-contract.md",
        "artifact-recording.md",
        "artifact-semantics.md",
        "external-owner-routing.md",
        "interaction-and-gates.md",
        "lineage.md",
        "source-identity.md",
        "survey-artifacts.md",
        "terminal-report.md",
    }
)

STALE_TERMS = {
    "isomer-rsch-": "isomer-deepsci-",
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
    "deepsci_storage_binding_file_globs": (
        "deepsci/isomer-deepsci-shared/references/semantic-placeholders.md",
        "*/placeholder-bindings.md",
        "*/migrate/**",
        "*/org/**",
        "*/templates/**",
    ),
    "deepsci_storage_binding_section_headings": (
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

LOCAL_REFERENCE_PREFIXES = ("commands/", "references/", "assets/", "scripts/")

KAOJU_FORBIDDEN_ACTIVE_PATTERNS = (
    ("provider-specific runtime binding", re.compile(r"\b(?:Tavily|Semantic Scholar|Crossref|GitHub|GitLab|Hugging Face|arXiv API)\b", re.I)),
    ("feature-design runtime dependency", re.compile(r"\bcontext/features/[^\s)`\"']+")),
    ("OpenSpec runtime dependency", re.compile(r"\bopenspec/changes/[^\s)`\"']+")),
    ("retired research skill namespace", re.compile(r"\bisomer-(?:ext|rsch)-[a-z0-9-]+\b")),
)

DEEPSCI_STORAGE_BINDING_PATTERNS = (
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

DEEPSCI_STORAGE_BINDING_VERB_RE = re.compile(
    r"\b(?:create|emit|persist|register|store|submit|update|write)\b",
    re.I,
)

DEEPSCI_SUPPORT_SECTION_HEADINGS = frozenset(
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
DEEPSCI_FORMAT_PROFILE_RE = re.compile(r"^isomer:deepsci/record-format/profile/[A-Za-z0-9._/-]+/v2$")
DEEPSCI_FORMAT_PROFILE_V1_TEXT_RE = re.compile(r"isomer:deepsci/record-format/profile/[A-Za-z0-9._/-]+/v1")
DEEPSCI_PLAIN_OUTPUT_TERMS = (
    "json payload staging",
    "markdown draft",
    "csvs",
    "figures",
    "paper build",
    "previews",
    "reports",
    "local summar",
    "deck asset",
    "plain generated file",
)
DEEPSCI_WORKER_OUTPUT_REQUIRED_TERMS = (
    "project outputs policy",
    "operation-specific",
    "commit_after_operation",
)
DEEPSCI_SHARED_WORKER_OUTPUT_REQUIRED_TERMS = (
    "## Worker Output Policy",
    "project outputs policy",
    "operation-specific child set",
    ".gitignore",
    "commit_after_operation",
)
DEEPSCI_LATEST_CONTEXT_REQUIRED_TERMS = (
    "latest context preflight",
    "latest-context-snapshot",
)
DEEPSCI_LATEST_CONTEXT_FRESHNESS_TERMS = (
    "prompt memory",
    "chat memory",
    "prior prose",
    "remembered research state",
    "older rendered records",
    "worker-local files",
)
DEEPSCI_CALLBACK_ANTI_PATTERN = "User Skill Callback reminder"
DEEPSCI_CALLBACK_REQUIRED_TERMS = (
    "empty callback results continue normally",
    "conflicts must be reported",
)


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
    if rel_target.startswith("deepsci/"):
        roles.add("deepsci")
    if rel_target.startswith("kaoju/"):
        roles.add("kaoju")
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
    if rel_target == "deepsci/isomer-deepsci-shared/references/semantic-placeholders.md":
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


def workflow_numbered_steps(lines: tuple[str, ...], workflow_line: int) -> list[tuple[int, int, str]]:
    steps: list[tuple[int, int, str]] = []
    for line_number, line in enumerate(lines[workflow_line:], start=workflow_line + 1):
        match = HEADING_RE.match(line)
        if match and len(match.group(1)) <= 2:
            break
        number_match = re.match(r"^(\d+)\.\s+", line)
        if number_match:
            steps.append((line_number, int(number_match.group(1)), line))
    return steps


def validate_skill_layout(
    skill_dir: Path,
    repo_root: Path,
    diagnostics: list[Diagnostic],
    family: FamilyConfig,
) -> None:
    skill_name = skill_dir.name
    if not family.name_pattern.match(skill_name):
        add(diagnostics, repo_root, skill_dir, 1, "RPS007", f"skill folder '{skill_name}' must match {family.name_shape}")
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
    if family.key == "kaoju":
        if set(frontmatter) != {"name", "description"}:
            add(diagnostics, repo_root, skill_md, 1, "RPS018", "Kaoju frontmatter must contain only name and description")
        if not frontmatter.get("description", "").startswith("Use when"):
            add(diagnostics, repo_root, skill_md, 3, "RPS018", "Kaoju frontmatter description must start with 'Use when'")

    workflow_line = find_h2(lines, "Workflow")
    workflow_steps: list[tuple[int, int, str]] = []
    if workflow_line is None:
        add(diagnostics, repo_root, skill_md, 1, "RPS007", "SKILL.md must contain ## Workflow")
    else:
        if workflow_line > family.max_workflow_line:
            add(diagnostics, repo_root, skill_md, workflow_line, "RPS007", "## Workflow must appear near the top")
        workflow_steps = workflow_numbered_steps(lines, workflow_line)
        numbers = [number for _, number, _ in workflow_steps]
        if len(numbers) < 2 or numbers[0] != 1:
            add(diagnostics, repo_root, skill_md, workflow_line, "RPS007", "## Workflow must contain numbered steps")

    if find_h2(lines, "Reference Routing") is None:
        add(diagnostics, repo_root, skill_md, 1, "RPS007", "SKILL.md must contain ## Reference Routing")

    if not any("does not map cleanly" in line for line in lines):
        add(diagnostics, repo_root, skill_md, 1, "RPS007", "SKILL.md must include fallback guidance")

    if family.key == "kaoju":
        for heading in ("Overview", "When to Use", "Guardrails"):
            if find_h2(lines, heading) is None:
                add(diagnostics, repo_root, skill_md, 1, "RPS018", f"Kaoju SKILL.md must contain ## {heading}")

    if family.key in {"deepsci", "kaoju"}:
        reminder_line = next(
            (line_number for line_number, line in enumerate(lines, start=1) if DEEPSCI_CALLBACK_ANTI_PATTERN in line),
            None,
        )
        begin_command = f"isomer-cli --print-json project skill-callbacks resolve --skill {skill_name} --stage begin"
        end_command = f"isomer-cli --print-json project skill-callbacks resolve --skill {skill_name} --stage end"
        begin_steps = [
            (line_number, number, line)
            for line_number, number, line in workflow_steps
            if begin_command in line and "Apply begin callbacks" in line
        ]
        end_steps = [
            (line_number, number, line)
            for line_number, number, line in workflow_steps
            if end_command in line and "Apply end callbacks" in line
        ]
        begin_ok = any(
            number > 1 and all(term in line for term in DEEPSCI_CALLBACK_REQUIRED_TERMS)
            for _, number, line in begin_steps
        )
        end_ok = any(all(term in line for term in DEEPSCI_CALLBACK_REQUIRED_TERMS) for _, _, line in end_steps)
        ordered_ok = bool(begin_steps and end_steps and min(number for _, number, _ in begin_steps) < max(number for _, number, _ in end_steps))
        if reminder_line is not None or not begin_ok or not end_ok or not ordered_ok:
            add(
                diagnostics,
                repo_root,
                skill_md,
                reminder_line or workflow_line or 1,
                "RPS017",
                f"production {family.key} SKILL.md must express User Skill Callback begin/end resolution as numbered workflow steps",
            )


def validate_manifest(skill_dir: Path, repo_root: Path, diagnostics: list[Diagnostic]) -> None:
    skill_name = skill_dir.name
    manifest = skill_dir / "agents" / "openai.yaml"
    if not manifest.exists():
        add(diagnostics, repo_root, skill_dir, 1, "RPS006", "agents/openai.yaml is required")
        return
    expected_version = package_release_version(repo_root)
    if expected_version is not None:
        validate_release_version_metadata(manifest, expected_version, repo_root, diagnostics, "RPS006")
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


def package_release_version(repo_root: Path) -> str | None:
    pyproject = repo_root / "pyproject.toml"
    if not pyproject.is_file():
        return None
    raw = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    project = raw.get("project")
    version = project.get("version") if isinstance(project, dict) else None
    return version if isinstance(version, str) and version else None


def validate_release_version_metadata(
    manifest: Path,
    expected_version: str,
    repo_root: Path,
    diagnostics: list[Diagnostic],
    code: str,
) -> None:
    try:
        raw = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        add(diagnostics, repo_root, manifest, 1, code, f"agents/openai.yaml is invalid YAML: {exc}")
        return
    metadata = raw.get("metadata") if isinstance(raw, dict) else None
    version = metadata.get("version") if isinstance(metadata, dict) else None
    if not isinstance(version, str) or not version:
        add(diagnostics, repo_root, manifest, 1, code, "agents/openai.yaml metadata.version is required")
        return
    try:
        Version(version)
    except InvalidVersion:
        add(diagnostics, repo_root, manifest, 1, code, f"agents/openai.yaml metadata.version is not valid PEP 440: {version!r}")
        return
    if version != expected_version:
        add(
            diagnostics,
            repo_root,
            manifest,
            1,
            code,
            f"agents/openai.yaml metadata.version must match Isomer release {expected_version!r}",
        )

def clean_reference(raw: str) -> str | None:
    value = raw.strip().strip("<>").strip()
    if "://" in value or value.startswith("#") or any(character.isspace() for character in value):
        return None
    value = value.split("#", 1)[0].strip()
    value = value.rstrip(".,;:)")
    if any(value.startswith(prefix) for prefix in LOCAL_REFERENCE_PREFIXES) or value.startswith(("./", "../")):
        return value
    if re.match(r"^isomer-(?:deepsci|kaoju)-[a-z0-9-]+/", value):
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
        if raw_id.casefold() in {"placeholder", "id", "---"} or set(raw_id) <= {"-"}:
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
        if raw_id.casefold() in {"placeholder", "id", "---"} or set(raw_id) <= {"-"}:
            continue
        match = MIGRATION_PLACEHOLDER_CELL_RE.match(raw_id)
        if match:
            ids[match.group(1)] = line_number
    return ids


def _identity_table_cells(path: Path) -> list[tuple[int, str]]:
    cells: list[tuple[int, str]] = []
    for line_number, line in enumerate(read_lines(path), start=1):
        if not line.startswith("|"):
            continue
        raw_id = line.strip().strip("|").split("|", 1)[0].strip().strip("`")
        if raw_id.casefold() in {"placeholder", "id", "semantic id", "---"} or set(raw_id) <= {"-"}:
            continue
        if ":" in raw_id or raw_id.startswith(("DEEPSCI", "<", "[[")):
            cells.append((line_number, raw_id))
    return cells


def validate_deepsci_identity_inventory(
    skill_dirs: list[tuple[Path, str]],
    repo_root: Path,
    diagnostics: list[Diagnostic],
) -> set[str]:
    """Validate collision-free canonical DeepSci registry and binding coverage."""

    binding_occurrences: dict[str, tuple[Path, int]] = {}
    migration_ids: set[str] = set()
    binding_ids: set[str] = set()
    for skill_dir, generation in skill_dirs:
        if generation != "deepsci":
            continue
        migration_path = skill_dir / "migrate" / "placeholders.md"
        binding_path = skill_dir / "placeholder-bindings.md"
        local_migration: set[str] = set()
        local_bindings: set[str] = set()
        for path, destination in ((migration_path, local_migration), (binding_path, local_bindings)):
            if not path.exists():
                continue
            seen: dict[str, int] = {}
            for line_number, semantic_id in _identity_table_cells(path):
                try:
                    parsed = parse_artifact_identity(semantic_id, expected_extension="deepsci")
                except ArtifactIdentityError as exc:
                    add(diagnostics, repo_root, path, line_number, "RPS028", f"invalid DeepSci artifact identity '{semantic_id}': {exc}")
                    continue
                if parsed.value in seen:
                    add(
                        diagnostics,
                        repo_root,
                        path,
                        line_number,
                        "RPS012",
                        f"duplicate DeepSci artifact identity '{parsed.value}'; first declared on line {seen[parsed.value]}",
                    )
                    continue
                seen[parsed.value] = line_number
                destination.add(parsed.value)
                if path == binding_path:
                    prior = binding_occurrences.get(parsed.value)
                    if prior is not None:
                        add(
                            diagnostics,
                            repo_root,
                            path,
                            line_number,
                            "RPS012",
                            f"DeepSci binding identity '{parsed.value}' collides with {relpath(prior[0], repo_root)}:{prior[1]}",
                        )
                    else:
                        binding_occurrences[parsed.value] = (path, line_number)
        migration_ids.update(local_migration)
        binding_ids.update(local_bindings)
        if migration_path.exists():
            for semantic_id in sorted(local_migration - local_bindings):
                add(diagnostics, repo_root, binding_path, 1, "RPS012", f"binding coverage is missing '{semantic_id}'")
            for semantic_id in sorted(local_bindings - local_migration):
                add(diagnostics, repo_root, binding_path, 1, "RPS012", f"binding row '{semantic_id}' has no matching source registry row")

    for semantic_id in sorted(migration_ids - binding_ids):
        add(diagnostics, repo_root, repo_root, 1, "RPS012", f"DeepSci source inventory has no binding for '{semantic_id}'")

    semantic_path = next(
        (
            skill_dir / "references" / "semantic-placeholders.md"
            for skill_dir, generation in skill_dirs
            if generation == "deepsci" and skill_dir.name == "isomer-deepsci-shared"
        ),
        None,
    )
    semantic_ids: set[str] = set()
    if semantic_path is not None and semantic_path.exists():
        for line_number, semantic_id in _identity_table_cells(semantic_path):
            try:
                semantic_ids.add(parse_artifact_identity(semantic_id, expected_extension="deepsci").value)
            except ArtifactIdentityError as exc:
                add(diagnostics, repo_root, semantic_path, line_number, "RPS028", f"invalid DeepSci artifact identity '{semantic_id}': {exc}")
    return binding_ids | migration_ids | semantic_ids


def validate_artifact_identity_guidance(
    document: Document,
    repo_root: Path,
    diagnostics: list[Diagnostic],
    registered_by_family: dict[str, set[str]],
) -> None:
    """Reject superseded, unowned, unknown, and lossy artifact identity forms."""

    family = "deepsci" if "deepsci" in document.roles else "kaoju" if "kaoju" in document.roles else None
    if family is None or not is_active_guidance(document):
        return
    registered = registered_by_family.get(family, set())
    known_whats = {identity.split(":", 1)[1] for identity in registered}
    known_legacy = {what.replace("-", "_") for what in known_whats}
    for line_number, line in enumerate(document.lines, start=1):
        offenders: set[str] = set()
        if "--placeholder" in line:
            offenders.add("--placeholder")
        offenders.update(match.group(0) for match in WRAPPED_IDENTITY_RE.finditer(line))
        offenders.update(match.group(0) for match in DOUBLE_BRACKET_ARTIFACT_RE.finditer(line))
        offenders.update(
            match.group(0)
            for match in LEGACY_ANGLE_ARTIFACT_RE.finditer(line)
            if match.group(1) in known_legacy
        )
        offenders.update(match.group(1) for match in NONCANONICAL_EXTENSION_ID_RE.finditer(line))
        for offender in sorted(offenders):
            add(diagnostics, repo_root, document.path, line_number, "RPS028", f"superseded artifact identity form '{offender}' is forbidden")

        for match in CANONICAL_IDENTITY_TOKEN_RE.finditer(line):
            semantic_id = match.group(1)
            try:
                parse_artifact_identity(
                    semantic_id,
                    expected_extension=family,
                    known_extensions=packaged_extension_ids(),
                )
            except ArtifactIdentityError as exc:
                add(diagnostics, repo_root, document.path, line_number, "RPS028", f"artifact identity '{semantic_id}' violates ownership: {exc}")
                continue
            if semantic_id not in registered and semantic_id != f"{family.upper()}:WHAT":
                add(diagnostics, repo_root, document.path, line_number, "RPS028", f"artifact identity '{semantic_id}' is not registered")

        for code_span in CODE_SPAN_RE.findall(line):
            if code_span in known_whats or code_span in known_legacy:
                add(diagnostics, repo_root, document.path, line_number, "RPS028", f"bare artifact identity '{code_span}' is forbidden")


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
    canonical_path = "deepsci/isomer-deepsci-shared/references/tbd-surface-registry.md"
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
    if "deepsci" not in document.roles or not is_active_guidance(document):
        return
    _ = registered_ids
    for line_number, line in enumerate(document.lines, start=1):
        for match in RSCH_OBJECT_PLACEHOLDER_RE.finditer(line):
            add(
                diagnostics,
                repo_root,
                document.path,
                line_number,
                "RPS028",
                f"superseded double-bracket artifact identity '{match.group(0)}' is forbidden",
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
    if len(parts) < 3 or parts[0] != "deepsci":
        return
    registered_ids = set().union(*registered_by_skill.values()) if registered_by_skill else set()
    for line_number, line in enumerate(document.lines, start=1):
        for match in MIGRATION_PLACEHOLDER_RE.finditer(line):
            semantic_id = match.group(1)
            if semantic_id not in registered_ids and semantic_id != "DEEPSCI:WHAT":
                add(
                    diagnostics,
                    repo_root,
                    document.path,
                    line_number,
                    "RPS009",
                    f"DeepSci artifact identity '{semantic_id}' is not registered in migrate/placeholders.md",
                )


def validate_deepsci_placeholder_bindings(
    skill_dirs: list[tuple[Path, str]],
    repo_root: Path,
    diagnostics: list[Diagnostic],
) -> None:
    for skill_dir, generation in skill_dirs:
        if generation != "deepsci":
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
                "production DeepSci skill with migrate/placeholders.md must include placeholder-bindings.md",
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
                f"placeholder-bindings.md is missing canonical identity '{placeholder_id}'",
            )
        for placeholder_id in sorted(set(actual) - set(expected)):
            add(
                diagnostics,
                repo_root,
                binding_path,
                actual[placeholder_id],
                "RPS012",
                f"placeholder-bindings.md has extra canonical identity '{placeholder_id}'",
            )


def validate_deepsci_payload_first_bindings(
    skill_dirs: list[tuple[Path, str]],
    repo_root: Path,
    diagnostics: list[Diagnostic],
) -> None:
    for skill_dir, generation in skill_dirs:
        if generation != "deepsci":
            continue
        binding_path = skill_dir / "placeholder-bindings.md"
        if not binding_path.exists():
            continue
        lines = read_lines(binding_path)
        has_structured_row = False
        has_validation_guidance = any(
            "ext research records validate" in line
            and "--format-profile" in line
            and "--payload-file" in line
            for line in lines
        )
        has_payload_inspection_guidance = any(
            "ext research records show" in line and "--include-payload" in line for line in lines
        )
        has_render_export_guidance = any(
            "ext research records render" in line and "--output-file" in line for line in lines
        )
        has_display_field_guidance = any(
            "top-level `title` and `summary`" in line and "non-empty" in line for line in lines
        )
        has_idea_entry_display_guidance = any(
            "idea-bearing entries" in line and "`title`" in line and "`summary`" in line for line in lines
        )
        for line_number, line in enumerate(lines, start=1):
            normalized_line = line.lower()
            if "one_liner" in normalized_line:
                add(
                    diagnostics,
                    repo_root,
                    binding_path,
                    line_number,
                    "RPS014",
                    "structured binding guidance must not use legacy one_liner authoring; use summary",
                )
            if (
                "generated markdown" in normalized_line
                and any(term in normalized_line for term in ("canonical", "source of truth", "authoritative", "durable state"))
            ):
                add(
                    diagnostics,
                    repo_root,
                    binding_path,
                    line_number,
                    "RPS014",
                    "structured binding guidance must not treat generated Markdown as canonical durable state",
                )
            if (
                "payload_json" in normalized_line
                and "sqlite" in normalized_line
                and any(term in normalized_line for term in ("canonical", "source of truth", "only durable", "authoritative"))
            ):
                add(
                    diagnostics,
                    repo_root,
                    binding_path,
                    line_number,
                    "RPS014",
                    "structured binding guidance must not treat SQLite payload_json as the only durable structured payload copy",
                )
            if not line.startswith(("| DEEPSCI:", "| `DEEPSCI:")):
                continue
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) < 7:
                continue
            profile_ref = cells[5].strip("`")
            command = cells[6].strip("`")
            if profile_ref.startswith("isomer:deepsci/record-format/profile/"):
                has_structured_row = True
                if DEEPSCI_FORMAT_PROFILE_RE.match(profile_ref) is None:
                    add(
                        diagnostics,
                        repo_root,
                        binding_path,
                        line_number,
                        "RPS014",
                        "structured binding profile must use an explicit isomer:deepsci/record-format/profile/.../v2 ref",
                    )
                if "--format-profile" not in command:
                    add(
                        diagnostics,
                        repo_root,
                        binding_path,
                        line_number,
                        "RPS014",
                        "structured binding command must use --format-profile",
                    )
                if "--profile " in command:
                    add(
                        diagnostics,
                        repo_root,
                        binding_path,
                        line_number,
                        "RPS014",
                        "structured binding command must not use bare --profile",
                    )
                if "--payload-file" not in command:
                    add(
                        diagnostics,
                        repo_root,
                        binding_path,
                        line_number,
                        "RPS014",
                        "structured binding command must use --payload-file",
                    )
                if "--body-file" in command or "--body " in command:
                    add(
                        diagnostics,
                        repo_root,
                        binding_path,
                        line_number,
                        "RPS014",
                        "structured binding command must not use direct Markdown body authoring",
                    )
                if "--render markdown" in command:
                    add(
                        diagnostics,
                        repo_root,
                        binding_path,
                        line_number,
                        "RPS014",
                        "structured binding command must not request default durable Markdown rendering; use ext research records render for review or explicit export",
                    )
                if "--content-name" in command:
                    add(
                        diagnostics,
                        repo_root,
                        binding_path,
                        line_number,
                        "RPS014",
                        "structured binding command must not use --content-name for normal structured create/update",
                    )
            elif "." in profile_ref and " " not in profile_ref:
                add(
                    diagnostics,
                    repo_root,
                    binding_path,
                    line_number,
                    "RPS014",
                    "structured binding profile must be promoted from legacy dotted profile names to --format-profile refs",
                )
        if has_structured_row and not has_validation_guidance:
            add(
                diagnostics,
                repo_root,
                binding_path,
                1,
                "RPS014",
                "structured binding page must include an ext research records validate step with --format-profile and --payload-file",
            )
        if has_structured_row and not has_payload_inspection_guidance:
            add(
                diagnostics,
                repo_root,
                binding_path,
                1,
                "RPS014",
                "structured binding page must show payload inspection with ext research records show --include-payload",
            )
        if has_structured_row and not has_render_export_guidance:
            add(
                diagnostics,
                repo_root,
                binding_path,
                1,
                "RPS014",
                "structured binding page must direct human review or Markdown export through ext research records render and explicit --output-file",
            )
        if has_structured_row and not has_display_field_guidance:
            add(
                diagnostics,
                repo_root,
                binding_path,
                1,
                "RPS014",
                "structured binding page must require non-empty top-level `title` and `summary` display fields",
            )
        if has_structured_row and not has_idea_entry_display_guidance:
            add(
                diagnostics,
                repo_root,
                binding_path,
                1,
                "RPS014",
                "structured binding page must require `title` and `summary` on idea-bearing entries",
            )


def validate_deepsci_display_contract_guidance(document: Document, repo_root: Path, diagnostics: list[Diagnostic]) -> None:
    if "deepsci" not in document.roles or not is_active_guidance(document):
        return
    for line_index, line in enumerate(document.lines):
        lowered = line.casefold()
        if "one_liner" in lowered and not is_rejection_line(line):
            add(
                diagnostics,
                repo_root,
                document.path,
                line_index + 1,
                "RPS014",
                "active DeepSci guidance must not author legacy one_liner display fields; use summary",
            )
        if DEEPSCI_FORMAT_PROFILE_V1_TEXT_RE.search(line) and not is_rejection_line(line):
            add(
                diagnostics,
                repo_root,
                document.path,
                line_index + 1,
                "RPS014",
                "active DeepSci guidance must not use structured-record v1 profile refs for new writes; use v2",
            )
    if document.rel_target.endswith("/SKILL.md") and not any(
        "supported deepsci v2 display contract" in line.casefold()
        and "`title`" in line
        and "`summary`" in line
        for line in document.lines
    ):
        add(
            diagnostics,
            repo_root,
            document.path,
            1,
            "RPS014",
            "active DeepSci SKILL.md must teach the supported v2 `title` and `summary` display contract",
        )


def validate_deepsci_storage_binding(
    document: Document,
    repo_root: Path,
    diagnostics: list[Diagnostic],
    allow_zones: dict[str, tuple[str, ...]],
) -> None:
    if "deepsci" not in document.roles or not is_active_guidance(document):
        return
    for line_index, line in enumerate(document.lines):
        if allowed_by_rule("deepsci_storage_binding", document, line_index, allow_zones):
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
        for label, pattern in DEEPSCI_STORAGE_BINDING_PATTERNS:
            if pattern.search(line):
                if label == "storage-bound research record" and not DEEPSCI_STORAGE_BINDING_VERB_RE.search(line):
                    continue
                add(
                    diagnostics,
                    repo_root,
                    document.path,
                    line_index + 1,
                    "RPS010",
                    f"active production DeepSci guidance contains {label}",
                )


def validate_deepsci_worker_output_policy(document: Document, repo_root: Path, diagnostics: list[Diagnostic]) -> None:
    if "deepsci" not in document.roles or not is_active_guidance(document):
        return
    if not document.rel_target.endswith("/SKILL.md"):
        return
    text = "\n".join(document.lines)
    lowered = text.casefold()
    if document.rel_target == "deepsci/isomer-deepsci-shared/SKILL.md":
        for term in DEEPSCI_SHARED_WORKER_OUTPUT_REQUIRED_TERMS:
            if term.casefold() not in lowered:
                add(
                    diagnostics,
                    repo_root,
                    document.path,
                    1,
                    "RPS015",
                    f"shared production DeepSci Worker Output Policy must mention {term}",
                )
        return
    if not any(term in lowered for term in DEEPSCI_PLAIN_OUTPUT_TERMS):
        return
    for term in DEEPSCI_WORKER_OUTPUT_REQUIRED_TERMS:
        if term not in lowered:
            add(
                diagnostics,
                repo_root,
                document.path,
                1,
                "RPS015",
                f"active production DeepSci skill guidance that writes plain files must mention {term}",
            )


def validate_deepsci_latest_context_preflight(document: Document, repo_root: Path, diagnostics: list[Diagnostic]) -> None:
    if "deepsci" not in document.roles or not is_active_guidance(document):
        return
    if not document.rel_target.endswith("/SKILL.md"):
        return
    if document.rel_target == "deepsci/isomer-deepsci-shared/SKILL.md":
        return
    if not (document.path.parent / "placeholder-bindings.md").exists():
        return
    text = "\n".join(document.lines)
    lowered = text.casefold()
    missing_required = [term for term in DEEPSCI_LATEST_CONTEXT_REQUIRED_TERMS if term not in lowered]
    has_freshness_intent = any(term in lowered for term in DEEPSCI_LATEST_CONTEXT_FRESHNESS_TERMS)
    if not missing_required and has_freshness_intent:
        return
    if "worker-output reminder" in lowered and "latest context preflight" not in lowered:
        message = "worker-output guidance does not satisfy the latest-context preflight requirement for durable record work"
    elif missing_required:
        message = "active production DeepSci durable-record-writing entrypoint must mention Latest Context Preflight and latest-context-snapshot"
    else:
        message = "active production DeepSci durable-record-writing entrypoint must include freshness-intent wording before trusting prompt memory or prior prose"
    add(diagnostics, repo_root, document.path, 1, "RPS016", message)


def validate_deepsci_support_section_intros(
    document: Document,
    repo_root: Path,
    diagnostics: list[Diagnostic],
) -> None:
    if "deepsci" not in document.roles or not is_active_guidance(document):
        return
    for line_index, line in enumerate(document.lines):
        match = HEADING_RE.match(line)
        if not match:
            continue
        heading = normalize_heading(match.group(2))
        if heading not in DEEPSCI_SUPPORT_SECTION_HEADINGS:
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
                f"active production DeepSci {heading} section must start with a one-to-three-sentence interpretive paragraph",
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
                f"active production DeepSci {heading} section must start with a one-to-three-sentence interpretive paragraph",
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
                f"active production DeepSci {heading} section intro must be one to three sentences",
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
                    f"active production DeepSci {heading} section intro must be separated from following content by a blank line",
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


def validate_kaoju_direct_references(
    skill_dir: Path,
    repo_root: Path,
    diagnostics: list[Diagnostic],
) -> None:
    skill_root = skill_dir.resolve()
    active_files = sorted(
        path
        for path in skill_dir.rglob("*")
        if path.is_file()
        and path.suffix in {".md", ".yaml", ".yml"}
        and not any(part in {"assets", "scripts"} for part in path.relative_to(skill_dir).parts[:-1])
    )
    for path in active_files:
        for line_number, line in enumerate(read_lines(path), start=1):
            for reference in local_references_from_line(line):
                if is_placeholder_reference(reference):
                    continue
                target = (skill_dir / reference).resolve()
                if not target.is_relative_to(skill_root) or not target.exists():
                    add(
                        diagnostics,
                        repo_root,
                        path,
                        line_number,
                        "RPS005",
                        f"local reference '{reference}' does not exist inside {skill_dir.name}",
                    )


def validate_kaoju_command_page(
    path: Path,
    repo_root: Path,
    diagnostics: list[Diagnostic],
) -> None:
    lines = read_lines(path)
    workflow_line = find_h2(lines, "Workflow")
    if workflow_line is None:
        add(diagnostics, repo_root, path, 1, "RPS018", "Kaoju command page must contain ## Workflow")
        return
    if workflow_line > 20:
        add(diagnostics, repo_root, path, workflow_line, "RPS018", "Kaoju command ## Workflow must appear near the top")
    numbers = workflow_step_numbers(lines, workflow_line)
    if len(numbers) < 2 or numbers[0] != 1:
        add(diagnostics, repo_root, path, workflow_line, "RPS018", "Kaoju command ## Workflow must contain numbered steps")
    text = "\n".join(lines)
    if "Gates, Blockers, and Resume" not in text and not any("does not map cleanly" in line for line in lines):
        add(diagnostics, repo_root, path, 1, "RPS018", "Kaoju command page must include Gate, blocker, and resume guidance")


def load_kaoju_process_contract(
    kaoju_root: Path,
    repo_root: Path,
    diagnostics: list[Diagnostic],
) -> dict[str, object] | None:
    path = kaoju_root / "isomer-kaoju-pipeline" / "SKILL.md"
    try:
        contract = load_contract()
        raw = contract.raw
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        add(diagnostics, repo_root, path, 1, "RPS026", f"Kaoju extension process resource is unavailable: {exc}")
        return None
    return dict(raw)


def _contract_commands(contract: dict[str, object]) -> tuple[str, ...]:
    commands: list[str] = []
    for field in ("survey_intents", "compatibility_procedures"):
        values = contract.get(field, [])
        if isinstance(values, list):
            commands.extend(str(value) for value in values)
    managers = contract.get("manager_actions", {})
    if isinstance(managers, dict):
        commands.extend(str(value) for value in managers if str(value) not in commands)
    return tuple(commands)


def validate_kaoju_package_contract(
    kaoju_root: Path,
    repo_root: Path,
    diagnostics: list[Diagnostic],
    contract: dict[str, object],
) -> None:
    contract_path = kaoju_root / "isomer-kaoju-pipeline" / "SKILL.md"
    skills = tuple(str(value) for value in contract.get("skills", []) if isinstance(value, str))
    intents = tuple(str(value) for value in contract.get("survey_intents", []) if isinstance(value, str))
    if len(skills) != 14:
        add(diagnostics, repo_root, contract_path, 1, "RPS026", f"Kaoju contract must declare fourteen skills, found {len(skills)}")
    if len(intents) != 10:
        add(diagnostics, repo_root, contract_path, 1, "RPS026", f"Kaoju contract must declare ten survey intents, found {len(intents)}")

    actual_skills = tuple(path.name for path in kaoju_root.iterdir() if path.is_dir() and path.name.startswith("isomer-kaoju-"))
    if set(actual_skills) != set(skills):
        add(diagnostics, repo_root, contract_path, 1, "RPS026", "Kaoju contract skill inventory differs from packaged skill directories")

    manifest_path = kaoju_root.parents[1] / "manifest.toml"
    if not manifest_path.exists():
        return
    try:
        manifest = tomllib.loads(manifest_path.read_text(encoding="utf-8"))
        group = manifest["groups"]["kaoju"]
    except (OSError, tomllib.TOMLDecodeError, KeyError, TypeError) as exc:
        add(diagnostics, repo_root, manifest_path, 1, "RPS026", f"packaged Kaoju manifest cannot be checked: {exc}")
        return
    expected_skill_paths = [f"research-paradigm/kaoju/{name}" for name in skills]
    if group.get("entry_skill") != contract.get("entry_skill"):
        add(diagnostics, repo_root, manifest_path, 1, "RPS026", "Kaoju manifest entry skill differs from the checked contract")
    if group.get("skills") != expected_skill_paths:
        add(diagnostics, repo_root, manifest_path, 1, "RPS026", "Kaoju manifest skill order differs from the checked contract")
    if tuple(group.get("commands", [])) != _contract_commands(contract):
        add(diagnostics, repo_root, manifest_path, 1, "RPS026", "Kaoju manifest command order differs from the checked contract")


def validate_kaoju_command_surface(
    kaoju_root: Path,
    repo_root: Path,
    diagnostics: list[Diagnostic],
) -> None:
    pipeline = kaoju_root / "isomer-kaoju-pipeline"
    command_root = pipeline / "commands"
    if not command_root.exists():
        add(diagnostics, repo_root, command_root, 1, "RPS018", "Kaoju pipeline commands directory is missing")
        return
    contract = load_kaoju_process_contract(kaoju_root, repo_root, diagnostics)
    expected_commands = set(_contract_commands(contract)) if contract is not None else set(EXPECTED_KAOJU_COMMANDS)
    command_pages = {path.stem: path for path in command_root.glob("*.md") if path.is_file()}
    for missing in sorted(expected_commands - set(command_pages)):
        add(diagnostics, repo_root, command_root / f"{missing}.md", 1, "RPS018", f"expected Kaoju command '{missing}' is missing")
    for extra in sorted(set(command_pages) - expected_commands):
        add(diagnostics, repo_root, command_pages[extra], 1, "RPS018", f"unapproved Kaoju command '{extra}' is active")
    for forbidden in sorted(FORBIDDEN_KAOJU_PROCEDURES & set(command_pages)):
        add(diagnostics, repo_root, command_pages[forbidden], 1, "RPS018", f"generic procedure '{forbidden}' must not be exposed by Kaoju")
    for path in command_pages.values():
        validate_kaoju_command_page(path, repo_root, diagnostics)

    skill_md = pipeline / "SKILL.md"
    if skill_md.exists():
        lines = read_lines(skill_md)
        text = "\n".join(lines)
        for heading in ("Survey Intents", "Compatibility Procedures", "Grouped Managers"):
            if find_h2(lines, heading) is None:
                add(diagnostics, repo_root, skill_md, 1, "RPS018", f"Kaoju pipeline must contain ## {heading}")
        for command in sorted(expected_commands):
            if f"`{command}`" not in text or f"commands/{command}.md" not in text:
                add(diagnostics, repo_root, skill_md, 1, "RPS018", f"Kaoju pipeline must link command '{command}'")
        for forbidden in sorted(FORBIDDEN_KAOJU_PROCEDURES):
            public_row = re.compile(rf"^\|\s*`{re.escape(forbidden)}`\s*\|", re.M)
            if public_row.search(text):
                add(diagnostics, repo_root, skill_md, 1, "RPS018", f"generic procedure '{forbidden}' must not be public")

    action_contracts = {
        "manage-survey": ("list", "show", "status", "export"),
        "manage-dataset": ("register", "list", "show", "refresh", "remove"),
    }
    for command, actions in action_contracts.items():
        path = command_pages.get(command)
        if path is None:
            continue
        text = path.read_text(encoding="utf-8")
        for action in actions:
            if f"`{action}`" not in text:
                add(diagnostics, repo_root, path, 1, "RPS018", f"{command} must include action '{action}'")


def validate_kaoju_shared_references(
    kaoju_root: Path,
    repo_root: Path,
    diagnostics: list[Diagnostic],
) -> None:
    references = kaoju_root / "isomer-kaoju-shared" / "references"
    actual = {path.name for path in references.glob("*.md") if path.is_file()} if references.exists() else set()
    for missing in sorted(EXPECTED_KAOJU_SHARED_REFERENCES - actual):
        add(diagnostics, repo_root, references / missing, 1, "RPS019", f"required Kaoju shared reference '{missing}' is missing")


def validate_kaoju_active_guidance(
    document: Document,
    repo_root: Path,
    diagnostics: list[Diagnostic],
) -> None:
    if "kaoju" not in document.roles or not is_active_guidance(document):
        return
    for line_number, line in enumerate(document.lines, start=1):
        if re.search(r"(?:survey-process\.v2|bindings\.v2(?:\.schema)?|artifact-semantics\.v1(?:\.schema)?)\.json", line):
            add(diagnostics, repo_root, document.path, line_number, "RPS029", "active Kaoju guidance names an extension-owned resource file directly")
        for label, pattern in KAOJU_FORBIDDEN_ACTIVE_PATTERNS:
            if pattern.search(line) and not is_rejection_line(line):
                add(diagnostics, repo_root, document.path, line_number, "RPS020", f"active Kaoju guidance contains {label}")


def validate_kaoju_resource_and_shared_routing(
    kaoju_root: Path,
    repo_root: Path,
    diagnostics: list[Diagnostic],
) -> None:
    """Enforce extension-query data access and the family shared-procedure route."""

    pipeline = kaoju_root / "isomer-kaoju-pipeline" / "SKILL.md"
    if pipeline.exists():
        text = pipeline.read_text(encoding="utf-8")
        if "isomer-cli --print-json ext kaoju process show" not in text:
            add(diagnostics, repo_root, pipeline, 1, "RPS029", "Kaoju pipeline must load process data through ext kaoju process show")
        if "## Plan First" not in text or "internal todo list or planning tool" not in text:
            add(diagnostics, repo_root, pipeline, 1, "RPS029", "Kaoju pipeline must preserve its upfront internal planning requirement")

    shared = kaoju_root / "isomer-kaoju-shared"
    for path in (shared / "SKILL.md", shared / "references" / "artifact-semantics.md"):
        if path.exists() and "ext kaoju bindings describe KAOJU:WHAT" not in path.read_text(encoding="utf-8"):
            add(diagnostics, repo_root, path, 1, "RPS029", "shared Kaoju artifact guidance must route through ext kaoju bindings describe KAOJU:WHAT")

    for skill_dir in sorted(path for path in kaoju_root.glob("isomer-kaoju-*") if path.is_dir()):
        skill_md = skill_dir / "SKILL.md"
        if skill_dir.name != "isomer-kaoju-shared" and skill_md.exists():
            if "isomer-kaoju-shared" not in skill_md.read_text(encoding="utf-8"):
                add(diagnostics, repo_root, skill_md, 1, "RPS029", "common Kaoju procedure must route through isomer-kaoju-shared")
        binding_page = skill_dir / "artifact-bindings.md"
        if binding_page.exists() and len(read_lines(binding_page)) > 25:
            add(diagnostics, repo_root, binding_page, 1, "RPS024", "producer binding projection is oversized and competes with extension query authority")


def _markdown_table(lines: tuple[str, ...], required_header: str) -> tuple[list[str], list[tuple[int, list[str]]]]:
    for index, line in enumerate(lines):
        if not line.startswith("|"):
            continue
        header = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
        if required_header not in header or index + 1 >= len(lines):
            continue
        rows: list[tuple[int, list[str]]] = []
        for row_index, row in enumerate(lines[index + 2 :], start=index + 3):
            if not row.startswith("|"):
                break
            cells = [cell.strip().strip("`") for cell in row.strip().strip("|").split("|")]
            if len(cells) == len(header):
                rows.append((row_index, cells))
        return header, rows
    return [], []


def _kaoju_catalog_profiles(repo_root: Path) -> dict[str, dict[str, object]]:
    relative = Path("src/isomer_labs/artifact_formats/assets/research_record_formats/profiles/kaoju.v1.json")
    candidates = (repo_root / relative, Path(__file__).resolve().parents[1] / relative)
    catalog_path = next((candidate for candidate in candidates if candidate.exists()), None)
    if catalog_path is None:
        return {}
    raw = json.loads(catalog_path.read_text(encoding="utf-8"))
    result: dict[str, dict[str, object]] = {}
    for entry in raw.get("profiles", []):
        if not isinstance(entry, dict):
            continue
        semantic_id = str(entry.get("semantic_id") or "")
        try:
            parse_artifact_identity(semantic_id, expected_extension="kaoju")
        except ArtifactIdentityError:
            continue
        profile_slug = str(entry.get("profile_slug") or "")
        profile_ref = str(
            entry.get("ref")
            or "isomer:research/record-format/profile/"
            f"{entry.get('family')}/{entry.get('artifact_class')}/{profile_slug}/{entry.get('version')}"
        )
        normalized = dict(entry)
        normalized["profile_ref"] = profile_ref
        result[semantic_id] = normalized
    return result


def validate_kaoju_artifact_bindings(
    kaoju_root: Path,
    repo_root: Path,
    diagnostics: list[Diagnostic],
    config: FamilyConfig,
) -> None:
    if config.semantic_id_pattern is None or config.binding_filename is None:
        return
    summary_path = kaoju_root / "isomer-kaoju-shared" / "references" / "artifact-semantics.md"
    registry_path = summary_path
    try:
        coverage = resource_coverage_diagnostics()
        loaded_bindings = load_binding_registry()
        loaded_semantics = load_semantic_registry()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        add(diagnostics, repo_root, registry_path, 1, "RPS021", f"Kaoju extension resources are unavailable: {exc}")
        return
    for message in coverage:
        add(diagnostics, repo_root, registry_path, 1, "RPS021", message)
    bindings = {semantic_id: asdict(binding) for semantic_id, binding in loaded_bindings.items()}
    if set(bindings) != set(loaded_semantics):
        add(diagnostics, repo_root, registry_path, 1, "RPS021", "Kaoju semantic and binding resource identifiers differ")

    catalog = _kaoju_catalog_profiles(repo_root)
    for semantic_id, binding in sorted(bindings.items()):
        profile_ref = binding.get("profile_ref")
        content_mode = binding.get("content_mode")
        if content_mode == "structured_file" and not isinstance(profile_ref, str):
            add(diagnostics, repo_root, registry_path, 1, "RPS022", f"structured binding '{semantic_id}' requires a profile")
        if isinstance(profile_ref, str):
            profile = catalog.get(semantic_id)
            if profile is None:
                add(diagnostics, repo_root, registry_path, 1, "RPS022", f"binding '{semantic_id}' has no profile catalog entry")
                continue
            if profile.get("profile_ref") != profile_ref:
                add(diagnostics, repo_root, registry_path, 1, "RPS022", f"binding '{semantic_id}' profile ref differs from the catalog")
            kinds = profile.get("compatible_record_kinds", [])
            if not isinstance(kinds, list) or binding.get("record_kind") not in kinds:
                add(diagnostics, repo_root, registry_path, 1, "RPS022", f"binding '{semantic_id}' record kind conflicts with its profile")
            if profile.get("artifact_type") != binding.get("artifact_type"):
                add(diagnostics, repo_root, registry_path, 1, "RPS022", f"binding '{semantic_id}' artifact type conflicts with its profile")
            if not isinstance(profile.get("renderer"), str) or not profile.get("renderer"):
                add(diagnostics, repo_root, registry_path, 1, "RPS022", f"profile '{semantic_id}' has no renderer")
            if not isinstance(profile.get("required_payload_paths"), list):
                add(diagnostics, repo_root, registry_path, 1, "RPS022", f"profile '{semantic_id}' has no structured schema hints")
    for semantic_id in sorted(set(catalog) - set(bindings)):
        add(diagnostics, repo_root, registry_path, 1, "RPS022", f"profile catalog id '{semantic_id}' has no binding")

    if summary_path.exists():
        summary_ids = set(re.findall(r"`(KAOJU:[A-Z0-9]+(?:-[A-Z0-9]+)*)`", summary_path.read_text(encoding="utf-8")))
        if summary_ids != set(bindings):
            missing = sorted(set(bindings) - summary_ids)
            extra = sorted(summary_ids - set(bindings))
            add(diagnostics, repo_root, summary_path, 1, "RPS022", f"generated semantic summary differs from registry; missing={missing}, extra={extra}")
    else:
        add(diagnostics, repo_root, summary_path, 1, "RPS022", "generated Kaoju semantic summary is missing")

    contract = load_kaoju_process_contract(kaoju_root, repo_root, diagnostics)
    skill_names = set(str(value) for value in contract.get("skills", [])) if contract is not None else set(EXPECTED_KAOJU_SKILLS)
    allowed_participants = skill_names | {"isomer-srv-topic-env-setup"}
    produced: dict[str, set[str]] = {name: set() for name in skill_names}
    for semantic_id, binding in bindings.items():
        producer = binding.get("producer")
        consumers = binding.get("consumers")
        if producer not in allowed_participants:
            add(diagnostics, repo_root, registry_path, 1, "RPS022", f"binding '{semantic_id}' has unknown producer '{producer}'")
        if isinstance(producer, str) and producer in produced:
            produced[producer].add(semantic_id)
        if not isinstance(consumers, (list, tuple)) or any(consumer not in allowed_participants for consumer in consumers):
            add(diagnostics, repo_root, registry_path, 1, "RPS022", f"binding '{semantic_id}' has an unknown consumer")

    for owner, expected_ids in sorted(produced.items()):
        if not expected_ids:
            continue
        binding_path = kaoju_root / owner / config.binding_filename
        if not binding_path.exists():
            add(diagnostics, repo_root, binding_path, 1, "RPS022", f"Kaoju producer '{owner}' is missing its binding summary")
            continue
        text = binding_path.read_text(encoding="utf-8")
        match = re.search(r"(?m)^Produced semantic ids:\s*(.+)$", text)
        actual_ids = set(re.findall(r"KAOJU:[A-Z0-9]+(?:-[A-Z0-9]+)*", match.group(1))) if match else set()
        if actual_ids != expected_ids:
            add(diagnostics, repo_root, binding_path, 1, "RPS022", f"producer summary differs from registry; expected={sorted(expected_ids)}, actual={sorted(actual_ids)}")
        for term in ("ext kaoju bindings describe KAOJU:WHAT", "project artifacts put", "project artifacts revise"):
            if term not in text:
                add(diagnostics, repo_root, binding_path, 1, "RPS024", f"binding summary is missing '{term}'")
        if re.search(r"--(?:record-kind|semantic-label|format-profile|payload-file|content-name)", text):
            add(diagnostics, repo_root, binding_path, 1, "RPS023", "producer binding summary repeats physical command fields")

    active_refs: dict[str, tuple[Path, int]] = {}
    for path in sorted(kaoju_root.rglob("*.md")):
        if path.name == config.binding_filename or path == summary_path:
            continue
        if path.parts[-2:] == ("references", "artifact-recording.md"):
            continue
        for line_number, line in enumerate(read_lines(path), start=1):
            for semantic_id in re.findall(r"KAOJU:[A-Z0-9]+(?:-[A-Z0-9]+)*", line):
                active_refs.setdefault(semantic_id, (path, line_number))
            if path.name == "SKILL.md" and (
                (config.profile_namespace and config.profile_namespace in line)
                or "--record-kind" in line
                or "--semantic-label" in line
            ):
                add(diagnostics, repo_root, path, line_number, "RPS023", "active stage prose contains physical binding instead of routing to artifact-bindings.md")
    for semantic_id, (path, line_number) in sorted(active_refs.items()):
        if semantic_id not in bindings and semantic_id != "KAOJU:WHAT":
            add(diagnostics, repo_root, path, line_number, "RPS021", f"active Kaoju guidance references unregistered semantic id '{semantic_id}'")

    shared_recording = kaoju_root / "isomer-kaoju-shared" / "references" / "artifact-recording.md"
    if shared_recording.exists():
        shared_text = shared_recording.read_text(encoding="utf-8")
        for term in ("title", "summary", "artifact_family", "semantic_id", "artifact_type", "sections", "worker output policy", "latest", "revision", "lineage", "Markdown", "large-material"):
            if term.casefold() not in shared_text.casefold():
                add(diagnostics, repo_root, shared_recording, 1, "RPS024", f"shared Kaoju recording contract is missing '{term}' guidance")


def validate_kaoju_architecture_guidance(kaoju_root: Path, repo_root: Path, diagnostics: list[Diagnostic]) -> None:
    """Check the cross-skill architecture rules that prevent workflow drift."""

    requirements = {
        "isomer-kaoju-shared/SKILL.md": ("ext kaoju bindings describe", "state DB", "Service Request", "Execution Adapter Command Request", "Run", "Gate"),
        "isomer-kaoju-workspace-mgr/SKILL.md": ("binding registry", "state DB", "scope", "content mode", "Run", "reset"),
        "isomer-kaoju-write/SKILL.md": ("MyST", "canonical", "accepted `KAOJU:AUDIT-REPORT`", "paper-display", "project artifacts"),
        "isomer-kaoju-trial/SKILL.md": ("Service Request", "code_trial", "ambient environment", "method-trial-wrapper", "project artifacts"),
        "isomer-kaoju-reproduce/SKILL.md": ("genuine reproduction", "isomer-kaoju-trial", "capability-probe"),
        "isomer-kaoju-export/SKILL.md": ("state DB", "isomer-cli ext kaoju wiki", "package-owned viewer", "Do not invoke", "typed Artifact service"),
    }
    for relative, terms in requirements.items():
        path = kaoju_root / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for term in terms:
            if term.casefold() not in text.casefold():
                add(diagnostics, repo_root, path, 1, "RPS027", f"Kaoju architecture guidance is missing '{term}'")

    for path in sorted(kaoju_root.rglob("*.md")):
        for line_number, line in enumerate(read_lines(path), start=1):
            if "imsight-llm-wiki" in line.casefold() and not (is_rejection_line(line) or "never invoke" in line.casefold()):
                add(diagnostics, repo_root, path, line_number, "RPS027", "active Kaoju guidance must not invoke the external imsight-llm-wiki skill")


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


def validate_workspace_manager_team_specialization_gate(
    target: Path,
    repo_root: Path,
    diagnostics: list[Diagnostic],
) -> None:
    reference_path = (
        target
        / "deepsci"
        / "isomer-deepsci-workspace-mgr"
        / "references"
        / "validation-and-blockers.md"
    )
    if not reference_path.exists():
        return
    lines = read_lines(reference_path)
    text = "\n".join(lines)
    required_terms = (
        "When the selected topology includes a formal Agent Team layer",
        "When no formal Agent Team layer is selected",
        "without inferring specialization",
    )
    for term in required_terms:
        if term not in text:
            add(
                diagnostics,
                repo_root,
                reference_path,
                1,
                "RPS025",
                f"DeepSci workspace readiness must document the Topic Team Specialization gate phrase '{term}'",
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
    flat_skill_dirs = sorted(
        path
        for path in target.iterdir()
        if path.is_dir() and path.name.startswith(("isomer-deepsci-", "isomer-kaoju-"))
    )
    for skill_dir in flat_skill_dirs:
        add(
            diagnostics,
            repo_root,
            skill_dir,
            1,
            "RPS007",
            "active flat root research skill folders are not allowed; use the configured family root",
        )

    skill_dirs: list[tuple[Path, str]] = []
    for retired_root in ("v1", "v2"):
        root_path = target / retired_root
        if root_path.exists():
            add(diagnostics, repo_root, root_path, 1, "RPS007", f"{retired_root}/ retired skill root must be absent")

    family_by_key = {family.key: family for family in FAMILY_CONFIGS}
    for family in FAMILY_CONFIGS:
        family_root = target / family.root_name
        if not family_root.exists():
            if family.required:
                add(diagnostics, repo_root, family_root, 1, "RPS007", f"{family.root_name}/ production skill directory is missing")
            continue
        all_dirs = sorted(path for path in family_root.iterdir() if path.is_dir())
        valid_skill_dirs = sorted(path for path in all_dirs if family.name_pattern.match(path.name))
        candidate_dirs = sorted(path for path in all_dirs if (path / "SKILL.md").exists())
        for skill_dir in candidate_dirs:
            if skill_dir not in valid_skill_dirs:
                if family.key == "deepsci" and skill_dir.name.startswith("isomer-rsch-"):
                    message = "legacy isomer-rsch-* skill folder must be renamed to isomer-deepsci-*"
                else:
                    message = f"skill folder '{skill_dir.name}' in {family.root_name}/ must match {family.name_shape}"
                add(
                    diagnostics,
                    repo_root,
                    skill_dir,
                    1,
                    "RPS007",
                    message,
                )
        actual_names = {path.name for path in valid_skill_dirs}
        for missing in sorted(family.expected_skills - actual_names):
            add(diagnostics, repo_root, family_root / missing, 1, "RPS007", f"expected {family.key} skill is missing")
        if family.key == "kaoju":
            for extra in sorted(actual_names - family.expected_skills):
                add(diagnostics, repo_root, family_root / extra, 1, "RPS007", f"unapproved Kaoju skill '{extra}' is active")
        for skill_dir in valid_skill_dirs:
            skill_dirs.append((skill_dir, family.key))

    if not any(generation == "deepsci" for _, generation in skill_dirs):
        add(diagnostics, repo_root, target, 1, "RPS007", "no production deepsci isomer-deepsci-* skill folders were found")
    for skill_dir, generation in skill_dirs:
        validate_skill_layout(skill_dir, repo_root, diagnostics, family_by_key[generation])
        validate_manifest(skill_dir, repo_root, diagnostics)
        validate_local_references(skill_dir, repo_root, diagnostics)
        if generation == "kaoju":
            validate_kaoju_direct_references(skill_dir, repo_root, diagnostics)

    documents = collect_documents(target, repo_root, file_roles)
    deepsci_identity_ids = validate_deepsci_identity_inventory(skill_dirs, repo_root, diagnostics)
    registry_path = target / "deepsci" / "isomer-deepsci-shared" / "references" / "tbd-surface-registry.md"
    if registry_path.exists():
        canonical_rows = parse_registry_rows(read_lines(registry_path))
    else:
        canonical_rows = {}
    registered_ids = set(canonical_rows)

    semantic_registry_path = target / "deepsci" / "isomer-deepsci-shared" / "references" / "semantic-placeholders.md"
    if semantic_registry_path.exists():
        semantic_placeholder_ids = set(parse_semantic_placeholder_ids(read_lines(semantic_registry_path)))
        deepsci_identity_ids.update(semantic_placeholder_ids)
    else:
        semantic_placeholder_ids = set()
        add(diagnostics, repo_root, semantic_registry_path, 1, "RPS009", "production DeepSci semantic-placeholder registry is missing")

    migration_placeholder_ids_by_skill: dict[str, set[str]] = {}
    for skill_dir, _generation in skill_dirs:
        rel_skill_dir = relpath(skill_dir, target)
        placeholder_path = skill_dir / "migrate" / "placeholders.md"
        if placeholder_path.exists():
            migration_placeholder_ids_by_skill[rel_skill_dir] = set(
                parse_migration_placeholder_ids(read_lines(placeholder_path))
            )
    migration_placeholder_ids_by_skill["__canonical_inventory__"] = set(deepsci_identity_ids)

    kaoju_identity_ids: set[str] = set()
    if (target / "kaoju").exists():
        try:
            kaoju_identity_ids = set(load_binding_registry())
        except (OSError, ValueError, json.JSONDecodeError):
            pass
    registered_by_family = {"deepsci": deepsci_identity_ids, "kaoju": kaoju_identity_ids}

    for document in documents:
        validate_tbd_placeholders(document, repo_root, diagnostics, registered_ids)
        validate_migration_placeholders(document, repo_root, diagnostics, migration_placeholder_ids_by_skill)
        validate_resolved_id_text(document, repo_root, diagnostics, allow_zones)
        validate_stale_terms(document, repo_root, diagnostics, allow_zones)
        validate_coupling_patterns(document, repo_root, diagnostics, allow_zones)
        validate_deepsci_storage_binding(document, repo_root, diagnostics, allow_zones)
        validate_deepsci_worker_output_policy(document, repo_root, diagnostics)
        validate_deepsci_latest_context_preflight(document, repo_root, diagnostics)
        validate_deepsci_display_contract_guidance(document, repo_root, diagnostics)
        validate_deepsci_support_section_intros(document, repo_root, diagnostics)
        validate_kaoju_active_guidance(document, repo_root, diagnostics)
        validate_artifact_identity_guidance(document, repo_root, diagnostics, registered_by_family)
    validate_deepsci_placeholder_bindings(skill_dirs, repo_root, diagnostics)
    validate_deepsci_payload_first_bindings(skill_dirs, repo_root, diagnostics)
    validate_workspace_manager_team_specialization_gate(target, repo_root, diagnostics)
    validate_registry_mirrors(documents, canonical_rows, repo_root, diagnostics)
    kaoju_root = target / "kaoju"
    if kaoju_root.exists():
        kaoju_contract = load_kaoju_process_contract(kaoju_root, repo_root, diagnostics)
        if kaoju_contract is not None:
            validate_kaoju_package_contract(kaoju_root, repo_root, diagnostics, kaoju_contract)
        validate_kaoju_command_surface(kaoju_root, repo_root, diagnostics)
        validate_kaoju_shared_references(kaoju_root, repo_root, diagnostics)
        validate_kaoju_artifact_bindings(kaoju_root, repo_root, diagnostics, family_by_key["kaoju"])
        validate_kaoju_architecture_guidance(kaoju_root, repo_root, diagnostics)
        validate_kaoju_resource_and_shared_routing(kaoju_root, repo_root, diagnostics)
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
