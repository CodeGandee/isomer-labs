"""Project generated content-root relocation planning and execution."""

from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
import os
from typing import Any

import tomlkit  # type: ignore[import-untyped]

from isomer_labs.workspace.layout import (
    TOPIC_WORKSPACE_BASE_NAME,
    content_root_path,
)
from isomer_labs.core.diagnostics import Diagnostic, has_errors
from isomer_labs.houmao.manifests import ADAPTER_MANIFEST_ROOT
from isomer_labs.project.manifest import parse_project_manifest
from isomer_labs.models import Project
from isomer_labs.core.path_utils import canonicalize, display_path, is_within
from isomer_labs.project import (
    config_dir_for_root,
    find_ancestor_manifest,
    manifest_path_for_root,
    project_root_for_manifest,
    root_houmao_overlay_dir_for_root,
)
from isomer_labs.runtime.models import RUNTIME_DIRECTORIES
from isomer_labs.core.toml_loader import load_toml


CONTENT_POLICY_FILES = ("README.md", ".gitignore")
RUNTIME_DB_FILENAME = "state.sqlite"
PROJECT_CONTENT_RELOCATION_CONCEPT = "Project content-root relocation"
RUNTIME_BREAKAGE_WARNING = (
    "Moving the Isomer content root updates Project Manifest paths and moves Isomer-managed content containers only. "
    "Existing Workspace Runtime records, Pixi environments, installed packages, adapter runtime material, logs, and stored path plans may contain old paths and may require reinstall or reinitialization."
)


@dataclass(frozen=True)
class RelocationMove:
    managed_kind: str
    source: Path
    destination: Path
    target_kind: str
    exists: bool
    status: str
    reason: str | None = None

    @property
    def movable(self) -> bool:
        return self.status == "planned" and self.exists

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "managed_kind": self.managed_kind,
            "source": str(self.source),
            "destination": str(self.destination),
            "target_kind": self.target_kind,
            "exists": self.exists,
            "status": self.status,
        }
        if self.reason is not None:
            data["reason"] = self.reason
        return data


@dataclass(frozen=True)
class ManifestUpdate:
    field: str
    old_value: str | None
    new_value: str
    status: str = "planned"

    def to_json(self) -> dict[str, object]:
        return {
            "field": self.field,
            "old_value": self.old_value,
            "new_value": self.new_value,
            "status": self.status,
        }


@dataclass(frozen=True)
class RelocationEntry:
    path: Path
    entry_kind: str
    reason: str

    def to_json(self) -> dict[str, object]:
        return {
            "path": str(self.path),
            "entry_kind": self.entry_kind,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class ContentRootRelocationPlan:
    project_root: Path
    manifest_path: Path
    authority: str
    old_content_root: Path
    new_content_root: Path
    dry_run: bool
    confirmation_required: bool
    managed_moves: tuple[RelocationMove, ...]
    manifest_updates: tuple[ManifestUpdate, ...]
    skipped_entries: tuple[RelocationEntry, ...]
    unmanaged_leftovers: tuple[RelocationEntry, ...]
    warnings: tuple[str, ...]
    diagnostics: tuple[Diagnostic, ...]

    @property
    def ok(self) -> bool:
        return not has_errors(list(self.diagnostics))

    @property
    def can_execute(self) -> bool:
        return self.ok and not self.dry_run

    def to_json(self) -> dict[str, object]:
        return {
            "project_root": str(self.project_root),
            "project_manifest_path": str(self.manifest_path),
            "authority": self.authority,
            "old_content_root": str(self.old_content_root),
            "new_content_root": str(self.new_content_root),
            "dry_run": self.dry_run,
            "confirmation_required": self.confirmation_required,
            "managed_moves": [move.to_json() for move in self.managed_moves],
            "manifest_updates": [update.to_json() for update in self.manifest_updates],
            "skipped_entries": [entry.to_json() for entry in self.skipped_entries],
            "unmanaged_leftovers": [entry.to_json() for entry in self.unmanaged_leftovers],
            "warnings": list(self.warnings),
        }


@dataclass(frozen=True)
class ContentRootRelocationExecution:
    plan: ContentRootRelocationPlan
    applied_moves: tuple[RelocationMove, ...]
    skipped_moves: tuple[RelocationMove, ...]
    rolled_back_moves: tuple[RelocationMove, ...]
    removed_empty_dirs: tuple[Path, ...]
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
            "old_content_root": str(self.plan.old_content_root),
            "new_content_root": str(self.plan.new_content_root),
            "dry_run": self.plan.dry_run,
            "confirmation_required": self.plan.confirmation_required,
            "relocation": self.plan.to_json(),
            "managed_moves": [move.to_json() for move in self.plan.managed_moves],
            "manifest_updates": [update.to_json() for update in self.plan.manifest_updates],
            "applied_moves": [move.to_json() for move in self.applied_moves],
            "skipped_moves": [move.to_json() for move in self.skipped_moves],
            "rolled_back_moves": [move.to_json() for move in self.rolled_back_moves],
            "removed_empty_dirs": [str(path) for path in self.removed_empty_dirs],
            "skipped_entries": [entry.to_json() for entry in self.plan.skipped_entries],
            "unmanaged_leftovers": [entry.to_json() for entry in self.plan.unmanaged_leftovers],
            "warnings": list(self.plan.warnings),
        }


