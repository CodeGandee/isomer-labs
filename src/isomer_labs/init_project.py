"""Project initialization for the Milestone 1 CLI."""

from __future__ import annotations

from pathlib import Path
import re

from isomer_labs.diagnostics import Diagnostic
from isomer_labs.project import config_dir_for_root, manifest_path_for_root


TOPIC_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")


def initialize_project(
    project_root: Path,
    *,
    topic_id: str,
    topic_statement: str | None = None,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if TOPIC_ID_PATTERN.fullmatch(topic_id) is None:
        return [
            Diagnostic(
                code="ISO003",
                severity="error",
                concept="Research Topic",
                field="topic_id",
                message="Research Topic id must start with an alphanumeric character and contain only letters, numbers, dot, underscore, or hyphen.",
            )
        ]

    root = project_root.resolve(strict=False)
    manifest_path = manifest_path_for_root(root)
    if manifest_path.exists():
        return [
            Diagnostic(
                code="ISO003",
                severity="error",
                concept="Project Manifest",
                path=manifest_path,
                message="Project Manifest already exists; Milestone 1 init refuses to overwrite it.",
            )
        ]

    config_dir = config_dir_for_root(root)
    topic_config_dir = config_dir / "research-topics"
    topic_config_path = topic_config_dir / f"{topic_id}.toml"
    topic_workspace_path = root / "topic-workspaces" / topic_id

    topic_config_dir.mkdir(parents=True, exist_ok=True)
    topic_workspace_path.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(_manifest_text(topic_id), encoding="utf-8")
    topic_config_path.write_text(
        _topic_config_text(topic_id, topic_statement or f"{topic_id} Research Topic"),
        encoding="utf-8",
    )
    return diagnostics


def _manifest_text(topic_id: str) -> str:
    return (
        'schema_version = "isomer-project-manifest.v1"\n'
        "\n"
        "[defaults]\n"
        f'research_topic_id = "{topic_id}"\n'
        f'topic_workspace_id = "{topic_id}"\n'
        "\n"
        "[[research_topics]]\n"
        f'id = "{topic_id}"\n'
        'schema_version = "isomer-research-topic-registration.v1"\n'
        f'config_path = ".isomer-labs/research-topics/{topic_id}.toml"\n'
        f'topic_workspace_id = "{topic_id}"\n'
        'status = "active"\n'
        "\n"
        "[[topic_workspaces]]\n"
        f'id = "{topic_id}"\n'
        'schema_version = "isomer-topic-workspace.v1"\n'
        f'research_topic_id = "{topic_id}"\n'
        f'path = "topic-workspaces/{topic_id}"\n'
        'status = "active"\n'
    )


def _topic_config_text(topic_id: str, topic_statement: str) -> str:
    escaped_statement = topic_statement.replace("\\", "\\\\").replace('"', '\\"')
    return (
        'schema_version = "isomer-research-topic-config.v1"\n'
        f'research_topic_id = "{topic_id}"\n'
        f'topic_statement = "{escaped_statement}"\n'
        "measurable_objectives = []\n"
    )
