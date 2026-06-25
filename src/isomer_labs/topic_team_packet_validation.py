"""Validation for Topic Team Instantiation Packets."""

from __future__ import annotations

from pathlib import Path

from isomer_labs.context import resolve_topic_workspace
from isomer_labs.diagnostics import Diagnostic, has_errors
from isomer_labs.models import DomainAgentTeamTemplate, EffectiveTopicContext, Project
from isomer_labs.path_utils import canonicalize, is_within, resolve_project_path
from isomer_labs.topic_team_instantiation import (
    PROFILE_BUNDLE_PROFILE_FILENAME,
    PacketValidationReport,
    TopicTeamInstantiationPacket,
    _is_placeholder,
    _ref_encodes_topic_id,
    _scan_user_selected_profile_ids,
    _string_values_for_placeholder_scan,
    scan_packet_for_forbidden_fields,
    topic_profile_bundle_path,
)
from isomer_labs.workspace_refs import validate_agent_workspace_ref_scope


def validate_topic_team_instantiation_packet(
    packet: TopicTeamInstantiationPacket | None,
    *,
    context: EffectiveTopicContext | None = None,
    project: Project | None = None,
    template: DomainAgentTeamTemplate | None = None,
    launch_facing: bool = False,
    existing_bundle_allowed: bool = True,
) -> PacketValidationReport:
    source_path = packet.source_path if packet is not None else Path(".")
    if packet is None:
        diagnostic = Diagnostic(
            code="ISO090",
            severity="error",
            concept="Topic Team Instantiation Packet",
            path=source_path,
            message="Topic Team Instantiation Packet could not be parsed.",
        )
        return PacketValidationReport("unknown", source_path, False, [diagnostic], None)
    diagnostics: list[Diagnostic] = []
    diagnostics.extend(scan_packet_for_forbidden_fields(packet.raw, source_path))
    diagnostics.extend(_scan_user_selected_profile_ids(packet.raw, source_path))
    _validate_context(packet, context, diagnostics, existing_bundle_allowed=existing_bundle_allowed)
    _validate_project_scope(packet, project or (context.project if context is not None else None), diagnostics)
    _validate_template(packet, template, diagnostics)
    _validate_role_bindings(packet, template, diagnostics)
    _validate_required_refs(packet, diagnostics)
    _validate_placeholders(packet, template, diagnostics, launch_facing=launch_facing)
    _validate_copied_material(packet, template, diagnostics)
    _validate_topic_edits(packet, diagnostics)
    _validate_approval(packet, diagnostics, launch_facing=launch_facing)
    return PacketValidationReport(
        packet_ref=str(source_path),
        source_path=source_path,
        ok=not has_errors(diagnostics),
        diagnostics=diagnostics,
        packet=packet,
        launch_blocker_refs=_launch_blocker_refs(packet),
    )


def _validate_context(
    packet: TopicTeamInstantiationPacket,
    context: EffectiveTopicContext | None,
    diagnostics: list[Diagnostic],
    *,
    existing_bundle_allowed: bool,
) -> None:
    if context is None:
        return
    if packet.research_topic_id != context.research_topic.id:
        diagnostics.append(
            Diagnostic(
                code="ISO019",
                severity="error",
                concept="Topic Team Instantiation Packet isolation",
                path=packet.source_path,
                field="research_topic_id",
                message="Packet Research Topic does not match the selected Effective Topic Context.",
            )
        )
    if packet.topic_workspace_ref != context.topic_workspace_id:
        diagnostics.append(
            Diagnostic(
                code="ISO019",
                severity="error",
                concept="Topic Team Instantiation Packet isolation",
                path=packet.source_path,
                field="topic_workspace_ref",
                message="Packet Topic Workspace ref does not match the selected Effective Topic Context.",
            )
        )
    target = resolve_project_path(context.project.root, packet.target_profile_bundle_path)
    expected = topic_profile_bundle_path(context)
    if canonicalize(target) != canonicalize(expected):
        diagnostics.append(
            Diagnostic(
                code="ISO019",
                severity="error",
                concept="Topic Agent Team Profile Bundle",
                path=packet.source_path,
                field="target_profile_bundle_path",
                message="Packet target must be the selected Research Topic's fixed Topic Workspace-local team-profile bundle path.",
            )
        )
    if not is_within(target, context.topic_workspace_path):
        diagnostics.append(
            Diagnostic(
                code="ISO019",
                severity="error",
                concept="Topic Agent Team Profile Bundle",
                path=packet.source_path,
                field="target_profile_bundle_path",
                message="Packet target resolves outside the selected Topic Workspace.",
            )
        )
    if not existing_bundle_allowed and (target / PROFILE_BUNDLE_PROFILE_FILENAME).exists():
        diagnostics.append(
            Diagnostic(
                code="ISO094",
                severity="error",
                concept="Topic Agent Team Profile Bundle",
                path=target / PROFILE_BUNDLE_PROFILE_FILENAME,
                field="target_profile_bundle_path",
                message="A Topic Agent Team Profile Bundle already exists for this Research Topic; topic-level parallelism requires another Research Topic.",
            )
        )


