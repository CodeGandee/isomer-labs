"""Semantic workspace surface catalog."""

from __future__ import annotations

from dataclasses import dataclass


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
    path_kind: str = "directory"
    command_required: tuple[str, ...] = ()
    git_semantics: str | None = None

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "label": self.label,
            "scope": self.scope,
            "owner": self.owner,
            "durability": self.durability,
            "sharing": self.sharing,
            "compatibility_surface": self.compatibility_surface,
            "default_template": self.default_template,
            "path_kind": self.path_kind,
            "command_required": list(self.command_required),
        }
        if self.required_context is not None:
            data["required_context"] = self.required_context
        if self.git_semantics is not None:
            data["git_semantics"] = self.git_semantics
        return data


LOCAL_TMP_SURFACE_LABELS = ("topic.tmp", "topic.main_repo.tmp", "agent.tmp")


def catalog() -> dict[str, SemanticSurface]:
    return {surface.label: surface for surface in SEMANTIC_SURFACES}


def compatibility_aliases() -> dict[str, str]:
    return {surface.compatibility_surface: surface.label for surface in SEMANTIC_SURFACES}


def semantic_label_for_surface(surface: str) -> str | None:
    if ":" in surface:
        prefix, _ = surface.split(":", 1)
        return compatibility_aliases().get(prefix)
    return compatibility_aliases().get(surface)


def compatibility_surface_for_label(label: str, *, agent_name: str | None = None) -> str | None:
    surface = catalog().get(label)
    if surface is None:
        return None
    if surface.scope == "agent" and agent_name:
        return f"{surface.compatibility_surface}:{agent_name}"
    return surface.compatibility_surface


def _surface(
    label: str,
    scope: str,
    owner: str,
    durability: str,
    sharing: str,
    compatibility_surface: str,
    default_template: str,
    *,
    required_context: str | None = None,
    path_kind: str = "directory",
    command_required: tuple[str, ...] = (),
    git_semantics: str | None = None,
) -> SemanticSurface:
    return SemanticSurface(
        label=label,
        scope=scope,
        owner=owner,
        durability=durability,
        sharing=sharing,
        required_context=required_context,
        compatibility_surface=compatibility_surface,
        default_template=default_template,
        path_kind=path_kind,
        command_required=command_required,
        git_semantics=git_semantics,
    )


SEMANTIC_SURFACES = (
    _surface("topic.workspace", "topic", "topic", "durable", "topic", "topic_workspace", "."),
    _surface("topic.runtime.db", "topic", "runtime", "durable", "private", "workspace_runtime_db", "state.sqlite", path_kind="file", command_required=("runtime.init",)),
    _surface("topic.runtime", "topic", "runtime", "durable", "private", "runtime", "runtime", command_required=("runtime.init",)),
    _surface("topic.records", "topic", "topic", "durable", "topic", "records", "records", command_required=("runtime.init",)),
    _surface("topic.records.artifacts", "topic", "topic", "durable", "topic", "records_artifacts", "records/artifacts", command_required=("runtime.init",)),
    _surface("topic.records.tasks", "topic", "topic", "durable", "topic", "records_tasks", "records/tasks", command_required=("runtime.init",)),
    _surface("topic.records.runs", "topic", "topic", "durable", "topic", "records_runs", "records/runs", command_required=("runtime.init",)),
    _surface("topic.records.views", "topic", "topic", "durable", "topic", "records_views", "records/views", command_required=("runtime.init",)),
    _surface("topic.records.logs", "topic", "topic", "durable", "topic", "records_logs", "records/logs", command_required=("runtime.init",)),
    _surface("topic.team_profile_bundle", "topic", "topic", "durable", "topic", "topic_team_profile_bundle", "team-profile"),
    _surface("topic.tmp", "topic", "topic", "disposable", "private", "topic_tmp", "tmp"),
    _surface("topic.main_repo", "topic", "topic", "git", "topic", "topic_main_repo", "repos/topic-main", git_semantics="repository"),
    _surface("topic.main_repo.tmp", "topic", "topic", "disposable", "private", "topic_main_tmp", "repos/topic-main/tmp"),
    _surface("topic.main_repo.isomer_managed", "topic", "topic", "durable", "topic", "topic_main_isomer_managed", "repos/topic-main/isomer-managed"),
    _surface("topic.main_repo.tracked", "topic", "topic", "durable", "shared", "topic_main_tracked", "repos/topic-main/isomer-managed/tracked"),
    _surface("topic.main_repo.tracked.shared", "topic", "topic", "durable", "shared", "topic_main_tracked_shared", "repos/topic-main/isomer-managed/tracked/shared"),
    _surface("topic.main_repo.tracked.artifacts", "topic", "topic", "durable", "shared", "topic_main_tracked_artifacts", "repos/topic-main/isomer-managed/tracked/artifacts"),
    _surface("topic.main_repo.tracked.tasks", "topic", "topic", "durable", "shared", "topic_main_tracked_tasks", "repos/topic-main/isomer-managed/tracked/tasks"),
    _surface("topic.main_repo.tracked.runs", "topic", "topic", "durable", "shared", "topic_main_tracked_runs", "repos/topic-main/isomer-managed/tracked/runs"),
    _surface("topic.main_repo.tracked.views", "topic", "topic", "durable", "shared", "topic_main_tracked_views", "repos/topic-main/isomer-managed/tracked/views"),
    _surface("topic.main_repo.tracked.tools", "topic", "topic", "durable", "shared", "topic_main_tracked_tools", "repos/topic-main/isomer-managed/tracked/tools"),
    _surface("topic.main_repo.tracked.boundaries", "topic", "topic", "durable", "shared", "topic_main_tracked_boundaries", "repos/topic-main/isomer-managed/tracked/boundaries"),
    _surface("topic.main_repo.tracked.manifests", "topic", "topic", "durable", "shared", "topic_main_tracked_manifests", "repos/topic-main/isomer-managed/tracked/manifests"),
    _surface("topic.agents_root", "topic", "topic", "durable", "private", "agents", "agents"),
    _surface("agent.workspace", "agent", "agent", "durable", "private", "agent_workspace", "agents/{agent_name}", required_context="agent", git_semantics="worktree"),
    _surface("agent.tmp", "agent", "agent", "disposable", "private", "agent_tmp", "agents/{agent_name}/tmp", required_context="agent"),
    _surface("agent.isomer_managed", "agent", "agent", "durable", "private", "agent_isomer_managed", "agents/{agent_name}/isomer-managed", required_context="agent"),
    _surface("agent.owned", "agent", "agent", "durable", "private", "agent_owned", "agents/{agent_name}/isomer-managed/agent-owned", required_context="agent"),
    _surface("agent.runtime", "agent", "agent", "durable", "private", "agent_runtime", "agents/{agent_name}/isomer-managed/agent-owned/runtime", required_context="agent"),
    _surface("agent.private_artifacts", "agent", "agent", "durable", "private", "agent_artifacts", "agents/{agent_name}/isomer-managed/agent-owned/artifacts", required_context="agent"),
    _surface("agent.scratch", "agent", "agent", "disposable", "private", "agent_scratch", "agents/{agent_name}/isomer-managed/agent-owned/scratch", required_context="agent"),
    _surface("agent.logs", "agent", "agent", "durable", "private", "agent_logs", "agents/{agent_name}/isomer-managed/agent-owned/logs", required_context="agent"),
    _surface("agent.public_share", "agent", "agent", "durable", "peer_read", "agent_public_share", "agents/{agent_name}/isomer-managed/agent-owned/public", required_context="agent"),
    _surface("agent.inbox", "agent", "agent", "durable", "private", "agent_inbox", "agents/{agent_name}/isomer-managed/agent-owned/inbox", required_context="agent"),
    _surface("agent.topic_owned", "agent", "topic", "durable", "topic", "agent_topic_owned", "agents/{agent_name}/isomer-managed/topic-owned", required_context="agent"),
    _surface("agent.topic_readonly", "agent", "topic", "durable", "topic_read", "agent_topic_readonly", "agents/{agent_name}/isomer-managed/topic-owned/readonly", required_context="agent"),
    _surface("agent.topic_writable", "agent", "topic", "durable", "topic_write", "agent_topic_writable", "agents/{agent_name}/isomer-managed/topic-owned/writable", required_context="agent"),
    _surface("agent.links", "agent", "agent", "advisory", "private", "agent_links", "agents/{agent_name}/isomer-managed/links", required_context="agent"),
)


