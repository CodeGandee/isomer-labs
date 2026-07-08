"""User Plugin registration and runtime-param helpers."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, replace
from pathlib import Path
import re
from typing import Any, Iterable, Mapping, TypeAlias

import tomlkit

from isomer_labs.core.diagnostics import Diagnostic, has_errors
from isomer_labs.core.path_utils import canonicalize, is_within
from isomer_labs.core.toml_loader import load_toml
from isomer_labs.models import (
    EffectiveTopicContext,
    Project,
    UserPluginRegistration,
    UserPluginRuntimeParam,
    UserPluginRuntimeParamImport,
)
from isomer_labs.project.callback_keys import CALLBACK_PLUGIN_ID_RE
from isomer_labs.project.skill_callbacks import secret_like_diagnostics


USER_PLUGIN_STATUS_VALUES = ("active", "disabled")
USER_PLUGIN_RUNTIME_PARAM_IMPORT_SCHEMA_VERSION = "isomer-user-plugin-runtime-params.v1"
PROJECT_RUNTIME_PARAM_SCOPES = ("project",)
TOPIC_RUNTIME_PARAM_SCOPES = ("research_topic", "topic_actor", "topic_agent")
RUNTIME_PARAM_SCOPES = PROJECT_RUNTIME_PARAM_SCOPES + TOPIC_RUNTIME_PARAM_SCOPES
RUNTIME_PARAM_VALUE_TYPES = ("string", "bool", "integer", "number", "enum", "string_list")
PARAM_KEY_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_/-]*$")
TOPIC_SELECTOR_SCOPES = {"topic_actor", "topic_agent"}
UserPluginConfigRow: TypeAlias = UserPluginRegistration | UserPluginRuntimeParamImport | UserPluginRuntimeParam


@dataclass(frozen=True)
class UserPluginEffectiveStatus:
    plugin_id: str
    status: str
    source: str
    registration: UserPluginRegistration | None = None
    diagnostics: tuple[Diagnostic, ...] = ()

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "plugin_id": self.plugin_id,
            "status": self.status,
            "source": self.source,
        }
        if self.registration is not None:
            data["registration"] = self.registration.to_json()
        if self.diagnostics:
            data["diagnostics"] = [diagnostic.to_json() for diagnostic in self.diagnostics]
        return data


@dataclass(frozen=True)
class RuntimeParamCandidate:
    layer: str
    param: UserPluginRuntimeParam

    def to_json(self) -> dict[str, object]:
        data = self.param.to_json()
        data["layer"] = self.layer
        return data


@dataclass(frozen=True)
class EffectiveRuntimeParam:
    param_id: str
    plugin_id: str
    key: str
    value: Any
    value_type: str
    effective_scope: str
    selected: UserPluginRuntimeParam
    candidates: tuple[RuntimeParamCandidate, ...]
    overridden: tuple[RuntimeParamCandidate, ...]
    diagnostics: tuple[Diagnostic, ...] = ()

    def to_json(self, *, explain: bool = False) -> dict[str, object]:
        data: dict[str, object] = {
            "param_id": self.param_id,
            "plugin_id": self.plugin_id,
            "key": self.key,
            "value": self.value,
            "value_type": self.value_type,
            "effective_scope": self.effective_scope,
            "source": self.selected.to_json(),
            "diagnostics": [diagnostic.to_json() for diagnostic in self.diagnostics],
        }
        if explain:
            data["candidates"] = [candidate.to_json() for candidate in self.candidates]
            data["overridden"] = [candidate.to_json() for candidate in self.overridden]
        return data


@dataclass(frozen=True)
class RuntimeParamResolution:
    params: tuple[EffectiveRuntimeParam, ...]
    candidates: tuple[RuntimeParamCandidate, ...]
    diagnostics: tuple[Diagnostic, ...]

    @property
    def ok(self) -> bool:
        return not any(diagnostic.is_error for diagnostic in self.diagnostics)

    def get(self, param_id: str) -> EffectiveRuntimeParam | None:
        return next((param for param in self.params if param.param_id == param_id), None)

    def to_json(self, *, explain: bool = False) -> dict[str, object]:
        return {
            "ok": self.ok,
            "params": [param.to_json(explain=explain) for param in self.params],
            "diagnostics": [diagnostic.to_json() for diagnostic in self.diagnostics],
        }


@dataclass(frozen=True)
class UserPluginCommandResult:
    ok: bool
    mutated: bool
    project_root: Path
    diagnostics: tuple[Diagnostic, ...] = ()
    plugins: tuple[UserPluginRegistration, ...] = ()
    plugin_statuses: tuple[dict[str, object], ...] = ()
    params: tuple[EffectiveRuntimeParam, ...] = ()
    param_candidates: tuple[RuntimeParamCandidate, ...] = ()
    imports: tuple[UserPluginRuntimeParamImport, ...] = ()
    plugin: UserPluginRegistration | None = None
    param: EffectiveRuntimeParam | None = None
    import_ref: UserPluginRuntimeParamImport | None = None

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "ok": self.ok,
            "mutated": self.mutated,
            "project_root": str(self.project_root),
            "diagnostics": [diagnostic.to_json() for diagnostic in self.diagnostics],
        }
        if self.plugins:
            data["plugins"] = [plugin.to_json() for plugin in self.plugins]
        if self.plugin_statuses:
            data["plugin_statuses"] = list(self.plugin_statuses)
        if self.params:
            data["params"] = [param.to_json() for param in self.params]
        if self.param_candidates:
            data["param_candidates"] = [candidate.to_json() for candidate in self.param_candidates]
        if self.imports:
            data["imports"] = [import_ref.to_json() for import_ref in self.imports]
        if self.plugin is not None:
            data["plugin"] = self.plugin.to_json()
        if self.param is not None:
            data["param"] = self.param.to_json(explain=True)
        if self.import_ref is not None:
            data["import"] = self.import_ref.to_json()
        return data


def parse_user_plugin_registrations(
    path: Path,
    raw: Mapping[str, Any],
    *,
    default_scope: str,
) -> list[UserPluginRegistration]:
    registrations: list[UserPluginRegistration] = []
    for index, item in enumerate(_table_items(raw.get("user_plugins"))):
        plugin_id = _string(item.get("plugin_id") or item.get("id"))
        if plugin_id is None:
            continue
        source_path_input = _string(item.get("source_path") or item.get("path") or item.get("plugin_dir"))
        registrations.append(
            UserPluginRegistration(
                plugin_id=plugin_id,
                scope=_string(item.get("scope")) or default_scope,
                status=_string(item.get("status")) or "active",
                source_path_input=source_path_input,
                source_path=path,
                topic_actor_name=_string(item.get("topic_actor_name")),
                topic_agent_name=_string(item.get("topic_agent_name") or item.get("agent_name")),
                source_detail=f"{path.name}:user_plugins[{index}]",
            )
        )
    return registrations


def parse_user_plugin_runtime_param_imports(
    path: Path,
    raw: Mapping[str, Any],
    *,
    default_scope: str,
) -> list[UserPluginRuntimeParamImport]:
    imports: list[UserPluginRuntimeParamImport] = []
    for index, item in enumerate(_table_items(raw.get("user_plugin_runtime_param_imports"))):
        plugin_id = _string(item.get("plugin_id") or item.get("id"))
        path_input = _string(item.get("path") or item.get("import_path"))
        if plugin_id is None or path_input is None:
            continue
        imports.append(
            UserPluginRuntimeParamImport(
                plugin_id=plugin_id,
                path_input=path_input,
                scope=_string(item.get("scope")) or default_scope,
                status=_string(item.get("status")) or "active",
                source_path=path,
                topic_actor_name=_string(item.get("topic_actor_name")),
                topic_agent_name=_string(item.get("topic_agent_name") or item.get("agent_name")),
                source_detail=f"{path.name}:user_plugin_runtime_param_imports[{index}]",
            )
        )
    return imports


def parse_user_plugin_runtime_params(
    path: Path,
    raw: Mapping[str, Any],
    *,
    default_scope: str,
    imported_from: Path | None = None,
) -> list[UserPluginRuntimeParam]:
    params: list[UserPluginRuntimeParam] = []
    for index, item in enumerate(_table_items(raw.get("user_plugin_runtime_params"))):
        plugin_id = _string(item.get("plugin_id") or item.get("id"))
        key = _string(item.get("key") or item.get("param_key") or item.get("name"))
        if plugin_id is None or key is None or "value" not in item:
            continue
        params.append(
            UserPluginRuntimeParam(
                plugin_id=plugin_id,
                key=key,
                value=item.get("value"),
                scope=_string(item.get("scope")) or default_scope,
                status=_string(item.get("status")) or "active",
                value_type=_string(item.get("value_type") or item.get("type")),
                allowed_values=_string_tuple(item.get("allowed_values")),
                description=_string(item.get("description")),
                source_path=path,
                topic_actor_name=_string(item.get("topic_actor_name")),
                topic_agent_name=_string(item.get("topic_agent_name") or item.get("agent_name")),
                source_detail=f"{path.name}:user_plugin_runtime_params[{index}]",
                imported_from=imported_from,
            )
        )
    return params


def validate_user_plugin_tables(
    *,
    project: Project,
    context: EffectiveTopicContext | None = None,
    registrations: Iterable[UserPluginRegistration],
    imports: Iterable[UserPluginRuntimeParamImport],
    params: Iterable[UserPluginRuntimeParam],
    source_path: Path,
    allowed_scopes: tuple[str, ...],
    concept: str,
    broader_definitions: Mapping[str, UserPluginRuntimeParam] | None = None,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    rows: list[UserPluginConfigRow] = [*registrations, *imports, *params]
    diagnostics.extend(secret_like_diagnostics([_row_scan_payload(row) for row in rows], concept, source_path, ()))
    for row in rows:
        diagnostics.extend(_validate_plugin_id(row.plugin_id, concept, source_path, "plugin_id"))
        if row.scope not in allowed_scopes:
            diagnostics.append(
                Diagnostic(
                    code="ISO103",
                    severity="error",
                    concept=concept,
                    path=source_path,
                    field="scope",
                    message=f"User Plugin scope `{row.scope}` is not allowed in this manifest.",
                )
            )
        if getattr(row, "status", "active") not in USER_PLUGIN_STATUS_VALUES:
            diagnostics.append(
                Diagnostic(
                    code="ISO103",
                    severity="error",
                    concept=concept,
                    path=source_path,
                    field="status",
                    message="User Plugin status must be active or disabled.",
                )
            )
        diagnostics.extend(_selector_diagnostics(row, source_path, concept, context))
    for import_ref in imports:
        diagnostics.extend(_validate_import_ref(project, import_ref, allowed_scopes, concept))
    broader = broader_definitions or {}
    for param in params:
        diagnostics.extend(_validate_param_identity(param, source_path, concept))
        inherited = broader.get(param.param_id)
        diagnostics.extend(_validate_param_value(param, source_path, concept, inherited=inherited))
        if allowed_scopes == TOPIC_RUNTIME_PARAM_SCOPES and inherited is None and not _self_defining(param):
            diagnostics.append(
                Diagnostic(
                    code="ISO103",
                    severity="error",
                    concept=concept,
                    path=source_path,
                    field=param.param_id,
                    message="Topic-scope runtime param without a broader definition must include complete definition metadata.",
                )
            )
    diagnostics.extend(_duplicate_active_row_diagnostics(params, source_path, concept))
    diagnostics.extend(_duplicate_active_plugin_diagnostics(registrations, source_path, concept))
    return diagnostics


def validate_project_user_plugins(project: Project) -> list[Diagnostic]:
    return validate_user_plugin_tables(
        project=project,
        registrations=project.manifest.user_plugins,
        imports=project.manifest.user_plugin_runtime_param_imports,
        params=project.manifest.user_plugin_runtime_params,
        source_path=project.manifest_path,
        allowed_scopes=PROJECT_RUNTIME_PARAM_SCOPES,
        concept="Project Manifest User Plugin configuration",
    )


def load_imported_runtime_params(
    project: Project,
    import_ref: UserPluginRuntimeParamImport,
    *,
    allowed_scopes: tuple[str, ...],
    layer: str,
) -> tuple[list[RuntimeParamCandidate], list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    import_path = Path(import_ref.path_input)
    if import_path.is_absolute():
        diagnostics.append(
            Diagnostic(
                code="ISO005",
                severity="error",
                concept="User Plugin runtime param import",
                path=import_ref.source_path,
                field="path",
                message="Runtime param import path must be relative to the declaring manifest file.",
            )
        )
        return [], diagnostics
    resolved = canonicalize(import_ref.source_path.parent / import_path)
    if not is_within(resolved, project.root):
        diagnostics.append(
            Diagnostic(
                code="ISO005",
                severity="error",
                concept="User Plugin runtime param import",
                path=import_ref.source_path,
                field="path",
                message="Runtime param import path must resolve inside the Project root.",
            )
        )
        return [], diagnostics
    raw, load_diagnostics = load_toml(resolved, "User Plugin runtime param import")
    diagnostics.extend(load_diagnostics)
    if raw is None:
        return [], diagnostics
    schema_version = _string(raw.get("schema_version"))
    if schema_version is not None and schema_version != USER_PLUGIN_RUNTIME_PARAM_IMPORT_SCHEMA_VERSION:
        diagnostics.append(
            Diagnostic(
                code="ISO102",
                severity="error",
                concept="User Plugin runtime param import",
                path=resolved,
                field="schema_version",
                message=f"Runtime param import schema_version must be {USER_PLUGIN_RUNTIME_PARAM_IMPORT_SCHEMA_VERSION}.",
            )
        )
    unsupported = sorted(key for key in raw if key not in {"schema_version", "user_plugin_runtime_params"})
    if unsupported:
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="User Plugin runtime param import",
                path=resolved,
                message=f"Runtime param imports may contain only param rows; unsupported fields: {', '.join(unsupported)}.",
            )
        )
    params = [
        replace(param, imported_from=resolved, source_path=resolved)
        for param in parse_user_plugin_runtime_params(resolved, raw, default_scope=import_ref.scope, imported_from=resolved)
        if param.plugin_id == import_ref.plugin_id
    ]
    diagnostics.extend(
        validate_user_plugin_tables(
            project=project,
            registrations=(),
            imports=(),
            params=params,
            source_path=resolved,
            allowed_scopes=allowed_scopes,
            concept="User Plugin runtime param import",
        )
    )
    return [RuntimeParamCandidate(layer=layer, param=param) for param in params if param.status == "active"], diagnostics


def resolve_runtime_params(
    project: Project,
    context: EffectiveTopicContext | None = None,
    *,
    topic_actor_name: str | None = None,
    topic_agent_name: str | None = None,
) -> RuntimeParamResolution:
    diagnostics: list[Diagnostic] = []
    candidates: list[RuntimeParamCandidate] = []
    for import_ref in project.manifest.user_plugin_runtime_param_imports:
        if import_ref.status == "active":
            imported, import_diagnostics = load_imported_runtime_params(
                project,
                import_ref,
                allowed_scopes=PROJECT_RUNTIME_PARAM_SCOPES,
                layer="project_import",
            )
            candidates.extend(imported)
            diagnostics.extend(import_diagnostics)
    candidates.extend(
        RuntimeParamCandidate("project_explicit", param)
        for param in project.manifest.user_plugin_runtime_params
        if param.status == "active"
    )
    if context is not None:
        from isomer_labs.workspace.manifest import load_topic_workspace_manifest

        manifest, manifest_diagnostics = load_topic_workspace_manifest(context)
        diagnostics.extend(manifest_diagnostics)
        for import_ref in manifest.user_plugin_runtime_param_imports:
            if import_ref.status == "active" and _matches_topic_selector(import_ref, topic_actor_name, topic_agent_name):
                imported, import_diagnostics = load_imported_runtime_params(
                    project,
                    import_ref,
                    allowed_scopes=TOPIC_RUNTIME_PARAM_SCOPES,
                    layer="topic_import",
                )
                candidates.extend(candidate for candidate in imported if _matches_topic_selector(candidate.param, topic_actor_name, topic_agent_name))
                diagnostics.extend(import_diagnostics)
        candidates.extend(
            RuntimeParamCandidate("topic_explicit", param)
            for param in manifest.user_plugin_runtime_params
            if param.status == "active" and _matches_topic_selector(param, topic_actor_name, topic_agent_name)
        )
    selected_by_id: dict[str, EffectiveRuntimeParam] = {}
    grouped: dict[str, list[RuntimeParamCandidate]] = {}
    for candidate in candidates:
        grouped.setdefault(candidate.param.param_id, []).append(candidate)
    for param_id, group in sorted(grouped.items()):
        selected = group[-1].param
        inherited = _definition_source(group)
        value_type = selected.value_type or inherited.value_type if inherited is not None else selected.value_type
        if value_type is None:
            value_type = infer_value_type(selected.value)
        selected_by_id[param_id] = EffectiveRuntimeParam(
            param_id=param_id,
            plugin_id=selected.plugin_id,
            key=selected.key,
            value=selected.value,
            value_type=value_type,
            effective_scope=selected.scope,
            selected=selected,
            candidates=tuple(group),
            overridden=tuple(group[:-1]),
            diagnostics=tuple(_validate_param_value(selected, selected.source_path, "User Plugin runtime param", inherited=inherited)),
        )
    diagnostics.extend(diagnostic for param in selected_by_id.values() for diagnostic in param.diagnostics)
    return RuntimeParamResolution(
        params=tuple(selected_by_id[param_id] for param_id in sorted(selected_by_id)),
        candidates=tuple(candidates),
        diagnostics=tuple(diagnostics),
    )


def effective_user_plugin_status(
    project: Project,
    context: EffectiveTopicContext | None,
    plugin_id: str,
    *,
    topic_actor_name: str | None = None,
    topic_agent_name: str | None = None,
) -> UserPluginEffectiveStatus:
    registrations = [registration for registration in project.manifest.user_plugins if registration.plugin_id == plugin_id and registration.status in USER_PLUGIN_STATUS_VALUES]
    if context is not None:
        from isomer_labs.workspace.manifest import load_topic_workspace_manifest

        manifest, diagnostics = load_topic_workspace_manifest(context)
        registrations.extend(
            registration
            for registration in manifest.user_plugins
            if registration.plugin_id == plugin_id
            and registration.status in USER_PLUGIN_STATUS_VALUES
            and _matches_topic_selector(registration, topic_actor_name, topic_agent_name)
        )
        if registrations:
            selected = registrations[-1]
            return UserPluginEffectiveStatus(plugin_id, selected.status, "registration", selected, tuple(diagnostics))
        return UserPluginEffectiveStatus(plugin_id, "active", "missing-registration", None, tuple(diagnostics))
    if registrations:
        selected = registrations[-1]
        return UserPluginEffectiveStatus(plugin_id, selected.status, "registration", selected, ())
    return UserPluginEffectiveStatus(plugin_id, "active", "missing-registration", None, ())


def parse_param_id(param_id: str) -> tuple[str, str] | None:
    if ":" not in param_id:
        return None
    plugin_id, key = param_id.split(":", 1)
    if not CALLBACK_PLUGIN_ID_RE.match(plugin_id) or not PARAM_KEY_RE.match(key):
        return None
    return plugin_id, key


def infer_value_type(value: Any) -> str:
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int) and not isinstance(value, bool):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return "string_list"
    return "string"


def ensure_user_plugin_registration(
    project: Project,
    context: EffectiveTopicContext | None,
    *,
    plugin_id: str,
    source_path_input: str | None,
    scope: str,
    status: str = "active",
) -> tuple[UserPluginRegistration | None, list[Diagnostic]]:
    if scope == "project":
        path = project.manifest_path
        row = _registration_row(plugin_id, source_path_input, scope, status)
        diagnostics = _upsert_toml_row(path, "user_plugins", row, _plugin_row_matches(plugin_id, scope, None, None))
        registration = UserPluginRegistration(plugin_id, scope, status, source_path_input, path)
        return registration, diagnostics
    if context is None:
        return None, [
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="User Plugin registration",
                field="scope",
                message="Topic-scoped User Plugin registration requires a selected Research Topic.",
            )
        ]
    from isomer_labs.workspace.manifest import topic_workspace_manifest_path

    path = topic_workspace_manifest_path(context.topic_workspace_path)
    row = _registration_row(plugin_id, source_path_input, "research_topic", status)
    diagnostics = _upsert_toml_row(path, "user_plugins", row, _plugin_row_matches(plugin_id, "research_topic", None, None))
    registration = UserPluginRegistration(plugin_id, "research_topic", status, source_path_input, path)
    return registration, diagnostics


def upsert_user_plugin_registration(
    project: Project,
    context: EffectiveTopicContext | None,
    *,
    plugin_id: str,
    source_path_input: str | None,
    scope: str,
    status: str,
    topic_actor_name: str | None = None,
    topic_agent_name: str | None = None,
) -> UserPluginCommandResult:
    diagnostics = _mutation_scope_diagnostics(context, scope, topic_actor_name, topic_agent_name)
    if diagnostics:
        return UserPluginCommandResult(False, False, project.root, tuple(diagnostics))
    path = _manifest_path_for_mutation(project, context, scope)
    row = _registration_row(plugin_id, source_path_input, scope, status, topic_actor_name, topic_agent_name)
    diagnostics.extend(_validate_plugin_id(plugin_id, "User Plugin registration", path, "plugin_id"))
    if status not in USER_PLUGIN_STATUS_VALUES:
        diagnostics.append(Diagnostic(code="ISO103", severity="error", concept="User Plugin registration", path=path, field="status", message="User Plugin status must be active or disabled."))
    if has_errors(diagnostics):
        return UserPluginCommandResult(False, False, project.root, tuple(diagnostics))
    diagnostics.extend(_upsert_toml_row(path, "user_plugins", row, _plugin_row_matches(plugin_id, scope, topic_actor_name, topic_agent_name)))
    plugin = UserPluginRegistration(plugin_id, scope, status, source_path_input, path, topic_actor_name, topic_agent_name)
    return UserPluginCommandResult(not has_errors(diagnostics), not has_errors(diagnostics), project.root, tuple(diagnostics), plugins=(plugin,), plugin=plugin)


def remove_user_plugin_registration(
    project: Project,
    context: EffectiveTopicContext | None,
    *,
    plugin_id: str,
    scope: str,
    topic_actor_name: str | None = None,
    topic_agent_name: str | None = None,
) -> UserPluginCommandResult:
    diagnostics = _mutation_scope_diagnostics(context, scope, topic_actor_name, topic_agent_name)
    if diagnostics:
        return UserPluginCommandResult(False, False, project.root, tuple(diagnostics))
    path = _manifest_path_for_mutation(project, context, scope)
    diagnostics.extend(_remove_toml_rows(path, "user_plugins", _plugin_row_matches(plugin_id, scope, topic_actor_name, topic_agent_name)))
    return UserPluginCommandResult(not has_errors(diagnostics), not has_errors(diagnostics), project.root, tuple(diagnostics))


def set_runtime_param(
    project: Project,
    context: EffectiveTopicContext | None,
    *,
    plugin_id: str,
    key: str,
    value: Any,
    scope: str,
    value_type: str | None,
    allowed_values: tuple[str, ...] = (),
    description: str | None = None,
    topic_actor_name: str | None = None,
    topic_agent_name: str | None = None,
) -> UserPluginCommandResult:
    diagnostics = _mutation_scope_diagnostics(context, scope, topic_actor_name, topic_agent_name)
    path = _manifest_path_for_mutation(project, context, scope) if not diagnostics else project.manifest_path
    temp = UserPluginRuntimeParam(
        plugin_id=plugin_id,
        key=key,
        value=value,
        scope=scope,
        source_path=path,
        status="active",
        value_type=value_type,
        allowed_values=allowed_values,
        description=description,
        topic_actor_name=topic_actor_name,
        topic_agent_name=topic_agent_name,
    )
    diagnostics.extend(_validate_param_identity(temp, path, "User Plugin runtime param"))
    diagnostics.extend(_validate_param_value(temp, path, "User Plugin runtime param", inherited=None))
    diagnostics.extend(secret_like_diagnostics(_row_scan_payload(temp), "User Plugin runtime param", path, ()))
    if has_errors(diagnostics):
        return UserPluginCommandResult(False, False, project.root, tuple(diagnostics))
    row = _param_row(temp)
    diagnostics.extend(_upsert_toml_row(path, "user_plugin_runtime_params", row, _param_row_matches(plugin_id, key, scope, topic_actor_name, topic_agent_name)))
    candidate = RuntimeParamCandidate("written", temp)
    effective = EffectiveRuntimeParam(
        param_id=temp.param_id,
        plugin_id=temp.plugin_id,
        key=temp.key,
        value=temp.value,
        value_type=temp.value_type or infer_value_type(temp.value),
        effective_scope=temp.scope,
        selected=temp,
        candidates=(candidate,),
        overridden=(),
    )
    return UserPluginCommandResult(
        not has_errors(diagnostics),
        not has_errors(diagnostics),
        project.root,
        tuple(diagnostics),
        params=(effective,),
        param=effective,
    )


def unset_runtime_param(
    project: Project,
    context: EffectiveTopicContext | None,
    *,
    plugin_id: str,
    key: str,
    scope: str,
    topic_actor_name: str | None = None,
    topic_agent_name: str | None = None,
) -> UserPluginCommandResult:
    diagnostics = _mutation_scope_diagnostics(context, scope, topic_actor_name, topic_agent_name)
    if diagnostics:
        return UserPluginCommandResult(False, False, project.root, tuple(diagnostics))
    path = _manifest_path_for_mutation(project, context, scope)
    diagnostics.extend(_remove_toml_rows(path, "user_plugin_runtime_params", _param_row_matches(plugin_id, key, scope, topic_actor_name, topic_agent_name)))
    return UserPluginCommandResult(not has_errors(diagnostics), not has_errors(diagnostics), project.root, tuple(diagnostics))


def add_runtime_param_import(
    project: Project,
    context: EffectiveTopicContext | None,
    *,
    plugin_id: str,
    path_input: str,
    scope: str,
    topic_actor_name: str | None = None,
    topic_agent_name: str | None = None,
) -> UserPluginCommandResult:
    diagnostics = _mutation_scope_diagnostics(context, scope, topic_actor_name, topic_agent_name)
    path = _manifest_path_for_mutation(project, context, scope) if not diagnostics else project.manifest_path
    import_ref = UserPluginRuntimeParamImport(plugin_id, path_input, scope, path, "active", topic_actor_name, topic_agent_name)
    diagnostics.extend(_validate_plugin_id(plugin_id, "User Plugin runtime param import", path, "plugin_id"))
    diagnostics.extend(_validate_import_ref(project, import_ref, PROJECT_RUNTIME_PARAM_SCOPES if scope == "project" else TOPIC_RUNTIME_PARAM_SCOPES, "User Plugin runtime param import"))
    if has_errors(diagnostics):
        return UserPluginCommandResult(False, False, project.root, tuple(diagnostics))
    row = _import_row(import_ref)
    diagnostics.extend(_upsert_toml_row(path, "user_plugin_runtime_param_imports", row, _import_row_matches(plugin_id, path_input, scope, topic_actor_name, topic_agent_name)))
    return UserPluginCommandResult(not has_errors(diagnostics), not has_errors(diagnostics), project.root, tuple(diagnostics), imports=(import_ref,), import_ref=import_ref)


def remove_runtime_param_import(
    project: Project,
    context: EffectiveTopicContext | None,
    *,
    plugin_id: str,
    path_input: str,
    scope: str,
    topic_actor_name: str | None = None,
    topic_agent_name: str | None = None,
) -> UserPluginCommandResult:
    diagnostics = _mutation_scope_diagnostics(context, scope, topic_actor_name, topic_agent_name)
    if diagnostics:
        return UserPluginCommandResult(False, False, project.root, tuple(diagnostics))
    path = _manifest_path_for_mutation(project, context, scope)
    diagnostics.extend(_remove_toml_rows(path, "user_plugin_runtime_param_imports", _import_row_matches(plugin_id, path_input, scope, topic_actor_name, topic_agent_name)))
    return UserPluginCommandResult(not has_errors(diagnostics), not has_errors(diagnostics), project.root, tuple(diagnostics))


def _validate_import_ref(
    project: Project,
    import_ref: UserPluginRuntimeParamImport,
    allowed_scopes: tuple[str, ...],
    concept: str,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if import_ref.scope not in allowed_scopes:
        return diagnostics
    import_path = Path(import_ref.path_input)
    if import_path.is_absolute():
        diagnostics.append(Diagnostic(code="ISO005", severity="error", concept=concept, path=import_ref.source_path, field="path", message="Runtime param import path must be relative to the declaring manifest file."))
        return diagnostics
    resolved = canonicalize(import_ref.source_path.parent / import_path)
    if not is_within(resolved, project.root):
        diagnostics.append(Diagnostic(code="ISO005", severity="error", concept=concept, path=import_ref.source_path, field="path", message="Runtime param import path must resolve inside the Project root."))
        return diagnostics
    if not resolved.is_file():
        diagnostics.append(Diagnostic(code="ISO001", severity="error", concept=concept, path=resolved, field="path", message="Runtime param import file does not exist."))
    return diagnostics


def _validate_plugin_id(plugin_id: str, concept: str, path: Path, field: str) -> list[Diagnostic]:
    if CALLBACK_PLUGIN_ID_RE.match(plugin_id):
        return []
    return [
        Diagnostic(
            code="ISO103",
            severity="error",
            concept=concept,
            path=path,
            field=field,
            message="User Plugin plugin_id must start with an alphanumeric character and contain only letters, numbers, underscore, dot, or dash.",
        )
    ]


def _validate_param_identity(param: UserPluginRuntimeParam, path: Path, concept: str) -> list[Diagnostic]:
    diagnostics = _validate_plugin_id(param.plugin_id, concept, path, "plugin_id")
    if not PARAM_KEY_RE.match(param.key):
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept=concept,
                path=path,
                field="key",
                message="Runtime param key must start with an alphanumeric character and contain only letters, numbers, slash, underscore, or dash.",
            )
        )
    return diagnostics


def _validate_param_value(
    param: UserPluginRuntimeParam,
    path: Path,
    concept: str,
    *,
    inherited: UserPluginRuntimeParam | None,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    value_type = param.value_type or inherited.value_type if inherited is not None else param.value_type
    allowed_values = param.allowed_values or inherited.allowed_values if inherited is not None else param.allowed_values
    if value_type is None:
        value_type = infer_value_type(param.value)
    if value_type not in RUNTIME_PARAM_VALUE_TYPES:
        diagnostics.append(Diagnostic(code="ISO103", severity="error", concept=concept, path=path, field=param.param_id, message=f"Unsupported runtime param value_type: {value_type}."))
        return diagnostics
    if value_type == "string" and not isinstance(param.value, str):
        diagnostics.append(_type_diagnostic(concept, path, param, "a string"))
    if value_type == "bool" and not isinstance(param.value, bool):
        diagnostics.append(_type_diagnostic(concept, path, param, "a boolean"))
    if value_type == "integer" and (not isinstance(param.value, int) or isinstance(param.value, bool)):
        diagnostics.append(_type_diagnostic(concept, path, param, "an integer"))
    if value_type == "number" and (not isinstance(param.value, int | float) or isinstance(param.value, bool)):
        diagnostics.append(_type_diagnostic(concept, path, param, "a number"))
    if value_type == "string_list" and (not isinstance(param.value, list) or not all(isinstance(item, str) for item in param.value)):
        diagnostics.append(_type_diagnostic(concept, path, param, "a list of strings"))
    if value_type == "enum":
        if not allowed_values:
            diagnostics.append(Diagnostic(code="ISO103", severity="error", concept=concept, path=path, field=param.param_id, message="Enum runtime params must define allowed_values."))
        elif not isinstance(param.value, str) or param.value not in allowed_values:
            diagnostics.append(Diagnostic(code="ISO103", severity="error", concept=concept, path=path, field=param.param_id, message=f"Enum runtime param value must be one of: {', '.join(allowed_values)}."))
    if inherited is not None and param.value_type is not None and inherited.value_type is not None and param.value_type != inherited.value_type:
        diagnostics.append(Diagnostic(code="ISO103", severity="error", concept=concept, path=path, field=param.param_id, message="Runtime param override value_type must match the broader definition."))
    return diagnostics


def _type_diagnostic(concept: str, path: Path, param: UserPluginRuntimeParam, expected: str) -> Diagnostic:
    return Diagnostic(code="ISO103", severity="error", concept=concept, path=path, field=param.param_id, message=f"Runtime param value must be {expected}.")


def _selector_diagnostics(row: object, source_path: Path, concept: str, context: EffectiveTopicContext | None) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    scope = getattr(row, "scope")
    topic_actor_name = getattr(row, "topic_actor_name", None)
    topic_agent_name = getattr(row, "topic_agent_name", None)
    if scope == "topic_actor":
        if topic_actor_name is None:
            diagnostics.append(Diagnostic(code="ISO103", severity="error", concept=concept, path=source_path, field="topic_actor_name", message="topic_actor scope requires topic_actor_name."))
        elif context is not None:
            from isomer_labs.workspace.manifest import load_topic_workspace_manifest

            manifest, _ = load_topic_workspace_manifest(context)
            if manifest.topic_actor_binding_for(topic_actor_name) is None:
                diagnostics.append(Diagnostic(code="ISO103", severity="error", concept=concept, path=source_path, field="topic_actor_name", message=f"Unknown Topic Actor binding: {topic_actor_name}."))
    if scope == "topic_agent" and topic_agent_name is None:
        diagnostics.append(Diagnostic(code="ISO103", severity="error", concept=concept, path=source_path, field="topic_agent_name", message="topic_agent scope requires topic_agent_name."))
    if scope not in TOPIC_SELECTOR_SCOPES and (topic_actor_name is not None or topic_agent_name is not None):
        diagnostics.append(Diagnostic(code="ISO103", severity="error", concept=concept, path=source_path, field="scope", message="Selector names are only allowed for topic_actor or topic_agent scope."))
    return diagnostics


def _duplicate_active_row_diagnostics(params: Iterable[UserPluginRuntimeParam], path: Path, concept: str) -> list[Diagnostic]:
    keys = [
        (param.plugin_id, param.key, param.scope, param.topic_actor_name, param.topic_agent_name)
        for param in params
        if param.status == "active"
    ]
    return [
        Diagnostic(code="ISO104", severity="error", concept=concept, path=path, field=f"{plugin_id}:{key}", message="Duplicate active runtime param row.")
        for (plugin_id, key, _scope, _actor, _agent), count in Counter(keys).items()
        if count > 1
    ]


def _duplicate_active_plugin_diagnostics(registrations: Iterable[UserPluginRegistration], path: Path, concept: str) -> list[Diagnostic]:
    keys = [
        (registration.plugin_id, registration.scope, registration.topic_actor_name, registration.topic_agent_name)
        for registration in registrations
        if registration.status == "active"
    ]
    return [
        Diagnostic(code="ISO104", severity="error", concept=concept, path=path, field=plugin_id, message="Duplicate active User Plugin registration.")
        for (plugin_id, _scope, _actor, _agent), count in Counter(keys).items()
        if count > 1
    ]


def _matches_topic_selector(row: object, topic_actor_name: str | None, topic_agent_name: str | None) -> bool:
    scope = getattr(row, "scope")
    if scope == "research_topic":
        return True
    if scope == "topic_actor":
        return getattr(row, "topic_actor_name", None) == topic_actor_name
    if scope == "topic_agent":
        return getattr(row, "topic_agent_name", None) == topic_agent_name
    return True


def _definition_source(group: list[RuntimeParamCandidate]) -> UserPluginRuntimeParam | None:
    for candidate in group:
        if candidate.param.value_type is not None:
            return candidate.param
    return None


def _self_defining(param: UserPluginRuntimeParam) -> bool:
    return param.value_type is not None and (param.value_type != "enum" or bool(param.allowed_values))


def _mutation_scope_diagnostics(
    context: EffectiveTopicContext | None,
    scope: str,
    topic_actor_name: str | None,
    topic_agent_name: str | None,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if scope not in RUNTIME_PARAM_SCOPES:
        diagnostics.append(Diagnostic(code="ISO103", severity="error", concept="User Plugin configuration", field="scope", message=f"Unsupported User Plugin scope: {scope}."))
    if scope != "project" and context is None:
        diagnostics.append(Diagnostic(code="ISO103", severity="error", concept="User Plugin configuration", field="scope", message="Topic-scoped User Plugin configuration requires a selected Research Topic."))
    temp = type("_ScopeRow", (), {"scope": scope, "topic_actor_name": topic_actor_name, "topic_agent_name": topic_agent_name})()
    diagnostics.extend(_selector_diagnostics(temp, Path("<cli>"), "User Plugin configuration", context))
    return diagnostics


def _manifest_path_for_mutation(project: Project, context: EffectiveTopicContext | None, scope: str) -> Path:
    if scope == "project":
        return project.manifest_path
    assert context is not None
    from isomer_labs.workspace.manifest import topic_workspace_manifest_path

    return topic_workspace_manifest_path(context.topic_workspace_path)


def _upsert_toml_row(path: Path, table: str, row: Mapping[str, Any], match: Any) -> list[Diagnostic]:
    doc, diagnostics = _load_tomlkit_doc(path)
    if doc is None:
        return diagnostics
    aot = doc.get(table)
    if not isinstance(aot, list):
        aot = tomlkit.aot()
        doc[table] = aot
    replaced = False
    for index, item in enumerate(aot):
        if isinstance(item, Mapping) and match(item):
            replacement = tomlkit.table()
            merged = dict(item)
            merged.update(row)
            for key, value in merged.items():
                replacement[key] = value
            aot[index] = replacement
            replaced = True
            break
    if not replaced:
        new_item = tomlkit.table()
        for key, value in row.items():
            new_item[key] = value
        aot.append(new_item)
    diagnostics.extend(_write_tomlkit_doc(path, doc))
    return diagnostics


def _remove_toml_rows(path: Path, table: str, match: Any) -> list[Diagnostic]:
    doc, diagnostics = _load_tomlkit_doc(path)
    if doc is None:
        return diagnostics
    aot = doc.get(table)
    if isinstance(aot, list):
        retained = tomlkit.aot()
        for item in aot:
            if not (isinstance(item, Mapping) and match(item)):
                retained.append(item)
        doc[table] = retained
    diagnostics.extend(_write_tomlkit_doc(path, doc))
    return diagnostics


def _load_tomlkit_doc(path: Path) -> tuple[Any | None, list[Diagnostic]]:
    try:
        if path.exists():
            return tomlkit.parse(path.read_text(encoding="utf-8")), []
        doc = tomlkit.document()
        if path.name == "topic-workspace.toml":
            doc["schema_version"] = "isomer-topic-workspace-manifest.v1"
        return doc, []
    except OSError as exc:
        return None, [Diagnostic(code="ISO001", severity="error", concept="User Plugin configuration", path=path, message=f"Could not read manifest: {exc}")]


def _write_tomlkit_doc(path: Path, doc: Any) -> list[Diagnostic]:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(tomlkit.dumps(doc), encoding="utf-8")
    except OSError as exc:
        return [Diagnostic(code="ISO001", severity="error", concept="User Plugin configuration", path=path, message=f"Could not write manifest: {exc}")]
    return []


def _plugin_row_matches(plugin_id: str, scope: str, topic_actor_name: str | None, topic_agent_name: str | None) -> Any:
    return lambda row: _string(row.get("plugin_id") or row.get("id")) == plugin_id and (_string(row.get("scope")) or "project") == scope and _string(row.get("topic_actor_name")) == topic_actor_name and _string(row.get("topic_agent_name") or row.get("agent_name")) == topic_agent_name


def _param_row_matches(plugin_id: str, key: str, scope: str, topic_actor_name: str | None, topic_agent_name: str | None) -> Any:
    return lambda row: _string(row.get("plugin_id") or row.get("id")) == plugin_id and _string(row.get("key") or row.get("param_key") or row.get("name")) == key and (_string(row.get("scope")) or "project") == scope and _string(row.get("topic_actor_name")) == topic_actor_name and _string(row.get("topic_agent_name") or row.get("agent_name")) == topic_agent_name


def _import_row_matches(plugin_id: str, path_input: str, scope: str, topic_actor_name: str | None, topic_agent_name: str | None) -> Any:
    return lambda row: _string(row.get("plugin_id") or row.get("id")) == plugin_id and _string(row.get("path") or row.get("import_path")) == path_input and (_string(row.get("scope")) or "project") == scope and _string(row.get("topic_actor_name")) == topic_actor_name and _string(row.get("topic_agent_name") or row.get("agent_name")) == topic_agent_name


def _registration_row(plugin_id: str, source_path_input: str | None, scope: str, status: str, topic_actor_name: str | None = None, topic_agent_name: str | None = None) -> dict[str, Any]:
    row: dict[str, Any] = {"plugin_id": plugin_id, "scope": scope, "status": status}
    if source_path_input is not None:
        row["source_path"] = source_path_input
    if topic_actor_name is not None:
        row["topic_actor_name"] = topic_actor_name
    if topic_agent_name is not None:
        row["topic_agent_name"] = topic_agent_name
    return row


def _param_row(param: UserPluginRuntimeParam) -> dict[str, Any]:
    row: dict[str, Any] = {
        "plugin_id": param.plugin_id,
        "key": param.key,
        "value": param.value,
        "scope": param.scope,
        "status": param.status,
    }
    if param.value_type is not None:
        row["value_type"] = param.value_type
    if param.allowed_values:
        row["allowed_values"] = list(param.allowed_values)
    if param.description is not None:
        row["description"] = param.description
    if param.topic_actor_name is not None:
        row["topic_actor_name"] = param.topic_actor_name
    if param.topic_agent_name is not None:
        row["topic_agent_name"] = param.topic_agent_name
    return row


def _import_row(import_ref: UserPluginRuntimeParamImport) -> dict[str, Any]:
    row: dict[str, Any] = {
        "plugin_id": import_ref.plugin_id,
        "path": import_ref.path_input,
        "scope": import_ref.scope,
        "status": import_ref.status,
    }
    if import_ref.topic_actor_name is not None:
        row["topic_actor_name"] = import_ref.topic_actor_name
    if import_ref.topic_agent_name is not None:
        row["topic_agent_name"] = import_ref.topic_agent_name
    return row


def _row_scan_payload(row: object) -> dict[str, object]:
    if hasattr(row, "to_json"):
        return getattr(row, "to_json")()
    return {}


def _table_items(value: object) -> list[Mapping[str, Any]]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, Mapping)]
    if isinstance(value, Mapping):
        if all(isinstance(item, Mapping) for item in value.values()):
            items: list[Mapping[str, Any]] = []
            for key, item in value.items():
                copied = dict(item)
                copied.setdefault("id", key)
                items.append(copied)
            return items
        return [value]
    return []


def _string(value: object) -> str | None:
    return value if isinstance(value, str) and value else None


def _string_tuple(value: object) -> tuple[str, ...]:
    if isinstance(value, list):
        return tuple(item for item in value if isinstance(item, str) and item)
    return ()
