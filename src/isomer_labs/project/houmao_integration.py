"""Project-scoped Houmao integration policy and skill projection helpers."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import shutil
from typing import Mapping

import tomlkit

from isomer_labs.core.diagnostics import Diagnostic, has_errors
from isomer_labs.core.path_utils import canonicalize, display_path, is_within, resolve_project_path
from isomer_labs.houmao.manifests import file_digest
from isomer_labs.models import EffectiveTopicContext, HoumaoIntegrationPolicy, Project
from isomer_labs.project import (
    config_dir_for_root,
    houmao_project_dir_for_root,
    houmao_skill_projection_dir_for_root,
)
from isomer_labs.project.topic_service_master import topic_service_master_identity_for_context


HOUMAO_SKILL_PROJECTION_SCHEMA_VERSION = "isomer-houmao-skill-projection.v1"
PROJECTION_MANIFEST_FILENAME = "projection-manifest.json"
PROJECTION_METADATA_FILENAME = ".isomer-projection.json"
ROUTE_NAME_RE = re.compile(r"^[a-z][a-z0-9-]*$")

TOPIC_SERVICE_MASTER_ROUTES = (
    "prepare-topic-service-master",
    "launch-topic-service-master",
    "inspect-topic-service-master",
    "stop-topic-service-master",
    "repair-topic-service-master",
)

ROUTE_DEPENDENCY_SKILLS: dict[str, tuple[str, ...]] = {
    "prepare-topic-service-master": (
        "houmao-project-mgr",
        "houmao-credential-mgr",
        "houmao-agent-definition",
        "houmao-utils-workspace-mgr",
    ),
    "launch-topic-service-master": (
        "houmao-agent-instance",
        "houmao-agent-definition",
        "houmao-agent-gateway",
        "houmao-mailbox-mgr",
    ),
    "inspect-topic-service-master": (
        "houmao-agent-inspect",
        "houmao-agent-messaging",
        "houmao-agent-email-comms",
    ),
    "stop-topic-service-master": (
        "houmao-agent-instance",
        "houmao-agent-gateway",
        "houmao-agent-messaging",
    ),
    "repair-topic-service-master": (
        "houmao-project-mgr",
        "houmao-agent-definition",
        "houmao-agent-instance",
        "houmao-utils-workspace-mgr",
        "houmao-mailbox-mgr",
        "houmao-agent-gateway",
    ),
}


@dataclass(frozen=True)
class HoumaoIntegrationState:
    integration_status: str
    skill_root_input: str
    project_dir_input: str
    skill_root_path: Path
    houmao_project_path: Path
    houmao_overlay_path: Path
    diagnostics: tuple[Diagnostic, ...]

    @property
    def ok(self) -> bool:
        return not has_errors(list(self.diagnostics))

    @property
    def skipped(self) -> bool:
        return self.integration_status == "disabled"

    @property
    def skip_reason(self) -> str | None:
        if self.integration_status == "disabled":
            return "Project Manifest disables Houmao integration."
        if self.integration_status == "not_configured":
            return "Project Manifest has no operator.integrations.houmao policy."
        return None

    @property
    def next_action(self) -> str | None:
        if self.integration_status == "not_configured":
            return "Run `isomer-cli project integrations houmao enable` or `isomer-cli project integrations houmao disable`."
        if self.integration_status == "enabled":
            return "Run `isomer-cli project integrations houmao prepare-skills` to refresh projected Houmao support skills."
        return None

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "integration_status": self.integration_status,
            "skill_root": self.skill_root_input,
            "project_dir": self.project_dir_input,
            "houmao_skill_root": str(self.skill_root_path),
            "houmao_project_path": str(self.houmao_project_path),
            "houmao_overlay_path": str(self.houmao_overlay_path),
            "skip_reason": self.skip_reason,
            "next_action": self.next_action,
            "diagnostics": [diagnostic.to_json() for diagnostic in self.diagnostics],
        }
        return data


@dataclass(frozen=True)
class HoumaoIntegrationCommandResult:
    ok: bool
    mutated: bool
    project_root: Path
    state: HoumaoIntegrationState
    diagnostics: tuple[Diagnostic, ...]
    projection_manifest_path: Path | None = None
    projected_routes: tuple[str, ...] = ()

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "ok": self.ok,
            "mutated": self.mutated,
            "project_root": str(self.project_root),
            **self.state.to_json(),
            "projected_routes": list(self.projected_routes),
        }
        if self.projection_manifest_path is not None:
            data["projection_manifest_path"] = str(self.projection_manifest_path)
        data["diagnostics"] = [diagnostic.to_json() for diagnostic in self.diagnostics]
        return data


@dataclass(frozen=True)
class HoumaoSkillContextResult:
    ok: bool
    mutated: bool
    project_root: Path
    integration_status: str
    skill_name: str
    diagnostics: tuple[Diagnostic, ...]
    houmao_skill_path: Path | None = None
    houmao_project_path: Path | None = None
    houmao_overlay_path: Path | None = None
    topic_context: EffectiveTopicContext | None = None
    topic_service_master: dict[str, object] | None = None
    skip_reason: str | None = None
    next_action: str | None = None

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "ok": self.ok,
            "mutated": self.mutated,
            "project_root": str(self.project_root),
            "integration_status": self.integration_status,
            "skill_name": self.skill_name,
            "houmao_skill_path": str(self.houmao_skill_path) if self.houmao_skill_path is not None else None,
            "houmao_project_path": str(self.houmao_project_path) if self.houmao_project_path is not None else None,
            "houmao_overlay_path": str(self.houmao_overlay_path) if self.houmao_overlay_path is not None else None,
            "skip_reason": self.skip_reason,
            "next_action": self.next_action,
            "instructions": self.instructions,
            "diagnostics": [diagnostic.to_json() for diagnostic in self.diagnostics],
        }
        if self.topic_context is not None:
            data["research_topic_id"] = self.topic_context.research_topic.id
            data["topic_workspace_id"] = self.topic_context.topic_workspace_id
            data["topic_workspace_path"] = str(self.topic_context.topic_workspace_path)
        if self.topic_service_master is not None:
            data["topic_service_master"] = self.topic_service_master
        return data

    @property
    def instructions(self) -> str | None:
        if self.houmao_skill_path is None or self.houmao_project_path is None:
            return None
        return (
            "Read houmao_skill_path. Run Houmao commands with "
            f"--project-dir {self.houmao_project_path}. Do not rely on implicit .houmao discovery from cwd."
        )


def houmao_integration_state(project: Project) -> HoumaoIntegrationState:
    policy = project.manifest.houmao_integration
    status = "not_configured"
    skill_root_input = ".isomer-labs/houmao-skills"
    project_dir_input = ".isomer-labs"
    if policy is not None:
        status = policy.status
        skill_root_input = policy.skill_root_input or skill_root_input
        project_dir_input = policy.project_dir_input or project_dir_input

    skill_root_path = resolve_project_path(project.root, skill_root_input)
    houmao_project_path = resolve_project_path(project.root, project_dir_input)
    houmao_overlay_path = houmao_project_path / ".houmao"
    diagnostics = _integration_path_diagnostics(
        project,
        status=status,
        skill_root_input=skill_root_input,
        skill_root_path=skill_root_path,
        project_dir_input=project_dir_input,
        houmao_project_path=houmao_project_path,
    )
    return HoumaoIntegrationState(
        integration_status=status,
        skill_root_input=skill_root_input,
        project_dir_input=project_dir_input,
        skill_root_path=skill_root_path,
        houmao_project_path=houmao_project_path,
        houmao_overlay_path=houmao_overlay_path,
        diagnostics=tuple(diagnostics),
    )


def set_houmao_integration_policy(project: Project, status: str) -> HoumaoIntegrationCommandResult:
    if status not in {"enabled", "disabled"}:
        diagnostic = Diagnostic(
            code="ISO003",
            severity="error",
            concept="Project Houmao integration",
            field="status",
            message="Houmao integration status must be enabled or disabled.",
        )
        state = houmao_integration_state(project)
        return HoumaoIntegrationCommandResult(False, False, project.root, state, (diagnostic,))

    previous = project.manifest.houmao_integration
    skill_root = previous.skill_root_input if previous is not None and previous.skill_root_input else ".isomer-labs/houmao-skills"
    project_dir = previous.project_dir_input if previous is not None and previous.project_dir_input else ".isomer-labs"
    mutated = previous is None or previous.status != status or previous.skill_root_input != skill_root or previous.project_dir_input != project_dir
    if mutated:
        _write_houmao_integration_policy(project.manifest_path, status, skill_root=skill_root, project_dir=project_dir)
    next_policy = HoumaoIntegrationPolicy(status=status, skill_root_input=skill_root, project_dir_input=project_dir, source_path=project.manifest_path)
    next_project = _project_with_policy(project, next_policy)
    state = houmao_integration_state(next_project)
    diagnostics = tuple(state.diagnostics)
    return HoumaoIntegrationCommandResult(not has_errors(list(diagnostics)), mutated, project.root, state, diagnostics)


def prepare_houmao_skills(project: Project, *, env: Mapping[str, str] | None = None) -> HoumaoIntegrationCommandResult:
    state = houmao_integration_state(project)
    diagnostics = list(state.diagnostics)
    if state.integration_status == "disabled":
        return HoumaoIntegrationCommandResult(True, False, project.root, state, tuple(diagnostics))
    if state.integration_status == "not_configured":
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="Project Houmao integration",
                message="Houmao integration is not configured for this Project.",
                hint="Run `isomer-cli project integrations houmao enable` or `isomer-cli project integrations houmao disable`.",
            )
        )
        return HoumaoIntegrationCommandResult(False, False, project.root, state, tuple(diagnostics))
    if has_errors(diagnostics):
        return HoumaoIntegrationCommandResult(False, False, project.root, state, tuple(diagnostics))

    source_root = discover_houmao_system_skills_source(project.root, env=env)
    if source_root is None:
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="Houmao system skill projection",
                message="Could not locate Houmao packaged system skills for projection.",
                hint="Set ISOMER_HOUMAO_SYSTEM_SKILLS_SOURCE to a directory containing Houmao system skill folders.",
            )
        )
        return HoumaoIntegrationCommandResult(False, False, project.root, state, tuple(diagnostics))

    before = _projection_digest(state.skill_root_path)
    state.skill_root_path.mkdir(parents=True, exist_ok=True)
    dependency_root = state.skill_root_path / "houmao-system-skills"
    all_dependencies = tuple(sorted({skill for skills in ROUTE_DEPENDENCY_SKILLS.values() for skill in skills}))
    for skill_name in all_dependencies:
        source = source_root / skill_name
        if not source.joinpath("SKILL.md").is_file():
            diagnostics.append(
                Diagnostic(
                    code="ISO103",
                    severity="error",
                    concept="Houmao system skill projection",
                    path=source,
                    field=skill_name,
                    message="Required Houmao system skill source is missing.",
                )
            )
            continue
        try:
            _copy_managed_directory(
                source,
                dependency_root / skill_name,
                source_kind="houmao-system-skill",
                source_ref=str(source),
            )
        except ValueError as exc:
            diagnostics.append(
                Diagnostic(
                    code="ISO005",
                    severity="error",
                    concept="Houmao system skill projection",
                    path=dependency_root / skill_name,
                    field=skill_name,
                    message=str(exc),
                )
            )
    if has_errors(diagnostics):
        return HoumaoIntegrationCommandResult(False, False, project.root, state, tuple(diagnostics))

    routes: dict[str, dict[str, object]] = {}
    for route_name in TOPIC_SERVICE_MASTER_ROUTES:
        route_dir = state.skill_root_path / route_name
        try:
            _write_route_skill(route_dir, route_name, ROUTE_DEPENDENCY_SKILLS[route_name])
        except ValueError as exc:
            diagnostics.append(
                Diagnostic(
                    code="ISO005",
                    severity="error",
                    concept="Houmao system skill projection",
                    path=route_dir,
                    field=route_name,
                    message=str(exc),
                )
            )
            continue
        routes[route_name] = {
            "skill_dir": route_name,
            "skill_file": f"{route_name}/SKILL.md",
            "dependencies": [f"houmao-system-skills/{skill}" for skill in ROUTE_DEPENDENCY_SKILLS[route_name]],
        }
    if has_errors(diagnostics):
        return HoumaoIntegrationCommandResult(False, False, project.root, state, tuple(diagnostics))

    manifest = {
        "schema_version": HOUMAO_SKILL_PROJECTION_SCHEMA_VERSION,
        "owner": "isomer-labs",
        "projection_root": str(state.skill_root_path),
        "houmao_project_path": str(state.houmao_project_path),
        "routes": routes,
    }
    manifest_path = state.skill_root_path / PROJECTION_MANIFEST_FILENAME
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    after = _projection_digest(state.skill_root_path)
    return HoumaoIntegrationCommandResult(
        True,
        before != after,
        project.root,
        state,
        tuple(diagnostics),
        projection_manifest_path=manifest_path,
        projected_routes=TOPIC_SERVICE_MASTER_ROUTES,
    )


def resolve_houmao_skill_context(
    project: Project,
    skill_name: str,
    *,
    topic_context: EffectiveTopicContext | None = None,
) -> HoumaoSkillContextResult:
    state = houmao_integration_state(project)
    diagnostics = list(state.diagnostics)
    if not ROUTE_NAME_RE.match(skill_name):
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="Houmao skill context",
                field="skill_name",
                message=f"Unknown Houmao skill route: {skill_name}.",
            )
        )
        return HoumaoSkillContextResult(False, False, project.root, state.integration_status, skill_name, tuple(diagnostics))
    if state.integration_status in {"disabled", "not_configured"}:
        ok = state.integration_status == "disabled"
        topic_service_master = None
        if topic_context is not None:
            topic_service_master, identity_diagnostics = topic_service_master_identity_for_context(topic_context)
            diagnostics.extend(identity_diagnostics)
        return HoumaoSkillContextResult(
            ok,
            False,
            project.root,
            state.integration_status,
            skill_name,
            tuple(diagnostics),
            topic_context=topic_context,
            topic_service_master=topic_service_master,
            skip_reason=state.skip_reason,
            next_action=state.next_action,
        )
    if has_errors(diagnostics):
        return HoumaoSkillContextResult(False, False, project.root, state.integration_status, skill_name, tuple(diagnostics))

    manifest_path = state.skill_root_path / PROJECTION_MANIFEST_FILENAME
    manifest = _load_projection_manifest(manifest_path, diagnostics)
    if manifest is None:
        return HoumaoSkillContextResult(False, False, project.root, state.integration_status, skill_name, tuple(diagnostics), next_action=state.next_action)
    routes = manifest.get("routes")
    route = routes.get(skill_name) if isinstance(routes, dict) else None
    if not isinstance(route, dict):
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="Houmao skill context",
                field="skill_name",
                message=f"Unknown Houmao skill route: {skill_name}.",
            )
        )
        return HoumaoSkillContextResult(False, False, project.root, state.integration_status, skill_name, tuple(diagnostics))
    skill_file = route.get("skill_file")
    if not isinstance(skill_file, str) or not skill_file:
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="Houmao skill context",
                path=manifest_path,
                field=f"routes.{skill_name}.skill_file",
                message="Projection manifest route does not declare a skill_file.",
            )
        )
        return HoumaoSkillContextResult(False, False, project.root, state.integration_status, skill_name, tuple(diagnostics))
    skill_path = canonicalize(state.skill_root_path / skill_file)
    if not is_within(skill_path, state.skill_root_path) or skill_path.name != "SKILL.md":
        diagnostics.append(
            Diagnostic(
                code="ISO005",
                severity="error",
                concept="Houmao skill context",
                path=skill_path,
                field=f"routes.{skill_name}.skill_file",
                message="Projection manifest route resolves outside the Houmao skill projection root.",
            )
        )
        return HoumaoSkillContextResult(False, False, project.root, state.integration_status, skill_name, tuple(diagnostics))
    if not skill_path.is_file():
        diagnostics.append(
            Diagnostic(
                code="ISO001",
                severity="error",
                concept="Houmao skill context",
                path=skill_path,
                field=f"routes.{skill_name}.skill_file",
                message="Projected Houmao skill route file does not exist.",
            )
        )
        return HoumaoSkillContextResult(False, False, project.root, state.integration_status, skill_name, tuple(diagnostics))
    topic_service_master = None
    if topic_context is not None:
        topic_service_master, identity_diagnostics = topic_service_master_identity_for_context(topic_context)
        diagnostics.extend(identity_diagnostics)
    return HoumaoSkillContextResult(
        True,
        False,
        project.root,
        state.integration_status,
        skill_name,
        tuple(diagnostics),
        houmao_skill_path=skill_path,
        houmao_project_path=state.houmao_project_path,
        houmao_overlay_path=state.houmao_overlay_path,
        topic_context=topic_context,
        topic_service_master=topic_service_master,
    )


def discover_houmao_system_skills_source(
    project_root: Path,
    *,
    env: Mapping[str, str] | None = None,
) -> Path | None:
    environment = dict(os.environ if env is None else env)
    candidates: list[Path] = []
    configured = environment.get("ISOMER_HOUMAO_SYSTEM_SKILLS_SOURCE")
    if configured:
        candidates.append(Path(configured))
    checkout = environment.get("ISOMER_HOUMAO_CHECKOUT")
    if checkout:
        candidates.append(Path(checkout) / "src" / "houmao" / "agents" / "assets" / "system_skills")
    candidates.extend(
        [
            project_root / "extern" / "orphan" / "houmao" / "src" / "houmao" / "agents" / "assets" / "system_skills",
            Path.home() / "workspace" / "code" / "houmao" / "src" / "houmao" / "agents" / "assets" / "system_skills",
        ]
    )
    for candidate in candidates:
        root = canonicalize(candidate)
        if root.joinpath("catalog.toml").is_file() and root.joinpath("houmao-agent-definition", "SKILL.md").is_file():
            return root
    return None


def _integration_path_diagnostics(
    project: Project,
    *,
    status: str,
    skill_root_input: str,
    skill_root_path: Path,
    project_dir_input: str,
    houmao_project_path: Path,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    config_dir = config_dir_for_root(project.root)
    if status not in {"enabled", "disabled", "not_configured"}:
        diagnostics.append(
            Diagnostic(
                code="ISO003",
                severity="error",
                concept="Project Houmao integration",
                path=project.manifest_path,
                field="operator.integrations.houmao.status",
                message="Houmao integration status must be enabled or disabled.",
            )
        )
    if not is_within(skill_root_path, config_dir):
        diagnostics.append(
            Diagnostic(
                code="ISO005",
                severity="error",
                concept="Project Houmao integration",
                path=skill_root_path,
                field="operator.integrations.houmao.skill_root",
                message="Houmao skill projection root must resolve inside the Project Config Directory.",
                hint=f"Use a Project-relative path such as {display_path(houmao_skill_projection_dir_for_root(project.root), project.root)}.",
            )
        )
    if not is_within(houmao_project_path, config_dir):
        diagnostics.append(
            Diagnostic(
                code="ISO005",
                severity="error",
                concept="Project Houmao integration",
                path=houmao_project_path,
                field="operator.integrations.houmao.project_dir",
                message="Houmao Project directory must resolve inside the Project Config Directory.",
                hint=f"Use a Project-relative path such as {display_path(houmao_project_dir_for_root(project.root), project.root)}.",
            )
        )
    if skill_root_input.endswith("/.houmao") or project_dir_input.endswith("/houmao-skills"):
        diagnostics.append(
            Diagnostic(
                code="ISO005",
                severity="error",
                concept="Project Houmao integration",
                path=project.manifest_path,
                field="operator.integrations.houmao",
                message="Houmao skill projection and Houmao Project overlay paths must stay separate.",
            )
        )
    return diagnostics


def _write_houmao_integration_policy(manifest_path: Path, status: str, *, skill_root: str, project_dir: str) -> None:
    document = tomlkit.parse(manifest_path.read_text(encoding="utf-8"))
    operator = document.get("operator")
    if not isinstance(operator, dict):
        operator = tomlkit.table()
        document["operator"] = operator
    integrations = operator.get("integrations")
    if not isinstance(integrations, dict):
        integrations = tomlkit.table()
        operator["integrations"] = integrations
    houmao = integrations.get("houmao")
    if not isinstance(houmao, dict):
        houmao = tomlkit.table()
        integrations["houmao"] = houmao
    houmao["status"] = status
    houmao["skill_root"] = skill_root
    houmao["project_dir"] = project_dir
    manifest_path.write_text(tomlkit.dumps(document), encoding="utf-8")


def _project_with_policy(project: Project, policy: HoumaoIntegrationPolicy) -> Project:
    from dataclasses import replace

    return replace(project, manifest=replace(project.manifest, houmao_integration=policy))


def _copy_managed_directory(source: Path, target: Path, *, source_kind: str, source_ref: str) -> None:
    _ensure_managed_target(target)
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target)
    _write_projection_metadata(target, source_kind=source_kind, source_ref=source_ref)


def _write_route_skill(route_dir: Path, route_name: str, dependencies: tuple[str, ...]) -> None:
    _ensure_managed_target(route_dir)
    if route_dir.exists():
        shutil.rmtree(route_dir)
    route_dir.mkdir(parents=True, exist_ok=True)
    dependency_lines = "\n".join(f"- `houmao-system-skills/{skill}/SKILL.md`" for skill in dependencies)
    route_dir.joinpath("SKILL.md").write_text(
        f"""---
