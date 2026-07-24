"""Inventory and future-facing application of recognized Kaoju derived intent."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Mapping

from isomer_labs.kaoju.artifacts import KaojuServiceError
from isomer_labs.kaoju.mindsets import (
    DEFAULT_KEYS,
    SOURCE_SEMANTIC_LABEL,
    canonical_digest,
    ensure_mindset_sources,
    load_mindset_source,
    mindset_source_child,
)
from isomer_labs.kaoju.template_initialization import ensure_default_templates
from isomer_labs.kaoju.templates import KaojuTemplateService
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.workspace.path_resolution import resolve_semantic_path


GENERATED_DERIVED_LABELS = (
    "topic.env.topic_setup_target_spec",
    "topic.env.agent_setup_target_spec",
    "topic.env.actor_env_gates",
)


def initialize_derived_intent(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    cwd: Path,
    actor: str,
    specialize: Callable[
        [Mapping[str, Any], str],
        Mapping[str, Any],
    ]
    | None = None,
) -> dict[str, object]:
    """Initialize missing Mindset Sources and default template stock."""

    mindsets = ensure_mindset_sources(
        context,
        env=env,
        cwd=cwd,
        specialize=specialize,
    )
    templates = ensure_default_templates(
        context,
        env=env,
        cwd=cwd,
        actor=actor,
    )
    return {
        "ok": mindsets.get("ok") is True and templates.get("ok") is True,
        "mutated": (
            mindsets.get("mutated") is True
            or templates.get("mutated") is True
        ),
        "operation": "derived-intent.initialize",
        "mindsets": mindsets,
        "writing_templates": templates,
        "initialization_boundary": "derived-intent-ready",
        "next_actions": [
            "Review intent/derived Mindset Sources and non-canonical writing-template exports.",
            "Edit supported material now or later, then ask to apply the modified derived materials.",
        ],
    }


def inventory_derived_intent(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    cwd: Path,
) -> dict[str, object]:
    """Inspect only semantic Mindset Sources, registered exports, and generated targets."""

    materials: list[dict[str, object]] = []
    diagnostics: list[dict[str, object]] = []
    mindset_root, mindset_path_diagnostics = resolve_semantic_path(
        context,
        SOURCE_SEMANTIC_LABEL,
        env=env,
        cwd=cwd,
    )
    diagnostics.extend(
        {
            "severity": item.severity,
            "code": item.code,
            "message": item.message,
            "path": str(item.path) if item.path is not None else None,
        }
        for item in mindset_path_diagnostics
    )
    if mindset_root is not None:
        for key in DEFAULT_KEYS:
            path = mindset_source_child(mindset_root.path, key)
            if not path.exists():
                materials.append(
                    {
                        "material_type": "mindset-source",
                        "mindset_key": key,
                        "semantic_label": SOURCE_SEMANTIC_LABEL,
                        "path": str(path),
                        "posture": "missing",
                        "application_route": "create-topic",
                    }
                )
                continue
            source, source_diagnostics = load_mindset_source(
                path,
                expected_key=key,
            )
            materials.append(
                {
                    "material_type": "mindset-source",
                    "mindset_key": key,
                    "semantic_label": SOURCE_SEMANTIC_LABEL,
                    "path": str(path),
                    "posture": (
                        "validated"
                        if source is not None and not source_diagnostics
                        else "invalid"
                    ),
                    "digest": (
                        canonical_digest(source)
                        if source is not None and not source_diagnostics
                        else None
                    ),
                    "diagnostics": [
                        item.to_json() for item in source_diagnostics
                    ],
                    "application_route": "direct-source-validation",
                }
            )
    for kind in ("content", "latex"):
        service = KaojuTemplateService(
            context,
            env=env,
            cwd=cwd,
            kind=kind,
        )
        try:
            export_payload = service.exports()
        except KaojuServiceError as exc:
            diagnostics.append(
                {
                    "severity": "error",
                    "code": exc.code,
                    "message": str(exc),
                }
            )
            continue
        exports = export_payload.get("exports")
        for item in exports if isinstance(exports, list) else []:
            if not isinstance(item, dict):
                continue
            materials.append(
                {
                    "material_type": "writing-template-export",
                    "semantic_label": "topic.paper.template_exchange_root",
                    "application_route": "typed-template-promotion",
                    **item,
                }
            )
    for label in GENERATED_DERIVED_LABELS:
        resolution, path_diagnostics = resolve_semantic_path(
            context,
            label,
            env=env,
            cwd=cwd,
        )
        diagnostics.extend(
            {
                "severity": item.severity,
                "code": item.code,
                "message": item.message,
                "path": str(item.path) if item.path is not None else None,
            }
            for item in path_diagnostics
            if item.is_error
        )
        if resolution is not None and resolution.path.exists():
            materials.append(
                {
                    "material_type": "generated-derived-output",
                    "semantic_label": label,
                    "path": str(resolution.path),
                    "posture": "unsupported-direct-override",
                    "application_route": "regenerate-from-source-intent",
                }
            )
    blocking = [
        item
        for item in materials
        if item.get("posture") in {
            "invalid",
            "identity-invalid",
            "canonical-changed",
        }
    ]
    return {
        "ok": not blocking and not any(
            item.get("severity") == "error" for item in diagnostics
        ),
        "mutated": False,
        "operation": "derived-intent.inspect",
        "materials": materials,
        "diagnostics": diagnostics,
        "historical_scope": "preserved",
        "next_actions": [],
    }


def apply_derived_intent(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    cwd: Path,
    actor: str,
) -> dict[str, object]:
    """Validate recognized materials, then promote eligible edited exports."""

    inventory = inventory_derived_intent(context, env=env, cwd=cwd)
    materials = inventory.get("materials")
    inspected = [
        dict(item)
        for item in materials
        if isinstance(item, dict)
    ] if isinstance(materials, list) else []
    blocking = [
        item
        for item in inspected
        if item.get("posture") in {
            "invalid",
            "identity-invalid",
            "canonical-changed",
        }
    ]
    results: list[dict[str, object]] = []
    for item in inspected:
        material_type = item.get("material_type")
        posture = item.get("posture")
        if material_type == "mindset-source":
            results.append(
                {
                    **item,
                    "apply_status": (
                        "validated"
                        if posture == "validated"
                        else posture
                    ),
                }
            )
        elif material_type == "generated-derived-output":
            results.append(
                {
                    **item,
                    "apply_status": "unsupported",
                    "recovery": (
                        "Edit the corresponding source intent and invoke the owning "
                        "environment regeneration workflow."
                    ),
                }
            )
        elif material_type == "writing-template-export":
            if posture != "edited":
                results.append(
                    {
                        **item,
                        "apply_status": posture,
                    }
                )
                continue
            if blocking:
                results.append(
                    {
                        **item,
                        "apply_status": "preflight-blocked",
                        "recovery": (
                            "Resolve invalid or stale recognized material, then repeat "
                            "the complete apply request."
                        ),
                    }
                )
                continue
            try:
                promoted = KaojuTemplateService(
                    context,
                    env=env,
                    cwd=cwd,
                    kind=str(item["template_kind"]),
                ).promote_export(
                    Path(str(item["path"])),
                    actor=actor,
                    change_summary=(
                        "Apply assessed derived writing-template edits for future work."
                    ),
                )
            except KaojuServiceError as exc:
                results.append(
                    {
                        **item,
                        "apply_status": "conflicting",
                        "error": exc.payload()["error"],
                        "recovery_actions": list(exc.recovery_actions),
                    }
                )
            else:
                results.append(
                    {
                        **item,
                        "apply_status": (
                            "promoted"
                            if promoted.get("mutated") is True
                            else "unchanged"
                        ),
                        "stable_ref": promoted.get("stable_ref"),
                        "state_token": promoted.get("state_token"),
                        "tree_digest": promoted.get("tree_digest"),
                        "audit_ref": promoted.get("audit_ref"),
                    }
                )
    failures = [
        item
        for item in results
        if item.get("apply_status") in {
            "invalid",
            "identity-invalid",
            "canonical-changed",
            "preflight-blocked",
            "conflicting",
        }
    ]
    return {
        "ok": not failures,
        "mutated": any(
            item.get("apply_status") == "promoted"
            for item in results
        ),
        "operation": "derived-intent.apply",
        "materials": results,
        "diagnostics": inventory.get("diagnostics", []),
        "future_effective": True,
        "historical_scope": "preserved",
        "retrospective_reconciliation": "requires-explicit-targets",
        "synthetic_aggregate_artifact_created": False,
        "next_actions": (
            [
                "Resolve each reported invalid or conflicting material and repeat apply."
            ]
            if failures
            else [
                "Use the accepted state in later Runs and newly initialized paper work."
            ]
        ),
    }
