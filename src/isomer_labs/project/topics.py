"""Research Topic CRUD operations."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import re
from typing import Any

import tomlkit  # type: ignore[import-untyped]

from isomer_labs.workspace.layout import topic_workspace_path as default_topic_workspace_path
from isomer_labs.workspace.layout import topic_workspace_path_input_from_defaults
from isomer_labs.core.diagnostics import Diagnostic, has_errors
from isomer_labs.houmao.manifests import ADAPTER_MANIFEST_ROOT
from isomer_labs.models import Project, ProjectState, TopicWorkspaceRegistration
from isomer_labs.core.path_utils import display_path, is_within, resolve_project_path
from isomer_labs.project import houmao_overlay_dir_for_root, root_houmao_overlay_dir_for_root
from isomer_labs.runtime.models import RUNTIME_DIRECTORIES


TOPIC_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")
RESEARCH_TOPIC_SCHEMA_VERSION = "isomer-research-topic-config.v1"
TOPIC_REGISTRATION_SCHEMA_VERSION = "isomer-research-topic-registration.v1"
TOPIC_WORKSPACE_SCHEMA_VERSION = "isomer-topic-workspace.v1"
VALID_TOPIC_STATUSES = {"active", "archived"}
RUNTIME_DB_FILENAME = "state.sqlite"
TOPIC_CRUD_CONCEPT = "Research Topic"


@dataclass(frozen=True)
class TopicCreateResult:
    project_root: Path
    topic_id: str
    topic_statement: str | None
    topic_config_path: Path
    topic_workspace_id: str
    topic_workspace_path: Path
    topic_workspace_path_input: str
    set_default: bool
    mutated: bool
    diagnostics: list[Diagnostic]

    @property
    def ok(self) -> bool:
        return not has_errors(self.diagnostics)

    def to_json(self) -> dict[str, object]:
        return {
            "ok": self.ok,
            "mutated": self.mutated,
            "project_root": str(self.project_root),
            "research_topic_id": self.topic_id,
            "topic_statement": self.topic_statement,
            "topic_config_path": str(self.topic_config_path),
            "topic_workspace_id": self.topic_workspace_id,
            "topic_workspace_path": str(self.topic_workspace_path),
            "topic_workspace_path_input": self.topic_workspace_path_input,
            "set_default": self.set_default,
        }


@dataclass(frozen=True)
class TopicShowResult:
    project_root: Path
    topic: dict[str, object] | None
    topic_config: dict[str, object] | None
    topic_workspace: dict[str, object] | None
    topic_workspace_path: Path | None
    diagnostics: list[Diagnostic]

    @property
    def ok(self) -> bool:
        return not has_errors(self.diagnostics)

    def to_json(self) -> dict[str, object]:
        return {
            "ok": self.ok,
            "mutated": False,
            "project_root": str(self.project_root),
            "topic": self.topic,
            "topic_config": self.topic_config,
            "topic_workspace": self.topic_workspace,
            "topic_workspace_path": str(self.topic_workspace_path) if self.topic_workspace_path is not None else None,
        }


@dataclass(frozen=True)
class TopicUpdateResult:
    project_root: Path
    topic_id: str
    updated_fields: tuple[str, ...]
    mutated: bool
    diagnostics: list[Diagnostic]

    @property
    def ok(self) -> bool:
        return not has_errors(self.diagnostics)

    def to_json(self) -> dict[str, object]:
        return {
            "ok": self.ok,
            "mutated": self.mutated,
            "project_root": str(self.project_root),
            "research_topic_id": self.topic_id,
            "updated_fields": list(self.updated_fields),
        }


@dataclass(frozen=True)
class TopicDeletePlan:
    project_root: Path
    topic_id: str
    dry_run: bool
    confirmation_required: bool
    topic_config_path: Path | None
    topic_workspace_path: Path | None
    preserved_paths: tuple[Path, ...]
    removed_manifest_entries: tuple[str, ...]
    cleared_defaults: tuple[str, ...]
    blockers: tuple[str, ...]
    diagnostics: list[Diagnostic]

    def to_json(self) -> dict[str, object]:
        return {
            "project_root": str(self.project_root),
            "research_topic_id": self.topic_id,
            "dry_run": self.dry_run,
            "confirmation_required": self.confirmation_required,
            "topic_config_path": str(self.topic_config_path) if self.topic_config_path is not None else None,
            "topic_workspace_path": str(self.topic_workspace_path) if self.topic_workspace_path is not None else None,
            "preserved_paths": [str(path) for path in self.preserved_paths],
            "removed_manifest_entries": list(self.removed_manifest_entries),
            "cleared_defaults": list(self.cleared_defaults),
            "blockers": list(self.blockers),
            "cleanup_guidance": "Use `isomer-cli project cleanup --part topic-workspace --topic <topic-id> --dry-run` to review filesystem workspace removal.",
        }


@dataclass(frozen=True)
class TopicDeleteResult:
    plan: TopicDeletePlan
    mutated: bool
    removed_paths: tuple[Path, ...]
    diagnostics: list[Diagnostic]

    @property
    def ok(self) -> bool:
        return not has_errors(self.diagnostics)

    def to_json(self) -> dict[str, object]:
        payload = self.plan.to_json()
        payload.update(
            {
                "ok": self.ok,
                "mutated": self.mutated,
                "delete_plan": self.plan.to_json(),
                "removed_paths": [str(path) for path in self.removed_paths],
            }
        )
        return payload


def create_research_topic(
    project: Project,
    *,
    topic_id: str,
    statement: str | None,
    workspace_dir: str | None = None,
    set_default: bool = False,
) -> TopicCreateResult:
    diagnostics: list[Diagnostic] = []
    topic_config_path = project.config_dir / "research-topics" / f"{topic_id}.toml"
    workspace_path, workspace_path_input = _workspace_target(project, topic_id, workspace_dir)

    diagnostics.extend(_topic_id_diagnostics(topic_id))
    normalized_statement = _normalized_statement(statement)
    diagnostics.extend(_topic_statement_diagnostics(topic_id, normalized_statement))
    diagnostics.extend(_topic_create_collision_diagnostics(project, topic_id, topic_config_path, workspace_path))

    if has_errors(diagnostics):
        return TopicCreateResult(
            project_root=project.root,
            topic_id=topic_id,
            topic_statement=normalized_statement,
            topic_config_path=topic_config_path,
            topic_workspace_id=topic_id,
            topic_workspace_path=workspace_path,
            topic_workspace_path_input=workspace_path_input,
            set_default=set_default,
            mutated=False,
            diagnostics=diagnostics,
        )

    document = _read_manifest_document(project)
    topics = _ensure_aot(document, "research_topics")
    topic_table = tomlkit.table()
    topic_table["id"] = topic_id
    topic_table["schema_version"] = TOPIC_REGISTRATION_SCHEMA_VERSION
    topic_table["config_path"] = display_path(topic_config_path, project.root)
    topic_table["topic_workspace_id"] = topic_id
    topic_table["status"] = "active"
    topics.append(topic_table)

    workspaces = _ensure_aot(document, "topic_workspaces")
    workspace_table = tomlkit.table()
    workspace_table["id"] = topic_id
    workspace_table["schema_version"] = TOPIC_WORKSPACE_SCHEMA_VERSION
    workspace_table["research_topic_id"] = topic_id
    workspace_table["path"] = workspace_path_input
    workspace_table["status"] = "active"
    workspaces.append(workspace_table)

    if set_default:
        defaults = _ensure_table(document, "defaults")
        defaults["research_topic_id"] = topic_id
        defaults["topic_workspace_id"] = topic_id

    topic_config_path.parent.mkdir(parents=True, exist_ok=True)
    workspace_path.mkdir(parents=True, exist_ok=True)
    _atomic_write(topic_config_path, _topic_config_text(topic_id, normalized_statement or ""))
    _atomic_write(project.manifest_path, tomlkit.dumps(document))

    return TopicCreateResult(
        project_root=project.root,
        topic_id=topic_id,
        topic_statement=normalized_statement,
        topic_config_path=topic_config_path,
        topic_workspace_id=topic_id,
        topic_workspace_path=workspace_path,
        topic_workspace_path_input=workspace_path_input,
        set_default=set_default,
        mutated=True,
        diagnostics=diagnostics,
    )


def show_research_topic(state: ProjectState, topic_id: str) -> TopicShowResult:
    project = state.project
    diagnostics: list[Diagnostic] = []
    topic = project.manifest.first_topic(topic_id)
    if topic is None:
        diagnostics.append(
            Diagnostic(
                code="ISO013",
                severity="error",
                concept=TOPIC_CRUD_CONCEPT,
                field="topic_id",
                message=f"Research Topic is not registered by the Project Manifest: {topic_id}.",
            )
        )
        return TopicShowResult(project.root, None, None, None, None, diagnostics)

    workspace = _associated_workspace(project, topic_id, topic.topic_workspace_id)
    workspace_path = _workspace_path_for_registration(project, topic_id, workspace)
    topic_config = state.topic_configs.get(topic_id)
    return TopicShowResult(
        project_root=project.root,
        topic=topic.to_json(),
        topic_config=topic_config.to_json() if topic_config is not None else None,
        topic_workspace=workspace.to_json() if workspace is not None else None,
        topic_workspace_path=workspace_path,
        diagnostics=diagnostics,
    )


def update_research_topic(
    state: ProjectState,
    *,
    topic_id: str,
    statement: str | None = None,
    status: str | None = None,
    set_default: bool = False,
    new_id: str | None = None,
) -> TopicUpdateResult:
    project = state.project
    diagnostics: list[Diagnostic] = []
    updated_fields: list[str] = []
    topic = project.manifest.first_topic(topic_id)
    if topic is None:
        diagnostics.append(
            Diagnostic(
                code="ISO013",
                severity="error",
                concept=TOPIC_CRUD_CONCEPT,
                field="topic_id",
                message=f"Research Topic is not registered by the Project Manifest: {topic_id}.",
            )
        )
    if new_id is not None:
        diagnostics.append(
            Diagnostic(
                code="ISO003",
                severity="error",
                concept=TOPIC_CRUD_CONCEPT,
                field="new_id",
                message="Research Topic rename is not supported by `isomer-cli project topics update`.",
            )
        )
    normalized_statement = _normalized_statement(statement)
    if statement is not None:
        diagnostics.extend(_topic_statement_diagnostics(topic_id, normalized_statement))
    if status is not None and status not in VALID_TOPIC_STATUSES:
        diagnostics.append(
            Diagnostic(
                code="ISO003",
                severity="error",
                concept=TOPIC_CRUD_CONCEPT,
                field="status",
                message="Research Topic status must be active or archived.",
            )
        )
    if statement is None and status is None and not set_default and new_id is None:
        diagnostics.append(
            Diagnostic(
                code="ISO003",
                severity="error",
                concept=TOPIC_CRUD_CONCEPT,
                message="Select at least one topic update: --statement, --status, or --set-default.",
            )
        )
    if has_errors(diagnostics):
        return TopicUpdateResult(project.root, topic_id, tuple(updated_fields), False, diagnostics)

    assert topic is not None
    document = _read_manifest_document(project)
    if status is not None:
        for table in document.get("research_topics", []):
            if str(table.get("id", "")) == topic_id:
                table["status"] = status
                updated_fields.append("status")

    if set_default:
        workspace = _associated_workspace(project, topic_id, topic.topic_workspace_id)
        defaults = _ensure_table(document, "defaults")
        defaults["research_topic_id"] = topic_id
        defaults["topic_workspace_id"] = workspace.id if workspace is not None else topic_id
        updated_fields.extend(("defaults.research_topic_id", "defaults.topic_workspace_id"))

    if statement is not None:
        config_path = resolve_project_path(project.root, topic.config_path_input)
        config_document = _read_topic_config_document(config_path)
        config_document["topic_statement"] = normalized_statement or ""
        _atomic_write(config_path, tomlkit.dumps(config_document))
        updated_fields.append("topic_statement")

    _atomic_write(project.manifest_path, tomlkit.dumps(document))
    return TopicUpdateResult(project.root, topic_id, tuple(updated_fields), True, diagnostics)


def plan_delete_research_topic(
    state: ProjectState,
    *,
    topic_id: str,
    dry_run: bool,
    yes: bool,
) -> TopicDeletePlan:
    project = state.project
    diagnostics: list[Diagnostic] = []
    effective_dry_run = dry_run or not yes
    topic = project.manifest.first_topic(topic_id)
    topic_config_path = None
    topic_workspace_path = None
    preserved_paths: list[Path] = []
    removed_manifest_entries: list[str] = []
    cleared_defaults: list[str] = []
    blockers: list[str] = []

    if not dry_run and not yes:
        diagnostics.append(
            Diagnostic(
                code="ISO003",
                severity="error",
                concept=TOPIC_CRUD_CONCEPT,
                field="confirmation",
                message="Research Topic deletion requires --dry-run or --yes.",
            )
        )

    if topic is None:
        diagnostics.append(
            Diagnostic(
                code="ISO013",
                severity="error",
                concept=TOPIC_CRUD_CONCEPT,
                field="topic_id",
                message=f"Research Topic is not registered by the Project Manifest: {topic_id}.",
            )
        )
        return TopicDeletePlan(
            project_root=project.root,
            topic_id=topic_id,
            dry_run=effective_dry_run,
            confirmation_required=not yes,
            topic_config_path=topic_config_path,
            topic_workspace_path=topic_workspace_path,
            preserved_paths=tuple(preserved_paths),
            removed_manifest_entries=tuple(removed_manifest_entries),
            cleared_defaults=tuple(cleared_defaults),
            blockers=tuple(blockers),
            diagnostics=diagnostics,
        )

    topic_config_path = resolve_project_path(project.root, topic.config_path_input)
    workspace = _associated_workspace(project, topic_id, topic.topic_workspace_id)
    topic_workspace_path = _workspace_path_for_registration(project, topic_id, workspace)
    if topic_workspace_path is not None:
        preserved_paths.append(topic_workspace_path)

    removed_manifest_entries.append(f"research_topics.{topic_id}")
    if workspace is not None:
        removed_manifest_entries.append(f"topic_workspaces.{workspace.id}")

    if project.manifest.default_research_topic_id() == topic_id:
        cleared_defaults.append("defaults.research_topic_id")
    if workspace is not None and project.manifest.default_topic_workspace_id() == workspace.id:
        cleared_defaults.append("defaults.topic_workspace_id")

    blockers.extend(_delete_blockers(state, topic_id, topic_workspace_path))
    if blockers and not effective_dry_run:
        diagnostics.extend(
            Diagnostic(
                code="ISO016",
                severity="error",
                concept=TOPIC_CRUD_CONCEPT,
                field="topic_id",
                message=blocker,
            )
            for blocker in blockers
        )

    return TopicDeletePlan(
        project_root=project.root,
        topic_id=topic_id,
        dry_run=effective_dry_run,
        confirmation_required=not yes,
        topic_config_path=topic_config_path,
        topic_workspace_path=topic_workspace_path,
        preserved_paths=tuple(preserved_paths),
        removed_manifest_entries=tuple(removed_manifest_entries),
        cleared_defaults=tuple(cleared_defaults),
        blockers=tuple(blockers),
        diagnostics=diagnostics,
    )


def delete_research_topic(plan: TopicDeletePlan, project: Project) -> TopicDeleteResult:
    diagnostics = list(plan.diagnostics)
    if plan.dry_run:
        return TopicDeleteResult(plan=plan, mutated=False, removed_paths=(), diagnostics=diagnostics)
    if has_errors(diagnostics) or plan.blockers:
        return TopicDeleteResult(plan=plan, mutated=False, removed_paths=(), diagnostics=diagnostics)

    document = _read_manifest_document(project)
    _remove_table_by_id(document, "research_topics", plan.topic_id)
    topic = project.manifest.first_topic(plan.topic_id)
    workspace_ids = [
        workspace.id
        for workspace in project.manifest.topic_workspaces
        if workspace.research_topic_id == plan.topic_id
        or (topic is not None and workspace.id == topic.topic_workspace_id)
    ]
    for workspace_id in workspace_ids:
        _remove_table_by_id(document, "topic_workspaces", workspace_id)
    _clear_matching_defaults(document, plan.topic_id, tuple(workspace_ids))
    _atomic_write(project.manifest_path, tomlkit.dumps(document))

    removed_paths: list[Path] = []
    if plan.topic_config_path is not None and plan.topic_config_path.exists():
        plan.topic_config_path.unlink()
        removed_paths.append(plan.topic_config_path)

    return TopicDeleteResult(plan=plan, mutated=True, removed_paths=tuple(removed_paths), diagnostics=diagnostics)


def render_topic_create_text(result: TopicCreateResult) -> list[str]:
    if not result.ok:
        return []
    return [
        f"Created Research Topic: {result.topic_id}",
        f"Research Topic Config: {result.topic_config_path}",
        f"Topic Workspace: {result.topic_workspace_path}",
    ]


def render_topic_show_text(result: TopicShowResult) -> list[str]:
    if not result.ok or result.topic is None:
        return []
    lines = [f"Research Topic: {result.topic['id']}"]
    if result.topic_config is not None and result.topic_config.get("topic_statement") is not None:
        lines.append(f"Topic Statement: {result.topic_config['topic_statement']}")
    if result.topic_workspace_path is not None:
        lines.append(f"Topic Workspace: {result.topic_workspace_path}")
    return lines


def render_topic_update_text(result: TopicUpdateResult) -> list[str]:
    if not result.ok:
        return []
    return [
        f"Updated Research Topic: {result.topic_id}",
        "Updated fields: " + ", ".join(result.updated_fields),
    ]


def render_topic_delete_text(result: TopicDeleteResult) -> list[str]:
    plan = result.plan
    lines = [f"Research Topic deletion plan: {plan.topic_id}", f"Mode: {'dry-run' if plan.dry_run else 'confirmed'}"]
    if plan.blockers:
        lines.extend(f"Blocker: {blocker}" for blocker in plan.blockers)
    if plan.preserved_paths:
        lines.extend(f"Preserved workspace: {path}" for path in plan.preserved_paths)
    if result.mutated:
        lines.append("Research Topic deleted; workspace contents preserved.")
    elif plan.dry_run:
        lines.append("Dry-run only. Pass --yes to apply after review.")
    return lines


def _workspace_target(project: Project, topic_id: str, workspace_dir: str | None) -> tuple[Path, str]:
    if workspace_dir is not None and workspace_dir:
        path = resolve_project_path(project.root, workspace_dir)
        return path, display_path(path, project.root)
    path = default_topic_workspace_path(project.root, topic_id, project.manifest.path_defaults)
    return path, topic_workspace_path_input_from_defaults(topic_id, project.manifest.path_defaults)


def _topic_id_diagnostics(topic_id: str) -> list[Diagnostic]:
    if TOPIC_ID_PATTERN.fullmatch(topic_id) is not None:
        return []
    return [
        Diagnostic(
            code="ISO003",
            severity="error",
            concept=TOPIC_CRUD_CONCEPT,
            field="topic_id",
            message="Research Topic id must start with an alphanumeric character and contain only letters, numbers, dot, underscore, or hyphen.",
        )
    ]


def _topic_statement_diagnostics(topic_id: str, statement: str | None) -> list[Diagnostic]:
    if statement is None or not statement:
        return [
            Diagnostic(
                code="ISO003",
                severity="error",
                concept=TOPIC_CRUD_CONCEPT,
                field="statement",
                message="Research Topic creation requires a concrete --statement.",
            )
        ]
    lowered = statement.casefold()
    placeholders = {
        "default research topic",
        f"{topic_id.casefold()} research topic",
        topic_id.casefold(),
    }
    if lowered in placeholders:
        return [
            Diagnostic(
                code="ISO003",
                severity="error",
                concept=TOPIC_CRUD_CONCEPT,
                field="statement",
                message="Research Topic statement must be concrete and must not be a generic placeholder.",
            )
        ]
    return []


def _normalized_statement(statement: str | None) -> str | None:
    if statement is None:
        return None
    return statement.strip()


def _topic_create_collision_diagnostics(
    project: Project,
    topic_id: str,
    topic_config_path: Path,
    workspace_path: Path,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if project.manifest.first_topic(topic_id) is not None:
        diagnostics.append(
            Diagnostic(
                code="ISO003",
                severity="error",
                concept=TOPIC_CRUD_CONCEPT,
                field="topic_id",
                message=f"Research Topic is already registered by the Project Manifest: {topic_id}.",
            )
        )
    if project.manifest.first_workspace(topic_id) is not None:
        diagnostics.append(
            Diagnostic(
                code="ISO003",
                severity="error",
                concept="Topic Workspace",
                field="topic_workspace_id",
                message=f"Topic Workspace id is already registered by the Project Manifest: {topic_id}.",
            )
        )
    if topic_config_path.exists():
        diagnostics.append(
            Diagnostic(
                code="ISO003",
                severity="error",
                concept=TOPIC_CRUD_CONCEPT,
                path=topic_config_path,
                message="Research Topic Config path already exists.",
            )
        )
    diagnostics.extend(_workspace_path_diagnostics(project, workspace_path))
    return diagnostics


def _workspace_path_diagnostics(project: Project, workspace_path: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    reserved = {
        project.config_dir: "Project Config Directory",
        houmao_overlay_dir_for_root(project.root): "Isomer-managed Houmao overlay",
        root_houmao_overlay_dir_for_root(project.root): "root .houmao external Houmao state",
    }
    if not is_within(workspace_path, project.root):
        diagnostics.append(
            Diagnostic(
                code="ISO005",
                severity="error",
                concept="Topic Workspace",
                path=workspace_path,
                field="workspace_dir",
                message="Topic Workspace path resolves outside the Project root.",
            )
        )
    if workspace_path == project.root:
        diagnostics.append(
            Diagnostic(
                code="ISO005",
                severity="error",
                concept="Topic Workspace",
                path=workspace_path,
                field="workspace_dir",
                message="Topic Workspace path must not be the Project root.",
            )
        )
    for reserved_path, label in reserved.items():
        if workspace_path == reserved_path or is_within(workspace_path, reserved_path):
            diagnostics.append(
                Diagnostic(
                    code="ISO005",
                    severity="error",
                    concept="Topic Workspace",
                    path=workspace_path,
                    field="workspace_dir",
                    message=f"Topic Workspace path must not live inside {label}.",
                )
            )
    for workspace in project.manifest.topic_workspaces:
        existing_path = _workspace_path_for_registration(project, workspace.research_topic_id or workspace.id, workspace)
        if existing_path is None:
            continue
        if workspace_path == existing_path or is_within(workspace_path, existing_path) or is_within(existing_path, workspace_path):
            diagnostics.append(
                Diagnostic(
                    code="ISO005",
                    severity="error",
                    concept="Topic Workspace",
                    path=workspace_path,
                    field="workspace_dir",
                    message=f"Topic Workspace path collides with registered Topic Workspace: {workspace.id}.",
                )
            )
    return diagnostics


def _associated_workspace(project: Project, topic_id: str, workspace_id: str | None) -> TopicWorkspaceRegistration | None:
    if workspace_id is not None:
        return project.manifest.first_workspace(workspace_id)
    matches = [workspace for workspace in project.manifest.topic_workspaces if workspace.research_topic_id == topic_id]
    if len(matches) == 1:
        return matches[0]
    return None


def _workspace_path_for_registration(
    project: Project,
    topic_id: str,
    workspace: TopicWorkspaceRegistration | None,
) -> Path | None:
    if workspace is None:
        return default_topic_workspace_path(project.root, topic_id, project.manifest.path_defaults)
    if workspace.path_input is not None:
        return resolve_project_path(project.root, workspace.path_input)
    if workspace.research_topic_id is not None:
        return default_topic_workspace_path(project.root, workspace.research_topic_id, project.manifest.path_defaults)
    return None


def _delete_blockers(state: ProjectState, topic_id: str, workspace_path: Path | None) -> list[str]:
    blockers: list[str] = []
    profile_ids = sorted(
        profile.id for profile in state.project.manifest.topic_agent_team_profiles if profile.research_topic_id == topic_id
    )
    if profile_ids:
        blockers.append("Topic Agent Team Profile registrations depend on this Research Topic: " + ", ".join(profile_ids))
    if workspace_path is not None:
        markers = [
            workspace_path / RUNTIME_DB_FILENAME,
            workspace_path / ADAPTER_MANIFEST_ROOT,
            workspace_path / "runtime",
            *(workspace_path / directory for directory in RUNTIME_DIRECTORIES),
        ]
        existing_markers = [marker for marker in markers if marker.exists()]
        if existing_markers:
            names = ", ".join(str(marker.relative_to(workspace_path)) for marker in existing_markers)
            blockers.append(f"Topic Workspace contains runtime or adapter material: {names}")
    return blockers


def _read_manifest_document(project: Project) -> Any:
    return tomlkit.parse(project.manifest_path.read_text(encoding="utf-8"))


def _read_topic_config_document(path: Path) -> Any:
    if not path.exists():
        document = tomlkit.document()
        document["schema_version"] = RESEARCH_TOPIC_SCHEMA_VERSION
        return document
    return tomlkit.parse(path.read_text(encoding="utf-8"))


def _ensure_table(document: Any, key: str) -> Any:
    try:
        value = document[key]
        if value is not None:
            return value
    except KeyError:
        pass
    table = tomlkit.table()
    document[key] = table
    return table


def _ensure_aot(document: Any, key: str) -> Any:
    try:
        value = document[key]
        if value is not None:
            return value
    except KeyError:
        pass
    aot = tomlkit.aot()
    document[key] = aot
    return aot


def _remove_table_by_id(document: Any, key: str, value: str) -> None:
    existing = document.get(key)
    if existing is None:
        return
    replacement = tomlkit.aot()
    for table in existing:
        if str(table.get("id", "")) != value:
            replacement.append(table)
    if len(replacement) == 0:
        del document[key]
    else:
        document[key] = replacement


def _clear_matching_defaults(document: Any, topic_id: str, workspace_ids: tuple[str, ...]) -> None:
    defaults = document.get("defaults")
    if defaults is None:
        return
    if defaults.get("research_topic_id") == topic_id:
        del defaults["research_topic_id"]
    if defaults.get("topic_workspace_id") in workspace_ids:
        del defaults["topic_workspace_id"]
    if len(defaults) == 0:
        del document["defaults"]


def _topic_config_text(topic_id: str, statement: str) -> str:
    document = tomlkit.document()
    document["schema_version"] = RESEARCH_TOPIC_SCHEMA_VERSION
    document["research_topic_id"] = topic_id
    document["topic_statement"] = statement
    document["measurable_objectives"] = []
    return tomlkit.dumps(document)


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(f".{path.name}.tmp")
    temp_path.write_text(content, encoding="utf-8")
    os.replace(temp_path, path)