def _validate_project_scope(
    packet: TopicTeamInstantiationPacket,
    project: Project | None,
    diagnostics: list[Diagnostic],
) -> None:
    if project is None:
        return
    if project.manifest.first_topic(packet.research_topic_id) is None:
        diagnostics.append(
            Diagnostic(
                code="ISO020",
                severity="error",
                concept="Topic Team Instantiation Packet",
                path=packet.source_path,
                field="research_topic_id",
                message="Packet references an unregistered Research Topic.",
            )
        )
    workspace = project.manifest.first_workspace(packet.topic_workspace_ref)
    if workspace is not None and workspace.research_topic_id not in {None, packet.research_topic_id}:
        diagnostics.append(
            Diagnostic(
                code="ISO019",
                severity="error",
                concept="Topic Team Instantiation Packet isolation",
                path=packet.source_path,
                field="topic_workspace_ref",
                message="Packet Topic Workspace belongs to another Research Topic.",
            )
        )
    other_topic_ids = sorted(topic.id for topic in project.manifest.research_topics if topic.id != packet.research_topic_id)
    if other_topic_ids:
        _validate_topic_local_refs(packet, other_topic_ids, diagnostics)
    topic = project.manifest.first_topic(packet.research_topic_id)
    if topic is None:
        return
    _, workspace_path, _, workspace_diagnostics = resolve_topic_workspace(project, topic, packet.topic_workspace_ref)
    diagnostics.extend(workspace_diagnostics)
    if workspace_path is None:
        return
    _validate_agent_workspace_refs(
        packet,
        project=project,
        research_topic_id=packet.research_topic_id,
        topic_workspace_id=packet.topic_workspace_ref,
        topic_workspace_path=workspace_path,
        diagnostics=diagnostics,
    )


def _validate_template(
    packet: TopicTeamInstantiationPacket,
    template: DomainAgentTeamTemplate | None,
    diagnostics: list[Diagnostic],
) -> None:
    if template is not None and packet.source_template_ref != template.id:
        diagnostics.append(
            Diagnostic(
                code="ISO090",
                severity="error",
                concept="Topic Team Instantiation Packet",
                path=packet.source_path,
                field="source_template_ref",
                message="Packet source template ref does not match the selected Domain Agent Team Template.",
            )
        )


def _validate_role_bindings(
    packet: TopicTeamInstantiationPacket,
    template: DomainAgentTeamTemplate | None,
    diagnostics: list[Diagnostic],
) -> None:
    if not packet.role_bindings:
        diagnostics.append(
            Diagnostic(
                code="ISO090",
                severity="error",
                concept="Topic Team Instantiation Packet role bindings",
                path=packet.source_path,
                field="role_bindings",
                message="Packet must include role bindings for the topic team.",
            )
        )
        return
    if template is None:
        return
    by_role = {binding.role_id: binding for binding in packet.role_bindings}
    template_roles = {role.id: role for role in template.roles}
    for role in template.roles:
        binding = by_role.get(role.id)
        if binding is None:
            diagnostics.append(
                Diagnostic(
                    code="ISO090",
                    severity="error",
                    concept="Topic Team Instantiation Packet role bindings",
                    path=packet.source_path,
                    field=f"role_bindings.{role.id}",
                    message="Packet is missing a binding for a template Agent Role.",
                )
            )
            continue
        if role.required and not binding.active:
            diagnostics.append(
                Diagnostic(
                    code="ISO090",
                    severity="error",
                    concept="Topic Team Instantiation Packet role bindings",
                    path=packet.source_path,
                    field=f"role_bindings.{role.id}.active",
                    message="Required template Agent Role cannot be inactive in an authoritative packet.",
                )
            )
    for role_id in sorted(set(by_role) - set(template_roles)):
        diagnostics.append(
            Diagnostic(
                code="ISO090",
                severity="error",
                concept="Topic Team Instantiation Packet role bindings",
                path=packet.source_path,
                field=f"role_bindings.{role_id}",
                message="Packet contains a role not declared by the Domain Agent Team Template.",
            )
        )


