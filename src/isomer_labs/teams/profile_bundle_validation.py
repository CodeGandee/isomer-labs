"""Topic Agent Team Profile Bundle validation helpers."""

from __future__ import annotations

from isomer_labs.project.context import resolve_topic_workspace
from isomer_labs.core.diagnostics import Diagnostic
from isomer_labs.models import Project, TopicAgentTeamProfile
from isomer_labs.core.path_utils import canonicalize, is_within


def validate_bundle_layout(
    profile: TopicAgentTeamProfile,
    project: Project | None,
    diagnostics: list[Diagnostic],
) -> None:
    if profile.profile_bundle_ref is None or project is None:
        return
    topic = project.manifest.first_topic(profile.research_topic_id)
    if topic is None:
        return
    workspace, workspace_path, _, workspace_diagnostics = resolve_topic_workspace(project, topic, profile.topic_workspace_id)
    diagnostics.extend(workspace_diagnostics)
    if workspace_path is None:
        return
    profile_path = canonicalize(profile.source_path)
    expected_profile_path = canonicalize(workspace_path / "team-profile" / "profile.toml")
    if profile_path != expected_profile_path:
        diagnostics.append(
            Diagnostic(
                code="ISO019",
                severity="error",
                concept="Topic Agent Team Profile Bundle",
                path=profile.source_path,
                field="path",
                message="Authoritative Topic Agent Team Profile Bundle profile must live at the selected Topic Workspace team-profile/profile.toml path.",
            )
        )
    bundle_path = canonicalize(profile_path.parent)
    if not is_within(bundle_path, workspace_path):
        diagnostics.append(
            Diagnostic(
                code="ISO019",
                severity="error",
                concept="Topic Agent Team Profile Bundle",
                path=profile.source_path,
                field="profile_bundle_ref",
                message="Topic Agent Team Profile Bundle path resolves outside the selected Topic Workspace.",
            )
        )
    if workspace is not None and workspace.research_topic_id not in {None, profile.research_topic_id}:
        diagnostics.append(
            Diagnostic(
                code="ISO019",
                severity="error",
                concept="Topic Agent Team Profile Bundle",
                path=profile.source_path,
                field="topic_workspace_id",
                message="Topic Agent Team Profile Bundle references another Research Topic's Topic Workspace.",
            )
        )


def validate_profile_provenance(
    profile: TopicAgentTeamProfile,
    diagnostics: list[Diagnostic],
    *,
    launch_facing: bool,
) -> None:
    if profile.raw.get("preview") is True and launch_facing:
        diagnostics.append(
            Diagnostic(
                code="ISO097",
                severity="error",
                concept="Topic Agent Team Profile",
                path=profile.source_path,
                field="profile_materialization",
                message="Preview-only Topic Agent Team Profile material cannot be used for launch-facing Agent Team Instance creation.",
            )
        )
    if profile.profile_bundle_ref is None:
        return
    missing: list[str] = []
    if profile.instantiation_packet_ref is None:
        missing.append("instantiation_packet_ref")
    if profile.approval_ref is None:
        missing.append("approval_ref")
    if profile.approval_mode is None:
        missing.append("approval_mode")
    if missing:
        diagnostics.append(
            Diagnostic(
                code="ISO095",
                severity="error" if launch_facing else "warning",
                concept="Topic Agent Team Profile provenance",
                path=profile.source_path,
                field="profile_bundle_ref",
                message=f"Packet-backed profile bundle is missing {', '.join(missing)}.",
            )
        )


def validate_unresolved_placeholders(
    profile: TopicAgentTeamProfile,
    diagnostics: list[Diagnostic],
    *,
    launch_facing: bool,
) -> None:
    deferrals = {ref.removeprefix("placeholder:") for ref in profile.launch_blocker_refs}
    for field_name, value in _profile_string_values(profile):
        if not _is_placeholder(value):
            continue
        placeholder_name = value.strip("{}")
        if placeholder_name in deferrals:
            if launch_facing:
                diagnostics.append(
                    Diagnostic(
                        code="ISO092",
                        severity="error",
                        concept="Topic Agent Team Profile placeholder",
                        path=profile.source_path,
                        field=field_name,
                        message="Launch-facing Topic Agent Team Profile still has a deferred launch-blocking placeholder.",
                    )
                )
            continue
        diagnostics.append(
            Diagnostic(
                code="ISO092",
                severity="error" if launch_facing else "warning",
                concept="Topic Agent Team Profile placeholder",
                path=profile.source_path,
                field=field_name,
                message="Topic Agent Team Profile contains an unresolved placeholder without packet deferral provenance.",
            )
        )


def _profile_string_values(profile: TopicAgentTeamProfile) -> list[tuple[str, str]]:
    values: list[tuple[str, str]] = []
    for field_name, value in (
        ("profile_bundle_ref", profile.profile_bundle_ref),
        ("instantiation_packet_ref", profile.instantiation_packet_ref),
        ("approval_ref", profile.approval_ref),
        ("coordination_policy_ref", profile.coordination_policy_ref),
        ("gate_policy_ref", profile.gate_policy_ref),
        ("scheduler_policy_ref", profile.scheduler_policy_ref),
        ("baseline_waiver_policy_ref", profile.baseline_waiver_policy_ref),
        ("literature_provider_ref", profile.literature_provider_ref),
        ("automatic_mode_policy_ref", profile.automatic_mode_policy_ref),
    ):
        if value is not None:
            values.append((field_name, value))
    for index, artifact_ref in enumerate(profile.expected_artifacts):
        values.append((f"expected_artifacts[{index}]", artifact_ref))
    for binding in profile.role_bindings:
        for field_name, value in (
            ("agent_profile_ref", binding.agent_profile_ref),
            ("capability_binding_ref", binding.capability_binding_ref),
            ("skill_binding_projection_ref", binding.skill_binding_projection_ref),
            ("agent_name", binding.agent_name),
            ("agent_branch", binding.agent_branch),
            ("agent_workspace_ref", binding.agent_workspace_ref),
        ):
            if value is not None:
                values.append((f"role_bindings.{binding.role_id}.{field_name}", value))
    return values


def _is_placeholder(value: str) -> bool:
    stripped = value.strip()
    return stripped.startswith("{") and stripped.endswith("}")
