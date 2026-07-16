"""Click registration for Isomer research paper-writing template commands."""

from __future__ import annotations

import os
from dataclasses import replace
from pathlib import Path
from typing import Any, Callable, Literal

import click

from isomer_labs.cli.handlers.shared import _context_for_options
from isomer_labs.cli.options import (
    common_options as _common_options,
    merge_options as _merge_options,
    topic_selection_options as _topic_selection_options,
)
from isomer_labs.cli.output import emit_output
from isomer_labs.core.diagnostics import Diagnostic, has_errors
from isomer_labs.deepsci_ext.tools import dumps_raw_json
from isomer_labs.project.context import EffectiveTopicContext
from isomer_labs.project.validation import ProjectValidationScope
from isomer_labs.records.index import query_index_list
from isomer_labs.records.store import (
    ResearchRecordError,
    ResearchRecordRequest,
    effective_records_list_limit,
    show_record,
)


DEFAULT_TEMPLATE_NAME = "main"
TEMPLATE_RELATIVE_ROOT = Path("intent") / "derived" / "writing-template"
TEMPLATE_SEMANTIC_ID = "KAOJU:WRITING-TEMPLATE"

TemplateCallback = Callable[
    [EffectiveTopicContext, ResearchRecordRequest | None],
    tuple[dict[str, Any], list[Any]],
]


