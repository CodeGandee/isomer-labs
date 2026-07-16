"""Semantic Workspace Surface Labels, default layout helpers, and tmp policy."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import TYPE_CHECKING, Mapping

from isomer_labs.core.diagnostics import Diagnostic
from isomer_labs.core.path_utils import display_path, is_within, resolve_project_path
from isomer_labs.models import EffectiveTopicContext

if TYPE_CHECKING:
    from isomer_labs.workspace.manifest import EffectiveAgentContext, EffectiveTopicActorContext


ISOMER_CONTENT_ROOT_DIR = "isomer-content"
TOPIC_WORKSPACE_BASE_DIR = f"{ISOMER_CONTENT_ROOT_DIR}/topic-ws"
TOPIC_WORKSPACE_BASE_NAME = "topic-ws"

CONTENT_ROOT_README_TEXT = """# Isomer Content

This directory is the default Project-local home for Isomer-generated content.

Fresh Projects ignore generated content under this root by default. The generated `.gitignore` keeps this `README.md` and the `.gitignore` policy file trackable, while Topic Workspaces and other generated files stay local unless you intentionally track selected files.

Default Topic Workspaces live under `topic-ws/<topic-id>/`.
"""

CONTENT_ROOT_GITIGNORE_TEXT = """*
!.gitignore
!/README.md
"""


def content_path_defaults_for_init(project_root: Path, content_dir: str | None = None) -> dict[str, str]:
    content_root = selected_content_root_path(project_root, content_dir)
    content_root_input = display_path(content_root, project_root)
    return {
        "isomer_content_root": content_root_input,
        "topic_workspace_base_dir": f"{content_root_input}/{TOPIC_WORKSPACE_BASE_NAME}",
    }


def selected_content_root_path(project_root: Path, content_dir: str | None = None) -> Path:
    if content_dir is not None and content_dir:
        return resolve_project_path(project_root, content_dir)
    return project_root / ISOMER_CONTENT_ROOT_DIR


def content_root_path(project_root: Path, path_defaults: Mapping[str, object] | None = None) -> Path:
    value = _path_default(path_defaults, "isomer_content_root")
    if value is not None:
        return resolve_project_path(project_root, value)
    return project_root / ISOMER_CONTENT_ROOT_DIR


def topic_workspace_base_path(project_root: Path, path_defaults: Mapping[str, object] | None = None) -> Path:
    value = _path_default(path_defaults, "topic_workspace_base_dir")
    if value is not None:
        return resolve_project_path(project_root, value)
    return content_root_path(project_root, path_defaults) / TOPIC_WORKSPACE_BASE_NAME


def topic_workspace_path(
    project_root: Path,
    topic_id: str,
    path_defaults: Mapping[str, object] | None = None,
) -> Path:
    return topic_workspace_base_path(project_root, path_defaults) / topic_id


def topic_workspace_path_input(topic_id: str) -> str:
    return f"{TOPIC_WORKSPACE_BASE_DIR}/{topic_id}"


def topic_workspace_path_input_from_defaults(topic_id: str, path_defaults: Mapping[str, object]) -> str:
    base = _path_default(path_defaults, "topic_workspace_base_dir") or TOPIC_WORKSPACE_BASE_DIR
    return f"{base}/{topic_id}"


def _path_default(path_defaults: Mapping[str, object] | None, key: str) -> str | None:
    if path_defaults is None:
        return None
    value = path_defaults.get(key)
    if isinstance(value, str) and value:
        return value
    return None


@dataclass(frozen=True)
class StorageProfile:
    id: str
    context: str
    kind: str
    lifecycle: str
    visibility: str
    safety_policy: str
    owner: str
    path_kind: str = "directory"
    git_semantics: str | None = None

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "id": self.id,
            "context": self.context,
            "kind": self.kind,
            "lifecycle": self.lifecycle,
            "visibility": self.visibility,
            "safety_policy": self.safety_policy,
            "owner": self.owner,
            "path_kind": self.path_kind,
        }
        if self.git_semantics is not None:
            data["git_semantics"] = self.git_semantics
        return data


@dataclass(frozen=True)
class SemanticSurface:
    label: str
    scope: str
    owner: str
    durability: str
    sharing: str
    required_context: str | None
    compatibility_surface: str
    default_template: str
    storage_profile: str
    path_kind: str = "directory"
    command_required: tuple[str, ...] = ()
    git_semantics: str | None = None
    label_source: str = "builtin"
    grouped_family: str | None = None
    allow_user_binding: bool = True

    def to_json(self) -> dict[str, object]:
        storage_profile = storage_profile_by_id(self.storage_profile)
        data: dict[str, object] = {
            "label": self.label,
            "scope": self.scope,
            "owner": self.owner,
            "durability": self.durability,
            "sharing": self.sharing,
            "compatibility_surface": self.compatibility_surface,
            "default_template": self.default_template,
            "storage_profile": self.storage_profile,
            "path_kind": self.path_kind,
            "command_required": list(self.command_required),
            "label_source": self.label_source,
        }
        if storage_profile is not None:
            data["storage_profile_traits"] = storage_profile.to_json()
        if self.required_context is not None:
            data["required_context"] = self.required_context
        if self.git_semantics is not None:
            data["git_semantics"] = self.git_semantics
        if self.grouped_family is not None:
            data["grouped_family"] = self.grouped_family
        return data


@dataclass(frozen=True)
class TmpSurfaceIgnorePolicy:
    label: str
    gitignore_path: Path
    ignored_path: Path
    relative_root: Path
    entry: str

    def to_json(self) -> dict[str, object]:
        return {
            "semantic_label": self.label,
            "gitignore_path": str(self.gitignore_path),
            "ignored_path": str(self.ignored_path),
            "relative_root": str(self.relative_root),
            "entry": self.entry,
        }


STORAGE_PROFILES = (
    StorageProfile("project_durable_dir", "project", "directory", "durable", "project", "project_local", "project"),
    StorageProfile("topic_workspace_root", "topic", "directory", "durable", "topic", "topic_workspace_local", "topic"),
    StorageProfile("topic_runtime_file", "topic", "file", "durable", "private", "topic_workspace_local", "runtime", path_kind="file"),
    StorageProfile("topic_runtime_dir", "topic", "directory", "durable", "private", "topic_workspace_local", "runtime"),
    StorageProfile("topic_records_dir", "topic", "directory", "durable", "topic", "topic_workspace_local", "topic"),
    StorageProfile("topic_durable_dir", "topic", "directory", "durable", "topic", "topic_workspace_local", "topic"),
    StorageProfile("topic_workspace_summary_file", "topic", "file", "durable", "topic", "topic_workspace_local", "topic", path_kind="file"),
    StorageProfile("topic_intent_source_file", "topic", "file", "durable", "topic", "topic_workspace_local", "topic", path_kind="file"),
    StorageProfile("topic_env_target_spec_file", "topic", "file", "durable", "topic", "topic_workspace_local", "service", path_kind="file"),
    StorageProfile("topic_private_dir", "topic", "directory", "durable", "private", "topic_workspace_local", "topic"),
    StorageProfile("topic_disposable_dir", "topic", "directory", "disposable", "private", "topic_workspace_local", "topic"),
    StorageProfile("topic_repo", "topic", "repository", "durable", "topic", "topic_workspace_local", "topic", git_semantics="repository"),
    StorageProfile("topic_repo_disposable_dir", "topic", "directory", "disposable", "private", "topic_repo_local", "topic"),
    StorageProfile("topic_repo_tracked_dir", "topic", "directory", "durable", "shared", "topic_repo_local", "topic"),
    StorageProfile("topic_repo_readonly_projection_dir", "topic", "directory", "durable", "topic_read", "topic_repo_local", "topic"),
    StorageProfile("topic_repo_writable_projection_dir", "topic", "directory", "durable", "topic_write", "topic_repo_local", "topic"),
    StorageProfile("topic_repo_tracked_file", "topic", "file", "durable", "shared", "topic_repo_local", "topic", path_kind="file"),
    StorageProfile("topic_actor_worktree", "topic_actor", "repository", "durable", "private", "topic_actor_workspace_local", "topic_actor", git_semantics="worktree"),
    StorageProfile("topic_actor_durable_dir", "topic_actor", "directory", "durable", "private", "topic_actor_workspace_local", "topic_actor"),
    StorageProfile("topic_actor_disposable_dir", "topic_actor", "directory", "disposable", "private", "topic_actor_workspace_local", "topic_actor"),
    StorageProfile("topic_actor_advisory_dir", "topic_actor", "directory", "advisory", "private", "topic_actor_workspace_local", "topic_actor"),
    StorageProfile("agent_worktree", "agent", "repository", "durable", "private", "agent_workspace_local", "agent", git_semantics="worktree"),
    StorageProfile("agent_durable_dir", "agent", "directory", "durable", "private", "agent_workspace_local", "agent"),
    StorageProfile("agent_disposable_dir", "agent", "directory", "disposable", "private", "agent_workspace_local", "agent"),
    StorageProfile("agent_peer_read_dir", "agent", "directory", "durable", "peer_read", "agent_workspace_local", "agent"),
    StorageProfile("agent_topic_dir", "agent", "directory", "durable", "topic", "agent_workspace_local", "topic"),
    StorageProfile("agent_topic_read_dir", "agent", "directory", "durable", "topic_read", "agent_workspace_local", "topic"),
    StorageProfile("agent_topic_write_dir", "agent", "directory", "durable", "topic_write", "agent_workspace_local", "topic"),
    StorageProfile("agent_advisory_dir", "agent", "directory", "advisory", "private", "agent_workspace_local", "agent"),
)

LOCAL_TMP_SURFACE_LABELS = ("topic.tmp", "topic.repos.main.tmp", "topic.actors.tmp", "agent.tmp")

RESERVED_LABEL_ROOTS = frozenset(("project", "topic", "agent", "custom"))
ISOMER_RESERVED_LABEL_ROOTS = frozenset(("project", "topic", "agent"))
CUSTOM_LABEL_ROOT = "custom"
GROUPED_TOPIC_REPO_PREFIX = "topic.repos."
_LABEL_SEGMENT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")


def storage_profiles() -> dict[str, StorageProfile]:
    return {profile.id: profile for profile in STORAGE_PROFILES}


def storage_profile_by_id(profile_id: str) -> StorageProfile | None:
    return storage_profiles().get(profile_id)


def catalog() -> dict[str, SemanticSurface]:
    return {surface.label: surface for surface in SEMANTIC_SURFACES}


def compatibility_aliases() -> dict[str, str]:
    return {surface.compatibility_surface: surface.label for surface in SEMANTIC_SURFACES}


def semantic_label_for_surface(surface: str) -> str | None:
    if ":" in surface:
        prefix, _ = surface.split(":", 1)
        return compatibility_aliases().get(prefix)
    return compatibility_aliases().get(surface)


def compatibility_surface_for_label(
    label: str,
    *,
    agent_name: str | None = None,
    topic_actor_name: str | None = None,
) -> str | None:
    surface = catalog().get(label)
    if surface is None:
        if is_grouped_topic_repo_label(label):
            surface_name = label.replace(".", "_")
            return surface_name if agent_name is None else f"{surface_name}:{agent_name}"
        return None
    if surface.scope == "topic_actor" and topic_actor_name:
        return f"{surface.compatibility_surface}:{topic_actor_name}"
    if surface.scope == "agent" and agent_name:
        return f"{surface.compatibility_surface}:{agent_name}"
    return surface.compatibility_surface


def _surface(
    label: str,
    scope: str,
    compatibility_surface: str,
    default_template: str,
    storage_profile: str,
    *,
    required_context: str | None = None,
    command_required: tuple[str, ...] = (),
    label_source: str = "builtin",
    grouped_family: str | None = None,
    allow_user_binding: bool = True,
) -> SemanticSurface:
    profile = storage_profile_by_id(storage_profile)
    if profile is None:
        raise ValueError(f"Unknown storage profile: {storage_profile}")
    return SemanticSurface(
        label=label,
        scope=scope,
        owner=profile.owner,
        durability=profile.lifecycle,
        sharing=profile.visibility,
        required_context=required_context,
        compatibility_surface=compatibility_surface,
        default_template=default_template,
        storage_profile=storage_profile,
        path_kind=profile.path_kind,
        command_required=command_required,
        git_semantics=profile.git_semantics,
        label_source=label_source,
        grouped_family=grouped_family,
        allow_user_binding=allow_user_binding,
    )


SEMANTIC_SURFACES = (
    _surface("topic.workspace", "topic", "topic_workspace", ".", "topic_workspace_root"),
    _surface("topic.runtime.db", "topic", "workspace_runtime_db", "state.sqlite", "topic_runtime_file", command_required=("runtime.init",)),
    _surface("topic.runtime", "topic", "runtime", "runtime", "topic_runtime_dir", command_required=("runtime.init",)),
    _surface("topic.records", "topic", "records", "records", "topic_records_dir", command_required=("runtime.init",)),
    _surface("topic.records.artifacts", "topic", "records_artifacts", "records/artifacts", "topic_records_dir", command_required=("runtime.init",)),
    _surface("topic.records.tasks", "topic", "records_tasks", "records/tasks", "topic_records_dir", command_required=("runtime.init",)),
    _surface("topic.records.runs", "topic", "records_runs", "records/runs", "topic_records_dir", command_required=("runtime.init",)),
    _surface("topic.records.views", "topic", "records_views", "records/views", "topic_records_dir", command_required=("runtime.init",)),
    _surface("topic.records.logs", "topic", "records_logs", "records/logs", "topic_records_dir", command_required=("runtime.init",)),
    _surface("topic.team_profile_bundle", "topic", "topic_team_profile_bundle", "team-profile", "topic_durable_dir"),
    _surface("topic.workspace.summary", "topic", "topic_workspace_summary", "isomer-topic-workspace-summary.md", "topic_workspace_summary_file"),
    _surface("topic.intent.overview", "topic", "topic_intent_overview", "intent/src/topic-overview.md", "topic_intent_source_file"),
    _surface("topic.intent.topic_env_requirements", "topic", "topic_intent_topic_env_requirements", "intent/src/topic-env-gate.md", "topic_intent_source_file"),
    _surface("topic.intent.agent_env_requirements", "topic", "topic_intent_agent_env_requirements", "intent/src/agent-env-gate.md", "topic_intent_source_file"),
    _surface("topic.intent.actor_definitions", "topic", "topic_intent_actor_definitions", "intent/src/actor-definitions.md", "topic_intent_source_file"),
    _surface("topic.env.topic_setup_target_spec", "topic", "topic_env_topic_setup_target_spec", "intent/derived/isomer-env-gate.md", "topic_env_target_spec_file"),
    _surface("topic.env.agent_setup_target_spec", "topic", "topic_env_agent_setup_target_spec", "intent/derived/isomer-agent-env-gate.md", "topic_env_target_spec_file"),
    _surface("topic.env.actor_env_gates", "topic", "topic_env_actor_env_gates", "intent/derived/actor-env-gates.md", "topic_env_target_spec_file"),
    _surface("topic.paper.template_exchange_root", "topic", "topic_paper_template_exchange_root", "intent/derived/writing-template", "topic_durable_dir"),
    _surface("topic.tmp", "topic", "topic_tmp", "tmp", "topic_disposable_dir"),
    _surface("topic.repos.main", "topic", "topic_main_repo", "repos/topic-main", "topic_repo", grouped_family="topic.repos"),
    _surface("topic.repos.main.tmp", "topic", "topic_main_tmp", "repos/topic-main/tmp", "topic_repo_disposable_dir"),
    _surface("topic.repos.main.isomer_managed", "topic", "topic_main_isomer_managed", "repos/topic-main/isomer-managed", "topic_durable_dir"),
    _surface("topic.repos.main.tracked", "topic", "topic_main_tracked", "repos/topic-main/isomer-managed/tracked", "topic_repo_tracked_dir"),
    _surface("topic.repos.main.tracked.shared", "topic", "topic_main_tracked_shared", "repos/topic-main/isomer-managed/tracked/shared", "topic_repo_tracked_dir"),
    _surface("topic.repos.main.tracked.artifacts", "topic", "topic_main_tracked_artifacts", "repos/topic-main/isomer-managed/tracked/artifacts", "topic_repo_tracked_dir"),
    _surface("topic.repos.main.tracked.tasks", "topic", "topic_main_tracked_tasks", "repos/topic-main/isomer-managed/tracked/tasks", "topic_repo_tracked_dir"),
    _surface("topic.repos.main.tracked.runs", "topic", "topic_main_tracked_runs", "repos/topic-main/isomer-managed/tracked/runs", "topic_repo_tracked_dir"),
    _surface("topic.repos.main.tracked.views", "topic", "topic_main_tracked_views", "repos/topic-main/isomer-managed/tracked/views", "topic_repo_tracked_dir"),
    _surface("topic.repos.main.tracked.tools", "topic", "topic_main_tracked_tools", "repos/topic-main/isomer-managed/tracked/tools", "topic_repo_tracked_dir"),
    _surface("topic.repos.main.tracked.boundaries", "topic", "topic_main_tracked_boundaries", "repos/topic-main/isomer-managed/tracked/boundaries", "topic_repo_tracked_dir"),
    _surface("topic.repos.main.tracked.manifests", "topic", "topic_main_tracked_manifests", "repos/topic-main/isomer-managed/tracked/manifests", "topic_repo_tracked_dir"),
    _surface("topic.repos.main.projections.readonly", "topic", "topic_main_projections_readonly", "repos/topic-main/isomer-managed/topic-owned/readonly/extern", "topic_repo_readonly_projection_dir"),
    _surface("topic.repos.main.projections.writable", "topic", "topic_main_projections_writable", "repos/topic-main/isomer-managed/topic-owned/writable/extern", "topic_repo_writable_projection_dir"),
    _surface("topic.repos.main.projections.manifest", "topic", "topic_main_projections_manifest", "repos/topic-main/isomer-managed/tracked/manifests/extern-projections.toml", "topic_repo_tracked_file"),
    _surface("topic.agents_root", "topic", "agents", "agents", "topic_private_dir"),
    _surface("topic.actors_root", "topic", "actors", "actors", "topic_private_dir"),
    _surface("topic.actors.workspace", "topic_actor", "topic_actor_workspace", "actors/{topic_actor_name}", "topic_actor_worktree", required_context="topic_actor"),
    _surface("topic.actors.tmp", "topic_actor", "topic_actor_tmp", "actors/{topic_actor_name}/tmp", "topic_actor_disposable_dir", required_context="topic_actor"),
    _surface("topic.actors.isomer_managed", "topic_actor", "topic_actor_isomer_managed", "actors/{topic_actor_name}/isomer-managed", "topic_actor_durable_dir", required_context="topic_actor"),
    _surface("topic.actors.output_root", "topic_actor", "topic_actor_output_root", "actors/{topic_actor_name}/isomer-managed/worker-output/topic-actors/{topic_actor_name}", "topic_actor_durable_dir", required_context="topic_actor"),
    _surface("topic.actors.private_artifacts", "topic_actor", "topic_actor_private_artifacts", "actors/{topic_actor_name}/isomer-managed/actor-owned/artifacts", "topic_actor_durable_dir", required_context="topic_actor"),
    _surface("topic.actors.logs", "topic_actor", "topic_actor_logs", "actors/{topic_actor_name}/isomer-managed/actor-owned/logs", "topic_actor_durable_dir", required_context="topic_actor"),
    _surface("topic.actors.links", "topic_actor", "topic_actor_links", "actors/{topic_actor_name}/isomer-managed/links", "topic_actor_advisory_dir", required_context="topic_actor"),
    _surface("agent.workspace", "agent", "agent_workspace", "agents/{agent_name}", "agent_worktree", required_context="agent"),
    _surface("agent.tmp", "agent", "agent_tmp", "agents/{agent_name}/tmp", "agent_disposable_dir", required_context="agent"),
    _surface("agent.isomer_managed", "agent", "agent_isomer_managed", "agents/{agent_name}/isomer-managed", "agent_durable_dir", required_context="agent"),
    _surface("agent.output_root", "agent", "agent_output_root", "agents/{agent_name}/isomer-managed/worker-output/agents/{agent_name}", "agent_durable_dir", required_context="agent"),
    _surface("agent.owned", "agent", "agent_owned", "agents/{agent_name}/isomer-managed/agent-owned", "agent_durable_dir", required_context="agent"),
    _surface("agent.runtime", "agent", "agent_runtime", "agents/{agent_name}/isomer-managed/agent-owned/runtime", "agent_durable_dir", required_context="agent"),
    _surface("agent.private_artifacts", "agent", "agent_artifacts", "agents/{agent_name}/isomer-managed/agent-owned/artifacts", "agent_durable_dir", required_context="agent"),
    _surface("agent.scratch", "agent", "agent_scratch", "agents/{agent_name}/isomer-managed/agent-owned/scratch", "agent_disposable_dir", required_context="agent"),
    _surface("agent.logs", "agent", "agent_logs", "agents/{agent_name}/isomer-managed/agent-owned/logs", "agent_durable_dir", required_context="agent"),
    _surface("agent.public_share", "agent", "agent_public_share", "agents/{agent_name}/isomer-managed/agent-owned/public", "agent_peer_read_dir", required_context="agent"),
    _surface("agent.inbox", "agent", "agent_inbox", "agents/{agent_name}/isomer-managed/agent-owned/inbox", "agent_durable_dir", required_context="agent"),
    _surface("agent.topic_owned", "agent", "agent_topic_owned", "agents/{agent_name}/isomer-managed/topic-owned", "agent_topic_dir", required_context="agent"),
    _surface("agent.topic_readonly", "agent", "agent_topic_readonly", "agents/{agent_name}/isomer-managed/topic-owned/readonly", "agent_topic_read_dir", required_context="agent"),
    _surface("agent.topic_writable", "agent", "agent_topic_writable", "agents/{agent_name}/isomer-managed/topic-owned/writable", "agent_topic_write_dir", required_context="agent"),
    _surface("agent.links", "agent", "agent_links", "agents/{agent_name}/isomer-managed/links", "agent_advisory_dir", required_context="agent"),
)


STANDARD_TOPIC_MATERIALIZATION_LABELS = (
    "topic.runtime",
    "topic.records",
    "topic.records.artifacts",
    "topic.records.tasks",
    "topic.records.runs",
    "topic.records.views",
    "topic.records.logs",
    "topic.repos.main",
    "topic.tmp",
    "topic.repos.main.isomer_managed",
    "topic.agents_root",
    "topic.actors_root",
    "topic.team_profile_bundle",
)


PATH_ENV_VARS_BY_LABEL = {
    "topic.runtime.db": "ISOMER_TOPIC_WORKSPACE_RUNTIME_DB",
    "topic.tmp": "ISOMER_TOPIC_WORKSPACE_TMP_DIR",
    "topic.repos.main": "ISOMER_TOPIC_MAIN_REPO_DIR",
    "topic.repos.main.tmp": "ISOMER_TOPIC_MAIN_TMP_DIR",
    "topic.repos.main.isomer_managed": "ISOMER_TOPIC_MAIN_ISOMER_MANAGED_DIR",
    "topic.repos.main.projections.readonly": "ISOMER_TOPIC_MAIN_PROJECTIONS_READONLY_DIR",
    "topic.repos.main.projections.writable": "ISOMER_TOPIC_MAIN_PROJECTIONS_WRITABLE_DIR",
    "topic.repos.main.projections.manifest": "ISOMER_TOPIC_MAIN_PROJECTIONS_MANIFEST",
    "topic.records": "ISOMER_TOPIC_WORKSPACE_RECORDS_DIR",
    "topic.records.artifacts": "ISOMER_TOPIC_WORKSPACE_ARTIFACTS_DIR",
    "topic.records.tasks": "ISOMER_TOPIC_WORKSPACE_TASKS_DIR",
    "topic.records.runs": "ISOMER_TOPIC_WORKSPACE_RUNS_DIR",
    "topic.records.views": "ISOMER_TOPIC_WORKSPACE_VIEWS_DIR",
    "topic.records.logs": "ISOMER_TOPIC_WORKSPACE_LOGS_DIR",
    "topic.workspace.summary": "ISOMER_TOPIC_WORKSPACE_SUMMARY",
    "topic.runtime": "ISOMER_TOPIC_WORKSPACE_RUNTIME_DIR",
    "topic.paper.template_exchange_root": "ISOMER_TOPIC_PAPER_TEMPLATE_EXCHANGE_ROOT",
    "topic.actors_root": "ISOMER_TOPIC_ACTORS_ROOT_DIR",
    "topic.actors.workspace": "ISOMER_TOPIC_ACTOR_WORKSPACE_DIR",
    "topic.actors.tmp": "ISOMER_TOPIC_ACTOR_TMP_DIR",
    "topic.actors.isomer_managed": "ISOMER_TOPIC_ACTOR_ISOMER_MANAGED_DIR",
    "topic.actors.output_root": "ISOMER_TOPIC_ACTOR_OUTPUT_ROOT_DIR",
    "topic.actors.private_artifacts": "ISOMER_TOPIC_ACTOR_PRIVATE_ARTIFACTS_DIR",
    "topic.actors.logs": "ISOMER_TOPIC_ACTOR_LOGS_DIR",
    "topic.actors.links": "ISOMER_TOPIC_ACTOR_LINKS_DIR",
    "agent.workspace": "ISOMER_AGENT_WORKSPACE_DIR",
    "agent.tmp": "ISOMER_AGENT_WORKSPACE_TMP_DIR",
    "agent.isomer_managed": "ISOMER_AGENT_ISOMER_MANAGED_DIR",
    "agent.output_root": "ISOMER_AGENT_OUTPUT_ROOT_DIR",
    "agent.owned": "ISOMER_AGENT_OWNED_DIR",
    "agent.runtime": "ISOMER_AGENT_WORKSPACE_RUNTIME_DIR",
    "agent.private_artifacts": "ISOMER_AGENT_WORKSPACE_ARTIFACTS_DIR",
    "agent.scratch": "ISOMER_AGENT_WORKSPACE_SCRATCH_DIR",
    "agent.logs": "ISOMER_AGENT_WORKSPACE_LOGS_DIR",
    "agent.topic_owned": "ISOMER_AGENT_TOPIC_OWNED_DIR",
    "agent.links": "ISOMER_AGENT_LINKS_DIR",
}


def generated_env_var_for_label(label: str) -> str:
    return "ISOMER_PATH__" + "__".join(segment.upper() for segment in label.split("."))


def label_root(label: str) -> str:
    return label.split(".", 1)[0]


def label_segments_are_valid(label: str) -> bool:
    return all(_LABEL_SEGMENT_RE.match(segment) for segment in label.split("."))


def is_custom_label(label: str) -> bool:
    return label.startswith("custom.") and label_segments_are_valid(label)


def is_grouped_topic_repo_label(label: str) -> bool:
    if not label.startswith(GROUPED_TOPIC_REPO_PREFIX):
        return False
    suffix = label[len(GROUPED_TOPIC_REPO_PREFIX) :]
    if suffix.startswith("main."):
        return False
    return bool(suffix) and all(_LABEL_SEGMENT_RE.match(segment) for segment in suffix.split("."))


def dynamic_surface_for_label(label: str, storage_profile: str) -> SemanticSurface | None:
    profile = storage_profile_by_id(storage_profile)
    if profile is None:
        return None
    if is_custom_label(label):
        compatibility_surface = label.replace(".", "_")
        return SemanticSurface(
            label=label,
            scope=profile.context,
            owner=profile.owner,
            durability=profile.lifecycle,
            sharing=profile.visibility,
            required_context=profile.context if profile.context in {"agent", "topic_actor"} else None,
            compatibility_surface=compatibility_surface,
            default_template="",
            storage_profile=storage_profile,
            path_kind=profile.path_kind,
            git_semantics=profile.git_semantics,
            label_source="manifest",
        )
    if is_grouped_topic_repo_label(label) and storage_profile == "topic_repo":
        return SemanticSurface(
            label=label,
            scope="topic",
            owner=profile.owner,
            durability=profile.lifecycle,
            sharing=profile.visibility,
            required_context=None,
            compatibility_surface=label.replace(".", "_"),
            default_template="",
            storage_profile=storage_profile,
            path_kind=profile.path_kind,
            git_semantics=profile.git_semantics,
            label_source="manifest",
            grouped_family="topic.repos",
        )
    return None


def tmp_surface_ignore_policy(
    context: EffectiveTopicContext,
    label: str,
    tmp_path: Path,
    *,
    env: Mapping[str, str],
    agent_context: EffectiveAgentContext | None = None,
    topic_actor_context: EffectiveTopicActorContext | None = None,
) -> tuple[TmpSurfaceIgnorePolicy | None, list[Diagnostic]]:
    diagnostics = _tmp_surface_boundary_diagnostics(
        context,
        label,
        tmp_path,
        env=env,
        agent_context=agent_context,
        topic_actor_context=topic_actor_context,
    )
    if any(diagnostic.is_error for diagnostic in diagnostics):
        return None, diagnostics
    if label == "topic.tmp":
        entry = _gitignore_entry(context.topic_workspace_path, tmp_path)
        if entry is None:
            return None, diagnostics
        return (
            TmpSurfaceIgnorePolicy(label, context.topic_workspace_path / ".gitignore", tmp_path, context.topic_workspace_path, entry),
            diagnostics,
        )
    if label == "topic.repos.main.tmp":
        topic_main, topic_main_diagnostics = _resolve_topic_main(context, env)
        diagnostics.extend(topic_main_diagnostics)
        if topic_main is None or any(diagnostic.is_error for diagnostic in diagnostics):
            return None, diagnostics
        entry = _gitignore_entry(topic_main, tmp_path)
        if entry is None:
            return None, diagnostics
        return TmpSurfaceIgnorePolicy(label, topic_main / ".gitignore", tmp_path, topic_main, entry), diagnostics
    if label == "agent.tmp" and agent_context is not None:
        topic_main, topic_main_diagnostics = _resolve_topic_main(context, env)
        diagnostics.extend(topic_main_diagnostics)
        if topic_main is None or any(diagnostic.is_error for diagnostic in diagnostics):
            return None, diagnostics
        entry = _gitignore_entry(agent_context.agent_workspace_path, tmp_path)
        if entry is None:
            return None, diagnostics
        return (
            TmpSurfaceIgnorePolicy(label, topic_main / ".gitignore", tmp_path, agent_context.agent_workspace_path, entry),
            diagnostics,
        )
    if label == "topic.actors.tmp" and topic_actor_context is not None:
        entry = _gitignore_entry(topic_actor_context.topic_actor_workspace_path, tmp_path)
        if entry is None:
            return None, diagnostics
        return (
            TmpSurfaceIgnorePolicy(
                label,
                topic_actor_context.topic_actor_workspace_path / ".gitignore",
                tmp_path,
                topic_actor_context.topic_actor_workspace_path,
                entry,
            ),
            diagnostics,
        )
    return None, diagnostics


def ensure_tmp_surface_ignore_policy(
    context: EffectiveTopicContext,
    label: str,
    tmp_path: Path,
    *,
    env: Mapping[str, str],
    agent_context: EffectiveAgentContext | None = None,
    topic_actor_context: EffectiveTopicActorContext | None = None,
) -> list[Diagnostic]:
    policy, diagnostics = tmp_surface_ignore_policy(
        context,
        label,
        tmp_path,
        env=env,
        agent_context=agent_context,
        topic_actor_context=topic_actor_context,
    )
    if policy is None or any(diagnostic.is_error for diagnostic in diagnostics):
        return diagnostics
    policy.gitignore_path.parent.mkdir(parents=True, exist_ok=True)
    existing = policy.gitignore_path.read_text(encoding="utf-8") if policy.gitignore_path.exists() else ""
    entries = {line.strip() for line in existing.splitlines() if line.strip() and not line.lstrip().startswith("#")}
    if policy.entry not in entries:
        prefix = "" if not existing or existing.endswith("\n") else "\n"
        with policy.gitignore_path.open("a", encoding="utf-8") as stream:
            stream.write(f"{prefix}{policy.entry}\n")
    return diagnostics


def _tmp_surface_boundary_diagnostics(
    context: EffectiveTopicContext,
    label: str,
    path: Path,
    *,
    env: Mapping[str, str],
    agent_context: EffectiveAgentContext | None,
    topic_actor_context: EffectiveTopicActorContext | None,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if label == "topic.tmp":
        if not is_within(path, context.topic_workspace_path):
            diagnostics.append(_tmp_boundary_diagnostic(label, "Local Tmp Surface must stay inside the selected Topic Workspace."))
        return diagnostics
    if label == "topic.repos.main.tmp":
        topic_main, topic_main_diagnostics = _resolve_topic_main(context, env)
        diagnostics.extend(topic_main_diagnostics)
        if topic_main is not None and not is_within(path, topic_main):
            diagnostics.append(_tmp_boundary_diagnostic(label, "`topic.repos.main.tmp` must stay inside `topic.repos.main`."))
        return diagnostics
    if label == "agent.tmp" and agent_context is not None and not is_within(path, agent_context.agent_workspace_path):
        diagnostics.append(_tmp_boundary_diagnostic(label, "`agent.tmp` must stay inside the resolved `agent.workspace`."))
    if label == "topic.actors.tmp" and topic_actor_context is not None and not is_within(path, topic_actor_context.topic_actor_workspace_path):
        diagnostics.append(_tmp_boundary_diagnostic(label, "`topic.actors.tmp` must stay inside the resolved `topic.actors.workspace`."))
    return diagnostics


def _resolve_topic_main(context: EffectiveTopicContext, env: Mapping[str, str]) -> tuple[Path | None, list[Diagnostic]]:
    from isomer_labs.workspace.manifest import resolve_semantic_binding

    result, diagnostics = resolve_semantic_binding(context, "topic.repos.main", env=env, agent_context=None)
    return (result.path if result is not None else None), diagnostics


def _tmp_boundary_diagnostic(label: str, message: str) -> Diagnostic:
    return Diagnostic(code="ISO005", severity="error", concept="Workspace Path Resolution", field=label, message=message)


def _gitignore_entry(root: Path, ignored_path: Path) -> str | None:
    try:
        relative = ignored_path.resolve(strict=False).relative_to(root.resolve(strict=False))
    except ValueError:
        return None
    value = relative.as_posix().rstrip("/")
    if value in ("", "."):
        return None
    return f"{value}/"