def plan_project_content_root_move(
    *,
    cwd: Path,
    project_selector: str | None = None,
    manifest_selector: str | None = None,
    to_content_dir: str | None = None,
    dry_run: bool = False,
    yes: bool = False,
) -> ContentRootRelocationPlan:
    project, root, manifest_path, authority, diagnostics = _load_relocation_authority(
        cwd=cwd,
        project_selector=project_selector,
        manifest_selector=manifest_selector,
    )
    effective_dry_run = dry_run or not yes
    old_content_root = _old_content_root(root, project)
    new_content_root = _new_content_root(root, to_content_dir)
    warnings = [RUNTIME_BREAKAGE_WARNING]

    if to_content_dir is None or not to_content_dir.strip():
        diagnostics.append(
            Diagnostic(
                code="ISO003",
                severity="error",
                concept=PROJECT_CONTENT_RELOCATION_CONCEPT,
                field="to",
                message="Select the destination generated content root with --to <content-dir>.",
            )
        )

    if project is None:
        return ContentRootRelocationPlan(
            project_root=root,
            manifest_path=manifest_path,
            authority=authority,
            old_content_root=old_content_root,
            new_content_root=new_content_root,
            dry_run=effective_dry_run,
            confirmation_required=not yes,
            managed_moves=(),
            manifest_updates=(),
            skipped_entries=(),
            unmanaged_leftovers=(),
            warnings=tuple(warnings),
            diagnostics=tuple(diagnostics),
        )

    managed_moves, manifest_updates, skipped_entries = _planned_project_updates(project, old_content_root, new_content_root)
    unmanaged_leftovers = _unmanaged_leftovers(old_content_root, managed_moves)
    warnings.extend(_runtime_marker_warnings(managed_moves))
    diagnostics.extend(_path_safety_diagnostics(root, old_content_root, new_content_root, managed_moves))

    return ContentRootRelocationPlan(
        project_root=root,
        manifest_path=manifest_path,
        authority=authority,
        old_content_root=old_content_root,
        new_content_root=new_content_root,
        dry_run=effective_dry_run,
        confirmation_required=not yes,
        managed_moves=tuple(managed_moves),
        manifest_updates=tuple(manifest_updates),
        skipped_entries=tuple(skipped_entries),
        unmanaged_leftovers=tuple(unmanaged_leftovers),
        warnings=tuple(_dedupe(warnings)),
        diagnostics=tuple(diagnostics),
    )