def register_research_templates_commands(research_group: click.Group) -> None:
    @research_group.group(name="templates", help="Inspect and repair legacy non-canonical LaTeX templates; use ext kaoju paper for new paper state.")
    def templates_group() -> None:
        pass

    @templates_group.command(name="create", help="Deprecated: create an explicitly legacy non-canonical LaTeX template.")
    @_common_options
    @_topic_selection_options
    @click.option("--name", "template_name", default=DEFAULT_TEMPLATE_NAME, show_default=True, help="Template name.")
    @click.option("--venue", default=None, help="Target venue or conference.")
    @click.option("--paper-type", default="survey", show_default=True, help="Paper type, e.g. survey or empirical.")
    @click.option("--from-record", default=None, help="Parent writing-template record id to seed from.")
    @click.pass_context
    def create_command(ctx: click.Context, template_name: str, venue: str | None, paper_type: str, from_record: str | None, **kwargs: Any) -> int:
        def callback(context: EffectiveTopicContext, _request: ResearchRecordRequest | None) -> tuple[dict[str, Any], list[Any]]:
            return _legacy_mutation_disabled("create")

        return _with_template_context(ctx, kwargs, callback)

    @templates_group.command(name="list", help="List writing-template records.")
    @_common_options
    @_topic_selection_options
    @click.option("--venue", default=None, help="Filter by venue.")
    @click.option("--paper-type", default=None, help="Filter by paper type.")
    @click.pass_context
    def list_command(ctx: click.Context, venue: str | None, paper_type: str | None, **kwargs: Any) -> int:
        def callback(context: EffectiveTopicContext, _request: ResearchRecordRequest | None) -> tuple[dict[str, Any], list[Any]]:
            limit_diagnostics: list[Diagnostic] = []
            selected_limit = effective_records_list_limit(context, None, limit_diagnostics)
            indexed_payload, diagnostics = query_index_list(
                context,
                env=os.environ,
                semantic_id=TEMPLATE_SEMANTIC_ID,
                limit=selected_limit,
            )
            records = indexed_payload.get("records", [])
            filtered: list[dict[str, Any]] = []
            if not isinstance(records, list):
                records = []
            for row in records:
                if not isinstance(row, dict):
                    continue
                record = _template_summary_from_index_row(row)
                if record is None:
                    continue
                meta = record["transition_metadata"]
                if venue is not None and meta.get("venue") != venue:
                    continue
                if paper_type is not None and meta.get("paper_type") != paper_type:
                    continue
                filtered.append(record)
            payload = {
                **indexed_payload,
                "operation": "list",
                "count": len(filtered),
                "limit": selected_limit,
                "records": filtered,
            }
            return payload, [*limit_diagnostics, *diagnostics]

        return _with_template_context(ctx, kwargs, callback)

    @templates_group.command(name="show", help="Show a writing template record and file tree.")
    @_common_options
    @_topic_selection_options
    @click.option("--name", "template_name", default=None, help="Template name; defaults to 'main'.")
    @click.pass_context
    def show_command(ctx: click.Context, template_name: str | None, **kwargs: Any) -> int:
        def callback(context: EffectiveTopicContext, _request: ResearchRecordRequest | None) -> tuple[dict[str, Any], list[Any]]:
            name = template_name or DEFAULT_TEMPLATE_NAME
            record = _find_template_record(context, name)
            if record is None:
                return _error_payload("template_not_found", f"No writing template named '{name}'.")
            record_id = record["id"]
            detail, diagnostics = show_record(
                context,
                record_id,
                env=os.environ,
                include_payload=True,
            )
            template_dir = _template_dir(context, name)
            detail["template_dir"] = str(template_dir)
            detail["file_tree"] = _file_tree(template_dir)
            readme = template_dir / "README.md"
            if readme.exists():
                detail["readme"] = readme.read_text(encoding="utf-8")
            return detail, diagnostics

        return _with_template_context(ctx, kwargs, callback)

    @templates_group.command(name="refresh", help="Regenerate template files and create a descendant record.")
    @_common_options
    @_topic_selection_options
    @click.option("--name", "template_name", default=None, help="Template name; defaults to 'main'.")
    @click.option("--preserve-edits", is_flag=True, help="Keep manually edited files when regenerating.")
    @click.pass_context
    def refresh_command(ctx: click.Context, template_name: str | None, preserve_edits: bool, **kwargs: Any) -> int:
        def callback(context: EffectiveTopicContext, _request: ResearchRecordRequest | None) -> tuple[dict[str, Any], list[Any]]:
            return _legacy_mutation_disabled("refresh")

        return _with_template_context(ctx, kwargs, callback)

    @templates_group.command(name="compile", help="Recompile the preview PDF for an existing template.")
    @_common_options
    @_topic_selection_options
    @click.option("--name", "template_name", default=None, help="Template name; defaults to 'main'.")
    @click.pass_context
    def compile_command(ctx: click.Context, template_name: str | None, **kwargs: Any) -> int:
        def callback(context: EffectiveTopicContext, _request: ResearchRecordRequest | None) -> tuple[dict[str, Any], list[Any]]:
            return _legacy_mutation_disabled("compile")

        return _with_template_context(ctx, kwargs, callback)

    @templates_group.command(name="remove", help="Archive a writing-template record.")
    @_common_options
    @_topic_selection_options
    @click.option("--name", "template_name", default=None, help="Template name; defaults to 'main'.")
    @click.option("--delete-files", is_flag=True, help="Also remove the template directory.")
    @click.pass_context
    def remove_command(ctx: click.Context, template_name: str | None, delete_files: bool, **kwargs: Any) -> int:
        def callback(context: EffectiveTopicContext, _request: ResearchRecordRequest | None) -> tuple[dict[str, Any], list[Any]]:
            return _legacy_mutation_disabled("remove")

        return _with_template_context(ctx, kwargs, callback)


