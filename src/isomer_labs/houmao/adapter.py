"""CLI-backed Houmao Execution Adapter."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from pathlib import Path
import json
import os
import shlex
import shutil
import subprocess
from time import monotonic
from typing import Any, Iterable, Literal, Mapping, Protocol

from isomer_labs.core.diagnostics import Diagnostic, has_errors
from isomer_labs.houmao.manifests import (
    HOUMAO_ADAPTER_ID,
    AgentBinding,
    ManifestKind,
    MaterialFileRef,
    ReconciliationResult,
    adapter_manifest_path_plan_surface,
    build_adapter_link_manifest,
    build_adapter_runtime_manifest,
    build_launch_material_manifest,
    canonical_json_digest,
    file_digest,
    manifest_paths,
    reconcile_houmao_manifests,
    redact_payload,
    write_json_manifest,
)
from isomer_labs.models import EffectiveTopicContext, TopicAgentTeamProfile
from isomer_labs.runtime.records import (
    AdapterHandoffDispatchRecord,
    AdapterCommandRunRecord,
    HandoffNormalizationRecord,
    HandoffRecord,
    AdapterInspectionSnapshotRecord,
    AdapterLaunchAttemptRecord,
    AdapterManifestRefRecord,
    AdapterMaterializationRecord,
    AdapterPayloadRefRecord,
    AdapterStopOutcomeRecord,
    RuntimeLifecycleRecord,
    SignalObservationRecord,
    utc_timestamp,
)


HOUMAO_EXECUTION_ADAPTER_REF = "execution-adapter:houmao"
DEFAULT_HOUMAO_COMMAND = "houmao-mgr"
HOUMAO_COMMAND_ENV = "ISOMER_HOUMAO_COMMAND"
HOUMAO_CHECKOUT_ENV = "ISOMER_HOUMAO_CHECKOUT"
DEFAULT_COMMAND_TIMEOUT_SECONDS = 30


@dataclass(frozen=True)
class HoumaoCommandSpec:
    """One Houmao CLI command before command-prefix resolution."""

    operation_kind: str
    args: list[str]
    expects_json: bool = True

    def to_json(self) -> dict[str, object]:
        return {
            "operation_kind": self.operation_kind,
            "args": self.args,
            "expects_json": self.expects_json,
        }


@dataclass(frozen=True)
class HoumaoCommandCatalog:
    """Centralized command catalog for the supported Houmao CLI surface."""

    def version(self) -> HoumaoCommandSpec:
        return HoumaoCommandSpec("preflight_version", ["--version"], expects_json=False)

    def system_skills_list(self) -> HoumaoCommandSpec:
        return HoumaoCommandSpec("preflight_system_skills", ["--print-json", "system-skills", "list"])

    def project_init(self, project_dir: Path) -> HoumaoCommandSpec:
        return HoumaoCommandSpec("project_init", ["--print-json", "project", "--project-dir", str(project_dir), "init"])

    def project_status(self, project_dir: Path) -> HoumaoCommandSpec:
        return HoumaoCommandSpec("preflight_project_status", ["--print-json", "project", "--project-dir", str(project_dir), "status"])

    def specialist_create(self, project_dir: Path, *, name: str, system_prompt_file: Path, tool: str) -> HoumaoCommandSpec:
        return HoumaoCommandSpec(
            "specialist_create",
            [
                "--print-json",
                "project",
                "--project-dir",
                str(project_dir),
                "specialist",
                "create",
                "--name",
                name,
                "--tool",
                tool,
                "--system-prompt-file",
                str(system_prompt_file),
                "--yes",
            ],
        )

    def profile_create(self, project_dir: Path, *, name: str, specialist: str, agent_name: str, workdir: Path) -> HoumaoCommandSpec:
        return HoumaoCommandSpec(
            "profile_create",
            [
                "--print-json",
                "project",
                "--project-dir",
                str(project_dir),
                "profile",
                "create",
                "--name",
                name,
                "--specialist",
                specialist,
                "--agent-name",
                agent_name,
                "--workdir",
                str(workdir),
                "--headless",
                "--yes",
            ],
        )

    def agent_launch(self, project_dir: Path, *, profile: str, name: str, workdir: Path) -> HoumaoCommandSpec:
        return HoumaoCommandSpec(
            "agent_launch",
            [
                "--print-json",
                "project",
                "--project-dir",
                str(project_dir),
                "agents",
                "launch",
                "--profile",
                profile,
                "--name",
                name,
                "--workdir",
                str(workdir),
                "--headless",
            ],
        )

    def agents_list(self, project_dir: Path) -> HoumaoCommandSpec:
        return HoumaoCommandSpec("agent_inspect_list", ["--print-json", "project", "--project-dir", str(project_dir), "agents", "list"])

    def agent_get(self, project_dir: Path, *, name: str) -> HoumaoCommandSpec:
        return HoumaoCommandSpec("agent_inspect_get", ["--print-json", "project", "--project-dir", str(project_dir), "agents", "get", "--name", name])

    def agent_stop(self, project_dir: Path, *, name: str) -> HoumaoCommandSpec:
        return HoumaoCommandSpec("agent_stop", ["--print-json", "project", "--project-dir", str(project_dir), "agents", "stop", "--name", name])

    def handoff_dispatch(self, project_dir: Path, *, source: str, target: str, message_file: Path, handoff_id: str) -> HoumaoCommandSpec:
        return HoumaoCommandSpec(
            "manual_handoff",
            [
                "--print-json",
                "project",
                "--project-dir",
                str(project_dir),
                "mail",
                "send",
                "--from",
                source,
                "--to",
                target,
                "--handoff",
                handoff_id,
                "--message-file",
                str(message_file),
            ],
        )

    def handoff_observe(self, project_dir: Path, *, handoff_id: str, source: str) -> HoumaoCommandSpec:
        command = "gateway" if source == "gateway" else "mail"
        action = "events" if source == "gateway" else "read"
        return HoumaoCommandSpec(
            "manual_handoff_observe",
            [
                "--print-json",
                "project",
                "--project-dir",
                str(project_dir),
                command,
                action,
                "--handoff",
                handoff_id,
            ],
        )

    def global_agents_list(self) -> HoumaoCommandSpec:
        return HoumaoCommandSpec("preflight_global_agents", ["--print-json", "agents", "global", "list", "--state", "all"])


@dataclass(frozen=True)
class HoumaoCommandResolution:
    command_prefix: list[str]
    cwd: Path | None
    source: str
    diagnostics: list[Diagnostic] = field(default_factory=list)

    @property
    def available(self) -> bool:
        return bool(self.command_prefix) and not has_errors(self.diagnostics)

    def to_json(self) -> dict[str, object]:
        return {
            "available": self.available,
            "command_prefix": self.command_prefix,
            "cwd": str(self.cwd) if self.cwd is not None else None,
            "source": self.source,
            "diagnostics": [diagnostic.to_json() for diagnostic in self.diagnostics],
        }


@dataclass(frozen=True)
class HoumaoCommandResult:
    operation_kind: str
    argv: list[str]
    cwd: str | None
    env_hints: dict[str, str]
    returncode: int | None
    stdout: str
    stderr: str
    parsed_json: object | None
    started_at: str
    finished_at: str
    duration_seconds: float
    timed_out: bool
    diagnostics: list[Diagnostic] = field(default_factory=list)

    @property
    def succeeded(self) -> bool:
        return self.returncode == 0 and not self.timed_out and not has_errors(self.diagnostics)

    @property
    def status(self) -> str:
        if self.timed_out:
            return "timed_out"
        if any(diagnostic.code == "ISO071" for diagnostic in self.diagnostics):
            return "invalid_json"
        if self.returncode == 0 and not has_errors(self.diagnostics):
            return "succeeded"
        return "failed"

    def sanitized_output(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "stdout": _parse_json_or_text(self.stdout),
            "stderr": self.stderr.strip(),
            "parsed_json": self.parsed_json,
        }
        redacted = redact_payload(payload)
        return redacted if isinstance(redacted, dict) else payload

    def to_json(self) -> dict[str, object]:
        return {
            "operation_kind": self.operation_kind,
            "argv": self.argv,
            "cwd": self.cwd,
            "env_hints": self.env_hints,
            "returncode": self.returncode,
            "status": self.status,
            "timed_out": self.timed_out,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "duration_seconds": self.duration_seconds,
            "output": self.sanitized_output(),
            "diagnostics": [diagnostic.to_json() for diagnostic in self.diagnostics],
        }


class HoumaoRunnerProtocol(Protocol):
    def run(
        self,
        spec: HoumaoCommandSpec,
        *,
        cwd: Path | None = None,
        env: Mapping[str, str] | None = None,
        timeout_seconds: int = DEFAULT_COMMAND_TIMEOUT_SECONDS,
    ) -> HoumaoCommandResult:
        ...


class HoumaoCommandRunner:
    """Bounded subprocess runner for Houmao commands."""

    def __init__(self, project_root: Path, *, env: Mapping[str, str] | None = None) -> None:
        self.project_root = project_root
        self.env = dict(env or os.environ)
        self.resolution = resolve_houmao_command(project_root, self.env)

    def run(
        self,
        spec: HoumaoCommandSpec,
        *,
        cwd: Path | None = None,
        env: Mapping[str, str] | None = None,
        timeout_seconds: int = DEFAULT_COMMAND_TIMEOUT_SECONDS,
    ) -> HoumaoCommandResult:
        started_at = utc_timestamp()
        start = monotonic()
        command_cwd = cwd or self.resolution.cwd or self.project_root
        argv = [*self.resolution.command_prefix, *spec.args]
        diagnostics = list(self.resolution.diagnostics)
        if not self.resolution.command_prefix:
            diagnostics.append(_adapter_diagnostic("ISO070", "error", "Houmao command could not be resolved."))
            finished_at = utc_timestamp()
            return HoumaoCommandResult(
                operation_kind=spec.operation_kind,
                argv=argv,
                cwd=str(command_cwd),
                env_hints={},
                returncode=None,
                stdout="",
                stderr="",
                parsed_json=None,
                started_at=started_at,
                finished_at=finished_at,
                duration_seconds=0.0,
                timed_out=False,
                diagnostics=diagnostics,
            )
        run_env = _bounded_env(env or self.env)
        try:
            completed = subprocess.run(
                argv,
                check=False,
                capture_output=True,
                text=True,
                cwd=str(command_cwd),
                env=run_env,
                timeout=timeout_seconds,
            )
        except subprocess.TimeoutExpired as exc:
            finished_at = utc_timestamp()
            diagnostics.append(_adapter_diagnostic("ISO073", "error", f"Houmao command timed out after {timeout_seconds} second(s)."))
            return HoumaoCommandResult(
                operation_kind=spec.operation_kind,
                argv=argv,
                cwd=str(command_cwd),
                env_hints=_env_hints(run_env),
                returncode=None,
                stdout=_string_output(exc.stdout),
                stderr=_string_output(exc.stderr),
                parsed_json=None,
                started_at=started_at,
                finished_at=finished_at,
                duration_seconds=round(monotonic() - start, 6),
                timed_out=True,
                diagnostics=diagnostics,
            )
        except OSError as exc:
            finished_at = utc_timestamp()
            diagnostics.append(_adapter_diagnostic("ISO070", "error", f"Houmao command failed before execution: {exc}."))
            return HoumaoCommandResult(
                operation_kind=spec.operation_kind,
                argv=argv,
                cwd=str(command_cwd),
                env_hints=_env_hints(run_env),
                returncode=None,
                stdout="",
                stderr=str(exc),
                parsed_json=None,
                started_at=started_at,
                finished_at=finished_at,
                duration_seconds=round(monotonic() - start, 6),
                timed_out=False,
                diagnostics=diagnostics,
            )

        parsed_json = _parse_json_or_none(completed.stdout)
        if spec.expects_json and completed.returncode == 0 and parsed_json is None:
            diagnostics.append(_adapter_diagnostic("ISO071", "error", "Houmao command did not emit valid JSON for --print-json."))
        if completed.returncode != 0:
            diagnostics.append(_adapter_diagnostic("ISO072", "error", "Houmao command returned a non-zero status."))
        return HoumaoCommandResult(
            operation_kind=spec.operation_kind,
            argv=argv,
            cwd=str(command_cwd),
            env_hints=_env_hints(run_env),
            returncode=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
            parsed_json=parsed_json,
            started_at=started_at,
            finished_at=utc_timestamp(),
            duration_seconds=round(monotonic() - start, 6),
            timed_out=False,
            diagnostics=diagnostics,
        )


@dataclass(frozen=True)
class HoumaoPreflightResult:
    available: bool
    resolution: HoumaoCommandResolution
    command_results: list[HoumaoCommandResult]
    diagnostics: list[Diagnostic]

    @property
    def ok(self) -> bool:
        return self.available and not has_errors(self.diagnostics)

    def to_json(self) -> dict[str, object]:
        return {
            "ok": self.ok,
            "available": self.available,
            "resolution": self.resolution.to_json(),
            "command_results": [result.to_json() for result in self.command_results],
            "diagnostics": [diagnostic.to_json() for diagnostic in self.diagnostics],
        }


@dataclass(frozen=True)
class HoumaoAdapterPaths:
    adapter_root: Path
    launch_material_root: Path
    command_payloads: Path
    launch_logs: Path
    inspection_snapshots: Path
    stop_outcomes: Path
    handoff_payloads: Path
    handoff_observations: Path
    handoff_normalizations: Path
    houmao_project_dir: Path
    generated_profile_root: Path
    agent_material_roots: dict[str, Path]

    def to_json(self) -> dict[str, object]:
        return {
            "adapter_root": str(self.adapter_root),
            "launch_material_root": str(self.launch_material_root),
            "command_payloads": str(self.command_payloads),
            "launch_logs": str(self.launch_logs),
            "inspection_snapshots": str(self.inspection_snapshots),
            "stop_outcomes": str(self.stop_outcomes),
            "handoff_payloads": str(self.handoff_payloads),
            "handoff_observations": str(self.handoff_observations),
            "handoff_normalizations": str(self.handoff_normalizations),
            "houmao_project_dir": str(self.houmao_project_dir),
            "generated_profile_root": str(self.generated_profile_root),
            "agent_material_roots": {key: str(value) for key, value in self.agent_material_roots.items()},
        }


@dataclass(frozen=True)
class HoumaoMaterializedAgent:
    agent_instance_id: str
    agent_role_id: str
    agent_name: str
    houmao_profile: str
    houmao_agent_name: str
    workdir: Path
    system_prompt_path: Path
    specialist_payload_path: Path
    profile_payload_path: Path
    launch_payload_path: Path

    def to_json(self) -> dict[str, object]:
        return {
            "agent_instance_id": self.agent_instance_id,
            "agent_role_id": self.agent_role_id,
            "agent_name": self.agent_name,
            "houmao_profile": self.houmao_profile,
            "houmao_agent_name": self.houmao_agent_name,
            "workdir": str(self.workdir),
            "system_prompt_path": str(self.system_prompt_path),
            "specialist_payload_path": str(self.specialist_payload_path),
            "profile_payload_path": str(self.profile_payload_path),
            "launch_payload_path": str(self.launch_payload_path),
        }


@dataclass(frozen=True)
class HoumaoMaterializationResult:
    status: str
    paths: HoumaoAdapterPaths
    agents: list[HoumaoMaterializedAgent]
    link_manifest: dict[str, object]
    launch_material_manifest: dict[str, object]
    link_manifest_path: Path
    launch_material_manifest_path: Path
    material_refs: list[MaterialFileRef]
    manifest_ref_ids: list[str]
    payload_ref_ids: list[str]
    path_plan_ids: list[str]
    materialization_record_id: str
    diagnostics: list[Diagnostic] = field(default_factory=list)

    def manual_guidance(self, catalog: HoumaoCommandCatalog | None = None) -> list[dict[str, object]]:
        command_catalog = catalog or HoumaoCommandCatalog()
        project_dir = self.paths.houmao_project_dir
        guidance: list[dict[str, object]] = [command_catalog.project_init(project_dir).to_json()]
        for agent in self.agents:
            guidance.append(
                command_catalog.specialist_create(
                    project_dir,
                    name=agent.houmao_profile,
                    system_prompt_file=agent.system_prompt_path,
                    tool="codex",
                ).to_json()
            )
            guidance.append(
                command_catalog.profile_create(
                    project_dir,
                    name=agent.houmao_profile,
                    specialist=agent.houmao_profile,
                    agent_name=agent.houmao_agent_name,
                    workdir=agent.workdir,
                ).to_json()
            )
            guidance.append(
                command_catalog.agent_launch(
                    project_dir,
                    profile=agent.houmao_profile,
                    name=agent.houmao_agent_name,
                    workdir=agent.workdir,
                ).to_json()
            )
        return guidance

    def to_json(self) -> dict[str, object]:
        return {
            "status": self.status,
            "paths": self.paths.to_json(),
            "agents": [agent.to_json() for agent in self.agents],
            "link_manifest_path": str(self.link_manifest_path),
            "launch_material_manifest_path": str(self.launch_material_manifest_path),
            "manifest_ref_ids": self.manifest_ref_ids,
            "payload_ref_ids": self.payload_ref_ids,
            "path_plan_ids": self.path_plan_ids,
            "materialization_record_id": self.materialization_record_id,
            "manual_guidance": self.manual_guidance(),
            "diagnostics": [diagnostic.to_json() for diagnostic in self.diagnostics],
        }


@dataclass(frozen=True)
class HoumaoLaunchResult:
    status: str
    preflight: HoumaoPreflightResult
    materialization: HoumaoMaterializationResult | None
    command_run_ids: list[str]
    payload_ref_ids: list[str]
    launch_attempt_id: str | None
    runtime_manifest_path: Path | None
    runtime_manifest: dict[str, object] | None
    reconciliation: ReconciliationResult | None
    diagnostics: list[Diagnostic]

    def to_json(self) -> dict[str, object]:
        return {
            "status": self.status,
            "preflight": self.preflight.to_json(),
            "materialization": self.materialization.to_json() if self.materialization is not None else None,
            "command_run_ids": self.command_run_ids,
            "payload_ref_ids": self.payload_ref_ids,
            "launch_attempt_id": self.launch_attempt_id,
            "runtime_manifest_path": str(self.runtime_manifest_path) if self.runtime_manifest_path is not None else None,
            "runtime_manifest": self.runtime_manifest,
            "reconciliation": self.reconciliation.to_json() if self.reconciliation is not None else None,
            "diagnostics": [diagnostic.to_json() for diagnostic in self.diagnostics],
        }


@dataclass(frozen=True)
class HoumaoInspectionResult:
    status: str
    command_run_ids: list[str]
    payload_ref_ids: list[str]
    snapshot_record_id: str | None
    live_state: dict[str, object]
    reconciliation: ReconciliationResult | None
    diagnostics: list[Diagnostic]

    def to_json(self) -> dict[str, object]:
        return {
            "status": self.status,
            "command_run_ids": self.command_run_ids,
            "payload_ref_ids": self.payload_ref_ids,
            "snapshot_record_id": self.snapshot_record_id,
            "live_state": self.live_state,
            "reconciliation": self.reconciliation.to_json() if self.reconciliation is not None else None,
            "diagnostics": [diagnostic.to_json() for diagnostic in self.diagnostics],
        }


@dataclass(frozen=True)
class HoumaoStopResult:
    status: str
    command_run_ids: list[str]
    payload_ref_ids: list[str]
    stop_outcome_id: str | None
    diagnostics: list[Diagnostic]

    def to_json(self) -> dict[str, object]:
        return {
            "status": self.status,
            "command_run_ids": self.command_run_ids,
            "payload_ref_ids": self.payload_ref_ids,
            "stop_outcome_id": self.stop_outcome_id,
            "diagnostics": [diagnostic.to_json() for diagnostic in self.diagnostics],
        }


@dataclass(frozen=True)
class HoumaoHandoffDispatchResult:
    status: str
    handoff_id: str | None
    run_id: str | None
    dispatch_record_id: str | None
    command_run_ids: list[str]
    payload_ref_ids: list[str]
    diagnostics: list[Diagnostic]

    def to_json(self) -> dict[str, object]:
        return {
            "status": self.status,
            "handoff_id": self.handoff_id,
            "run_id": self.run_id,
            "dispatch_record_id": self.dispatch_record_id,
            "command_run_ids": self.command_run_ids,
            "payload_ref_ids": self.payload_ref_ids,
            "diagnostics": [diagnostic.to_json() for diagnostic in self.diagnostics],
        }


@dataclass(frozen=True)
class HoumaoHandoffObservationResult:
    status: str
    handoff_id: str
    signal_observation_id: str | None
    command_run_ids: list[str]
    payload_ref_ids: list[str]
    completion_authority: bool
    diagnostics: list[Diagnostic]

    def to_json(self) -> dict[str, object]:
        return {
            "status": self.status,
            "handoff_id": self.handoff_id,
            "signal_observation_id": self.signal_observation_id,
            "command_run_ids": self.command_run_ids,
            "payload_ref_ids": self.payload_ref_ids,
            "completion_authority": self.completion_authority,
            "diagnostics": [diagnostic.to_json() for diagnostic in self.diagnostics],
        }


@dataclass(frozen=True)
class HoumaoHandoffNormalizationResult:
    status: str
    handoff_id: str
    normalization_record_id: str | None
    run_id: str | None
    output_artifact_refs: list[str]
    payload_ref_ids: list[str]
    diagnostics: list[Diagnostic]

    def to_json(self) -> dict[str, object]:
        return {
            "status": self.status,
            "handoff_id": self.handoff_id,
            "normalization_record_id": self.normalization_record_id,
            "run_id": self.run_id,
            "output_artifact_refs": self.output_artifact_refs,
            "payload_ref_ids": self.payload_ref_ids,
            "diagnostics": [diagnostic.to_json() for diagnostic in self.diagnostics],
        }


class HoumaoAdapterFacade:
    """High-level Houmao adapter facade used by CLI handlers."""

    def __init__(
        self,
        *,
        runner: HoumaoRunnerProtocol | None = None,
        catalog: HoumaoCommandCatalog | None = None,
        env: Mapping[str, str] | None = None,
    ) -> None:
        self.runner = runner
        self.catalog = catalog or HoumaoCommandCatalog()
        self.env = dict(env or os.environ)

    def preflight(
        self,
        *,
        context: EffectiveTopicContext,
        store: Any,
        agent_team_instance_id: str,
        houmao_project_dir: Path | None = None,
        run_probes: bool = True,
    ) -> HoumaoPreflightResult:
        runner = self._runner(context.project.root)
        diagnostics = list(runner.resolution.diagnostics) if isinstance(runner, HoumaoCommandRunner) else []
        results: list[HoumaoCommandResult] = []
        if isinstance(runner, HoumaoCommandRunner) and not runner.resolution.available:
            diagnostics.append(_adapter_diagnostic("ISO070", "error", "Houmao backend is unavailable; configure houmao-mgr or a local Houmao checkout."))
        readiness = store.latest_readiness()
        if readiness is None or readiness.status != "ready":
            diagnostics.append(_adapter_diagnostic("ISO043", "error", "Houmao adapter preflight requires ready Topic Environment Readiness.", field="readiness"))
        summary = store.get_agent_team_instance_summary(agent_team_instance_id)
        if summary is None:
            diagnostics.append(_adapter_diagnostic("ISO041", "error", f"Unknown Agent Team Instance: {agent_team_instance_id}.", field="agent_team_instance_id"))
        elif summary.agent_team_instance.topic_workspace_id != context.topic_workspace_id:
            diagnostics.append(_adapter_diagnostic("ISO041", "error", "Agent Team Instance belongs to another Topic Workspace.", field="agent_team_instance_id"))
        if run_probes and not has_errors(diagnostics):
            probe_specs = [self.catalog.version(), self.catalog.system_skills_list(), self.catalog.global_agents_list()]
            if houmao_project_dir is not None and (houmao_project_dir / ".houmao").exists():
                probe_specs.insert(2, self.catalog.project_status(houmao_project_dir))
            for spec in probe_specs:
                result = runner.run(spec, env=self.env)
                results.append(result)
                diagnostics.extend(result.diagnostics)
        available = not (isinstance(runner, HoumaoCommandRunner) and not runner.resolution.available)
        resolution = runner.resolution if isinstance(runner, HoumaoCommandRunner) else HoumaoCommandResolution(["<mocked-houmao-mgr>"], None, "mock")
        return HoumaoPreflightResult(
            available=available,
            resolution=resolution,
            command_results=results,
            diagnostics=diagnostics,
        )

    def materialize(
        self,
        *,
        context: EffectiveTopicContext,
        store: Any,
        summary: Any,
        profile: TopicAgentTeamProfile,
        houmao_project_dir: Path | None,
        actor_ref: str | None,
        source: str,
    ) -> HoumaoMaterializationResult:
        diagnostics: list[Diagnostic] = []
        diagnostics.extend(_launchable_profile_diagnostics(profile))
        agent_team_instance_id = summary.agent_team_instance.id
        paths = build_houmao_adapter_paths(
            context.topic_workspace_path,
            agent_team_instance_id,
            [record.id for record in summary.agent_instances],
            houmao_project_dir=houmao_project_dir,
        )
        path_plan_ids = self._record_path_plans(context, store, agent_team_instance_id, paths, diagnostics)
        if has_errors(diagnostics):
            return _failed_materialization(paths, diagnostics)
        _ensure_adapter_directories(paths)

        operator_provenance = _bounded_operator_provenance(summary, profile, actor_ref)
        profile_by_role = {binding.role_id: binding for binding in profile.role_bindings}
        workspace_by_agent = {workspace.agent_instance_id: workspace for workspace in summary.agent_workspaces}
        path_plan_by_id = {plan.id: plan for plan in store.list_path_plans()}
        agents: list[HoumaoMaterializedAgent] = []
        material_refs: list[MaterialFileRef] = []
        for agent in summary.agent_instances:
            role_binding = profile_by_role.get(agent.agent_role_id)
            workspace = workspace_by_agent.get(agent.id)
            if workspace is None or workspace.agent_name is None:
                diagnostics.append(
                    _adapter_diagnostic(
                        "ISO041",
                        "error",
                        "Houmao launch requires a recorded topic-local Agent Workspace plan with agent_name.",
                        field=f"agent_instances.{agent.id}.agent_name",
                    )
                )
                continue
            plan = path_plan_by_id.get(workspace.path_plan_id)
            if plan is None:
                diagnostics.append(
                    _adapter_diagnostic(
                        "ISO041",
                        "error",
                        "Houmao launch requires a persisted Agent Workspace path plan.",
                        field=f"agent_instances.{agent.id}.agent_workspace",
                    )
                )
                continue
            workdir = Path(plan.path)
            agent_root = paths.agent_material_roots[agent.id]
            agent_root.mkdir(parents=True, exist_ok=True)
            houmao_profile = _houmao_profile_name(agent_team_instance_id, agent.agent_role_id)
            houmao_agent_name = workspace.agent_name
            system_prompt_path = agent_root / "system-prompt.md"
            specialist_payload_path = agent_root / "specialist.json"
            profile_payload_path = agent_root / "profile.json"
            launch_payload_path = agent_root / "launch.json"
            system_prompt_path.write_text(_system_prompt(profile, agent.agent_role_id, role_binding), encoding="utf-8")
            _write_json_file(
                specialist_payload_path,
                {
                    "kind": "houmao_specialist_input",
                    "agent_instance_id": agent.id,
                    "agent_role_id": agent.agent_role_id,
                    "name": houmao_profile,
                    "tool": "codex",
                    "system_prompt_file": str(system_prompt_path),
                    "operator_provenance": operator_provenance,
                },
            )
            _write_json_file(
                profile_payload_path,
                {
                    "kind": "houmao_profile_input",
                    "agent_instance_id": agent.id,
                    "agent_role_id": agent.agent_role_id,
                    "name": houmao_profile,
                    "specialist": houmao_profile,
                    "agent_name": houmao_agent_name,
                    "workdir": str(workdir),
                    "headless": True,
                    "operator_provenance": operator_provenance,
                },
            )
            _write_json_file(
                launch_payload_path,
                {
                    "kind": "houmao_launch_input",
                    "agent_instance_id": agent.id,
                    "agent_role_id": agent.agent_role_id,
                    "profile": houmao_profile,
                    "agent_name": houmao_agent_name,
                    "workdir": str(workdir),
                    "operator_provenance": operator_provenance,
                },
            )
            agents.append(
                HoumaoMaterializedAgent(
                    agent_instance_id=agent.id,
                    agent_role_id=agent.agent_role_id,
                    agent_name=workspace.agent_name,
                    houmao_profile=houmao_profile,
                    houmao_agent_name=houmao_agent_name,
                    workdir=workdir,
                    system_prompt_path=system_prompt_path,
                    specialist_payload_path=specialist_payload_path,
                    profile_payload_path=profile_payload_path,
                    launch_payload_path=launch_payload_path,
                )
            )
            for path, kind in (
                (system_prompt_path, "system_prompt"),
                (specialist_payload_path, "specialist_payload"),
                (profile_payload_path, "profile_payload"),
                (launch_payload_path, "launch_payload"),
            ):
                material_refs.append(
                    MaterialFileRef(
                        path=str(path.resolve(strict=False)),
                        digest=file_digest(path),
                        source="isomer_generated",
                        editable_policy="user_editable",
                        agent_instance_id=agent.id,
                        kind=kind,
                    )
                )

        if has_errors(diagnostics):
            return _failed_materialization(paths, diagnostics)

        link_manifest = build_adapter_link_manifest(
            project_root=context.project.root,
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            topic_workspace_path=context.topic_workspace_path,
            agent_team_instance_id=agent_team_instance_id,
            topic_agent_team_profile_id=summary.agent_team_instance.topic_agent_team_profile_id,
            domain_agent_team_template_id=summary.agent_team_instance.domain_agent_team_template_id,
            agent_bindings=[
                AgentBinding(
                    agent_instance_id=agent.agent_instance_id,
                    agent_role_id=agent.agent_role_id,
                    houmao_profile=agent.houmao_profile,
                    houmao_agent_name=agent.houmao_agent_name,
                    mapping_confidence="manual",
                )
                for agent in agents
            ],
            houmao_project_dir=paths.houmao_project_dir,
            actor_ref=actor_ref,
            operator_provenance=operator_provenance,
        )
        launch_material_manifest = build_launch_material_manifest(
            link_manifest=link_manifest,
            material_files=material_refs,
            source=source,
        )
        link_digest = write_json_manifest(paths.adapter_root / "adapter-link.json", link_manifest, expected_kind=ManifestKind.ADAPTER_LINK.value)
        launch_digest = write_json_manifest(
            paths.adapter_root / "launch-material-manifest.json",
            launch_material_manifest,
            expected_kind=ManifestKind.LAUNCH_MATERIAL.value,
        )
        payload_ref_ids = self._record_material_payload_refs(
            context,
            store,
            summary,
            material_refs,
            path_plan_by_surface={plan.surface: plan.id for plan in store.list_path_plans()},
        )
        manifest_ref_ids = self._record_manifest_refs(
            context,
            store,
            summary,
            [
                (ManifestKind.ADAPTER_LINK.value, paths.adapter_root / "adapter-link.json", link_digest, "houmao_materialization"),
                (ManifestKind.LAUNCH_MATERIAL.value, paths.adapter_root / "launch-material-manifest.json", launch_digest, "houmao_materialization"),
            ],
        )
        timestamp = utc_timestamp()
        materialization_record_id = f"adapter-materialization-{_slug(agent_team_instance_id)}-{_slug(source)}-{_timestamp_slug(timestamp)}"
        store.record_adapter_materialization(
            AdapterMaterializationRecord(
                id=materialization_record_id,
                research_topic_id=context.research_topic.id,
                topic_workspace_id=context.topic_workspace_id,
                agent_team_instance_id=agent_team_instance_id,
                adapter_id=HOUMAO_ADAPTER_ID,
                status="prepared",
                material_ref_ids=payload_ref_ids,
                manifest_ref_ids=manifest_ref_ids,
                path_plan_ids=path_plan_ids,
                diagnostics=[],
                created_at=timestamp,
                updated_at=timestamp,
                actor_ref=actor_ref,
                provenance_refs=[
                    f"provenance:houmao-materialization:{agent_team_instance_id}:{timestamp}",
                    *_operator_provenance_ref_list(operator_provenance),
                ],
            )
        )
        return HoumaoMaterializationResult(
            status="prepared",
            paths=paths,
            agents=agents,
            link_manifest=link_manifest,
            launch_material_manifest=launch_material_manifest,
            link_manifest_path=paths.adapter_root / "adapter-link.json",
            launch_material_manifest_path=paths.adapter_root / "launch-material-manifest.json",
            material_refs=material_refs,
            manifest_ref_ids=manifest_ref_ids,
            payload_ref_ids=payload_ref_ids,
            path_plan_ids=path_plan_ids,
            materialization_record_id=materialization_record_id,
            diagnostics=diagnostics,
        )

    def quick_launch(
        self,
        *,
        context: EffectiveTopicContext,
        store: Any,
        summary: Any,
        profile: TopicAgentTeamProfile,
        houmao_project_dir: Path | None,
        actor_ref: str | None,
    ) -> HoumaoLaunchResult:
        materialization = self.materialize(
            context=context,
            store=store,
            summary=summary,
            profile=profile,
            houmao_project_dir=houmao_project_dir,
            actor_ref=actor_ref,
            source="isomer_quick_launch",
        )
        preflight = self.preflight(
            context=context,
            store=store,
            agent_team_instance_id=summary.agent_team_instance.id,
            houmao_project_dir=materialization.paths.houmao_project_dir,
            run_probes=True,
        )
        diagnostics = [*materialization.diagnostics, *preflight.diagnostics]
        if has_errors(diagnostics):
            return HoumaoLaunchResult(
                status="failed",
                preflight=preflight,
                materialization=materialization,
                command_run_ids=[],
                payload_ref_ids=[],
                launch_attempt_id=None,
                runtime_manifest_path=None,
                runtime_manifest=None,
                reconciliation=None,
                diagnostics=diagnostics,
            )
        runner = self._runner(context.project.root)
        launch_started = utc_timestamp()
        launch_attempt_id = f"adapter-launch-{_slug(summary.agent_team_instance.id)}-{_timestamp_slug(launch_started)}"
        command_run_ids: list[str] = []
        payload_ref_ids: list[str] = []
        adapter_refs: list[dict[str, object]] = []
        operator_provenance = _bounded_operator_provenance(summary, profile, actor_ref)
        command_specs = [self.catalog.project_init(materialization.paths.houmao_project_dir)]
        for agent in materialization.agents:
            command_specs.extend(
                [
                    self.catalog.specialist_create(
                        materialization.paths.houmao_project_dir,
                        name=agent.houmao_profile,
                        system_prompt_file=agent.system_prompt_path,
                        tool="codex",
                    ),
                    self.catalog.profile_create(
                        materialization.paths.houmao_project_dir,
                        name=agent.houmao_profile,
                        specialist=agent.houmao_profile,
                        agent_name=agent.houmao_agent_name,
                        workdir=agent.workdir,
                    ),
                    self.catalog.agent_launch(
                        materialization.paths.houmao_project_dir,
                        profile=agent.houmao_profile,
                        name=agent.houmao_agent_name,
                        workdir=agent.workdir,
                    ),
                ]
            )
        agent_by_launch_name = {agent.houmao_agent_name: agent for agent in materialization.agents}
        for spec in command_specs:
            result = runner.run(spec, env=self.env)
            agent_for_result = _agent_for_command(spec, agent_by_launch_name)
            command_record_id, payload_ref_id = self._record_command_result(
                context,
                store,
                summary.agent_team_instance.id,
                agent_for_result.agent_instance_id if agent_for_result is not None else None,
                result,
                materialization.paths.command_payloads,
                actor_ref=actor_ref,
                operator_provenance=operator_provenance,
            )
            command_run_ids.append(command_record_id)
            payload_ref_ids.append(payload_ref_id)
            diagnostics.extend(result.diagnostics)
            if spec.operation_kind == "agent_launch" and result.succeeded and agent_for_result is not None:
                adapter_refs.append(
                    {
                        "agent_instance_id": agent_for_result.agent_instance_id,
                        "houmao_agent_name": agent_for_result.houmao_agent_name,
                        "houmao_profile": agent_for_result.houmao_profile,
                        "launch_command_run_id": command_record_id,
                        "observed": _agent_observation_from_result(result),
                    }
                )
            if not result.succeeded:
                break
        launched_count = len(adapter_refs)
        if has_errors(diagnostics):
            launch_status = "partial" if launched_count else "failed"
        else:
            launch_status = "launched"
        launch_finished = utc_timestamp()
        live_state = {
            "available": True,
            "source_mode": "isomer_quick_launch",
            "agents": [
                {
                    "agent_name": ref["houmao_agent_name"],
                    "profile": ref["houmao_profile"],
                    "agent_instance_id": ref["agent_instance_id"],
                    "launch_command_run_id": ref["launch_command_run_id"],
                }
                for ref in adapter_refs
            ],
        }
        reconciliation = reconcile_houmao_manifests(
            link_manifest=materialization.link_manifest,
            launch_material_manifest=materialization.launch_material_manifest,
            runtime_manifest={"source_mode": "isomer_quick_launch"},
            live_state=live_state,
            material_base_dir=context.topic_workspace_path,
        )
        diagnostics.extend(reconciliation.diagnostics)
        runtime_manifest = build_adapter_runtime_manifest(
            link_manifest=materialization.link_manifest,
            result=reconciliation,
            source_mode="isomer_quick_launch",
        )
        runtime_manifest_path = materialization.paths.adapter_root / "adapter-runtime-manifest.json"
        runtime_digest = write_json_manifest(runtime_manifest_path, runtime_manifest, expected_kind=ManifestKind.ADAPTER_RUNTIME.value)
        manifest_ref_ids = self._record_manifest_refs(
            context,
            store,
            summary,
            [(ManifestKind.ADAPTER_RUNTIME.value, runtime_manifest_path, runtime_digest, "houmao_quick_launch")],
        )
        store.record_adapter_launch_attempt(
            AdapterLaunchAttemptRecord(
                id=launch_attempt_id,
                research_topic_id=context.research_topic.id,
                topic_workspace_id=context.topic_workspace_id,
                agent_team_instance_id=summary.agent_team_instance.id,
                adapter_id=HOUMAO_ADAPTER_ID,
                status=launch_status,
                agent_instance_ids=[agent.agent_instance_id for agent in materialization.agents],
                command_run_ids=command_run_ids,
                manifest_ref_ids=[*materialization.manifest_ref_ids, *manifest_ref_ids],
                payload_ref_ids=[*materialization.payload_ref_ids, *payload_ref_ids],
                adapter_refs=adapter_refs,
                diagnostics=[diagnostic.to_json() for diagnostic in diagnostics],
                started_at=launch_started,
                updated_at=launch_finished,
                finished_at=launch_finished,
                actor_ref=actor_ref,
                provenance_refs=[
                    f"provenance:houmao-launch:{summary.agent_team_instance.id}:{launch_started}",
                    *_operator_provenance_ref_list(operator_provenance),
                ],
            )
        )
        store.record_adapter_reconciliation(
            _adapter_reconciliation_record(
                context,
                summary.agent_team_instance.id,
                reconciliation,
                actor_ref,
                operator_provenance=operator_provenance,
            )
        )
        return HoumaoLaunchResult(
            status=launch_status,
            preflight=preflight,
            materialization=materialization,
            command_run_ids=command_run_ids,
            payload_ref_ids=payload_ref_ids,
            launch_attempt_id=launch_attempt_id,
            runtime_manifest_path=runtime_manifest_path,
            runtime_manifest=runtime_manifest,
            reconciliation=reconciliation,
            diagnostics=diagnostics,
        )

    def inspect_live(
        self,
        *,
        context: EffectiveTopicContext,
        store: Any,
        summary: Any,
        link_manifest: Mapping[str, object] | None,
        launch_material_manifest: Mapping[str, object] | None,
        runtime_manifest: Mapping[str, object] | None,
        actor_ref: str | None,
    ) -> HoumaoInspectionResult:
        diagnostics: list[Diagnostic] = []
        paths = build_houmao_adapter_paths(
            context.topic_workspace_path,
            summary.agent_team_instance.id,
            [record.id for record in summary.agent_instances],
            houmao_project_dir=_project_dir_from_link(link_manifest),
        )
        _ensure_adapter_directories(paths)
        runner = self._runner(context.project.root)
        results = [runner.run(self.catalog.agents_list(paths.houmao_project_dir), env=self.env)]
        for agent in _bindings_from_link(link_manifest):
            agent_name = agent.get("houmao_agent_name")
            if isinstance(agent_name, str):
                results.append(runner.run(self.catalog.agent_get(paths.houmao_project_dir, name=agent_name), env=self.env))
        command_run_ids: list[str] = []
        payload_ref_ids: list[str] = []
        operator_provenance = _bounded_summary_provenance(summary, actor_ref)
        for result in results:
            command_record_id, payload_ref_id = self._record_command_result(
                context,
                store,
                summary.agent_team_instance.id,
                None,
                result,
                paths.command_payloads,
                actor_ref=actor_ref,
                operator_provenance=operator_provenance,
            )
            command_run_ids.append(command_record_id)
            payload_ref_ids.append(payload_ref_id)
            diagnostics.extend(result.diagnostics)
        live_state = {
            "available": not has_errors(diagnostics),
            "commands": [result.to_json() for result in results],
            "agents": _agents_from_results(results),
        }
        reconciliation = reconcile_houmao_manifests(
            link_manifest=link_manifest,
            launch_material_manifest=launch_material_manifest,
            runtime_manifest=runtime_manifest,
            live_state=live_state,
            material_base_dir=context.topic_workspace_path,
        )
        diagnostics.extend(reconciliation.diagnostics)
        timestamp = utc_timestamp()
        snapshot_path = paths.inspection_snapshots / f"inspection-{_timestamp_slug(timestamp)}.json"
        snapshot_path.parent.mkdir(parents=True, exist_ok=True)
        _write_json_file(
            snapshot_path,
            {
                "live_state": live_state,
                "reconciliation": reconciliation.to_json(),
                "operator_provenance": operator_provenance,
            },
        )
        snapshot_ref_id = self._record_payload_ref(
            context,
            store,
            agent_team_instance_id=summary.agent_team_instance.id,
            agent_instance_id=None,
            payload_kind="inspection_snapshot",
            payload_path=snapshot_path,
            payload_digest=file_digest(snapshot_path),
            source="houmao_inspect_live",
            command_run_id=None,
            path_plan_id=None,
        )
        snapshot_record_id = f"adapter-inspection-{_slug(summary.agent_team_instance.id)}-{_timestamp_slug(timestamp)}"
        store.record_adapter_inspection_snapshot(
            AdapterInspectionSnapshotRecord(
                id=snapshot_record_id,
                research_topic_id=context.research_topic.id,
                topic_workspace_id=context.topic_workspace_id,
                agent_team_instance_id=summary.agent_team_instance.id,
                adapter_id=HOUMAO_ADAPTER_ID,
                status="failed" if has_errors(diagnostics) else "observed",
                command_run_ids=command_run_ids,
                manifest_ref_ids=[record.id for record in summary.adapter_manifest_refs],
                snapshot_payload_ref_id=snapshot_ref_id,
                live_observation_summary=live_state,
                diagnostics=[diagnostic.to_json() for diagnostic in diagnostics],
                inspected_at=timestamp,
                actor_ref=actor_ref,
                provenance_refs=[
                    f"provenance:houmao-inspection:{summary.agent_team_instance.id}:{timestamp}",
                    *_operator_provenance_ref_list(operator_provenance),
                ],
            )
        )
        store.record_adapter_reconciliation(
            _adapter_reconciliation_record(
                context,
                summary.agent_team_instance.id,
                reconciliation,
                actor_ref,
                operator_provenance=operator_provenance,
            )
        )
        return HoumaoInspectionResult(
            status="failed" if has_errors(diagnostics) else "observed",
            command_run_ids=command_run_ids,
            payload_ref_ids=[*payload_ref_ids, snapshot_ref_id],
            snapshot_record_id=snapshot_record_id,
            live_state=live_state,
            reconciliation=reconciliation,
            diagnostics=diagnostics,
        )

    def stop(
        self,
        *,
        context: EffectiveTopicContext,
        store: Any,
        summary: Any,
        link_manifest: Mapping[str, object] | None,
        actor_ref: str | None,
    ) -> HoumaoStopResult:
        diagnostics: list[Diagnostic] = []
        paths = build_houmao_adapter_paths(
            context.topic_workspace_path,
            summary.agent_team_instance.id,
            [record.id for record in summary.agent_instances],
            houmao_project_dir=_project_dir_from_link(link_manifest),
        )
        _ensure_adapter_directories(paths)
        targets = _bindings_from_link(link_manifest)
        if not targets:
            latest_launch = store.latest_adapter_launch_attempt(agent_team_instance_id=summary.agent_team_instance.id)
            if latest_launch is not None:
                targets = [
                    {
                        "agent_instance_id": ref.get("agent_instance_id"),
                        "houmao_agent_name": ref.get("houmao_agent_name"),
                    }
                    for ref in latest_launch.adapter_refs
                    if isinstance(ref, dict)
                ]
        if not targets:
            diagnostics.append(_adapter_diagnostic("ISO076", "warning", "No Houmao mapped agents are known for stop."))
        runner = self._runner(context.project.root)
        command_run_ids: list[str] = []
        payload_ref_ids: list[str] = []
        operator_provenance = _bounded_summary_provenance(summary, actor_ref)
        stopped = 0
        for target in targets:
            agent_name = target.get("houmao_agent_name")
            if not isinstance(agent_name, str):
                continue
            result = runner.run(self.catalog.agent_stop(paths.houmao_project_dir, name=agent_name), env=self.env)
            command_record_id, payload_ref_id = self._record_command_result(
                context,
                store,
                summary.agent_team_instance.id,
                str(target.get("agent_instance_id")) if target.get("agent_instance_id") else None,
                result,
                paths.command_payloads,
                actor_ref=actor_ref,
                operator_provenance=operator_provenance,
            )
            command_run_ids.append(command_record_id)
            payload_ref_ids.append(payload_ref_id)
            diagnostics.extend(result.diagnostics)
            if result.succeeded:
                stopped += 1
        if stopped == len(targets) and targets:
            status = "stopped"
        elif stopped:
            status = "partial"
        elif targets:
            status = "failed"
        else:
            status = "stale"
        timestamp = utc_timestamp()
        outcome_path = paths.stop_outcomes / f"stop-{_timestamp_slug(timestamp)}.json"
        _write_json_file(
            outcome_path,
            {
                "status": status,
                "targets": targets,
                "command_run_ids": command_run_ids,
                "operator_provenance": operator_provenance,
            },
        )
        outcome_ref_id = self._record_payload_ref(
            context,
            store,
            agent_team_instance_id=summary.agent_team_instance.id,
            agent_instance_id=None,
            payload_kind="stop_outcome",
            payload_path=outcome_path,
            payload_digest=file_digest(outcome_path),
            source="houmao_stop",
            command_run_id=None,
            path_plan_id=None,
        )
        stop_outcome_id = f"adapter-stop-{_slug(summary.agent_team_instance.id)}-{_timestamp_slug(timestamp)}"
        store.record_adapter_stop_outcome(
            AdapterStopOutcomeRecord(
                id=stop_outcome_id,
                research_topic_id=context.research_topic.id,
                topic_workspace_id=context.topic_workspace_id,
                agent_team_instance_id=summary.agent_team_instance.id,
                adapter_id=HOUMAO_ADAPTER_ID,
                status=status,
                target_agent_instance_ids=[str(target["agent_instance_id"]) for target in targets if target.get("agent_instance_id")],
                command_run_ids=command_run_ids,
                payload_ref_ids=[*payload_ref_ids, outcome_ref_id],
                remaining_live_refs=[],
                diagnostics=[diagnostic.to_json() for diagnostic in diagnostics],
                stopped_at=timestamp,
                actor_ref=actor_ref,
                provenance_refs=[
                    f"provenance:houmao-stop:{summary.agent_team_instance.id}:{timestamp}",
                    *_operator_provenance_ref_list(operator_provenance),
                ],
            )
        )
        return HoumaoStopResult(
            status=status,
            command_run_ids=command_run_ids,
            payload_ref_ids=[*payload_ref_ids, outcome_ref_id],
            stop_outcome_id=stop_outcome_id,
            diagnostics=diagnostics,
        )

    def dispatch_handoff(
        self,
        *,
        context: EffectiveTopicContext,
        store: Any,
        summary: Any,
        source_agent_instance_id: str,
        target_agent_instance_id: str,
        message: str,
        run_id: str | None,
        research_task_id: str | None,
        expected_output_refs: list[str],
        completion_watcher_contract_refs: list[str],
        actor_ref: str | None,
    ) -> HoumaoHandoffDispatchResult:
        diagnostics: list[Diagnostic] = []
        team_id = summary.agent_team_instance.id
        source_agent = _summary_agent(summary, source_agent_instance_id)
        target_agent = _summary_agent(summary, target_agent_instance_id)
        if source_agent is None:
            diagnostics.append(_adapter_diagnostic("ISO041", "error", f"Unknown source Agent Instance: {source_agent_instance_id}.", field="source_agent_instance_id"))
        if target_agent is None:
            diagnostics.append(_adapter_diagnostic("ISO041", "error", f"Unknown target Agent Instance: {target_agent_instance_id}.", field="target_agent_instance_id"))
        latest_reconciliation = store.latest_adapter_reconciliation_record(agent_team_instance_id=team_id)
        latest_launch = store.latest_adapter_launch_attempt(agent_team_instance_id=team_id)
        if latest_launch is None and (latest_reconciliation is None or latest_reconciliation.state not in {"adopted", "linked", "launched_by_isomer", "external_detected"}):
            diagnostics.append(_adapter_diagnostic("ISO077", "error", "Handoff dispatch requires a launched, adopted, or linked Houmao adapter context.", field="agent_team_instance_id"))
        preflight = self.preflight(
            context=context,
            store=store,
            agent_team_instance_id=team_id,
            houmao_project_dir=None,
            run_probes=False,
        )
        diagnostics.extend(preflight.diagnostics)
        if has_errors(diagnostics):
            return HoumaoHandoffDispatchResult(
                status="failed",
                handoff_id=None,
                run_id=run_id,
                dispatch_record_id=None,
                command_run_ids=[],
                payload_ref_ids=[],
                diagnostics=diagnostics,
            )

        timestamp = utc_timestamp()
        run_record = store.ensure_run_record(
            context=context,
            agent_team_instance_id=team_id,
            run_id=run_id,
            research_task_id=research_task_id,
            actor_ref=actor_ref,
        )
        handoff_id = f"handoff-{_slug(team_id)}-{_slug(run_record.id)}-{_slug(target_agent_instance_id)}"
        paths = build_houmao_adapter_paths(
            context.topic_workspace_path,
            team_id,
            [record.id for record in summary.agent_instances],
            houmao_project_dir=_latest_houmao_project_dir(summary),
        )
        self._record_path_plans(context, store, team_id, paths, diagnostics)
        if has_errors(diagnostics):
            return HoumaoHandoffDispatchResult(
                status="failed",
                handoff_id=None,
                run_id=run_record.id,
                dispatch_record_id=None,
                command_run_ids=[],
                payload_ref_ids=[],
                diagnostics=diagnostics,
            )
        _ensure_adapter_directories(paths)
        dispatch_payload_path = paths.handoff_payloads / f"{handoff_id}-dispatch.json"
        source_name = _houmao_name_for_agent(summary, source_agent_instance_id)
        target_name = _houmao_name_for_agent(summary, target_agent_instance_id)
        dispatch_payload = {
            "kind": "houmao_manual_handoff_dispatch",
            "handoff_id": handoff_id,
            "agent_team_instance_id": team_id,
            "source_agent_instance_id": source_agent_instance_id,
            "target_agent_instance_id": target_agent_instance_id,
            "source_houmao_agent_name": source_name,
            "target_houmao_agent_name": target_name,
            "run_id": run_record.id,
            "research_task_id": research_task_id,
            "expected_output_refs": expected_output_refs,
            "completion_watcher_contract_refs": completion_watcher_contract_refs,
            "message": message,
            "created_at": timestamp,
        }
        _write_json_file(dispatch_payload_path, dispatch_payload)
        dispatch_payload_ref = self._record_payload_ref(
            context,
            store,
            agent_team_instance_id=team_id,
            agent_instance_id=target_agent_instance_id,
            payload_kind="handoff_dispatch_payload",
            payload_path=dispatch_payload_path,
            payload_digest=file_digest(dispatch_payload_path),
            source="isomer_handoff_dispatch",
            command_run_id=None,
            path_plan_id=_path_plan_id_by_surface(store, context.topic_workspace_id, adapter_handoff_payload_surface(team_id)),
        )
        runner = self._runner(context.project.root)
        result = runner.run(
            self.catalog.handoff_dispatch(
                paths.houmao_project_dir,
                source=source_name,
                target=target_name,
                message_file=dispatch_payload_path,
                handoff_id=handoff_id,
            ),
            env=self.env,
        )
        command_record_id, command_payload_ref_id = self._record_command_result(
            context,
            store,
            team_id,
            target_agent_instance_id,
            result,
            paths.command_payloads,
            actor_ref=actor_ref,
        )
        diagnostics.extend(result.diagnostics)
        status = "failed" if has_errors(diagnostics) else "sent"
        handoff = HandoffRecord(
            id=handoff_id,
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            source_actor_ref=source_agent_instance_id,
            target_actor_ref=target_agent_instance_id,
            status=status,
            created_at=timestamp,
            updated_at=utc_timestamp(),
            research_task_id=research_task_id,
            run_id=run_record.id,
            agent_team_instance_id=team_id,
            completion_watcher_contract_refs=completion_watcher_contract_refs,
            expected_output_refs=expected_output_refs,
            provenance_refs=[f"provenance:houmao-handoff-dispatch:{handoff_id}:{timestamp}"],
        )
        store.record_handoff(handoff)
        store.link_agent_team_instance_refs(team_id, run_ids=[run_record.id], handoff_ids=[handoff_id])
        dispatch_record_id = f"adapter-handoff-dispatch-{_slug(handoff_id)}-{_timestamp_slug(timestamp)}"
        payload_ref_ids = [dispatch_payload_ref, command_payload_ref_id]
        store.record_adapter_handoff_dispatch(
            AdapterHandoffDispatchRecord(
                id=dispatch_record_id,
                research_topic_id=context.research_topic.id,
                topic_workspace_id=context.topic_workspace_id,
                handoff_id=handoff_id,
                agent_team_instance_id=team_id,
                source_agent_instance_id=source_agent_instance_id,
                target_agent_instance_id=target_agent_instance_id,
                adapter_id=HOUMAO_ADAPTER_ID,
                status=status,
                research_task_id=research_task_id,
                run_id=run_record.id,
                command_run_ids=[command_record_id],
                payload_ref_ids=payload_ref_ids,
                expected_output_refs=expected_output_refs,
                completion_watcher_contract_refs=completion_watcher_contract_refs,
                diagnostics=[diagnostic.to_json() for diagnostic in diagnostics],
                actor_ref=actor_ref,
                created_at=timestamp,
                updated_at=utc_timestamp(),
                provenance_refs=[f"provenance:houmao-handoff-dispatch:{handoff_id}:{timestamp}"],
            )
        )
        return HoumaoHandoffDispatchResult(
            status=status,
            handoff_id=handoff_id,
            run_id=run_record.id,
            dispatch_record_id=dispatch_record_id,
            command_run_ids=[command_record_id],
            payload_ref_ids=payload_ref_ids,
            diagnostics=diagnostics,
        )

    def observe_handoff(
        self,
        *,
        context: EffectiveTopicContext,
        store: Any,
        summary: Any,
        handoff: HandoffRecord,
        observation_source: str,
        observation_payload_path: Path | None,
        summary_text: str | None,
        actor_ref: str | None,
    ) -> HoumaoHandoffObservationResult:
        diagnostics: list[Diagnostic] = []
        team_id = summary.agent_team_instance.id
        paths = build_houmao_adapter_paths(
            context.topic_workspace_path,
            team_id,
            [record.id for record in summary.agent_instances],
            houmao_project_dir=_latest_houmao_project_dir(summary),
        )
        self._record_path_plans(context, store, team_id, paths, diagnostics)
        if has_errors(diagnostics):
            return HoumaoHandoffObservationResult(
                status="failed",
                handoff_id=handoff.id,
                signal_observation_id=None,
                command_run_ids=[],
                payload_ref_ids=[],
                completion_authority=False,
                diagnostics=diagnostics,
            )
        _ensure_adapter_directories(paths)
        timestamp = utc_timestamp()
        command_run_ids: list[str] = []
        payload_ref_ids: list[str] = []
        observed_payload: dict[str, object]
        if observation_source in {"mail", "gateway"}:
            result = self._runner(context.project.root).run(
                self.catalog.handoff_observe(paths.houmao_project_dir, handoff_id=handoff.id, source=observation_source),
                env=self.env,
            )
            command_record_id, command_payload_ref_id = self._record_command_result(
                context,
                store,
                team_id,
                None,
                result,
                paths.command_payloads,
                actor_ref=actor_ref,
            )
            command_run_ids.append(command_record_id)
            payload_ref_ids.append(command_payload_ref_id)
            diagnostics.extend(result.diagnostics)
            observed_payload = {"source": observation_source, "command_result": result.to_json()}
        elif observation_source == "file" and observation_payload_path is not None:
            observed_payload = _load_observation_file(observation_payload_path, diagnostics)
        else:
            latest_snapshot = summary.adapter_inspection_snapshots[-1] if summary.adapter_inspection_snapshots else None
            observed_payload = {
                "source": observation_source,
                "inspection_snapshot": latest_snapshot.to_json() if latest_snapshot is not None else None,
            }
        observation_suffix = f"{_slug(observation_source)}-{_timestamp_slug(timestamp)}-{_stable_suffix(observed_payload)}"
        observation_path = paths.handoff_observations / f"{handoff.id}-observation-{observation_suffix}.json"
        observation_doc = {
            "kind": "houmao_manual_handoff_observation",
            "handoff_id": handoff.id,
            "source": observation_source,
            "summary": summary_text or _observation_summary(observed_payload),
            "candidate_completion": not has_errors(diagnostics),
            "payload": observed_payload,
            "observed_at": timestamp,
        }
        _write_json_file(observation_path, observation_doc)
        observation_payload_ref = self._record_payload_ref(
            context,
            store,
            agent_team_instance_id=team_id,
            agent_instance_id=handoff.target_actor_ref,
            payload_kind=f"handoff_observation:{observation_source}",
            payload_path=observation_path,
            payload_digest=file_digest(observation_path),
            source=f"houmao_handoff_{observation_source}",
            command_run_id=command_run_ids[-1] if command_run_ids else None,
            path_plan_id=_path_plan_id_by_surface(store, context.topic_workspace_id, adapter_handoff_observation_surface(team_id)),
        )
        payload_ref_ids.append(observation_payload_ref)
        status = "failed" if has_errors(diagnostics) else "candidate_completion"
        observation_id = f"signal-observation-{_slug(handoff.id)}-{observation_suffix}"
        store.record_signal_observation(
            SignalObservationRecord(
                id=observation_id,
                research_topic_id=context.research_topic.id,
                topic_workspace_id=context.topic_workspace_id,
                handoff_id=handoff.id,
                run_id=handoff.run_id,
                agent_team_instance_id=team_id,
                source_agent_instance_id=handoff.source_actor_ref,
                target_agent_instance_id=handoff.target_actor_ref,
                adapter_id=HOUMAO_ADAPTER_ID,
                observation_kind=observation_source,
                status=status,
                summary=summary_text or _observation_summary(observed_payload),
                command_run_ids=command_run_ids,
                payload_ref_ids=payload_ref_ids,
                diagnostics=[diagnostic.to_json() for diagnostic in diagnostics],
                actor_ref=actor_ref,
                observed_at=timestamp,
                provenance_refs=[f"provenance:houmao-signal-observation:{handoff.id}:{timestamp}"],
            )
        )
        store.record_handoff(replace(handoff, status="candidate" if status == "candidate_completion" else "failed", updated_at=utc_timestamp()))
        return HoumaoHandoffObservationResult(
            status=status,
            handoff_id=handoff.id,
            signal_observation_id=observation_id,
            command_run_ids=command_run_ids,
            payload_ref_ids=payload_ref_ids,
            completion_authority=False,
            diagnostics=diagnostics,
        )

    def normalize_handoff(
        self,
        *,
        context: EffectiveTopicContext,
        store: Any,
        handoff: HandoffRecord,
        status: str,
        rationale: str,
        signal_observation_ids: list[str],
        output_artifact_refs: list[str],
        corrective_refs: list[str],
        actor_ref: str | None,
    ) -> HoumaoHandoffNormalizationResult:
        diagnostics: list[Diagnostic] = []
        timestamp = utc_timestamp()
        paths = build_houmao_adapter_paths(
            context.topic_workspace_path,
            handoff.agent_team_instance_id or "unknown-team",
            [],
            houmao_project_dir=None,
        )
        self._record_path_plans(context, store, handoff.agent_team_instance_id or "unknown-team", paths, diagnostics)
        if has_errors(diagnostics):
            return HoumaoHandoffNormalizationResult(status="failed", handoff_id=handoff.id, normalization_record_id=None, run_id=handoff.run_id, output_artifact_refs=output_artifact_refs, payload_ref_ids=[], diagnostics=diagnostics)
        _ensure_adapter_directories(paths)
        normalization_id = f"handoff-normalization-{_slug(handoff.id)}-{_slug(status)}-{_timestamp_slug(timestamp)}"
        normalization_path = paths.handoff_normalizations / f"{normalization_id}.json"
        normalization_doc = {
            "kind": "houmao_manual_handoff_normalization",
            "handoff_id": handoff.id,
            "status": status,
            "rationale": rationale,
            "signal_observation_ids": signal_observation_ids,
            "output_artifact_refs": output_artifact_refs,
            "corrective_refs": corrective_refs,
            "actor_ref": actor_ref,
            "created_at": timestamp,
        }
        _write_json_file(normalization_path, normalization_doc)
        payload_ref_id = self._record_payload_ref(
            context,
            store,
            agent_team_instance_id=handoff.agent_team_instance_id or "unknown-team",
            agent_instance_id=None,
            payload_kind="handoff_normalization",
            payload_path=normalization_path,
            payload_digest=file_digest(normalization_path),
            source="isomer_handoff_normalization",
            command_run_id=None,
            path_plan_id=_path_plan_id_by_surface(store, context.topic_workspace_id, adapter_handoff_normalization_surface(handoff.agent_team_instance_id or "unknown-team")),
        )
        for artifact_ref in output_artifact_refs:
            _record_artifact_lifecycle(context, store, artifact_ref, timestamp, actor_ref)
        if status == "accepted" and handoff.run_id is not None:
            run = store.get_lifecycle_record(handoff.run_id)
            if run is not None:
                store.upsert_lifecycle_record(
                    replace(
                        run,
                        status="complete",
                        updated_at=timestamp,
                        transition_metadata={**run.transition_metadata, "handoff_normalization_id": normalization_id},
                    )
                )
        handoff_status = _handoff_status_from_normalization(status)
        store.record_handoff(replace(handoff, status=handoff_status, updated_at=timestamp))
        store.record_handoff_normalization(
            HandoffNormalizationRecord(
                id=normalization_id,
                research_topic_id=context.research_topic.id,
                topic_workspace_id=context.topic_workspace_id,
                handoff_id=handoff.id,
                run_id=handoff.run_id,
                status=status,
                rationale=rationale,
                signal_observation_ids=signal_observation_ids,
                output_artifact_refs=output_artifact_refs,
                corrective_refs=corrective_refs,
                payload_ref_ids=[payload_ref_id],
                actor_ref=actor_ref,
                created_at=timestamp,
                provenance_refs=[f"provenance:houmao-handoff-normalization:{handoff.id}:{timestamp}"],
            )
        )
        return HoumaoHandoffNormalizationResult(
            status=status,
            handoff_id=handoff.id,
            normalization_record_id=normalization_id,
            run_id=handoff.run_id,
            output_artifact_refs=output_artifact_refs,
            payload_ref_ids=[payload_ref_id],
            diagnostics=diagnostics,
        )

    def _runner(self, project_root: Path) -> Any:
        return self.runner or HoumaoCommandRunner(project_root, env=self.env)

    def _record_path_plans(
        self,
        context: EffectiveTopicContext,
        store: Any,
        agent_team_instance_id: str,
        paths: HoumaoAdapterPaths,
        diagnostics: list[Diagnostic],
    ) -> list[str]:
        surfaces = houmao_adapter_path_plan_targets(agent_team_instance_id, paths)
        path_plan_ids: list[str] = []
        for surface, path in surfaces.items():
            diagnostics.extend(validate_generated_adapter_path(context, path))
            if has_errors(diagnostics):
                continue
            plan = store.record_path_plan(
                topic_workspace_id=context.topic_workspace_id,
                surface=surface,
                path=path,
                source="houmao_adapter",
                source_detail="Houmao adapter durable material",
            )
            path_plan_ids.append(plan.id)
        return path_plan_ids

    def _record_material_payload_refs(
        self,
        context: EffectiveTopicContext,
        store: Any,
        summary: Any,
        material_refs: list[MaterialFileRef],
        path_plan_by_surface: Mapping[str, str],
    ) -> list[str]:
        ref_ids: list[str] = []
        for item in material_refs:
            path = Path(item.path)
            surface = adapter_agent_material_surface(summary.agent_team_instance.id, item.agent_instance_id or "shared")
            ref_ids.append(
                self._record_payload_ref(
                    context,
                    store,
                    agent_team_instance_id=summary.agent_team_instance.id,
                    agent_instance_id=item.agent_instance_id,
                    payload_kind=item.kind or "launch_material",
                    payload_path=path,
                    payload_digest=item.digest,
                    source=item.source,
                    command_run_id=None,
                    path_plan_id=path_plan_by_surface.get(surface),
                )
            )
        return ref_ids

    def _record_manifest_refs(
        self,
        context: EffectiveTopicContext,
        store: Any,
        summary: Any,
        refs: list[tuple[str, Path, str, str]],
    ) -> list[str]:
        ref_ids: list[str] = []
        for manifest_kind, manifest_path, manifest_digest, source in refs:
            timestamp = utc_timestamp()
            record_id = f"adapter-manifest-ref-{_slug(summary.agent_team_instance.id)}-{_slug(manifest_kind)}"
            path_plan = store.get_path_plan(
                context.topic_workspace_id,
                adapter_manifest_path_plan_surface(summary.agent_team_instance.id, manifest_kind),
            )
            store.record_adapter_manifest_ref(
                AdapterManifestRefRecord(
                    id=record_id,
                    research_topic_id=context.research_topic.id,
                    topic_workspace_id=context.topic_workspace_id,
                    agent_team_instance_id=summary.agent_team_instance.id,
                    adapter_id=HOUMAO_ADAPTER_ID,
                    manifest_kind=manifest_kind,
                    manifest_path=str(manifest_path.resolve(strict=False)),
                    manifest_digest=manifest_digest,
                    source=source,
                    path_plan_id=path_plan.id if path_plan is not None else None,
                    agent_instance_ids=[record.id for record in summary.agent_instances],
                    created_at=timestamp,
                    updated_at=timestamp,
                    provenance_refs=[f"provenance:houmao-manifest:{summary.agent_team_instance.id}:{manifest_kind}"],
                )
            )
            ref_ids.append(record_id)
        return ref_ids

    def _record_command_result(
        self,
        context: EffectiveTopicContext,
        store: Any,
        agent_team_instance_id: str,
        agent_instance_id: str | None,
        result: HoumaoCommandResult,
        payload_root: Path,
        *,
        actor_ref: str | None,
        operator_provenance: Mapping[str, object] | None = None,
    ) -> tuple[str, str]:
        timestamp = utc_timestamp()
        record_id = (
            f"adapter-command-{_slug(agent_team_instance_id)}-{_slug(result.operation_kind)}-"
            f"{_timestamp_slug(timestamp)}-{_stable_suffix({'argv': result.argv, 'agent_instance_id': agent_instance_id})}"
        )
        payload_path = payload_root / f"{record_id}.json"
        payload = result.to_json()
        if operator_provenance:
            payload["operator_provenance"] = dict(operator_provenance)
        _write_json_file(payload_path, payload)
        payload_ref_id = self._record_payload_ref(
            context,
            store,
            agent_team_instance_id=agent_team_instance_id,
            agent_instance_id=agent_instance_id,
            payload_kind=f"command:{result.operation_kind}",
            payload_path=payload_path,
            payload_digest=file_digest(payload_path),
            source="houmao_cli",
            command_run_id=record_id,
            path_plan_id=None,
        )
        store.record_adapter_command_run(
            AdapterCommandRunRecord(
                id=record_id,
                research_topic_id=context.research_topic.id,
                topic_workspace_id=context.topic_workspace_id,
                agent_team_instance_id=agent_team_instance_id,
                agent_instance_id=agent_instance_id,
                adapter_id=HOUMAO_ADAPTER_ID,
                operation_kind=result.operation_kind,
                argv=result.argv,
                cwd=result.cwd,
                env_hints=result.env_hints,
                status=result.status,
                returncode=result.returncode,
                started_at=result.started_at,
                finished_at=result.finished_at,
                duration_seconds=result.duration_seconds,
                payload_ref_ids=[payload_ref_id],
                diagnostics=[diagnostic.to_json() for diagnostic in result.diagnostics],
                actor_ref=actor_ref,
                provenance_refs=[
                    f"provenance:houmao-command:{agent_team_instance_id}:{timestamp}",
                    *_operator_provenance_ref_list(operator_provenance),
                ],
            )
        )
        return record_id, payload_ref_id

    def _record_payload_ref(
        self,
        context: EffectiveTopicContext,
        store: Any,
        *,
        agent_team_instance_id: str,
        agent_instance_id: str | None,
        payload_kind: str,
        payload_path: Path,
        payload_digest: str,
        source: str,
        command_run_id: str | None,
        path_plan_id: str | None,
    ) -> str:
        record_id = (
            f"adapter-payload-{_slug(agent_team_instance_id)}-"
            f"{_slug(agent_instance_id or 'team')}-{_slug(payload_kind)}-{_slug(payload_digest[-12:])}"
        )
        timestamp = utc_timestamp()
        store.record_adapter_payload_ref(
            AdapterPayloadRefRecord(
                id=record_id,
                research_topic_id=context.research_topic.id,
                topic_workspace_id=context.topic_workspace_id,
                agent_team_instance_id=agent_team_instance_id,
                agent_instance_id=agent_instance_id,
                adapter_id=HOUMAO_ADAPTER_ID,
                payload_kind=payload_kind,
                payload_path=str(payload_path.resolve(strict=False)),
                payload_digest=payload_digest,
                source=source,
                command_run_id=command_run_id,
                path_plan_id=path_plan_id,
                created_at=timestamp,
                provenance_refs=[f"provenance:houmao-payload:{agent_team_instance_id}:{timestamp}"],
            )
        )
        return record_id


def resolve_houmao_command(project_root: Path, env: Mapping[str, str]) -> HoumaoCommandResolution:
    configured = env.get(HOUMAO_COMMAND_ENV)
    if configured:
        return HoumaoCommandResolution(shlex.split(configured), project_root, "env")
    executable = shutil.which(DEFAULT_HOUMAO_COMMAND, path=env.get("PATH"))
    if executable is not None:
        return HoumaoCommandResolution([executable], project_root, "path")
    checkout_value = env.get(HOUMAO_CHECKOUT_ENV)
    checkout_candidates = []
    if checkout_value:
        checkout_candidates.append(Path(checkout_value).expanduser())
    checkout_candidates.extend([project_root / "extern" / "orphan" / "houmao", Path.home() / "workspace" / "code" / "houmao"])
    pixi = shutil.which("pixi", path=env.get("PATH"))
    for checkout in checkout_candidates:
        resolved = checkout.resolve(strict=False)
        if (resolved / "pyproject.toml").exists() and pixi is not None:
            return HoumaoCommandResolution([pixi, "run", DEFAULT_HOUMAO_COMMAND], resolved, "local_checkout")
    diagnostics = [
        _adapter_diagnostic(
            "ISO070",
            "error",
            "Houmao command was not found on PATH and no Pixi-backed local checkout was available.",
            field=DEFAULT_HOUMAO_COMMAND,
        )
    ]
    return HoumaoCommandResolution([], project_root, "missing", diagnostics)


def build_houmao_adapter_paths(
    topic_workspace_path: Path,
    agent_team_instance_id: str,
    agent_instance_ids: list[str],
    *,
    houmao_project_dir: Path | None,
) -> HoumaoAdapterPaths:
    root = manifest_paths(topic_workspace_path, agent_team_instance_id).root
    return HoumaoAdapterPaths(
        adapter_root=root,
        launch_material_root=root / "launch-material",
        command_payloads=root / "command-payloads",
        launch_logs=root / "logs",
        inspection_snapshots=root / "inspection-snapshots",
        stop_outcomes=root / "stop-outcomes",
        handoff_payloads=root / "handoff-payloads",
        handoff_observations=root / "handoff-observations",
        handoff_normalizations=root / "handoff-normalizations",
        houmao_project_dir=(houmao_project_dir or root / "houmao-project").resolve(strict=False),
        generated_profile_root=root / "houmao-project-files",
        agent_material_roots={agent_id: root / "launch-material" / "agents" / _slug(agent_id) for agent_id in agent_instance_ids},
    )


def houmao_adapter_path_plan_targets(agent_team_instance_id: str, paths: HoumaoAdapterPaths) -> dict[str, Path]:
    targets = {
        adapter_root_surface(agent_team_instance_id): paths.adapter_root,
        adapter_manifest_path_plan_surface(agent_team_instance_id, ManifestKind.ADAPTER_LINK.value): paths.adapter_root / "adapter-link.json",
        adapter_manifest_path_plan_surface(agent_team_instance_id, ManifestKind.LAUNCH_MATERIAL.value): paths.adapter_root / "launch-material-manifest.json",
        adapter_manifest_path_plan_surface(agent_team_instance_id, ManifestKind.ADAPTER_RUNTIME.value): paths.adapter_root / "adapter-runtime-manifest.json",
        adapter_launch_material_surface(agent_team_instance_id): paths.launch_material_root,
        adapter_command_payload_surface(agent_team_instance_id): paths.command_payloads,
        adapter_launch_log_surface(agent_team_instance_id): paths.launch_logs,
        adapter_inspection_snapshot_surface(agent_team_instance_id): paths.inspection_snapshots,
        adapter_stop_outcome_surface(agent_team_instance_id): paths.stop_outcomes,
        adapter_handoff_payload_surface(agent_team_instance_id): paths.handoff_payloads,
        adapter_handoff_observation_surface(agent_team_instance_id): paths.handoff_observations,
        adapter_handoff_normalization_surface(agent_team_instance_id): paths.handoff_normalizations,
        adapter_houmao_project_surface(agent_team_instance_id): paths.houmao_project_dir,
        adapter_generated_profile_surface(agent_team_instance_id): paths.generated_profile_root,
    }
    for agent_id, path in paths.agent_material_roots.items():
        targets[adapter_agent_material_surface(agent_team_instance_id, agent_id)] = path
    return targets


def adapter_root_surface(agent_team_instance_id: str) -> str:
    return f"houmao_adapter_root:{HOUMAO_ADAPTER_ID}:{agent_team_instance_id}"


def adapter_launch_material_surface(agent_team_instance_id: str) -> str:
    return f"houmao_launch_material_root:{HOUMAO_ADAPTER_ID}:{agent_team_instance_id}"


def adapter_agent_material_surface(agent_team_instance_id: str, agent_instance_id: str) -> str:
    return f"houmao_agent_material:{HOUMAO_ADAPTER_ID}:{agent_team_instance_id}:{agent_instance_id}"


def adapter_command_payload_surface(agent_team_instance_id: str) -> str:
    return f"houmao_command_payloads:{HOUMAO_ADAPTER_ID}:{agent_team_instance_id}"


def adapter_launch_log_surface(agent_team_instance_id: str) -> str:
    return f"houmao_launch_logs:{HOUMAO_ADAPTER_ID}:{agent_team_instance_id}"


def adapter_inspection_snapshot_surface(agent_team_instance_id: str) -> str:
    return f"houmao_inspection_snapshots:{HOUMAO_ADAPTER_ID}:{agent_team_instance_id}"


def adapter_stop_outcome_surface(agent_team_instance_id: str) -> str:
    return f"houmao_stop_outcomes:{HOUMAO_ADAPTER_ID}:{agent_team_instance_id}"


def adapter_handoff_payload_surface(agent_team_instance_id: str) -> str:
    return f"houmao_handoff_payloads:{HOUMAO_ADAPTER_ID}:{agent_team_instance_id}"


def adapter_handoff_observation_surface(agent_team_instance_id: str) -> str:
    return f"houmao_handoff_observations:{HOUMAO_ADAPTER_ID}:{agent_team_instance_id}"


def adapter_handoff_normalization_surface(agent_team_instance_id: str) -> str:
    return f"houmao_handoff_normalizations:{HOUMAO_ADAPTER_ID}:{agent_team_instance_id}"


def adapter_houmao_project_surface(agent_team_instance_id: str) -> str:
    return f"houmao_project_dir:{HOUMAO_ADAPTER_ID}:{agent_team_instance_id}"


def adapter_generated_profile_surface(agent_team_instance_id: str) -> str:
    return f"houmao_generated_profile_files:{HOUMAO_ADAPTER_ID}:{agent_team_instance_id}"


def validate_generated_adapter_path(context: EffectiveTopicContext, path: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    candidate = path.resolve(strict=False)
    topic_workspace = context.topic_workspace_path.resolve(strict=False)
    try:
        candidate.relative_to(topic_workspace)
    except ValueError:
        diagnostics.append(_adapter_diagnostic("ISO005", "error", "Houmao adapter path must resolve under the selected Topic Workspace.", path=candidate))
    try:
        candidate.relative_to((context.project.root / ".isomer-labs").resolve(strict=False))
    except ValueError:
        pass
    else:
        diagnostics.append(_adapter_diagnostic("ISO005", "error", "Houmao adapter path must not resolve under .isomer-labs.", path=candidate))
    for checkout in (context.project.root / "extern" / "orphan" / "houmao", Path.home() / "workspace" / "code" / "houmao"):
        try:
            candidate.relative_to(checkout.resolve(strict=False))
        except ValueError:
            continue
        diagnostics.append(_adapter_diagnostic("ISO005", "error", "Houmao adapter path must not resolve under the Houmao source checkout.", path=candidate))
    return diagnostics


def _failed_materialization(paths: HoumaoAdapterPaths, diagnostics: list[Diagnostic]) -> HoumaoMaterializationResult:
    return HoumaoMaterializationResult(
        status="failed",
        paths=paths,
        agents=[],
        link_manifest={},
        launch_material_manifest={},
        link_manifest_path=paths.adapter_root / "adapter-link.json",
        launch_material_manifest_path=paths.adapter_root / "launch-material-manifest.json",
        material_refs=[],
        manifest_ref_ids=[],
        payload_ref_ids=[],
        path_plan_ids=[],
        materialization_record_id="",
        diagnostics=diagnostics,
    )


def _adapter_reconciliation_record(
    context: EffectiveTopicContext,
    agent_team_instance_id: str,
    result: Any,
    actor_ref: str | None,
    *,
    operator_provenance: Mapping[str, object] | None = None,
) -> Any:
    from isomer_labs.runtime.records import AdapterReconciliationRecord

    timestamp = utc_timestamp()
    state = str(result.state)
    return AdapterReconciliationRecord(
        id=f"adapter-reconciliation-{_slug(agent_team_instance_id)}-{_slug(state)}-{_timestamp_slug(timestamp)}",
        research_topic_id=context.research_topic.id,
        topic_workspace_id=context.topic_workspace_id,
        agent_team_instance_id=agent_team_instance_id,
        adapter_id=HOUMAO_ADAPTER_ID,
        state=state,
        mapping_confidence=str(result.mapping_confidence),
        manifest_refs=list(result.manifest_refs),
        manifest_digest_summary=dict(result.manifest_digest_summary),
        live_observation_summary=dict(result.live_observation_summary),
        diagnostics=[diagnostic.to_json() for diagnostic in result.diagnostics],
        actor_ref=actor_ref,
        created_at=timestamp,
        provenance_refs=[
            f"provenance:houmao-reconciliation:{agent_team_instance_id}:{timestamp}",
            *_operator_provenance_ref_list(operator_provenance),
        ],
    )


def _bounded_operator_provenance(summary: Any, profile: TopicAgentTeamProfile, actor_ref: str | None) -> dict[str, object]:
    data = _bounded_summary_provenance(summary, actor_ref)
    for key, value in (
        ("topic_agent_team_profile_bundle_ref", profile.profile_bundle_ref),
        ("instantiation_packet_ref", profile.instantiation_packet_ref),
        ("approval_ref", profile.approval_ref),
        ("approval_actor_ref", profile.approval_actor_ref),
        ("approval_mode", profile.approval_mode),
        ("project_operator_ref", profile.project_operator_ref),
    ):
        if value:
            data[key] = value
    if profile.topic_service_agent_refs:
        data["topic_service_agent_refs"] = list(profile.topic_service_agent_refs)
    if profile.validation_refs:
        data["validation_refs"] = list(profile.validation_refs)
    return data


def _bounded_summary_provenance(summary: Any, actor_ref: str | None) -> dict[str, object]:
    team = getattr(summary, "agent_team_instance", None)
    data: dict[str, object] = {}
    if actor_ref:
        data["actor_ref"] = actor_ref
    if team is None:
        return data
    for key in (
        "topic_agent_team_profile_bundle_ref",
        "instantiation_packet_ref",
        "approval_ref",
        "project_operator_ref",
    ):
        value = getattr(team, key, None)
        if value:
            data[key] = value
    for key in ("topic_service_agent_refs", "validation_refs"):
        value = getattr(team, key, None)
        if value:
            data[key] = list(value)
    return data


def _operator_provenance_ref_list(operator_provenance: Mapping[str, object] | None) -> list[str]:
    if not operator_provenance:
        return []
    refs: list[str] = []
    for key in (
        "actor_ref",
        "project_operator_ref",
        "topic_agent_team_profile_bundle_ref",
        "instantiation_packet_ref",
        "approval_ref",
        "approval_actor_ref",
    ):
        value = operator_provenance.get(key)
        if isinstance(value, str) and value:
            refs.append(value)
    for key in ("topic_service_agent_refs", "validation_refs"):
        value = operator_provenance.get(key)
        if isinstance(value, list):
            refs.extend(item for item in value if isinstance(item, str) and item)
    return list(dict.fromkeys(refs))


def _summary_agent(summary: Any, agent_instance_id: str) -> Any | None:
    for agent in summary.agent_instances:
        if agent.id == agent_instance_id:
            return agent
    return None


def _latest_houmao_project_dir(summary: Any) -> Path | None:
    for manifest_ref in reversed(summary.adapter_manifest_refs):
        if manifest_ref.manifest_kind == ManifestKind.ADAPTER_LINK.value:
            try:
                manifest = json.loads(Path(manifest_ref.manifest_path).read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            houmao = manifest.get("houmao")
            if isinstance(houmao, dict) and isinstance(houmao.get("project_dir"), str):
                return Path(str(houmao["project_dir"])).expanduser().resolve(strict=False)
    return None


def _houmao_name_for_agent(summary: Any, agent_instance_id: str) -> str:
    latest_launch = summary.adapter_launch_attempts[-1] if summary.adapter_launch_attempts else None
    if latest_launch is not None:
        for ref in latest_launch.adapter_refs:
            if isinstance(ref, dict) and ref.get("agent_instance_id") == agent_instance_id and isinstance(ref.get("houmao_agent_name"), str):
                return str(ref["houmao_agent_name"])
    for manifest_ref in reversed(summary.adapter_manifest_refs):
        if manifest_ref.manifest_kind != ManifestKind.ADAPTER_LINK.value:
            continue
        try:
            manifest = json.loads(Path(manifest_ref.manifest_path).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for binding in _bindings_from_link(manifest):
            if binding.get("agent_instance_id") == agent_instance_id and isinstance(binding.get("houmao_agent_name"), str):
                return str(binding["houmao_agent_name"])
    return _houmao_agent_name(agent_instance_id)


def _path_plan_id_by_surface(store: Any, topic_workspace_id: str, surface: str) -> str | None:
    plan = store.get_path_plan(topic_workspace_id, surface)
    return plan.id if plan is not None else None


def _load_observation_file(path: Path, diagnostics: list[Diagnostic]) -> dict[str, object]:
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        diagnostics.append(_adapter_diagnostic("ISO063", "error", f"Observation file could not be read: {exc}.", path=path))
        return {"source": "file", "error": str(exc)}
    try:
        loaded = json.loads(raw)
    except json.JSONDecodeError:
        return {"source": "file", "text": raw}
    if isinstance(loaded, dict):
        return {"source": "file", "json": loaded}
    return {"source": "file", "json": loaded}


def _observation_summary(payload: Mapping[str, object]) -> str:
    source = str(payload.get("source", "adapter"))
    if "command_result" in payload:
        command = payload["command_result"]
        if isinstance(command, dict):
            status = command.get("status") or command.get("returncode") or "observed"
            return f"{source} observation status: {status}"
    if "json" in payload:
        return f"{source} observation JSON payload recorded"
    if "text" in payload:
        text = str(payload["text"]).strip().splitlines()
        return text[0][:160] if text else f"{source} observation text recorded"
    return f"{source} observation recorded"


def _record_artifact_lifecycle(
    context: EffectiveTopicContext,
    store: Any,
    artifact_ref: str,
    timestamp: str,
    actor_ref: str | None,
) -> None:
    existing = store.get_lifecycle_record(artifact_ref)
    if existing is not None:
        return
    refs: dict[str, str] = {}
    if actor_ref is not None:
        refs["actor_ref"] = actor_ref
    store.upsert_lifecycle_record(
        RuntimeLifecycleRecord(
            id=artifact_ref,
            record_kind="artifact",
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            status="complete",
            created_at=timestamp,
            updated_at=timestamp,
            lifecycle_refs=refs,
            transition_metadata={"source": "handoff_normalization"},
            provenance_refs=[f"provenance:artifact:{artifact_ref}:{timestamp}"],
        )
    )


def _handoff_status_from_normalization(status: str) -> str:
    return {
        "accepted": "accepted",
        "rejected": "rejected",
        "blocked": "blocked",
        "superseded": "superseded",
        "repair_routed": "repair",
        "follow_up": "follow_up",
    }.get(status, "blocked")


def _ensure_adapter_directories(paths: HoumaoAdapterPaths) -> None:
    for path in [
        paths.adapter_root,
        paths.launch_material_root,
        paths.command_payloads,
        paths.launch_logs,
        paths.inspection_snapshots,
        paths.stop_outcomes,
        paths.handoff_payloads,
        paths.handoff_observations,
        paths.handoff_normalizations,
        paths.houmao_project_dir,
        paths.generated_profile_root,
        *paths.agent_material_roots.values(),
    ]:
        path.mkdir(parents=True, exist_ok=True)


def _bounded_env(env: Mapping[str, str]) -> dict[str, str]:
    allowed = ("PATH", "HOME", "SHELL", "TERM", "LANG", "LC_ALL", "PYTHONPATH", "PIXI_HOME")
    return {
        key: value
        for key, value in env.items()
        if key in allowed or key.startswith("HOMEBREW_") or key.startswith("HOUMAO_FAKE_")
    }


def _env_hints(env: Mapping[str, str]) -> dict[str, str]:
    hints: dict[str, str] = {}
    for key in ("PATH", "HOME", "PIXI_HOME"):
        if key in env:
            hints[key] = "[set]"
    return hints


def _parse_json_or_none(value: str) -> object | None:
    stripped = value.strip()
    if not stripped:
        return None
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        return None


def _parse_json_or_text(value: str) -> object:
    parsed = _parse_json_or_none(value)
    if parsed is not None:
        return parsed
    return value.strip()


def _string_output(value: bytes | str | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def _write_json_file(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(redact_payload(dict(payload)), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _system_prompt(profile: TopicAgentTeamProfile, agent_role_id: str, role_binding: Any | None) -> str:
    payload = {
        "topic_agent_team_profile_id": profile.id,
        "research_topic_id": profile.research_topic_id,
        "agent_role_id": agent_role_id,
        "agent_profile_ref": getattr(role_binding, "agent_profile_ref", None),
        "required_skills": getattr(role_binding, "required_skills", []),
        "optional_skills": getattr(role_binding, "optional_skills", []),
    }
    return (
        "# Isomer Agent Instance Launch Material\n\n"
        "You are being launched as one Agent Instance in an Isomer Labs Agent Team Instance.\n\n"
        "## Runtime Context\n\n"
        f"```json\n{json.dumps(payload, indent=2, sort_keys=True)}\n```\n"
    )


def _houmao_profile_name(agent_team_instance_id: str, agent_role_id: str) -> str:
    return f"isomer-{_slug(agent_team_instance_id)}-{_slug(agent_role_id)}"[:96]


def _houmao_agent_name(agent_instance_id: str) -> str:
    return f"isomer-{_slug(agent_instance_id)}"[:96]


def _launchable_profile_diagnostics(profile: TopicAgentTeamProfile) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if profile.raw.get("preview") is True:
        diagnostics.append(
            Diagnostic(
                code="ISO097",
                severity="error",
                concept="Houmao adapter launch material",
                field="profile_materialization",
                message="Houmao launch materialization requires approved profile bundle/runtime material, not preview-only Topic Agent Team Profile output.",
            )
        )
    if profile.profile_bundle_ref is not None and (profile.instantiation_packet_ref is None or profile.approval_ref is None):
        diagnostics.append(
            Diagnostic(
                code="ISO095",
                severity="error",
                concept="Houmao adapter launch material",
                field="profile_bundle_ref",
                message="Houmao launch materialization requires packet and approval provenance for profile bundles.",
            )
        )
    return diagnostics


def _agent_for_command(spec: HoumaoCommandSpec, by_name: Mapping[str, HoumaoMaterializedAgent]) -> HoumaoMaterializedAgent | None:
    for index, arg in enumerate(spec.args):
        if arg == "--name" and index + 1 < len(spec.args):
            candidate = by_name.get(spec.args[index + 1])
            if candidate is not None:
                return candidate
        if arg == "--agent-name" and index + 1 < len(spec.args):
            candidate = by_name.get(spec.args[index + 1])
            if candidate is not None:
                return candidate
    return None


def _agent_observation_from_result(result: HoumaoCommandResult) -> object:
    if result.parsed_json is not None:
        return redact_payload(result.parsed_json)
    return result.sanitized_output()


def _bindings_from_link(link_manifest: Mapping[str, object] | None) -> list[dict[str, object]]:
    if link_manifest is None:
        return []
    bindings = link_manifest.get("agent_bindings")
    if not isinstance(bindings, list):
        return []
    return [item for item in bindings if isinstance(item, dict)]


def _project_dir_from_link(link_manifest: Mapping[str, object] | None) -> Path | None:
    if link_manifest is None:
        return None
    houmao = link_manifest.get("houmao")
    if isinstance(houmao, dict) and isinstance(houmao.get("project_dir"), str):
        return Path(str(houmao["project_dir"])).expanduser().resolve(strict=False)
    return None


def _agents_from_results(results: list[HoumaoCommandResult]) -> list[dict[str, object]]:
    agents: list[dict[str, object]] = []
    for result in results:
        parsed = result.parsed_json
        if isinstance(parsed, dict):
            for key in ("agents", "managed_agents", "records"):
                value = parsed.get(key)
                if isinstance(value, list):
                    agents.extend(item for item in value if isinstance(item, dict))
            if any(key in parsed for key in ("agent_id", "managed_agent_id", "agent_name", "name")):
                agents.append(parsed)
        elif isinstance(parsed, list):
            agents.extend(item for item in parsed if isinstance(item, dict))
    redacted = redact_payload(agents)
    return _deduplicate_agent_records(redacted if isinstance(redacted, list) else agents)


def _deduplicate_agent_records(agents: Iterable[object]) -> list[dict[str, object]]:
    deduplicated: list[dict[str, object]] = []
    seen: set[str] = set()
    for agent in agents:
        if not isinstance(agent, dict):
            continue
        key = str(
            agent.get("agent_id")
            or agent.get("managed_agent_id")
            or agent.get("agent_name")
            or agent.get("name")
            or canonical_json_digest(agent)
        )
        if key in seen:
            continue
        seen.add(key)
        deduplicated.append(agent)
    return deduplicated


def _adapter_diagnostic(
    code: str,
    severity: Literal["error", "warning"],
    message: str,
    *,
    field: str | None = None,
    path: Path | None = None,
) -> Diagnostic:
    return Diagnostic(
        code=code,
        severity=severity,
        concept="Houmao CLI adapter",
        field=field,
        path=path,
        message=message,
    )


def _slug(value: str) -> str:
    return "".join(character if character.isalnum() or character in "._-" else "-" for character in value).strip("-") or "record"


def _timestamp_slug(value: str) -> str:
    return _slug(value.replace(":", "").replace("-", ""))


def _stable_suffix(value: object) -> str:
    return canonical_json_digest(value).split(":", 1)[1][:12]