def execute_project_content_root_move(plan: ContentRootRelocationPlan) -> ContentRootRelocationExecution:
    diagnostics = list(plan.diagnostics)
    applied: list[RelocationMove] = []
    skipped: list[RelocationMove] = []
    rolled_back: list[RelocationMove] = []
    removed_empty_dirs: list[Path] = []
    manifest_written = False

    if plan.dry_run or not plan.can_execute:
        return ContentRootRelocationExecution(
            plan=plan,
            applied_moves=(),
            skipped_moves=plan.managed_moves,
            rolled_back_moves=(),
            removed_empty_dirs=(),
            diagnostics=tuple(diagnostics),
            mutated=False,
        )

    try:
        for move in plan.managed_moves:
            if not move.movable:
                skipped.append(move)
                continue
            move.destination.parent.mkdir(parents=True, exist_ok=True)
            move.source.rename(move.destination)
            applied.append(replace(move, status="moved"))
        _write_manifest_updates(plan)
        manifest_written = True
        removed_empty_dirs.extend(_remove_empty_old_dirs(plan.old_content_root))
    except OSError as exc:
        exc_filename = getattr(exc, "filename", None)
        exc_path = Path(str(exc_filename)) if exc_filename is not None else None
        diagnostics.append(
            Diagnostic(
                code="ISO003",
                severity="error",
                concept=PROJECT_CONTENT_RELOCATION_CONCEPT,
                path=exc_path,
                message=f"Failed to apply content-root relocation: {exc}.",
            )
        )
        if not manifest_written:
            for moved in reversed(applied):
                try:
                    moved.source.parent.mkdir(parents=True, exist_ok=True)
                    moved.destination.rename(moved.source)
                    rolled_back.append(replace(moved, status="rolled_back"))
                except OSError as rollback_exc:
                    diagnostics.append(
                        Diagnostic(
                            code="ISO003",
                            severity="error",
                            concept=PROJECT_CONTENT_RELOCATION_CONCEPT,
                            path=moved.destination,
                            message=f"Failed to roll back moved entry {moved.destination}: {rollback_exc}.",
                        )
                    )
        return ContentRootRelocationExecution(
            plan=plan,
            applied_moves=tuple(applied),
            skipped_moves=tuple(skipped),
            rolled_back_moves=tuple(rolled_back),
            removed_empty_dirs=tuple(removed_empty_dirs),
            diagnostics=tuple(diagnostics),
            mutated=bool(applied) and len(rolled_back) != len(applied),
        )

    return ContentRootRelocationExecution(
        plan=plan,
        applied_moves=tuple(applied),
        skipped_moves=tuple(skipped),
        rolled_back_moves=tuple(rolled_back),
        removed_empty_dirs=tuple(removed_empty_dirs),
        diagnostics=tuple(diagnostics),
        mutated=bool(applied or plan.manifest_updates or removed_empty_dirs),
    )


def render_content_root_move_text(execution: ContentRootRelocationExecution) -> list[str]:
    plan = execution.plan
    lines = [
        "Project Content Root Relocation",
        f"Project root: {plan.project_root}",
        f"Authority: {plan.authority}",
        f"Mode: {'dry-run' if plan.dry_run else 'confirmed'}",
        f"Old content root: {display_path(plan.old_content_root, plan.project_root)}",
        f"New content root: {display_path(plan.new_content_root, plan.project_root)}",
    ]
    if plan.dry_run:
        lines.append("No files moved and no manifest written; pass --yes to apply this plan.")
    if plan.managed_moves:
        lines.append("Managed moves:")
        for move in plan.managed_moves:
            source = display_path(move.source, plan.project_root)
            destination = display_path(move.destination, plan.project_root)
            lines.append(f"- {move.managed_kind}: {source} -> {destination} [{move.status}]")
    else:
        lines.append("Managed moves: none")
    if plan.manifest_updates:
        lines.append("Manifest updates:")
        for update in plan.manifest_updates:
            lines.append(f"- {update.field}: {update.old_value} -> {update.new_value}")
    if plan.skipped_entries:
        lines.append("Skipped entries:")
        for entry in plan.skipped_entries:
            lines.append(f"- {display_path(entry.path, plan.project_root)}: {entry.reason}")
    if plan.unmanaged_leftovers:
        lines.append("Unmanaged leftovers:")
        for entry in plan.unmanaged_leftovers:
            lines.append(f"- {display_path(entry.path, plan.project_root)}: {entry.reason}")
    if execution.applied_moves:
        lines.append("Applied moves:")
        for move in execution.applied_moves:
            lines.append(f"- {display_path(move.destination, plan.project_root)}")
    if execution.removed_empty_dirs:
        lines.append("Removed empty directories:")
        for path in execution.removed_empty_dirs:
            lines.append(f"- {display_path(path, plan.project_root)}")
    if plan.warnings:
        lines.append("Warnings:")
        lines.extend(f"- {warning}" for warning in plan.warnings)
    return lines


