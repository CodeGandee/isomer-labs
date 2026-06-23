"""Packet-backed Topic Agent Team Profile Bundle materialization."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
import shutil

from isomer_labs.diagnostics import Diagnostic, has_errors
from isomer_labs.models import (
    DomainAgentTeamTemplate,
    EffectiveTopicContext,
    FanoutPolicy,
    ProfileValidationReport,
    TOPIC_AGENT_TEAM_PROFILE_SCHEMA_VERSION,
    TopicAgentTeamProfile,
)
from isomer_labs.path_utils import is_within
from isomer_labs.team_profiles import profile_to_toml, validate_topic_agent_team_profile
from isomer_labs.topic_team_instantiation import (
    PROFILE_BUNDLE_APPROVAL_FILENAME,
    PROFILE_BUNDLE_PACKET_FILENAME,
    PROFILE_BUNDLE_PROFILE_FILENAME,
    PacketValidationReport,
    TopicTeamInstantiationPacket,
    packet_to_toml,
    topic_profile_bundle_path,
    topic_profile_bundle_profile_path,
)
from isomer_labs.topic_team_packet_validation import validate_topic_team_instantiation_packet


@dataclass(frozen=True)
class ProfileBundleMaterializationResult:
    profile: TopicAgentTeamProfile | None
    bundle_path: Path
    profile_path: Path
    packet_path: Path
    approval_path: Path
    validation_path: Path
    written: bool
    copied_paths: list[Path] = field(default_factory=list)
    diagnostics: list[Diagnostic] = field(default_factory=list)
    packet_validation: PacketValidationReport | None = None
    profile_validation: ProfileValidationReport | None = None

    def to_json(self) -> dict[str, object]:
        return {
            "profile": self.profile.to_json() if self.profile is not None else None,
            "bundle_path": str(self.bundle_path),
            "profile_path": str(self.profile_path),
            "packet_path": str(self.packet_path),
            "approval_path": str(self.approval_path),
            "validation_path": str(self.validation_path),
            "written": self.written,
            "copied_paths": [str(path) for path in self.copied_paths],
            "diagnostics": [diagnostic.to_json() for diagnostic in self.diagnostics],
            "packet_validation": self.packet_validation.to_json() if self.packet_validation is not None else None,
            "profile_validation": self.profile_validation.to_json() if self.profile_validation is not None else None,
        }


def build_topic_agent_team_profile_from_packet(
    context: EffectiveTopicContext,
    template: DomainAgentTeamTemplate,
    packet: TopicTeamInstantiationPacket,
) -> TopicAgentTeamProfile:
    fanout_policies = [
        FanoutPolicy(
            role_id=role.id,
            parallel_execution_scope="research_task",
            max_shards=2,
            allocation_rule=f"{packet.derived_profile_id}:{role.id}:shard-agent-workspace-allocation",
        )
        for role in template.roles
        if role.scalable and any(binding.role_id == role.id and binding.active for binding in packet.role_bindings)
    ]
    return TopicAgentTeamProfile(
        id=packet.derived_profile_id,
        domain_agent_team_template_id=template.id,
        research_topic_id=packet.research_topic_id,
        topic_workspace_id=context.topic_workspace_id,
        source_path=topic_profile_bundle_profile_path(context),
        schema_version=TOPIC_AGENT_TEAM_PROFILE_SCHEMA_VERSION,
        role_bindings=list(packet.role_bindings),
        expected_artifacts=list(packet.expected_artifacts),
        constraints=list(packet.constraints),
        coordination_policy_ref=packet.policy_refs.get("coordination_policy_ref"),
        gate_policy_ref=packet.policy_refs.get("gate_policy_ref"),
        scheduler_policy_ref=packet.policy_refs.get("scheduler_policy_ref"),
        baseline_waiver_policy_ref=packet.policy_refs.get("baseline_waiver_policy_ref"),
        literature_provider_ref=packet.policy_refs.get("literature_provider_ref"),
        default_execution_mode=packet.control_mode or template.default_execution_mode or "manual",
        automatic_mode_policy_ref=packet.policy_refs.get("automatic_mode_policy_ref"),
        reviewer_read_access_policy=packet.policy_refs.get("reviewer_read_access_policy") or "promoted-artifacts-only",
        fanout_policies=fanout_policies,
        profile_bundle_ref=packet.profile_bundle_ref,
        instantiation_packet_ref=str(topic_profile_bundle_path(context) / PROFILE_BUNDLE_PACKET_FILENAME),
        approval_ref=packet.approval.approval_ref,
        approval_actor_ref=packet.approval.approval_actor_ref,
        approval_mode=packet.approval.approval_mode,
        project_operator_ref=packet.project_operator_ref or packet.project_operator_session_ref,
        topic_service_agent_refs=list(packet.topic_service_agent_refs),
        copied_material_refs=[item.target_path_input for item in packet.copied_material],
        validation_refs=list(packet.validation_refs),
        launch_blocker_refs=[f"placeholder:{item.name}" for item in packet.deferrals if item.launch_blocking],
        raw={"profile_materialization": "packet_backed", "approval_state": packet.approval.state},
    )


def materialize_topic_agent_team_profile_bundle(
    context: EffectiveTopicContext,
    template: DomainAgentTeamTemplate,
    packet: TopicTeamInstantiationPacket,
    *,
    write: bool,
    overwrite: bool = False,
) -> ProfileBundleMaterializationResult:
    bundle_path = topic_profile_bundle_path(context)
    profile_path = bundle_path / PROFILE_BUNDLE_PROFILE_FILENAME
    packet_path = bundle_path / PROFILE_BUNDLE_PACKET_FILENAME
    approval_path = bundle_path / PROFILE_BUNDLE_APPROVAL_FILENAME
    validation_path = bundle_path / "validation" / "packet-validation.json"
    packet_report = validate_topic_team_instantiation_packet(
        packet,
        context=context,
        project=context.project,
        template=template,
        launch_facing=False,
        existing_bundle_allowed=overwrite,
    )
    diagnostics = list(packet_report.diagnostics)
    if packet.approval.state != "approved":
        diagnostics.append(
            Diagnostic(
                code="ISO095",
                severity="error",
                concept="Topic Team Instantiation Packet approval",
                path=packet.source_path,
                field="approval.state",
                message="Authoritative Topic Agent Team Profile Bundle materialization requires approved packet provenance.",
            )
        )
    if profile_path.exists() and not overwrite:
        diagnostics.append(
            Diagnostic(
                code="ISO094",
                severity="error",
                concept="Topic Agent Team Profile Bundle",
                path=profile_path,
                message="A Topic Agent Team Profile Bundle already exists for this Research Topic.",
            )
        )
    profile = build_topic_agent_team_profile_from_packet(context, template, packet)
    profile_report = validate_topic_agent_team_profile(profile, template, project=context.project, launch_facing=False)
    diagnostics.extend(profile_report.diagnostics)
    copied_paths: list[Path] = []
    if has_errors(diagnostics) or not write:
        return _result(
            profile,
            bundle_path,
            profile_path,
            packet_path,
            approval_path,
            validation_path,
            False,
            copied_paths,
            diagnostics,
            packet_report,
            profile_report,
        )
    bundle_path.mkdir(parents=True, exist_ok=True)
    (bundle_path / "validation").mkdir(parents=True, exist_ok=True)
    (bundle_path / "provenance").mkdir(parents=True, exist_ok=True)
    for item in packet.copied_material:
        source = template.source_path / item.source_path_input.removeprefix("execplan/")
        target = bundle_path / item.target_path_input
        if not is_within(target, bundle_path):
            diagnostics.append(
                Diagnostic(
                    code="ISO091",
                    severity="error",
                    concept="Topic Agent Team Profile Bundle",
                    path=target,
                    message="Copied material target escapes the Topic Agent Team Profile Bundle.",
                )
            )
            continue
        if source.is_dir():
            shutil.copytree(source, target, dirs_exist_ok=overwrite)
        elif source.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        copied_paths.append(target)
    _apply_topic_edits(bundle_path, packet, diagnostics)
    if has_errors(diagnostics):
        return _result(
            profile,
            bundle_path,
            profile_path,
            packet_path,
            approval_path,
            validation_path,
            False,
            copied_paths,
            diagnostics,
            packet_report,
            profile_report,
        )
    profile_path.write_text(profile_to_toml(profile), encoding="utf-8")
    packet_path.write_text(packet_to_toml(packet), encoding="utf-8")
    approval_path.write_text(_approval_to_toml(packet), encoding="utf-8")
    validation_path.write_text(json.dumps(packet_report.to_json(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (bundle_path / "provenance" / "README.md").write_text(_provenance_readme(packet), encoding="utf-8")
    return _result(
        profile,
        bundle_path,
        profile_path,
        packet_path,
        approval_path,
        validation_path,
        True,
        copied_paths,
        diagnostics,
        packet_report,
        profile_report,
    )


def _result(
    profile: TopicAgentTeamProfile,
    bundle_path: Path,
    profile_path: Path,
    packet_path: Path,
    approval_path: Path,
    validation_path: Path,
    written: bool,
    copied_paths: list[Path],
    diagnostics: list[Diagnostic],
    packet_report: PacketValidationReport,
    profile_report: ProfileValidationReport,
) -> ProfileBundleMaterializationResult:
    return ProfileBundleMaterializationResult(
        profile=profile,
        bundle_path=bundle_path,
        profile_path=profile_path,
        packet_path=packet_path,
        approval_path=approval_path,
        validation_path=validation_path,
        written=written,
        copied_paths=copied_paths,
        diagnostics=diagnostics,
        packet_validation=packet_report,
        profile_validation=profile_report,
    )


def _apply_topic_edits(
    bundle_path: Path,
    packet: TopicTeamInstantiationPacket,
    diagnostics: list[Diagnostic],
) -> None:
    for index, item in enumerate(packet.topic_edits):
        target = bundle_path / item.target_path_input
        if not is_within(target, bundle_path):
            diagnostics.append(
                Diagnostic(
                    code="ISO091",
                    severity="error",
                    concept="Topic Agent Team Profile Bundle topic edit",
                    path=target,
                    field=f"topic_edits[{index}].target_path",
                    message="Topic edit target escapes the Topic Agent Team Profile Bundle.",
                )
            )
            continue
        if item.search is None or item.replace is None:
            continue
        if not target.is_file():
            diagnostics.append(
                Diagnostic(
                    code="ISO091",
                    severity="error",
                    concept="Topic Agent Team Profile Bundle topic edit",
                    path=target,
                    field=f"topic_edits[{index}].target_path",
                    message="Topic edit target file does not exist after copied material materialization.",
                )
            )
            continue
        text = target.read_text(encoding="utf-8")
        if item.search not in text:
            diagnostics.append(
                Diagnostic(
                    code="ISO091",
                    severity="error",
                    concept="Topic Agent Team Profile Bundle topic edit",
                    path=target,
                    field=f"topic_edits[{index}].search",
                    message="Topic edit search text was not found in the copied target file.",
                )
            )
            continue
        target.write_text(text.replace(item.search, item.replace), encoding="utf-8")


def _approval_to_toml(packet: TopicTeamInstantiationPacket) -> str:
    lines = [f'state = "{packet.approval.state}"']
    for key, value in (
        ("approval_ref", packet.approval.approval_ref),
        ("approval_actor_ref", packet.approval.approval_actor_ref),
        ("approval_mode", packet.approval.approval_mode),
        ("review_summary", packet.approval.review_summary),
        ("validation_result_ref", packet.approval.validation_result_ref),
        ("approved_at", packet.approval.approved_at),
        ("instantiation_packet_ref", str(packet.source_path)),
    ):
        if value is not None:
            lines.append(f'{key} = "{value}"')
    return "\n".join(lines) + "\n"


def _provenance_readme(packet: TopicTeamInstantiationPacket) -> str:
    lines = [
        "# Topic Agent Team Profile Bundle Provenance",
        "",
        f"- Source template: `{packet.source_template_ref}`",
        f"- Research Topic: `{packet.research_topic_id}`",
        f"- Topic Workspace: `{packet.topic_workspace_ref}`",
    ]
    if packet.project_operator_ref is not None:
        lines.append(f"- Project operator: `{packet.project_operator_ref}`")
    if packet.project_operator_session_ref is not None:
        lines.append(f"- Project operator session: `{packet.project_operator_session_ref}`")
    if packet.topic_service_agent_refs:
        refs = ", ".join(f"`{ref}`" for ref in packet.topic_service_agent_refs)
        lines.append(f"- Topic Service Agents: {refs}")
    if packet.approval.approval_ref is not None:
        lines.append(f"- Approval: `{packet.approval.approval_ref}`")
    return "\n".join(lines) + "\n"
