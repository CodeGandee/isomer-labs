"""Research Topic Config and local active context parsing."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from isomer_labs.diagnostics import Diagnostic
from isomer_labs.models import (
    LOCAL_ACTIVE_CONTEXT_SCHEMA_VERSION,
    RESEARCH_TOPIC_CONFIG_SCHEMA_VERSION,
    LocalActiveContext,
    ResearchTopicConfig,
)


LOCAL_CONTEXT_ALLOWED_FIELDS = {
    "schema_version",
    "research_topic_id",
    "topic_workspace_id",
    "research_inquiry_id",
    "research_task_id",
    "run_id",
    "agent_team_instance_id",
    "agent_instance_id",
    "topic_agent_team_profile_id",
}


def parse_research_topic_config(
    path: Path,
    raw: dict[str, Any],
) -> tuple[ResearchTopicConfig | None, list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    research_topic_id = raw.get("research_topic_id")
    if not isinstance(research_topic_id, str) or not research_topic_id:
        diagnostics.append(
            Diagnostic(
                code="ISO003",
                severity="error",
                concept="Research Topic Config",
                path=path,
                field="research_topic_id",
                message="Research Topic Config must include research_topic_id.",
            )
        )
        return None, diagnostics

    measurable_objectives = _string_list(raw.get("measurable_objectives"))
    config = ResearchTopicConfig(
        schema_version=_string(raw.get("schema_version")) or RESEARCH_TOPIC_CONFIG_SCHEMA_VERSION,
        research_topic_id=research_topic_id,
        source_path=path,
        topic_statement=_string(raw.get("topic_statement")),
        measurable_objectives=measurable_objectives,
        defaults=_dict_value(raw.get("defaults")),
        refs=_collect_refs(raw),
        raw=raw,
    )
    return config, diagnostics


def parse_local_active_context(path: Path, raw: dict[str, Any]) -> tuple[LocalActiveContext, list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    refs: dict[str, str] = {}
    for key, value in raw.items():
        if key not in LOCAL_CONTEXT_ALLOWED_FIELDS:
            diagnostics.append(
                Diagnostic(
                    code="ISO011",
                    severity="error",
                    concept="Local active context",
                    path=path,
                    field=key,
                    message="Local active context may contain only candidate identity refs and schema_version.",
                )
            )
            continue
        if key == "schema_version":
            continue
        if isinstance(value, str) and value:
            refs[key] = value
        elif value is not None:
            diagnostics.append(
                Diagnostic(
                    code="ISO011",
                    severity="error",
                    concept="Local active context",
                    path=path,
                    field=key,
                    message="Local active context identity refs must be strings.",
                )
            )
    return (
        LocalActiveContext(
            schema_version=_string(raw.get("schema_version")) or LOCAL_ACTIVE_CONTEXT_SCHEMA_VERSION,
            source_path=path,
            refs=refs,
            raw=raw,
        ),
        diagnostics,
    )


def _collect_refs(raw: dict[str, Any]) -> dict[str, Any]:
    keys = (
        "default_research_inquiry_id",
        "default_domain_agent_team_template_id",
        "default_topic_agent_team_profile_id",
        "domain_agent_team_template_id",
        "domain_agent_team_template_ref",
        "topic_agent_team_profile_id",
        "topic_agent_team_profile_ref",
        "default_execution_adapter_id",
        "default_control_mode",
        "coordination_policy_ref",
        "coordination_policy_refs",
        "capability_binding_refs",
        "skill_binding_projection_refs",
        "research_operation_extension_point_refs",
        "gate_policy_refs",
        "scheduler_policy_refs",
        "baseline_waiver_policy_refs",
        "literature_provider_refs",
        "artifact_format_profile_defaults",
        "artifact_extension_refs",
        "topic_statement_artifact_refs",
        "default_refs",
        "extension_refs",
        "policy_refs",
        "artifact_format_defaults",
    )
    refs = {key: raw[key] for key in keys if key in raw}
    nested_refs = raw.get("refs")
    if isinstance(nested_refs, dict):
        refs.update(nested_refs)
    return refs


def _string(value: object) -> str | None:
    if isinstance(value, str) and value:
        return value
    return None


def _string_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str)]
    return []


def _dict_value(value: object) -> dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)
    return {}
