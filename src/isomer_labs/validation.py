"""Project Manifest, Research Topic Config, and local context validation."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from isomer_labs.diagnostics import Diagnostic
from isomer_labs.models import Project, ProjectState, ResearchTopicConfig
from isomer_labs.path_utils import is_within, resolve_project_path
from isomer_labs.toml_loader import load_toml
from isomer_labs.topic_config import parse_local_active_context, parse_research_topic_config


SECRET_TERMS = (
    "secret",
    "token",
    "api_key",
    "apikey",
    "password",
    "credential",
    "private_key",
    "access_key",
    "client_secret",
)
RUNTIME_TRUTH_KEYS = {
    "run_status",
    "command_output",
    "command_outputs",
    "live_process_id",
    "live_process_ids",
    "resolved_command_result",
    "resolved_command_results",
    "artifact_contents",
    "evidence_items",
    "findings",
    "gates",
    "decision_records",
    "provenance_records",
    "scheduler_internals",
    "provider_payload",
    "provider_payloads",
}


def build_project_state(project: Project) -> ProjectState:
    diagnostics: list[Diagnostic] = []
    diagnostics.extend(scan_for_forbidden_fields(project.manifest.raw, "Project Manifest", project.manifest_path))
    diagnostics.extend(_duplicate_id_diagnostics(project))
    diagnostics.extend(_validate_workspace_registrations(project))

    topic_configs: dict[str, ResearchTopicConfig] = {}
    for topic in project.manifest.research_topics:
        config_path = resolve_project_path(project.root, topic.config_path_input)
        if not is_within(config_path, project.root):
            diagnostics.append(
                Diagnostic(
                    code="ISO005",
                    severity="error",
                    concept="Research Topic Config",
                    path=project.manifest_path,
                    field=f"research_topics.{topic.id}.config_path",
                    message="Research Topic Config path resolves outside the Project root.",
                )
            )
            continue
        raw, load_diagnostics = load_toml(config_path, "Research Topic Config")
        diagnostics.extend(load_diagnostics)
        if raw is None:
            continue
        diagnostics.extend(scan_for_forbidden_fields(raw, "Research Topic Config", config_path))
        config, parse_diagnostics = parse_research_topic_config(config_path, raw)
        diagnostics.extend(parse_diagnostics)
        if config is None:
            continue
        if config.research_topic_id != topic.id:
            diagnostics.append(
                Diagnostic(
                    code="ISO007",
                    severity="error",
                    concept="Research Topic Config",
                    path=config_path,
                    field="research_topic_id",
                    message="Research Topic Config research_topic_id does not match the Project Manifest registration.",
                )
            )
        topic_configs.setdefault(topic.id, config)

    local_context = None
    local_path = project.config_dir / "local.toml"
    if local_path.exists():
        raw, load_diagnostics = load_toml(local_path, "Local active context")
        diagnostics.extend(load_diagnostics)
        if raw is not None:
            diagnostics.extend(scan_for_forbidden_fields(raw, "Local active context", local_path))
            local_context, parse_diagnostics = parse_local_active_context(local_path, raw)
            diagnostics.extend(parse_diagnostics)

    return ProjectState(
        project=project,
        topic_configs=topic_configs,
        local_context=local_context,
        diagnostics=diagnostics,
    )


def scan_for_forbidden_fields(data: object, concept: str, path: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    _scan_for_forbidden_fields(data, concept, path, (), diagnostics)
    return diagnostics


def _duplicate_id_diagnostics(project: Project) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    topic_counts = Counter(topic.id for topic in project.manifest.research_topics)
    workspace_counts = Counter(workspace.id for workspace in project.manifest.topic_workspaces)
    for topic_id in sorted(id_ for id_, count in topic_counts.items() if count > 1):
        diagnostics.append(
            Diagnostic(
                code="ISO004",
                severity="error",
                concept="Project Manifest",
                path=project.manifest_path,
                field="research_topics.id",
                message=f"Duplicate Research Topic id is registered: {topic_id}.",
            )
        )
    for workspace_id in sorted(id_ for id_, count in workspace_counts.items() if count > 1):
        diagnostics.append(
            Diagnostic(
                code="ISO004",
                severity="error",
                concept="Project Manifest",
                path=project.manifest_path,
                field="topic_workspaces.id",
                message=f"Duplicate Topic Workspace id is registered: {workspace_id}.",
            )
        )
    return diagnostics


def _validate_workspace_registrations(project: Project) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    topic_ids = {topic.id for topic in project.manifest.research_topics}
    for workspace in project.manifest.topic_workspaces:
        if workspace.path_input is not None:
            workspace_path = resolve_project_path(project.root, workspace.path_input)
            if not is_within(workspace_path, project.root):
                diagnostics.append(
                    Diagnostic(
                        code="ISO005",
                        severity="error",
                        concept="Topic Workspace",
                        path=project.manifest_path,
                        field=f"topic_workspaces.{workspace.id}.path",
                        message="Topic Workspace path resolves outside the Project root.",
                    )
                )
        if workspace.research_topic_id is not None and workspace.research_topic_id not in topic_ids:
            diagnostics.append(
                Diagnostic(
                    code="ISO008",
                    severity="error",
                    concept="Topic Workspace",
                    path=project.manifest_path,
                    field=f"topic_workspaces.{workspace.id}.research_topic_id",
                    message="Topic Workspace references an unregistered Research Topic.",
                )
            )

    workspace_ids = {workspace.id for workspace in project.manifest.topic_workspaces}
    for topic in project.manifest.research_topics:
        if topic.topic_workspace_id is not None and topic.topic_workspace_id not in workspace_ids:
            diagnostics.append(
                Diagnostic(
                    code="ISO008",
                    severity="error",
                    concept="Research Topic registration",
                    path=project.manifest_path,
                    field=f"research_topics.{topic.id}.topic_workspace_id",
                    message="Research Topic registration references a missing Topic Workspace.",
                )
            )
        if topic.topic_workspace_id is not None:
            referenced_workspace = project.manifest.first_workspace(topic.topic_workspace_id)
            if (
                referenced_workspace is not None
                and referenced_workspace.research_topic_id is not None
                and referenced_workspace.research_topic_id != topic.id
            ):
                diagnostics.append(
                    Diagnostic(
                        code="ISO012",
                        severity="error",
                        concept="Project Manifest",
                        path=project.manifest_path,
                        field=f"research_topics.{topic.id}.topic_workspace_id",
                        message="Research Topic registration references a Topic Workspace assigned to a different Research Topic.",
                    )
                )
    return diagnostics


def _scan_for_forbidden_fields(
    value: object,
    concept: str,
    path: Path,
    key_path: tuple[str, ...],
    diagnostics: list[Diagnostic],
) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            field_path = (*key_path, str(key))
            normalized_key = _normalize_key(str(key))
            field = ".".join(field_path)
            if _is_secret_key(normalized_key):
                diagnostics.append(
                    Diagnostic(
                        code="ISO010",
                        severity="error",
                        concept=concept,
                        path=path,
                        field=field,
                        message="Inline secret-like material is not allowed here; use a credential backend or a ref.",
                    )
                )
            if normalized_key in RUNTIME_TRUTH_KEYS:
                diagnostics.append(
                    Diagnostic(
                        code="ISO009",
                        severity="error",
                        concept=concept,
                        path=path,
                        field=field,
                        message="Runtime truth belongs in future Workspace Runtime records or file-backed Artifacts, not configuration.",
                    )
                )
            _scan_for_forbidden_fields(item, concept, path, field_path, diagnostics)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _scan_for_forbidden_fields(item, concept, path, (*key_path, f"[{index}]"), diagnostics)


def _is_secret_key(normalized_key: str) -> bool:
    return any(term in normalized_key for term in SECRET_TERMS)


def _normalize_key(key: str) -> str:
    return key.lower().replace("-", "_").replace(" ", "_")