def _load_relocation_authority(
    *,
    cwd: Path,
    project_selector: str | None,
    manifest_selector: str | None,
) -> tuple[Project | None, Path, Path, str, list[Diagnostic]]:
    if manifest_selector is not None:
        manifest_path = _entry_path(Path(manifest_selector))
        root = project_root_for_manifest(manifest_path)
        source = "explicit Project Manifest selector"
    elif project_selector is not None:
        selected = _entry_path(Path(project_selector))
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
        else:
            root = canonicalize(cwd)
            manifest_path = manifest_path_for_root(root)
        source = "current directory"

    raw, diagnostics = load_toml(manifest_path, "Project Manifest")
    if raw is None:
        return None, root, manifest_path, source, diagnostics
    manifest, parse_diagnostics = parse_project_manifest(manifest_path, raw)
    diagnostics.extend(parse_diagnostics)
    if has_errors(diagnostics):
        return None, root, manifest_path, source, diagnostics
    return (
        Project(
            root=root,
            config_dir=canonicalize(manifest_path.parent),
            manifest_path=manifest_path,
            manifest=manifest,
            discovery_source=source,
        ),
        root,
        manifest_path,
        f"Project Manifest ({source})",
        diagnostics,
    )


def _old_content_root(root: Path, project: Project | None) -> Path:
    if project is None:
        return content_root_path(root, None)
    value = project.manifest.path_defaults.get("isomer_content_root")
    if isinstance(value, str) and value:
        return _project_entry_path(root, value)
    return content_root_path(root, project.manifest.path_defaults)


def _new_content_root(root: Path, value: str | None) -> Path:
    if value is None or not value.strip():
        return content_root_path(root, None)
    return _project_entry_path(root, value)


def _planned_project_updates(
    project: Project,
    old_root: Path,
    new_root: Path,
) -> tuple[list[RelocationMove], list[ManifestUpdate], list[RelocationEntry]]:
    moves: list[RelocationMove] = []
    updates: list[ManifestUpdate] = [
        ManifestUpdate(
            field="paths.isomer_content_root",
            old_value=_string_default(project, "isomer_content_root"),
            new_value=display_path(new_root, project.root),
        )
    ]
    skipped: list[RelocationEntry] = []

    for file_name in CONTENT_POLICY_FILES:
        source = old_root / file_name
        destination = new_root / file_name
        if source.exists():
            moves.append(_move("content-policy", source, destination))

    base_input = _string_default(project, "topic_workspace_base_dir")
    if base_input is None:
        new_base = new_root / TOPIC_WORKSPACE_BASE_NAME
        updates.append(ManifestUpdate("paths.topic_workspace_base_dir", None, display_path(new_base, project.root)))
    else:
        old_base = _project_entry_path(project.root, base_input)
        if _path_inside(old_base, old_root):
            new_base = new_root / old_base.relative_to(old_root)
            updates.append(ManifestUpdate("paths.topic_workspace_base_dir", base_input, display_path(new_base, project.root)))
        else:
            skipped.append(RelocationEntry(old_base, _entry_kind(old_base), "topic_workspace_base_dir is outside the old content root."))

    for workspace in project.manifest.topic_workspaces:
        workspace_source = _workspace_path(project, workspace_id=workspace.id)
        if workspace_source is None:
            continue
        if not _path_inside(workspace_source, old_root):
            skipped.append(
                RelocationEntry(
                    workspace_source,
                    _entry_kind(workspace_source),
                    f"Topic Workspace {workspace.id} is outside the old content root.",
                )
            )
            continue
        destination = new_root / workspace_source.relative_to(old_root)
        moves.append(_move("topic-workspace", workspace_source, destination, absent_status="absent"))
        updates.append(
            ManifestUpdate(
                field=f"topic_workspaces.{workspace.id}.path",
                old_value=workspace.path_input,
                new_value=display_path(destination, project.root),
            )
        )
    return moves, updates, skipped