def _validate_required_refs(packet: TopicTeamInstantiationPacket, diagnostics: list[Diagnostic]) -> None:
    for key in ("coordination_policy_ref", "gate_policy_ref"):
        if not packet.policy_refs.get(key):
            diagnostics.append(
                Diagnostic(
                    code="ISO090",
                    severity="error",
                    concept="Topic Team Instantiation Packet policy refs",
                    path=packet.source_path,
                    field=f"policy_refs.{key}",
                    message="Packet must resolve coordination and gate policy refs.",
                )
            )


def _validate_placeholders(
    packet: TopicTeamInstantiationPacket,
    template: DomainAgentTeamTemplate | None,
    diagnostics: list[Diagnostic],
    *,
    launch_facing: bool,
) -> None:
    deferred_names = {item.name for item in packet.deferrals}
    resolved = {item.name: item for item in packet.placeholder_resolutions}
    if template is not None:
        for parameter in template.parameters:
            if parameter.required_for_topic_profile and resolved.get(parameter.name) is None and parameter.name not in deferred_names:
                diagnostics.append(
                    Diagnostic(
                        code="ISO092",
                        severity="error",
                        concept="Topic Team Instantiation Packet placeholder",
                        path=packet.source_path,
                        field=f"placeholder_resolutions.{parameter.name}",
                        message="Required template placeholder is unresolved and not explicitly deferred.",
                    )
                )
            if launch_facing and parameter.blocks_launch and parameter.name in deferred_names:
                diagnostics.append(
                    Diagnostic(
                        code="ISO092",
                        severity="error",
                        concept="Topic Team Instantiation Packet placeholder",
                        path=packet.source_path,
                        field=f"deferrals.{parameter.name}",
                        message="Launch-facing validation cannot proceed while a launch-blocking placeholder is deferred.",
                    )
                )
    for item in [*packet.placeholder_resolutions, *packet.deferrals]:
        if item.deferred or item.name in deferred_names:
            missing = [
                name
                for name, value in (
                    ("reason", item.reason),
                    ("launch_impact", item.launch_impact),
                    ("required_action", item.required_action),
                )
                if value is None
            ]
            if missing:
                diagnostics.append(
                    Diagnostic(
                        code="ISO093",
                        severity="error",
                        concept="Topic Team Instantiation Packet deferral",
                        path=packet.source_path,
                        field=f"deferrals.{item.name}",
                        message=f"Deferred placeholders must include {', '.join(missing)}.",
                    )
                )
    for field_name, value in _string_values_for_placeholder_scan(packet):
        if _is_placeholder(value) and value.strip("{}") not in deferred_names:
            diagnostics.append(
                Diagnostic(
                    code="ISO092",
                    severity="error",
                    concept="Topic Team Instantiation Packet placeholder",
                    path=packet.source_path,
                    field=field_name,
                    message="Unresolved placeholder value is not explicitly deferred.",
                )
            )


def _validate_copied_material(
    packet: TopicTeamInstantiationPacket,
    template: DomainAgentTeamTemplate | None,
    diagnostics: list[Diagnostic],
) -> None:
    if template is None:
        return
    for index, item in enumerate(packet.copied_material):
        source_path = template.source_path / item.source_path_input.removeprefix("execplan/")
        if not is_within(source_path, template.source_path):
            diagnostics.append(
                Diagnostic(
                    code="ISO091",
                    severity="error",
                    concept="Topic Team Instantiation Packet copied material",
                    path=packet.source_path,
                    field=f"copied_material[{index}].source_path",
                    message="Copied material source path escapes the Domain Agent Team Template.",
                )
            )
        elif item.required and not source_path.exists():
            diagnostics.append(
                Diagnostic(
                    code="ISO091",
                    severity="error",
                    concept="Topic Team Instantiation Packet copied material",
                    path=source_path,
                    field=f"copied_material[{index}].source_path",
                    message="Required copied material source path does not exist.",
                )
            )
        if Path(item.target_path_input).is_absolute() or ".." in Path(item.target_path_input).parts:
            diagnostics.append(
                Diagnostic(
                    code="ISO091",
                    severity="error",
                    concept="Topic Team Instantiation Packet copied material",
                    path=packet.source_path,
                    field=f"copied_material[{index}].target_path",
                    message="Copied material target path must stay inside the Topic Agent Team Profile Bundle.",
                )
            )