STANDARD_TOPIC_MATERIALIZATION_LABELS = (
    "topic.runtime",
    "topic.records",
    "topic.records.artifacts",
    "topic.records.tasks",
    "topic.records.runs",
    "topic.records.views",
    "topic.records.logs",
    "topic.main_repo",
    "topic.tmp",
    "topic.main_repo.isomer_managed",
    "topic.agents_root",
    "topic.team_profile_bundle",
)


PATH_ENV_VARS_BY_LABEL = {
    "topic.runtime.db": "ISOMER_TOPIC_WORKSPACE_RUNTIME_DB",
    "topic.tmp": "ISOMER_TOPIC_WORKSPACE_TMP_DIR",
    "topic.main_repo": "ISOMER_TOPIC_MAIN_REPO_DIR",
    "topic.main_repo.tmp": "ISOMER_TOPIC_MAIN_TMP_DIR",
    "topic.main_repo.isomer_managed": "ISOMER_TOPIC_MAIN_ISOMER_MANAGED_DIR",
    "topic.records": "ISOMER_TOPIC_WORKSPACE_RECORDS_DIR",
    "topic.records.artifacts": "ISOMER_TOPIC_WORKSPACE_ARTIFACTS_DIR",
    "topic.records.tasks": "ISOMER_TOPIC_WORKSPACE_TASKS_DIR",
    "topic.records.runs": "ISOMER_TOPIC_WORKSPACE_RUNS_DIR",
    "topic.records.views": "ISOMER_TOPIC_WORKSPACE_VIEWS_DIR",
    "topic.records.logs": "ISOMER_TOPIC_WORKSPACE_LOGS_DIR",
    "topic.runtime": "ISOMER_TOPIC_WORKSPACE_RUNTIME_DIR",
    "agent.workspace": "ISOMER_AGENT_WORKSPACE_DIR",
    "agent.tmp": "ISOMER_AGENT_WORKSPACE_TMP_DIR",
    "agent.isomer_managed": "ISOMER_AGENT_ISOMER_MANAGED_DIR",
    "agent.owned": "ISOMER_AGENT_OWNED_DIR",
    "agent.runtime": "ISOMER_AGENT_WORKSPACE_RUNTIME_DIR",
    "agent.private_artifacts": "ISOMER_AGENT_WORKSPACE_ARTIFACTS_DIR",
    "agent.scratch": "ISOMER_AGENT_WORKSPACE_SCRATCH_DIR",
    "agent.logs": "ISOMER_AGENT_WORKSPACE_LOGS_DIR",
    "agent.topic_owned": "ISOMER_AGENT_TOPIC_OWNED_DIR",
    "agent.links": "ISOMER_AGENT_LINKS_DIR",
}
