"""Result payload builders shared by named-template state and exchange services."""

from __future__ import annotations

from typing import Mapping, Sequence
import uuid

from isomer_labs.kaoju.template_support import TemplateKindSpec, TemplateState, _required_actor


def mutation_payload(
    template_kind: TemplateKindSpec,
    *,
    operation: str,
    name: str,
    stable_ref: str,
    prior_state_token: str | None,
    state_token: str | None,
    prior_tree_digest: str | None,
    tree_digest: str | None,
    audit_ref: str,
    authored_metadata: Mapping[str, object],
    status: str,
    default_working_path: str,
    source_refs: Sequence[str] = (),
    diagnostics: Sequence[Mapping[str, object]] = (),
) -> dict[str, object]:
    next_actions = ["Run 'isomer-cli ext research records index rebuild' to repair query-index state."] if diagnostics else []
    return {
        "ok": True,
        "mutated": True,
        "operation": f"paper.template.{operation}",
        "template_kind": template_kind.kind,
        "template_label": template_kind.label,
        "name": name,
        "stable_ref": stable_ref,
        "status": status,
        "prior_state_token": prior_state_token,
        "state_token": state_token,
        "prior_tree_digest": prior_tree_digest,
        "tree_digest": tree_digest,
        "authored_metadata": dict(authored_metadata),
        "default_working_path": default_working_path,
        "source_refs": list(source_refs),
        "audit_ref": audit_ref,
        "affected_refs": [stable_ref, audit_ref],
        "diagnostics": [dict(item) for item in diagnostics],
        "next_actions": next_actions,
    }


def no_change_payload(
    template_kind: TemplateKindSpec,
    state: TemplateState,
    *,
    operation: str,
    default_working_path: str,
    source_refs: Sequence[str] = (),
) -> dict[str, object]:
    return {
        "ok": True,
        "mutated": False,
        "operation": f"paper.template.{operation}",
        "template_kind": template_kind.kind,
        "template_label": template_kind.label,
        "name": state.name,
        "stable_ref": state.record.id,
        "status": state.record.status,
        "prior_state_token": state.state_token,
        "state_token": state.state_token,
        "prior_tree_digest": state.tree_digest,
        "tree_digest": state.tree_digest,
        "authored_metadata": state.authored_metadata,
        "default_working_path": default_working_path,
        "source_refs": list(source_refs),
        "audit_ref": None,
        "affected_refs": [],
        "diagnostics": [],
        "next_actions": [],
    }


def mutation_summary(
    operation: str,
    actor: str,
    occurred_at: str,
    source_refs: Sequence[str],
    change_summary: str | None,
) -> dict[str, object]:
    return {
        "operation": operation,
        "actor": _required_actor(actor),
        "occurred_at": occurred_at,
        "source_refs": list(source_refs),
        "change_summary": change_summary,
    }


def audit_id(template_kind: TemplateKindSpec, name: str) -> str:
    return f"artifact-paper-template-mutation-audit-{template_kind.kind}-{name}-{uuid.uuid4().hex[:12]}"
