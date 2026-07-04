"""Project Manifest parsing."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from isomer_labs.core.diagnostics import Diagnostic
from isomer_labs.models import (
    DOMAIN_AGENT_TEAM_TEMPLATE_REF_SCHEMA_VERSION,
    PROJECT_MANIFEST_SCHEMA_VERSION,
    TEAM_REPOSITORY_MANIFEST_SCHEMA_VERSION,
    TOPIC_AGENT_TEAM_PROFILE_SCHEMA_VERSION,
    DomainAgentTeamTemplateRegistration,
    ProjectManifest,
    ResearchTopicRegistration,
    TeamRepositoryRegistration,
    TopicAgentTeamProfileRegistration,
    TopicPixiEnvironmentBinding,
    TopicStandalonePixiBinding,
    TopicWorkspaceRegistration,
)


def parse_project_manifest(path: Path, raw: dict[str, Any]) -> tuple[ProjectManifest, list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    schema_version = _first_string(raw, ("manifest_schema_version", "schema_version"))
    if schema_version is None:
        schema_version = PROJECT_MANIFEST_SCHEMA_VERSION

    defaults = _dict_value(raw.get("defaults"))
    path_defaults = _dict_value(raw.get("paths"))
    path_defaults.update(_dict_value(raw.get("path_defaults")))

    topics = _parse_research_topics(path, raw, schema_version, diagnostics)
    workspaces = _parse_topic_workspaces(path, raw, schema_version, diagnostics)
    pixi_environment_bindings = _parse_topic_pixi_environment_bindings(path, raw, diagnostics)
    standalone_pixi_bindings = _parse_topic_standalone_pixi_bindings(path, raw, diagnostics)
    team_repositories = _parse_team_repositories(path, raw, diagnostics)
    templates = _parse_domain_agent_team_templates(path, raw, diagnostics)
    profiles = _parse_topic_agent_team_profiles(path, raw, diagnostics)
    artifact_format_profiles = _registration_ids(raw.get("artifact_format_profiles"))
    artifact_extensions = _registration_ids(raw.get("artifact_extensions"))
    user_skill_callback_registry_refs = _callback_registry_ref_values(raw)

    manifest = ProjectManifest(
        schema_version=schema_version,
        source_path=path,
        research_topics=topics,
        topic_workspaces=workspaces,
        topic_pixi_environment_bindings=pixi_environment_bindings,
        topic_standalone_pixi_bindings=standalone_pixi_bindings,
        team_repositories=team_repositories,
        domain_agent_team_templates=templates,
        topic_agent_team_profiles=profiles,
        defaults=defaults,
        path_defaults=path_defaults,
        artifact_format_profiles=artifact_format_profiles,
        artifact_extensions=artifact_extensions,
        user_skill_callback_registry_refs=user_skill_callback_registry_refs,
        raw=raw,
    )
    return manifest, diagnostics


def _parse_research_topics(
    path: Path,
    raw: dict[str, Any],
    manifest_schema_version: str,
    diagnostics: list[Diagnostic],
) -> list[ResearchTopicRegistration]:
    topics: list[ResearchTopicRegistration] = []
    for index, item in enumerate(_table_items(raw.get("research_topics"))):
        field = f"research_topics[{index}]"
        topic_id = _first_string(item, ("id", "research_topic_id"))
        config_path = _first_string(item, ("config_path", "research_topic_config_path", "config"))
        if topic_id is None:
            diagnostics.append(
                Diagnostic(
                    code="ISO003",
                    severity="error",
                    concept="Research Topic registration",
                    path=path,
                    field=f"{field}.id",
                    message="Research Topic registration must include an id.",
                )
            )
            continue
        if config_path is None:
            diagnostics.append(
                Diagnostic(
                    code="ISO003",
                    severity="error",
                    concept="Research Topic registration",
                    path=path,
                    field=f"{field}.config_path",
                    message="Research Topic registration must include a Research Topic Config path.",
                )
            )
            continue
        topics.append(
            ResearchTopicRegistration(
                id=topic_id,
                config_path_input=config_path,
                topic_workspace_id=_first_string(item, ("topic_workspace_id", "topic_workspace_ref")),
                schema_version=_first_string(item, ("schema_version",)) or manifest_schema_version,
                status=_first_string(item, ("status",)) or "active",
                source_path=path,
            )
        )
    return topics


def _parse_topic_workspaces(
    path: Path,
    raw: dict[str, Any],
    manifest_schema_version: str,
    diagnostics: list[Diagnostic],
) -> list[TopicWorkspaceRegistration]:
    workspaces: list[TopicWorkspaceRegistration] = []
    for index, item in enumerate(_table_items(raw.get("topic_workspaces"))):
        field = f"topic_workspaces[{index}]"
        workspace_id = _first_string(item, ("id", "topic_workspace_id"))
        if workspace_id is None:
            diagnostics.append(
                Diagnostic(
                    code="ISO003",
                    severity="error",
                    concept="Topic Workspace registration",
                    path=path,
                    field=f"{field}.id",
                    message="Topic Workspace registration must include an id.",
                )
            )
            continue
        workspaces.append(
            TopicWorkspaceRegistration(
                id=workspace_id,
                research_topic_id=_first_string(item, ("research_topic_id", "topic_id")),
                path_input=_first_string(item, ("path", "path_input", "topic_workspace_path", "root")),
                schema_version=_first_string(item, ("schema_version",)) or manifest_schema_version,
                status=_first_string(item, ("status",)) or "active",
                source_path=path,
            )
        )
    return workspaces


def _parse_topic_pixi_environment_bindings(
    path: Path,
    raw: dict[str, Any],
    diagnostics: list[Diagnostic],
) -> list[TopicPixiEnvironmentBinding]:
    bindings: list[TopicPixiEnvironmentBinding] = []
    for index, item in enumerate(_table_items(raw.get("topic_pixi_environment_bindings"))):
        field = f"topic_pixi_environment_bindings[{index}]"
        research_topic_id = _first_string(item, ("research_topic_id", "topic_id"))
        pixi_environment = _first_string(item, ("pixi_environment", "environment", "pixi_env"))
        status = _status_string(item, path, field, "Topic Pixi environment binding", diagnostics)
        missing: list[str] = []
        if research_topic_id is None:
            missing.append("research_topic_id")
        if pixi_environment is None:
            missing.append("pixi_environment")
        if missing:
            diagnostics.append(
                Diagnostic(
                    code="ISO003",
                    severity="error",
                    concept="Topic Pixi environment binding",
                    path=path,
                    field=field,
                    message=f"Topic Pixi environment binding must include {', '.join(missing)}.",
                )
            )
            continue
        if status is None:
            continue
        assert research_topic_id is not None
        assert pixi_environment is not None
        bindings.append(
            TopicPixiEnvironmentBinding(
                research_topic_id=research_topic_id,
                pixi_environment=pixi_environment,
                purpose=_first_string(item, ("purpose",)),
                status=status,
                source_path=path,
            )
        )
    return bindings


def _parse_topic_standalone_pixi_bindings(
    path: Path,
    raw: dict[str, Any],
    diagnostics: list[Diagnostic],
) -> list[TopicStandalonePixiBinding]:
    bindings: list[TopicStandalonePixiBinding] = []
    for index, item in enumerate(_table_items(raw.get("topic_standalone_pixi_bindings"))):
        field = f"topic_standalone_pixi_bindings[{index}]"
        research_topic_id = _first_string(item, ("research_topic_id", "topic_id"))
        superseded_target_fields = [
            name
            for name in ("manifest_path", "path", "pixi_manifest_path")
            if isinstance(item.get(name), str) and item.get(name)
        ]
        if superseded_target_fields:
            diagnostics.append(
                Diagnostic(
                    code="ISO003",
                    severity="error",
                    concept="Topic standalone Pixi binding",
                    path=path,
                    field=field,
                    message=(
                        "Topic standalone Pixi binding uses superseded target field(s) "
                        f"{', '.join(superseded_target_fields)}; use manifest_path_or_dir instead."
                    ),
                )
            )
            continue
        manifest_path_or_dir = _first_string(item, ("manifest_path_or_dir",))
        status = _status_string(item, path, field, "Topic standalone Pixi binding", diagnostics)
        missing: list[str] = []
        if research_topic_id is None:
            missing.append("research_topic_id")
        if manifest_path_or_dir is None:
            missing.append("manifest_path_or_dir")
        if missing:
            diagnostics.append(
                Diagnostic(
                    code="ISO003",
                    severity="error",
                    concept="Topic standalone Pixi binding",
                    path=path,
                    field=field,
                    message=f"Topic standalone Pixi binding must include {', '.join(missing)}.",
                )
            )
            continue
        if status is None:
            continue
        assert research_topic_id is not None
        assert manifest_path_or_dir is not None
        bindings.append(
            TopicStandalonePixiBinding(
                research_topic_id=research_topic_id,
                manifest_path_or_dir_input=manifest_path_or_dir,
                pixi_environment=_first_string(item, ("pixi_environment", "environment", "pixi_env")),
                purpose=_first_string(item, ("purpose",)),
                status=status,
                source_path=path,
            )
        )
    return bindings


def _parse_domain_agent_team_templates(
    path: Path,
    raw: dict[str, Any],
    diagnostics: list[Diagnostic],
) -> list[DomainAgentTeamTemplateRegistration]:
    registrations: list[DomainAgentTeamTemplateRegistration] = []
    for index, item in enumerate(_table_items(raw.get("domain_agent_team_templates"))):
        field = f"domain_agent_team_templates[{index}]"
        template_id = _first_string(item, ("id", "domain_agent_team_template_id", "template_id", "ref"))
        source_kind = _first_string(item, ("source_kind", "kind")) or "project"
        source_path = _first_string(item, ("source_path", "path", "template_path", "execplan_path", "source"))
        team_repository_id = _first_string(item, ("team_repository_id", "team_repo_id", "repository_id"))
        if template_id is None:
            diagnostics.append(
                Diagnostic(
                    code="ISO003",
                    severity="error",
                    concept="Domain Agent Team Template registration",
                    path=path,
                    field=f"{field}.id",
                    message="Domain Agent Team Template registration must include an id.",
                )
            )
            continue
        if source_path is None:
            diagnostics.append(
                Diagnostic(
                    code="ISO003",
                    severity="error",
                    concept="Domain Agent Team Template registration",
                    path=path,
                    field=f"{field}.source_path",
                    message="Domain Agent Team Template registration must include a source path.",
                )
            )
            continue
        registrations.append(
            DomainAgentTeamTemplateRegistration(
                id=template_id,
                source_path_input=source_path,
                source_kind=source_kind,
                schema_version=_first_string(item, ("schema_version",)) or DOMAIN_AGENT_TEAM_TEMPLATE_REF_SCHEMA_VERSION,
                status=_first_string(item, ("status",)) or "active",
                source_path=path,
                team_repository_id=team_repository_id,
            )
        )
    return registrations


def _parse_team_repositories(
    path: Path,
    raw: dict[str, Any],
    diagnostics: list[Diagnostic],
) -> list[TeamRepositoryRegistration]:
    registrations: list[TeamRepositoryRegistration] = []
    for index, item in enumerate(_table_items(raw.get("team_repositories"))):
        field = f"team_repositories[{index}]"
        repository_id = _first_string(item, ("id", "team_repository_id", "repository_id", "ref"))
        repository_path = _first_string(item, ("path", "root", "source_path", "repository_path"))
        if repository_id is None:
            diagnostics.append(
                Diagnostic(
                    code="ISO003",
                    severity="error",
                    concept="Team Repository registration",
                    path=path,
                    field=f"{field}.id",
                    message="Team Repository registration must include an id.",
                )
            )
            continue
        if repository_path is None:
            diagnostics.append(
                Diagnostic(
                    code="ISO003",
                    severity="error",
                    concept="Team Repository registration",
                    path=path,
                    field=f"{field}.path",
                    message="Team Repository registration must include a path.",
                )
            )
            continue
        registrations.append(
            TeamRepositoryRegistration(
                id=repository_id,
                path_input=repository_path,
                schema_version=_first_string(item, ("schema_version",)) or TEAM_REPOSITORY_MANIFEST_SCHEMA_VERSION,
                status=_first_string(item, ("status",)) or "active",
                source_path=path,
            )
        )
    return registrations


def _parse_topic_agent_team_profiles(
    path: Path,
    raw: dict[str, Any],
    diagnostics: list[Diagnostic],
) -> list[TopicAgentTeamProfileRegistration]:
    registrations: list[TopicAgentTeamProfileRegistration] = []
    for index, item in enumerate(_table_items(raw.get("topic_agent_team_profiles"))):
        field = f"topic_agent_team_profiles[{index}]"
        profile_id = _first_string(item, ("id", "topic_agent_team_profile_id", "profile_id", "ref"))
        profile_path = _first_string(item, ("path", "profile_path", "source_path", "config_path", "source"))
        template_id = _first_string(
            item,
            (
                "domain_agent_team_template_id",
                "domain_agent_team_template_ref",
                "template_id",
                "template_ref",
            ),
        )
        research_topic_id = _first_string(item, ("research_topic_id", "topic_id"))
        missing: list[str] = []
        if profile_id is None:
            missing.append("id")
        if profile_path is None:
            missing.append("path")
        if template_id is None:
            missing.append("domain_agent_team_template_id")
        if research_topic_id is None:
            missing.append("research_topic_id")
        if missing:
            diagnostics.append(
                Diagnostic(
                    code="ISO003",
                    severity="error",
                    concept="Topic Agent Team Profile registration",
                    path=path,
                    field=field,
                    message=f"Topic Agent Team Profile registration must include {', '.join(missing)}.",
                )
            )
            continue
        assert profile_id is not None
        assert profile_path is not None
        assert template_id is not None
        assert research_topic_id is not None
        registrations.append(
            TopicAgentTeamProfileRegistration(
                id=profile_id,
                path_input=profile_path,
                domain_agent_team_template_id=template_id,
                research_topic_id=research_topic_id,
                schema_version=_first_string(item, ("schema_version",)) or TOPIC_AGENT_TEAM_PROFILE_SCHEMA_VERSION,
                status=_first_string(item, ("status",)) or "active",
                source_path=path,
            )
        )
    return registrations


def _table_items(value: object) -> list[dict[str, Any]]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        if all(isinstance(item, dict) for item in value.values()):
            items: list[dict[str, Any]] = []
            for key, item in value.items():
                copied = dict(item)
                copied.setdefault("id", key)
                items.append(copied)
            return items
        return [value]
    return []


def _registration_ids(value: object) -> list[str]:
    if isinstance(value, list):
        ids: list[str] = []
        for item in value:
            if isinstance(item, str):
                ids.append(item)
            elif isinstance(item, dict):
                item_id = _first_string(item, ("id", "ref", "built_in_ref"))
                if item_id is not None:
                    ids.append(item_id)
        return ids
    if isinstance(value, dict):
        return sorted(str(key) for key in value)
    return []


def _callback_registry_ref_values(raw: dict[str, Any]) -> list[str]:
    values: list[str] = []
    values.extend(_string_refs(raw.get("user_skill_callback_registry_ref")))
    values.extend(_string_refs(raw.get("user_skill_callback_registry_refs")))
    nested_refs = raw.get("refs")
    if isinstance(nested_refs, dict):
        values.extend(_string_refs(nested_refs.get("user_skill_callback_registry_ref")))
        values.extend(_string_refs(nested_refs.get("user_skill_callback_registry_refs")))
    return list(dict.fromkeys(values))


def _string_refs(value: object) -> list[str]:
    if isinstance(value, str) and value:
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str) and item]
    return []


def _dict_value(value: object) -> dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)
    return {}


def _first_string(data: dict[str, Any], keys: tuple[str, ...]) -> str | None:
    for key in keys:
        value = data.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def _status_string(
    data: dict[str, Any],
    path: Path,
    field: str,
    concept: str,
    diagnostics: list[Diagnostic],
) -> str | None:
    value = data.get("status", "active")
    if value in {"active", "archived"}:
        return str(value)
    diagnostics.append(
        Diagnostic(
            code="ISO003",
            severity="error",
            concept=concept,
            path=path,
            field=f"{field}.status",
            message="Status must be active or archived.",
        )
    )
    return None
