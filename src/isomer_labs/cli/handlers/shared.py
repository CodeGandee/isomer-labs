"""Shared helpers and imports for CLI command handlers."""

# ruff: noqa: F401
from __future__ import annotations

from dataclasses import dataclass, replace
import json
import os
from pathlib import Path
from typing import Any, Sequence

import tomlkit

from isomer_labs.core.builtins import list_built_in_schemas
from isomer_labs.cli.options import CliOptions, value as _value
from isomer_labs.cli.output import emit_output, output_format
from isomer_labs.workspace.surfaces import topic_workspace_path as default_topic_workspace_path
from isomer_labs.project.context import resolve_effective_topic_context
from isomer_labs.core.diagnostics import Diagnostic, has_errors
from isomer_labs.project.doctor import build_doctor_report, render_doctor_text
from isomer_labs.houmao.manifests import (
    HOUMAO_ADAPTER_ID,
    AgentBinding,
    ManifestKind,
    ManifestValidationError,
    adapter_manifest_path_plan_surface,
    build_adapter_link_manifest,
    build_adapter_runtime_manifest,
    canonical_json_digest,
    collect_houmao_read_only_state,
    load_json_manifest,
    manifest_paths,
    reconcile_houmao_manifests,
    write_json_manifest,
)
from isomer_labs.houmao.adapter import HoumaoAdapterFacade
from isomer_labs.project.init import initialize_project
from isomer_labs.models import EffectiveTopicContext, Project, ProjectState, SelectionRequest, TopicAgentTeamProfile
from isomer_labs.core.path_utils import display_path
from isomer_labs.workspace.path_resolution import (
    default_semantic_path,
    explain_semantic_path,
    list_semantic_paths,
    materialize_default_paths,
    materialize_semantic_path,
    preview_paths,
    resolve_effective_agent_context,
    resolve_effective_topic_actor_context,
    resolve_semantic_path,
)
from isomer_labs.workspace.manifest import (
    WORKER_OUTPUT_TRACKING_AUTHORITY,
    register_manifest_binding,
    reset_manifest_binding,
    resolve_worker_output_policy,
    unregister_manifest_binding,
    update_manifest_binding,
)
from isomer_labs.workspace.actors import (
    archive_topic_actor,
    diagnose_topic_actor,
    list_topic_actors,
    materialize_topic_actor_workspace,
    register_topic_actor,
    show_topic_actor,
    update_topic_actor,
)
from isomer_labs.workspace.guidance import (
    ensure_topic_main_guidance,
    guidance_metadata,
    inspect_topic_main_guidance,
    render_topic_main_guidance_block,
)
from isomer_labs.teams.profile_bundles import materialize_topic_agent_team_profile_bundle
from isomer_labs.project import (
    discover_project,
    find_ancestor_manifest,
    houmao_project_dir_for_root,
    project_root_for_manifest,
)
from isomer_labs.project.cleanup import execute_project_cleanup, plan_project_cleanup, render_cleanup_text
from isomer_labs.project.content_root import (
    execute_project_content_root_move,
    plan_project_content_root_move,
    render_content_root_move_text,
)
from isomer_labs.core.rendering import render_key_values
from isomer_labs.project.topics import (
    create_research_topic,
    delete_research_topic,
    plan_delete_research_topic,
    render_topic_create_text,
    render_topic_delete_text,
    render_topic_show_text,
    render_topic_update_text,
    show_research_topic,
    update_research_topic,
)
from isomer_labs.runtime.store import (
    initialize_workspace_runtime,
    open_workspace_runtime,
    prepare_topic_environment_readiness,
)
from isomer_labs.runtime.records import AdapterManifestRefRecord, AdapterReconciliationRecord, utc_timestamp
from isomer_labs.runtime.validation import inspect_workspace_runtime, validate_workspace_runtime
from isomer_labs.workspace.self_query import (
    build_self_env_payload,
    build_self_identity_payload,
    build_self_paths_payload,
    build_self_pixi_payload,
    build_self_queries_payload,
    build_self_show_payload,
    resolve_self_identity_contexts,
)
from isomer_labs.teams.profiles import (
    parse_topic_agent_team_profile,
    profile_to_toml,
    specialize_topic_agent_team_profile,
    validate_topic_agent_team_profile,
)
from isomer_labs.teams.repositories import discover_team_repositories
from isomer_labs.teams.templates import (
    discover_domain_agent_team_templates,
    find_domain_agent_team_template,
    resolve_template_source_path,
    validate_domain_agent_team_template,
)
from isomer_labs.teams.instantiation import parse_topic_team_instantiation_packet
from isomer_labs.core.toml_loader import load_toml
from isomer_labs.project.validation import build_project_state