def _with_template_context(
    ctx: click.Context,
    values: dict[str, Any],
    callback: TemplateCallback,
) -> int:
    options = _merge_options(
        ctx,
        project=values.get("project"),
        manifest=values.get("manifest"),
        output_format=values.get("output_format"),
        json_output=bool(values.get("json_output", False)),
        research_topic_id=values.get("research_topic_id"),
        topic_workspace_id=values.get("topic_workspace_id"),
        research_inquiry_id=values.get("research_inquiry_id"),
        research_task_id=values.get("research_task_id"),
        run_id=values.get("run_id"),
        agent_team_instance_id=values.get("agent_team_instance_id"),
        agent_instance_id=values.get("agent_instance_id"),
        topic_agent_team_profile_id=values.get("topic_agent_team_profile_id"),
    )
    command = f"ext research templates {ctx.command.name}"
    context, diagnostics = _context_for_options(
        options,
        validation_scope=ProjectValidationScope.RESEARCH_TEMPLATES,
    )
    if context is None or has_errors(diagnostics):
        payload: dict[str, Any] = {
            "ok": False,
            "mutated": False,
            "error": {
                "code": "context_resolution_failed",
                "message": "Research template commands require a selected Isomer Topic Workspace.",
            },
        }
        return _emit_template_failure(command, options, payload, _context_guidance(diagnostics))
    try:
        payload, callback_diagnostics = callback(context, None)
    except ResearchRecordError as exc:
        payload = exc.to_payload()
        payload.setdefault("mutated", False)
        return _emit_template_failure(
            command,
            options,
            payload,
            [*diagnostics, *_diagnostics_from_payload(payload)],
        )
    typed_callback_diagnostics = [
        diagnostic
        for diagnostic in callback_diagnostics
        if isinstance(diagnostic, Diagnostic)
    ]
    all_diagnostics = [*diagnostics, *typed_callback_diagnostics]
    if payload.get("ok") is False or has_errors(typed_callback_diagnostics):
        payload.setdefault("mutated", False)
        payload.setdefault(
            "error",
            {
                "code": "template_operation_failed",
                "message": f"Research template {ctx.command.name} failed.",
            },
        )
        return _emit_template_failure(command, options, payload, all_diagnostics)
    payload["canonical"] = False
    payload["compatibility_surface"] = "legacy-latex-template"
    payload["deprecation"] = {
        "code": "research_templates_noncanonical",
        "message": "ext research templates preserves historical LaTeX inspection and repair only; it does not create canonical Kaoju paper state.",
        "migration": "Use $isomer-kaoju-pipeline create-paper-template for canonical MyST and ext kaoju paper for exchange, derivation, TeX initialization, and PDF builds.",
    }
    click.echo(dumps_raw_json(payload))
    return 0


def _emit_template_failure(
    command: str,
    options: Any,
    payload: dict[str, Any],
    diagnostics: list[Diagnostic],
) -> int:
    error = payload.get("error")
    error_data = error if isinstance(error, dict) else {}
    code = str(error_data.get("code") or "template_operation_failed")
    message = str(error_data.get("message") or "Research template operation failed.")
    text_lines = [f"ERROR | {code} | {message}"]
    if isinstance(payload.get("mutated"), bool):
        text_lines.append(f"Mutated: {str(payload['mutated']).lower()}")
    return emit_output(command, options, payload, diagnostics, text_lines)


def _context_guidance(diagnostics: list[Diagnostic]) -> list[Diagnostic]:
    hint = "Pass --topic <topic-id>, run inside a registered Topic Workspace, or configure Project Manifest defaults."
    return [
        replace(diagnostic, hint=hint)
        if diagnostic.code == "ISO013" and diagnostic.hint is None
        else diagnostic
        for diagnostic in diagnostics
    ]


def _diagnostics_from_payload(payload: dict[str, Any]) -> list[Diagnostic]:
    raw_diagnostics = payload.get("diagnostics")
    if not isinstance(raw_diagnostics, list):
        return []
    diagnostics: list[Diagnostic] = []
    for item in raw_diagnostics:
        if not isinstance(item, dict):
            continue
        severity: Literal["error", "warning"] = "warning" if item.get("severity") == "warning" else "error"
        diagnostics.append(
            Diagnostic(
                code=str(item.get("code") or "query_index_diagnostic"),
                severity=severity,
                concept=str(item.get("concept") or "Research Record Query Index"),
                message=str(item.get("message") or "The research-record query index reported an error."),
                hint=str(item["hint"]) if item.get("hint") is not None else None,
            )
        )
    return diagnostics


