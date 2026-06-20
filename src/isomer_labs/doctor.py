"""Read-only host, Project, and topic diagnostics for the doctor command."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import shutil
import subprocess
from typing import Any, Literal

from isomer_labs.diagnostics import Diagnostic, has_errors
from isomer_labs.models import EffectiveTopicContext, Project
from isomer_labs.path_utils import display_path, is_within, resolve_project_path
from isomer_labs.toml_loader import load_toml


CheckScope = Literal["host", "project", "topic"]
CheckStatus = Literal["pass", "warn", "fail", "skip"]


@dataclass(frozen=True)
class DoctorCheck:
    id: str
    scope: CheckScope
    status: CheckStatus
    concept: str
    summary: str
    source_path: str | None = None
    source_detail: str | None = None
    details: dict[str, object] = field(default_factory=dict)

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "id": self.id,
            "scope": self.scope,
            "status": self.status,
            "concept": self.concept,
            "summary": self.summary,
        }
        if self.source_path is not None:
            data["source_path"] = self.source_path
        if self.source_detail is not None:
            data["source_detail"] = self.source_detail
        if self.details:
            data["details"] = self.details
        return data


@dataclass(frozen=True)
class PixiHostInfo:
    available: bool
    executable_path: str | None = None
    version: str | None = None

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {"available": self.available}
        if self.executable_path is not None:
            data["executable_path"] = self.executable_path
        if self.version is not None:
            data["version"] = self.version
        return data


@dataclass(frozen=True)
class PixiManifestInfo:
    manifest_path: Path
    manifest_kind: str
    environments: list[str]
    requires_pixi: str | None = None

    def to_json(self, project_root: Path | None = None) -> dict[str, object]:
        path = display_path(self.manifest_path, project_root) if project_root is not None else str(self.manifest_path)
        data: dict[str, object] = {
            "manifest_path": path,
            "manifest_kind": self.manifest_kind,
            "environments": self.environments,
        }
        if self.requires_pixi is not None:
            data["requires_pixi"] = self.requires_pixi
        return data


@dataclass(frozen=True)
class DoctorReport:
    mode: Literal["dependency-only", "project", "topic"]
    checks: list[DoctorCheck]
    diagnostics: list[Diagnostic]
    pixi: PixiHostInfo
    project: dict[str, object] | None = None
    topic: dict[str, object] | None = None

    @property
    def ok(self) -> bool:
        return not has_errors(self.diagnostics) and all(check.status != "fail" for check in self.checks)

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "ok": self.ok,
            "mode": self.mode,
            "mutated": False,
            "checks": [check.to_json() for check in self.checks],
            "pixi": self.pixi.to_json(),
        }
        if self.project is not None:
            payload["project"] = self.project
        if self.topic is not None:
            payload["topic"] = self.topic
        return payload


def build_doctor_report(
    *,
    project: Project | None,
    discovery_diagnostics: list[Diagnostic],
    project_diagnostics: list[Diagnostic],
    context: EffectiveTopicContext | None,
    context_diagnostics: list[Diagnostic],
    topic_skipped: bool,
) -> DoctorReport:
    checks: list[DoctorCheck] = []
    diagnostics = [*discovery_diagnostics, *project_diagnostics, *context_diagnostics]
    pixi, host_checks, host_diagnostics = inspect_host_pixi()
    checks.extend(host_checks)
    diagnostics.extend(host_diagnostics)

    project_payload: dict[str, object] | None = None
    project_pixi_info: PixiManifestInfo | None = None
    if project is None:
        if discovery_diagnostics:
            checks.append(
                DoctorCheck(
                    id="project.discovery",
                    scope="project",
                    status="fail",
                    concept="Project",
                    summary="Project discovery failed; Project-level Pixi checks were not run.",
                )
            )
            mode: Literal["dependency-only", "project", "topic"] = "project"
        else:
            checks.append(
                DoctorCheck(
                    id="project.discovery",
                    scope="project",
                    status="skip",
                    concept="Project",
                    summary="No Project was discovered; only host dependency checks were run.",
                )
            )
            mode = "dependency-only"
    else:
        project_pixi_info, project_payload, project_checks, project_pixi_diagnostics = inspect_project_pixi(
            project,
            pixi,
            project_diagnostics,
        )
        checks.extend(project_checks)
        diagnostics.extend(project_pixi_diagnostics)
        if context is None:
            checks.append(
                DoctorCheck(
                    id="topic.selection",
                    scope="topic",
                    status="skip" if topic_skipped else "fail",
                    concept="Effective Topic Context",
                    summary=(
                        "No Research Topic was selected; topic Pixi binding checks were skipped."
                        if topic_skipped
                        else "Research Topic selection failed; topic Pixi binding checks were not run."
                    ),
                )
            )
            mode = "project"
        else:
            topic_payload, topic_checks, topic_diagnostics = inspect_topic_pixi(context, project_pixi_info)
            checks.extend(topic_checks)
            diagnostics.extend(topic_diagnostics)
            mode = "topic"

    return DoctorReport(
        mode=mode,
        checks=checks,
        diagnostics=diagnostics,
        pixi=pixi,
        project=project_payload,
        topic=topic_payload if context is not None else None,
    )


def inspect_host_pixi() -> tuple[PixiHostInfo, list[DoctorCheck], list[Diagnostic]]:
    checks: list[DoctorCheck] = []
    diagnostics: list[Diagnostic] = []
    pixi_path = shutil.which("pixi")
    if pixi_path is None:
        checks.append(
            DoctorCheck(
                id="host.pixi.executable",
                scope="host",
                status="fail",
                concept="Pixi",
                summary="Pixi executable was not found on PATH.",
            )
        )
        diagnostics.append(
            Diagnostic(
                code="ISO030",
                severity="error",
                concept="Pixi",
                message="Pixi is a required dependency for this Isomer Labs version, but no pixi executable was found on PATH.",
            )
        )
        checks.append(
            DoctorCheck(
                id="host.pixi.version",
                scope="host",
                status="skip",
                concept="Pixi",
                summary="Pixi version check was skipped because the executable is missing.",
            )
        )
        return PixiHostInfo(available=False), checks, diagnostics

    checks.append(
        DoctorCheck(
            id="host.pixi.executable",
            scope="host",
            status="pass",
            concept="Pixi",
            summary="Pixi executable was found.",
            source_detail=pixi_path,
        )
    )
    result, error = _run_command([pixi_path, "--version"])
    if error is not None:
        checks.append(
            DoctorCheck(
                id="host.pixi.version",
                scope="host",
                status="fail",
                concept="Pixi",
                summary=f"Pixi version check failed: {error}.",
            )
        )
        diagnostics.append(
            Diagnostic(
                code="ISO031",
                severity="error",
                concept="Pixi",
                message=f"Pixi version check failed: {error}.",
            )
        )
        return PixiHostInfo(available=True, executable_path=pixi_path), checks, diagnostics
    assert result is not None
    if result.returncode != 0:
        message = _command_failure_summary(result)
        checks.append(
            DoctorCheck(
                id="host.pixi.version",
                scope="host",
                status="fail",
                concept="Pixi",
                summary=f"Pixi version check failed: {message}.",
            )
        )
        diagnostics.append(
            Diagnostic(
                code="ISO031",
                severity="error",
                concept="Pixi",
                message=f"Pixi version check returned a non-zero exit status: {message}.",
            )
        )
        return PixiHostInfo(available=True, executable_path=pixi_path), checks, diagnostics

    version = _first_output_line(result.stdout) or _first_output_line(result.stderr)
    if version is None:
        checks.append(
            DoctorCheck(
                id="host.pixi.version",
                scope="host",
                status="warn",
                concept="Pixi",
                summary="Pixi version check completed, but no parseable version output was returned.",
            )
        )
        return PixiHostInfo(available=True, executable_path=pixi_path), checks, diagnostics

    checks.append(
        DoctorCheck(
            id="host.pixi.version",
            scope="host",
            status="pass",
            concept="Pixi",
            summary=f"Pixi version detected: {version}.",
        )
    )
    return PixiHostInfo(available=True, executable_path=pixi_path, version=version), checks, diagnostics


def inspect_project_pixi(
    project: Project,
    pixi: PixiHostInfo,
    project_diagnostics: list[Diagnostic],
) -> tuple[PixiManifestInfo | None, dict[str, object], list[DoctorCheck], list[Diagnostic]]:
    checks: list[DoctorCheck] = [
        DoctorCheck(
            id="project.discovery",
            scope="project",
            status="pass",
            concept="Project",
            summary="Project was discovered.",
            source_path=display_path(project.manifest_path, project.root),
            source_detail=project.discovery_source,
        )
    ]
    diagnostics: list[Diagnostic] = []
    checks.append(_project_manifest_validation_check(project, project_diagnostics))

    pixi_info, pixi_diagnostics = find_project_pixi_manifest(project.root)
    diagnostics.extend(pixi_diagnostics)
    if pixi_info is None:
        checks.append(
            DoctorCheck(
                id="project.pixi.manifest",
                scope="project",
                status="fail",
                concept="Project Pixi manifest",
                summary="No Project-level pixi.toml or pyproject.toml Pixi configuration was found.",
            )
        )
        checks.append(
            DoctorCheck(
                id="project.pixi.lockfile",
                scope="project",
                status="skip",
                concept="Project Pixi lockfile",
                summary="Pixi lockfile check was skipped because no Project-level Pixi manifest was found.",
            )
        )
        checks.append(
            DoctorCheck(
                id="project.pixi.requires",
                scope="project",
                status="skip",
                concept="Pixi version requirement",
                summary="Pixi requirement verification was skipped because no Project-level Pixi manifest was found.",
            )
        )
        project_payload = {
            **project.to_json(),
            "pixi_manifest": None,
            "pixi_lockfile": None,
        }
        return pixi_info, project_payload, checks, diagnostics

    checks.append(
        DoctorCheck(
            id="project.pixi.manifest",
            scope="project",
            status="pass",
            concept="Project Pixi manifest",
            summary="Project-level Pixi manifest was found.",
            source_path=display_path(pixi_info.manifest_path, project.root),
            details={
                "manifest_kind": pixi_info.manifest_kind,
                "environments": pixi_info.environments,
            },
        )
    )
    lockfile = project.root / "pixi.lock"
    if lockfile.exists():
        checks.append(
            DoctorCheck(
                id="project.pixi.lockfile",
                scope="project",
                status="pass",
                concept="Project Pixi lockfile",
                summary="pixi.lock is present.",
                source_path=display_path(lockfile, project.root),
            )
        )
    else:
        checks.append(
            DoctorCheck(
                id="project.pixi.lockfile",
                scope="project",
                status="warn",
                concept="Project Pixi lockfile",
                summary="Project-level Pixi manifest exists, but pixi.lock is absent.",
                source_path=display_path(lockfile, project.root),
            )
        )

    checks.append(_requires_pixi_check(pixi, pixi_info, project.root, diagnostics))
    project_payload = {
        **project.to_json(),
        "pixi_manifest": pixi_info.to_json(project.root),
        "pixi_lockfile": display_path(lockfile, project.root) if lockfile.exists() else None,
    }
    return pixi_info, project_payload, checks, diagnostics


def inspect_topic_pixi(
    context: EffectiveTopicContext,
    project_pixi_info: PixiManifestInfo | None,
) -> tuple[dict[str, object], list[DoctorCheck], list[Diagnostic]]:
    checks: list[DoctorCheck] = [
        DoctorCheck(
            id="topic.selection",
            scope="topic",
            status="pass",
            concept="Effective Topic Context",
            summary=f"Research Topic selected: {context.research_topic.id}.",
            source_detail=context.sources.get("research_topic_id"),
        )
    ]
    diagnostics: list[Diagnostic] = []
    project = context.project
    topic_id = context.research_topic.id
    project_bindings = project.manifest.active_topic_pixi_environment_bindings(topic_id)
    standalone_bindings = project.manifest.active_topic_standalone_pixi_bindings(topic_id)

    if not project_bindings and not standalone_bindings:
        checks.append(
            DoctorCheck(
                id="topic.pixi.binding.present",
                scope="topic",
                status="fail",
                concept="Topic Pixi environment binding",
                summary=(
                    "Selected Research Topic has no active Project Manifest Pixi binding; "
                    "no environment was inferred from topic or environment names."
                ),
                source_path=display_path(project.manifest_path, project.root),
            )
        )

    for index, binding in enumerate(project_bindings):
        check_id = f"topic.pixi.project-env.{index + 1}"
        if project_pixi_info is None:
            checks.append(
                DoctorCheck(
                    id=check_id,
                    scope="topic",
                    status="fail",
                    concept="Topic Pixi environment binding",
                    summary=(
                        f"Topic is bound to Project Pixi environment {binding.pixi_environment}, "
                        "but no Project-level Pixi manifest is available."
                    ),
                    source_path=display_path(project.manifest_path, project.root),
                    details=binding.to_json(),
                )
            )
        elif binding.pixi_environment in project_pixi_info.environments:
            checks.append(
                DoctorCheck(
                    id=check_id,
                    scope="topic",
                    status="pass",
                    concept="Topic Pixi environment binding",
                    summary=f"Project Pixi environment binding is declared: {binding.pixi_environment}.",
                    source_path=display_path(project_pixi_info.manifest_path, project.root),
                    details=binding.to_json(),
                )
            )
        else:
            checks.append(
                DoctorCheck(
                    id=check_id,
                    scope="topic",
                    status="fail",
                    concept="Topic Pixi environment binding",
                    summary=(
                        f"Project Manifest binds topic {topic_id} to Pixi environment {binding.pixi_environment}, "
                        "but that environment is not declared in the Project-level Pixi manifest."
                    ),
                    source_path=display_path(project_pixi_info.manifest_path, project.root),
                    details=binding.to_json(),
                )
            )

    for index, standalone_binding in enumerate(standalone_bindings):
        checks.extend(_standalone_binding_checks(context, standalone_binding.to_json(), index + 1))

    topic_payload: dict[str, object] = {
        "research_topic_id": topic_id,
        "context": context.to_json(),
        "project_pixi_environment_bindings": [binding.to_json() for binding in project_bindings],
        "standalone_pixi_bindings": [binding.to_json() for binding in standalone_bindings],
    }
    return topic_payload, checks, diagnostics


def find_project_pixi_manifest(project_root: Path) -> tuple[PixiManifestInfo | None, list[Diagnostic]]:
    pixi_toml = project_root / "pixi.toml"
    if pixi_toml.exists():
        return load_pixi_manifest(pixi_toml, project_root=project_root, require_pyproject_pixi=False)

    pyproject = project_root / "pyproject.toml"
    if pyproject.exists():
        return load_pixi_manifest(pyproject, project_root=project_root, require_pyproject_pixi=True)

    return None, []


def load_pixi_manifest(
    path: Path,
    *,
    project_root: Path,
    require_pyproject_pixi: bool,
) -> tuple[PixiManifestInfo | None, list[Diagnostic]]:
    raw, diagnostics = load_toml(path, "Pixi manifest")
    if raw is None:
        return None, diagnostics
    if path.name == "pyproject.toml":
        pixi_config = _dict_at(raw, ("tool", "pixi"))
        if require_pyproject_pixi and not pixi_config:
            return None, []
        if pixi_config is None:
            pixi_config = {}
        return _parse_pixi_info(path, "pyproject.toml", pixi_config, project_root)
    return _parse_pixi_info(path, "pixi.toml", raw, project_root)


def render_doctor_text(report: DoctorReport) -> list[str]:
    lines = [f"Doctor mode: {report.mode}", f"Mutated: {str(False).lower()}"]
    for scope in ("host", "project", "topic"):
        scoped_checks = [check for check in report.checks if check.scope == scope]
        if not scoped_checks:
            continue
        lines.append(scope.title())
        lines.extend(f"- [{check.status}] {check.id}: {check.summary}" for check in scoped_checks)
    return lines


def _project_manifest_validation_check(project: Project, diagnostics: list[Diagnostic]) -> DoctorCheck:
    error_count = sum(1 for diagnostic in diagnostics if diagnostic.is_error)
    warning_count = sum(1 for diagnostic in diagnostics if not diagnostic.is_error)
    if error_count:
        return DoctorCheck(
            id="project.manifest.validation",
            scope="project",
            status="fail",
            concept="Project Manifest",
            summary=f"Project Manifest validation reported {error_count} error(s) and {warning_count} warning(s).",
            source_path=display_path(project.manifest_path, project.root),
        )
    if warning_count:
        return DoctorCheck(
            id="project.manifest.validation",
            scope="project",
            status="warn",
            concept="Project Manifest",
            summary=f"Project Manifest validation reported {warning_count} warning(s).",
            source_path=display_path(project.manifest_path, project.root),
        )
    return DoctorCheck(
        id="project.manifest.validation",
        scope="project",
        status="pass",
        concept="Project Manifest",
        summary="Project Manifest and registered configs are valid.",
        source_path=display_path(project.manifest_path, project.root),
    )


def _requires_pixi_check(
    pixi: PixiHostInfo,
    pixi_info: PixiManifestInfo,
    project_root: Path,
    diagnostics: list[Diagnostic],
) -> DoctorCheck:
    if pixi_info.requires_pixi is None:
        return DoctorCheck(
            id="project.pixi.requires",
            scope="project",
            status="skip",
            concept="Pixi version requirement",
            summary="No requires-pixi constraint is declared in the Project-level Pixi manifest.",
            source_path=display_path(pixi_info.manifest_path, project_root),
        )
    if pixi.executable_path is None:
        return DoctorCheck(
            id="project.pixi.requires",
            scope="project",
            status="skip",
            concept="Pixi version requirement",
            summary="requires-pixi verification was skipped because the pixi executable is missing.",
            source_path=display_path(pixi_info.manifest_path, project_root),
            details={"requires_pixi": pixi_info.requires_pixi},
        )
    command = [
        pixi.executable_path,
        "workspace",
        "requires-pixi",
        "verify",
        "--manifest-path",
        str(pixi_info.manifest_path),
    ]
    result, error = _run_command(command)
    if error is not None:
        diagnostics.append(
            Diagnostic(
                code="ISO031",
                severity="error",
                concept="Pixi version requirement",
                path=pixi_info.manifest_path,
                message=f"requires-pixi verification failed: {error}.",
            )
        )
        return DoctorCheck(
            id="project.pixi.requires",
            scope="project",
            status="fail",
            concept="Pixi version requirement",
            summary=f"requires-pixi verification failed: {error}.",
            source_path=display_path(pixi_info.manifest_path, project_root),
            details={"requires_pixi": pixi_info.requires_pixi},
        )
    assert result is not None
    if result.returncode != 0:
        message = _command_failure_summary(result)
        diagnostics.append(
            Diagnostic(
                code="ISO031",
                severity="error",
                concept="Pixi version requirement",
                path=pixi_info.manifest_path,
                message=f"requires-pixi verification failed: {message}.",
            )
        )
        return DoctorCheck(
            id="project.pixi.requires",
            scope="project",
            status="fail",
            concept="Pixi version requirement",
            summary=f"requires-pixi verification failed: {message}.",
            source_path=display_path(pixi_info.manifest_path, project_root),
            details={"requires_pixi": pixi_info.requires_pixi},
        )
    return DoctorCheck(
        id="project.pixi.requires",
        scope="project",
        status="pass",
        concept="Pixi version requirement",
        summary="requires-pixi constraint is satisfied by the available pixi executable.",
        source_path=display_path(pixi_info.manifest_path, project_root),
        details={"requires_pixi": pixi_info.requires_pixi},
    )


def _standalone_binding_checks(
    context: EffectiveTopicContext,
    binding: dict[str, object],
    index: int,
) -> list[DoctorCheck]:
    project = context.project
    manifest_path_value = binding.get("manifest_path")
    env_value = binding.get("pixi_environment")
    manifest_path_input = manifest_path_value if isinstance(manifest_path_value, str) else ""
    pixi_environment = env_value if isinstance(env_value, str) and env_value else None
    check_id = f"topic.pixi.standalone.{index}"
    standalone_path = resolve_project_path(project.root, manifest_path_input)
    if not is_within(standalone_path, project.root):
        return [
            DoctorCheck(
                id=check_id,
                scope="topic",
                status="fail",
                concept="Standalone Pixi isolation",
                summary="Standalone Pixi manifest path resolves outside the Project root.",
                source_path=manifest_path_input,
                details=binding,
            )
        ]
    if not standalone_path.exists():
        return [
            DoctorCheck(
                id=check_id,
                scope="topic",
                status="fail",
                concept="Standalone Pixi isolation",
                summary="Standalone Pixi manifest does not exist.",
                source_path=display_path(standalone_path, project.root),
                details=binding,
            )
        ]

    standalone_info, diagnostics = load_pixi_manifest(
        standalone_path,
        project_root=project.root,
        require_pyproject_pixi=standalone_path.name == "pyproject.toml",
    )
    if diagnostics or standalone_info is None:
        return [
            DoctorCheck(
                id=check_id,
                scope="topic",
                status="fail",
                concept="Standalone Pixi isolation",
                summary="Standalone Pixi manifest exists but could not be parsed as Pixi configuration.",
                source_path=display_path(standalone_path, project.root),
                details=binding,
            )
        ]
    if pixi_environment is None:
        return [
            DoctorCheck(
                id=check_id,
                scope="topic",
                status="pass",
                concept="Standalone Pixi isolation",
                summary="Standalone Pixi manifest exists for the selected Research Topic.",
                source_path=display_path(standalone_path, project.root),
                details=binding,
            )
        ]
    if pixi_environment in standalone_info.environments:
        return [
            DoctorCheck(
                id=check_id,
                scope="topic",
                status="pass",
                concept="Standalone Pixi isolation",
                summary=f"Standalone Pixi environment binding is declared: {pixi_environment}.",
                source_path=display_path(standalone_path, project.root),
                details=binding,
            )
        ]
    return [
        DoctorCheck(
            id=check_id,
            scope="topic",
            status="fail",
            concept="Standalone Pixi isolation",
            summary=(
                f"Standalone Pixi binding names environment {pixi_environment}, "
                "but that environment is not declared in the standalone manifest."
            ),
            source_path=display_path(standalone_path, project.root),
            details=binding,
        )
    ]


def _parse_pixi_info(
    path: Path,
    manifest_kind: str,
    config: dict[str, Any],
    project_root: Path,
) -> tuple[PixiManifestInfo | None, list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    environments = {"default"}
    env_table = _dict_value(config.get("environments"))
    if env_table is None:
        diagnostics.append(
            Diagnostic(
                code="ISO032",
                severity="error",
                concept="Pixi manifest",
                path=path,
                field="environments",
                message="Pixi environments must be declared as a TOML table.",
            )
        )
    else:
        environments.update(str(name) for name in env_table)
    workspace = _dict_value(config.get("workspace")) or {}
    requires_pixi_value = workspace.get("requires-pixi")
    requires_pixi = requires_pixi_value if isinstance(requires_pixi_value, str) and requires_pixi_value else None
    info = PixiManifestInfo(
        manifest_path=path,
        manifest_kind=manifest_kind,
        environments=sorted(environments),
        requires_pixi=requires_pixi,
    )
    if not is_within(path, project_root):
        diagnostics.append(
            Diagnostic(
                code="ISO005",
                severity="error",
                concept="Pixi manifest",
                path=path,
                message="Pixi manifest path resolves outside the Project root.",
            )
        )
    return info, diagnostics


def _dict_at(data: dict[str, Any], keys: tuple[str, ...]) -> dict[str, Any] | None:
    current: object = data
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current if isinstance(current, dict) else None


def _dict_value(value: object) -> dict[str, Any] | None:
    if value is None:
        return {}
    if isinstance(value, dict):
        return value
    return None


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
