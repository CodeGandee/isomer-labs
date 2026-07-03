"""Project-scoped cleanup planning and execution."""

from __future__ import annotations

from dataclasses import dataclass, replace
import shutil
from pathlib import Path

from isomer_labs.workspace.layout import content_root_path, selected_content_root_path
from isomer_labs.project.context import resolve_topic_workspace
from isomer_labs.core.diagnostics import Diagnostic, has_errors
from isomer_labs.houmao.manifests import ADAPTER_MANIFEST_ROOT
from isomer_labs.project.manifest import parse_project_manifest
from isomer_labs.models import Project
from isomer_labs.core.path_utils import canonicalize, display_path, is_within
from isomer_labs.project import (
    config_dir_for_root,
    find_ancestor_manifest,
    houmao_overlay_dir_for_root,
    manifest_path_for_root,
    project_root_for_manifest,
    root_houmao_overlay_dir_for_root,
)
from isomer_labs.runtime.models import RUNTIME_DIRECTORIES
from isomer_labs.core.toml_loader import load_toml


CLEANUP_PARTS = (
    "bootstrap",
    "project-config",
    "houmao-overlay",
    "content-policy",
    "topic-workspace",
    "runtime",
    "content-root",
)
RUNTIME_DB_FILENAME = "state.sqlite"
CONTENT_POLICY_FILES = ("README.md", ".gitignore")


@dataclass(frozen=True)
class CleanupTarget:
    part: str
    path: Path
    action: str
    target_kind: str
    exists: bool
    status: str
    warnings: tuple[str, ...] = ()
    reason: str | None = None

    @property
    def removable(self) -> bool:
        return self.status in {"planned", "absent"}

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "part": self.part,
            "path": str(self.path),
            "action": self.action,
            "target_kind": self.target_kind,
            "exists": self.exists,
            "status": self.status,
        }
        if self.reason is not None:
            data["reason"] = self.reason
        if self.warnings:
            data["warnings"] = list(self.warnings)
        return data


@dataclass(frozen=True)
class CleanupPlan:
    project_root: Path
    manifest_path: Path
    authority: str
    selected_parts: tuple[str, ...]
    selected_topics: tuple[str, ...]
    all_topics: bool
    content_root: Path
    dry_run: bool
    confirmation_required: bool
    purge_content_root: bool
    targets: tuple[CleanupTarget, ...]
    diagnostics: tuple[Diagnostic, ...]

    @property
    def ok(self) -> bool:
        return not has_errors(list(self.diagnostics))

    @property
    def can_execute(self) -> bool:
        return self.ok and all(target.removable for target in self.targets)

    def to_json(self) -> dict[str, object]:
        return {
            "project_root": str(self.project_root),
            "project_manifest_path": str(self.manifest_path),
            "authority": self.authority,
            "selected_parts": list(self.selected_parts),
            "selected_topics": list(self.selected_topics),
            "all_topics": self.all_topics,
            "content_root_path": str(self.content_root),
            "dry_run": self.dry_run,
            "confirmation_required": self.confirmation_required,
            "purge_content_root": self.purge_content_root,
            "targets": [target.to_json() for target in self.targets],
        }


@dataclass(frozen=True)
class CleanupExecution:
    plan: CleanupPlan
    removed_targets: tuple[CleanupTarget, ...]
    skipped_targets: tuple[CleanupTarget, ...]
    diagnostics: tuple[Diagnostic, ...]
    mutated: bool

    @property
    def ok(self) -> bool:
        return not has_errors(list(self.diagnostics))

    def to_json(self) -> dict[str, object]:
        return {
            "ok": self.ok,
            "mutated": self.mutated,
            "project_root": str(self.plan.project_root),
            "project_manifest_path": str(self.plan.manifest_path),
            "authority": self.plan.authority,
            "selected_parts": list(self.plan.selected_parts),
            "selected_topics": list(self.plan.selected_topics),
            "all_topics": self.plan.all_topics,
            "content_root_path": str(self.plan.content_root),
            "dry_run": self.plan.dry_run,
            "confirmation_required": self.plan.confirmation_required,
            "purge_content_root": self.plan.purge_content_root,
            "cleanup": self.plan.to_json(),
            "planned_removals": [target.to_json() for target in self.plan.targets],
            "removed_targets": [target.to_json() for target in self.removed_targets],
            "skipped_targets": [target.to_json() for target in self.skipped_targets],
        }


