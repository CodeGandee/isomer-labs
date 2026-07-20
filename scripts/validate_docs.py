#!/usr/bin/env python3
"""Repository-local documentation validation for Isomer Labs."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from pathlib import Path

from isomer_labs.cli.examples import COMMAND_EXAMPLES
from isomer_labs.skills.system_assets import system_skill_catalog


REQUIRED_PAGES = [
    "docs/index.md",
    "docs/tutorial/index.md",
    "docs/tutorial/quickstart.md",
    "docs/tutorial/first-project.md",
    "docs/tutorial/author-research-intent.md",
    "docs/tutorial/prepare-topic-environment.md",
    "docs/tutorial/run-a-human-steered-research-pass.md",
    "docs/tutorial/validate-with-real-evidence.md",
    "docs/tutorial/develop-a-white-box-model.md",
    "docs/tutorial/write-and-inspect-a-paper.md",
    "docs/manual/index.md",
    "docs/manual/concepts.md",
    "docs/manual/cli-reference.md",
    "docs/manual/project-lifecycle.md",
    "docs/manual/topic-workspaces.md",
    "docs/manual/workspace-runtime.md",
    "docs/manual/research-records.md",
    "docs/manual/project-web.md",
    "docs/manual/houmao-adapter.md",
    "docs/manual/troubleshooting.md",
    "docs/developer/index.md",
    "docs/developer/architecture.md",
    "docs/developer/packaged-system-skills.md",
    "docs/developer/contributing-docs.md",
]

FORBIDDEN_TERMS: list[tuple[str, str]] = [
    ("quest", r"\bquest\b"),
    ("state of the art", r"state of the art"),
    ("research goal", r"research goal"),
    ("control plane", r"control plane"),
]

README_LINK_TARGETS = [
    "docs/index.md",
    "docs/tutorial/quickstart.md",
    "docs/manual/cli-reference.md",
    "docs/developer/index.md",
]
CLI_REFERENCE_PAGE = "docs/manual/cli-reference.md"
TOPIC_WORKSPACE_PAGE = "docs/manual/topic-workspaces.md"
SYSTEM_SKILL_SCOPE_PAGES = (
    "README.md",
    "docs/tutorial/quickstart.md",
    "docs/manual/cli-reference.md",
    "docs/developer/packaged-system-skills.md",
)
SYSTEM_SKILL_MODEL_PAGE = "docs/developer/packaged-system-skills.md"
SYSTEM_SKILL_STALE_SCOPE_TERMS = (
    "every target-resolving command requires",
    "every install, status, upgrade, and uninstall command requires",
    "the `install`, `status`, `upgrade`, and `uninstall` commands require",
    "the target-resolving commands `install`, `status`, `upgrade`, and `uninstall` require",
)
STALE_ISOMER_JSON_PATTERNS = [
    re.compile(r"\bisomer-cli\b[^\n]*\s--json\b"),
    re.compile(r"\bisomer-cli\b[^\n]*\s--format(?:=|\s+)json\b"),
    re.compile(r"^\s*--json\s*$"),
]
LEGACY_WORKSPACE_PATTERNS = [
    ("legacy support root", re.compile(r"\.isomer-agent/")),
    (
        "legacy top-level topic-main collaboration path",
        re.compile(r"\brepos/topic-main/(?:shared|artifacts|tasks|runs|views|logs|tools)\b"),
    ),
]
BREAKING_LAYOUT_NOTE_TERMS = ("legacy", "breaking", "break", "diagnostic", "compatibility")
SEMANTIC_PATH_COMMANDS = (
    "project paths default",
    "project paths explain",
    "project paths get",
    "project paths list",
    "project paths materialize",
    "project paths materialize-default",
    "project paths register",
    "project paths reset",
    "project paths unregister",
    "project paths update",
    "project repos create",
    "project repos register",
)
FIXED_PATH_ONLY_PATTERNS = [
    ("fixed agent workspace path", re.compile(r"\b(always|must|only)\b[^\n]*(?:agents/<agent-name>|<topic-workspace>/agents)", re.IGNORECASE)),
    ("fixed topic main path", re.compile(r"\b(always|must|only)\b[^\n]*repos/topic-main", re.IGNORECASE)),
]
REPOSITORY_BOUNDARY_EXACT_PATTERNS = (
    ("removed repository command", re.compile(r"\bproject\s+repos\s+acquire\b", re.IGNORECASE)),
    ("removed repository extension point", re.compile(r"\brepository_" r"acquisition\b")),
    ("removed Kaoju repository service", re.compile(r"\bKaojuRepository" r"Service\b")),
    ("removed repository acquisition service", re.compile(r"\brepository acquisition service\b", re.IGNORECASE)),
)
REPOSITORY_BOUNDARY_CONTEXT_PATTERNS = (
    (
        "fixed Isomer repository clone promise",
        re.compile(
            r"(?:\bIsomer\b|isomer-cli|repository service).{0,120}(?:runs?|executes?|performs?|owns?|will|must).{0,80}"
            r"(?:git\s+(?:clone|fetch|pull|checkout|submodule|lfs)|(?:clone|fetch|pull|checkout)s?\s+(?:the\s+)?repo)",
            re.IGNORECASE,
        ),
    ),
    (
        "mandatory fixed shallow-clone policy",
        re.compile(
            r"(?:default(?:s|ing)?\s+to|must\s+use|always\s+use).{0,100}"
            r"(?:shallow|--depth[ =]?1|depth\s+one)|(?:--depth[ =]?1|depth\s+one).{0,100}"
            r"(?:default|canonical|mandatory)",
            re.IGNORECASE,
        ),
    ),
    (
        "repository registration before verification",
        re.compile(
            r"(?:register|create (?:the )?binding).{0,100}"
            r"before.{0,100}(?:verify|clone|acquir|copy|extract)|first.{0,60}"
            r"register.{0,100}"
            r"(?:then|before).{0,100}(?:clone|acquir|verify|copy|extract)",
            re.IGNORECASE,
        ),
    ),
    (
        "Isomer-owned partial repository cleanup",
        re.compile(
            r"(?:\bIsomer\b|isomer-cli|repository service).{0,100}(?:clean|remove|delete|repair|roll back).{0,100}"
            r"(?:partial|checkout|clone|repository)",
            re.IGNORECASE,
        ),
    ),
)
DEFAULT_CLI_HELP_WORKERS = min(8, os.cpu_count() or 1)


def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def iter_docs_markdown(repo_root: Path) -> list[Path]:
    return sorted((repo_root / "docs").glob("**/*.md"))


def run_cli_help(args: list[str]) -> str:
    argv = [sys.executable, "-m", "isomer_labs", *args, "--help"]
    completed = subprocess.run(argv, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        return ""
    return completed.stdout


def _command_name(line: str) -> str | None:
    match = re.match(r"^  (\S+)", line)
    return match.group(1) if match else None


def _command_names(help_text: str) -> list[str]:
    names: list[str] = []
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
            names.append(name)
    return names


def collect_cli_commands(
    base_args: list[str],
    help_text: str,
    executor: ThreadPoolExecutor | None = None,
) -> list[str]:
    commands: list[str] = []
    names = _command_names(help_text)
    if not names:
        return commands

    root_path = tuple(base_args)
    if executor is not None:
        children_by_path: dict[tuple[str, ...], list[str]] = {root_path: names}
        pending: dict[Future[str], tuple[str, ...]] = {}

        def submit_help(path: tuple[str, ...]) -> None:
            pending[executor.submit(run_cli_help, list(path))] = path

        for name in names:
            submit_help(root_path + (name,))

        while pending:
            completed, _ = wait(pending, return_when=FIRST_COMPLETED)
            for future in completed:
                path = pending.pop(future)
                child_names = _command_names(future.result())
                if not child_names:
                    continue
                children_by_path[path] = child_names
                for child_name in child_names:
                    submit_help(path + (child_name,))

        return _render_cli_commands(root_path, children_by_path)

    sub_args_by_name = [(name, base_args + [name]) for name in names]
    help_by_name = [(name, run_cli_help(sub_args)) for name, sub_args in sub_args_by_name]
    for name, sub_help in help_by_name:
        sub_args = base_args + [name]
        if "Commands:" in sub_help:
            commands.extend(collect_cli_commands(sub_args, sub_help, executor))
        else:
            commands.append(" ".join(sub_args))
    return commands


def _render_cli_commands(
    base_args: tuple[str, ...],
    children_by_path: dict[tuple[str, ...], list[str]],
) -> list[str]:
    commands: list[str] = []
    for name in children_by_path.get(base_args, []):
        path = base_args + (name,)
        if path in children_by_path:
            commands.extend(_render_cli_commands(path, children_by_path))
        else:
            commands.append(" ".join(path))
    return commands


def get_public_commands(max_workers: int = DEFAULT_CLI_HELP_WORKERS) -> list[str]:
    top_help = run_cli_help([])
    if not top_help:
        return []
    if max_workers <= 1:
        return collect_cli_commands([], top_help)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        return collect_cli_commands([], top_help, executor)


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
        expected = ", ".join(README_LINK_TARGETS)
        return [f"README.md does not link to one of the required docs targets: {expected}"]
    return []


def check_cli_coverage(repo_root: Path, commands: list[str]) -> list[str]:
    cli_doc = repo_root / CLI_REFERENCE_PAGE
    if not cli_doc.is_file():
        return [f"{CLI_REFERENCE_PAGE} is missing"]
    content = cli_doc.read_text(encoding="utf-8")
    issues: list[str] = []
    for command in commands:
        if command not in content:
            issues.append(f"{CLI_REFERENCE_PAGE} missing command: {command}")
    return issues


def _without_inline_code(content: str) -> str:
    """Return content with inline code spans replaced by spaces of equal length."""
    return re.sub(r"`[^`]*`", lambda match: " " * len(match.group(0)), content)


def check_forbidden_terms(repo_root: Path) -> list[str]:
    issues: list[str] = []
    for path in iter_docs_markdown(repo_root):
        content = path.read_text(encoding="utf-8")
        searchable = _without_inline_code(content)
        for label, pattern in FORBIDDEN_TERMS:
            for match in re.finditer(pattern, searchable, flags=re.IGNORECASE):
                line_number = content[: match.start()].count("\n") + 1
                issues.append(f"{path.relative_to(repo_root)}:{line_number}: forbidden term '{label}'")
    return issues


def check_stale_isomer_cli_json_examples(repo_root: Path) -> list[str]:
    issues: list[str] = []
    paths = [repo_root / "README.md", *iter_docs_markdown(repo_root)]
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


def check_system_skill_scope_documentation(repo_root: Path) -> list[str]:
    issues: list[str] = []
    for relative in SYSTEM_SKILL_SCOPE_PAGES:
        path = repo_root / relative
        if not path.is_file():
            continue
        content = path.read_text(encoding="utf-8")
        install_lines = [line for line in content.splitlines() if "isomer-cli system-skills install --target" in line]
        if not any("--scope" not in line for line in install_lines):
            issues.append(f"{relative} must include a Project-default system-skills install example without --scope")
        if not any("--scope user" in line for line in install_lines):
            issues.append(f"{relative} must include an explicit user-scoped system-skills install example")
        for term in ("`--scope` is omitted", "defaults to Project scope", "require an explicit `--scope user|project`"):
            if term not in content:
                issues.append(f"{relative} missing system-skill scope guidance: {term}")
        lowered = content.lower()
        for stale_term in SYSTEM_SKILL_STALE_SCOPE_TERMS:
            if stale_term in lowered:
                issues.append(f"{relative} contains stale universal system-skill scope guidance: {stale_term}")
    return issues


def check_system_skill_manifest_documentation(repo_root: Path) -> list[str]:
    """Check public skill examples and role documentation against manifest v4."""

    catalog = system_skill_catalog()
    model_path = repo_root / SYSTEM_SKILL_MODEL_PAGE
    if not model_path.is_file():
        return [f"{SYSTEM_SKILL_MODEL_PAGE} is missing"]

    issues: list[str] = []
    model_content = model_path.read_text(encoding="utf-8")
    model_lines = model_content.splitlines()
    if catalog.schema_version not in model_content:
        issues.append(f"{SYSTEM_SKILL_MODEL_PAGE} must name current schema {catalog.schema_version}")
    for heading in ("Public Welcome", "Execution Entrypoint"):
        if heading not in model_content:
            issues.append(f"{SYSTEM_SKILL_MODEL_PAGE} missing public role heading: {heading}")
    for pack in catalog.packs:
        welcome = pack.welcome
        if welcome is None:
            issues.append(f"Manifest pack {pack.pack_id} has no welcome role to document")
            continue
        if not any(welcome.name in line and pack.entry_skill in line for line in model_lines):
            issues.append(
                f"{SYSTEM_SKILL_MODEL_PAGE} must document {welcome.name} and {pack.entry_skill} as one public pair"
            )

    public_by_name = {
        public.name: public
        for pack in catalog.packs
        for public in pack.public_skills
    }
    protected_names = {capability.logical_id for capability in catalog.capabilities}
    public_pattern = "|".join(re.escape(name) for name in sorted(public_by_name, key=len, reverse=True))
    command_pattern = re.compile(rf"\$({public_pattern})\s+use\s+([a-z0-9][a-z0-9-]*|<subcommand>)")
    direct_skill_pattern = re.compile(r"\$(isomer-[a-z0-9][a-z0-9-]*)")
    paths = [repo_root / "README.md", *iter_docs_markdown(repo_root)]
    seen_public: set[str] = set()
    for path in paths:
        if not path.is_file():
            continue
        content = path.read_text(encoding="utf-8")
        relative = path.relative_to(repo_root)
        for line_number, line in enumerate(content.splitlines(), start=1):
            for match in direct_skill_pattern.finditer(line):
                name = match.group(1)
                if name in public_by_name:
                    seen_public.add(name)
                elif name in protected_names:
                    issues.append(
                        f"{relative}:{line_number}: protected skill {name} must not be shown as a direct $ invocation"
                    )
            if "isomer-op-entrypoint->welcome" in line:
                issues.append(f"{relative}:{line_number}: retired protected welcome designator")
            for match in command_pattern.finditer(line):
                name, command = match.groups()
                if command == "<subcommand>":
                    continue
                if command not in public_by_name[name].public_commands:
                    issues.append(
                        f"{relative}:{line_number}: {command!r} is not a manifest v4 public command of {name}"
                    )
    for name in sorted(public_by_name):
        if name not in seen_public:
            issues.append(f"Documentation does not include a public invocation for manifest skill {name}")
    return issues


def check_cli_error_example_registry(repo_root: Path) -> list[str]:
    cli_doc = repo_root / CLI_REFERENCE_PAGE
    if not cli_doc.is_file():
        return [f"{CLI_REFERENCE_PAGE} is missing"]
    content = cli_doc.read_text(encoding="utf-8")
    issues: list[str] = []
    for command, examples in sorted(COMMAND_EXAMPLES.items()):
        for example in examples:
            if example not in content:
                issues.append(f"{CLI_REFERENCE_PAGE} missing CLI error example for `{command}`: {example}")
    return issues


def check_legacy_workspace_paths(repo_root: Path) -> list[str]:
    issues: list[str] = []
    paths = [repo_root / "README.md", *iter_docs_markdown(repo_root)]
    for path in paths:
        if not path.is_file():
            continue
        content = path.read_text(encoding="utf-8")
        breaking_layout_context = False
        for line_number, line in enumerate(content.splitlines(), start=1):
            if line.startswith("## "):
                breaking_layout_context = any(term in line.lower() for term in BREAKING_LAYOUT_NOTE_TERMS)
            is_breaking_layout_note = breaking_layout_context or any(term in line.lower() for term in BREAKING_LAYOUT_NOTE_TERMS)
            for label, pattern in LEGACY_WORKSPACE_PATTERNS:
                if pattern.search(line) and not is_breaking_layout_note:
                    issues.append(
                        f"{path.relative_to(repo_root)}:{line_number}: stale workspace layout language uses {label}; use isomer-managed/ or explicit breaking-layout diagnostics"
                    )
    return issues


def check_semantic_path_documentation(repo_root: Path) -> list[str]:
    issues: list[str] = []
    cli_doc = repo_root / CLI_REFERENCE_PAGE
    if cli_doc.is_file():
        content = cli_doc.read_text(encoding="utf-8")
        for command in SEMANTIC_PATH_COMMANDS:
            if command not in content:
                issues.append(f"{CLI_REFERENCE_PAGE} missing semantic path command coverage: {command}")
    topic_doc = repo_root / TOPIC_WORKSPACE_PAGE
    if topic_doc.is_file():
        content = topic_doc.read_text(encoding="utf-8")
        if "topic-workspace.toml" not in content or "isomer-default.v1" not in content:
            issues.append(f"{TOPIC_WORKSPACE_PAGE} must document Topic Workspace Manifest, topic-workspace.toml, and isomer-default.v1")
        for term in ("storage_profile", "custom.*", "topic.repos.<group...>.<repo-name>", "label", "path"):
            if term not in content:
                issues.append(f"{TOPIC_WORKSPACE_PAGE} missing storage contract term: {term}")
    cli_doc = repo_root / CLI_REFERENCE_PAGE
    if cli_doc.is_file():
        content = cli_doc.read_text(encoding="utf-8")
        for term in ("--storage-profile", "ISOMER_PATH__TOPIC__REPOS__MAIN", "ISOMER_PATH__CUSTOM__DATASETS__RAW", "--configured"):
            if term not in content:
                issues.append(f"{CLI_REFERENCE_PAGE} missing semantic storage CLI term: {term}")
    for path in [repo_root / "README.md", *iter_docs_markdown(repo_root)]:
        if not path.is_file():
            continue
        content = path.read_text(encoding="utf-8")
        for line_number, line in enumerate(content.splitlines(), start=1):
            for label, pattern in FIXED_PATH_ONLY_PATTERNS:
                if pattern.search(line) and "default" not in line.lower() and "isomer-default.v1" not in line:
                    issues.append(
                        f"{path.relative_to(repo_root)}:{line_number}: stale fixed-path-only wording uses {label}; name the semantic label and default binding"
                    )
        if "tmp/" in content:
            lowered = content.lower()
            if not (
                "topic.tmp" in content
                and "topic.repos.main.tmp" in content
                and "agent.tmp" in content
                and "disposable" in lowered
                and "not durable" in lowered
            ):
                issues.append(
                    f"{path.relative_to(repo_root)}: tmp/ wording must describe semantic labels and local, ignored, disposable, not durable semantics"
                )
    return issues


def check_external_repository_boundary(repo_root: Path) -> list[str]:
    """Reject docs that assign external repository execution or cleanup to Isomer."""

    issues: list[str] = []
    paths = [repo_root / "README.md", *iter_docs_markdown(repo_root)]
    for path in paths:
        if not path.is_file():
            continue
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            for label, pattern in REPOSITORY_BOUNDARY_EXACT_PATTERNS:
                if pattern.search(line):
                    issues.append(f"{path.relative_to(repo_root)}:{line_number}: repository boundary violation: {label}")
            if _repository_boundary_rejection_line(line):
                continue
            for label, pattern in REPOSITORY_BOUNDARY_CONTEXT_PATTERNS:
                if pattern.search(line):
                    issues.append(f"{path.relative_to(repo_root)}:{line_number}: repository boundary violation: {label}")
    return issues


def _repository_boundary_rejection_line(line: str) -> bool:
    lowered = line.casefold()
    return any(
        marker in lowered
        for marker in (
            "does not ",
            "do not ",
            "never ",
            "not an isomer",
            "outside isomer",
            "outside `isomer-cli`",
            "external command",
            "externally acquired",
            "user or agent",
            "user-controlled or agent-controlled",
        )
    )


def validate_docs(repo_root: Path, cli_help_workers: int = DEFAULT_CLI_HELP_WORKERS) -> list[str]:
    issues: list[str] = []
    issues.extend(check_required_pages(repo_root))
    issues.extend(check_readme_links(repo_root))
    commands = get_public_commands(max_workers=cli_help_workers)
    if not commands:
        issues.append("Could not discover public isomer-cli commands")
    else:
        issues.extend(check_cli_coverage(repo_root, commands))
    issues.extend(check_stale_isomer_cli_json_examples(repo_root))
    issues.extend(check_system_skill_scope_documentation(repo_root))
    issues.extend(check_system_skill_manifest_documentation(repo_root))
    issues.extend(check_cli_error_example_registry(repo_root))
    issues.extend(check_legacy_workspace_paths(repo_root))
    issues.extend(check_semantic_path_documentation(repo_root))
    issues.extend(check_external_repository_boundary(repo_root))
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
    parser.add_argument(
        "--cli-help-workers",
        type=int,
        default=DEFAULT_CLI_HELP_WORKERS,
        help="Maximum parallel workers for isomer-cli help discovery.",
    )
    args = parser.parse_args()

    issues = validate_docs(args.repo_root, cli_help_workers=max(1, args.cli_help_workers))
    if issues:
        print("Documentation validation failed:", file=sys.stderr)
        for issue in issues:
            print(f"  - {issue}", file=sys.stderr)
        return 1

    print("Documentation validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
