"""Topic Main Development Repository agent guidance helpers."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import resources
from pathlib import Path
import subprocess
from typing import Literal

from jinja2 import Environment, StrictUndefined

from isomer_labs.diagnostics import Diagnostic, has_errors


GUIDANCE_VERSION = "v1"
GUIDANCE_FENCE_TAG = "isomer-labs-topic-main-guidance"
GUIDANCE_BEGIN_MARKER = f"<!-- BEGIN isomer-labs-topic-main-guidance {GUIDANCE_VERSION} -->"
GUIDANCE_END_MARKER = f"<!-- END isomer-labs-topic-main-guidance {GUIDANCE_VERSION} -->"
GUIDANCE_MARKER_PREFIX = "<!-- BEGIN isomer-labs-topic-main-guidance "
GUIDANCE_TEMPLATE_RESOURCE = "assets/topic_main_guidance/isomer-labs-topic-main-guidance.v1.md.j2"
TARGET_FILENAMES = ("AGENTS.md", "CLAUDE.md")
PIXI_PYTHON_COMMAND = "pixi run --manifest-path <manifest_path> --environment <pixi_environment> python ..."
QUERY_COMMANDS = (
    "isomer-cli --print-json project self show",
    "isomer-cli --print-json project self identity",
    "isomer-cli --print-json project self pixi",
    "isomer-cli --print-json project self env",
    "isomer-cli --print-json project self paths <semantic-label>",
    "isomer-cli --print-json project context show",
    "isomer-cli --print-json project paths get <semantic-label>",
    "isomer-cli --print-json project paths explain <semantic-label>",
    "isomer-cli --print-json project topics list",
    "isomer-cli --print-json project topic-actors list",
)
SEMANTIC_LABELS = (
    "topic.repos.main",
    "topic.repos.main.isomer_managed",
    "topic.repos.main.projections.readonly",
    "topic.repos.main.projections.writable",
    "topic.records",
    "topic.runtime",
    "topic.actors.workspace",
    "agent.workspace",
)

GuidanceStatus = Literal["missing", "current", "stale", "duplicate", "malformed", "unknown_version", "unsafe"]
GuidanceAction = Literal["created", "appended", "updated", "unchanged", "blocked"]


@dataclass(frozen=True)
class GuidanceTarget:
    """Inspection or mutation result for one guidance file."""

    filename: str
    path: Path
    status: GuidanceStatus
    action: GuidanceAction = "unchanged"
    changed: bool = False
    message: str | None = None

    def to_json(self, repo_path: Path | None = None) -> dict[str, object]:
        data: dict[str, object] = {
            "filename": self.filename,
            "path": str(self.path),
            "status": self.status,
            "action": self.action,
            "changed": self.changed,
        }
        if repo_path is not None:
            try:
                data["relative_path"] = self.path.resolve(strict=False).relative_to(repo_path.resolve(strict=False)).as_posix()
            except ValueError:
                data["relative_path"] = self.filename
        if self.message is not None:
            data["message"] = self.message
        return data


def guidance_metadata() -> dict[str, object]:
    """Return stable metadata for the current guidance template."""

    return {
        "version": GUIDANCE_VERSION,
        "template_resource": GUIDANCE_TEMPLATE_RESOURCE,
        "begin_marker": GUIDANCE_BEGIN_MARKER,
        "end_marker": GUIDANCE_END_MARKER,
        "fence_tag": GUIDANCE_FENCE_TAG,
    }


def render_topic_main_guidance_block() -> str:
    """Render the canonical topic-main guidance block from the packaged template."""

    template_text = _template_text()
    env = Environment(undefined=StrictUndefined, autoescape=False, keep_trailing_newline=True)
    template = env.from_string(template_text)
    rendered = template.render(
        begin_marker=GUIDANCE_BEGIN_MARKER,
        end_marker=GUIDANCE_END_MARKER,
        fence_tag=GUIDANCE_FENCE_TAG,
        pixi_python_command=PIXI_PYTHON_COMMAND,
        query_commands=QUERY_COMMANDS,
        semantic_labels=SEMANTIC_LABELS,
        version=GUIDANCE_VERSION,
    )
    return rendered.rstrip() + "\n"


def inspect_topic_main_guidance_file(path: Path) -> GuidanceTarget:
    """Inspect one root guidance file without mutating it."""

    if not path.exists():
        return GuidanceTarget(filename=path.name, path=path, status="missing", message="File is missing.")
    if not path.is_file():
        return GuidanceTarget(filename=path.name, path=path, status="unsafe", message="Path exists but is not a file.")
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        return GuidanceTarget(filename=path.name, path=path, status="unsafe", message=str(exc))
    status, message = _classify_content(content)
    return GuidanceTarget(filename=path.name, path=path, status=status, message=message)


def upsert_topic_main_guidance_file(path: Path, rendered_block: str | None = None) -> GuidanceTarget:
    """Create, append, or update one guidance file while preserving owner content."""

    rendered = rendered_block or render_topic_main_guidance_block()
    target = inspect_topic_main_guidance_file(path)
    if target.status in {"duplicate", "malformed", "unknown_version", "unsafe"}:
        return GuidanceTarget(
            filename=path.name,
            path=path,
            status=target.status,
            action="blocked",
            changed=False,
            message=target.message,
        )
    if target.status == "missing":
        try:
            path.write_text(rendered, encoding="utf-8")
        except OSError as exc:
            return GuidanceTarget(filename=path.name, path=path, status="unsafe", action="blocked", message=str(exc))
        return GuidanceTarget(filename=path.name, path=path, status="current", action="created", changed=True)
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        return GuidanceTarget(filename=path.name, path=path, status="unsafe", action="blocked", message=str(exc))
    if target.status == "current":
        return GuidanceTarget(filename=path.name, path=path, status="current", action="unchanged")
    if _has_current_markers(content):
        new_content = _replace_current_block(content, rendered)
        action: GuidanceAction = "updated"
    else:
        if content and not content.endswith("\n"):
            separator = "\n\n"
        elif content:
            separator = "\n"
        else:
            separator = ""
        new_content = f"{content}{separator}{rendered}"
        action = "appended"
    try:
        path.write_text(new_content, encoding="utf-8")
    except OSError as exc:
        return GuidanceTarget(filename=path.name, path=path, status="unsafe", action="blocked", message=str(exc))
    return GuidanceTarget(filename=path.name, path=path, status="current", action=action, changed=True)


def inspect_topic_main_guidance(repo_path: Path) -> tuple[dict[str, object], list[Diagnostic]]:
    """Inspect guidance files for an existing topic-main repository."""

    repo_diagnostics = validate_topic_main_repo(repo_path)
    targets = [inspect_topic_main_guidance_file(repo_path / filename) for filename in TARGET_FILENAMES] if not has_errors(repo_diagnostics) else []
    payload = _payload(repo_path, targets=targets, mutated=False, changed_files=[])
    return payload, repo_diagnostics


def ensure_topic_main_guidance(repo_path: Path) -> tuple[dict[str, object], list[Diagnostic]]:
    """Ensure guidance files exist and contain the current rendered block."""

    repo_diagnostics = validate_topic_main_repo(repo_path)
    if has_errors(repo_diagnostics):
        return _payload(repo_path, targets=[], mutated=False, changed_files=[]), repo_diagnostics
    rendered = render_topic_main_guidance_block()
    targets = [upsert_topic_main_guidance_file(repo_path / filename, rendered) for filename in TARGET_FILENAMES]
    changed_files = [target.filename for target in targets if target.changed]
    diagnostics = [
        _blocked_target_diagnostic(repo_path, target)
        for target in targets
        if target.action == "blocked" or target.status in {"duplicate", "malformed", "unknown_version", "unsafe"}
    ]
    payload = _payload(repo_path, targets=targets, mutated=bool(changed_files), changed_files=changed_files)
    return payload, diagnostics


def validate_topic_main_repo(repo_path: Path) -> list[Diagnostic]:
    """Validate that repo_path is an existing safe normal non-bare Git repository."""

    diagnostics: list[Diagnostic] = []
    if not repo_path.exists():
        diagnostics.append(_repo_diagnostic(repo_path, "Resolved topic.repos.main does not exist."))
        return diagnostics
    if not repo_path.is_dir():
        diagnostics.append(_repo_diagnostic(repo_path, "Resolved topic.repos.main is not a directory."))
        return diagnostics
    try:
        inside = subprocess.run(
            ["git", "-C", str(repo_path), "rev-parse", "--is-inside-work-tree"],
            check=False,
            capture_output=True,
            text=True,
        )
        bare = subprocess.run(
            ["git", "-C", str(repo_path), "rev-parse", "--is-bare-repository"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        diagnostics.append(_repo_diagnostic(repo_path, f"Could not inspect Git repository: {exc}."))
        return diagnostics
    if inside.returncode != 0 or inside.stdout.strip() != "true":
        diagnostics.append(_repo_diagnostic(repo_path, "Resolved topic.repos.main is not a normal Git work tree."))
    if bare.returncode != 0 or bare.stdout.strip() == "true":
        diagnostics.append(_repo_diagnostic(repo_path, "Resolved topic.repos.main is bare or cannot report non-bare state."))
    return diagnostics


def _template_text() -> str:
    package_root = resources.files("isomer_labs")
    return package_root.joinpath(GUIDANCE_TEMPLATE_RESOURCE).read_text(encoding="utf-8")


def _payload(
    repo_path: Path | None,
    *,
    targets: list[GuidanceTarget],
    mutated: bool,
    changed_files: list[str],
) -> dict[str, object]:
    return {
        "ok": True,
        "mutated": mutated,
        "guidance": guidance_metadata(),
        "topic_main_repo": str(repo_path) if repo_path is not None else None,
        "targets": [target.to_json(repo_path) for target in targets],
        "changed_files": changed_files,
    }


def _classify_content(content: str) -> tuple[GuidanceStatus, str | None]:
    if content.count(GUIDANCE_BEGIN_MARKER) > 1 or content.count(GUIDANCE_END_MARKER) > 1:
        return "duplicate", "File contains duplicate current Isomer guidance markers."
    if GUIDANCE_MARKER_PREFIX in content and GUIDANCE_BEGIN_MARKER not in content:
        return "unknown_version", "File contains an Isomer topic-main guidance block with an unknown version."
    begin_count = content.count(GUIDANCE_BEGIN_MARKER)
    end_count = content.count(GUIDANCE_END_MARKER)
    if begin_count != end_count:
        return "malformed", "File contains unmatched Isomer guidance markers."
    if begin_count == 0:
        return "stale", "File does not contain the current Isomer guidance block."
    if content.index(GUIDANCE_BEGIN_MARKER) > content.index(GUIDANCE_END_MARKER):
        return "malformed", "File contains Isomer guidance markers in the wrong order."
    block = _extract_current_block(content)
    if block is None:
        return "malformed", "File contains malformed Isomer guidance markers."
    if block.rstrip() + "\n" == render_topic_main_guidance_block():
        return "current", None
    return "stale", "File contains a stale Isomer guidance block."


def _has_current_markers(content: str) -> bool:
    return GUIDANCE_BEGIN_MARKER in content and GUIDANCE_END_MARKER in content


def _extract_current_block(content: str) -> str | None:
    begin_index = content.find(GUIDANCE_BEGIN_MARKER)
    end_index = content.find(GUIDANCE_END_MARKER)
    if begin_index < 0 or end_index < 0 or end_index < begin_index:
        return None
    return content[begin_index : end_index + len(GUIDANCE_END_MARKER)]


def _replace_current_block(content: str, rendered_block: str) -> str:
    begin_index = content.index(GUIDANCE_BEGIN_MARKER)
    end_index = content.index(GUIDANCE_END_MARKER) + len(GUIDANCE_END_MARKER)
    replacement = rendered_block.rstrip()
    return f"{content[:begin_index]}{replacement}{content[end_index:]}"


def _repo_diagnostic(repo_path: Path, message: str) -> Diagnostic:
    return Diagnostic(
        code="ISO085",
        severity="error",
        concept="Topic Main Guidance",
        path=repo_path,
        field="topic.repos.main",
        message=message,
        hint="Prepare topic.repos.main through the topic-main setup workflow before running topic-main guidance ensure.",
    )


def _blocked_target_diagnostic(repo_path: Path, target: GuidanceTarget) -> Diagnostic:
    return Diagnostic(
        code="ISO086",
        severity="error",
        concept="Topic Main Guidance",
        path=target.path,
        field=target.filename,
        message=target.message or f"Cannot update {target.filename} because its guidance status is {target.status}.",
        hint=f"Repair {target.filename} in {repo_path} manually or remove malformed Isomer guidance markers before rerunning ensure.",
    )
