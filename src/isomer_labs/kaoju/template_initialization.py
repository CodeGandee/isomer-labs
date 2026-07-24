"""Topic-initialization support for Kaoju writing-template stock."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

from isomer_labs.kaoju.artifacts import KaojuServiceError
from isomer_labs.kaoju.template_exchange import KaojuTemplateExchangeService
from isomer_labs.kaoju.template_support import (
    DEFAULT_TEMPLATE_NAME,
    EXPORT_METADATA_NAME,
    TemplateSelection,
    _load_export_metadata,
    template_tree_digest,
)
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.workspace.path_resolution import resolve_semantic_path


def ensure_default_templates(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    cwd: Path,
    actor: str,
) -> dict[str, object]:
    """Create and safely export missing role-local ``main`` stock."""

    overview, diagnostics = resolve_semantic_path(
        context,
        "topic.intent.overview",
        env=env,
        cwd=cwd,
    )
    if overview is None:
        return {
            "ok": False,
            "mutated": False,
            "operation": "paper.template.ensure-defaults",
            "roles": [],
            "diagnostics": [
                {
                    "severity": "error",
                    "code": "topic_overview_unavailable",
                    "message": item.message,
                    "path": (
                        str(item.path)
                        if item.path is not None
                        else None
                    ),
                }
                for item in diagnostics
            ],
            "next_actions": [
                "Complete generic topic creation and Workspace Runtime initialization, then retry.",
            ],
        }
    try:
        overview_text = overview.path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        overview_text = ""
        diagnostics_payload = [
            {
                "severity": "error",
                "code": "topic_overview_unreadable",
                "message": (
                    f"Concrete topic overview is unreadable: {exc}"
                ),
                "path": str(overview.path),
            }
        ]
    else:
        diagnostics_payload = []
    if not overview_text.strip():
        if not diagnostics_payload:
            diagnostics_payload.append(
                {
                    "severity": "error",
                    "code": "topic_overview_empty",
                    "message": (
                        "Concrete topic overview must be non-empty before "
                        "Kaoju template initialization."
                    ),
                    "path": str(overview.path),
                }
            )
        return {
            "ok": False,
            "mutated": False,
            "operation": "paper.template.ensure-defaults",
            "roles": [],
            "diagnostics": diagnostics_payload,
            "next_actions": [
                "Complete the concrete topic overview, then retry.",
            ],
        }

    from isomer_labs.kaoju.template_defaults import load_packaged_template
    from isomer_labs.kaoju.templates import KaojuTemplateService

    roles: list[dict[str, object]] = []
    affected_refs: list[str] = []
    for kind in ("content", "latex"):
        service = KaojuTemplateService(
            context,
            env=env,
            cwd=cwd,
            kind=kind,
        )
        role: dict[str, object] = {
            "template_kind": kind,
            "name": DEFAULT_TEMPLATE_NAME,
            "created": False,
            "preserved": False,
            "exported": False,
            "fallback_available": False,
            "posture": "pending",
        }
        try:
            packaged = load_packaged_template(kind)
            role["fallback_available"] = True
            role["packaged_identity"] = packaged.identity
            role["packaged_resource_version"] = (
                packaged.resource_version
            )
            role["packaged_tree_digest"] = packaged.tree_digest
            claims = service._records_claiming_name(
                DEFAULT_TEMPLATE_NAME
            )
            if claims:
                selection = service.resolve_selection()
                role["preserved"] = True
                role["posture"] = "preserved"
            else:
                created = service.create(
                    DEFAULT_TEMPLATE_NAME,
                    source=packaged.root,
                    authored_metadata=packaged.authored_metadata,
                    actor=actor,
                    source_refs=(packaged.identity,),
                    change_summary=(
                        "Initialize role-local main stock from the "
                        "checked packaged default."
                    ),
                )
                role["created"] = True
                role["posture"] = "created"
                role["audit_ref"] = created.get("audit_ref")
                created_refs = created.get("affected_refs")
                if isinstance(created_refs, list):
                    affected_refs.extend(
                        value
                        for value in created_refs
                        if isinstance(value, str)
                    )
                selection = service.resolve_selection()
            role.update(
                {
                    "stable_ref": selection.stable_ref,
                    "state_token": selection.state_token,
                    "tree_digest": selection.tree_digest,
                }
            )
            target = service._default_working_path(
                DEFAULT_TEMPLATE_NAME,
                materialize=False,
            )
            role["exchange_path"] = str(target)
            export_posture = _initialization_export_posture(
                service,
                selection,
                target,
            )
            if export_posture == "absent":
                exported = service.export(
                    DEFAULT_TEMPLATE_NAME,
                    actor=actor,
                )
                role["exported"] = True
                role["export_posture"] = "exported"
                exported_refs = exported.get("affected_refs")
                if isinstance(exported_refs, list):
                    affected_refs.extend(
                        value
                        for value in exported_refs
                        if isinstance(value, str)
                    )
            else:
                role["export_posture"] = export_posture
                if export_posture in {
                    "unrecognized",
                    "identity-invalid",
                }:
                    role["posture"] = "conflicting"
        except KaojuServiceError as exc:
            role["posture"] = (
                "conflicting"
                if exc.code.startswith("template_export_")
                or exc.code == "template_identity_conflict"
                else "invalid"
            )
            role["error"] = exc.payload()["error"]
            role["recovery_actions"] = list(
                exc.recovery_actions
            )
        roles.append(role)
    blocking = [
        role
        for role in roles
        if role.get("posture") in {"invalid", "conflicting"}
    ]
    return {
        "ok": not blocking,
        "mutated": any(
            role.get("created") is True
            or role.get("exported") is True
            for role in roles
        ),
        "operation": "paper.template.ensure-defaults",
        "roles": roles,
        "affected_refs": affected_refs,
        "diagnostics": [],
        "next_actions": (
            [
                "Resolve each invalid or conflicting role, then repeat ensure-defaults.",
            ]
            if blocking
            else [
                "Review the plural-path working copies before later paper work.",
                "After editing, ask the Kaoju agent to apply the modified derived materials.",
            ]
        ),
    }


def _initialization_export_posture(
    service: KaojuTemplateExchangeService,
    selection: TemplateSelection,
    target: Path,
) -> str:
    if not target.exists():
        return "absent"
    if not target.is_dir():
        return "unrecognized"
    entries = list(target.iterdir())
    if not entries:
        return "absent"
    metadata_path = target / EXPORT_METADATA_NAME
    if not metadata_path.is_file():
        return "unrecognized"
    try:
        metadata = _load_export_metadata(
            metadata_path,
            expected_kind=service.template_kind.kind,
        )
        if not service._metadata_matches_selection(
            metadata,
            selection,
        ):
            return "identity-invalid"
        working_digest = template_tree_digest(
            target,
            exclude_exchange_metadata=True,
        )
    except KaojuServiceError:
        return "identity-invalid"
    if working_digest != metadata.get("exported_tree_digest"):
        return "edited"
    if (
        metadata.get("state_token") != selection.state_token
        or metadata.get("canonical_tree_digest")
        != selection.tree_digest
    ):
        return "canonical-changed"
    return "unchanged"
