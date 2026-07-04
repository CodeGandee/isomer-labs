"""CLI-facing User Skill Callback operations."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from isomer_labs.core.diagnostics import Diagnostic, has_errors
from isomer_labs.core.path_utils import display_path, is_within, resolve_project_path
from isomer_labs.models import EffectiveTopicContext, Project, ProjectState
from isomer_labs.project.skill_callbacks import (
    DEFAULT_CALLBACK_PRIORITY,
    CallbackRegistryRef,
    CallbackSource,
    UserSkillCallback,
    _callback_identity_diagnostics,
    _callback_sort_key,
    _duplicate_active_callback_diagnostics,
    _ensure_registry_ref,
    _missing_source_diagnostic,
    _write_callback_registry,
    default_callback_registry_path,
    load_callback_registry,
    managed_prompt_path,
    secret_like_diagnostics,
    visible_callback_registry_refs,
)


@dataclass(frozen=True)
class CallbackCommandResult:
    ok: bool
    mutated: bool
    project_root: Path
    callbacks: tuple[UserSkillCallback, ...]
    diagnostics: tuple[Diagnostic, ...]
    registry_refs: tuple[CallbackRegistryRef, ...] = ()
    callback: UserSkillCallback | None = None
    previous_status: str | None = None
    new_status: str | None = None

    def to_json(self) -> dict[str, object]:
        project_root = self.project_root
        payload: dict[str, object] = {
            "ok": self.ok,
            "mutated": self.mutated,
            "project_root": str(project_root),
            "callbacks": [callback.to_json(project_root) for callback in self.callbacks],
            "registry_refs": [ref.to_json(project_root) for ref in self.registry_refs],
        }
        if self.callback is not None:
            payload["callback"] = self.callback.to_json(project_root)
        if self.previous_status is not None:
            payload["previous_status"] = self.previous_status
        if self.new_status is not None:
            payload["new_status"] = self.new_status
        return payload


def register_user_skill_callback(
    state: ProjectState,
    context: EffectiveTopicContext | None,
    *,
    callback_id: str | None,
    skill: str,
    stage: str,
    scope: str,
    priority: int | None,
    prompt: str | None,
    prompt_file: str | None,
    skill_dir: str | None,
    allow_external_source: bool,
) -> CallbackCommandResult:
    project = state.project
    diagnostics: list[Diagnostic] = []
    diagnostics.extend(_callback_identity_diagnostics(skill=skill, stage=stage, scope=scope, callback_id=callback_id))
    if scope == "research_topic" and context is None:
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="User Skill Callback",
                field="scope",
                message="Research Topic scoped callbacks require a selected Research Topic.",
            )
        )
    effective_id = callback_id or _generated_callback_id(skill, stage, prompt_file or skill_dir or "prompt")
    diagnostics.extend(_callback_identity_diagnostics(skill=skill, stage=stage, scope=scope, callback_id=effective_id))
    callback_priority = priority if priority is not None else DEFAULT_CALLBACK_PRIORITY
    if callback_priority < 0:
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="User Skill Callback",
                field="priority",
                message="User Skill Callback priority must be zero or greater.",
            )
        )
    source_kind, source_path_input, source_diagnostics, prompt_material = prepare_callback_source(
        project,
        scope=scope,
        research_topic_id=context.research_topic.id if context is not None else None,
        callback_id=effective_id,
        prompt=prompt,
        prompt_file=prompt_file,
        skill_dir=skill_dir,
        allow_external_source=allow_external_source,
    )
    diagnostics.extend(source_diagnostics)
    if source_kind is None or source_path_input is None:
        return CallbackCommandResult(False, False, project.root, (), tuple(diagnostics))
    if has_errors(diagnostics):
        return CallbackCommandResult(False, False, project.root, (), tuple(diagnostics))

    registry_path = default_callback_registry_path(
        project,
        scope=scope,
        research_topic_id=context.research_topic.id if context is not None else None,
    )
    registry_path_input = display_path(registry_path, project.root)
    ref = CallbackRegistryRef(
        scope=scope,
        path_input=registry_path_input,
        path=registry_path,
        source_path=context.research_topic_config.source_path if scope == "research_topic" and context is not None and context.research_topic_config is not None else project.manifest_path,
        research_topic_id=context.research_topic.id if scope == "research_topic" and context is not None else None,
    )
    existing_result = load_callback_registry(project, ref, missing_severity="warning")
    existing_callbacks = [callback for callback in existing_result.callbacks if callback.id != effective_id]
    prompt_source_path = resolve_project_path(project.root, source_path_input)
    source = CallbackSource(
        source_type=source_kind,
        path_input=source_path_input,
        resolved_path=prompt_source_path,
        external=not is_within(prompt_source_path, project.root),
    )
    callback = UserSkillCallback(
        id=effective_id,
        skill=skill,
        stage=stage,
        scope=scope,
        status="active",
        priority=callback_priority,
        source=source,
        registry_path=registry_path,
        research_topic_id=context.research_topic.id if scope == "research_topic" and context is not None else None,
    )
    callbacks = [*existing_callbacks, callback]
    if prompt_material is not None:
        prompt_source_path.parent.mkdir(parents=True, exist_ok=True)
        prompt_source_path.write_text(prompt_material, encoding="utf-8")
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    _write_callback_registry(registry_path, callbacks)
    _ensure_registry_ref(project, ref)
    return CallbackCommandResult(
        ok=True,
        mutated=True,
        project_root=project.root,
        callbacks=(callback,),
        callback=callback,
        registry_refs=(ref,),
        diagnostics=(),
    )


def prepare_callback_source(
    project: Project,
    *,
    scope: str,
    research_topic_id: str | None,
    callback_id: str,
    prompt: str | None,
    prompt_file: str | None,
    skill_dir: str | None,
    allow_external_source: bool,
) -> tuple[str | None, str | None, list[Diagnostic], str | None]:
    diagnostics: list[Diagnostic] = []
    sources = [
        ("prompt", prompt),
        ("prompt_file", prompt_file),
        ("skill_dir", skill_dir),
    ]
    selected = [(kind, value) for kind, value in sources if isinstance(value, str) and value]
    if len(selected) != 1:
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="User Skill Callback source",
                message="Provide exactly one of --prompt, --prompt-file, or --skill-dir.",
            )
        )
        return None, None, diagnostics, None
    kind, value = selected[0]
    assert value is not None
    if kind == "prompt":
        if not value.strip():
            diagnostics.append(
                Diagnostic(
                    code="ISO103",
                    severity="error",
                    concept="User Skill Callback source",
                    field="prompt",
                    message="Inline callback prompt must not be empty.",
                )
            )
        diagnostics.extend(secret_like_diagnostics(value, "User Skill Callback prompt", Path("<inline>"), ("prompt",)))
        path = managed_prompt_path(
            project,
            scope=scope,
            research_topic_id=research_topic_id,
            callback_id=callback_id,
        )
        return "prompt", display_path(path, project.root), diagnostics, value.rstrip() + "\n"

    resolved = resolve_project_path(project.root, value)
    external = not is_within(resolved, project.root)
    if external and not allow_external_source:
        diagnostics.append(
            Diagnostic(
                code="ISO005",
                severity="error",
                concept="User Skill Callback source",
                field=kind,
                message="Callback source resolves outside the Project root; pass --allow-external-source to register it explicitly.",
            )
        )
    if kind == "prompt_file":
        if not resolved.exists():
            diagnostics.append(_missing_source_diagnostic(kind, resolved))
        elif not resolved.is_file():
            diagnostics.append(
                Diagnostic(
                    code="ISO103",
                    severity="error",
                    concept="User Skill Callback source",
                    path=resolved,
                    field="prompt_file",
                    message="Callback prompt file source must be a readable file.",
                )
            )
        else:
            try:
                content = resolved.read_text(encoding="utf-8")
            except OSError as exc:
                diagnostics.append(
                    Diagnostic(
                        code="ISO001",
                        severity="error",
                        concept="User Skill Callback source",
                        path=resolved,
                        field="prompt_file",
                        message=f"Callback prompt file could not be read: {exc}",
                    )
                )
            else:
                diagnostics.extend(secret_like_diagnostics(content, "User Skill Callback prompt", resolved, ("prompt_file",)))
        return "prompt_file", value, diagnostics, None

    if not resolved.exists():
        diagnostics.append(_missing_source_diagnostic(kind, resolved))
    elif not resolved.is_dir():
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="User Skill Callback source",
                path=resolved,
                field="skill_dir",
                message="Callback skill directory source must be a directory.",
            )
        )
    elif not (resolved / "SKILL.md").is_file():
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="User Skill Callback source",
                path=resolved,
                field="skill_dir",
                message="Callback skill directory source must contain SKILL.md.",
            )
        )
    return "skill_dir", value, diagnostics, None


def resolve_user_skill_callbacks(
    state: ProjectState,
    context: EffectiveTopicContext | None,
    *,
    skill: str,
    stage: str,
) -> CallbackCommandResult:
    project = state.project
    diagnostics: list[Diagnostic] = _callback_identity_diagnostics(skill=skill, stage=stage, scope=None, callback_id=None)
    callbacks, refs, load_diagnostics = _load_visible_callbacks(project, context, missing_severity="warning")
    diagnostics.extend(load_diagnostics)
    selected = tuple(
        sorted(
            (callback for callback in callbacks if callback.active and callback.skill == skill and callback.stage == stage),
            key=_callback_sort_key,
        )
    )
    return CallbackCommandResult(
        ok=not has_errors(diagnostics),
        mutated=False,
        project_root=project.root,
        callbacks=selected,
        registry_refs=refs,
        diagnostics=tuple(diagnostics),
    )


def list_user_skill_callbacks(
    state: ProjectState,
    context: EffectiveTopicContext | None,
) -> CallbackCommandResult:
    project = state.project
    callbacks, refs, diagnostics = _load_visible_callbacks(project, context, missing_severity="warning")
    return CallbackCommandResult(
        ok=not has_errors(diagnostics),
        mutated=False,
        project_root=project.root,
        callbacks=tuple(sorted(callbacks, key=_callback_sort_key)),
        registry_refs=refs,
        diagnostics=tuple(diagnostics),
    )


def show_user_skill_callback(
    state: ProjectState,
    context: EffectiveTopicContext | None,
    *,
    callback_id: str,
) -> CallbackCommandResult:
    project = state.project
    callbacks, refs, diagnostics = _load_visible_callbacks(project, context, missing_severity="warning")
    matches = [callback for callback in callbacks if callback.id == callback_id]
    if not matches:
        diagnostics.append(
            Diagnostic(
                code="ISO104",
                severity="error",
                concept="User Skill Callback",
                field="callback_id",
                message=f"User Skill Callback was not found: {callback_id}.",
            )
        )
    selected = tuple(sorted(matches, key=_callback_sort_key))
    return CallbackCommandResult(
        ok=not has_errors(diagnostics),
        mutated=False,
        project_root=project.root,
        callbacks=selected,
        callback=selected[0] if selected else None,
        registry_refs=refs,
        diagnostics=tuple(diagnostics),
    )


def disable_user_skill_callback(
    state: ProjectState,
    context: EffectiveTopicContext | None,
    *,
    callback_id: str,
) -> CallbackCommandResult:
    project = state.project
    refs = visible_callback_registry_refs(project, context)
    diagnostics: list[Diagnostic] = []
    matches: list[UserSkillCallback] = []
    loaded = []
    for ref in refs:
        result = load_callback_registry(project, ref, missing_severity="warning")
        loaded.append(result)
        diagnostics.extend(result.diagnostics)
        matches.extend(callback for callback in result.callbacks if callback.id == callback_id)
    if not matches:
        diagnostics.append(
            Diagnostic(
                code="ISO104",
                severity="error",
                concept="User Skill Callback",
                field="callback_id",
                message=f"User Skill Callback was not found: {callback_id}.",
            )
        )
        return CallbackCommandResult(False, False, project.root, (), tuple(diagnostics), registry_refs=refs)
    active_matches = [callback for callback in matches if callback.active]
    selected = sorted(active_matches or matches, key=_callback_sort_key)[0]
    previous_status = selected.status
    replacement = UserSkillCallback(
        id=selected.id,
        skill=selected.skill,
        stage=selected.stage,
        scope=selected.scope,
        status="inactive",
        priority=selected.priority,
        source=selected.source,
        registry_path=selected.registry_path,
        research_topic_id=selected.research_topic_id,
    )
    for result in loaded:
        if result.ref.path != selected.registry_path:
            continue
        updated = [replacement if callback.id == selected.id else callback for callback in result.callbacks]
        _write_callback_registry(selected.registry_path, updated)
        break
    return CallbackCommandResult(
        ok=not has_errors(diagnostics),
        mutated=True,
        project_root=project.root,
        callbacks=(replacement,),
        callback=replacement,
        registry_refs=refs,
        diagnostics=tuple(diagnostics),
        previous_status=previous_status,
        new_status="inactive",
    )


def validate_user_skill_callbacks(
    state: ProjectState,
    context: EffectiveTopicContext | None,
) -> CallbackCommandResult:
    project = state.project
    refs = visible_callback_registry_refs(project, context)
    diagnostics: list[Diagnostic] = []
    all_callbacks: list[UserSkillCallback] = []
    for ref in refs:
        result = load_callback_registry(project, ref, missing_severity="error")
        diagnostics.extend(result.diagnostics)
        all_callbacks.extend(result.callbacks)
    diagnostics.extend(_duplicate_active_callback_diagnostics(project, refs))
    return CallbackCommandResult(
        ok=not has_errors(diagnostics),
        mutated=False,
        project_root=project.root,
        callbacks=tuple(sorted(all_callbacks, key=_callback_sort_key)),
        registry_refs=refs,
        diagnostics=tuple(diagnostics),
    )


def _load_visible_callbacks(
    project: Project,
    context: EffectiveTopicContext | None,
    *,
    missing_severity: str,
) -> tuple[tuple[UserSkillCallback, ...], tuple[CallbackRegistryRef, ...], list[Diagnostic]]:
    refs = visible_callback_registry_refs(project, context)
    callbacks: list[UserSkillCallback] = []
    diagnostics: list[Diagnostic] = []
    for ref in refs:
        result = load_callback_registry(project, ref, missing_severity=missing_severity)
        diagnostics.extend(result.diagnostics)
        callbacks.extend(result.callbacks)
    return tuple(callbacks), refs, diagnostics


def _generated_callback_id(skill: str, stage: str, source_hint: str) -> str:
    hint = Path(source_hint).stem if source_hint else "prompt"
    suffix = re.sub(r"[^A-Za-z0-9_.-]+", "-", hint).strip("-._") or "prompt"
    return f"{skill}-{stage}-{suffix}"
