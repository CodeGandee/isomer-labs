"""User Skill Callback registries and resolution."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any, Iterable

import tomlkit  # type: ignore[import-untyped]

from isomer_labs.core.diagnostics import Diagnostic, has_errors
from isomer_labs.core.path_utils import display_path, is_within, resolve_project_path
from isomer_labs.core.toml_loader import load_toml
from isomer_labs.models import EffectiveTopicContext, Project
from isomer_labs.skills.system_assets import SystemSkillAssetError, iter_system_skill_paths


USER_SKILL_CALLBACK_REGISTRY_SCHEMA_VERSION = "isomer-user-skill-callback-registry.v1"
VALID_CALLBACK_STAGES = ("begin", "end")
VALID_CALLBACK_SCOPES = ("project", "research_topic")
VALID_CALLBACK_STATUSES = ("active", "inactive", "disabled")
VALID_CALLBACK_SOURCE_TYPES = ("prompt", "prompt_file", "skill_dir")
DEFAULT_CALLBACK_PRIORITY = 100
CALLBACK_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")
SECRET_KEY_TERMS = (
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
SECRET_VALUE_RE = re.compile(
    r"(?i)\b(?:api[_-]?key|token|password|secret|credential|private[_-]?key|access[_-]?key)\b\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{8,}"
)


@dataclass(frozen=True)
class CallbackRegistryRef:
    scope: str
    path_input: str
    path: Path
    source_path: Path
    research_topic_id: str | None = None

    def to_json(self, project_root: Path) -> dict[str, object]:
        data: dict[str, object] = {
            "scope": self.scope,
            "path": display_path(self.path, project_root),
            "path_input": self.path_input,
            "source_path": display_path(self.source_path, project_root),
        }
        if self.research_topic_id is not None:
            data["research_topic_id"] = self.research_topic_id
        return data


@dataclass(frozen=True)
class CallbackSource:
    source_type: str
    path_input: str
    resolved_path: Path
    external: bool

    def to_json(self, project_root: Path) -> dict[str, object]:
        data: dict[str, object] = {
            "source_type": self.source_type,
            "path": display_path(self.resolved_path, project_root),
            "path_input": self.path_input,
            "external": self.external,
        }
        if self.source_type == "skill_dir":
            data["skill_md"] = display_path(self.resolved_path / "SKILL.md", project_root)
        return data

    def summary(self, project_root: Path) -> str:
        if self.source_type == "skill_dir":
            return f"skill_dir:{display_path(self.resolved_path, project_root)}"
        return f"{self.source_type}:{display_path(self.resolved_path, project_root)}"


@dataclass(frozen=True)
class UserSkillCallback:
    id: str
    skill: str
    stage: str
    scope: str
    status: str
    priority: int
    source: CallbackSource
    registry_path: Path
    research_topic_id: str | None = None

    @property
    def active(self) -> bool:
        return self.status == "active"

    def to_json(self, project_root: Path) -> dict[str, object]:
        data: dict[str, object] = {
            "id": self.id,
            "skill": self.skill,
            "stage": self.stage,
            "scope": self.scope,
            "status": self.status,
            "priority": self.priority,
            "registry_path": display_path(self.registry_path, project_root),
            "source": self.source.to_json(project_root),
            "source_summary": self.source.summary(project_root),
        }
        if self.research_topic_id is not None:
            data["research_topic_id"] = self.research_topic_id
        return data


@dataclass(frozen=True)
class CallbackRegistryLoadResult:
    ref: CallbackRegistryRef
    callbacks: tuple[UserSkillCallback, ...]
    diagnostics: tuple[Diagnostic, ...]


def project_callback_registry_refs(project: Project) -> tuple[CallbackRegistryRef, ...]:
    return tuple(
        CallbackRegistryRef(
            scope="project",
            path_input=path_input,
            path=resolve_project_path(project.root, path_input),
            source_path=project.manifest_path,
        )
        for path_input in project.manifest.user_skill_callback_registry_refs
    )


def topic_callback_registry_refs(context: EffectiveTopicContext | None) -> tuple[CallbackRegistryRef, ...]:
    if context is None or context.research_topic_config is None:
        return ()
    refs = _callback_registry_ref_values(context.research_topic_config.refs)
    return tuple(
        CallbackRegistryRef(
            scope="research_topic",
            path_input=path_input,
            path=resolve_project_path(context.project.root, path_input),
            source_path=context.research_topic_config.source_path,
            research_topic_id=context.research_topic.id,
        )
        for path_input in refs
    )


def visible_callback_registry_refs(
    project: Project,
    context: EffectiveTopicContext | None,
) -> tuple[CallbackRegistryRef, ...]:
    return (*topic_callback_registry_refs(context), *project_callback_registry_refs(project))


def validate_callback_registry_refs(
    project: Project,
    topic_configs: dict[str, Any],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    refs = list(project_callback_registry_refs(project))
    for topic_id, config in sorted(topic_configs.items()):
        for path_input in _callback_registry_ref_values(config.refs):
            refs.append(
                CallbackRegistryRef(
                    scope="research_topic",
                    path_input=path_input,
                    path=resolve_project_path(project.root, path_input),
                    source_path=config.source_path,
                    research_topic_id=topic_id,
                )
            )
    for ref in refs:
        diagnostics.extend(_validate_registry_ref_path(project, ref))
        result = load_callback_registry(project, ref, missing_severity="error")
        diagnostics.extend(result.diagnostics)
    diagnostics.extend(_duplicate_active_callback_diagnostics(project, refs))
    return diagnostics


def load_callback_registry(
    project: Project,
    ref: CallbackRegistryRef,
    *,
    missing_severity: str,
) -> CallbackRegistryLoadResult:
    diagnostics: list[Diagnostic] = []
    if not is_within(ref.path, project.root):
        diagnostics.append(
            Diagnostic(
                code="ISO005",
                severity="error",
                concept="User Skill Callback registry",
                path=ref.source_path,
                field="user_skill_callback_registry_refs",
                message="User Skill Callback registry ref resolves outside the Project root.",
            )
        )
    raw, load_diagnostics = load_toml(ref.path, "User Skill Callback registry")
    if raw is None:
        diagnostics.extend(_with_severity(load_diagnostics, missing_severity))
        return CallbackRegistryLoadResult(ref, (), tuple(diagnostics))
    diagnostics.extend(secret_like_diagnostics(raw, "User Skill Callback registry", ref.path, ()))
    schema_version = raw.get("schema_version")
    if schema_version != USER_SKILL_CALLBACK_REGISTRY_SCHEMA_VERSION:
        diagnostics.append(
            Diagnostic(
                code="ISO102",
                severity="error",
                concept="User Skill Callback registry",
                path=ref.path,
                field="schema_version",
                message=f"User Skill Callback registry schema_version must be {USER_SKILL_CALLBACK_REGISTRY_SCHEMA_VERSION}.",
            )
        )
    callbacks: list[UserSkillCallback] = []
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
                    concept="User Skill Callback registry",
                    path=ref.path,
                    field="callbacks",
                    message="User Skill Callback registry callbacks must be tables.",
                )
            )
    else:
        raw_items = []
        diagnostics.append(
            Diagnostic(
                code="ISO102",
                severity="error",
                concept="User Skill Callback registry",
                path=ref.path,
                field="callbacks",
                message="User Skill Callback registry callbacks must be an array of tables.",
            )
        )
    for index, item in enumerate(raw_items):
        parsed, item_diagnostics = _parse_callback_item(project, ref, item, index)
        diagnostics.extend(item_diagnostics)
        if parsed is not None:
            callbacks.append(parsed)
    active_counts = Counter(callback.id for callback in callbacks if callback.active)
    for callback_id in sorted(id_ for id_, count in active_counts.items() if count > 1):
        diagnostics.append(
            Diagnostic(
                code="ISO104",
                severity="error",
                concept="User Skill Callback registry",
                path=ref.path,
                field="callbacks.id",
                message=f"Duplicate active User Skill Callback id is registered: {callback_id}.",
            )
        )
    return CallbackRegistryLoadResult(ref, tuple(callbacks), tuple(diagnostics))


def default_callback_registry_path(
    project: Project,
    *,
    scope: str,
    research_topic_id: str | None,
) -> Path:
    if scope == "research_topic" and research_topic_id:
        return project.config_dir / "user-skill-callbacks" / "topics" / research_topic_id / "registry.toml"
    return project.config_dir / "user-skill-callbacks" / "registry.toml"


def managed_prompt_path(
    project: Project,
    *,
    scope: str,
    research_topic_id: str | None,
    callback_id: str,
) -> Path:
    if scope == "research_topic" and research_topic_id:
        return project.config_dir / "user-skill-callbacks" / "topics" / research_topic_id / "prompts" / f"{callback_id}.md"
    return project.config_dir / "user-skill-callbacks" / "prompts" / f"{callback_id}.md"


def callback_registry_ref_values_from_raw(raw: dict[str, Any]) -> tuple[str, ...]:
    values = _string_refs(raw.get("user_skill_callback_registry_ref"))
    values.extend(_string_refs(raw.get("user_skill_callback_registry_refs")))
    nested_refs = raw.get("refs")
    if isinstance(nested_refs, dict):
        values.extend(_string_refs(nested_refs.get("user_skill_callback_registry_ref")))
        values.extend(_string_refs(nested_refs.get("user_skill_callback_registry_refs")))
    return tuple(dict.fromkeys(values))


def secret_like_diagnostics(
    value: object,
    concept: str,
    path: Path,
    field_path: tuple[str, ...],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    _scan_secret_like(value, concept, path, field_path, diagnostics)
    return diagnostics


def _parse_callback_item(
    project: Project,
    ref: CallbackRegistryRef,
    item: dict[str, Any],
    index: int,
) -> tuple[UserSkillCallback | None, list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    field = f"callbacks[{index}]"
    callback_id = _string(item.get("id"))
    skill = _string(item.get("skill"))
    stage = _string(item.get("stage"))
    scope = _string(item.get("scope")) or ref.scope
    status = _string(item.get("status")) or "active"
    source_type = _string(item.get("source_type"))
    priority = item.get("priority", DEFAULT_CALLBACK_PRIORITY)
    diagnostics.extend(_callback_identity_diagnostics(skill=skill, stage=stage, scope=scope, callback_id=callback_id))
    if status not in VALID_CALLBACK_STATUSES:
        diagnostics.append(
            Diagnostic(
                code="ISO102",
                severity="error",
                concept="User Skill Callback registry",
                path=ref.path,
                field=f"{field}.status",
                message="User Skill Callback status must be active, inactive, or disabled.",
            )
        )
    if not isinstance(priority, int) or priority < 0:
        diagnostics.append(
            Diagnostic(
                code="ISO102",
                severity="error",
                concept="User Skill Callback registry",
                path=ref.path,
                field=f"{field}.priority",
                message="User Skill Callback priority must be a zero-or-greater integer.",
            )
        )
        priority = DEFAULT_CALLBACK_PRIORITY
    if source_type not in VALID_CALLBACK_SOURCE_TYPES:
        diagnostics.append(
            Diagnostic(
                code="ISO102",
                severity="error",
                concept="User Skill Callback registry",
                path=ref.path,
                field=f"{field}.source_type",
                message="User Skill Callback source_type must be prompt, prompt_file, or skill_dir.",
            )
        )
    source_path_input = _string(item.get("skill_dir" if source_type == "skill_dir" else "prompt_file"))
    if source_path_input is None:
        diagnostics.append(
            Diagnostic(
                code="ISO102",
                severity="error",
                concept="User Skill Callback registry",
                path=ref.path,
                field=f"{field}.source",
                message="User Skill Callback source must point to prompt_file or skill_dir according to source_type.",
            )
        )
    if has_errors(diagnostics) or callback_id is None or skill is None or stage is None or source_type is None or source_path_input is None:
        return None, diagnostics
    source_path = resolve_project_path(project.root, source_path_input)
    external = not is_within(source_path, project.root)
    external_source = bool(item.get("external_source", False))
    if external and not external_source:
        diagnostics.append(
            Diagnostic(
                code="ISO005",
                severity="error",
                concept="User Skill Callback source",
                path=ref.path,
                field=f"{field}.source",
                message="Callback source resolves outside the Project root without external_source = true.",
            )
        )
    source = CallbackSource(
        source_type=source_type,
        path_input=source_path_input,
        resolved_path=source_path,
        external=external,
    )
    diagnostics.extend(_source_file_diagnostics(source))
    if has_errors(diagnostics):
        return None, diagnostics
    return (
        UserSkillCallback(
            id=callback_id,
            skill=skill,
            stage=stage,
            scope=scope,
            status=status,
            priority=priority,
            source=source,
            registry_path=ref.path,
            research_topic_id=ref.research_topic_id if scope == "research_topic" else None,
        ),
        diagnostics,
    )


def _callback_identity_diagnostics(
    *,
    skill: str | None,
    stage: str | None,
    scope: str | None,
    callback_id: str | None,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if callback_id is not None and not CALLBACK_ID_RE.match(callback_id):
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="User Skill Callback",
                field="id",
                message="User Skill Callback id must start with an alphanumeric character and contain only letters, numbers, underscore, dot, or dash.",
            )
        )
    if skill is None:
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="User Skill Callback",
                field="skill",
                message="User Skill Callback must target a system skill name.",
            )
        )
    elif skill not in active_system_skill_names():
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="User Skill Callback",
                field="skill",
                message=f"User Skill Callback target is not an active packaged system skill: {skill}.",
            )
        )
    if stage is None:
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="User Skill Callback",
                field="stage",
                message="User Skill Callback must include a stage.",
            )
        )
    elif stage not in VALID_CALLBACK_STAGES:
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="User Skill Callback",
                field="stage",
                message="User Skill Callback stage must be begin or end.",
            )
        )
    if scope is not None and scope not in VALID_CALLBACK_SCOPES:
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="User Skill Callback",
                field="scope",
                message="User Skill Callback scope must be project or research_topic.",
            )
        )
    return diagnostics


def active_system_skill_names() -> frozenset[str]:
    try:
        return frozenset(Path(path).name for path in iter_system_skill_paths())
    except SystemSkillAssetError:
        return frozenset()


def _source_file_diagnostics(source: CallbackSource) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if source.source_type in {"prompt", "prompt_file"}:
        if not source.resolved_path.exists():
            diagnostics.append(_missing_source_diagnostic("prompt_file", source.resolved_path))
        elif not source.resolved_path.is_file():
            diagnostics.append(
                Diagnostic(
                    code="ISO103",
                    severity="error",
                    concept="User Skill Callback source",
                    path=source.resolved_path,
                    field="prompt_file",
                    message="Callback prompt source must be a file.",
                )
            )
        else:
            try:
                content = source.resolved_path.read_text(encoding="utf-8")
            except OSError as exc:
                diagnostics.append(
                    Diagnostic(
                        code="ISO001",
                        severity="error",
                        concept="User Skill Callback source",
                        path=source.resolved_path,
                        field="prompt_file",
                        message=f"Callback prompt source could not be read: {exc}",
                    )
                )
            else:
                diagnostics.extend(secret_like_diagnostics(content, "User Skill Callback prompt", source.resolved_path, ("prompt_file",)))
    elif not (source.resolved_path / "SKILL.md").is_file():
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="User Skill Callback source",
                path=source.resolved_path,
                field="skill_dir",
                message="Callback skill directory source must contain SKILL.md.",
            )
        )
    return diagnostics


def _missing_source_diagnostic(kind: str, path: Path) -> Diagnostic:
    return Diagnostic(
        code="ISO001",
        severity="error",
        concept="User Skill Callback source",
        path=path,
        field=kind,
        message="Callback source path does not exist.",
    )


def _callback_sort_key(callback: UserSkillCallback) -> tuple[int, int, str]:
    scope_rank = 0 if callback.scope == "research_topic" else 1
    return (scope_rank, callback.priority, callback.id)


def _duplicate_active_callback_diagnostics(project: Project, refs: Iterable[CallbackRegistryRef]) -> list[Diagnostic]:
    callbacks: list[UserSkillCallback] = []
    diagnostics: list[Diagnostic] = []
    for ref in refs:
        result = load_callback_registry(project, ref, missing_severity="error")
        if has_errors(list(result.diagnostics)):
            continue
        callbacks.extend(callback for callback in result.callbacks if callback.active)
    counts = Counter(callback.id for callback in callbacks)
    for callback_id in sorted(id_ for id_, count in counts.items() if count > 1):
        diagnostics.append(
            Diagnostic(
                code="ISO104",
                severity="error",
                concept="User Skill Callback",
                field="callbacks.id",
                message=f"Duplicate active User Skill Callback id is visible: {callback_id}.",
            )
        )
    return diagnostics


def _validate_registry_ref_path(project: Project, ref: CallbackRegistryRef) -> list[Diagnostic]:
    if is_within(ref.path, project.root):
        return []
    return [
        Diagnostic(
            code="ISO005",
            severity="error",
            concept="User Skill Callback registry",
            path=ref.source_path,
            field="user_skill_callback_registry_refs",
            message="User Skill Callback registry ref resolves outside the Project root.",
        )
    ]


def _callback_registry_ref_values(refs: dict[str, Any]) -> tuple[str, ...]:
    values: list[str] = []
    values.extend(_string_refs(refs.get("user_skill_callback_registry_ref")))
    values.extend(_string_refs(refs.get("user_skill_callback_registry_refs")))
    return tuple(dict.fromkeys(values))


def _string_refs(value: object) -> list[str]:
    if isinstance(value, str) and value:
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str) and item]
    return []


def _string(value: object) -> str | None:
    if isinstance(value, str) and value:
        return value
    return None


def _with_severity(diagnostics: list[Diagnostic], severity: str) -> list[Diagnostic]:
    if severity not in {"error", "warning"}:
        severity = "error"
    return [
        Diagnostic(
            code=diagnostic.code,
            severity=severity,  # type: ignore[arg-type]
            concept=diagnostic.concept,
            message=diagnostic.message,
            path=diagnostic.path,
            field=diagnostic.field,
            line=diagnostic.line,
            hint=diagnostic.hint,
            usage=diagnostic.usage,
            examples=diagnostic.examples,
        )
        for diagnostic in diagnostics
    ]


def _scan_secret_like(
    value: object,
    concept: str,
    path: Path,
    field_path: tuple[str, ...],
    diagnostics: list[Diagnostic],
) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            nested = (*field_path, str(key))
            normalized_key = str(key).lower().replace("-", "_").replace(" ", "_")
            if any(term in normalized_key for term in SECRET_KEY_TERMS):
                diagnostics.append(
                    Diagnostic(
                        code="ISO010",
                        severity="error",
                        concept=concept,
                        path=path,
                        field=".".join(nested),
                        message="Inline secret-like material is not allowed in User Skill Callback material.",
                    )
                )
            _scan_secret_like(item, concept, path, nested, diagnostics)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _scan_secret_like(item, concept, path, (*field_path, f"[{index}]"), diagnostics)
    elif isinstance(value, str) and SECRET_VALUE_RE.search(value):
        diagnostics.append(
            Diagnostic(
                code="ISO010",
                severity="error",
                concept=concept,
                path=path,
                field=".".join(field_path) or None,
                message="Inline secret-like material is not allowed in User Skill Callback material.",
            )
        )


def _write_callback_registry(path: Path, callbacks: Iterable[UserSkillCallback]) -> None:
    document = tomlkit.document()
    document["schema_version"] = USER_SKILL_CALLBACK_REGISTRY_SCHEMA_VERSION
    callback_items = tomlkit.aot()
    for callback in sorted(callbacks, key=_callback_sort_key):
        table = tomlkit.table()
        table["id"] = callback.id
        table["skill"] = callback.skill
        table["stage"] = callback.stage
        table["scope"] = callback.scope
        if callback.research_topic_id is not None:
            table["research_topic_id"] = callback.research_topic_id
        table["status"] = callback.status
        table["priority"] = callback.priority
        table["source_type"] = callback.source.source_type
        if callback.source.source_type == "skill_dir":
            table["skill_dir"] = callback.source.path_input
        else:
            table["prompt_file"] = callback.source.path_input
        if callback.source.external:
            table["external_source"] = True
        callback_items.append(table)
    document["callbacks"] = callback_items
    _atomic_write(path, tomlkit.dumps(document))


def _ensure_registry_ref(project: Project, ref: CallbackRegistryRef) -> None:
    if ref.scope == "project":
        document = tomlkit.parse(project.manifest_path.read_text(encoding="utf-8"))
        changed = _append_ref(document, "user_skill_callback_registry_refs", ref.path_input)
        if changed:
            _atomic_write(project.manifest_path, tomlkit.dumps(document))
        return
    if ref.source_path.exists():
        document = tomlkit.parse(ref.source_path.read_text(encoding="utf-8"))
    else:
        document = tomlkit.document()
    changed = _append_ref(document, "user_skill_callback_registry_refs", ref.path_input)
    if changed:
        _atomic_write(ref.source_path, tomlkit.dumps(document))


def _append_ref(document: Any, key: str, value: str) -> bool:
    singular_key = key.removesuffix("s")
    existing_values = _string_refs(document.get(key))
    existing_values.extend(_string_refs(document.get(singular_key)))
    if value in existing_values:
        return False
    existing_values.append(value)
    array = tomlkit.array()
    array.multiline(False)
    for item in dict.fromkeys(existing_values):
        array.append(item)
    document[key] = array
    return True


def _atomic_write(path: Path, text: str) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)
