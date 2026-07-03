"""Topic Workspace Pixi binding target selection and resolution."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
import shutil
import subprocess
from typing import Any, Literal

from isomer_labs.models import (
    EffectiveTopicContext,
    ResolvedTopicStandalonePixiBinding,
    TopicStandalonePixiBindingTarget,
    TopicStandalonePixiTargetKind,
)
from isomer_labs.core.path_utils import canonicalize, display_path, is_within, resolve_project_path


PixiBindingFailureKind = Literal["pixi-tooling", "unresolvable-target", "confinement"]

PIXI_INSTALL_GUIDANCE = {
    "online": "Install Pixi with `curl -fsSL https://pixi.sh/install.sh | sh` or a supported package manager, then ensure `pixi` is on PATH.",
    "offline": "Copy a pre-downloaded Pixi executable for this platform to a directory on PATH, then rerun the command.",
}


@dataclass(frozen=True)
class TopicStandalonePixiBindingResolutionFailure:
    kind: PixiBindingFailureKind
    message: str
    target: TopicStandalonePixiBindingTarget
    target_path: Path
    target_kind: TopicStandalonePixiTargetKind
    command: list[str] = field(default_factory=list)
    resolved_manifest_path: Path | None = None
    environment_prefix: Path | None = None

    def to_json(self, project_root: Path) -> dict[str, object]:
        data: dict[str, object] = {
            "kind": self.kind,
            "message": self.message,
            "target": self.target.to_json(),
            "target_path": display_path(self.target_path, project_root),
            "target_kind": self.target_kind,
        }
        if self.command:
            data["command"] = self.command
        if self.resolved_manifest_path is not None:
            data["resolved_manifest_path"] = display_path(self.resolved_manifest_path, project_root)
        if self.environment_prefix is not None:
            data["environment_prefix"] = display_path(self.environment_prefix, project_root)
        if self.kind == "pixi-tooling":
            data["install_guidance"] = PIXI_INSTALL_GUIDANCE
        return data


def resolve_topic_standalone_pixi_binding(
    context: EffectiveTopicContext,
    *,
    pixi_executable: str | None = None,
) -> tuple[ResolvedTopicStandalonePixiBinding | None, TopicStandalonePixiBindingResolutionFailure | None]:
    project = context.project
    target = project.manifest.effective_topic_standalone_pixi_binding_target(
        context.research_topic.id,
        topic_workspace_path=context.topic_workspace_path,
        project_root=project.root,
    )
    target_path = resolve_project_path(project.root, target.target_path_input)
    target_kind = _target_kind(target_path)
    if not is_within(target_path, project.root):
        return None, TopicStandalonePixiBindingResolutionFailure(
            kind="confinement",
            message="Standalone Pixi binding target resolves outside the Project root.",
            target=target,
            target_path=target_path,
            target_kind=target_kind,
        )

    pixi_path = pixi_executable or shutil.which("pixi")
    if pixi_path is None:
        return None, TopicStandalonePixiBindingResolutionFailure(
            kind="pixi-tooling",
            message="Pixi executable was not found on PATH.",
            target=target,
            target_path=target_path,
            target_kind=target_kind,
        )

    command = [pixi_path, "info", "--json", "--manifest-path", str(target_path)]
    result, error = _run_command(command)
    if error is not None:
        return None, TopicStandalonePixiBindingResolutionFailure(
            kind="pixi-tooling",
            message=f"Pixi binding target resolution failed: {error}.",
            target=target,
            target_path=target_path,
            target_kind=target_kind,
            command=command,
        )
    assert result is not None
    if result.returncode != 0:
        return None, TopicStandalonePixiBindingResolutionFailure(
            kind="pixi-tooling",
            message=f"Pixi binding target resolution failed: {_command_failure_summary(result)}.",
            target=target,
            target_path=target_path,
            target_kind=target_kind,
            command=command,
        )

    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        return None, TopicStandalonePixiBindingResolutionFailure(
            kind="pixi-tooling",
            message=f"Pixi returned invalid JSON while resolving the binding target: {exc.msg}.",
            target=target,
            target_path=target_path,
            target_kind=target_kind,
            command=command,
        )
    if not isinstance(payload, dict):
        return None, TopicStandalonePixiBindingResolutionFailure(
            kind="pixi-tooling",
            message="Pixi returned JSON that was not an object while resolving the binding target.",
            target=target,
            target_path=target_path,
            target_kind=target_kind,
            command=command,
        )

    project_info = payload.get("project_info")
    if project_info is None:
        return None, TopicStandalonePixiBindingResolutionFailure(
            kind="unresolvable-target",
            message="Pixi did not resolve a workspace manifest for the binding target.",
            target=target,
            target_path=target_path,
            target_kind=target_kind,
            command=command,
        )
    if not isinstance(project_info, dict):
        return None, _missing_required_field_failure(
            target,
            target_path,
            target_kind,
            command,
            "project_info",
        )
    manifest_path_value = project_info.get("manifest_path")
    if not isinstance(manifest_path_value, str) or not manifest_path_value:
        return None, _missing_required_field_failure(
            target,
            target_path,
            target_kind,
            command,
            "project_info.manifest_path",
        )

    environment_info, missing_environment_fields = _selected_environment_info(
        payload.get("environments_info"),
        target.pixi_environment,
    )
    if missing_environment_fields:
        return None, _missing_required_field_failure(
            target,
            target_path,
            target_kind,
            command,
            ", ".join(missing_environment_fields),
        )
    if environment_info is None:
        return None, TopicStandalonePixiBindingResolutionFailure(
            kind="unresolvable-target",
            message=f"Pixi did not report selected environment {target.pixi_environment!r} for the binding target.",
            target=target,
            target_path=target_path,
            target_kind=target_kind,
            command=command,
            resolved_manifest_path=canonicalize(Path(manifest_path_value)),
        )

    prefix_value = environment_info.get("prefix")
    if not isinstance(prefix_value, str) or not prefix_value:
        return None, _missing_required_field_failure(
            target,
            target_path,
            target_kind,
            command,
            f"environments_info[{target.pixi_environment}].prefix",
        )

    resolved_manifest_path = canonicalize(Path(manifest_path_value))
    environment_prefix = canonicalize(Path(prefix_value))
    topic_workspace_path = canonicalize(context.topic_workspace_path)
    topic_workspace_pixi_dir = topic_workspace_path / ".pixi"
    if not is_within(resolved_manifest_path, topic_workspace_path):
        return None, TopicStandalonePixiBindingResolutionFailure(
            kind="confinement",
            message="Pixi resolved a manifest outside the registered Topic Workspace.",
            target=target,
            target_path=target_path,
            target_kind=target_kind,
            command=command,
            resolved_manifest_path=resolved_manifest_path,
            environment_prefix=environment_prefix,
        )
    if not is_within(environment_prefix, topic_workspace_pixi_dir):
        return None, TopicStandalonePixiBindingResolutionFailure(
            kind="confinement",
            message="Pixi resolved an environment prefix outside the registered Topic Workspace .pixi directory.",
            target=target,
            target_path=target_path,
            target_kind=target_kind,
            command=command,
            resolved_manifest_path=resolved_manifest_path,
            environment_prefix=environment_prefix,
        )

    return ResolvedTopicStandalonePixiBinding(
        research_topic_id=target.research_topic_id,
        source=target.source,
        target_path=target_path,
        target_path_input=target.target_path_input,
        target_kind=target_kind,
        resolved_manifest_path=resolved_manifest_path,
        pixi_environment=target.pixi_environment,
        environment_prefix=environment_prefix,
    ), None


def _selected_environment_info(
    environments_info: object,
    selected_environment: str,
) -> tuple[dict[str, Any] | None, list[str]]:
    if not isinstance(environments_info, list):
        return None, ["environments_info"]
    for item in environments_info:
        if not isinstance(item, dict):
            continue
        if item.get("name") == selected_environment:
            return item, []
    return None, []


def _missing_required_field_failure(
    target: TopicStandalonePixiBindingTarget,
    target_path: Path,
    target_kind: TopicStandalonePixiTargetKind,
    command: list[str],
    field: str,
) -> TopicStandalonePixiBindingResolutionFailure:
    return TopicStandalonePixiBindingResolutionFailure(
        kind="pixi-tooling",
        message=f"Pixi JSON omitted required binding-resolution field: {field}.",
        target=target,
        target_path=target_path,
        target_kind=target_kind,
        command=command,
    )


def _target_kind(path: Path) -> TopicStandalonePixiTargetKind:
    if path.is_file():
        return "file"
    if path.is_dir():
        return "directory"
    if path.exists():
        return "unknown"
    return "missing"


def _run_command(command: list[str]) -> tuple[subprocess.CompletedProcess[str] | None, str | None]:
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=15, check=False)
    except OSError as exc:
        return None, str(exc)
    except subprocess.TimeoutExpired:
        return None, "command timed out"
    return result, None


def _command_failure_summary(result: subprocess.CompletedProcess[str]) -> str:
    output = _first_output_line(result.stderr) or _first_output_line(result.stdout)
    if output is None:
        return f"exit status {result.returncode}"
    return f"exit status {result.returncode}: {output}"


def _first_output_line(value: str | None) -> str | None:
    if value is None:
        return None
    for line in value.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return None
