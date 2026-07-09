"""Read-only, progressive self queries for Isomer worker processes."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

from isomer_labs.project.context import IDENTITY_ENV_FIELDS
from isomer_labs.core.diagnostics import Diagnostic, has_errors
from isomer_labs.project.topic_service_master import topic_service_master_identity_for_context
from isomer_labs.project.doctor import find_project_pixi_manifest
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.core.path_utils import display_path
from isomer_labs.workspace.path_resolution import (
    PATH_ENV_VARS,
    resolve_effective_agent_context,
    resolve_effective_topic_actor_context,
    resolve_semantic_path,
)
from isomer_labs.workspace.pixi import resolve_topic_standalone_pixi_binding
from isomer_labs.workspace.manifest import EffectiveAgentContext, EffectiveTopicActorContext


SELF_QUERY_COMMANDS = (
    {
        "name": "show",
        "command": "isomer-cli --print-json project self show",
        "purpose": "Small self summary and available self query slices.",
    },
    {
        "name": "identity",
        "command": "isomer-cli --print-json project self identity",
        "purpose": "Resolved topic, Topic Actor, Agent, and source metadata.",
    },
    {
        "name": "pixi",
        "command": "isomer-cli --print-json project self pixi",
        "purpose": "Selected Pixi manifest, environment, and Python command hint.",
    },
    {
        "name": "env",
        "command": "isomer-cli --print-json project self env",
        "purpose": "Recognized Isomer environment inputs without values by default.",
    },
    {
        "name": "paths",
        "command": "isomer-cli --print-json project self paths <semantic-label>",
        "purpose": "Resolve only requested semantic labels.",
    },
    {
        "name": "queries",
        "command": "isomer-cli --print-json project self queries",
        "purpose": "Safe follow-up query commands.",
    },
)
SAFE_CONFIG_ENV_VARS = ("ISOMER_HOUMAO_COMMAND", "ISOMER_HOUMAO_CHECKOUT")
SELF_IDENTITY_ENV_VARS = (
    ("ISOMER_AGENT_NAME", "Effective Agent Context"),
    ("ISOMER_TOPIC_ACTOR_NAME", "Effective Topic Actor Context"),
)
SECRET_ENV_FRAGMENTS = ("TOKEN", "SECRET", "PASSWORD", "PASSWD", "API_KEY", "CREDENTIAL", "PRIVATE_KEY")


def build_self_show_payload(
    context: EffectiveTopicContext | None,
    *,
    diagnostics: list[Diagnostic],
    topic_actor_context: EffectiveTopicActorContext | None,
    agent_context: EffectiveAgentContext | None,
) -> dict[str, object]:
    """Build the intentionally small self summary payload."""

    summary: dict[str, object] = {
        "project": _project_headline(context),
        "topic": _topic_headline(context),
        "topic_actor": _topic_actor_headline(topic_actor_context),
        "agent": _agent_headline(agent_context),
        "diagnostic_counts": _diagnostic_counts(diagnostics),
    }
    if context is not None:
        topic_service_master, tsm_diagnostics = topic_service_master_identity_for_context(context)
        diagnostics.extend(tsm_diagnostics)
        summary["topic_service_master"] = _topic_service_master_headline(topic_service_master)
    return {
        "ok": not has_errors(diagnostics),
        "mutated": False,
        "summary": summary,
        "available_queries": list(SELF_QUERY_COMMANDS),
    }


def build_self_identity_payload(
    context: EffectiveTopicContext | None,
    *,
    diagnostics: list[Diagnostic],
    topic_actor_context: EffectiveTopicActorContext | None,
    agent_context: EffectiveAgentContext | None,
) -> dict[str, object]:
    """Build identity-only self payload."""

    identity: dict[str, object] = {
        "context": _context_identity(context),
        "topic_actor": topic_actor_context.to_json() if topic_actor_context is not None else {"resolved": False},
        "agent": agent_context.to_json() if agent_context is not None else {"resolved": False},
    }
    if context is not None:
        identity["sources"] = dict(context.sources)
        identity["lifecycle_refs"] = dict(context.lifecycle_refs)
        topic_service_master, tsm_diagnostics = topic_service_master_identity_for_context(context)
        diagnostics.extend(tsm_diagnostics)
        identity["topic_service_master"] = topic_service_master
    return {
        "ok": not has_errors(diagnostics),
        "mutated": False,
        "identity": identity,
    }


def build_self_env_payload(
    context: EffectiveTopicContext | None,
    *,
    diagnostics: list[Diagnostic],
    env: Mapping[str, str],
    include_values: bool = False,
) -> dict[str, object]:
    """Build a safe allowlisted environment input report."""

    recognized: list[dict[str, object]] = []
    for name, field in sorted(IDENTITY_ENV_FIELDS.items()):
        recognized.append(
            _env_entry(name, env, category="identity", influences=field, context=context, include_value=include_values)
        )
    for name, influences in SELF_IDENTITY_ENV_VARS:
        recognized.append(
            _env_entry(
                name,
                env,
                category="identity",
                influences=influences,
                context=context,
                include_value=include_values,
            )
        )
    for name in sorted(set(PATH_ENV_VARS.values())):
        recognized.append(
            _env_entry(
                name,
                env,
                category="path",
                influences="Workspace Path Resolution",
                context=context,
                include_value=include_values,
            )
        )
    for name in SAFE_CONFIG_ENV_VARS:
        recognized.append(
            _env_entry(
                name,
                env,
                category="config",
                influences="adapter discovery",
                context=context,
                include_value=include_values,
            )
        )
    for name in sorted(key for key in env if key.startswith("ISOMER_PATH__")):
        recognized.append(
            _env_entry(
                name,
                env,
                category="semantic-path",
                influences="Workspace Path Resolution",
                context=context,
                include_value=include_values,
            )
        )
    return {
        "ok": not has_errors(diagnostics),
        "mutated": False,
        "environment": {
            "values_included": include_values,
            "recognized": recognized,
            "omitted_secret_like": sorted(key for key in env if key.startswith("ISOMER_") and _is_secret_like(key)),
        },
    }


def build_self_paths_payload(
    context: EffectiveTopicContext | None,
    *,
    diagnostics: list[Diagnostic],
    env: Mapping[str, str],
    cwd: Path,
    semantic_labels: tuple[str, ...],
    agent_name: str | None,
    agent_instance_id: str | None,
    topic_actor_name: str | None,
) -> dict[str, object]:
    """Build a requested-label-only semantic path payload."""

    paths: list[dict[str, object]] = []
    if context is not None:
        for label in semantic_labels:
            result, path_diagnostics = resolve_semantic_path(
                context,
                label,
                env=env,
                cwd=cwd,
                agent_name=agent_name,
                agent_instance_id=agent_instance_id,
                topic_actor_name=topic_actor_name,
            )
            diagnostics.extend(path_diagnostics)
            paths.append(
                {
                    "semantic_label": label,
                    "resolved": result is not None,
                    "path": result.to_json() if result is not None else None,
                    "diagnostics": [diagnostic.to_json() for diagnostic in path_diagnostics],
                }
            )
    return {
        "ok": not has_errors(diagnostics),
        "mutated": False,
        "semantic_paths": paths,
    }


def build_self_pixi_payload(
    context: EffectiveTopicContext | None,
    *,
    diagnostics: list[Diagnostic],
) -> dict[str, object]:
    """Build Pixi-only self payload."""

    pixi: dict[str, object] = {
        "selected": None,
        "candidates": [],
        "python_command": None,
    }
    if context is None:
        return {"ok": False, "mutated": False, "pixi": pixi}

    project = context.project
    topic_id = context.research_topic.id
    project_bindings = project.manifest.active_topic_pixi_environment_bindings(topic_id)
    standalone_bindings = project.manifest.active_topic_standalone_pixi_bindings(topic_id)
    pixi["project_pixi_environment_bindings"] = [binding.to_json() for binding in project_bindings]
    pixi["standalone_pixi_bindings"] = [binding.to_json() for binding in standalone_bindings]

    if len(project_bindings) > 1:
        pixi["candidates"] = [binding.to_json() for binding in project_bindings]
        diagnostics.append(
            Diagnostic(
                code="ISO088",
                severity="error",
                concept="Agent Self Pixi Query",
                field="topic_pixi_environment_bindings",
                message="Multiple active Project Pixi environment bindings are available; self pixi will not guess one.",
            )
        )
        return {"ok": False, "mutated": False, "pixi": pixi}

    if len(project_bindings) == 1 and not standalone_bindings:
        binding = project_bindings[0]
        project_pixi_info, pixi_diagnostics = find_project_pixi_manifest(project.root)
        diagnostics.extend(pixi_diagnostics)
        if project_pixi_info is None:
            diagnostics.append(
                Diagnostic(
                    code="ISO032",
                    severity="error",
                    concept="Agent Self Pixi Query",
                    field="manifest_path",
                    message="The selected topic uses a Project Pixi environment, but no Project Pixi manifest was found.",
                    usage="isomer-cli --print-json doctor",
                )
            )
        elif binding.pixi_environment not in project_pixi_info.environments:
            diagnostics.append(
                Diagnostic(
                    code="ISO032",
                    severity="error",
                    concept="Agent Self Pixi Query",
                    field="pixi_environment",
                    message=f"Project Pixi manifest does not declare selected environment {binding.pixi_environment!r}.",
                    usage="isomer-cli --print-json doctor",
                )
            )
        else:
            selected = {
                "kind": "project",
                "source": "Project Manifest topic_pixi_environment_bindings",
                "manifest_path": str(project_pixi_info.manifest_path),
                "manifest_path_display": display_path(project_pixi_info.manifest_path, project.root),
                "pixi_environment": binding.pixi_environment,
            }
            pixi["selected"] = selected
            pixi["python_command"] = _pixi_python_command(project_pixi_info.manifest_path, binding.pixi_environment)
        return {"ok": not has_errors(diagnostics), "mutated": False, "pixi": pixi}

    resolved, failure = resolve_topic_standalone_pixi_binding(context)
    if resolved is not None:
        selected = {
            "kind": "standalone",
            "source": resolved.source,
            "manifest_path": str(resolved.resolved_manifest_path),
            "manifest_path_display": display_path(resolved.resolved_manifest_path, project.root),
            "pixi_environment": resolved.pixi_environment,
            "environment_prefix": str(resolved.environment_prefix),
        }
        pixi["selected"] = selected
        pixi["python_command"] = _pixi_python_command(resolved.resolved_manifest_path, resolved.pixi_environment)
    elif failure is not None:
        pixi["failure"] = failure.to_json(project.root)
        diagnostics.append(
            Diagnostic(
                code="ISO032",
                severity="error",
                concept="Agent Self Pixi Query",
                field="pixi",
                message=f"Pixi binding could not be resolved: {failure.message}",
                usage="isomer-cli --print-json doctor",
            )
        )
    return {"ok": not has_errors(diagnostics), "mutated": False, "pixi": pixi}


def build_self_queries_payload(
    context: EffectiveTopicContext | None,
    *,
    diagnostics: list[Diagnostic],
) -> dict[str, object]:
    """Build the explicit follow-up query catalog."""

    topic_selector = ""
    if context is not None:
        topic_selector = f" --topic {context.research_topic.id}"
    queries = [
        *SELF_QUERY_COMMANDS,
        {
            "command": f"isomer-cli --print-json project context show{topic_selector}",
            "purpose": "Raw Effective Topic Context.",
        },
        {
            "command": f"isomer-cli --print-json project paths get <semantic-label>{topic_selector}",
            "purpose": "Resolve one semantic path.",
        },
        {
            "command": f"isomer-cli --print-json project paths explain <semantic-label>{topic_selector}",
            "purpose": "Explain candidate sources for one semantic path.",
        },
        {
            "command": f"isomer-cli --print-json project topic-actors show <topic-actor>{topic_selector}",
            "purpose": "Inspect one Topic Actor binding.",
        },
        {
            "command": f"isomer-cli --print-json project runtime inspect{topic_selector}",
            "purpose": "Inspect Workspace Runtime.",
        },
    ]
    return {
        "ok": not has_errors(diagnostics),
        "mutated": False,
        "queries": queries,
    }


def resolve_self_identity_contexts(
    context: EffectiveTopicContext | None,
    *,
    env: Mapping[str, str],
    cwd: Path,
    explicit_agent_name: str | None,
    explicit_agent_instance_id: str | None,
    explicit_topic_actor_name: str | None,
) -> tuple[EffectiveTopicActorContext | None, EffectiveAgentContext | None, list[Diagnostic]]:
    """Resolve optional Topic Actor and Agent contexts for self queries."""

    diagnostics: list[Diagnostic] = []
    if context is None:
        return None, None, diagnostics
    topic_actor_context, actor_diagnostics = resolve_effective_topic_actor_context(
        context,
        env=env,
        cwd=cwd,
        explicit_topic_actor_name=explicit_topic_actor_name,
        missing_is_error=False,
    )
    diagnostics.extend(actor_diagnostics)
    agent_context, agent_diagnostics = resolve_effective_agent_context(
        context,
        env=env,
        cwd=cwd,
        explicit_agent_name=explicit_agent_name,
        explicit_agent_instance_id=explicit_agent_instance_id,
        missing_is_error=False,
    )
    diagnostics.extend(agent_diagnostics)
    return topic_actor_context, agent_context, diagnostics


def _context_identity(context: EffectiveTopicContext | None) -> dict[str, object] | None:
    if context is None:
        return None
    return {
        "project_root": str(context.project.root),
        "project_manifest": str(context.project.manifest_path),
        "research_topic_id": context.research_topic.id,
        "research_topic_config_path": (
            str(context.research_topic_config.source_path) if context.research_topic_config is not None else None
        ),
        "topic_workspace_id": context.topic_workspace_id,
        "topic_workspace_path": str(context.topic_workspace_path),
        "topic_agent_team_profile_id": context.topic_agent_team_profile_id,
        "domain_agent_team_template_id": context.domain_agent_team_template_id,
    }


def _project_headline(context: EffectiveTopicContext | None) -> dict[str, object] | None:
    if context is None:
        return None
    return {
        "root": str(context.project.root),
        "source": context.project.discovery_source,
    }


def _topic_headline(context: EffectiveTopicContext | None) -> dict[str, object] | None:
    if context is None:
        return None
    return {
        "research_topic_id": context.research_topic.id,
        "topic_workspace_id": context.topic_workspace_id,
        "source": context.sources.get("research_topic_id"),
    }


def _topic_actor_headline(topic_actor_context: EffectiveTopicActorContext | None) -> dict[str, object]:
    if topic_actor_context is None:
        return {"resolved": False}
    return {
        "resolved": True,
        "topic_actor_name": topic_actor_context.topic_actor_name,
        "source": topic_actor_context.source,
    }


def _agent_headline(agent_context: EffectiveAgentContext | None) -> dict[str, object]:
    if agent_context is None:
        return {"resolved": False}
    data: dict[str, object] = {
        "resolved": True,
        "agent_name": agent_context.agent_name,
        "source": agent_context.source,
    }
    if agent_context.agent_instance_id is not None:
        data["agent_instance_id"] = agent_context.agent_instance_id
    return data


def _topic_service_master_headline(topic_service_master: dict[str, object]) -> dict[str, object]:
    data: dict[str, object] = {
        "binding_status": topic_service_master.get("binding_status"),
    }
    suggested = topic_service_master.get("suggested_names")
    if isinstance(suggested, dict):
        data["specialist_name"] = suggested.get("specialist_name")
        data["launch_profile_name"] = suggested.get("launch_profile_name")
        data["managed_agent_name"] = suggested.get("managed_agent_name")
    if topic_service_master.get("drift"):
        data["drift"] = topic_service_master.get("drift")
    return data


def _diagnostic_counts(diagnostics: list[Diagnostic]) -> dict[str, int]:
    errors = sum(1 for diagnostic in diagnostics if diagnostic.severity == "error")
    warnings = sum(1 for diagnostic in diagnostics if diagnostic.severity == "warning")
    return {"errors": errors, "warnings": warnings, "total": len(diagnostics)}


def _env_entry(
    name: str,
    env: Mapping[str, str],
    *,
    category: str,
    influences: str,
    context: EffectiveTopicContext | None,
    include_value: bool,
) -> dict[str, object]:
    present = name in env and bool(env.get(name))
    entry: dict[str, object] = {
        "name": name,
        "category": category,
        "present": present,
        "influences": influences,
        "influenced_resolution": _influenced_resolution(name, env.get(name), context),
    }
    if present and include_value and not _is_secret_like(name):
        entry["value"] = env[name]
    elif present and _is_secret_like(name):
        entry["value_omitted"] = "secret-like"
    elif present:
        entry["value_omitted"] = "default"
    return entry


def _influenced_resolution(name: str, value: str | None, context: EffectiveTopicContext | None) -> bool:
    if not value or context is None:
        return False
    field = IDENTITY_ENV_FIELDS.get(name)
    if field is None:
        return False
    if field == "research_topic_id":
        return context.research_topic.id == value
    if field == "topic_workspace_id":
        return context.topic_workspace_id == value
    if field == "topic_agent_team_profile_id":
        return context.topic_agent_team_profile_id == value
    return context.lifecycle_refs.get(field) == value


def _is_secret_like(name: str) -> bool:
    upper = name.upper()
    return any(fragment in upper for fragment in SECRET_ENV_FRAGMENTS)


def _pixi_python_command(manifest_path: Path, pixi_environment: str) -> str:
    return f"pixi run --manifest-path {manifest_path} --environment {pixi_environment} python ..."
