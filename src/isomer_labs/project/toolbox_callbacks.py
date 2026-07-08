"""Toolbox callback manifest parsing."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from isomer_labs.core.diagnostics import Diagnostic, has_errors
from isomer_labs.core.path_utils import display_path, is_within, resolve_project_path
from isomer_labs.core.toml_loader import load_toml
from isomer_labs.models import Project
from isomer_labs.project.callback_keys import CALLBACK_TOOLBOX_ID_RE, CALLBACK_TOOLBOX_KEY_RE
from isomer_labs.project.skill_callbacks import (
    VALID_CALLBACK_SOURCE_TYPES,
    secret_like_diagnostics,
)
from isomer_labs.project.toolboxes import PARAM_KEY_RE, RUNTIME_PARAM_VALUE_TYPES
from isomer_labs.skills.system_assets import has_system_skill_callback_insertion_point


TOOLBOX_SCHEMA_VERSION = "isomer-toolbox.v1"
TOOLBOX_CALLBACK_BUNDLE_KIND = "toolbox-callback-bundle"


@dataclass(frozen=True)
class ToolboxCallbackEntry:
    toolbox_key: str
    target_skill: str
    stage: str
    source_type: str
    source_value: str
    source_field: str
    description: str | None = None

    @property
    def installed_key_suffix(self) -> str:
        return self.toolbox_key

    def source_path_input(self, project: Project, toolbox_root: Path) -> str:
        if self.source_type == "prompt":
            return self.source_value
        source_path = Path(self.source_value)
        resolved = source_path.expanduser().resolve(strict=False) if source_path.is_absolute() else (toolbox_root / source_path).resolve(strict=False)
        return display_path(resolved, project.root)


@dataclass(frozen=True)
class ToolboxRuntimeParamDefinition:
    key: str
    value_type: str
    default_value: Any | None = None
    allowed_values: tuple[str, ...] = ()
    description: str | None = None


@dataclass(frozen=True)
class ToolboxRuntimeParamBundle:
    name: str
    path_input: str
    description: str | None = None


@dataclass(frozen=True)
class ToolboxCallbackManifest:
    toolbox_id: str
    toolbox_root: Path
    toolbox_dir_input: str
    toolbox_source_path_input: str
    callbacks: tuple[ToolboxCallbackEntry, ...]
    runtime_params: tuple[ToolboxRuntimeParamDefinition, ...] = ()
    runtime_param_bundles: tuple[ToolboxRuntimeParamBundle, ...] = ()


@dataclass(frozen=True)
class ToolboxCallbackManifestLoadResult:
    manifest: ToolboxCallbackManifest | None
    diagnostics: tuple[Diagnostic, ...]


def load_toolbox_callback_manifest(
    project: Project,
    toolbox_dir_input: str,
) -> ToolboxCallbackManifestLoadResult:
    toolbox_root = resolve_project_path(project.root, toolbox_dir_input)
    diagnostics: list[Diagnostic] = []
    if not toolbox_root.exists():
        diagnostics.append(
            Diagnostic(
                code="ISO001",
                severity="error",
                concept="Toolbox callback manifest",
                path=toolbox_root,
                field="toolbox_dir",
                message="Toolbox directory does not exist.",
            )
        )
        return ToolboxCallbackManifestLoadResult(None, tuple(diagnostics))
    if not toolbox_root.is_dir():
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="Toolbox callback manifest",
                path=toolbox_root,
                field="toolbox_dir",
                message="Toolbox path must be a directory.",
            )
        )
        return ToolboxCallbackManifestLoadResult(None, tuple(diagnostics))
    if not is_within(toolbox_root, project.root):
        diagnostics.append(
            Diagnostic(
                code="ISO005",
                severity="error",
                concept="Toolbox callback manifest",
                path=toolbox_root,
                field="toolbox_dir",
                message="Toolbox directory must resolve inside the Project root.",
            )
        )
        return ToolboxCallbackManifestLoadResult(None, tuple(diagnostics))

    manifest_path = toolbox_root / "manifest.toml"
    raw, load_diagnostics = load_toml(manifest_path, "Toolbox callback manifest")
    diagnostics.extend(load_diagnostics)
    if raw is None:
        return ToolboxCallbackManifestLoadResult(None, tuple(diagnostics))
    diagnostics.extend(secret_like_diagnostics(raw, "Toolbox callback manifest", manifest_path, ()))

    schema_version = _string(raw.get("schema_version"))
    if schema_version != TOOLBOX_SCHEMA_VERSION:
        diagnostics.append(
            Diagnostic(
                code="ISO102",
                severity="error",
                concept="Toolbox callback manifest",
                path=manifest_path,
                field="schema_version",
                message=f"Toolbox manifest schema_version must be {TOOLBOX_SCHEMA_VERSION}.",
            )
        )
    kind = _string(raw.get("kind"))
    if kind != TOOLBOX_CALLBACK_BUNDLE_KIND:
        diagnostics.append(
            Diagnostic(
                code="ISO102",
                severity="error",
                concept="Toolbox callback manifest",
                path=manifest_path,
                field="kind",
                message=f"Toolbox manifest kind must be {TOOLBOX_CALLBACK_BUNDLE_KIND}.",
            )
        )
    if "id" in raw:
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="Toolbox callback manifest",
                path=manifest_path,
                field="id",
                message="Use toolbox_id for toolbox identity; top-level id is not supported.",
            )
        )
    toolbox_id = _string(raw.get("toolbox_id"))
    if toolbox_id is None:
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="Toolbox callback manifest",
                path=manifest_path,
                field="toolbox_id",
                message="Toolbox manifest must include toolbox_id.",
            )
        )
    elif not CALLBACK_TOOLBOX_ID_RE.match(toolbox_id):
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="Toolbox callback manifest",
                path=manifest_path,
                field="toolbox_id",
                message="Toolbox toolbox_id must start with an alphanumeric character and contain only letters, numbers, underscore, dot, or dash.",
            )
        )

    raw_callbacks = raw.get("callbacks")
    if raw_callbacks is None:
        raw_items: list[dict[str, Any]] = []
    elif isinstance(raw_callbacks, list):
        raw_items = [item for item in raw_callbacks if isinstance(item, dict)]
        if len(raw_items) != len(raw_callbacks):
            diagnostics.append(
                Diagnostic(
                    code="ISO102",
                    severity="error",
                    concept="Toolbox callback manifest",
                    path=manifest_path,
                    field="callbacks",
                    message="Toolbox callback entries must be tables.",
                )
            )
    else:
        raw_items = []
        diagnostics.append(
            Diagnostic(
                code="ISO102",
                severity="error",
                concept="Toolbox callback manifest",
                path=manifest_path,
                field="callbacks",
                message="Toolbox manifest callbacks must be an array of tables.",
            )
        )

    entries: list[ToolboxCallbackEntry] = []
    for index, item in enumerate(raw_items):
        parsed, item_diagnostics = _parse_callback_entry(project, manifest_path, item, index)
        diagnostics.extend(item_diagnostics)
        if parsed is not None:
            entries.append(parsed)
    key_counts = Counter(entry.toolbox_key for entry in entries)
    for toolbox_key in sorted(key for key, count in key_counts.items() if count > 1):
        diagnostics.append(
            Diagnostic(
                code="ISO104",
                severity="error",
                concept="Toolbox callback manifest",
                path=manifest_path,
                field="callbacks.key",
                message=f"Duplicate toolbox callback key is registered inside this Toolbox: {toolbox_key}.",
            )
        )

    runtime_params, param_diagnostics = _parse_runtime_param_definitions(manifest_path, raw)
    diagnostics.extend(param_diagnostics)
    runtime_param_bundles, bundle_diagnostics = _parse_runtime_param_bundles(manifest_path, raw)
    diagnostics.extend(bundle_diagnostics)

    if has_errors(diagnostics) or toolbox_id is None:
        return ToolboxCallbackManifestLoadResult(None, tuple(diagnostics))
    return ToolboxCallbackManifestLoadResult(
        ToolboxCallbackManifest(
            toolbox_id=toolbox_id,
            toolbox_root=toolbox_root,
            toolbox_dir_input=toolbox_dir_input,
            toolbox_source_path_input=display_path(toolbox_root, project.root),
            callbacks=tuple(entries),
            runtime_params=tuple(runtime_params),
            runtime_param_bundles=tuple(runtime_param_bundles),
        ),
        tuple(diagnostics),
    )


def _parse_callback_entry(
    project: Project,
    manifest_path: Path,
    item: dict[str, Any],
    index: int,
) -> tuple[ToolboxCallbackEntry | None, list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    field = f"callbacks[{index}]"
    if "id" in item:
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="Toolbox callback manifest",
                path=manifest_path,
                field=f"{field}.id",
                message="Use key for toolbox callback identity; callback id is not supported.",
            )
        )
    target_skill = _string(item.get("target_skill"))
    stage = _string(item.get("stage"))
    source_type = _string(item.get("source_type"))
    explicit_key = _string(item.get("key"))
    toolbox_key = explicit_key
    if toolbox_key is None and target_skill is not None and stage is not None:
        toolbox_key = f"{target_skill}/{stage}"
    if target_skill is None:
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="Toolbox callback manifest",
                path=manifest_path,
                field=f"{field}.target_skill",
                message="Toolbox callback must target a system skill name.",
            )
        )
    if stage is None:
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="Toolbox callback manifest",
                path=manifest_path,
                field=f"{field}.stage",
                message="Toolbox callback must include a stage.",
            )
        )
    if target_skill is not None and stage is not None and not has_system_skill_callback_insertion_point(target_skill, stage):
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="Toolbox callback manifest",
                path=manifest_path,
                field=f"{field}.target_skill",
                message=f"Toolbox callback insertion point is not declared in the packaged catalog: {target_skill}/{stage}. Query `isomer-cli project skill-callbacks insertion-points` for supported targets.",
            )
        )
    if toolbox_key is None:
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="Toolbox callback manifest",
                path=manifest_path,
                field=f"{field}.key",
                message="Toolbox callback key must be provided or derivable from target_skill and stage.",
            )
        )
    elif not CALLBACK_TOOLBOX_KEY_RE.match(toolbox_key):
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="Toolbox callback manifest",
                path=manifest_path,
                field=f"{field}.key",
                message="Toolbox callback key must contain only letters, numbers, dash, underscore, or slash.",
            )
        )
    if source_type not in VALID_CALLBACK_SOURCE_TYPES:
        diagnostics.append(
            Diagnostic(
                code="ISO102",
                severity="error",
                concept="Toolbox callback manifest",
                path=manifest_path,
                field=f"{field}.source_type",
                message="Toolbox callback source_type must be prompt, prompt_file, or skill_dir.",
            )
        )
    selected_sources = [
        (source_field, _string(item.get(source_field)))
        for source_field in ("skill_dir", "prompt_file", "prompt")
        if _string(item.get(source_field)) is not None
    ]
    if len(selected_sources) != 1:
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="Toolbox callback manifest",
                path=manifest_path,
                field=f"{field}.source",
                message="Toolbox callback must provide exactly one of skill_dir, prompt_file, or prompt.",
            )
        )
    source_field: str | None = None
    source_value: str | None = None
    if selected_sources:
        source_field, source_value = selected_sources[0]
        if source_type is not None and source_field != source_type:
            diagnostics.append(
                Diagnostic(
                    code="ISO103",
                    severity="error",
                    concept="Toolbox callback manifest",
                    path=manifest_path,
                    field=f"{field}.source",
                    message="Toolbox callback source field must match source_type.",
                )
            )
        if source_field in {"skill_dir", "prompt_file"} and source_value is not None and Path(source_value).is_absolute():
            diagnostics.append(
                Diagnostic(
                    code="ISO005",
                    severity="error",
                    concept="Toolbox callback manifest",
                    path=manifest_path,
                    field=f"{field}.{source_field}",
                    message="Toolbox callback source paths must be relative to the Toolbox directory.",
                )
            )
    if has_errors(diagnostics) or toolbox_key is None or target_skill is None or stage is None or source_type is None or source_field is None or source_value is None:
        return None, diagnostics
    return (
        ToolboxCallbackEntry(
            toolbox_key=toolbox_key,
            target_skill=target_skill,
            stage=stage,
            source_type=source_type,
            source_value=source_value,
            source_field=source_field,
            description=_string(item.get("description")),
        ),
        diagnostics,
    )


def _string(value: object) -> str | None:
    if isinstance(value, str) and value:
        return value
    return None


def _parse_runtime_param_definitions(
    manifest_path: Path,
    raw: dict[str, Any],
) -> tuple[list[ToolboxRuntimeParamDefinition], list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    raw_params = raw.get("runtime_params")
    if raw_params is None:
        return [], diagnostics
    if not isinstance(raw_params, list):
        return [], [
            Diagnostic(
                code="ISO102",
                severity="error",
                concept="Toolbox callback manifest",
                path=manifest_path,
                field="runtime_params",
                message="Toolbox runtime_params must be an array of tables.",
            )
        ]
    definitions: list[ToolboxRuntimeParamDefinition] = []
    for index, item in enumerate(raw_params):
        field = f"runtime_params[{index}]"
        if not isinstance(item, dict):
            diagnostics.append(
                Diagnostic(
                    code="ISO102",
                    severity="error",
                    concept="Toolbox callback manifest",
                    path=manifest_path,
                    field=field,
                    message="Runtime param definitions must be tables.",
                )
            )
            continue
        stale_fields = sorted(field_name for field_name in ("name", "type") if field_name in item)
        if stale_fields:
            diagnostics.append(
                Diagnostic(
                    code="ISO103",
                    severity="error",
                    concept="Toolbox callback manifest",
                    path=manifest_path,
                    field=field,
                    message=f"Old runtime param definition fields are not supported: {', '.join(stale_fields)}.",
                )
            )
        key = _string(item.get("key"))
        value_type = _string(item.get("value_type"))
        if key is None:
            diagnostics.append(
                Diagnostic(
                    code="ISO103",
                    severity="error",
                    concept="Toolbox callback manifest",
                    path=manifest_path,
                    field=f"{field}.key",
                    message="Runtime param definition must include key.",
                )
            )
        elif not PARAM_KEY_RE.match(key):
            diagnostics.append(
                Diagnostic(
                    code="ISO103",
                    severity="error",
                    concept="Toolbox callback manifest",
                    path=manifest_path,
                    field=f"{field}.key",
                    message="Runtime param key must start with an alphanumeric character and contain only letters, numbers, slash, underscore, or dash.",
                )
            )
        if value_type is None:
            diagnostics.append(
                Diagnostic(
                    code="ISO103",
                    severity="error",
                    concept="Toolbox callback manifest",
                    path=manifest_path,
                    field=f"{field}.value_type",
                    message="Runtime param definition must include value_type.",
                )
            )
        elif value_type not in RUNTIME_PARAM_VALUE_TYPES:
            diagnostics.append(
                Diagnostic(
                    code="ISO103",
                    severity="error",
                    concept="Toolbox callback manifest",
                    path=manifest_path,
                    field=f"{field}.value_type",
                    message=f"Unsupported runtime param value_type: {value_type}.",
                )
            )
        allowed_values = tuple(value for value in item.get("allowed_values", []) if isinstance(value, str)) if isinstance(item.get("allowed_values"), list) else ()
        if value_type == "enum" and not allowed_values:
            diagnostics.append(
                Diagnostic(
                    code="ISO103",
                    severity="error",
                    concept="Toolbox callback manifest",
                    path=manifest_path,
                    field=f"{field}.allowed_values",
                    message="Enum runtime param definitions must include allowed_values.",
                )
            )
        if key is not None and value_type is not None:
            definitions.append(
                ToolboxRuntimeParamDefinition(
                    key=key,
                    value_type=value_type,
                    default_value=item.get("default"),
                    allowed_values=allowed_values,
                    description=_string(item.get("description")),
                )
            )
    for key, count in Counter(definition.key for definition in definitions).items():
        if count > 1:
            diagnostics.append(
                Diagnostic(
                    code="ISO104",
                    severity="error",
                    concept="Toolbox callback manifest",
                    path=manifest_path,
                    field="runtime_params.key",
                    message=f"Duplicate runtime param definition key is registered inside this Toolbox: {key}.",
                )
            )
    return definitions, diagnostics


def _parse_runtime_param_bundles(
    manifest_path: Path,
    raw: dict[str, Any],
) -> tuple[list[ToolboxRuntimeParamBundle], list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    raw_bundles = raw.get("runtime_param_bundles")
    if raw_bundles is None:
        return [], diagnostics
    if not isinstance(raw_bundles, list):
        return [], [
            Diagnostic(
                code="ISO102",
                severity="error",
                concept="Toolbox callback manifest",
                path=manifest_path,
                field="runtime_param_bundles",
                message="Toolbox runtime_param_bundles must be an array of tables.",
            )
        ]
    bundles: list[ToolboxRuntimeParamBundle] = []
    for index, item in enumerate(raw_bundles):
        field = f"runtime_param_bundles[{index}]"
        if not isinstance(item, dict):
            diagnostics.append(
                Diagnostic(
                    code="ISO102",
                    severity="error",
                    concept="Toolbox callback manifest",
                    path=manifest_path,
                    field=field,
                    message="Runtime param bundle declarations must be tables.",
                )
            )
            continue
        name = _string(item.get("name") or item.get("id"))
        path_input = _string(item.get("path"))
        if name is None:
            diagnostics.append(Diagnostic(code="ISO103", severity="error", concept="Toolbox callback manifest", path=manifest_path, field=f"{field}.name", message="Runtime param bundle must include name."))
        if path_input is None:
            diagnostics.append(Diagnostic(code="ISO103", severity="error", concept="Toolbox callback manifest", path=manifest_path, field=f"{field}.path", message="Runtime param bundle must include path."))
        elif Path(path_input).is_absolute():
            diagnostics.append(Diagnostic(code="ISO005", severity="error", concept="Toolbox callback manifest", path=manifest_path, field=f"{field}.path", message="Runtime param bundle path must be relative to the Toolbox directory."))
        if name is not None and path_input is not None:
            bundles.append(ToolboxRuntimeParamBundle(name=name, path_input=path_input, description=_string(item.get("description"))))
    for name, count in Counter(bundle.name for bundle in bundles).items():
        if count > 1:
            diagnostics.append(Diagnostic(code="ISO104", severity="error", concept="Toolbox callback manifest", path=manifest_path, field="runtime_param_bundles.name", message=f"Duplicate runtime param bundle is declared inside this Toolbox: {name}."))
    return bundles, diagnostics
