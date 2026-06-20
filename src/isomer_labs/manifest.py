"""Project Manifest parsing."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from isomer_labs.diagnostics import Diagnostic
from isomer_labs.models import (
    PROJECT_MANIFEST_SCHEMA_VERSION,
    ProjectManifest,
    ResearchTopicRegistration,
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
    artifact_format_profiles = _registration_ids(raw.get("artifact_format_profiles"))
    artifact_extensions = _registration_ids(raw.get("artifact_extensions"))

    if not topics:
        diagnostics.append(
            Diagnostic(
                code="ISO003",
                severity="error",
                concept="Project Manifest",
                path=path,
                field="research_topics",
                message="Project Manifest must register at least one Research Topic.",
            )
        )

    manifest = ProjectManifest(
        schema_version=schema_version,
        source_path=path,
        research_topics=topics,
        topic_workspaces=workspaces,
        defaults=defaults,
        path_defaults=path_defaults,
        artifact_format_profiles=artifact_format_profiles,
        artifact_extensions=artifact_extensions,
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
