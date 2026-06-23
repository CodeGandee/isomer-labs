"""Topic Team Instantiation Packet parsing and rendering."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from isomer_labs.diagnostics import Diagnostic
from isomer_labs.models import EffectiveTopicContext, RoleBinding


TOPIC_TEAM_INSTANTIATION_PACKET_SCHEMA_VERSION = "isomer-topic-team-instantiation-packet.v1"
PROFILE_BUNDLE_DIRNAME = "team-profile"
PROFILE_BUNDLE_PROFILE_FILENAME = "profile.toml"
PROFILE_BUNDLE_PACKET_FILENAME = "instantiation-packet.toml"
PROFILE_BUNDLE_APPROVAL_FILENAME = "approval.toml"

_PACKET_RUNTIME_KEYS = {
    "run_status",
    "command_output",
    "command_outputs",
    "live_process_id",
    "live_process_ids",
    "mailbox",
    "mailbox_ref",
    "mailbox_state",
    "gateway",
    "gateway_ref",
    "gateway_state",
    "agent_team_instance_id",
    "agent_instance_id",
    "houmao_managed_agent_id",
    "houmao_managed_agent_ids",
    "adapter_launch_ref",
    "houmao_launch_ref",
    "launch_ref",
    "launch_refs",
    "launch_dossier_ref",
    "provider_payload",
    "provider_payloads",
    "artifact_contents",
    "evidence_items",
    "findings",
    "gates",
    "decision_records",
    "provenance_records",
}
_SECRET_TERMS = (
    "secret",
    "token",
    "api_key",
    "apikey",
    "password",
    "credential",
    "private_key",
    "access_key",
    "client_secret",
)
_USER_SELECTED_PROFILE_FIELDS = {
    "profile_id",
    "topic_agent_team_profile_id",
    "selected_profile_id",
    "profile_variant_id",
}


@dataclass(frozen=True)
class CopiedMaterialPlan:
    source_path_input: str
    target_path_input: str
    required: bool = True
    purpose: str | None = None

    def to_json(self) -> dict[str, object]:
        return {
            "source_path": self.source_path_input,
            "target_path": self.target_path_input,
            "required": self.required,
            "purpose": self.purpose,
        }


@dataclass(frozen=True)
class TopicEdit:
    target_path_input: str
    description: str
    search: str | None = None
    replace: str | None = None

    def to_json(self) -> dict[str, object]:
        return {
            "target_path": self.target_path_input,
            "description": self.description,
            "search": self.search,
            "replace": self.replace,
        }


@dataclass(frozen=True)
class PlaceholderResolution:
    name: str
    value: str | None = None
    required: bool = False
    deferred: bool = False
    reason: str | None = None
    launch_impact: str | None = None
    required_action: str | None = None
    launch_blocking: bool = False

    def to_json(self) -> dict[str, object]:
        return {
            "name": self.name,
            "value": self.value,
            "required": self.required,
            "deferred": self.deferred,
            "reason": self.reason,
            "launch_impact": self.launch_impact,
            "required_action": self.required_action,
            "launch_blocking": self.launch_blocking,
        }


@dataclass(frozen=True)
class TopicTeamApproval:
    state: str
    approval_ref: str | None = None
    approval_actor_ref: str | None = None
    approval_mode: str | None = None
    review_summary: str | None = None
    validation_result_ref: str | None = None
    approved_at: str | None = None

    def to_json(self) -> dict[str, object]:
        return {
            "state": self.state,
            "approval_ref": self.approval_ref,
            "approval_actor_ref": self.approval_actor_ref,
            "approval_mode": self.approval_mode,
            "review_summary": self.review_summary,
            "validation_result_ref": self.validation_result_ref,
            "approved_at": self.approved_at,
        }


@dataclass(frozen=True)
class TopicTeamInstantiationPacket:
    schema_version: str
    source_path: Path
    source_template_ref: str
    research_topic_id: str
    topic_workspace_ref: str
    workspace_runtime_ref: str | None
    target_profile_bundle_path: str
    role_bindings: list[RoleBinding] = field(default_factory=list)
    policy_refs: dict[str, str] = field(default_factory=dict)
    expected_artifacts: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    control_mode: str | None = None
    copied_material: list[CopiedMaterialPlan] = field(default_factory=list)
    topic_edits: list[TopicEdit] = field(default_factory=list)
    placeholder_resolutions: list[PlaceholderResolution] = field(default_factory=list)
    deferrals: list[PlaceholderResolution] = field(default_factory=list)
    approval: TopicTeamApproval = field(default_factory=lambda: TopicTeamApproval(state="draft"))
    project_operator_ref: str | None = None
    project_operator_session_ref: str | None = None
    topic_service_agent_refs: list[str] = field(default_factory=list)
    service_request_refs: list[str] = field(default_factory=list)
    validation_refs: list[str] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)

    @property
    def template_id(self) -> str:
        return self.source_template_ref

    @property
    def profile_bundle_ref(self) -> str:
        return self.target_profile_bundle_path

    @property
    def derived_profile_id(self) -> str:
        return derive_topic_agent_team_profile_id(self.research_topic_id, self.source_template_ref)

    def to_json(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "source_path": str(self.source_path),
            "source_template_ref": self.source_template_ref,
            "research_topic_id": self.research_topic_id,
            "topic_workspace_ref": self.topic_workspace_ref,
            "workspace_runtime_ref": self.workspace_runtime_ref,
            "target_profile_bundle_path": self.target_profile_bundle_path,
            "derived_topic_agent_team_profile_id": self.derived_profile_id,
            "role_bindings": [binding.to_json() for binding in self.role_bindings],
            "policy_refs": self.policy_refs,
            "expected_artifacts": self.expected_artifacts,
            "constraints": self.constraints,
            "control_mode": self.control_mode,
            "copied_material": [item.to_json() for item in self.copied_material],
            "topic_edits": [item.to_json() for item in self.topic_edits],
            "placeholder_resolutions": [item.to_json() for item in self.placeholder_resolutions],
            "deferrals": [item.to_json() for item in self.deferrals],
            "approval": self.approval.to_json(),
            "project_operator_ref": self.project_operator_ref,
            "project_operator_session_ref": self.project_operator_session_ref,
            "topic_service_agent_refs": self.topic_service_agent_refs,
            "service_request_refs": self.service_request_refs,
            "validation_refs": self.validation_refs,
        }


@dataclass(frozen=True)
class PacketValidationReport:
    packet_ref: str
    source_path: Path
    ok: bool
    diagnostics: list[Diagnostic]
    packet: TopicTeamInstantiationPacket | None = None
    launch_blocker_refs: list[str] = field(default_factory=list)

    def to_json(self) -> dict[str, object]:
        return {
            "packet_ref": self.packet_ref,
            "source_path": str(self.source_path),
            "ok": self.ok,
            "packet": self.packet.to_json() if self.packet is not None else None,
            "diagnostics": [diagnostic.to_json() for diagnostic in self.diagnostics],
            "launch_blocker_refs": self.launch_blocker_refs,
        }


def derive_topic_agent_team_profile_id(research_topic_id: str, template_id: str) -> str:
    return f"{research_topic_id}-{template_id}"


def topic_profile_bundle_path(context: EffectiveTopicContext) -> Path:
    return context.topic_workspace_path / PROFILE_BUNDLE_DIRNAME


def topic_profile_bundle_profile_path(context: EffectiveTopicContext) -> Path:
    return topic_profile_bundle_path(context) / PROFILE_BUNDLE_PROFILE_FILENAME


def parse_topic_team_instantiation_packet(
    path: Path,
    raw: dict[str, Any],
) -> tuple[TopicTeamInstantiationPacket | None, list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    diagnostics.extend(scan_packet_for_forbidden_fields(raw, path))
    data = _dict_value(raw.get("packet")) or raw
    source_template_ref = _first_string(data, "source_template_ref", "domain_agent_team_template_id", "template_id")
    research_topic_id = _first_string(data, "research_topic_id", "topic_id")
    topic_workspace_ref = _first_string(data, "topic_workspace_ref", "topic_workspace_id")
    target_profile_bundle_path = _first_string(
        data,
        "target_profile_bundle_path",
        "profile_bundle_path",
        "topic_agent_team_profile_bundle_ref",
    )
    missing: list[str] = []
    if source_template_ref is None:
        missing.append("source_template_ref")
    if research_topic_id is None:
        missing.append("research_topic_id")
    if topic_workspace_ref is None:
        missing.append("topic_workspace_ref")
    if target_profile_bundle_path is None:
        missing.append("target_profile_bundle_path")
    if missing:
        diagnostics.append(
            Diagnostic(
                code="ISO090",
                severity="error",
                concept="Topic Team Instantiation Packet",
                path=path,
                message=f"Topic Team Instantiation Packet must include {', '.join(missing)}.",
            )
        )
        return None, diagnostics
    assert source_template_ref is not None
    assert research_topic_id is not None
    assert topic_workspace_ref is not None
    assert target_profile_bundle_path is not None

    role_bindings = _parse_role_bindings(data.get("role_bindings") or data.get("roles"))
    policy_refs = {
        key: value
        for key, value in _dict_value(data.get("policy_refs")).items()
        if isinstance(key, str) and isinstance(value, str) and value
    }
    for key in (
        "coordination_policy_ref",
        "gate_policy_ref",
        "scheduler_policy_ref",
        "baseline_waiver_policy_ref",
        "literature_provider_ref",
        "automatic_mode_policy_ref",
    ):
        value = _string(data.get(key))
        if value is not None:
            policy_refs.setdefault(key, value)

    packet = TopicTeamInstantiationPacket(
        schema_version=_string(data.get("schema_version")) or TOPIC_TEAM_INSTANTIATION_PACKET_SCHEMA_VERSION,
        source_path=path,
        source_template_ref=source_template_ref,
        research_topic_id=research_topic_id,
        topic_workspace_ref=topic_workspace_ref,
        workspace_runtime_ref=_string(data.get("workspace_runtime_ref")),
        target_profile_bundle_path=target_profile_bundle_path,
        role_bindings=role_bindings,
        policy_refs=policy_refs,
        expected_artifacts=_string_list(data.get("expected_artifacts")),
        constraints=_string_list(data.get("constraints")),
        control_mode=_string(data.get("control_mode")) or _string(data.get("default_execution_mode")),
        copied_material=_parse_copied_material(data.get("copied_material") or data.get("copied_template_material")),
        topic_edits=_parse_topic_edits(data.get("topic_edits") or data.get("proposed_topic_edits")),
        placeholder_resolutions=_parse_placeholder_resolutions(data.get("placeholder_resolutions")),
        deferrals=_parse_placeholder_resolutions(data.get("deferrals") or data.get("deferred_placeholders"), force_deferred=True),
        approval=_parse_approval(data),
        project_operator_ref=_string(data.get("project_operator_ref")),
        project_operator_session_ref=_string(data.get("project_operator_session_ref")),
        topic_service_agent_refs=_string_list(data.get("topic_service_agent_refs")),
        service_request_refs=_string_list(data.get("service_request_refs")),
        validation_refs=_string_list(data.get("validation_refs")),
        raw=raw,
    )
    return packet, diagnostics


def packet_to_toml(packet: TopicTeamInstantiationPacket) -> str:
    lines = [
        f"schema_version = {_toml_string(packet.schema_version)}",
        f"source_template_ref = {_toml_string(packet.source_template_ref)}",
        f"research_topic_id = {_toml_string(packet.research_topic_id)}",
        f"topic_workspace_ref = {_toml_string(packet.topic_workspace_ref)}",
        f"target_profile_bundle_path = {_toml_string(packet.target_profile_bundle_path)}",
    ]
    if packet.workspace_runtime_ref is not None:
        lines.append(f"workspace_runtime_ref = {_toml_string(packet.workspace_runtime_ref)}")
    if packet.control_mode is not None:
        lines.append(f"control_mode = {_toml_string(packet.control_mode)}")
    if packet.project_operator_ref is not None:
        lines.append(f"project_operator_ref = {_toml_string(packet.project_operator_ref)}")
    if packet.project_operator_session_ref is not None:
        lines.append(f"project_operator_session_ref = {_toml_string(packet.project_operator_session_ref)}")
    lines.append(_array_line("topic_service_agent_refs", packet.topic_service_agent_refs))
    lines.append(_array_line("service_request_refs", packet.service_request_refs))
    lines.append(_array_line("validation_refs", packet.validation_refs))
    lines.append(_array_line("expected_artifacts", packet.expected_artifacts))
    lines.append(_array_line("constraints", packet.constraints))
    if packet.policy_refs:
        lines.append("")
        lines.append("[policy_refs]")
        lines.extend(f"{key} = {_toml_string(value)}" for key, value in sorted(packet.policy_refs.items()))
    for binding in packet.role_bindings:
        lines.extend(["", "[[role_bindings]]", f"role_id = {_toml_string(binding.role_id)}", f"active = {str(binding.active).lower()}"])
        for key, value in (
            ("agent_profile_ref", binding.agent_profile_ref),
            ("capability_binding_ref", binding.capability_binding_ref),
            ("skill_binding_projection_ref", binding.skill_binding_projection_ref),
            ("agent_workspace_ref", binding.agent_workspace_ref),
        ):
            if value is not None:
                lines.append(f"{key} = {_toml_string(value)}")
        lines.append(_array_line("required_skills", binding.required_skills))
        lines.append(_array_line("optional_skills", binding.optional_skills))
    for copied_item in packet.copied_material:
        lines.extend(
            [
                "",
                "[[copied_material]]",
                f"source_path = {_toml_string(copied_item.source_path_input)}",
                f"target_path = {_toml_string(copied_item.target_path_input)}",
                f"required = {str(copied_item.required).lower()}",
            ]
        )
        if copied_item.purpose is not None:
            lines.append(f"purpose = {_toml_string(copied_item.purpose)}")
    for edit_item in packet.topic_edits:
        lines.extend(
            [
                "",
                "[[topic_edits]]",
                f"target_path = {_toml_string(edit_item.target_path_input)}",
                f"description = {_toml_string(edit_item.description)}",
            ]
        )
        if edit_item.search is not None:
            lines.append(f"search = {_toml_string(edit_item.search)}")
        if edit_item.replace is not None:
            lines.append(f"replace = {_toml_string(edit_item.replace)}")
    for resolution_item in packet.placeholder_resolutions:
        _append_placeholder_resolution(lines, "placeholder_resolutions", resolution_item)
    for deferral_item in packet.deferrals:
        _append_placeholder_resolution(lines, "deferrals", deferral_item)
    lines.extend(["", "[approval]", f"state = {_toml_string(packet.approval.state)}"])
    for key, value in (
        ("approval_ref", packet.approval.approval_ref),
        ("approval_actor_ref", packet.approval.approval_actor_ref),
        ("approval_mode", packet.approval.approval_mode),
        ("review_summary", packet.approval.review_summary),
        ("validation_result_ref", packet.approval.validation_result_ref),
        ("approved_at", packet.approval.approved_at),
    ):
        if value is not None:
            lines.append(f"{key} = {_toml_string(value)}")
    return "\n".join(lines) + "\n"


def scan_packet_for_forbidden_fields(data: object, path: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    _scan_packet_for_forbidden_fields(data, path, (), diagnostics)
    return diagnostics


def _parse_role_bindings(value: object) -> list[RoleBinding]:
    result: list[RoleBinding] = []
    for item in _dict_items(value):
        role_id = _string(item.get("role_id")) or _string(item.get("id"))
        if role_id is None:
            continue
        result.append(
            RoleBinding(
                role_id=role_id,
                active=_bool(item.get("active"), default=True),
                agent_profile_ref=_string(item.get("agent_profile_ref")),
                capability_binding_ref=_string(item.get("capability_binding_ref")),
                skill_binding_projection_ref=_string(item.get("skill_binding_projection_ref") or item.get("skill_projection_ref")),
                agent_workspace_ref=_string(item.get("agent_workspace_ref")),
                required_skills=_string_list(item.get("required_skills")),
                optional_skills=_string_list(item.get("optional_skills")),
            )
        )
    return result


def _parse_copied_material(value: object) -> list[CopiedMaterialPlan]:
    result: list[CopiedMaterialPlan] = []
    for item in _dict_items(value):
        source_path = _string(item.get("source_path")) or _string(item.get("path"))
        target_path = _string(item.get("target_path")) or source_path
        if source_path is None or target_path is None:
            continue
        result.append(
            CopiedMaterialPlan(
                source_path_input=source_path,
                target_path_input=target_path,
                required=_bool(item.get("required"), default=True),
                purpose=_string(item.get("purpose")) or _string(item.get("description")),
            )
        )
    return result


def _parse_topic_edits(value: object) -> list[TopicEdit]:
    result: list[TopicEdit] = []
    for item in _dict_items(value):
        target_path = _string(item.get("target_path")) or _string(item.get("path"))
        description = _string(item.get("description"))
        if target_path is None or description is None:
            continue
        result.append(
            TopicEdit(
                target_path_input=target_path,
                description=description,
                search=_string(item.get("search")),
                replace=_string(item.get("replace")),
            )
        )
    return result


def _parse_placeholder_resolutions(value: object, *, force_deferred: bool = False) -> list[PlaceholderResolution]:
    result: list[PlaceholderResolution] = []
    for item in _dict_items(value):
        name = _string(item.get("name")) or _string(item.get("placeholder"))
        if name is None:
            continue
        result.append(
            PlaceholderResolution(
                name=name,
                value=_string(item.get("value")),
                required=_bool(item.get("required"), default=False),
                deferred=force_deferred or _bool(item.get("deferred"), default=False),
                reason=_string(item.get("reason")),
                launch_impact=_string(item.get("launch_impact")),
                required_action=_string(item.get("required_action")),
                launch_blocking=_bool(item.get("launch_blocking"), default=False),
            )
        )
    return result


def _parse_approval(data: dict[str, Any]) -> TopicTeamApproval:
    approval_data = _dict_value(data.get("approval"))
    merged = {**data, **approval_data}
    return TopicTeamApproval(
        state=_string(merged.get("state")) or _string(merged.get("approval_state")) or "draft",
        approval_ref=_string(merged.get("approval_ref")),
        approval_actor_ref=_string(merged.get("approval_actor_ref")),
        approval_mode=_string(merged.get("approval_mode")),
        review_summary=_string(merged.get("review_summary")),
        validation_result_ref=_string(merged.get("validation_result_ref")),
        approved_at=_string(merged.get("approved_at")),
    )


def _append_placeholder_resolution(lines: list[str], table_name: str, item: PlaceholderResolution) -> None:
    lines.extend(["", f"[[{table_name}]]", f"name = {_toml_string(item.name)}"])
    if item.value is not None:
        lines.append(f"value = {_toml_string(item.value)}")
    lines.append(f"required = {str(item.required).lower()}")
    lines.append(f"deferred = {str(item.deferred).lower()}")
    for key, value in (
        ("reason", item.reason),
        ("launch_impact", item.launch_impact),
        ("required_action", item.required_action),
    ):
        if value is not None:
            lines.append(f"{key} = {_toml_string(value)}")
    lines.append(f"launch_blocking = {str(item.launch_blocking).lower()}")


def _string_values_for_placeholder_scan(packet: TopicTeamInstantiationPacket) -> list[tuple[str, str]]:
    values: list[tuple[str, str]] = [
        ("source_template_ref", packet.source_template_ref),
        ("research_topic_id", packet.research_topic_id),
        ("topic_workspace_ref", packet.topic_workspace_ref),
        ("target_profile_bundle_path", packet.target_profile_bundle_path),
    ]
    if packet.workspace_runtime_ref is not None:
        values.append(("workspace_runtime_ref", packet.workspace_runtime_ref))
    values.extend((f"policy_refs.{key}", value) for key, value in packet.policy_refs.items())
    values.extend((f"expected_artifacts[{index}]", value) for index, value in enumerate(packet.expected_artifacts))
    for binding in packet.role_bindings:
        for key, value in (
            ("agent_profile_ref", binding.agent_profile_ref),
            ("capability_binding_ref", binding.capability_binding_ref),
            ("skill_binding_projection_ref", binding.skill_binding_projection_ref),
            ("agent_workspace_ref", binding.agent_workspace_ref),
        ):
            if value is not None:
                values.append((f"role_bindings.{binding.role_id}.{key}", value))
    return values


def _scan_packet_for_forbidden_fields(
    value: object,
    path: Path,
    key_path: tuple[str, ...],
    diagnostics: list[Diagnostic],
) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            field_path = (*key_path, str(key))
            normalized_key = _normalize_key(str(key))
            if any(term in normalized_key for term in _SECRET_TERMS):
                diagnostics.append(
                    Diagnostic(
                        code="ISO010",
                        severity="error",
                        concept="Topic Team Instantiation Packet",
                        path=path,
                        field=".".join(field_path),
                        message="Inline secret-like material is not allowed here; use a credential backend or a ref.",
                    )
                )
            if normalized_key in _PACKET_RUNTIME_KEYS:
                diagnostics.append(
                    Diagnostic(
                        code="ISO009",
                        severity="error",
                        concept="Topic Team Instantiation Packet",
                        path=path,
                        field=".".join(field_path),
                        message="Runtime truth belongs in Workspace Runtime records or adapter-backed Artifacts, not a Topic Team Instantiation Packet.",
                    )
                )
            _scan_packet_for_forbidden_fields(item, path, field_path, diagnostics)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _scan_packet_for_forbidden_fields(item, path, (*key_path, f"[{index}]"), diagnostics)


def _scan_user_selected_profile_ids(data: object, path: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    _scan_user_selected_profile_ids_inner(data, path, (), diagnostics)
    return diagnostics


def _scan_user_selected_profile_ids_inner(
    value: object,
    path: Path,
    key_path: tuple[str, ...],
    diagnostics: list[Diagnostic],
) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            normalized_key = _normalize_key(str(key))
            field_path = (*key_path, str(key))
            if normalized_key in _USER_SELECTED_PROFILE_FIELDS:
                diagnostics.append(
                    Diagnostic(
                        code="ISO096",
                        severity="error",
                        concept="Topic Team Instantiation Packet",
                        path=path,
                        field=".".join(field_path),
                        message="Launch-facing packet material must not select a profile id; profile identity is derived from the Research Topic and team-profile bundle path.",
                    )
                )
            _scan_user_selected_profile_ids_inner(item, path, field_path, diagnostics)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _scan_user_selected_profile_ids_inner(item, path, (*key_path, f"[{index}]"), diagnostics)


def _ref_encodes_topic_id(value: str, topic_id: str) -> bool:
    normalized = value.replace("/", ":")
    tokens = [token for token in normalized.split(":") if token]
    return any(token == topic_id or token.startswith(f"{topic_id}-") or token.startswith(f"{topic_id}_") for token in tokens)


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


def _first_string(data: dict[str, Any], *keys: str) -> str | None:
    for key in keys:
        value = data.get(key)
        if isinstance(value, str) and value:
            return value
    return None


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


def _toml_string(value: str) -> str:
    return json.dumps(value)


def _array_line(key: str, values: list[str]) -> str:
    rendered = ", ".join(_toml_string(value) for value in values)
    return f"{key} = [{rendered}]"