def _validate_topic_edits(packet: TopicTeamInstantiationPacket, diagnostics: list[Diagnostic]) -> None:
    copied_targets = {item.target_path_input.rstrip("/") for item in packet.copied_material}
    for index, item in enumerate(packet.topic_edits):
        target = Path(item.target_path_input)
        if target.is_absolute() or ".." in target.parts:
            diagnostics.append(
                Diagnostic(
                    code="ISO091",
                    severity="error",
                    concept="Topic Team Instantiation Packet topic edits",
                    path=packet.source_path,
                    field=f"topic_edits[{index}].target_path",
                    message="Topic edit target path must stay inside copied Topic Agent Team Profile Bundle material.",
                )
            )
        if item.search is None and item.replace is not None:
            diagnostics.append(
                Diagnostic(
                    code="ISO091",
                    severity="error",
                    concept="Topic Team Instantiation Packet topic edits",
                    path=packet.source_path,
                    field=f"topic_edits[{index}].search",
                    message="Topic edit replacement requires a search string.",
                )
            )
        if copied_targets and not any(item.target_path_input == target_ref or item.target_path_input.startswith(f"{target_ref}/") for target_ref in copied_targets):
            diagnostics.append(
                Diagnostic(
                    code="ISO091",
                    severity="warning",
                    concept="Topic Team Instantiation Packet topic edits",
                    path=packet.source_path,
                    field=f"topic_edits[{index}].target_path",
                    message="Topic edit target is not covered by the copied material plan.",
                )
            )


def _validate_approval(
    packet: TopicTeamInstantiationPacket,
    diagnostics: list[Diagnostic],
    *,
    launch_facing: bool,
) -> None:
    if packet.approval.state == "approved":
        missing = [
            name
            for name, value in (
                ("approval_ref", packet.approval.approval_ref),
                ("approval_actor_ref", packet.approval.approval_actor_ref),
                ("approval_mode", packet.approval.approval_mode),
            )
            if value is None
        ]
        if missing:
            diagnostics.append(
                Diagnostic(
                    code="ISO095",
                    severity="error",
                    concept="Topic Team Instantiation Packet approval",
                    path=packet.source_path,
                    field="approval",
                    message=f"Approved packets must include {', '.join(missing)}.",
                )
            )
        return
    if launch_facing:
        diagnostics.append(
            Diagnostic(
                code="ISO095",
                severity="error",
                concept="Topic Team Instantiation Packet approval",
                path=packet.source_path,
                field="approval.state",
                message="Launch-facing use requires an approved packet with bundle-local approval provenance.",
            )
        )


def _validate_topic_local_refs(
    packet: TopicTeamInstantiationPacket,
    other_topic_ids: list[str],
    diagnostics: list[Diagnostic],
) -> None:
    for field_name, value in _string_values_for_placeholder_scan(packet):
        leaked_topic = next((topic_id for topic_id in other_topic_ids if _ref_encodes_topic_id(value, topic_id)), None)
        if leaked_topic is not None:
            diagnostics.append(
                Diagnostic(
                    code="ISO019",
                    severity="error",
                    concept="Topic Team Instantiation Packet isolation",
                    path=packet.source_path,
                    field=field_name,
                    message=f"Packet ref encodes another Research Topic id: {leaked_topic}.",
                )
            )


def _validate_agent_workspace_refs(
    packet: TopicTeamInstantiationPacket,
    *,
    project: Project,
    research_topic_id: str,
    topic_workspace_id: str,
    topic_workspace_path: Path,
    diagnostics: list[Diagnostic],
) -> None:
    for binding in packet.role_bindings:
        if not binding.active or binding.agent_workspace_ref is None:
            continue
        diagnostics.extend(
            validate_agent_workspace_ref_scope(
                project=project,
                research_topic_id=research_topic_id,
                topic_workspace_id=topic_workspace_id,
                topic_workspace_path=topic_workspace_path,
                workspace_ref=binding.agent_workspace_ref,
                source_path=packet.source_path,
                field=f"role_bindings.{binding.role_id}.agent_workspace_ref",
                concept="Topic Team Instantiation Packet isolation",
            )
        )


def _launch_blocker_refs(packet: TopicTeamInstantiationPacket) -> list[str]:
    return [f"placeholder:{item.name}" for item in packet.deferrals if item.launch_blocking]
