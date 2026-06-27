"""Topic Workspace Manifest and semantic workspace surface helpers."""

from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Mapping

from isomer_labs.diagnostics import Diagnostic
from isomer_labs.local_tmp_surfaces import ensure_tmp_surface_ignore_policy
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.path_utils import canonicalize, is_within, resolve_project_path
from isomer_labs.semantic_surfaces import (
    LOCAL_TMP_SURFACE_LABELS,
    PATH_ENV_VARS_BY_LABEL,
    STANDARD_TOPIC_MATERIALIZATION_LABELS,
    SemanticSurface,
    catalog,
    compatibility_aliases as compatibility_aliases,
    compatibility_surface_for_label,
    semantic_label_for_surface as semantic_label_for_surface,
)
from isomer_labs.toml_loader import load_toml


TOPIC_WORKSPACE_MANIFEST_SCHEMA_VERSION = "isomer-topic-workspace-manifest.v1"
TOPIC_WORKSPACE_MANIFEST_FILENAME = "topic-workspace.toml"
DEFAULT_LAYOUT_PROFILE = "isomer-default.v1"
MANIFEST_SOURCE = "topic_workspace_manifest"
DEFAULT_PROFILE_SOURCE = "default_profile"
PROJECT_MANIFEST_SOURCE = "project_manifest"
PATH_PLAN_SOURCE = "path_plan"


@dataclass(frozen=True)
class TopicWorkspaceBinding:
    label: str
    path_template: str
    owner: str
    durability: str
    sharing: str
    status: str = "active"
    source_detail: str | None = None

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "label": self.label,
            "path_template": self.path_template,
            "owner": self.owner,
            "durability": self.durability,
            "sharing": self.sharing,
            "status": self.status,
        }
        if self.source_detail is not None:
            data["source_detail"] = self.source_detail
        return data


@dataclass(frozen=True)
class TopicWorkspaceManifest:
    path: Path
    schema_version: str
    research_topic_id: str | None
    topic_workspace_id: str | None
    layout_profile: str
    bindings: tuple[TopicWorkspaceBinding, ...]
    exists: bool

    def active_bindings(self) -> tuple[TopicWorkspaceBinding, ...]:
        return tuple(binding for binding in self.bindings if binding.status == "active")

    def binding_for(self, label: str) -> TopicWorkspaceBinding | None:
        return next((binding for binding in self.active_bindings() if binding.label == label), None)

    def to_json(self) -> dict[str, object]:
        return {
            "path": str(self.path),
            "schema_version": self.schema_version,
            "research_topic_id": self.research_topic_id,
            "topic_workspace_id": self.topic_workspace_id,
            "layout_profile": self.layout_profile,
            "exists": self.exists,
            "bindings": [binding.to_json() for binding in self.bindings],
        }


@dataclass(frozen=True)
class SemanticPathResult:
    label: str
    path: Path
    source: str
    source_detail: str | None
    catalog: SemanticSurface
    scope_ref: str
    compatibility_surface: str
    exists: bool
    agent_name: str | None = None
    agent_instance_id: str | None = None
    agent_context_source: str | None = None

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "semantic_label": self.label,
            "path": str(self.path),
            "source": self.source,
            "scope": self.catalog.scope,
            "scope_ref": self.scope_ref,
            "compatibility_surface": self.compatibility_surface,
            "owner": self.catalog.owner,
            "durability": self.catalog.durability,
            "sharing": self.catalog.sharing,
            "path_kind": self.catalog.path_kind,
            "exists": self.exists,
        }
        if self.source_detail is not None:
            data["source_detail"] = self.source_detail
        if self.agent_name is not None:
            data["agent_name"] = self.agent_name
        if self.agent_instance_id is not None:
            data["agent_instance_id"] = self.agent_instance_id
        if self.agent_context_source is not None:
            data["agent_context_source"] = self.agent_context_source
        return data


@dataclass(frozen=True)
class EffectiveAgentContext:
    agent_name: str
    agent_workspace_path: Path
    source: str
    agent_instance_id: str | None = None

    @property
    def scope_ref(self) -> str:
        if self.agent_instance_id is not None:
            return f"agent_instance:{self.agent_instance_id}"
        return f"agent_name:{self.agent_name}"

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "agent_name": self.agent_name,
            "agent_workspace_path": str(self.agent_workspace_path),
            "source": self.source,
        }
        if self.agent_instance_id is not None:
            data["agent_instance_id"] = self.agent_instance_id
        return data