def _template_dir(context: EffectiveTopicContext, template_name: str) -> Path:
    return Path(context.topic_workspace_path) / TEMPLATE_RELATIVE_ROOT / template_name


def _template_summary_from_index_row(row: dict[str, Any]) -> dict[str, Any] | None:
    record_id = row.get("record_id")
    if not isinstance(record_id, str) or not record_id:
        return None
    metadata = row.get("metadata")
    metadata = metadata if isinstance(metadata, dict) else {}
    transition_metadata = metadata.get("transition_metadata")
    transition_metadata = transition_metadata if isinstance(transition_metadata, dict) else {}
    lifecycle_refs = metadata.get("lifecycle_refs")
    lifecycle_refs = lifecycle_refs if isinstance(lifecycle_refs, dict) else {}
    template_name = transition_metadata.get("template_name")
    return {
        "id": record_id,
        "record_kind": row.get("record_kind"),
        "research_topic_id": row.get("research_topic_id"),
        "topic_workspace_id": row.get("topic_workspace_id"),
        "status": row.get("status"),
        "created_at": row.get("created_at"),
        "updated_at": row.get("updated_at"),
        "content_path": row.get("content_path"),
        "lifecycle_refs": lifecycle_refs,
        "transition_metadata": transition_metadata,
        "template_name": template_name,
        "venue": transition_metadata.get("venue"),
        "paper_type": transition_metadata.get("paper_type"),
        "preview_status": transition_metadata.get("preview_status"),
        "is_default": template_name == DEFAULT_TEMPLATE_NAME,
    }


def _find_template_record(context: EffectiveTopicContext, template_name: str) -> dict[str, Any] | None:
    payload, _ = query_index_list(
        context,
        env=os.environ,
        semantic_id=TEMPLATE_SEMANTIC_ID,
        status="ready",
        limit=None,
    )
    if payload.get("ok") is False:
        error = payload.get("error")
        error_data = error if isinstance(error, dict) else {}
        raise ResearchRecordError(
            str(error_data.get("message") or "The research-record query index could not select a writing template."),
            code=str(error_data.get("code") or "query_index_unavailable"),
            payload={
                "mutated": False,
                "operation": payload.get("operation", "query.list"),
                "diagnostics": payload.get("diagnostics", []),
            },
        )
    records = payload.get("records", [])
    if not isinstance(records, list):
        return None
    for row in records:
        if not isinstance(row, dict):
            continue
        record = _template_summary_from_index_row(row)
        if record is None:
            continue
        if record.get("status") == "archived":
            continue
        meta = record["transition_metadata"]
        if meta.get("template_name") == template_name:
            return record
    return None


def _file_tree(template_dir: Path) -> list[str]:
    if not template_dir.exists():
        return []
    return sorted(
        str(path.relative_to(template_dir))
        for path in template_dir.rglob("*")
        if path.is_file()
    )


def _error_payload(code: str, message: str) -> tuple[dict[str, Any], list[Any]]:
    return (
        {
            "ok": False,
            "mutated": False,
            "error": {"code": code, "message": message},
        },
        [],
    )


def _legacy_mutation_disabled(operation: str) -> tuple[dict[str, Any], list[Any]]:
    guidance = "Use 'isomer-cli ext kaoju paper template' low-level named CRUD and the Kaoju agent for arbitrary template construction or reconciliation."
    return (
        {
            "ok": False,
            "mutated": False,
            "operation": f"legacy-template.{operation}",
            "error": {
                "code": "legacy_template_mutation_disabled",
                "message": f"Legacy 'ext research templates {operation}' mutation is disabled. {guidance}",
            },
            "diagnostics": [],
            "recovery_actions": [guidance, "Inspect legacy KAOJU:WRITING-TEMPLATE records through generic record reads or run named-template migration inspection."],
            "next_actions": [guidance],
        },
        [],
    )