def plan_project_cleanup(
    *,
    cwd: Path,
    project_selector: str | None = None,
    manifest_selector: str | None = None,
    parts: tuple[str, ...],
    topics: tuple[str, ...] = (),
    all_topics: bool = False,
    content_dir: str | None = None,
    purge_content_root: bool = False,
    dry_run: bool = False,
    yes: bool = False,
) -> CleanupPlan:
    project, root, manifest_path, authority, authority_diagnostics = _load_cleanup_authority(
        cwd=cwd,
        project_selector=project_selector,
        manifest_selector=manifest_selector,
    )
    effective_dry_run = dry_run or not yes
    selected_parts = _dedupe(parts)
    diagnostics = list(authority_diagnostics)

    if not selected_parts:
        diagnostics.append(
            Diagnostic(
                code="ISO003",
                severity="error",
                concept="Project cleanup",
                field="part",
                message="Select at least one cleanup part with --part <part>.",
            )
        )
    unknown_parts = tuple(part for part in selected_parts if part not in CLEANUP_PARTS)
    for part in unknown_parts:
        diagnostics.append(
            Diagnostic(
                code="ISO003",
                severity="error",
                concept="Project cleanup",
                field="part",
                message=f"Unknown cleanup part: {part}.",
            )
        )
    if all_topics and topics:
        diagnostics.append(
            Diagnostic(
                code="ISO003",
                severity="error",
                concept="Project cleanup",
                field="topic",
                message="Use either --topic or --all-topics for topic-scoped cleanup, not both.",
            )
        )

    content_root = _cleanup_content_root(root, project, content_dir)
    workspace_topics = _selected_cleanup_topics(project, selected_parts, topics, all_topics, diagnostics)

    targets: list[CleanupTarget] = []
    expanded_parts = _expand_parts(selected_parts)
    if "project-config" in expanded_parts:
        targets.append(_target("project-config", config_dir_for_root(root), root=root))
    if "houmao-overlay" in expanded_parts:
        targets.append(_target("houmao-overlay", houmao_overlay_dir_for_root(root), root=root))
    if "content-policy" in expanded_parts:
        targets.extend(_target("content-policy", content_root / file_name, root=root) for file_name in CONTENT_POLICY_FILES)
    if "topic-workspace" in expanded_parts:
        targets.extend(_topic_workspace_targets(root, project, workspace_topics, diagnostics))
    if "runtime" in expanded_parts:
        targets.extend(_runtime_targets(root, project, workspace_topics, diagnostics))
    if "content-root" in expanded_parts:
        targets.append(_content_root_target(content_root, root, purge_content_root))

    plan = CleanupPlan(
        project_root=root,
        manifest_path=manifest_path,
        authority=authority,
        selected_parts=selected_parts,
        selected_topics=workspace_topics,
        all_topics=all_topics,
        content_root=content_root,
        dry_run=effective_dry_run,
        confirmation_required=not yes,
        purge_content_root=purge_content_root,
        targets=tuple(_dedupe_targets(targets)),
        diagnostics=tuple(diagnostics),
    )
    safety_diagnostics, safety_targets = _validate_targets(plan)
    return replace(plan, targets=tuple(safety_targets), diagnostics=tuple([*plan.diagnostics, *safety_diagnostics]))


def execute_project_cleanup(plan: CleanupPlan) -> CleanupExecution:
    diagnostics = list(plan.diagnostics)
    removed: list[CleanupTarget] = []
    skipped: list[CleanupTarget] = []
    if plan.dry_run or not plan.can_execute:
        return CleanupExecution(
            plan=plan,
            removed_targets=(),
            skipped_targets=plan.targets,
            diagnostics=tuple(diagnostics),
            mutated=False,
        )

    for target in _deepest_first(plan.targets):
        if not target.exists:
            skipped.append(target)
            continue
        try:
            if target.target_kind == "directory":
                shutil.rmtree(target.path)
            else:
                target.path.unlink()
        except OSError as exc:
            failed = replace(target, status="failed", reason=str(exc))
            skipped.append(failed)
            diagnostics.append(
                Diagnostic(
                    code="ISO003",
                    severity="error",
                    concept="Project cleanup",
                    path=target.path,
                    message=f"Failed to remove planned cleanup target: {exc}.",
                )
            )
            continue
        removed.append(replace(target, status="removed"))

    return CleanupExecution(
        plan=plan,
        removed_targets=tuple(removed),
        skipped_targets=tuple(skipped),
        diagnostics=tuple(diagnostics),
        mutated=bool(removed),
    )