def topic_workspace_manifest_path(topic_workspace_path: Path) -> Path:
    return topic_workspace_path / TOPIC_WORKSPACE_MANIFEST_FILENAME


def load_topic_workspace_manifest(context: EffectiveTopicContext) -> tuple[TopicWorkspaceManifest, list[Diagnostic]]:
    manifest_path = topic_workspace_manifest_path(context.topic_workspace_path)
    if not manifest_path.exists():
        return (
            TopicWorkspaceManifest(
                path=manifest_path,
                schema_version=TOPIC_WORKSPACE_MANIFEST_SCHEMA_VERSION,
                research_topic_id=context.research_topic.id,
                topic_workspace_id=context.topic_workspace_id,
                layout_profile=DEFAULT_LAYOUT_PROFILE,
                bindings=(),
                exists=False,
            ),
            [],
        )
    raw, diagnostics = load_toml(manifest_path, "Topic Workspace Manifest")
    if raw is None:
        return (
            TopicWorkspaceManifest(
                path=manifest_path,
                schema_version=TOPIC_WORKSPACE_MANIFEST_SCHEMA_VERSION,
                research_topic_id=None,
                topic_workspace_id=None,
                layout_profile=DEFAULT_LAYOUT_PROFILE,
                bindings=(),
                exists=True,
            ),
            diagnostics,
        )
    manifest = parse_topic_workspace_manifest(manifest_path, raw)
    diagnostics.extend(validate_topic_workspace_manifest(context, manifest))
    return manifest, diagnostics


def parse_topic_workspace_manifest(path: Path, raw: Mapping[str, Any]) -> TopicWorkspaceManifest:
    bindings: list[TopicWorkspaceBinding] = []
    for table_name in ("bindings", "surface_bindings", "agent_bindings"):
        for index, item in enumerate(_table_items(raw.get(table_name))):
            label = _string(item.get("label") or item.get("semantic_label"))
            path_template = _string(item.get("path_template") or item.get("path") or item.get("template"))
            if label is None or path_template is None:
                continue
            surface = catalog().get(label)
            bindings.append(
                TopicWorkspaceBinding(
                    label=label,
                    path_template=path_template,
                    owner=_string(item.get("owner")) or (surface.owner if surface is not None else "custom"),
                    durability=_string(item.get("durability")) or (surface.durability if surface is not None else "unknown"),
                    sharing=_string(item.get("sharing")) or (surface.sharing if surface is not None else "unknown"),
                    status=_string(item.get("status")) or "active",
                    source_detail=f"{path.name}:{table_name}[{index}]",
                )
            )
    return TopicWorkspaceManifest(
        path=path,
        schema_version=_string(raw.get("schema_version")) or TOPIC_WORKSPACE_MANIFEST_SCHEMA_VERSION,
        research_topic_id=_string(raw.get("research_topic_id")),
        topic_workspace_id=_string(raw.get("topic_workspace_id")),
        layout_profile=_string(raw.get("layout_profile")) or DEFAULT_LAYOUT_PROFILE,
        bindings=tuple(bindings),
        exists=True,
    )