_IMPLICIT_TOPIC_SELECTION_SOURCES = {
    "Project Manifest default",
    "single Project Manifest registration",
}


def _context_for_options(options: CliOptions) -> tuple[EffectiveTopicContext | None, list[Diagnostic]]:
    project, diagnostics = _discover(options)
    if project is None:
        return None, diagnostics
    state = build_project_state(project)
    diagnostics.extend(state.diagnostics)
    request = SelectionRequest(
        research_topic_id=_value(options, "research_topic_id"),
        topic_workspace_id=_value(options, "topic_workspace_id"),
        research_inquiry_id=_value(options, "research_inquiry_id"),
        research_task_id=_value(options, "research_task_id"),
        run_id=_value(options, "run_id"),
        agent_team_instance_id=_value(options, "agent_team_instance_id"),
        agent_instance_id=_value(options, "agent_instance_id"),
        topic_agent_team_profile_id=_value(options, "topic_agent_team_profile_id"),
    )
    context, context_diagnostics = resolve_effective_topic_context(
        state,
        request,
        cwd=Path.cwd(),
        env=os.environ,
    )
    diagnostics.extend(context_diagnostics)
    return context, diagnostics


def _self_identity_inputs(options: CliOptions) -> tuple[Any, Any, Any, list[Diagnostic]]:
    context, diagnostics = _context_for_options(options)
    topic_actor_context = None
    agent_context = None
    if context is not None:
        topic_actor_context, agent_context, identity_diagnostics = resolve_self_identity_contexts(
            context,
            env=os.environ,
            cwd=Path.cwd(),
            explicit_agent_name=_value(options, "agent_name"),
            explicit_agent_instance_id=_value(options, "agent_instance_id"),
            explicit_topic_actor_name=_value(options, "topic_actor_name"),
        )
        diagnostics.extend(identity_diagnostics)
    return context, topic_actor_context, agent_context, diagnostics


def _resolved_name(data: dict[str, object], key: str) -> object:
    if data.get("resolved") is True:
        return data.get(key, "resolved")
    return "unresolved"


def _context_for_path_options(
    options: CliOptions,
    semantic_label: str | None = None,
) -> tuple[EffectiveTopicContext | None, list[Diagnostic]]:
    context, diagnostics = _context_for_options(options)
    if context is None:
        return None, diagnostics
    if not _path_label_requires_selected_topic(semantic_label):
        return context, diagnostics
    source = context.sources.get("research_topic_id")
    if source not in _IMPLICIT_TOPIC_SELECTION_SOURCES:
        return context, diagnostics
    diagnostics.append(
        Diagnostic(
            code="ISO013",
            severity="error",
            concept="Workspace Path Resolution",
            field=semantic_label or "semantic_label",
            message=(
                "Semantic storage labels that require a Topic context need an explicit "
                "`--topic` or `--topic-workspace` selector unless the command is run inside "
                "the selected Topic Workspace."
            ),
        )
    )
    return None, diagnostics


def _path_label_requires_selected_topic(semantic_label: str | None) -> bool:
    if semantic_label is None:
        return True
    return semantic_label.startswith(("topic.", "agent.", "custom."))


def _selection_request_from_options(options: CliOptions) -> SelectionRequest:
    return SelectionRequest(
        research_topic_id=_value(options, "research_topic_id"),
        topic_workspace_id=_value(options, "topic_workspace_id"),
        research_inquiry_id=_value(options, "research_inquiry_id"),
        research_task_id=_value(options, "research_task_id"),
        run_id=_value(options, "run_id"),
        agent_team_instance_id=_value(options, "agent_team_instance_id"),
        agent_instance_id=_value(options, "agent_instance_id"),
        topic_agent_team_profile_id=_value(options, "topic_agent_team_profile_id"),
    )


def _discover(options: CliOptions) -> tuple[Project | None, list[Diagnostic]]:
    return discover_project(
        cwd=Path.cwd(),
        env=os.environ,
        project_selector=_value(options, "project"),
        manifest_selector=_value(options, "manifest"),
    )


def _discover_optional(options: CliOptions) -> tuple[Project | None, list[Diagnostic]]:
    project, diagnostics = _discover(options)
    if project is not None:
        return project, diagnostics
    if _value(options, "project") is None and _value(options, "manifest") is None:
        return None, []
    return project, diagnostics


