"""Domain Agent Team Template discovery and validation."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import subprocess
from typing import Any

from isomer_labs.diagnostics import Diagnostic, has_errors
from isomer_labs.models import (
    DOMAIN_AGENT_TEAM_TEMPLATE_REF_SCHEMA_VERSION,
    AgentRoleDefinition,
    DomainAgentTeamTemplate,
    DomainAgentTeamTemplateRegistration,
    Project,
    TemplateArtifact,
    TemplateParameter,
    TemplateValidationReport,
    WorkflowStageRoute,
)
from isomer_labs.path_utils import canonicalize, is_within, resolve_project_path
from isomer_labs.toml_loader import load_toml


BUILT_IN_DEEPSCI_ORG_ID = "deepsci-org"
BUILT_IN_DEEPSCI_MINI_ID = "deepsci-mini"
EXPECTED_DEEPSCI_ORG_ROLES = (
    "deepsci-org-master",
    "deepsci-org-framer",
    "deepsci-org-designer",
    "deepsci-org-experimenter",
    "deepsci-org-analyzer",
    "deepsci-org-publisher",
    "deepsci-org-reviewer",
)
EXPECTED_DEEPSCI_MINI_ROLES = (
    "deepsci-mini-lead",
    "deepsci-mini-scout",
    "deepsci-mini-synth-reviewer",
)
SCALABLE_DEEPSCI_ORG_ROLES = {"deepsci-org-experimenter", "deepsci-org-analyzer"}
_REPO_ROOT = Path(__file__).resolve().parents[2]
_BUILT_IN_DEEPSCI_ORG_SOURCE = _REPO_ROOT / "teams" / "deepsci-org" / "execplan"
_BUILT_IN_DEEPSCI_MINI_SOURCE = _REPO_ROOT / "teams" / "deepsci-mini" / "execplan"

_BOUNDARY_KEYS = {
    "research_topic_id",
    "topic_workspace_id",
    "topic_workspace_ref",
    "workspace_runtime_ref",
    "topic_agent_team_profile_id",
    "agent_team_instance_id",
    "agent_instance_id",
    "adapter_launch_ref",
    "houmao_launch_ref",
    "houmao_managed_agent_id",
    "launch_dossier_ref",
    "mailbox",
    "mailbox_ref",
    "mailbox_state",
    "gateway",
    "gateway_ref",
    "gateway_state",
    "credential",
    "credential_ref",
    "launch_ref",
    "run_id",
    "run_status",
    "command_output",
    "command_outputs",
    "live_process_id",
    "provider_payload",
}


@dataclass(frozen=True)
class SourceDocument:
    path: Path
    data: dict[str, Any]


def built_in_deepsci_org_registration() -> DomainAgentTeamTemplateRegistration:
    return DomainAgentTeamTemplateRegistration(
        id=BUILT_IN_DEEPSCI_ORG_ID,
        source_path_input=str(_BUILT_IN_DEEPSCI_ORG_SOURCE),
        source_kind="built-in",
        schema_version=DOMAIN_AGENT_TEAM_TEMPLATE_REF_SCHEMA_VERSION,
        status="active",
        source_path=_BUILT_IN_DEEPSCI_ORG_SOURCE,
    )


def built_in_deepsci_mini_registration() -> DomainAgentTeamTemplateRegistration:
    return DomainAgentTeamTemplateRegistration(
        id=BUILT_IN_DEEPSCI_MINI_ID,
        source_path_input=str(_BUILT_IN_DEEPSCI_MINI_SOURCE),
        source_kind="built-in",
        schema_version=DOMAIN_AGENT_TEAM_TEMPLATE_REF_SCHEMA_VERSION,
        status="active",
        source_path=_BUILT_IN_DEEPSCI_MINI_SOURCE,
    )


def discover_domain_agent_team_templates(project: Project | None = None) -> list[DomainAgentTeamTemplateRegistration]:
    registrations = [built_in_deepsci_org_registration(), built_in_deepsci_mini_registration()]
    if project is None:
        return registrations
    seen = {BUILT_IN_DEEPSCI_ORG_ID, BUILT_IN_DEEPSCI_MINI_ID}
    for registration in project.manifest.domain_agent_team_templates:
        if registration.status == "archived":
            continue
        if registration.id in seen:
            continue
        seen.add(registration.id)
        registrations.append(registration)
    return registrations


def find_domain_agent_team_template(
    template_id: str,
    project: Project | None = None,
) -> DomainAgentTeamTemplateRegistration | None:
    return next(
        (registration for registration in discover_domain_agent_team_templates(project) if registration.id == template_id),
        None,
    )


def resolve_template_source_path(project: Project | None, registration: DomainAgentTeamTemplateRegistration) -> Path:
    if registration.source_kind == "built-in" or (
        registration.id in {BUILT_IN_DEEPSCI_ORG_ID, BUILT_IN_DEEPSCI_MINI_ID}
        and registration.source_path_input is None
    ):
        return canonicalize(registration.source_path)
    if registration.source_path_input is None:
        return canonicalize(registration.source_path)
    if project is None:
        return canonicalize(Path(registration.source_path_input))
    return resolve_project_path(project.root, registration.source_path_input)


def validate_domain_agent_team_template(
    project: Project | None,
    registration: DomainAgentTeamTemplateRegistration,
    *,
    include_harness: bool = True,
) -> TemplateValidationReport:
    diagnostics: list[Diagnostic] = []
    source_path = resolve_template_source_path(project, registration)
    if registration.source_kind != "built-in" and project is not None and not is_within(source_path, project.root):
        diagnostics.append(
            Diagnostic(
                code="ISO016",
                severity="error",
                concept="Domain Agent Team Template",
                path=registration.source_path,
                field="source_path",
                message="Domain Agent Team Template source path resolves outside the Project root.",
            )
        )
        return TemplateValidationReport(registration.id, source_path, False, diagnostics, None)

    manifest = _load_execplan_toml(source_path, "manifest.toml", "Domain Agent Team Template manifest", diagnostics)
    participants = _load_execplan_toml(
        source_path,
        "specs/participants/participants.toml",
        "Domain Agent Team Template participant contract",
        diagnostics,
    )
    bindings = _load_execplan_toml(source_path, "agents/bindings.toml", "Domain Agent Team Template bindings", diagnostics)
    parameters = _load_execplan_toml(
        source_path,
        "harness/refs/instantiation-parameters.toml",
        "Domain Agent Team Template parameters",
        diagnostics,
    )
    workspace_contract = _load_execplan_toml(
        source_path,
        "specs/workspace/workspace.toml",
        "Domain Agent Team Template workspace contract",
        diagnostics,
    )
    _load_execplan_json(
        source_path,
        "harness/schemas/topic-profile-instantiation.schema.json",
        "Topic Agent Team Profile instantiation schema",
        diagnostics,
    )

    for document in (manifest, participants, bindings, parameters, workspace_contract):
        if document is not None:
            _scan_template_boundary(document.data, document.path, (), diagnostics)

    required_files = (
        "manifest.toml",
        "specs/participants/participants.toml",
        "agents/bindings.toml",
        "harness/refs/instantiation-parameters.toml",
        "harness/schemas/topic-profile-instantiation.schema.json",
        "specs/workspace/workspace.toml",
        "specs/state/schema.sql",
        "specs/run/run-contract.md",
    )
    for relative in required_files:
        _require_path(source_path, relative, "Domain Agent Team Template artifact", diagnostics)

    artifacts = _parse_artifacts(source_path, manifest.data if manifest is not None else {}, diagnostics)
    roles = _parse_roles(participants.data if participants is not None else {}, bindings.data if bindings is not None else {}, source_path, diagnostics)
    stage_routes = _parse_stage_routes(participants.data if participants is not None else {}, diagnostics)
    template_parameters = _parse_parameters(parameters.data if parameters is not None else {})

    if manifest is not None:
        _validate_manifest_metadata(registration, manifest, diagnostics)
    _validate_deepsci_role_contract(registration.id, roles, diagnostics)
    _validate_referenced_binding_paths(source_path, bindings.data if bindings is not None else {}, diagnostics)
    _validate_workspace_contract(source_path, workspace_contract.data if workspace_contract is not None else {}, diagnostics)
    if include_harness:
        diagnostics.extend(_harness_diagnostics(source_path))

    template = None
    if manifest is not None or participants is not None:
        manifest_data = manifest.data if manifest is not None else {}
        template_data = _dict_value((participants.data if participants is not None else {}).get("template"))
        parsed_template_id = _string(template_data.get("id")) or registration.id
        template = DomainAgentTeamTemplate(
            id=parsed_template_id,
            source_path=source_path,
            source_kind=registration.source_kind,
            root_role=_string(template_data.get("root_role")) or _string(manifest_data.get("internal_root_role")),
            topology_mode=_string(template_data.get("topology_mode")) or _string(manifest_data.get("topology_mode")),
            default_execution_mode=_string(template_data.get("default_execution_mode"))
            or _string(manifest_data.get("default_execution_mode")),
            topic_instantiation_required=_bool(
                template_data.get("topic_instantiation_required"),
                default=_bool(manifest_data.get("topic_instantiation_required"), default=False),
            ),
            auto_mode_requires_topic_policy=_bool(
                template_data.get("auto_mode_requires_topic_policy"),
                default=_bool(manifest_data.get("auto_mode_requires_topic_policy"), default=False),
            ),
            artifacts=artifacts,
            roles=roles,
            workflow_stage_routes=stage_routes,
            parameters=template_parameters,
            raw_metadata=manifest_data,
        )
    return TemplateValidationReport(registration.id, source_path, not has_errors(diagnostics), diagnostics, template)


def _load_execplan_toml(
    source_path: Path,
    relative_path: str,
    concept: str,
    diagnostics: list[Diagnostic],
) -> SourceDocument | None:
    path = source_path / relative_path
    raw, load_diagnostics = load_toml(path, concept)
    diagnostics.extend(load_diagnostics)
    if raw is None:
        return None
    return SourceDocument(path=path, data=raw)


def _load_execplan_json(
    source_path: Path,
    relative_path: str,
    concept: str,
    diagnostics: list[Diagnostic],
) -> SourceDocument | None:
    path = source_path / relative_path
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        diagnostics.append(
            Diagnostic(code="ISO001", severity="error", concept=concept, path=path, message=f"{concept} file does not exist.")
        )
        return None
    except json.JSONDecodeError as exc:
        diagnostics.append(
            Diagnostic(code="ISO002", severity="error", concept=concept, path=path, message=f"{concept} JSON is malformed: {exc}.")
        )
        return None
    except OSError as exc:
        diagnostics.append(
            Diagnostic(code="ISO001", severity="error", concept=concept, path=path, message=f"{concept} file could not be read: {exc}.")
        )
        return None
    if not isinstance(data, dict):
        diagnostics.append(
            Diagnostic(code="ISO017", severity="error", concept=concept, path=path, message=f"{concept} must be a JSON object.")
        )
        return None
    return SourceDocument(path=path, data=data)


def _parse_artifacts(source_path: Path, raw: dict[str, Any], diagnostics: list[Diagnostic]) -> list[TemplateArtifact]:
    artifacts: list[TemplateArtifact] = []
    for index, item in enumerate(_dict_items(raw.get("artifacts"))):
        artifact_id = _string(item.get("id"))
        path_input = _string(item.get("path"))
        artifact_kind = _string(item.get("artifact_kind")) or "unknown"
        if artifact_id is None or path_input is None:
            diagnostics.append(
                Diagnostic(
                    code="ISO017",
                    severity="error",
                    concept="Domain Agent Team Template artifact",
                    path=source_path / "manifest.toml",
                    field=f"artifacts[{index}]",
                    message="Template artifacts must include id and path.",
                )
            )
            continue
        _require_path(source_path, path_input, "Domain Agent Team Template artifact", diagnostics)
        artifacts.append(
            TemplateArtifact(
                id=artifact_id,
                path_input=path_input,
                artifact_kind=artifact_kind,
                purpose=_string(item.get("purpose")),
                description=_string(item.get("description")),
            )
        )
    return artifacts


def _parse_roles(
    participants: dict[str, Any],
    bindings: dict[str, Any],
    source_path: Path,
    diagnostics: list[Diagnostic],
) -> list[AgentRoleDefinition]:
    workspace_placeholders = {
        item.get("role_id"): item.get("workspace_placeholder")
        for item in _dict_items(bindings.get("participants"))
        if isinstance(item.get("role_id"), str)
    }
    roles: list[AgentRoleDefinition] = []
    for index, item in enumerate(_dict_items(participants.get("roles"))):
        role_id = _string(item.get("id"))
        if role_id is None:
            diagnostics.append(
                Diagnostic(
                    code="ISO017",
                    severity="error",
                    concept="Domain Agent Team Template role",
                    path=source_path / "specs/participants/participants.toml",
                    field=f"roles[{index}].id",
                    message="Template Agent Role definition must include an id.",
                )
            )
            continue
        roles.append(
            AgentRoleDefinition(
                id=role_id,
                role_kind=_string(item.get("role_kind")) or "unknown",
                description=_string(item.get("description")) or "",
                required=_bool(item.get("required"), default=False),
                scalable=_bool(item.get("scalable"), default=False),
                scaling_scope=_string(item.get("scaling_scope")),
                agent_profile_placeholder=_string(item.get("agent_profile_placeholder")),
                capability_binding_placeholder=_string(item.get("capability_binding_placeholder")),
                skill_projection_placeholder=_string(item.get("skill_projection_placeholder")),
                workspace_placeholder=_string(workspace_placeholders.get(role_id)),
                required_skills=_string_list(item.get("required_skills")),
                optional_skills=_string_list(item.get("optional_skills")),
            )
        )
    return roles


def _parse_stage_routes(raw: dict[str, Any], diagnostics: list[Diagnostic]) -> list[WorkflowStageRoute]:
    stage_routes: list[WorkflowStageRoute] = []
    for index, item in enumerate(_dict_items(raw.get("stage_routes"))):
        stage = _string(item.get("workflow_stage"))
        owner = _string(item.get("owner_role"))
        if stage is None or owner is None:
            diagnostics.append(
                Diagnostic(
                    code="ISO017",
                    severity="error",
                    concept="Workflow Stage route",
                    field=f"stage_routes[{index}]",
                    message="Workflow Stage routes must include workflow_stage and owner_role.",
                )
            )
            continue
        stage_routes.append(
            WorkflowStageRoute(
                workflow_stage=stage,
                owner_role=owner,
                alternate_owner_role=_string(item.get("alternate_owner_role")),
                description=_string(item.get("description")),
            )
        )
    return stage_routes


def _parse_parameters(raw: dict[str, Any]) -> list[TemplateParameter]:
    return [
        TemplateParameter(
            name=_string(item.get("name")) or "",
            description=_string(item.get("description")),
            required_for_topic_profile=_bool(item.get("required_for_topic_profile"), default=False),
        )
        for item in _dict_items(raw.get("placeholders"))
        if _string(item.get("name")) is not None
    ]


def _validate_manifest_metadata(
    registration: DomainAgentTeamTemplateRegistration,
    manifest: SourceDocument,
    diagnostics: list[Diagnostic],
) -> None:
    raw = manifest.data
    if raw.get("isomer_template_layer") != "domain_agent_team_template" or raw.get("domain_agent_team_template") is not True:
        diagnostics.append(
            Diagnostic(
                code="ISO017",
                severity="error",
                concept="Domain Agent Team Template manifest",
                path=manifest.path,
                field="isomer_template_layer",
                message="Template manifest must identify the domain_agent_team_template layer.",
            )
        )
    if registration.id == BUILT_IN_DEEPSCI_ORG_ID and raw.get("loop_slug") != BUILT_IN_DEEPSCI_ORG_ID:
        diagnostics.append(
            Diagnostic(
                code="ISO017",
                severity="error",
                concept="Domain Agent Team Template manifest",
                path=manifest.path,
                field="loop_slug",
                message="Built-in deepsci-org template manifest must keep loop_slug deepsci-org.",
            )
        )
    if registration.id == BUILT_IN_DEEPSCI_MINI_ID and raw.get("loop_slug") != BUILT_IN_DEEPSCI_MINI_ID:
        diagnostics.append(
            Diagnostic(
                code="ISO017",
                severity="error",
                concept="Domain Agent Team Template manifest",
                path=manifest.path,
                field="loop_slug",
                message="Built-in deepsci-mini template manifest must keep loop_slug deepsci-mini.",
            )
        )


def _validate_deepsci_role_contract(
    template_id: str,
    roles: list[AgentRoleDefinition],
    diagnostics: list[Diagnostic],
) -> None:
    if template_id == BUILT_IN_DEEPSCI_MINI_ID:
        role_ids = [role.id for role in roles]
        missing = [role_id for role_id in EXPECTED_DEEPSCI_MINI_ROLES if role_id not in role_ids]
        if missing:
            diagnostics.append(
                Diagnostic(
                    code="ISO017",
                    severity="error",
                    concept="Domain Agent Team Template role",
                    field="roles",
                    message=f"deepsci-mini participant contract is missing role ids: {', '.join(missing)}.",
                )
            )
        for role in roles:
            if role.id in EXPECTED_DEEPSCI_MINI_ROLES and not role.required:
                diagnostics.append(
                    Diagnostic(
                        code="ISO017",
                        severity="error",
                        concept="Domain Agent Team Template role",
                        field=f"roles.{role.id}.required",
                        message="deepsci-mini Agent Roles must stay required at the template layer.",
                    )
                )
            if role.scalable:
                diagnostics.append(
                    Diagnostic(
                        code="ISO017",
                        severity="error",
                        concept="Domain Agent Team Template role",
                        field=f"roles.{role.id}.scalable",
                        message="deepsci-mini Agent Roles must stay non-scalable for the compact seed template.",
                    )
                )
    if template_id != BUILT_IN_DEEPSCI_ORG_ID:
        return
    role_ids = [role.id for role in roles]
    missing = [role_id for role_id in EXPECTED_DEEPSCI_ORG_ROLES if role_id not in role_ids]
    if missing:
        diagnostics.append(
            Diagnostic(
                code="ISO017",
                severity="error",
                concept="Domain Agent Team Template role",
                field="roles",
                message=f"deepsci-org participant contract is missing role ids: {', '.join(missing)}.",
            )
        )
    for role in roles:
        if role.id in EXPECTED_DEEPSCI_ORG_ROLES and not role.required:
            diagnostics.append(
                Diagnostic(
                    code="ISO017",
                    severity="error",
                    concept="Domain Agent Team Template role",
                    field=f"roles.{role.id}.required",
                    message="deepsci-org Agent Roles must stay required at the template layer.",
                )
            )
        if role.id in SCALABLE_DEEPSCI_ORG_ROLES:
            if not role.scalable or role.scaling_scope != "research_task":
                diagnostics.append(
                    Diagnostic(
                        code="ISO017",
                        severity="error",
                        concept="Domain Agent Team Template role",
                        field=f"roles.{role.id}.scaling_scope",
                        message="deepsci-org experimenter and analyzer must preserve task-level scalability.",
                    )
                )
        elif role.scalable:
            diagnostics.append(
                Diagnostic(
                    code="ISO017",
                    severity="error",
                    concept="Domain Agent Team Template role",
                    field=f"roles.{role.id}.scalable",
                    message="Only deepsci-org experimenter and analyzer may be scalable in the seed template.",
                )
            )
        if not role.required_skills:
            diagnostics.append(
                Diagnostic(
                    code="ISO017",
                    severity="error",
                    concept="Domain Agent Team Template role",
                    field=f"roles.{role.id}.required_skills",
                    message="Template Agent Role must declare required skills.",
                )
            )
        for field_name, value in (
            ("agent_profile_placeholder", role.agent_profile_placeholder),
            ("capability_binding_placeholder", role.capability_binding_placeholder),
            ("skill_projection_placeholder", role.skill_projection_placeholder),
            ("workspace_placeholder", role.workspace_placeholder),
        ):
            if value is None or not _is_placeholder(value):
                diagnostics.append(
                    Diagnostic(
                        code="ISO017",
                        severity="error",
                        concept="Domain Agent Team Template role",
                        field=f"roles.{role.id}.{field_name}",
                        message="Template Agent Role binding slots must be placeholders.",
                    )
                )


def _validate_referenced_binding_paths(
    source_path: Path,
    bindings: dict[str, Any],
    diagnostics: list[Diagnostic],
) -> None:
    generated_skills = _dict_value(bindings.get("generated_skills"))
    for key, path_input in sorted(generated_skills.items()):
        if key == "description" or not isinstance(path_input, str):
            continue
        _require_path(source_path, path_input, "Domain Agent Team Template generated skill", diagnostics)
    for item in _dict_items(bindings.get("participants")):
        role_id = _string(item.get("role_id")) or "unknown"
        for field_name in ("profile_path", "notifier_prompt_path"):
            path_input = _string(item.get(field_name))
            if path_input is None:
                diagnostics.append(
                    Diagnostic(
                        code="ISO017",
                        severity="error",
                        concept="Domain Agent Team Template binding",
                        field=f"participants.{role_id}.{field_name}",
                        message="Template participant binding must name role profile and notifier prompt paths.",
                    )
                )
                continue
            _require_path(source_path, path_input, "Domain Agent Team Template binding", diagnostics)


def _validate_workspace_contract(
    source_path: Path,
    raw: dict[str, Any],
    diagnostics: list[Diagnostic],
) -> None:
    rules = _dict_items(raw.get("read_write_rules"))
    if "no-workspace-local-teams" not in {_string(item.get("id")) for item in rules}:
        diagnostics.append(
            Diagnostic(
                code="ISO017",
                severity="error",
                concept="Domain Agent Team Template workspace contract",
                path=source_path / "specs/workspace/workspace.toml",
                field="read_write_rules",
                message="Workspace contract must prohibit a workspace-local teams directory.",
            )
        )


def _harness_diagnostics(source_path: Path) -> list[Diagnostic]:
    harness = source_path / "harness/bin/deepsci-org"
    if not harness.exists():
        return []
    try:
        result = subprocess.run(
            [str(harness), "validate"],
            cwd=source_path,
            text=True,
            capture_output=True,
            timeout=15,
            check=False,
        )
    except OSError as exc:
        return [
            Diagnostic(
                code="ISO021",
                severity="warning",
                concept="Domain Agent Team Template harness",
                path=harness,
                message=f"Generated harness validation could not be run: {exc}.",
            )
        ]
    except subprocess.TimeoutExpired:
        return [
            Diagnostic(
                code="ISO021",
                severity="warning",
                concept="Domain Agent Team Template harness",
                path=harness,
                message="Generated harness validation timed out.",
            )
        ]
    if result.returncode == 0:
        return []
    message = (result.stderr or result.stdout or "Generated harness validation failed.").strip().splitlines()[0]
    return [
        Diagnostic(
            code="ISO021",
            severity="error",
            concept="Domain Agent Team Template harness",
            path=harness,
            message=message,
        )
    ]


def _require_path(source_path: Path, path_input: str, concept: str, diagnostics: list[Diagnostic]) -> None:
    path = _execplan_path(source_path, path_input)
    try:
        exists = path.exists()
    except OSError:
        exists = False
    if not exists:
        diagnostics.append(
            Diagnostic(
                code="ISO017",
                severity="error",
                concept=concept,
                path=path,
                message="Referenced template artifact path does not exist.",
            )
        )


def _execplan_path(source_path: Path, path_input: str) -> Path:
    relative = path_input
    if relative.startswith("execplan/"):
        relative = relative.removeprefix("execplan/")
    return source_path / relative


def _scan_template_boundary(
    value: object,
    path: Path,
    key_path: tuple[str, ...],
    diagnostics: list[Diagnostic],
) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            normalized_key = _normalize_key(str(key))
            field_path = (*key_path, str(key))
            if normalized_key in _BOUNDARY_KEYS and not _is_template_placeholder_value(item):
                diagnostics.append(
                    Diagnostic(
                        code="ISO018",
                        severity="error",
                        concept="Domain Agent Team Template boundary",
                        path=path,
                        field=".".join(field_path),
                        message="Concrete topic, runtime, credential, launch, mailbox, gateway, or Run truth is not allowed in template material.",
                    )
                )
            _scan_template_boundary(item, path, field_path, diagnostics)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _scan_template_boundary(item, path, (*key_path, f"[{index}]"), diagnostics)


def _is_template_placeholder_value(value: object) -> bool:
    if isinstance(value, str):
        return _is_placeholder(value)
    if isinstance(value, list):
        return all(_is_template_placeholder_value(item) for item in value)
    if value is None:
        return True
    return False


def _is_placeholder(value: str) -> bool:
    stripped = value.strip()
    return stripped.startswith("{") and stripped.endswith("}")


def _dict_items(value: object) -> list[dict[str, Any]]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        return [value]
    return []


def _dict_value(value: object) -> dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)
    return {}


def _string(value: object) -> str | None:
    if isinstance(value, str) and value:
        return value
    return None


def _string_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str)]
    return []


def _bool(value: object, *, default: bool) -> bool:
    if isinstance(value, bool):
        return value
    return default


def _normalize_key(key: str) -> str:
    return key.lower().replace("-", "_").replace(" ", "_")