def validate_topic_workspace_manifest(
    context: EffectiveTopicContext,
    manifest: TopicWorkspaceManifest,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if not manifest.exists:
        return diagnostics
    if manifest.schema_version != TOPIC_WORKSPACE_MANIFEST_SCHEMA_VERSION:
        diagnostics.append(
            Diagnostic(
                code="ISO060",
                severity="error",
                concept="Topic Workspace Manifest",
                path=manifest.path,
                field="schema_version",
                message=f"Unsupported Topic Workspace Manifest schema version: {manifest.schema_version}.",
            )
        )
    if manifest.research_topic_id is not None and manifest.research_topic_id != context.research_topic.id:
        diagnostics.append(
            Diagnostic(
                code="ISO060",
                severity="error",
                concept="Topic Workspace Manifest",
                path=manifest.path,
                field="research_topic_id",
                message="Topic Workspace Manifest research_topic_id does not match the selected Research Topic.",
            )
        )
    if manifest.topic_workspace_id is not None and manifest.topic_workspace_id != context.topic_workspace_id:
        diagnostics.append(
            Diagnostic(
                code="ISO060",
                severity="error",
                concept="Topic Workspace Manifest",
                path=manifest.path,
                field="topic_workspace_id",
                message="Topic Workspace Manifest topic_workspace_id does not match the selected Topic Workspace.",
            )
        )
    seen: set[str] = set()
    for binding in manifest.active_bindings():
        surface = catalog().get(binding.label)
        if surface is None:
            diagnostics.append(
                Diagnostic(
                    code="ISO060",
                    severity="error",
                    concept="Topic Workspace Manifest",
                    path=manifest.path,
                    field=binding.label,
                    message="Unknown semantic surface label.",
                )
            )
            continue
        if binding.label in seen:
            diagnostics.append(
                Diagnostic(
                    code="ISO060",
                    severity="error",
                    concept="Topic Workspace Manifest",
                    path=manifest.path,
                    field=binding.label,
                    message="Duplicate active semantic surface binding.",
                )
            )
        seen.add(binding.label)
        if binding.label == "agent.workspace":
            diagnostics.extend(_validate_agent_workspace_template(binding, manifest.path))
        if surface.scope == "topic":
            path = resolve_binding_path(context, binding, agent_name=None)
            diagnostics.extend(_path_safety_diagnostics(context, path, binding.label, manifest.path, scope="topic"))
            diagnostics.extend(_manifest_tmp_surface_boundary_diagnostics(context, manifest, binding.label, path))
    return diagnostics


def resolve_semantic_binding(
    context: EffectiveTopicContext,
    label: str,
    *,
    env: Mapping[str, str],
    agent_context: EffectiveAgentContext | None = None,
) -> tuple[SemanticPathResult | None, list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    surface = catalog().get(label)
    if surface is None:
        diagnostics.append(
            Diagnostic(
                code="ISO061",
                severity="error",
                concept="Workspace Path Resolution",
                field=label,
                message="Unknown semantic surface label.",
            )
        )
        return None, diagnostics
    if surface.scope == "agent" and agent_context is None:
        diagnostics.append(
            Diagnostic(
                code="ISO061",
                severity="error",
                concept="Effective Agent Context",
                field=label,
                message="Agent-scoped semantic label requires an Agent Name or Agent Instance selector.",
            )
        )
        return None, diagnostics
    env_var = PATH_ENV_VARS_BY_LABEL.get(label)
    if env_var is not None and env.get(env_var):
        path = resolve_project_path(context.project.root, env[env_var])
        result = _result(context, surface, path, "env", env_var, agent_context)
        diagnostics.extend(_path_safety_diagnostics(context, result.path, label, None, scope=surface.scope))
        diagnostics.extend(_tmp_surface_boundary_diagnostics(context, label, result.path, env=env, agent_context=agent_context))
        return result if not any(d.is_error for d in diagnostics) else None, diagnostics
    manifest, manifest_diagnostics = load_topic_workspace_manifest(context)
    diagnostics.extend(manifest_diagnostics)
    if any(d.is_error for d in diagnostics):
        return None, diagnostics
    binding = manifest.binding_for(label)
    if binding is not None:
        path = resolve_binding_path(context, binding, agent_name=agent_context.agent_name if agent_context is not None else None)
        result = _result(context, surface, path, MANIFEST_SOURCE, binding.source_detail or str(manifest.path), agent_context)
        diagnostics.extend(_path_safety_diagnostics(context, result.path, label, manifest.path, scope=surface.scope))
        diagnostics.extend(_tmp_surface_boundary_diagnostics(context, label, result.path, env=env, agent_context=agent_context))
        return result if not any(d.is_error for d in diagnostics) else None, diagnostics
    path = _default_path_for_result(context, surface, label, agent_context)
    result = _result(context, surface, path, DEFAULT_PROFILE_SOURCE, DEFAULT_LAYOUT_PROFILE, agent_context)
    diagnostics.extend(_path_safety_diagnostics(context, result.path, label, None, scope=surface.scope))
    diagnostics.extend(_tmp_surface_boundary_diagnostics(context, label, result.path, env=env, agent_context=agent_context))
    return result if not any(d.is_error for d in diagnostics) else None, diagnostics


def default_path_for_label(context: EffectiveTopicContext, label: str, *, agent_name: str | None) -> Path:
    surface = catalog()[label]
    return _resolve_template(context.topic_workspace_path, surface.default_template, agent_name=agent_name)


def resolve_binding_path(
    context: EffectiveTopicContext,
    binding: TopicWorkspaceBinding,
    *,
    agent_name: str | None,
) -> Path:
    path = _resolve_template(context.topic_workspace_path, binding.path_template, agent_name=agent_name)
    return path


def _default_path_for_result(
    context: EffectiveTopicContext,
    surface: SemanticSurface,
    label: str,
    agent_context: EffectiveAgentContext | None,
) -> Path:
    if surface.scope != "agent" or agent_context is None or label == "agent.workspace":
        return default_path_for_label(context, label, agent_name=agent_context.agent_name if agent_context is not None else None)
    default_workspace = default_path_for_label(context, "agent.workspace", agent_name=agent_context.agent_name)
    default_path = default_path_for_label(context, label, agent_name=agent_context.agent_name)
    try:
        suffix = default_path.relative_to(default_workspace)
    except ValueError:
        return default_path
    return (agent_context.agent_workspace_path / suffix).resolve(strict=False)


def materialize_default_manifest(
    context: EffectiveTopicContext,
    *,
    labels: tuple[str, ...],
    agent_name: str | None,
) -> tuple[TopicWorkspaceManifest | None, list[Path], list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    selected_labels = labels or STANDARD_TOPIC_MATERIALIZATION_LABELS
    for label in selected_labels:
        surface = catalog().get(label)
        if surface is None:
            diagnostics.append(
                Diagnostic(
                    code="ISO061",
                    severity="error",
                    concept="Workspace Path Resolution",
                    field=label,
                    message="Unknown semantic surface label.",
                )
            )
        elif surface.scope == "agent" and agent_name is None:
            diagnostics.append(
                Diagnostic(
                    code="ISO061",
                    severity="error",
                    concept="Effective Agent Context",
                    field=label,
                    message="Default materialization of agent-scoped labels requires an Agent Name selector.",
                )
            )
    if any(diagnostic.is_error for diagnostic in diagnostics):
        return None, [], diagnostics

    manifest, load_diagnostics = load_topic_workspace_manifest(context)
    diagnostics.extend(load_diagnostics)
    if any(diagnostic.is_error for diagnostic in diagnostics):
        return None, [], diagnostics
    existing = {binding.label: binding for binding in manifest.bindings}
    for label in selected_labels:
        surface = catalog()[label]
        if label not in existing:
            existing[label] = TopicWorkspaceBinding(
                label=label,
                path_template=surface.default_template,
                owner=surface.owner,
                durability=surface.durability,
                sharing=surface.sharing,
                status="active",
                source_detail=f"{TOPIC_WORKSPACE_MANIFEST_FILENAME}:materialize-default",
            )
    next_manifest = replace(
        manifest,
        schema_version=TOPIC_WORKSPACE_MANIFEST_SCHEMA_VERSION,
        research_topic_id=context.research_topic.id,
        topic_workspace_id=context.topic_workspace_id,
        layout_profile=DEFAULT_LAYOUT_PROFILE,
        bindings=tuple(existing[label] for label in sorted(existing)),
        exists=True,
    )
    diagnostics.extend(validate_topic_workspace_manifest(context, next_manifest))
    if any(diagnostic.is_error for diagnostic in diagnostics):
        return None, [], diagnostics
    manifest.path.parent.mkdir(parents=True, exist_ok=True)
    manifest.path.write_text(render_topic_workspace_manifest(next_manifest), encoding="utf-8")
    created: list[Path] = []
    for label in selected_labels:
        surface = catalog()[label]
        path = default_path_for_label(context, label, agent_name=agent_name)
        if surface.path_kind == "directory":
            path.mkdir(parents=True, exist_ok=True)
            created.append(path)
            if label in LOCAL_TMP_SURFACE_LABELS:
                agent_context = (
                    EffectiveAgentContext(
                        agent_name=agent_name,
                        agent_workspace_path=default_path_for_label(context, "agent.workspace", agent_name=agent_name),
                        source="materialize-default",
                    )
                    if surface.scope == "agent" and agent_name is not None
                    else None
                )
                diagnostics.extend(ensure_tmp_surface_ignore_policy(context, label, path, env={}, agent_context=agent_context))
        elif surface.path_kind == "file":
            path.parent.mkdir(parents=True, exist_ok=True)
            created.append(path.parent)
    return next_manifest, created, diagnostics


def render_topic_workspace_manifest(manifest: TopicWorkspaceManifest) -> str:
    lines = [
        f"schema_version = {_toml_string(manifest.schema_version)}",
        f"research_topic_id = {_toml_string(manifest.research_topic_id or '')}",
        f"topic_workspace_id = {_toml_string(manifest.topic_workspace_id or '')}",
        f"layout_profile = {_toml_string(manifest.layout_profile)}",
        "",
    ]
    for binding in sorted(manifest.bindings, key=lambda item: item.label):
        lines.extend(
            [
                "[[bindings]]",
                f"label = {_toml_string(binding.label)}",
                f"path_template = {_toml_string(binding.path_template)}",
                f"owner = {_toml_string(binding.owner)}",
                f"durability = {_toml_string(binding.durability)}",
                f"sharing = {_toml_string(binding.sharing)}",
                f"status = {_toml_string(binding.status)}",
                "",
            ]
        )
    return "\n".join(lines)


def match_agent_name_from_template(
    topic_workspace_path: Path,
    template: str,
    cwd: Path,
) -> tuple[str | None, Path | None, str | None]:
    parts = Path(template).parts
    placeholder_count = sum(1 for part in parts if part == "{agent_name}")
    if placeholder_count != 1:
        return None, None, "agent.workspace template must contain exactly one {agent_name} path segment."
    if any("{agent_name}" in part and part != "{agent_name}" for part in parts):
        return None, None, "{agent_name} must occupy a whole path segment."
    canonical_cwd = canonicalize(cwd)
    placeholder_index = parts.index("{agent_name}")
    prefix = topic_workspace_path.joinpath(*parts[:placeholder_index]).resolve(strict=False)
    suffix = parts[placeholder_index + 1 :]
    try:
        relative = canonical_cwd.relative_to(prefix)
    except ValueError:
        return None, None, None
    relative_parts = relative.parts
    if not relative_parts:
        return None, None, None
    agent_name = relative_parts[0]
    workspace_root = prefix / agent_name
    if suffix:
        workspace_root = workspace_root.joinpath(*suffix)
        try:
            canonical_cwd.relative_to(workspace_root)
        except ValueError:
            return None, None, None
    return agent_name, workspace_root.resolve(strict=False), None


def _result(
    context: EffectiveTopicContext,
    surface: SemanticSurface,
    path: Path,
    source: str,
    source_detail: str | None,
    agent_context: EffectiveAgentContext | None,
) -> SemanticPathResult:
    compatibility_surface = compatibility_surface_for_label(surface.label, agent_name=agent_context.agent_name if agent_context is not None else None)
    scope_ref = f"topic_workspace:{context.topic_workspace_id}"
    if surface.scope == "agent" and agent_context is not None:
        scope_ref = agent_context.scope_ref
    return SemanticPathResult(
        label=surface.label,
        path=path.resolve(strict=False),
        source=source,
        source_detail=source_detail,
        catalog=surface,
        scope_ref=scope_ref,
        compatibility_surface=compatibility_surface or surface.compatibility_surface,
        exists=path.exists(),
        agent_name=agent_context.agent_name if agent_context is not None else None,
        agent_instance_id=agent_context.agent_instance_id if agent_context is not None else None,
        agent_context_source=agent_context.source if agent_context is not None else None,
    )


def _resolve_template(topic_workspace_path: Path, template: str, *, agent_name: str | None) -> Path:
    value = template
    if agent_name is not None:
        value = value.replace("{agent_name}", agent_name)
    if "{agent_name}" in value:
        value = value.replace("{agent_name}", "agent-name-required")
    candidate = Path(value).expanduser()
    if candidate.is_absolute():
        return candidate.resolve(strict=False)
    return (topic_workspace_path / candidate).resolve(strict=False)


def _path_safety_diagnostics(
    context: EffectiveTopicContext,
    path: Path,
    label: str,
    manifest_path: Path | None,
    *,
    scope: str,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if not is_within(path, context.project.root):
        diagnostics.append(
            Diagnostic(
                code="ISO005",
                severity="error",
                concept="Workspace Path Resolution",
                path=manifest_path,
                field=label,
                message="Manifest-backed semantic path points outside the Project root.",
            )
        )
    if is_within(path, context.project.config_dir):
        diagnostics.append(
            Diagnostic(
                code="ISO005",
                severity="error",
                concept="Workspace Path Resolution",
                path=manifest_path,
                field=label,
                message="Topic Workspace body material must not live inside the Project Config Directory.",
            )
        )
    if scope == "agent" and not is_within(path, context.topic_workspace_path):
        diagnostics.append(
            Diagnostic(
                code="ISO005",
                severity="error",
                concept="Workspace Path Resolution",
                path=manifest_path,
                field=label,
                message="Agent-scoped semantic path points outside the selected Topic Workspace.",
            )
        )
    for workspace_path in _registered_other_topic_workspace_paths(context):
        if is_within(path, workspace_path):
            diagnostics.append(
                Diagnostic(
                    code="ISO005",
                    severity="error",
                    concept="Workspace Path Resolution",
                    path=manifest_path,
                    field=label,
                    message="Semantic binding points into another registered Topic Workspace.",
                )
            )
            break
    return diagnostics


def _registered_other_topic_workspace_paths(context: EffectiveTopicContext) -> list[Path]:
    paths: list[Path] = []
    for workspace in context.project.manifest.topic_workspaces:
        if workspace.id == context.topic_workspace_id or workspace.path_input is None:
            continue
        paths.append(resolve_project_path(context.project.root, workspace.path_input))
    return paths


def _manifest_tmp_surface_boundary_diagnostics(
    context: EffectiveTopicContext,
    manifest: TopicWorkspaceManifest,
    label: str,
    path: Path,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if label == "topic.tmp" and not is_within(path, context.topic_workspace_path):
        diagnostics.append(_tmp_boundary_diagnostic(manifest.path, label, "Local Tmp Surface must stay inside the selected Topic Workspace."))
    if label == "topic.main_repo.tmp":
        topic_main_binding = manifest.binding_for("topic.main_repo")
        topic_main_path = (
            resolve_binding_path(context, topic_main_binding, agent_name=None)
            if topic_main_binding is not None
            else default_path_for_label(context, "topic.main_repo", agent_name=None)
        )
        if not is_within(path, topic_main_path):
            diagnostics.append(_tmp_boundary_diagnostic(manifest.path, label, "`topic.main_repo.tmp` must stay inside `topic.main_repo`."))
    return diagnostics


def _tmp_surface_boundary_diagnostics(
    context: EffectiveTopicContext,
    label: str,
    path: Path,
    *,
    env: Mapping[str, str],
    agent_context: EffectiveAgentContext | None,
) -> list[Diagnostic]:
    if label not in LOCAL_TMP_SURFACE_LABELS:
        return []
    diagnostics: list[Diagnostic] = []
    if label == "topic.tmp":
        if not is_within(path, context.topic_workspace_path):
            diagnostics.append(_tmp_boundary_diagnostic(None, label, "Local Tmp Surface must stay inside the selected Topic Workspace."))
        return diagnostics
    if label == "topic.main_repo.tmp":
        topic_main, topic_main_diagnostics = resolve_semantic_binding(context, "topic.main_repo", env=env, agent_context=None)
        diagnostics.extend(topic_main_diagnostics)
        if topic_main is not None and not is_within(path, topic_main.path):
            diagnostics.append(_tmp_boundary_diagnostic(None, label, "`topic.main_repo.tmp` must stay inside `topic.main_repo`."))
        return diagnostics
    if label == "agent.tmp":
        if agent_context is None:
            return diagnostics
        if not is_within(path, agent_context.agent_workspace_path):
            diagnostics.append(_tmp_boundary_diagnostic(None, label, "`agent.tmp` must stay inside the resolved `agent.workspace`."))
        return diagnostics
    return diagnostics


def _tmp_boundary_diagnostic(path: Path | None, label: str, message: str) -> Diagnostic:
    return Diagnostic(
        code="ISO005",
        severity="error",
        concept="Workspace Path Resolution",
        path=path,
        field=label,
        message=message,
    )


def _validate_agent_workspace_template(binding: TopicWorkspaceBinding, path: Path) -> list[Diagnostic]:
    _, _, issue = match_agent_name_from_template(Path("/topic-workspace"), binding.path_template, Path("/topic-workspace/agents/example"))
    if issue is None:
        return []
    return [
        Diagnostic(
            code="ISO060",
            severity="error",
            concept="Topic Workspace Manifest",
            path=path,
            field=binding.label,
            message=issue,
        )
    ]


def _table_items(value: object) -> list[Mapping[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, Mapping)]


def _string(value: object) -> str | None:
    return value if isinstance(value, str) and value else None


def _toml_string(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'
