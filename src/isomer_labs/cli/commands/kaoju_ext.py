"""Kaoju paper and wiki extension commands."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Callable

import click

from isomer_labs.cli.handlers.shared import _context_for_options
from isomer_labs.cli.options import common_options, merge_options, topic_selection_options
from isomer_labs.cli.output import emit_output
from isomer_labs.kaoju.artifacts import KaojuServiceError
from isomer_labs.kaoju.paper import KaojuPaperService, REQUIRED_PAPER_SECTIONS
from isomer_labs.kaoju.wiki import KaojuWikiService
from isomer_labs.models import EffectiveTopicContext


ServiceCallback = Callable[[EffectiveTopicContext], dict[str, object]]


def register_kaoju_ext_commands(app: click.Group) -> None:
    """Register ``ext kaoju paper`` and ``ext kaoju wiki``."""

    ext_command = app.commands.get("ext")
    if not isinstance(ext_command, click.Group):
        ext_command = click.Group(name="ext", help="Use extension command surfaces.")
        app.add_command(ext_command)

    @ext_command.group(name="kaoju", help="Use checked Kaoju survey-process services.")
    def kaoju_group() -> None:
        pass

    @kaoju_group.group(name="paper", help="Validate and derive the canonical MyST-first paper graph.")
    def paper_group() -> None:
        pass

    @paper_group.command(name="validate", help="Validate MyST syntax, sections, placeholders, citations, displays, and source refs.")
    @common_options
    @topic_selection_options
    @click.option("--required-section", "required_sections", multiple=True, help="Required heading. Repeat as needed.")
    @click.option("--allowed-placeholder", "allowed_placeholders", multiple=True, help="Allowed untyped placeholder. Repeat as needed.")
    @click.option("--source-ref", "source_refs", multiple=True, help="Allowed source or display Artifact ref.")
    @click.argument("source", type=click.Path(path_type=Path, exists=True, dir_okay=False))
    @click.pass_context
    def paper_validate(ctx: click.Context, source: Path, **values: Any) -> int:
        return _with_kaoju_service(
            ctx,
            values,
            lambda context: KaojuPaperService(context, env=os.environ, cwd=Path.cwd()).validate(
                source,
                required_sections=list(values["required_sections"]) or REQUIRED_PAPER_SECTIONS,
                allowed_placeholders=list(values["allowed_placeholders"]) if values["allowed_placeholders"] else None,
                source_refs=list(values["source_refs"]),
            ),
        )

    @paper_group.command(name="export-template", help="Export a versioned actor-editable MyST template and register its manifest.")
    @common_options
    @topic_selection_options
    @click.option("--source-ref", required=True, help="Current paper structure or MyST template Artifact ref.")
    @click.option("--paper-line", required=True, help="Exact paper-line scope key.")
    @click.option("--draft-ref", required=True, help="Tied canonical MyST draft ref.")
    @click.option("--citation-map-ref", required=True, help="Tied citation-map ref.")
    @click.option("--source-digest-ref", "source_digest_refs", multiple=True, help="Accepted Source Digest ref.")
    @click.option("--display-ref", "display_refs", multiple=True, help="Accepted file-backed paper display Artifact ref.")
    @click.option("--target", type=click.Path(path_type=Path), default=None, help="Actor-authorized export directory.")
    @click.option("--target-policy", type=click.Choice(["create", "update", "overwrite"]), default="create", show_default=True)
    @click.pass_context
    def paper_export_template(ctx: click.Context, **values: Any) -> int:
        return _with_kaoju_service(ctx, values, lambda context: KaojuPaperService(context, env=os.environ, cwd=Path.cwd()).export_template(source_ref=str(values["source_ref"]), paper_line=str(values["paper_line"]), draft_ref=str(values["draft_ref"]), citation_map_ref=str(values["citation_map_ref"]), source_digest_refs=list(values["source_digest_refs"]), target=values.get("target"), target_policy=str(values["target_policy"]), display_refs=list(values["display_refs"])))

    @paper_group.command(name="apply-template", help="Validate and apply an externally edited MyST template without stale-base mutation.")
    @common_options
    @topic_selection_options
    @click.option("--confirm-orphans", is_flag=True, help="Confirm removal of reported optional grounded sections.")
    @click.argument("export_directory", type=click.Path(path_type=Path, exists=True, file_okay=False))
    @click.pass_context
    def paper_apply_template(ctx: click.Context, export_directory: Path, **values: Any) -> int:
        return _with_kaoju_service(ctx, values, lambda context: KaojuPaperService(context, env=os.environ, cwd=Path.cwd()).apply_template(export_directory, confirm_orphans=bool(values["confirm_orphans"])))

    @paper_group.command(name="derive-markdown", help="Create a deterministic non-canonical Markdown review view from MyST.")
    @common_options
    @topic_selection_options
    @click.option("--source-ref", required=True, help="Canonical MyST draft ref.")
    @click.option("--paper-line", required=True, help="Exact paper-line scope key.")
    @click.option("--output", type=click.Path(path_type=Path), default=None, help="Optional actor review-file target.")
    @click.pass_context
    def paper_derive_markdown(ctx: click.Context, **values: Any) -> int:
        return _with_kaoju_service(ctx, values, lambda context: KaojuPaperService(context, env=os.environ, cwd=Path.cwd()).derive_markdown(source_ref=str(values["source_ref"]), paper_line=str(values["paper_line"]), output=values.get("output")))

    @paper_group.command(name="init-tex", help="Initialize derived TeX template and draft manifests from canonical MyST.")
    @common_options
    @topic_selection_options
    @click.option("--draft-ref", required=True, help="Canonical MyST draft ref.")
    @click.option("--template-myst-ref", required=True, help="Canonical MyST template or structure ref.")
    @click.option("--paper-line", required=True, help="Exact paper-line scope key.")
    @click.option("--venue", default="generic", show_default=True)
    @click.option("--document-class", default="article", show_default=True)
    @click.option("--toolchain-policy", default="tectonic-first", show_default=True)
    @click.option("--citation-ref", "citation_refs", multiple=True, help="Citation input Artifact ref.")
    @click.pass_context
    def paper_init_tex(ctx: click.Context, **values: Any) -> int:
        return _with_kaoju_service(ctx, values, lambda context: KaojuPaperService(context, env=os.environ, cwd=Path.cwd()).init_tex(draft_ref=str(values["draft_ref"]), template_myst_ref=str(values["template_myst_ref"]), paper_line=str(values["paper_line"]), venue=str(values["venue"]), document_class=str(values["document_class"]), toolchain_policy=str(values["toolchain_policy"]), citation_refs=list(values["citation_refs"])))

    @paper_group.command(name="build-pdf", help="Build an inspected TeX draft through the document_build extension point.")
    @common_options
    @topic_selection_options
    @click.option("--draft-tex-ref", required=True)
    @click.option("--template-tex-ref", required=True)
    @click.option("--paper-line", required=True)
    @click.option("--audit-ref", required=True)
    @click.option("--inspected", is_flag=True, help="Record that an agent directly inspected the derived TeX tree.")
    @click.option("--pdf-inspected", is_flag=True, help="Record direct textual and visual inspection of the produced PDF.")
    @click.option("--publication-approved", is_flag=True, help="Record the human publication Gate as approved.")
    @click.option("--toolchain", type=click.Choice(["tectonic", "latexmk", "pdflatex"]), default=None)
    @click.option("--timeout", "timeout_seconds", type=float, default=120.0, show_default=True)
    @click.pass_context
    def paper_build_pdf(ctx: click.Context, **values: Any) -> int:
        return _with_kaoju_service(ctx, values, lambda context: KaojuPaperService(context, env=os.environ, cwd=Path.cwd()).build_pdf(draft_tex_ref=str(values["draft_tex_ref"]), template_tex_ref=str(values["template_tex_ref"]), paper_line=str(values["paper_line"]), audit_ref=str(values["audit_ref"]), inspected=bool(values["inspected"]), pdf_inspected=bool(values["pdf_inspected"]), publication_approved=bool(values["publication_approved"]), timeout_seconds=float(values["timeout_seconds"]), toolchain=values.get("toolchain")))

    @kaoju_group.group(name="wiki", help="Export accepted survey records and manage the package-owned local viewer.")
    def wiki_group() -> None:
        pass

    @wiki_group.command(name="export", help="Export selected accepted state-DB records as Markdown plus canonical JSON.")
    @common_options
    @topic_selection_options
    @click.option("--artifact-ref", "artifact_refs", multiple=True, help="Explicit accepted Artifact ref.")
    @click.option("--direction-scope", default=None, help="Direction scope selector.")
    @click.option("--paper-scope", default=None, help="Paper-line scope selector.")
    @click.option("--target", type=click.Path(path_type=Path), default=None, help="Actor-authorized wiki target.")
    @click.option("--target-policy", type=click.Choice(["create", "update"]), default="update", show_default=True)
    @click.pass_context
    def wiki_export(ctx: click.Context, **values: Any) -> int:
        return _with_kaoju_service(ctx, values, lambda context: KaojuWikiService(context, env=os.environ, cwd=Path.cwd()).export(artifact_refs=list(values["artifact_refs"]), direction_scope=values.get("direction_scope"), paper_scope=values.get("paper_scope"), target=values.get("target"), target_policy=str(values["target_policy"])))

    @wiki_group.command(name="deploy", help="Deploy or refresh the independently implemented packaged viewer.")
    @common_options
    @topic_selection_options
    @click.option("--target", type=click.Path(path_type=Path), default=None, help="Actor-authorized viewer target.")
    @click.option("--target-policy", type=click.Choice(["create", "update"]), default="update", show_default=True)
    @click.argument("wiki_target", type=click.Path(path_type=Path, exists=True, file_okay=False))
    @click.pass_context
    def wiki_deploy(ctx: click.Context, wiki_target: Path, **values: Any) -> int:
        return _with_kaoju_service(ctx, values, lambda context: KaojuWikiService(context, env=os.environ, cwd=Path.cwd()).deploy(wiki_target=wiki_target, target=values.get("target"), target_policy=str(values["target_policy"])))

    @wiki_group.command(name="start", help="Launch a deployed viewer through a recorded Execution Adapter Command Request.")
    @common_options
    @topic_selection_options
    @click.option("--host", default="127.0.0.1", show_default=True)
    @click.option("--port", type=int, default=8000, show_default=True)
    @click.option("--network-exposure-approved", is_flag=True, help="Record approval for non-loopback binding.")
    @click.option("--timeout", "timeout_seconds", type=float, default=10.0, show_default=True)
    @click.option("--dry-run", is_flag=True, help="Validate target, Gate, and port without launching.")
    @click.argument("viewer_target", type=click.Path(path_type=Path, exists=True, file_okay=False))
    @click.pass_context
    def wiki_start(ctx: click.Context, viewer_target: Path, **values: Any) -> int:
        return _with_kaoju_service(ctx, values, lambda context: KaojuWikiService(context, env=os.environ, cwd=Path.cwd()).start(viewer_target=viewer_target, host=str(values["host"]), port=int(values["port"]), network_exposure_approved=bool(values["network_exposure_approved"]), timeout_seconds=float(values["timeout_seconds"]), dry_run=bool(values["dry_run"])))


def _with_kaoju_service(ctx: click.Context, values: dict[str, Any], callback: ServiceCallback) -> int:
    options = merge_options(ctx, project=values.get("project"), manifest=values.get("manifest"), research_topic_id=values.get("research_topic_id"), topic_workspace_id=values.get("topic_workspace_id"), research_inquiry_id=values.get("research_inquiry_id"), research_task_id=values.get("research_task_id"), run_id=values.get("run_id"), agent_team_instance_id=values.get("agent_team_instance_id"), agent_instance_id=values.get("agent_instance_id"), topic_agent_team_profile_id=values.get("topic_agent_team_profile_id"))
    context, diagnostics = _context_for_options(options)
    if context is None:
        payload: dict[str, object] = {"ok": False, "mutated": False, "error": {"code": "context_resolution_failed", "message": "Select one Topic Workspace."}}
    else:
        try:
            payload = callback(context)
        except KaojuServiceError as exc:
            payload = exc.payload()
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            payload = {"ok": False, "mutated": False, "error": {"code": "invalid_request", "message": str(exc)}, "recovery_actions": []}
    operation = str(payload.get("operation") or "error")
    error = payload.get("error")
    if payload.get("ok") is False and isinstance(error, dict):
        lines = [str(error.get("message") or "Kaoju service command failed.")]
    else:
        refs = payload.get("affected_refs")
        suffix = f": {', '.join(str(value) for value in refs)}" if isinstance(refs, list) and refs else ""
        lines = [f"{operation} succeeded{suffix}"]
    return emit_output(f"ext.kaoju.{operation}", options, payload, diagnostics, lines)