def _workspace_path(project: Project, *, workspace_id: str) -> Path | None:
    workspace = project.manifest.first_workspace(workspace_id)
    if workspace is None:
        return None
    if workspace.path_input is not None:
        return _project_entry_path(project.root, workspace.path_input)
    if workspace.research_topic_id is None:
        return None
    base_input = _string_default(project, "topic_workspace_base_dir")
    if base_input is not None:
        return _project_entry_path(project.root, f"{base_input}/{workspace.research_topic_id}")
    return content_root_path(project.root, project.manifest.path_defaults) / TOPIC_WORKSPACE_BASE_NAME / workspace.research_topic_id


def _move(managed_kind: str, source: Path, destination: Path, *, absent_status: str = "absent") -> RelocationMove:
    kind = _entry_kind(source)
    exists = kind != "absent"
    return RelocationMove(
        managed_kind=managed_kind,
        source=source,
        destination=destination,
        target_kind=kind,
        exists=exists,
        status="planned" if exists else absent_status,
    )


def _path_safety_diagnostics(
    root: Path,
    old_root: Path,
    new_root: Path,
    moves: list[RelocationMove],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    config_dir = config_dir_for_root(root)
    root_houmao_dir = root_houmao_overlay_dir_for_root(root)
    if old_root == new_root:
        diagnostics.append(
            Diagnostic(
                code="ISO003",
                severity="error",
                concept=PROJECT_CONTENT_RELOCATION_CONCEPT,
                path=new_root,
                field="to",
                message="Destination content root is already the configured content root.",
            )
        )
    for label, path in (("old", old_root), ("destination", new_root)):
        if path.is_symlink():
            diagnostics.append(
                Diagnostic(
                    code="ISO005",
                    severity="error",
                    concept=PROJECT_CONTENT_RELOCATION_CONCEPT,
                    path=path,
                    message=f"Refusing {label} content root because it is a symlink entry.",
                )
            )
        if not is_within(path, root):
            diagnostics.append(
                Diagnostic(
                    code="ISO005",
                    severity="error",
                    concept=PROJECT_CONTENT_RELOCATION_CONCEPT,
                    path=path,
                    message=f"Refusing {label} content root because it resolves outside the Project root.",
                )
            )
    if new_root == root:
        diagnostics.append(
            Diagnostic(
                code="ISO005",
                severity="error",
                concept=PROJECT_CONTENT_RELOCATION_CONCEPT,
                path=new_root,
                message="Destination content root must not be the Project root.",
            )
        )
    if is_within(new_root, config_dir):
        diagnostics.append(
            Diagnostic(
                code="ISO005",
                severity="error",
                concept=PROJECT_CONTENT_RELOCATION_CONCEPT,
                path=new_root,
                message="Destination content root must not live inside the Project Config Directory.",
            )
        )
    if is_within(new_root, root_houmao_dir):
        diagnostics.append(
            Diagnostic(
                code="ISO005",
                severity="error",
                concept=PROJECT_CONTENT_RELOCATION_CONCEPT,
                path=new_root,
                message="Destination content root must not collide with root .houmao external Houmao state.",
            )
        )
    if new_root.exists() and not new_root.is_dir():
        diagnostics.append(
            Diagnostic(
                code="ISO005",
                severity="error",
                concept=PROJECT_CONTENT_RELOCATION_CONCEPT,
                path=new_root,
                message="Destination content root already exists and is not a directory.",
            )
        )
    for move in moves:
        if move.destination.exists() and move.destination != move.source:
            diagnostics.append(
                Diagnostic(
                    code="ISO005",
                    severity="error",
                    concept=PROJECT_CONTENT_RELOCATION_CONCEPT,
                    path=move.destination,
                    message=f"Destination already contains a conflicting managed entry for {move.managed_kind}.",
                )
            )
    return diagnostics


def _unmanaged_leftovers(old_root: Path, moves: list[RelocationMove]) -> list[RelocationEntry]:
    if not old_root.is_dir() or old_root.is_symlink():
        return []
    managed_sources = tuple(move.source for move in moves if move.exists)
    leftovers: list[RelocationEntry] = []
    leftover_roots: list[Path] = []
    for path in sorted(old_root.rglob("*")):
        if _is_managed_path(path, managed_sources):
            continue
        if any(_path_inside(path, leftover) for leftover in leftover_roots):
            continue
        leftovers.append(RelocationEntry(path, _entry_kind(path), "unmanaged entry under old content root is preserved."))
        if path.is_dir():
            leftover_roots.append(path)
    return leftovers


def _is_managed_path(path: Path, managed_sources: tuple[Path, ...]) -> bool:
    for source in managed_sources:
        if _path_inside(path, source) or _path_inside(source, path):
            return True
    return False


def _runtime_marker_warnings(moves: list[RelocationMove]) -> list[str]:
    warnings: list[str] = []
    for move in moves:
        if move.managed_kind != "topic-workspace" or not move.source.exists() or not move.source.is_dir():
            continue
        markers = _runtime_markers(move.source)
        if markers:
            relative_markers = ", ".join(str(marker.relative_to(move.source)) for marker in markers)
            warnings.append(
                f"Topic Workspace {move.source} contains runtime or environment markers ({relative_markers}); relocation will move the containing directory but will not rewrite internal paths."
            )
    return warnings


def _runtime_markers(workspace_path: Path) -> list[Path]:
    candidates = [
        workspace_path / RUNTIME_DB_FILENAME,
        workspace_path / ".pixi",
        workspace_path / "pixi.toml",
        workspace_path / "pyproject.toml",
        workspace_path / "pixi.lock",
        workspace_path / ADAPTER_MANIFEST_ROOT,
        workspace_path / "runtime",
        *(workspace_path / directory for directory in RUNTIME_DIRECTORIES),
    ]
    return [path for path in candidates if path.exists()]


def _write_manifest_updates(plan: ContentRootRelocationPlan) -> None:
    text = plan.manifest_path.read_text(encoding="utf-8")
    document: Any = tomlkit.parse(text)
    paths = _ensure_table(document, "paths")
    for update in plan.manifest_updates:
        if update.field == "paths.isomer_content_root":
            paths["isomer_content_root"] = update.new_value
        elif update.field == "paths.topic_workspace_base_dir":
            paths["topic_workspace_base_dir"] = update.new_value
    workspace_updates = {
        update.field.removeprefix("topic_workspaces.").removesuffix(".path"): update.new_value
        for update in plan.manifest_updates
        if update.field.startswith("topic_workspaces.") and update.field.endswith(".path")
    }
    if workspace_updates:
        for workspace_table in document.get("topic_workspaces", []):
            workspace_id = workspace_table.get("id")
            workspace_id_text = str(workspace_id) if workspace_id is not None else None
            if workspace_id_text in workspace_updates:
                workspace_table["path"] = workspace_updates[workspace_id_text]
    _atomic_write(plan.manifest_path, tomlkit.dumps(document))


def _ensure_table(document: Any, key: str) -> Any:
    try:
        return document[key]
    except KeyError:
        table = tomlkit.table()
        document[key] = table
        return table


def _atomic_write(path: Path, content: str) -> None:
    temp_path = path.with_name(f".{path.name}.tmp")
    temp_path.write_text(content, encoding="utf-8")
    os.replace(temp_path, path)


def _remove_empty_old_dirs(old_root: Path) -> list[Path]:
    removed: list[Path] = []
    for path in (old_root / TOPIC_WORKSPACE_BASE_NAME, old_root):
        if path.is_dir() and not path.is_symlink():
            try:
                path.rmdir()
            except OSError:
                continue
            removed.append(path)
    return removed


def _project_entry_path(project_root: Path, value: str) -> Path:
    candidate = Path(value).expanduser()
    if candidate.is_absolute():
        return _entry_path(candidate)
    return _entry_path(project_root / candidate)


def _entry_path(path: Path) -> Path:
    expanded = path.expanduser()
    if expanded.is_symlink():
        return canonicalize(expanded.parent) / expanded.name
    return canonicalize(expanded)


def _entry_kind(path: Path) -> str:
    if path.is_symlink():
        return "symlink"
    if path.is_dir():
        return "directory"
    if path.is_file():
        return "file"
    if path.exists():
        return "other"
    return "absent"


def _string_default(project: Project, key: str) -> str | None:
    value = project.manifest.path_defaults.get(key)
    if isinstance(value, str) and value:
        return value
    return None


def _path_inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result