def _project_selector_requested(options: CliOptions) -> bool:
    return _value(options, "project") is not None or _value(options, "manifest") is not None


def _topic_selector_requested(options: CliOptions) -> bool:
    return any(
        _value(options, name) is not None
        for name in (
            "research_topic_id",
            "topic_workspace_id",
            "research_inquiry_id",
            "research_task_id",
            "run_id",
            "agent_team_instance_id",
            "agent_instance_id",
            "topic_agent_team_profile_id",
        )
    )


def _unknown_template_diagnostic(template_id: str) -> Diagnostic:
    return Diagnostic(
        code="ISO016",
        severity="error",
        concept="Domain Agent Team Template",
        field="template_id",
        message=f"Unknown Domain Agent Team Template: {template_id}.",
    )


def _missing_template_diagnostic() -> Diagnostic:
    return Diagnostic(
        code="ISO020",
        severity="error",
        concept="Domain Agent Team Template",
        field="template_id",
        message=(
            "No Domain Agent Team Template was selected. Pass --template, set a Project or Topic default, "
            "or configure a Team Repository template before running this command."
        ),
    )


def _resolve_profile_cli_path(
    project: Project | None,
    profile_path: str | None,
    diagnostics: list[Diagnostic],
) -> Path | None:
    if profile_path is not None:
        path = Path(profile_path)
        if path.is_absolute() or project is None:
            return path.expanduser().resolve(strict=False)
        return (project.root / path).expanduser().resolve(strict=False)
    if project is None:
        diagnostics.append(
            Diagnostic(
                code="ISO020",
                severity="error",
                concept="Topic Agent Team Profile",
                message="A Project or explicit profile path is required to validate a Topic Agent Team Profile.",
            )
        )
        return None
    profile_id = project.manifest.default_topic_agent_team_profile_id()
    if profile_id is None:
        diagnostics.append(
            Diagnostic(
                code="ISO020",
                severity="error",
                concept="Topic Agent Team Profile",
                path=project.manifest_path,
                field="defaults.topic_agent_team_profile_id",
                message="No Topic Agent Team Profile path was provided and the Project Manifest has no default profile.",
            )
        )
        return None
    registration = project.manifest.first_topic_agent_team_profile(profile_id)
    if registration is None:
        diagnostics.append(
            Diagnostic(
                code="ISO020",
                severity="error",
                concept="Topic Agent Team Profile",
                path=project.manifest_path,
                field="defaults.topic_agent_team_profile_id",
                message="Project Manifest default profile id is not registered.",
            )
        )
        return None
    return (project.root / registration.path_input).expanduser().resolve(strict=False)


def _resolve_cli_path(project_root: Path, path_input: str) -> Path:
    path = Path(path_input).expanduser()
    if path.is_absolute():
        return path.resolve(strict=False)
    return (project_root / path).resolve(strict=False)


def _profile_registration_suggestion(project_root: Path, profile: TopicAgentTeamProfile) -> dict[str, str]:
    return {
        "target": "Project Manifest",
        "section": "topic_agent_team_profiles",
        "id": profile.id,
        "path": _project_relative_path(project_root, profile.source_path),
        "domain_agent_team_template_id": profile.domain_agent_team_template_id,
        "research_topic_id": profile.research_topic_id,
        "status": "active",
    }


def _append_template_registration(manifest_path: Path, registration: dict[str, str]) -> None:
    document = tomlkit.parse(manifest_path.read_text(encoding="utf-8"))
    templates = document.get("domain_agent_team_templates")
    if templates is None:
        templates = tomlkit.aot()
        document["domain_agent_team_templates"] = templates
    item = tomlkit.table()
    for key, value in registration.items():
        item[key] = value
    templates.append(item)
    manifest_path.write_text(tomlkit.dumps(document), encoding="utf-8")


def _project_relative_path(project_root: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(project_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)


def _emit(
    command: str,
    options: CliOptions,
    payload: dict[str, Any],
    diagnostics: list[Diagnostic],
    text_lines: list[str],
) -> int:
    output_command = command
    if not command.startswith("project ") and command != "schemas list":
        output_command = f"project {command}"
    return emit_output(output_command, options, payload, diagnostics, text_lines)


def _render_validate_text(project_found: bool, diagnostics: list[Diagnostic]) -> list[str]:
    if project_found and not has_errors(diagnostics):
        return ["Project valid."]
    return []


def _output_format(options: CliOptions) -> str:
    return output_format(options)

__all__ = [name for name in globals() if not name.startswith("__")]
