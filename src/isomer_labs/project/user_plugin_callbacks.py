"""User-plugin callback manifest parsing."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from isomer_labs.core.diagnostics import Diagnostic, has_errors
from isomer_labs.core.path_utils import display_path, is_within, resolve_project_path
from isomer_labs.core.toml_loader import load_toml
from isomer_labs.models import Project
from isomer_labs.project.callback_keys import CALLBACK_PLUGIN_ID_RE, CALLBACK_PLUGIN_KEY_RE
from isomer_labs.project.skill_callbacks import (
    VALID_CALLBACK_SOURCE_TYPES,
    VALID_CALLBACK_STAGES,
    active_system_skill_names,
    secret_like_diagnostics,
)


USER_PLUGIN_SCHEMA_VERSION = "isomer-user-plugin.v1"
USER_PLUGIN_CALLBACK_BUNDLE_KIND = "user-skill-callback-bundle"


@dataclass(frozen=True)
class UserPluginCallbackEntry:
    plugin_key: str
    target_skill: str
    stage: str
    source_type: str
    source_value: str
    source_field: str
    description: str | None = None

    @property
    def installed_key_suffix(self) -> str:
        return self.plugin_key

    def source_path_input(self, project: Project, plugin_root: Path) -> str:
        if self.source_type == "prompt":
            return self.source_value
        source_path = Path(self.source_value)
        resolved = source_path.expanduser().resolve(strict=False) if source_path.is_absolute() else (plugin_root / source_path).resolve(strict=False)
        return display_path(resolved, project.root)


@dataclass(frozen=True)
class UserPluginCallbackManifest:
    plugin_id: str
    plugin_root: Path
    plugin_dir_input: str
    plugin_source_path_input: str
    callbacks: tuple[UserPluginCallbackEntry, ...]


@dataclass(frozen=True)
class UserPluginCallbackManifestLoadResult:
    manifest: UserPluginCallbackManifest | None
    diagnostics: tuple[Diagnostic, ...]


def load_user_plugin_callback_manifest(
    project: Project,
    plugin_dir_input: str,
) -> UserPluginCallbackManifestLoadResult:
    plugin_root = resolve_project_path(project.root, plugin_dir_input)
    diagnostics: list[Diagnostic] = []
    if not plugin_root.exists():
        diagnostics.append(
            Diagnostic(
                code="ISO001",
                severity="error",
                concept="User Plugin callback manifest",
                path=plugin_root,
                field="plugin_dir",
                message="User-plugin directory does not exist.",
            )
        )
        return UserPluginCallbackManifestLoadResult(None, tuple(diagnostics))
    if not plugin_root.is_dir():
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="User Plugin callback manifest",
                path=plugin_root,
                field="plugin_dir",
                message="User-plugin path must be a directory.",
            )
        )
        return UserPluginCallbackManifestLoadResult(None, tuple(diagnostics))
    if not is_within(plugin_root, project.root):
        diagnostics.append(
            Diagnostic(
                code="ISO005",
                severity="error",
                concept="User Plugin callback manifest",
                path=plugin_root,
                field="plugin_dir",
                message="User-plugin directory must resolve inside the Project root.",
            )
        )
        return UserPluginCallbackManifestLoadResult(None, tuple(diagnostics))

    manifest_path = plugin_root / "manifest.toml"
    raw, load_diagnostics = load_toml(manifest_path, "User Plugin callback manifest")
    diagnostics.extend(load_diagnostics)
    if raw is None:
        return UserPluginCallbackManifestLoadResult(None, tuple(diagnostics))
    diagnostics.extend(secret_like_diagnostics(raw, "User Plugin callback manifest", manifest_path, ()))

    schema_version = _string(raw.get("schema_version"))
    if schema_version != USER_PLUGIN_SCHEMA_VERSION:
        diagnostics.append(
            Diagnostic(
                code="ISO102",
                severity="error",
                concept="User Plugin callback manifest",
                path=manifest_path,
                field="schema_version",
                message=f"User-plugin manifest schema_version must be {USER_PLUGIN_SCHEMA_VERSION}.",
            )
        )
    kind = _string(raw.get("kind"))
    if kind != USER_PLUGIN_CALLBACK_BUNDLE_KIND:
        diagnostics.append(
            Diagnostic(
                code="ISO102",
                severity="error",
                concept="User Plugin callback manifest",
                path=manifest_path,
                field="kind",
                message=f"User-plugin manifest kind must be {USER_PLUGIN_CALLBACK_BUNDLE_KIND}.",
            )
        )
    if "id" in raw:
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="User Plugin callback manifest",
                path=manifest_path,
                field="id",
                message="Use plugin_id for user-plugin identity; top-level id is not supported.",
            )
        )
    plugin_id = _string(raw.get("plugin_id"))
    if plugin_id is None:
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="User Plugin callback manifest",
                path=manifest_path,
                field="plugin_id",
                message="User-plugin manifest must include plugin_id.",
            )
        )
    elif not CALLBACK_PLUGIN_ID_RE.match(plugin_id):
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="User Plugin callback manifest",
                path=manifest_path,
                field="plugin_id",
                message="User-plugin plugin_id must start with an alphanumeric character and contain only letters, numbers, underscore, dot, or dash.",
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
                    concept="User Plugin callback manifest",
                    path=manifest_path,
                    field="callbacks",
                    message="User-plugin callback entries must be tables.",
                )
            )
    else:
        raw_items = []
        diagnostics.append(
            Diagnostic(
                code="ISO102",
                severity="error",
                concept="User Plugin callback manifest",
                path=manifest_path,
                field="callbacks",
                message="User-plugin manifest callbacks must be an array of tables.",
            )
        )

    entries: list[UserPluginCallbackEntry] = []
    for index, item in enumerate(raw_items):
        parsed, item_diagnostics = _parse_callback_entry(project, manifest_path, item, index)
        diagnostics.extend(item_diagnostics)
        if parsed is not None:
            entries.append(parsed)
    key_counts = Counter(entry.plugin_key for entry in entries)
    for plugin_key in sorted(key for key, count in key_counts.items() if count > 1):
        diagnostics.append(
            Diagnostic(
                code="ISO104",
                severity="error",
                concept="User Plugin callback manifest",
                path=manifest_path,
                field="callbacks.key",
                message=f"Duplicate user-plugin callback key is registered inside this plugin: {plugin_key}.",
            )
        )

    if has_errors(diagnostics) or plugin_id is None:
        return UserPluginCallbackManifestLoadResult(None, tuple(diagnostics))
    return UserPluginCallbackManifestLoadResult(
        UserPluginCallbackManifest(
            plugin_id=plugin_id,
            plugin_root=plugin_root,
            plugin_dir_input=plugin_dir_input,
            plugin_source_path_input=display_path(plugin_root, project.root),
            callbacks=tuple(entries),
        ),
        tuple(diagnostics),
    )


def _parse_callback_entry(
    project: Project,
    manifest_path: Path,
    item: dict[str, Any],
    index: int,
) -> tuple[UserPluginCallbackEntry | None, list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    field = f"callbacks[{index}]"
    if "id" in item:
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="User Plugin callback manifest",
                path=manifest_path,
                field=f"{field}.id",
                message="Use key for user-plugin callback identity; callback id is not supported.",
            )
        )
    target_skill = _string(item.get("target_skill"))
    stage = _string(item.get("stage"))
    source_type = _string(item.get("source_type"))
    explicit_key = _string(item.get("key"))
    plugin_key = explicit_key
    if plugin_key is None and target_skill is not None and stage is not None:
        plugin_key = f"{target_skill}/{stage}"
    if target_skill is None:
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="User Plugin callback manifest",
                path=manifest_path,
                field=f"{field}.target_skill",
                message="User-plugin callback must target a system skill name.",
            )
        )
    elif target_skill not in active_system_skill_names():
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="User Plugin callback manifest",
                path=manifest_path,
                field=f"{field}.target_skill",
                message=f"User-plugin callback target is not an active packaged system skill: {target_skill}.",
            )
        )
    if stage is None:
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="User Plugin callback manifest",
                path=manifest_path,
                field=f"{field}.stage",
                message="User-plugin callback must include a stage.",
            )
        )
    elif stage not in VALID_CALLBACK_STAGES:
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="User Plugin callback manifest",
                path=manifest_path,
                field=f"{field}.stage",
                message="User-plugin callback stage must be begin or end.",
            )
        )
    if plugin_key is None:
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="User Plugin callback manifest",
                path=manifest_path,
                field=f"{field}.key",
                message="User-plugin callback key must be provided or derivable from target_skill and stage.",
            )
        )
    elif not CALLBACK_PLUGIN_KEY_RE.match(plugin_key):
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="User Plugin callback manifest",
                path=manifest_path,
                field=f"{field}.key",
                message="User-plugin callback key must contain only letters, numbers, dash, underscore, or slash.",
            )
        )
    if source_type not in VALID_CALLBACK_SOURCE_TYPES:
        diagnostics.append(
            Diagnostic(
                code="ISO102",
                severity="error",
                concept="User Plugin callback manifest",
                path=manifest_path,
                field=f"{field}.source_type",
                message="User-plugin callback source_type must be prompt, prompt_file, or skill_dir.",
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
                concept="User Plugin callback manifest",
                path=manifest_path,
                field=f"{field}.source",
                message="User-plugin callback must provide exactly one of skill_dir, prompt_file, or prompt.",
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
                    concept="User Plugin callback manifest",
                    path=manifest_path,
                    field=f"{field}.source",
                    message="User-plugin callback source field must match source_type.",
                )
            )
        if source_field in {"skill_dir", "prompt_file"} and source_value is not None and Path(source_value).is_absolute():
            diagnostics.append(
                Diagnostic(
                    code="ISO005",
                    severity="error",
                    concept="User Plugin callback manifest",
                    path=manifest_path,
                    field=f"{field}.{source_field}",
                    message="User-plugin callback source paths must be relative to the plugin directory.",
                )
            )
    if has_errors(diagnostics) or plugin_key is None or target_skill is None or stage is None or source_type is None or source_field is None or source_value is None:
        return None, diagnostics
    return (
        UserPluginCallbackEntry(
            plugin_key=plugin_key,
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
