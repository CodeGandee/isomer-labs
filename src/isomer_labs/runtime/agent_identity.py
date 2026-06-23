"""Project-level Agent Instance identity helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sqlite3

from isomer_labs.models import Project, TopicWorkspaceRegistration
from isomer_labs.path_utils import is_within, resolve_project_path


@dataclass(frozen=True)
class AgentInstanceIdLocation:
    agent_id: str
    db_path: Path
    agent_team_instance_id: str
    agent_role_id: str
    research_topic_id: str
    topic_workspace_id: str

    def record_ref(self) -> str:
        return (
            f"{self.db_path}:{self.topic_workspace_id}:"
            f"{self.agent_team_instance_id}:{self.agent_role_id}"
        )


def project_agent_instance_id_locations(
    project: Project,
) -> tuple[dict[str, list[AgentInstanceIdLocation]], list[tuple[Path, str]]]:
    locations: dict[str, list[AgentInstanceIdLocation]] = {}
    issues: list[tuple[Path, str]] = []

    for db_path in project_runtime_db_paths(project):
        if not db_path.exists():
            continue
        try:
            connection = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
            connection.row_factory = sqlite3.Row
            try:
                rows = connection.execute(
                    """
                    SELECT id, agent_team_instance_id, agent_role_id, research_topic_id, topic_workspace_id
                    FROM agent_instances
                    ORDER BY id, agent_team_instance_id, agent_role_id
                    """
                ).fetchall()
            finally:
                connection.close()
        except sqlite3.Error as exc:
            issues.append((db_path, str(exc)))
            continue
        for row in rows:
            location = AgentInstanceIdLocation(
                agent_id=row["id"],
                db_path=db_path,
                agent_team_instance_id=row["agent_team_instance_id"],
                agent_role_id=row["agent_role_id"],
                research_topic_id=row["research_topic_id"],
                topic_workspace_id=row["topic_workspace_id"],
            )
            locations.setdefault(location.agent_id, []).append(location)

    return locations, issues


def project_runtime_db_paths(project: Project) -> list[Path]:
    paths: list[Path] = []
    seen: set[Path] = set()

    for workspace in project.manifest.topic_workspaces:
        workspace_path = _workspace_path(project, workspace)
        if workspace_path is None:
            continue
        db_path = workspace_path / "state.sqlite"
        if db_path not in seen:
            paths.append(db_path)
            seen.add(db_path)

    registered_topic_ids = {
        workspace.research_topic_id
        for workspace in project.manifest.topic_workspaces
        if workspace.research_topic_id is not None
    }
    for topic in project.manifest.research_topics:
        if topic.id in registered_topic_ids:
            continue
        workspace_path = _default_workspace_path(project, topic.id)
        db_path = workspace_path / "state.sqlite"
        if db_path not in seen:
            paths.append(db_path)
            seen.add(db_path)

    return paths


def _workspace_path(project: Project, workspace: TopicWorkspaceRegistration) -> Path | None:
    if workspace.path_input is not None:
        path = resolve_project_path(project.root, workspace.path_input)
    else:
        workspace_id = workspace.research_topic_id or workspace.id
        path = _default_workspace_path(project, workspace_id)
    return path if is_within(path, project.root) else None


def _default_workspace_path(project: Project, workspace_id: str) -> Path:
    base = project.manifest.path_defaults.get("topic_workspace_base_dir")
    if isinstance(base, str) and base:
        return resolve_project_path(project.root, f"{base}/{workspace_id}")
    return resolve_project_path(project.root, f"topic-workspaces/{workspace_id}")
