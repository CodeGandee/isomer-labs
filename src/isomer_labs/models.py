"""Typed Milestone 1 domain models."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from isomer_labs.diagnostics import Diagnostic


OUTPUT_SCHEMA_VERSION = "isomer-cli-output.v1"
PROJECT_MANIFEST_SCHEMA_VERSION = "isomer-project-manifest.v1"
RESEARCH_TOPIC_CONFIG_SCHEMA_VERSION = "isomer-research-topic-config.v1"
LOCAL_ACTIVE_CONTEXT_SCHEMA_VERSION = "isomer-local-active-context.v1"


@dataclass(frozen=True)
class ResearchTopicRegistration:
    id: str
    config_path_input: str
    topic_workspace_id: str | None
    schema_version: str
    status: str
    source_path: Path

    def to_json(self) -> dict[str, object]:
        return {
            "id": self.id,
            "config_path": self.config_path_input,
            "topic_workspace_id": self.topic_workspace_id,
            "schema_version": self.schema_version,
            "status": self.status,
        }


@dataclass(frozen=True)
class TopicWorkspaceRegistration:
    id: str
    research_topic_id: str | None
    path_input: str | None
    schema_version: str
    status: str
    source_path: Path

    def to_json(self) -> dict[str, object]:
        return {
            "id": self.id,
            "research_topic_id": self.research_topic_id,
            "path": self.path_input,
            "schema_version": self.schema_version,
            "status": self.status,
        }


@dataclass(frozen=True)
class ProjectManifest:
    schema_version: str
    source_path: Path
    research_topics: list[ResearchTopicRegistration]
    topic_workspaces: list[TopicWorkspaceRegistration]
    defaults: dict[str, Any] = field(default_factory=dict)
    path_defaults: dict[str, Any] = field(default_factory=dict)
    artifact_format_profiles: list[str] = field(default_factory=list)
    artifact_extensions: list[str] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)

    def first_topic(self, topic_id: str) -> ResearchTopicRegistration | None:
        return next((topic for topic in self.research_topics if topic.id == topic_id), None)

    def first_workspace(self, workspace_id: str) -> TopicWorkspaceRegistration | None:
        return next((workspace for workspace in self.topic_workspaces if workspace.id == workspace_id), None)

    def default_research_topic_id(self) -> str | None:
        for key in ("research_topic_id", "default_research_topic_id", "default_topic_id"):
            value = self.defaults.get(key)
            if isinstance(value, str) and value:
                return value
        return None

    def default_topic_workspace_id(self) -> str | None:
        for key in ("topic_workspace_id", "default_topic_workspace_id", "default_workspace_id"):
            value = self.defaults.get(key)
            if isinstance(value, str) and value:
                return value
        return None

    def to_json(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "path": str(self.source_path),
            "research_topics": [topic.to_json() for topic in self.research_topics],
            "topic_workspaces": [workspace.to_json() for workspace in self.topic_workspaces],
            "defaults": self.defaults,
            "path_defaults": self.path_defaults,
            "artifact_format_profiles": self.artifact_format_profiles,
            "artifact_extensions": self.artifact_extensions,
        }


@dataclass(frozen=True)
class ResearchTopicConfig:
    schema_version: str
    research_topic_id: str
    source_path: Path
    topic_statement: str | None = None
    measurable_objectives: list[str] = field(default_factory=list)
    defaults: dict[str, Any] = field(default_factory=dict)
    refs: dict[str, Any] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "research_topic_id": self.research_topic_id,
            "path": str(self.source_path),
            "topic_statement": self.topic_statement,
            "measurable_objectives": self.measurable_objectives,
            "defaults": self.defaults,
            "refs": self.refs,
        }


@dataclass(frozen=True)
class LocalActiveContext:
    schema_version: str
    source_path: Path
    refs: dict[str, str]
    raw: dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "path": str(self.source_path),
            "refs": self.refs,
        }


@dataclass(frozen=True)
class Project:
    root: Path
    config_dir: Path
    manifest_path: Path
    manifest: ProjectManifest
    discovery_source: str

    def to_json(self) -> dict[str, object]:
        return {
            "root": str(self.root),
            "project_config_directory": str(self.config_dir),
            "project_manifest": str(self.manifest_path),
            "discovery_source": self.discovery_source,
        }


@dataclass(frozen=True)
class ProjectState:
    project: Project
    topic_configs: dict[str, ResearchTopicConfig]
    local_context: LocalActiveContext | None
    diagnostics: list[Diagnostic]


@dataclass(frozen=True)
class SelectionRequest:
    research_topic_id: str | None = None
    topic_workspace_id: str | None = None
    research_inquiry_id: str | None = None
    research_task_id: str | None = None
    run_id: str | None = None
    agent_team_instance_id: str | None = None
    agent_instance_id: str | None = None
    topic_agent_team_profile_id: str | None = None

    def lifecycle_refs(self) -> dict[str, str]:
        refs = {
            "research_inquiry_id": self.research_inquiry_id,
            "research_task_id": self.research_task_id,
            "run_id": self.run_id,
            "agent_team_instance_id": self.agent_team_instance_id,
            "agent_instance_id": self.agent_instance_id,
            "topic_agent_team_profile_id": self.topic_agent_team_profile_id,
        }
        return {key: value for key, value in refs.items() if value is not None}


@dataclass(frozen=True)
class EffectiveTopicContext:
    project: Project
    research_topic: ResearchTopicRegistration
    research_topic_config: ResearchTopicConfig | None
    topic_workspace_id: str
    topic_workspace_path_input: str | None
    topic_workspace_path: Path
    schema_versions: dict[str, str]
    sources: dict[str, str]
    lifecycle_refs: dict[str, str] = field(default_factory=dict)

    def to_json(self) -> dict[str, object]:
        return {
            "project": self.project.to_json(),
            "research_topic_id": self.research_topic.id,
            "research_topic_config_path": (
                str(self.research_topic_config.source_path) if self.research_topic_config is not None else None
            ),
            "topic_workspace_id": self.topic_workspace_id,
            "topic_workspace_path_input": self.topic_workspace_path_input,
            "topic_workspace_path": str(self.topic_workspace_path),
            "schema_versions": self.schema_versions,
            "sources": self.sources,
            "lifecycle_refs": self.lifecycle_refs,
        }


@dataclass(frozen=True)
class ResolvedPathEntry:
    surface: str
    path: Path
    source: str
    source_detail: str | None = None

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "surface": self.surface,
            "path": str(self.path),
            "source": self.source,
        }
        if self.source_detail is not None:
            data["source_detail"] = self.source_detail
        return data


@dataclass(frozen=True)
class BuiltInSchema:
    name: str
    kind: str
    schema_version: str
    description: str

    def to_json(self) -> dict[str, object]:
        return {
            "name": self.name,
            "kind": self.kind,
            "schema_version": self.schema_version,
            "description": self.description,
        }
