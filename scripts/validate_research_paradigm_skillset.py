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
REGISTRY_ROW_ID_RE = re.compile(r"^(?:path|api|schema|policy|provider)-[a-z0-9-]+$")

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
    ),
    "resolved_id_file_globs": (
        "isomer-rsch-shared/references/tbd-surface-registry.md",
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
}

LOCAL_REFERENCE_PREFIXES = ("references/", "assets/", "scripts/")


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


def classify_document(rel_target: str, lines: tuple[str, ...]) -> frozenset[str]:
    roles: set[str] = set()
    if rel_target == "PROVENANCE.md" or fnmatch.fnmatch(rel_target, "*/references/provenance.md"):
        roles.add("provenance")
    if fnmatch.fnmatch(rel_target, "licenses/*.md"):
        roles.add("license")
    if fnmatch.fnmatch(rel_target, "*/references/deferred-*.md") or rel_target.endswith(
        "references/package-index-decision.md"
    ):
        roles.add("deferred-resource")
    if rel_target.endswith("references/source-term-mapping.md"):
        roles.add("source-term-mapping")
    if rel_target == "isomer-rsch-shared/references/tbd-surface-registry.md":
        roles.add("canonical-registry")
    if any(normalize_heading(line.removeprefix("##")) == "TBD Surface Registry" for line in lines if line.startswith("##")):
        roles.add("registry-mirror")
    if not roles:
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


def collect_documents(target: Path, repo_root: Path) -> list[Document]:
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
                roles=classify_document(rel_target, lines),
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


def validate_skill_layout(skill_dir: Path, repo_root: Path, diagnostics: list[Diagnostic]) -> None:
    skill_name = skill_dir.name
    if not SKILL_NAME_RE.match(skill_name):
        add(diagnostics, repo_root, skill_dir, 1, "RPS007", f"skill folder '{skill_name}' must match isomer-rsch-*")

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
        if workflow_line > 30:
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
    canonical_path = "isomer-rsch-shared/references/tbd-surface-registry.md"
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


def validate_resolved_id_text(
    document: Document,
    repo_root: Path,
    diagnostics: list[Diagnostic],
    allow_zones: dict[str, tuple[str, ...]],
) -> None:
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


def validate_skillset(target: Path, repo_root: Path | None = None) -> list[Diagnostic]:
    target = target.resolve()
    repo_root = (repo_root or find_repo_root(target)).resolve()
    diagnostics: list[Diagnostic] = []
    if not target.exists():
        diagnostics.append(Diagnostic(relpath(target, repo_root), 1, "RPS000", "skillset path does not exist"))
        return diagnostics

    allow_zones = load_allow_zones(target)
    skill_dirs = sorted(path for path in target.iterdir() if path.is_dir() and path.name.startswith("isomer-rsch-"))
    if not skill_dirs:
        add(diagnostics, repo_root, target, 1, "RPS007", "no isomer-rsch-* skill folders were found")
    for skill_dir in skill_dirs:
        validate_skill_layout(skill_dir, repo_root, diagnostics)
        validate_manifest(skill_dir, repo_root, diagnostics)
        validate_local_references(skill_dir, repo_root, diagnostics)

    documents = collect_documents(target, repo_root)
    registry_path = target / "isomer-rsch-shared" / "references" / "tbd-surface-registry.md"
    if registry_path.exists():
        canonical_rows = parse_registry_rows(read_lines(registry_path))
    else:
        canonical_rows = {}
        add(diagnostics, repo_root, registry_path, 1, "RPS003", "canonical shared TBD registry is missing")
    registered_ids = set(canonical_rows)

    for document in documents:
        validate_tbd_placeholders(document, repo_root, diagnostics, registered_ids)
        validate_resolved_id_text(document, repo_root, diagnostics, allow_zones)
        validate_stale_terms(document, repo_root, diagnostics, allow_zones)
        validate_coupling_patterns(document, repo_root, diagnostics, allow_zones)
    validate_registry_mirrors(documents, canonical_rows, repo_root, diagnostics)
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