name: {route_name}
description: Isomer-projected Houmao procedure route for Topic Service Master lifecycle work.
---

# {route_name}

This projected route is internal Isomer support material. Use it only after `isomer-cli project integrations houmao skill-context {route_name}` returns this `houmao_skill_path`.

## Required Context

- Read the Isomer-provided `houmao_project_path` and pass it explicitly to Houmao commands with `--project-dir <houmao_project_path>`.
- Do not rely on implicit `.houmao/` discovery from the Topic Workspace cwd.
- Preserve Isomer terms for Project, Topic Workspace, Topic Actor, and Topic Service Master in user-facing output.

## Houmao Procedure Skills

Follow the relevant Houmao-owned skill material projected beside this route:

{dependency_lines}

## Output

Return Topic Service Master readiness, blockers, commands used or recommended, and any support Artifact refs. Do not store credentials in the output.
""",
        encoding="utf-8",
    )
    _write_projection_metadata(route_dir, source_kind="isomer-houmao-route", source_ref=route_name)


def _ensure_managed_target(target: Path) -> None:
    if not target.exists():
        return
    metadata_path = target / PROJECTION_METADATA_FILENAME
    if not metadata_path.is_file():
        raise ValueError(f"Refusing to overwrite unmanaged Houmao skill projection path: {target}")
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Refusing to overwrite projection path with invalid ownership metadata: {target}") from exc
    if metadata.get("owner") != "isomer-labs" or metadata.get("schema_version") != HOUMAO_SKILL_PROJECTION_SCHEMA_VERSION:
        raise ValueError(f"Refusing to overwrite unmanaged Houmao skill projection path: {target}")


def _write_projection_metadata(target: Path, *, source_kind: str, source_ref: str) -> None:
    metadata = {
        "schema_version": HOUMAO_SKILL_PROJECTION_SCHEMA_VERSION,
        "owner": "isomer-labs",
        "source_kind": source_kind,
        "source_ref": source_ref,
    }
    target.joinpath(PROJECTION_METADATA_FILENAME).write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _load_projection_manifest(path: Path, diagnostics: list[Diagnostic]) -> dict[str, object] | None:
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        diagnostics.append(
            Diagnostic(
                code="ISO001",
                severity="error",
                concept="Houmao skill projection manifest",
                path=path,
                message="Projection manifest does not exist.",
                hint="Run `isomer-cli project integrations houmao prepare-skills`.",
            )
        )
        return None
    except json.JSONDecodeError as exc:
        diagnostics.append(
            Diagnostic(
                code="ISO002",
                severity="error",
                concept="Houmao skill projection manifest",
                path=path,
                message=f"Projection manifest JSON is malformed: {exc}.",
            )
        )
        return None
    if not isinstance(manifest, dict) or manifest.get("schema_version") != HOUMAO_SKILL_PROJECTION_SCHEMA_VERSION:
        diagnostics.append(
            Diagnostic(
                code="ISO003",
                severity="error",
                concept="Houmao skill projection manifest",
                path=path,
                message="Projection manifest schema is unsupported.",
            )
        )
        return None
    return manifest


def _projection_digest(root: Path) -> str | None:
    if not root.exists():
        return None
    digest = sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(str(path.relative_to(root)).encode("utf-8"))
        digest.update(file_digest(path).encode("utf-8"))
    return digest.hexdigest()