def render_cleanup_text(execution: CleanupExecution) -> list[str]:
    plan = execution.plan
    lines = [
        "Project Cleanup",
        f"Project root: {plan.project_root}",
        f"Authority: {plan.authority}",
        f"Mode: {'dry-run' if plan.dry_run else 'confirmed'}",
    ]
    if plan.dry_run:
        lines.append("No files removed; pass --yes to apply this plan.")
    if not plan.targets:
        lines.append("Planned removals: none")
    else:
        lines.append("Planned removals:")
        for target in plan.targets:
            relative = display_path(target.path, plan.project_root)
            detail = f"{target.part}: {relative} [{target.action}; {target.target_kind}; {'exists' if target.exists else 'absent'}; {target.status}]"
            if target.reason:
                detail = f"{detail} {target.reason}"
            lines.append(f"- {detail}")
    if execution.removed_targets:
        lines.append("Removed:")
        for target in execution.removed_targets:
            lines.append(f"- {target.part}: {display_path(target.path, plan.project_root)}")
    return lines


def _load_cleanup_authority(
    *,
    cwd: Path,
    project_selector: str | None,
    manifest_selector: str | None,
) -> tuple[Project | None, Path, Path, str, list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    if manifest_selector is not None:
        manifest_path = canonicalize(Path(manifest_selector))
        root = project_root_for_manifest(manifest_path)
        source = "explicit Project Manifest selector"
    elif project_selector is not None:
        selected = canonicalize(Path(project_selector))
        if selected.name == "manifest.toml":
            manifest_path = selected
            root = project_root_for_manifest(manifest_path)
            source = "explicit Project Manifest selector"
        else:
            root = selected
            manifest_path = manifest_path_for_root(root)
            source = "explicit Project root selector"
    else:
        discovered = find_ancestor_manifest(canonicalize(cwd))
        if discovered is not None:
            manifest_path = discovered
            root = project_root_for_manifest(manifest_path)
            source = "current directory"
        else:
            root = canonicalize(cwd)
            manifest_path = manifest_path_for_root(root)
            source = "current directory without manifest"
            diagnostics.append(
                Diagnostic(
                    code="ISO001",
                    severity="warning",
                    concept="Project cleanup",
                    path=manifest_path,
                    message="No Project Manifest was found; cleanup authority is limited to obvious Project bootstrap surfaces and explicit/default content-root policy files.",
                )
            )

    project, manifest_diagnostics = _load_valid_manifest(root, manifest_path, source)
    diagnostics.extend(manifest_diagnostics)
    if project is not None:
        return project, root, manifest_path, f"Project Manifest ({source})", diagnostics
    return None, root, manifest_path, f"limited filesystem authority ({source})", diagnostics


def _load_valid_manifest(root: Path, manifest_path: Path, source: str) -> tuple[Project | None, list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    raw, load_diagnostics = load_toml(manifest_path, "Project Manifest")
    if raw is None:
        diagnostics.extend(_as_cleanup_warnings(load_diagnostics))
        return None, diagnostics
    manifest, parse_diagnostics = parse_project_manifest(manifest_path, raw)
    if has_errors(parse_diagnostics):
        diagnostics.extend(_as_cleanup_warnings(parse_diagnostics))
        diagnostics.append(
            Diagnostic(
                code="ISO003",
                severity="warning",
                concept="Project cleanup",
                path=manifest_path,
                message="Project Manifest is malformed; cleanup will not infer Research Topics or Topic Workspaces.",
            )
        )
        return None, diagnostics
    diagnostics.extend(parse_diagnostics)
    return (
        Project(
            root=root,
            config_dir=canonicalize(manifest_path.parent),
            manifest_path=manifest_path,
            manifest=manifest,
            discovery_source=source,
        ),
        diagnostics,
    )


def _as_cleanup_warnings(diagnostics: list[Diagnostic]) -> list[Diagnostic]:
    return [
        replace(
            diagnostic,
            severity="warning",
            concept="Project cleanup",
            message=f"{diagnostic.message} Cleanup authority is limited.",
        )
        for diagnostic in diagnostics
    ]


def _cleanup_content_root(root: Path, project: Project | None, content_dir: str | None) -> Path:
    if content_dir is not None:
        return selected_content_root_path(root, content_dir)
    if project is not None:
        return content_root_path(root, project.manifest.path_defaults)
    return selected_content_root_path(root, None)


def _selected_cleanup_topics(
    project: Project | None,
    parts: tuple[str, ...],
    topics: tuple[str, ...],
    all_topics: bool,
    diagnostics: list[Diagnostic],
) -> tuple[str, ...]:
    topic_scoped = bool({"topic-workspace", "runtime", "bootstrap"} & set(parts))
    if not topic_scoped:
        return _dedupe(topics)
    if project is None:
        if "topic-workspace" in parts or "runtime" in parts:
            diagnostics.append(
                Diagnostic(
                    code="ISO001",
                    severity="error",
                    concept="Project cleanup",
                    field="topic",
                    message="Topic-scoped cleanup requires a valid Project Manifest; cleanup will not infer topics from directories.",
                )
            )
        return ()
    if all_topics or "bootstrap" in parts:
        return tuple(sorted(topic.id for topic in project.manifest.research_topics))
    if topics:
        return _dedupe(topics)
    default_topic = project.manifest.default_research_topic_id()
    if default_topic is not None:
        return (default_topic,)
    if len(project.manifest.research_topics) == 1:
        return (project.manifest.research_topics[0].id,)
    diagnostics.append(
        Diagnostic(
            code="ISO013",
            severity="error",
            concept="Project cleanup",
            field="topic",
            message="Select --topic <topic-id> or --all-topics for topic-scoped cleanup.",
        )
    )
    return ()


def _expand_parts(parts: tuple[str, ...]) -> tuple[str, ...]:
    expanded: list[str] = []
    for part in parts:
        if part == "bootstrap":
            expanded.extend(("project-config", "houmao-overlay", "content-policy", "topic-workspace"))
        else:
            expanded.append(part)
    return _dedupe(tuple(expanded))


def _topic_workspace_targets(
    root: Path,
    project: Project | None,
    topics: tuple[str, ...],
    diagnostics: list[Diagnostic],
) -> list[CleanupTarget]:
    if project is None:
        return []
    targets: list[CleanupTarget] = []
    for topic_id in topics:
        workspace_path = _workspace_path_for_topic(project, topic_id, diagnostics)
        if workspace_path is None:
            continue
        targets.append(_target("topic-workspace", workspace_path, root=root))
    return targets


def _runtime_targets(
    root: Path,
    project: Project | None,
    topics: tuple[str, ...],
    diagnostics: list[Diagnostic],
) -> list[CleanupTarget]:
    if project is None:
        return []
    targets: list[CleanupTarget] = []
    for topic_id in topics:
        workspace_path = _workspace_path_for_topic(project, topic_id, diagnostics)
        if workspace_path is None:
            continue
        runtime_paths = [
            workspace_path / RUNTIME_DB_FILENAME,
            *(workspace_path / directory for directory in RUNTIME_DIRECTORIES),
            workspace_path / ADAPTER_MANIFEST_ROOT,
        ]
        targets.extend(_target("runtime", path, root=root) for path in runtime_paths)
    return targets


def _workspace_path_for_topic(project: Project, topic_id: str, diagnostics: list[Diagnostic]) -> Path | None:
    topic = project.manifest.first_topic(topic_id)
    if topic is None:
        diagnostics.append(
            Diagnostic(
                code="ISO013",
                severity="error",
                concept="Project cleanup",
                field="topic",
                message=f"Selected Research Topic is not registered by the Project Manifest: {topic_id}.",
            )
        )
        return None
    _, workspace_path, _, workspace_diagnostics = resolve_topic_workspace(project, topic, None)
    diagnostics.extend(workspace_diagnostics)
    return workspace_path


def _content_root_target(content_root: Path, root: Path, purge_content_root: bool) -> CleanupTarget:
    if not purge_content_root:
        return _target(
            "content-root",
            content_root,
            root=root,
            status="refused",
            reason="content-root cleanup requires --purge-content-root.",
        )
    reserved_dirs = {config_dir_for_root(root), houmao_overlay_dir_for_root(root), root_houmao_overlay_dir_for_root(root)}
    if content_root == root or content_root in reserved_dirs:
        return _target(
            "content-root",
            content_root,
            root=root,
            status="refused",
            reason="refusing to remove the Project root, Project Config Directory, or Houmao state directory as a content root.",
        )
    return _target("content-root", content_root, root=root)


def _target(
    part: str,
    path: Path,
    *,
    root: Path,
    action: str = "remove",
    status: str | None = None,
    reason: str | None = None,
) -> CleanupTarget:
    target_path = _entry_path(path)
    kind = _target_kind(target_path)
    exists = kind != "absent"
    effective_status = status or ("planned" if exists else "absent")
    return CleanupTarget(
        part=part,
        path=target_path,
        action=action,
        target_kind=kind,
        exists=exists,
        status=effective_status,
        warnings=_target_warnings(target_path, root),
        reason=reason,
    )


def _entry_path(path: Path) -> Path:
    expanded = path.expanduser()
    if expanded.is_absolute():
        absolute = expanded
    else:
        absolute = Path.cwd() / expanded
    if absolute.is_symlink():
        return canonicalize(absolute.parent) / absolute.name
    return canonicalize(absolute)


def _target_kind(path: Path) -> str:
    if path.is_symlink():
        return "symlink"
    if path.is_dir():
        return "directory"
    if path.is_file():
        return "file"
    if path.exists():
        return "other"
    return "absent"


def _target_warnings(path: Path, root: Path) -> tuple[str, ...]:
    if path.is_symlink():
        try:
            target = path.readlink()
        except OSError:
            target = Path("<unreadable>")
        return (f"planned target is a symlink entry; cleanup will remove the symlink itself and will not recurse into {target}.",)
    if path.exists() and path.is_dir() and any(path.iterdir()):
        return ("directory is not empty; cleanup removes this exact managed directory when confirmed.",)
    return ()


def _validate_targets(plan: CleanupPlan) -> tuple[list[Diagnostic], list[CleanupTarget]]:
    diagnostics: list[Diagnostic] = []
    targets: list[CleanupTarget] = []
    for target in plan.targets:
        if target.status == "refused":
            diagnostics.append(
                Diagnostic(
                    code="ISO003",
                    severity="error",
                    concept="Project cleanup",
                    path=target.path,
                    message=target.reason or "Cleanup target was refused.",
                )
            )
            targets.append(target)
            continue
        unsafe_reason = _unsafe_reason(target.path, plan.project_root, target)
        if unsafe_reason is not None:
            diagnostics.append(
                Diagnostic(
                    code="ISO005",
                    severity="error",
                    concept="Project cleanup",
                    path=target.path,
                    message=unsafe_reason,
                )
            )
            targets.append(replace(target, status="refused", reason=unsafe_reason))
        else:
            targets.append(target)
    return diagnostics, targets


def _unsafe_reason(path: Path, root: Path, target: CleanupTarget) -> str | None:
    canonical_root = canonicalize(root)
    if path == canonical_root:
        return "Refusing to remove the Project root."
    if path.is_symlink():
        if not is_within(path.parent, canonical_root):
            return "Refusing to remove a symlink entry outside the Project root."
        return None
    if not is_within(path, canonical_root):
        return "Cleanup target resolves outside the Project root."
    if target.part in {"content-policy", "content-root"} and (
        is_within(path, config_dir_for_root(canonical_root))
        or is_within(path, root_houmao_overlay_dir_for_root(canonical_root))
    ):
        return "Cleanup content targets must not resolve inside the Project Config Directory or a Houmao state directory."
    return None


def _dedupe(values: tuple[str, ...]) -> tuple[str, ...]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return tuple(result)


def _dedupe_targets(targets: list[CleanupTarget]) -> list[CleanupTarget]:
    seen: set[Path] = set()
    result: list[CleanupTarget] = []
    for target in targets:
        if target.path in seen:
            continue
        seen.add(target.path)
        result.append(target)
    return result


def _deepest_first(targets: tuple[CleanupTarget, ...]) -> tuple[CleanupTarget, ...]:
    return tuple(sorted(targets, key=lambda target: len(target.path.parts), reverse=True))
