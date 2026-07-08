"""Project Manifest, Research Topic Config, and local context validation."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from isomer_labs.workspace.surfaces import topic_workspace_path as default_topic_workspace_path
from isomer_labs.core.diagnostics import Diagnostic
from isomer_labs.models import Project, ProjectState, ResearchTopicConfig, TemplateValidationReport
from isomer_labs.core.path_utils import is_within, resolve_project_path
from isomer_labs.project import root_houmao_overlay_dir_for_root
from isomer_labs.teams.profiles import parse_topic_agent_team_profile, validate_topic_agent_team_profile
from isomer_labs.teams.templates import (
    discover_domain_agent_team_templates,
    find_domain_agent_team_template,
    resolve_template_source_path,
    validate_domain_agent_team_template,
)
from isomer_labs.core.toml_loader import load_toml
from isomer_labs.project.topic_config import parse_local_active_context, parse_research_topic_config
from isomer_labs.project.skill_callbacks import validate_callback_registry_refs
from isomer_labs.project.user_plugins import validate_project_user_plugins


SECRET_TERMS = (
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
RUNTIME_TRUTH_KEYS = {
    "run_status",
    "command_output",
    "command_outputs",
    "live_process_id",
    "live_process_ids",
    "resolved_command_result",
    "resolved_command_results",
    "artifact_contents",
    "evidence_items",
    "findings",
    "gates",
    "decision_records",
    "provenance_records",
    "scheduler_internals",
    "provider_payload",
    "provider_payloads",
    "pixi_install_output",
    "pixi_install_outputs",
    "pixi_prepared_environment_path",
    "pixi_prepared_environment_paths",
    "prepared_environment_path",
    "prepared_environment_paths",
    "environment_readiness",
    "environment_readiness_record",
    "environment_readiness_records",
    "environment_readiness_status",
    "mailbox_state",
    "gateway_state",
    "mailbox_ref",
    "gateway_ref",
    "agent_workspace_state",
    "agent_workspace_states",
    "agent_team_instance_state",
    "adapter_launch_ref",
    "launch_dossier_ref",
}
INLINE_CALLBACK_BODY_KEYS = {
    "callback_prompt",
    "callback_prompts",
    "callback_body",
    "callback_bodies",
    "callback_instruction",
    "callback_instructions",
    "user_skill_callback_prompt",
    "user_skill_callback_prompts",
    "user_skill_callback_body",
    "user_skill_callback_bodies",
    "user_skill_callback_instruction",
    "user_skill_callback_instructions",
    "external_skill_body",
    "external_skill_bodies",
    "external_skill_body_text",
}


def build_project_state(project: Project) -> ProjectState:
    diagnostics: list[Diagnostic] = []
    diagnostics.extend(scan_for_forbidden_fields(project.manifest.raw, "Project Manifest", project.manifest_path))
    diagnostics.extend(_validate_path_defaults(project))
    diagnostics.extend(_duplicate_id_diagnostics(project))
    diagnostics.extend(_validate_workspace_registrations(project))
    diagnostics.extend(_validate_environment_bindings(project))
    diagnostics.extend(_validate_template_registrations(project))
    diagnostics.extend(_validate_profile_registrations(project))
    diagnostics.extend(validate_project_user_plugins(project))

    topic_configs: dict[str, ResearchTopicConfig] = {}
    for topic in project.manifest.research_topics:
        config_path = resolve_project_path(project.root, topic.config_path_input)
        if not is_within(config_path, project.root):
            diagnostics.append(
                Diagnostic(
                    code="ISO005",
                    severity="error",
                    concept="Research Topic Config",
                    path=project.manifest_path,
                    field=f"research_topics.{topic.id}.config_path",
                    message="Research Topic Config path resolves outside the Project root.",
                )
            )
            continue
        raw, load_diagnostics = load_toml(config_path, "Research Topic Config")
        diagnostics.extend(load_diagnostics)
        if raw is None:
            continue
        diagnostics.extend(scan_for_forbidden_fields(raw, "Research Topic Config", config_path))
        config, parse_diagnostics = parse_research_topic_config(config_path, raw)
        diagnostics.extend(parse_diagnostics)
        if config is None:
            continue
        if config.research_topic_id != topic.id:
            diagnostics.append(
                Diagnostic(
                    code="ISO007",
                    severity="error",
                    concept="Research Topic Config",
                    path=config_path,
                    field="research_topic_id",
                    message="Research Topic Config research_topic_id does not match the Project Manifest registration.",
                )
            )
        topic_configs.setdefault(topic.id, config)

    diagnostics.extend(_validate_topic_config_profile_defaults(project, topic_configs))
    diagnostics.extend(validate_callback_registry_refs(project, topic_configs))
    diagnostics.extend(_validate_profile_files(project))

    local_context = None
    local_path = project.config_dir / "local.toml"
    if local_path.exists():
        raw, load_diagnostics = load_toml(local_path, "Local active context")
        diagnostics.extend(load_diagnostics)
        if raw is not None:
            diagnostics.extend(scan_for_forbidden_fields(raw, "Local active context", local_path))
            local_context, parse_diagnostics = parse_local_active_context(local_path, raw)
            diagnostics.extend(parse_diagnostics)

    return ProjectState(
        project=project,
        topic_configs=topic_configs,
        local_context=local_context,
        diagnostics=diagnostics,
    )


def scan_for_forbidden_fields(data: object, concept: str, path: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    _scan_for_forbidden_fields(data, concept, path, (), diagnostics)
    return diagnostics


def _duplicate_id_diagnostics(project: Project) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    topic_counts = Counter(topic.id for topic in project.manifest.research_topics)
    workspace_counts = Counter(workspace.id for workspace in project.manifest.topic_workspaces)
    template_counts = Counter(template.id for template in project.manifest.domain_agent_team_templates)
    profile_counts = Counter(profile.id for profile in project.manifest.topic_agent_team_profiles)
    for topic_id in sorted(id_ for id_, count in topic_counts.items() if count > 1):
        diagnostics.append(
            Diagnostic(
                code="ISO004",
                severity="error",
                concept="Project Manifest",
                path=project.manifest_path,
                field="research_topics.id",
                message=f"Duplicate Research Topic id is registered: {topic_id}.",
            )
        )
    for workspace_id in sorted(id_ for id_, count in workspace_counts.items() if count > 1):
        diagnostics.append(
            Diagnostic(
                code="ISO004",
                severity="error",
                concept="Project Manifest",
                path=project.manifest_path,
                field="topic_workspaces.id",
                message=f"Duplicate Topic Workspace id is registered: {workspace_id}.",
            )
        )
    for template_id in sorted(id_ for id_, count in template_counts.items() if count > 1):
        diagnostics.append(
            Diagnostic(
                code="ISO004",
                severity="error",
                concept="Project Manifest",
                path=project.manifest_path,
                field="domain_agent_team_templates.id",
                message=f"Duplicate Domain Agent Team Template id is registered: {template_id}.",
            )
        )
    for profile_id in sorted(id_ for id_, count in profile_counts.items() if count > 1):
        diagnostics.append(
            Diagnostic(
                code="ISO004",
                severity="error",
                concept="Project Manifest",
                path=project.manifest_path,
                field="topic_agent_team_profiles.id",
                message=f"Duplicate Topic Agent Team Profile id is registered: {profile_id}.",
            )
        )
    return diagnostics


def _validate_workspace_registrations(project: Project) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    topic_ids = {topic.id for topic in project.manifest.research_topics}
    for workspace in project.manifest.topic_workspaces:
        if workspace.path_input is not None:
            workspace_path = resolve_project_path(project.root, workspace.path_input)
            if not is_within(workspace_path, project.root):
                diagnostics.append(
                    Diagnostic(
                        code="ISO005",
                        severity="error",
                        concept="Topic Workspace",
                        path=project.manifest_path,
                        field=f"topic_workspaces.{workspace.id}.path",
                        message="Topic Workspace path resolves outside the Project root.",
                    )
                )
        if workspace.research_topic_id is not None and workspace.research_topic_id not in topic_ids:
            diagnostics.append(
                Diagnostic(
                    code="ISO008",
                    severity="error",
                    concept="Topic Workspace",
                    path=project.manifest_path,
                    field=f"topic_workspaces.{workspace.id}.research_topic_id",
                    message="Topic Workspace references an unregistered Research Topic.",
                )
            )

    workspace_ids = {workspace.id for workspace in project.manifest.topic_workspaces}
    for topic in project.manifest.research_topics:
        if topic.topic_workspace_id is not None and topic.topic_workspace_id not in workspace_ids:
            diagnostics.append(
                Diagnostic(
                    code="ISO008",
                    severity="error",
                    concept="Research Topic registration",
                    path=project.manifest_path,
                    field=f"research_topics.{topic.id}.topic_workspace_id",
                    message="Research Topic registration references a missing Topic Workspace.",
                )
            )
        if topic.topic_workspace_id is not None:
            referenced_workspace = project.manifest.first_workspace(topic.topic_workspace_id)
            if (
                referenced_workspace is not None
                and referenced_workspace.research_topic_id is not None
                and referenced_workspace.research_topic_id != topic.id
            ):
                diagnostics.append(
                    Diagnostic(
                        code="ISO012",
                        severity="error",
                        concept="Project Manifest",
                        path=project.manifest_path,
                        field=f"research_topics.{topic.id}.topic_workspace_id",
                        message="Research Topic registration references a Topic Workspace assigned to a different Research Topic.",
                    )
                )
    return diagnostics


def _validate_path_defaults(project: Project) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for key in ("isomer_content_root", "topic_workspace_base_dir"):
        if key not in project.manifest.path_defaults:
            continue
        value = project.manifest.path_defaults[key]
        field = f"paths.{key}"
        if not isinstance(value, str) or not value:
            diagnostics.append(
                Diagnostic(
                    code="ISO003",
                    severity="error",
                    concept="Project Manifest path default",
                    path=project.manifest_path,
                    field=field,
                    message="Project Manifest path default must be a non-empty string.",
                )
            )
            continue
        resolved = resolve_project_path(project.root, value)
        if not is_within(resolved, project.root):
            diagnostics.append(
                Diagnostic(
                    code="ISO005",
                    severity="error",
                    concept="Project Manifest path default",
                    path=project.manifest_path,
                    field=field,
                    message="Project Manifest path default resolves outside the Project root.",
                )
            )
        if key == "isomer_content_root" and is_within(resolved, project.config_dir):
            diagnostics.append(
                Diagnostic(
                    code="ISO005",
                    severity="error",
                    concept="Project generated content root",
                    path=project.manifest_path,
                    field=field,
                    message="Project generated content root must not live inside the Project Config Directory.",
                )
            )
        if key == "isomer_content_root" and is_within(resolved, root_houmao_overlay_dir_for_root(project.root)):
            diagnostics.append(
                Diagnostic(
                    code="ISO005",
                    severity="error",
                    concept="Project generated content root",
                    path=project.manifest_path,
                    field=field,
                    message="Project generated content root must not collide with root .houmao external Houmao state.",
                )
            )
    return diagnostics


def _validate_environment_bindings(project: Project) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    topic_ids = {topic.id for topic in project.manifest.research_topics}
    project_binding_keys = Counter(
        (binding.research_topic_id, binding.pixi_environment, binding.purpose or "")
        for binding in project.manifest.topic_pixi_environment_bindings
        if binding.status == "active"
    )
    standalone_binding_keys = Counter(
        (
            binding.research_topic_id,
            binding.manifest_path_or_dir_input,
            binding.pixi_environment or "",
            binding.purpose or "",
        )
        for binding in project.manifest.topic_standalone_pixi_bindings
        if binding.status == "active"
    )

    for project_binding in project.manifest.topic_pixi_environment_bindings:
        if project_binding.status == "archived":
            continue
        if project_binding.research_topic_id not in topic_ids:
            diagnostics.append(
                Diagnostic(
                    code="ISO008",
                    severity="error",
                    concept="Topic Pixi environment binding",
                    path=project.manifest_path,
                    field=f"topic_pixi_environment_bindings.{project_binding.research_topic_id}.research_topic_id",
                    message="Topic Pixi environment binding references an unregistered Research Topic.",
                )
            )

    for standalone_binding in project.manifest.topic_standalone_pixi_bindings:
        if standalone_binding.status == "archived":
            continue
        if standalone_binding.research_topic_id not in topic_ids:
            diagnostics.append(
                Diagnostic(
                    code="ISO008",
                    severity="error",
                    concept="Topic standalone Pixi binding",
                    path=project.manifest_path,
                    field=f"topic_standalone_pixi_bindings.{standalone_binding.research_topic_id}.research_topic_id",
                    message="Topic standalone Pixi binding references an unregistered Research Topic.",
                )
            )
        resolved_target_path = resolve_project_path(project.root, standalone_binding.manifest_path_or_dir_input)
        if not is_within(resolved_target_path, project.root):
            diagnostics.append(
                Diagnostic(
                    code="ISO005",
                    severity="error",
                    concept="Topic standalone Pixi binding",
                    path=project.manifest_path,
                    field=f"topic_standalone_pixi_bindings.{standalone_binding.research_topic_id}.manifest_path_or_dir",
                    message="Standalone Pixi binding target resolves outside the Project root.",
                )
            )

    for research_topic_id, pixi_environment, purpose in sorted(
        key for key, count in project_binding_keys.items() if count > 1
    ):
        diagnostics.append(
            Diagnostic(
                code="ISO004",
                severity="error",
                concept="Topic Pixi environment binding",
                path=project.manifest_path,
                field="topic_pixi_environment_bindings",
                message=(
                    "Duplicate active Topic Pixi environment binding is registered: "
                    f"{research_topic_id}/{pixi_environment}/{purpose or 'default'}."
                ),
            )
        )

    for research_topic_id, target_path_input, pixi_environment, purpose in sorted(
        key for key, count in standalone_binding_keys.items() if count > 1
    ):
        diagnostics.append(
            Diagnostic(
                code="ISO004",
                severity="error",
                concept="Topic standalone Pixi binding",
                path=project.manifest_path,
                field="topic_standalone_pixi_bindings",
                message=(
                    "Duplicate active Topic standalone Pixi binding is registered: "
                    f"{research_topic_id}/{target_path_input}/{pixi_environment or 'default'}/{purpose or 'default'}."
                ),
            )
        )
    return diagnostics


def _validate_template_registrations(project: Project) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for template in project.manifest.domain_agent_team_templates:
        if template.status == "archived":
            continue
        source_path = resolve_template_source_path(project, template)
        if template.source_kind != "team-repository" and not is_within(source_path, project.root):
            diagnostics.append(
                Diagnostic(
                    code="ISO016",
                    severity="error",
                    concept="Domain Agent Team Template registration",
                    path=project.manifest_path,
                    field=f"domain_agent_team_templates.{template.id}.source_path",
                    message="Domain Agent Team Template source path resolves outside the Project root.",
                )
            )
        if _is_under_topic_workspace(project, source_path):
            diagnostics.append(
                Diagnostic(
                    code="ISO016",
                    severity="error",
                    concept="Domain Agent Team Template registration",
                    path=project.manifest_path,
                    field=f"domain_agent_team_templates.{template.id}.source_path",
                    message="Domain Agent Team Template source must not live inside a Topic Workspace.",
                )
            )
    return diagnostics


def _validate_profile_registrations(project: Project) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    topic_ids = {topic.id for topic in project.manifest.research_topics}
    template_ids = _registered_template_ids(project)
    active_bundle_paths_by_topic: dict[str, list[Path]] = {}
    for profile in project.manifest.topic_agent_team_profiles:
        if profile.status == "archived":
            continue
        profile_path = resolve_project_path(project.root, profile.path_input)
        if _is_topic_profile_bundle_path(project, profile.research_topic_id, profile_path):
            active_bundle_paths_by_topic.setdefault(profile.research_topic_id, []).append(profile_path)
            expected_path = _topic_profile_bundle_path(project, profile.research_topic_id)
            if expected_path is not None and profile_path != expected_path:
                diagnostics.append(
                    Diagnostic(
                        code="ISO019",
                        severity="error",
                        concept="Topic Agent Team Profile Bundle registration",
                        path=project.manifest_path,
                        field=f"topic_agent_team_profiles.{profile.id}.path",
                        message="Topic Agent Team Profile Bundle registration must point at the owning Topic Workspace team-profile/profile.toml path.",
                    )
                )
        if not is_within(profile_path, project.root):
            diagnostics.append(
                Diagnostic(
                    code="ISO019",
                    severity="error",
                    concept="Topic Agent Team Profile registration",
                    path=project.manifest_path,
                    field=f"topic_agent_team_profiles.{profile.id}.path",
                    message="Topic Agent Team Profile path resolves outside the Project root.",
                )
            )
        if _is_under_topic_workspace_teams(project, profile_path):
            diagnostics.append(
                Diagnostic(
                    code="ISO019",
                    severity="error",
                    concept="Topic Agent Team Profile registration",
                    path=project.manifest_path,
                    field=f"topic_agent_team_profiles.{profile.id}.path",
                    message="Topic Agent Team Profile files must not live under a Topic Workspace teams directory.",
                )
            )
        if profile.research_topic_id not in topic_ids:
            diagnostics.append(
                Diagnostic(
                    code="ISO020",
                    severity="error",
                    concept="Topic Agent Team Profile registration",
                    path=project.manifest_path,
                    field=f"topic_agent_team_profiles.{profile.id}.research_topic_id",
                    message="Topic Agent Team Profile references an unregistered Research Topic.",
                )
            )
        if profile.domain_agent_team_template_id not in template_ids:
            diagnostics.append(
                Diagnostic(
                    code="ISO020",
                    severity="error",
                    concept="Topic Agent Team Profile registration",
                    path=project.manifest_path,
                    field=f"topic_agent_team_profiles.{profile.id}.domain_agent_team_template_id",
                    message="Topic Agent Team Profile references an unregistered Domain Agent Team Template.",
                )
            )
    for topic_id, paths in sorted(active_bundle_paths_by_topic.items()):
        if len(paths) <= 1:
            continue
        diagnostics.append(
            Diagnostic(
                code="ISO094",
                severity="error",
                concept="Topic Agent Team Profile Bundle registration",
                path=project.manifest_path,
                field=f"topic_agent_team_profiles.{topic_id}",
                message="A Research Topic can register only one active Topic Agent Team Profile Bundle; topic-level parallelism requires another Research Topic.",
            )
        )
    return diagnostics


def _validate_topic_config_profile_defaults(
    project: Project,
    topic_configs: dict[str, ResearchTopicConfig],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    template_ids = _registered_template_ids(project)
    for topic_id, config in sorted(topic_configs.items()):
        profile_id = config.default_topic_agent_team_profile_id()
        if profile_id is None:
            continue
        profile = project.manifest.first_topic_agent_team_profile(profile_id)
        if profile is None:
            diagnostics.append(
                Diagnostic(
                    code="ISO020",
                    severity="error",
                    concept="Research Topic Config",
                    path=config.source_path,
                    field="default_topic_agent_team_profile_id",
                    message="Research Topic Config references an unknown default Topic Agent Team Profile.",
                )
            )
            continue
        if profile.research_topic_id != topic_id:
            diagnostics.append(
                Diagnostic(
                    code="ISO019",
                    severity="error",
                    concept="Research Topic Config",
                    path=config.source_path,
                    field="default_topic_agent_team_profile_id",
                    message="Default Topic Agent Team Profile belongs to a different Research Topic.",
                )
            )
        if profile.domain_agent_team_template_id not in template_ids:
            diagnostics.append(
                Diagnostic(
                    code="ISO020",
                    severity="error",
                    concept="Research Topic Config",
                    path=config.source_path,
                    field="default_topic_agent_team_profile_id",
                    message="Default Topic Agent Team Profile specializes an unregistered Domain Agent Team Template.",
                )
            )
    return diagnostics


def _validate_profile_files(project: Project) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    template_reports: dict[str, TemplateValidationReport] = {}
    for profile_ref in project.manifest.topic_agent_team_profiles:
        if profile_ref.status == "archived":
            continue
        path = resolve_project_path(project.root, profile_ref.path_input)
        if not is_within(path, project.root) or _is_under_topic_workspace_teams(project, path):
            continue
        raw, load_diagnostics = load_toml(path, "Topic Agent Team Profile")
        diagnostics.extend(load_diagnostics)
        if raw is None:
            continue
        profile, parse_diagnostics = parse_topic_agent_team_profile(path, raw)
        diagnostics.extend(parse_diagnostics)
        registration = find_domain_agent_team_template(profile_ref.domain_agent_team_template_id, project)
        template = None
        if registration is not None:
            report = template_reports.get(registration.id)
            if report is None:
                report = validate_domain_agent_team_template(project, registration, include_harness=False)
                template_reports[registration.id] = report
            diagnostics.extend(report.diagnostics)
            template = report.template
        profile_report = validate_topic_agent_team_profile(profile, template, project=project, source_path=path)
        diagnostics.extend(profile_report.diagnostics)
        if profile is not None:
            if profile.id != profile_ref.id:
                diagnostics.append(
                    Diagnostic(
                        code="ISO020",
                        severity="error",
                        concept="Topic Agent Team Profile",
                        path=path,
                        field="id",
                        message="Topic Agent Team Profile id does not match the Project Manifest registration.",
                    )
                )
            if profile.research_topic_id != profile_ref.research_topic_id:
                diagnostics.append(
                    Diagnostic(
                        code="ISO019",
                        severity="error",
                        concept="Topic Agent Team Profile isolation",
                        path=path,
                        field="research_topic_id",
                        message="Topic Agent Team Profile Research Topic does not match its Project Manifest registration.",
                    )
                )
    return diagnostics


def _registered_template_ids(project: Project) -> set[str]:
    return {template.id for template in discover_domain_agent_team_templates(project)}


def _is_under_topic_workspace_teams(project: Project, path: Path) -> bool:
    for workspace_path in _topic_workspace_paths(project):
        if is_within(path, workspace_path / "teams"):
            return True
    return False


def _is_under_topic_workspace(project: Project, path: Path) -> bool:
    return any(is_within(path, workspace_path) for workspace_path in _topic_workspace_paths(project))


def _is_topic_profile_bundle_path(project: Project, topic_id: str, path: Path) -> bool:
    expected = _topic_profile_bundle_path(project, topic_id)
    if expected is not None and path == expected:
        return True
    return path.name == "profile.toml" and path.parent.name == "team-profile" and _is_under_topic_workspace(project, path)


def _topic_profile_bundle_path(project: Project, topic_id: str) -> Path | None:
    topic = project.manifest.first_topic(topic_id)
    if topic is None:
        return None
    workspace = project.manifest.first_workspace(topic.topic_workspace_id) if topic.topic_workspace_id is not None else None
    if workspace is None:
        matching = [workspace for workspace in project.manifest.topic_workspaces if workspace.research_topic_id == topic_id]
        if len(matching) == 1:
            workspace = matching[0]
    if workspace is not None and workspace.path_input is not None:
        return resolve_project_path(project.root, workspace.path_input) / "team-profile" / "profile.toml"
    return default_topic_workspace_path(project.root, topic_id, project.manifest.path_defaults) / "team-profile" / "profile.toml"


def _topic_workspace_paths(project: Project) -> list[Path]:
    paths: list[Path] = []
    for workspace in project.manifest.topic_workspaces:
        if workspace.path_input is not None:
            paths.append(resolve_project_path(project.root, workspace.path_input))
        elif workspace.research_topic_id is not None:
            paths.append(default_topic_workspace_path(project.root, workspace.research_topic_id, project.manifest.path_defaults))
    for topic in project.manifest.research_topics:
        paths.append(default_topic_workspace_path(project.root, topic.id, project.manifest.path_defaults))
    return paths


def _scan_for_forbidden_fields(
    value: object,
    concept: str,
    path: Path,
    key_path: tuple[str, ...],
    diagnostics: list[Diagnostic],
) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            field_path = (*key_path, str(key))
            normalized_key = _normalize_key(str(key))
            field = ".".join(field_path)
            if _is_secret_key(normalized_key):
                diagnostics.append(
                    Diagnostic(
                        code="ISO010",
                        severity="error",
                        concept=concept,
                        path=path,
                        field=field,
                        message="Inline secret-like material is not allowed here; use a credential backend or a ref.",
                    )
                )
            if normalized_key in RUNTIME_TRUTH_KEYS:
                diagnostics.append(
                    Diagnostic(
                        code="ISO009",
                        severity="error",
                        concept=concept,
                        path=path,
                        field=field,
                        message="Runtime truth belongs in future Workspace Runtime records or file-backed Artifacts, not configuration.",
                    )
                )
            if normalized_key in INLINE_CALLBACK_BODY_KEYS:
                diagnostics.append(
                    Diagnostic(
                        code="ISO009",
                        severity="error",
                        concept=concept,
                        path=path,
                        field=field,
                        message="User Skill Callback instruction bodies belong in managed callback registry content, not Project or Research Topic configuration.",
                    )
                )
            _scan_for_forbidden_fields(item, concept, path, field_path, diagnostics)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _scan_for_forbidden_fields(item, concept, path, (*key_path, f"[{index}]"), diagnostics)


def _is_secret_key(normalized_key: str) -> bool:
    return any(term in normalized_key for term in SECRET_TERMS)


def _normalize_key(key: str) -> str:
    return key.lower().replace("-", "_").replace(" ", "_")
