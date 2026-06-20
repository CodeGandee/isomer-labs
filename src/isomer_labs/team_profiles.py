"""Topic Agent Team Profile specialization and validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from isomer_labs.context import resolve_topic_workspace
from isomer_labs.diagnostics import Diagnostic, has_errors
from isomer_labs.models import (
    DomainAgentTeamTemplate,
    EffectiveTopicContext,
    FanoutPolicy,
    ProfileValidationReport,
    Project,
    RoleBinding,
    TOPIC_AGENT_TEAM_PROFILE_SCHEMA_VERSION,
    TopicAgentTeamProfile,
)


_PROFILE_RUNTIME_KEYS = {
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
    "managed_agent_id",
    "managed_agent_ids",
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


def parse_topic_agent_team_profile(
    path: Path,
    raw: dict[str, Any],
) -> tuple[TopicAgentTeamProfile | None, list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    diagnostics.extend(scan_profile_for_forbidden_fields(raw, path))
    data = _dict_value(raw.get("profile")) or raw
    profile_id = _string(data.get("id")) or _string(data.get("topic_agent_team_profile_id"))
    template_id = _string(data.get("domain_agent_team_template_id")) or _string(data.get("template_id"))
    research_topic_id = _string(data.get("research_topic_id")) or _string(data.get("topic_id"))
    missing: list[str] = []
    if profile_id is None:
        missing.append("id")
    if template_id is None:
        missing.append("domain_agent_team_template_id")
    if research_topic_id is None:
        missing.append("research_topic_id")
    if missing:
        diagnostics.append(
            Diagnostic(
                code="ISO020",
                severity="error",
                concept="Topic Agent Team Profile",
                path=path,
                message=f"Topic Agent Team Profile must include {', '.join(missing)}.",
            )
        )
        return None, diagnostics
    assert profile_id is not None
    assert template_id is not None
    assert research_topic_id is not None

    profile = TopicAgentTeamProfile(
        id=profile_id,
        domain_agent_team_template_id=template_id,
        research_topic_id=research_topic_id,
        topic_workspace_id=_string(data.get("topic_workspace_id")) or _string(data.get("topic_workspace_ref")),
        source_path=path,
        schema_version=_string(data.get("schema_version")) or TOPIC_AGENT_TEAM_PROFILE_SCHEMA_VERSION,
        role_bindings=_parse_role_bindings(data.get("role_bindings") or data.get("roles")),
        expected_artifacts=_string_list(data.get("expected_artifacts")),
        constraints=_string_list(data.get("constraints")),
        coordination_policy_ref=_string(data.get("coordination_policy_ref")),
        gate_policy_ref=_string(data.get("gate_policy_ref")),
        scheduler_policy_ref=_string(data.get("scheduler_policy_ref")),
        baseline_waiver_policy_ref=_string(data.get("baseline_waiver_policy_ref")),
        literature_provider_ref=_string(data.get("literature_provider_ref")),
        default_execution_mode=_string(data.get("default_execution_mode")),
        automatic_mode_policy_ref=_string(data.get("automatic_mode_policy_ref")),
        reviewer_read_access_policy=_string(data.get("reviewer_read_access_policy")),
        fanout_policies=_parse_fanout_policies(data.get("fanout_policies")),
        raw=raw,
    )
    return profile, diagnostics


def specialize_topic_agent_team_profile(
    context: EffectiveTopicContext,
    template: DomainAgentTeamTemplate,
    *,
    profile_id: str | None = None,
    selected_role_ids: list[str] | None = None,
    expected_artifacts: list[str] | None = None,
    use_case: str | None = None,
) -> TopicAgentTeamProfile:
    final_profile_id = profile_id or context.topic_agent_team_profile_id or f"{context.research_topic.id}-{template.id}"
    selected = set(selected_role_ids or [role.id for role in template.roles])
    profile_refs = context.profile_refs
    role_bindings: list[RoleBinding] = []
    for role in template.roles:
        role_active = role.id in selected
        role_bindings.append(
            RoleBinding(
                role_id=role.id,
                active=role_active,
                agent_profile_ref=_role_ref(profile_refs, "agent_profile_refs", role.id, f"{final_profile_id}:{role.id}:agent-profile"),
                capability_binding_ref=_role_ref(
                    profile_refs,
                    "capability_binding_refs",
                    role.id,
                    f"{final_profile_id}:{role.id}:capability-binding",
                ),
                skill_binding_projection_ref=_role_ref(
                    profile_refs,
                    "skill_binding_projection_refs",
                    role.id,
                    f"{final_profile_id}:{role.id}:skill-binding-projection",
                ),
                agent_workspace_ref=f"topic-workspaces/{context.research_topic.id}/agent-workspaces/{final_profile_id}/{role.id}",
                required_skills=list(role.required_skills),
                optional_skills=list(role.optional_skills),
            )
        )

    fanout_policies = [
        FanoutPolicy(
            role_id=role.id,
            parallel_execution_scope="research_task",
            max_shards=2,
            allocation_rule=f"{final_profile_id}:{role.id}:shard-agent-workspace-allocation",
        )
        for role in template.roles
        if role.scalable and role.id in selected
    ]
    artifacts = list(expected_artifacts or _default_expected_artifacts(use_case))
    constraints = [f"use_case:{use_case}"] if use_case else []
    return TopicAgentTeamProfile(
        id=final_profile_id,
        domain_agent_team_template_id=template.id,
        research_topic_id=context.research_topic.id,
        topic_workspace_id=context.topic_workspace_id,
        source_path=context.project.config_dir / "team-profiles" / f"{final_profile_id}.toml",
        schema_version=TOPIC_AGENT_TEAM_PROFILE_SCHEMA_VERSION,
        role_bindings=role_bindings,
        expected_artifacts=artifacts,
        constraints=constraints,
        coordination_policy_ref=_first_ref(profile_refs, "coordination_policy_ref", "coordination_policy_refs") or "coordination-policy:manual-review",
        gate_policy_ref=_first_ref(profile_refs, "gate_policy_ref", "gate_policy_refs") or "gate-policy:human-return",
        scheduler_policy_ref=_first_ref(profile_refs, "scheduler_policy_ref", "scheduler_policy_refs"),
        baseline_waiver_policy_ref=_first_ref(profile_refs, "baseline_waiver_policy_ref", "baseline_waiver_policy_refs"),
        literature_provider_ref=_first_ref(profile_refs, "literature_provider_ref", "literature_provider_refs"),
        default_execution_mode=template.default_execution_mode or "manual",
        automatic_mode_policy_ref=_first_ref(profile_refs, "automatic_mode_policy_ref", "automatic_mode_policy_refs"),
        reviewer_read_access_policy=_first_ref(profile_refs, "reviewer_read_access_policy") or "promoted-artifacts-only",
        fanout_policies=fanout_policies,
        raw={},
    )


def validate_topic_agent_team_profile(
    profile: TopicAgentTeamProfile | None,
    template: DomainAgentTeamTemplate | None,
    *,
    project: Project | None = None,
    source_path: Path | None = None,
) -> ProfileValidationReport:
    diagnostics: list[Diagnostic] = []
    if profile is None:
        return ProfileValidationReport(
            profile_id="unknown",
            source_path=source_path or Path("."),
            ok=False,
            diagnostics=[
                Diagnostic(
                    code="ISO020",
                    severity="error",
                    concept="Topic Agent Team Profile",
                    path=source_path,
                    message="Topic Agent Team Profile could not be parsed.",
                )
            ],
            profile=None,
        )
    if template is None:
        diagnostics.append(
            Diagnostic(
                code="ISO020",
                severity="error",
                concept="Topic Agent Team Profile",
                path=profile.source_path,
                field="domain_agent_team_template_id",
                message="Topic Agent Team Profile references a Domain Agent Team Template that could not be loaded.",
            )
        )
        return ProfileValidationReport(profile.id, profile.source_path, False, diagnostics, profile)

    if profile.domain_agent_team_template_id != template.id:
        diagnostics.append(
            Diagnostic(
                code="ISO020",
                severity="error",
                concept="Topic Agent Team Profile",
                path=profile.source_path,
                field="domain_agent_team_template_id",
                message="Topic Agent Team Profile template ref does not match the selected Domain Agent Team Template.",
            )
        )
    _validate_project_scope(profile, project, diagnostics)
    _validate_topic_local_refs(profile, project, diagnostics)
    _validate_roles(profile, template, diagnostics)
    _validate_fanout(profile, template, diagnostics)
    _validate_policy_posture(profile, diagnostics)
    return ProfileValidationReport(profile.id, profile.source_path, not has_errors(diagnostics), diagnostics, profile)


def profile_to_toml(profile: TopicAgentTeamProfile) -> str:
    lines = [
        f'schema_version = "{profile.schema_version}"',
        f'id = "{profile.id}"',
        f'domain_agent_team_template_id = "{profile.domain_agent_team_template_id}"',
        f'research_topic_id = "{profile.research_topic_id}"',
    ]
    if profile.topic_workspace_id is not None:
        lines.append(f'topic_workspace_id = "{profile.topic_workspace_id}"')
    for key, value in (
        ("coordination_policy_ref", profile.coordination_policy_ref),
        ("gate_policy_ref", profile.gate_policy_ref),
        ("scheduler_policy_ref", profile.scheduler_policy_ref),
        ("baseline_waiver_policy_ref", profile.baseline_waiver_policy_ref),
        ("literature_provider_ref", profile.literature_provider_ref),
        ("default_execution_mode", profile.default_execution_mode),
        ("automatic_mode_policy_ref", profile.automatic_mode_policy_ref),
        ("reviewer_read_access_policy", profile.reviewer_read_access_policy),
    ):
        if value is not None:
            lines.append(f'{key} = "{value}"')
    lines.append(_array_line("expected_artifacts", profile.expected_artifacts))
    lines.append(_array_line("constraints", profile.constraints))
    for binding in profile.role_bindings:
        lines.extend(
            [
                "",
                "[[role_bindings]]",
                f'role_id = "{binding.role_id}"',
                f"active = {str(binding.active).lower()}",
            ]
        )
        for key, value in (
            ("agent_profile_ref", binding.agent_profile_ref),
            ("capability_binding_ref", binding.capability_binding_ref),
            ("skill_binding_projection_ref", binding.skill_binding_projection_ref),
            ("agent_workspace_ref", binding.agent_workspace_ref),
        ):
            if value is not None:
                lines.append(f'{key} = "{value}"')
        lines.append(_array_line("required_skills", binding.required_skills))
        lines.append(_array_line("optional_skills", binding.optional_skills))
    for policy in profile.fanout_policies:
        lines.extend(
            [
                "",
                "[[fanout_policies]]",
                f'role_id = "{policy.role_id}"',
                f'parallel_execution_scope = "{policy.parallel_execution_scope}"',
            ]
        )
        if policy.max_shards is not None:
            lines.append(f"max_shards = {policy.max_shards}")
        if policy.allocation_rule is not None:
            lines.append(f'allocation_rule = "{policy.allocation_rule}"')
    return "\n".join(lines) + "\n"


def scan_profile_for_forbidden_fields(data: object, path: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    _scan_profile_for_forbidden_fields(data, path, (), diagnostics)
    return diagnostics


def _parse_role_bindings(value: object) -> list[RoleBinding]:
    return [
        RoleBinding(
            role_id=_string(item.get("role_id")) or _string(item.get("id")) or "",
            active=_bool(item.get("active"), default=True),
            agent_profile_ref=_string(item.get("agent_profile_ref")),
            capability_binding_ref=_string(item.get("capability_binding_ref")),
            skill_binding_projection_ref=_string(item.get("skill_binding_projection_ref")),
            agent_workspace_ref=_string(item.get("agent_workspace_ref")),
            required_skills=_string_list(item.get("required_skills")),
            optional_skills=_string_list(item.get("optional_skills")),
        )
        for item in _dict_items(value)
        if _string(item.get("role_id")) is not None or _string(item.get("id")) is not None
    ]


def _parse_fanout_policies(value: object) -> list[FanoutPolicy]:
    policies: list[FanoutPolicy] = []
    for item in _dict_items(value):
        role_id = _string(item.get("role_id"))
        scope = _string(item.get("parallel_execution_scope")) or _string(item.get("scope"))
        if role_id is None or scope is None:
            continue
        policies.append(
            FanoutPolicy(
                role_id=role_id,
                parallel_execution_scope=scope,
                max_shards=_int(item.get("max_shards")),
                allocation_rule=_string(item.get("allocation_rule")),
            )
        )
    return policies


def _validate_project_scope(
    profile: TopicAgentTeamProfile,
    project: Project | None,
    diagnostics: list[Diagnostic],
) -> None:
    if project is None:
        return
    topic = project.manifest.first_topic(profile.research_topic_id)
    if topic is None:
        diagnostics.append(
            Diagnostic(
                code="ISO020",
                severity="error",
                concept="Topic Agent Team Profile",
                path=profile.source_path,
                field="research_topic_id",
                message="Topic Agent Team Profile references an unregistered Research Topic.",
            )
        )
        return
    if profile.topic_workspace_id is not None:
        workspace, _, _, workspace_diagnostics = resolve_topic_workspace(project, topic, profile.topic_workspace_id)
        diagnostics.extend(workspace_diagnostics)
        if workspace is not None and workspace.research_topic_id not in {None, profile.research_topic_id}:
            diagnostics.append(
                Diagnostic(
                    code="ISO019",
                    severity="error",
                    concept="Topic Agent Team Profile isolation",
                    path=profile.source_path,
                    field="topic_workspace_id",
                    message="Topic Agent Team Profile references another Research Topic's Topic Workspace.",
                )
            )


def _validate_topic_local_refs(
    profile: TopicAgentTeamProfile,
    project: Project | None,
    diagnostics: list[Diagnostic],
) -> None:
    if project is None:
        return
    other_topic_ids = sorted(topic.id for topic in project.manifest.research_topics if topic.id != profile.research_topic_id)
    if not other_topic_ids:
        return
    for field_name, value in (
        ("coordination_policy_ref", profile.coordination_policy_ref),
        ("gate_policy_ref", profile.gate_policy_ref),
        ("scheduler_policy_ref", profile.scheduler_policy_ref),
        ("baseline_waiver_policy_ref", profile.baseline_waiver_policy_ref),
        ("literature_provider_ref", profile.literature_provider_ref),
        ("automatic_mode_policy_ref", profile.automatic_mode_policy_ref),
    ):
        _validate_topic_ref_value(profile, field_name, value, other_topic_ids, diagnostics)
    for index, artifact_ref in enumerate(profile.expected_artifacts):
        _validate_topic_ref_value(profile, f"expected_artifacts[{index}]", artifact_ref, other_topic_ids, diagnostics)
    for binding in profile.role_bindings:
        for field_name, value in (
            ("agent_profile_ref", binding.agent_profile_ref),
            ("capability_binding_ref", binding.capability_binding_ref),
            ("skill_binding_projection_ref", binding.skill_binding_projection_ref),
        ):
            _validate_topic_ref_value(
                profile,
                f"role_bindings.{binding.role_id}.{field_name}",
                value,
                other_topic_ids,
                diagnostics,
            )


def _validate_roles(
    profile: TopicAgentTeamProfile,
    template: DomainAgentTeamTemplate,
    diagnostics: list[Diagnostic],
) -> None:
    template_roles = {role.id: role for role in template.roles}
    profile_bindings = {binding.role_id: binding for binding in profile.role_bindings}
    for role in template.roles:
        binding = profile_bindings.get(role.id)
        if binding is None:
            diagnostics.append(
                Diagnostic(
                    code="ISO020",
                    severity="error",
                    concept="Topic Agent Team Profile role",
                    path=profile.source_path,
                    field=f"role_bindings.{role.id}",
                    message="Topic Agent Team Profile is missing a binding for a template Agent Role.",
                )
            )
            continue
        if role.required and not binding.active:
            diagnostics.append(
                Diagnostic(
                    code="ISO020",
                    severity="error",
                    concept="Topic Agent Team Profile role",
                    path=profile.source_path,
                    field=f"role_bindings.{role.id}.active",
                    message="Required template Agent Role is inactive in the Topic Agent Team Profile.",
                )
            )
        if binding.active:
            for field_name, value in (
                ("agent_profile_ref", binding.agent_profile_ref),
                ("capability_binding_ref", binding.capability_binding_ref),
                ("skill_binding_projection_ref", binding.skill_binding_projection_ref),
                ("agent_workspace_ref", binding.agent_workspace_ref),
            ):
                if value is None:
                    diagnostics.append(
                        Diagnostic(
                            code="ISO020",
                            severity="error",
                            concept="Topic Agent Team Profile role",
                            path=profile.source_path,
                            field=f"role_bindings.{role.id}.{field_name}",
                            message="Active Agent Role bindings must resolve profile, capability, skill projection, and Agent Workspace refs.",
                        )
                    )
            missing_skills = sorted(set(role.required_skills) - set(binding.required_skills))
            if missing_skills:
                diagnostics.append(
                    Diagnostic(
                        code="ISO020",
                        severity="error",
                        concept="Topic Agent Team Profile role",
                        path=profile.source_path,
                        field=f"role_bindings.{role.id}.required_skills",
                        message=f"Active Agent Role binding is missing required skill refs: {', '.join(missing_skills)}.",
                    )
                )
            if binding.agent_workspace_ref is not None:
                _validate_agent_workspace_topic(profile, role.id, binding.agent_workspace_ref, diagnostics)
    for role_id in sorted(set(profile_bindings) - set(template_roles)):
        diagnostics.append(
            Diagnostic(
                code="ISO020",
                severity="error",
                concept="Topic Agent Team Profile role",
                path=profile.source_path,
                field=f"role_bindings.{role_id}",
                message="Topic Agent Team Profile contains a role not declared by the Domain Agent Team Template.",
            )
        )


def _validate_fanout(
    profile: TopicAgentTeamProfile,
    template: DomainAgentTeamTemplate,
    diagnostics: list[Diagnostic],
) -> None:
    active = {binding.role_id for binding in profile.role_bindings if binding.active}
    policies = {policy.role_id: policy for policy in profile.fanout_policies}
    for role in template.roles:
        if not role.scalable or role.id not in active:
            continue
        policy = policies.get(role.id)
        if policy is None:
            diagnostics.append(
                Diagnostic(
                    code="ISO020",
                    severity="error",
                    concept="Topic Agent Team Profile fanout",
                    path=profile.source_path,
                    field=f"fanout_policies.{role.id}",
                    message="Active scalable Agent Role must declare a task-level fanout policy.",
                )
            )
            continue
        if policy.parallel_execution_scope not in {"research_task", "Research Task"}:
            diagnostics.append(
                Diagnostic(
                    code="ISO020",
                    severity="error",
                    concept="Topic Agent Team Profile fanout",
                    path=profile.source_path,
                    field=f"fanout_policies.{role.id}.parallel_execution_scope",
                    message="Fanout policy must use Research Task parallel execution scope.",
                )
            )
        if policy.max_shards is None and policy.allocation_rule is None:
            diagnostics.append(
                Diagnostic(
                    code="ISO020",
                    severity="error",
                    concept="Topic Agent Team Profile fanout",
                    path=profile.source_path,
                    field=f"fanout_policies.{role.id}",
                    message="Fanout policy must bound shards or name a future allocation rule.",
                )
            )


def _validate_policy_posture(profile: TopicAgentTeamProfile, diagnostics: list[Diagnostic]) -> None:
    if profile.default_execution_mode == "automatic" and profile.automatic_mode_policy_ref is None:
        diagnostics.append(
            Diagnostic(
                code="ISO020",
                severity="error",
                concept="Topic Agent Team Profile policy",
                path=profile.source_path,
                field="automatic_mode_policy_ref",
                message="Automatic mode requires an explicit automatic-mode policy ref.",
            )
        )
    reviewer_active = any(binding.role_id == "deepsci-org-reviewer" and binding.active for binding in profile.role_bindings)
    if reviewer_active and profile.reviewer_read_access_policy is None:
        diagnostics.append(
            Diagnostic(
                code="ISO020",
                severity="error",
                concept="Topic Agent Team Profile policy",
                path=profile.source_path,
                field="reviewer_read_access_policy",
                message="Reviewer read-access policy must be explicit.",
            )
        )
    if profile.coordination_policy_ref is None:
        diagnostics.append(
            Diagnostic(
                code="ISO020",
                severity="error",
                concept="Topic Agent Team Profile policy",
                path=profile.source_path,
                field="coordination_policy_ref",
                message="Topic Agent Team Profile must name a Coordination Policy ref.",
            )
        )
    if profile.gate_policy_ref is None:
        diagnostics.append(
            Diagnostic(
                code="ISO020",
                severity="error",
                concept="Topic Agent Team Profile policy",
                path=profile.source_path,
                field="gate_policy_ref",
                message="Topic Agent Team Profile must name a Gate Policy ref.",
            )
        )


def _validate_agent_workspace_topic(
    profile: TopicAgentTeamProfile,
    role_id: str,
    workspace_ref: str,
    diagnostics: list[Diagnostic],
) -> None:
    prefix = "topic-workspaces/"
    if not workspace_ref.startswith(prefix):
        return
    parts = workspace_ref.split("/")
    if len(parts) > 1 and parts[1] != profile.research_topic_id:
        diagnostics.append(
            Diagnostic(
                code="ISO019",
                severity="error",
                concept="Topic Agent Team Profile isolation",
                path=profile.source_path,
                field=f"role_bindings.{role_id}.agent_workspace_ref",
                message="Agent Workspace ref points at another Research Topic's Topic Workspace.",
            )
        )


def _validate_topic_ref_value(
    profile: TopicAgentTeamProfile,
    field: str,
    value: str | None,
    other_topic_ids: list[str],
    diagnostics: list[Diagnostic],
) -> None:
    if value is None:
        return
    leaked_topic = next((topic_id for topic_id in other_topic_ids if _ref_encodes_topic_id(value, topic_id)), None)
    if leaked_topic is None:
        return
    diagnostics.append(
        Diagnostic(
            code="ISO019",
            severity="error",
            concept="Topic Agent Team Profile isolation",
            path=profile.source_path,
            field=field,
            message=f"Topic-local ref encodes another Research Topic id: {leaked_topic}.",
        )
    )


def _ref_encodes_topic_id(value: str, topic_id: str) -> bool:
    normalized = value.replace("/", ":")
    tokens = [token for token in normalized.split(":") if token]
    return any(token == topic_id or token.startswith(f"{topic_id}-") or token.startswith(f"{topic_id}_") for token in tokens)


def _scan_profile_for_forbidden_fields(
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
                        concept="Topic Agent Team Profile",
                        path=path,
                        field=".".join(field_path),
                        message="Inline secret-like material is not allowed here; use a credential backend or a ref.",
                    )
                )
            if normalized_key in _PROFILE_RUNTIME_KEYS:
                diagnostics.append(
                    Diagnostic(
                        code="ISO009",
                        severity="error",
                        concept="Topic Agent Team Profile",
                        path=path,
                        field=".".join(field_path),
                        message="Runtime truth belongs in future Workspace Runtime records or adapter-backed Artifacts, not Topic Agent Team Profile configuration.",
                    )
                )
            _scan_profile_for_forbidden_fields(item, path, field_path, diagnostics)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _scan_profile_for_forbidden_fields(item, path, (*key_path, f"[{index}]"), diagnostics)


def _first_ref(refs: dict[str, object], *keys: str) -> str | None:
    for key in keys:
        value = refs.get(key)
        if isinstance(value, str) and value:
            return value
        if isinstance(value, list):
            first = next((item for item in value if isinstance(item, str) and item), None)
            if first is not None:
                return first
        if isinstance(value, dict):
            default = value.get("default")
            if isinstance(default, str) and default:
                return default
            first = next((item for item in value.values() if isinstance(item, str) and item), None)
            if first is not None:
                return first
    return None


def _role_ref(refs: dict[str, object], key: str, role_id: str, fallback: str) -> str:
    value = refs.get(key)
    if isinstance(value, dict):
        role_value = value.get(role_id) or value.get(role_id.removeprefix("deepsci-org-")) or value.get("default")
        if isinstance(role_value, str) and role_value:
            return role_value
    return fallback


def _default_expected_artifacts(use_case: str | None) -> list[str]:
    if use_case == "UC-01":
        return ["research-inquiry-map", "scout-report", "decision-record"]
    if use_case == "UC-02":
        return ["baseline-report", "metric-artifact", "optimization-frontier"]
    if use_case == "UC-03":
        return ["feedback-map", "claim-risk-register", "revision-plan"]
    if use_case == "UC-05":
        return ["manual-run-plan", "automatic-run-policy", "completion-watcher-contract"]
    return ["research-plan", "evidence-summary", "decision-record"]


def _array_line(key: str, values: list[str]) -> str:
    rendered = ", ".join(f'"{value}"' for value in values)
    return f"{key} = [{rendered}]"


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


def _int(value: object) -> int | None:
    if isinstance(value, int):
        return value
    return None


def _normalize_key(key: str) -> str:
    return key.lower().replace("-", "_").replace(" ", "_")
