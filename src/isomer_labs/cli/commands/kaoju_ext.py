"""Kaoju shared-resource, paper, and wiki extension commands."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Callable, Literal

import click

from isomer_labs.core.artifact_identity import ArtifactIdentityError
from isomer_labs.core.diagnostics import Diagnostic
from isomer_labs.cli.handlers.shared import _context_for_options
from isomer_labs.cli.options import common_options, merge_options, topic_selection_options
from isomer_labs.cli.output import emit_output
from isomer_labs.kaoju.artifacts import KaojuServiceError
from isomer_labs.kaoju.contracts import (
    describe_binding,
    list_binding_summaries,
    load_contract,
    resource_versions,
)
from isomer_labs.kaoju.paper import KaojuPaperService, REQUIRED_PAPER_SECTIONS
from isomer_labs.kaoju.templates import DEFAULT_TEMPLATE_NAME, KaojuTemplateService
from isomer_labs.kaoju.wiki import KaojuWikiService
from isomer_labs.models import EffectiveTopicContext


ServiceCallback = Callable[[EffectiveTopicContext], dict[str, object]]


def register_kaoju_ext_commands(app: click.Group) -> None:
    """Register context-free resources and topic-scoped Kaoju services."""

    ext_command = app.commands.get("ext")
    if not isinstance(ext_command, click.Group):
        ext_command = click.Group(name="ext", help="Use extension command surfaces.")
        app.add_command(ext_command)

    @ext_command.group(name="kaoju", help="Use checked Kaoju survey-process services.")
    def kaoju_group() -> None:
        pass

    @kaoju_group.group(name="process", help="Inspect the extension-owned Kaoju survey process.")
    def process_group() -> None:
        pass

    @process_group.command(name="show", help="Show the versioned Kaoju process and logical binding queries.")
    @click.pass_context
    def process_show(ctx: click.Context) -> int:
        try:
            contract = load_contract()
            payload: dict[str, Any] = {
                "ok": True,
                "mutated": False,
                "operation": "process.show",
                "versions": resource_versions(),
                "process": contract.raw,
            }
            lines = [
                f"Kaoju process: {contract.schema_version}",
                f"Entry skill: {contract.raw['entry_skill']}",
                f"Binding list: {contract.binding_queries['list']}",
                f"Binding describe: {contract.binding_queries['describe']}",
                f"Survey intents: {', '.join(contract.survey_intents)}",
                f"Compatibility procedures: {', '.join(contract.compatibility_procedures)}",
            ]
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            payload = {
                "ok": False,
                "mutated": False,
                "operation": "process.show",
                "error": {"code": "kaoju_resource_load_failed", "message": str(exc)},
            }
            lines = [str(exc)]
        return emit_output("ext.kaoju.process.show", merge_options(ctx), payload, [], lines)

    @kaoju_group.group(name="bindings", help="Query canonical Kaoju artifact semantics and storage bindings.")
    def bindings_group() -> None:
        pass

    @bindings_group.command(name="list", help="List canonical Kaoju artifact identifiers in sorted order.")
    @click.pass_context
    def bindings_list(ctx: click.Context) -> int:
        try:
            summaries = list_binding_summaries()
            payload: dict[str, Any] = {
                "ok": True,
                "mutated": False,
                "operation": "bindings.list",
                "versions": resource_versions(),
                "count": len(summaries),
                "bindings": summaries,
            }
            lines = [
                f"{item['semantic_id']} | {item['artifact_type']} | {item['record_kind']} | {item['producer']} | {item['meaning']}"
                for item in summaries
            ]
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            payload = {
                "ok": False,
                "mutated": False,
                "operation": "bindings.list",
                "error": {"code": "kaoju_resource_load_failed", "message": str(exc)},
            }
            lines = [str(exc)]
        return emit_output("ext.kaoju.bindings.list", merge_options(ctx), payload, [], lines)

    @bindings_group.command(name="describe", help="Describe one exact uppercase KAOJU:WHAT artifact identifier.")
    @click.argument("semantic_id")
    @click.pass_context
    def bindings_describe(ctx: click.Context, semantic_id: str) -> int:
        try:
            binding = describe_binding(semantic_id)
            payload: dict[str, Any] = {
                "ok": True,
                "mutated": False,
                "operation": "bindings.describe",
                "versions": resource_versions(),
                "binding": binding,
            }
            lines = [
                f"Semantic id: {binding['semantic_id']}",
                f"Meaning: {binding['meaning']}",
                f"Minimum content: {'; '.join(binding['minimum_content'])}",
                f"Producer: {binding['producer']}",
                f"Consumers: {', '.join(binding['consumers'])}",
                f"Record kind: {binding['record_kind']}",
                f"Profile: {binding['profile_ref'] or 'none'}",
                f"Revision: {binding['revision_mode']}",
                f"Update intent: {binding['update_intent']}",
            ]
        except ArtifactIdentityError as exc:
            payload = {
                "ok": False,
                "mutated": False,
                "operation": "bindings.describe",
                "error": {"code": exc.code, "message": str(exc)},
                "artifact_identity": semantic_id,
            }
            if exc.expected_namespace is not None:
                payload["expected_namespace"] = exc.expected_namespace
            lines = [str(exc)]
        except KeyError:
            message = f"Unknown Kaoju semantic id: {semantic_id}"
            payload = {
                "ok": False,
                "mutated": False,
                "operation": "bindings.describe",
                "error": {"code": "unknown_semantic_id", "message": message},
                "artifact_identity": semantic_id,
            }
            lines = [message]
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            payload = {
                "ok": False,
                "mutated": False,
                "operation": "bindings.describe",
                "error": {"code": "kaoju_resource_load_failed", "message": str(exc)},
            }
            lines = [str(exc)]
        return emit_output("ext.kaoju.bindings.describe", merge_options(ctx), payload, [], lines)

    @kaoju_group.group(name="paper", help="Validate and derive the canonical MyST-first paper graph.")
    def paper_group() -> None:
        pass

    @paper_group.group(name="template", help="Manage mutable named MyST-oriented paper template trees.")
    def paper_template_group() -> None:
        pass

    @paper_template_group.command(name="list", help="List the flat namespace of mutable named templates.")
    @common_options
    @topic_selection_options
    @click.pass_context
    def paper_template_list(ctx: click.Context, **values: Any) -> int:
        return _with_kaoju_service(ctx, values, lambda context: KaojuTemplateService(context, env=os.environ, cwd=Path.cwd()).list())

    @paper_template_group.command(name="show", help="Show one exact named template and its current state token.")
    @common_options
    @topic_selection_options
    @click.option("--name", required=True, help="Exact path-safe template name.")
    @click.pass_context
    def paper_template_show(ctx: click.Context, **values: Any) -> int:
        return _with_kaoju_service(ctx, values, lambda context: KaojuTemplateService(context, env=os.environ, cwd=Path.cwd()).show(str(values["name"])))

    @paper_template_group.command(name="create", help="Create a named template from a prepared tree or another named template.")
    @common_options
    @topic_selection_options
    @click.option("--name", required=True, help="New path-safe template name.")
    @click.option("--from", "from_path", type=click.Path(path_type=Path, exists=True, file_okay=False), default=None, help="Prepared template directory.")
    @click.option("--from-template", default=None, help="Existing named template to copy exactly.")
    @click.option("--metadata-file", type=click.Path(path_type=Path, exists=True, dir_okay=False), default=None, help="Bounded authored metadata JSON.")
    @click.option("--actor", default="agent", show_default=True, help="Actor or agent ref responsible for the mutation.")
    @click.option("--source-ref", "source_refs", multiple=True, help="Stable source ref for audit evidence.")
    @click.option("--change-summary", default=None, help="Agent-authored assessment or change summary.")
    @click.pass_context
    def paper_template_create(ctx: click.Context, **values: Any) -> int:
        metadata = _json_object_file(values.get("metadata_file"), label="Template metadata")
        return _with_kaoju_service(ctx, values, lambda context: KaojuTemplateService(context, env=os.environ, cwd=Path.cwd()).create(str(values["name"]), source=values.get("from_path"), from_template=values.get("from_template"), authored_metadata=metadata, actor=str(values["actor"]), source_refs=list(values["source_refs"]), change_summary=values.get("change_summary")))

    @paper_template_group.command(name="update", help="Atomically replace a named template from a prepared tree or known named template.")
    @common_options
    @topic_selection_options
    @click.option("--name", required=True, help="Target template name.")
    @click.option("--from", "from_path", type=click.Path(path_type=Path, exists=True, file_okay=False), default=None, help="Agent-prepared replacement directory.")
    @click.option("--from-template", default=None, help="Known named template used for exact replacement.")
    @click.option("--expected-state", required=True, help="Current opaque target state token.")
    @click.option("--actor", default="agent", show_default=True, help="Actor or agent ref responsible for the mutation.")
    @click.option("--source-ref", "source_refs", multiple=True, help="Stable source ref for audit evidence.")
    @click.option("--change-summary", default=None, help="Agent-authored assessment or change summary.")
    @click.pass_context
    def paper_template_update(ctx: click.Context, **values: Any) -> int:
        return _with_kaoju_service(ctx, values, lambda context: KaojuTemplateService(context, env=os.environ, cwd=Path.cwd()).update(str(values["name"]), source=values.get("from_path"), from_template=values.get("from_template"), expected_state=str(values["expected_state"]), actor=str(values["actor"]), source_refs=list(values["source_refs"]), change_summary=values.get("change_summary")))

    @paper_template_group.group(name="file", help="Apply low-level safe file edits to a named template.")
    def paper_template_file_group() -> None:
        pass

    @paper_template_file_group.command(name="put", help="Put one regular file at a safe relative path.")
    @common_options
    @topic_selection_options
    @click.option("--name", required=True)
    @click.option("--path", "relative_path", required=True, help="Safe path relative to the template root.")
    @click.option("--from", "source", type=click.Path(path_type=Path, exists=True, dir_okay=False), required=True)
    @click.option("--expected-state", required=True)
    @click.option("--actor", default="agent", show_default=True)
    @click.option("--source-ref", "source_refs", multiple=True)
    @click.option("--change-summary", default=None)
    @click.pass_context
    def paper_template_file_put(ctx: click.Context, **values: Any) -> int:
        return _with_kaoju_service(ctx, values, lambda context: KaojuTemplateService(context, env=os.environ, cwd=Path.cwd()).file_put(str(values["name"]), str(values["relative_path"]), values["source"], expected_state=str(values["expected_state"]), actor=str(values["actor"]), source_refs=list(values["source_refs"]), change_summary=values.get("change_summary")))

    @paper_template_file_group.command(name="remove", help="Remove one file at a safe relative path.")
    @common_options
    @topic_selection_options
    @click.option("--name", required=True)
    @click.option("--path", "relative_path", required=True, help="Safe path relative to the template root.")
    @click.option("--expected-state", required=True)
    @click.option("--actor", default="agent", show_default=True)
    @click.option("--source-ref", "source_refs", multiple=True)
    @click.option("--change-summary", default=None)
    @click.pass_context
    def paper_template_file_remove(ctx: click.Context, **values: Any) -> int:
        return _with_kaoju_service(ctx, values, lambda context: KaojuTemplateService(context, env=os.environ, cwd=Path.cwd()).file_remove(str(values["name"]), str(values["relative_path"]), expected_state=str(values["expected_state"]), actor=str(values["actor"]), source_refs=list(values["source_refs"]), change_summary=values.get("change_summary")))

    @paper_template_group.group(name="metadata", help="Edit bounded agent-authored template metadata.")
    def paper_template_metadata_group() -> None:
        pass

    @paper_template_metadata_group.command(name="patch", help="Patch entrypoint, use guidance, or extension metadata.")
    @common_options
    @topic_selection_options
    @click.option("--name", required=True)
    @click.option("--patch-file", type=click.Path(path_type=Path, exists=True, dir_okay=False), required=True)
    @click.option("--expected-state", required=True)
    @click.option("--actor", default="agent", show_default=True)
    @click.option("--source-ref", "source_refs", multiple=True)
    @click.option("--change-summary", default=None)
    @click.pass_context
    def paper_template_metadata_patch(ctx: click.Context, **values: Any) -> int:
        patch = _json_object_file(values.get("patch_file"), label="Template metadata patch")
        return _with_kaoju_service(ctx, values, lambda context: KaojuTemplateService(context, env=os.environ, cwd=Path.cwd()).metadata_patch(str(values["name"]), patch, expected_state=str(values["expected_state"]), actor=str(values["actor"]), source_refs=list(values["source_refs"]), change_summary=values.get("change_summary")))

    @paper_template_group.command(name="archive", help="Archive an unreferenced named template with optimistic concurrency.")
    @common_options
    @topic_selection_options
    @click.option("--name", required=True)
    @click.option("--expected-state", required=True)
    @click.option("--actor", default="agent", show_default=True)
    @click.option("--reason", default=None)
    @click.pass_context
    def paper_template_archive(ctx: click.Context, **values: Any) -> int:
        return _with_kaoju_service(ctx, values, lambda context: KaojuTemplateService(context, env=os.environ, cwd=Path.cwd()).archive(str(values["name"]), expected_state=str(values["expected_state"]), actor=str(values["actor"]), reason=values.get("reason")))

    @paper_template_group.command(name="delete", help="Delete an unreferenced named template with optimistic concurrency.")
    @common_options
    @topic_selection_options
    @click.option("--name", required=True)
    @click.option("--expected-state", required=True)
    @click.option("--actor", default="agent", show_default=True)
    @click.pass_context
    def paper_template_delete(ctx: click.Context, **values: Any) -> int:
        return _with_kaoju_service(ctx, values, lambda context: KaojuTemplateService(context, env=os.environ, cwd=Path.cwd()).delete(str(values["name"]), expected_state=str(values["expected_state"]), actor=str(values["actor"])))

    @paper_template_group.command(name="exports", help="List registered working copies and recompute their status.")
    @common_options
    @topic_selection_options
    @click.pass_context
    def paper_template_exports(ctx: click.Context, **values: Any) -> int:
        return _with_kaoju_service(ctx, values, lambda context: KaojuTemplateService(context, env=os.environ, cwd=Path.cwd()).exports())

    @paper_template_group.command(name="export", help="Export or observe one stable non-canonical working directory.")
    @common_options
    @topic_selection_options
    @click.option("--name", default=DEFAULT_TEMPLATE_NAME, show_default=True)
    @click.option("--target", type=click.Path(path_type=Path), default=None)
    @click.option("--observe", is_flag=True, help="Register an agent-prepared working tree without copying canonical content.")
    @click.option("--actor", default="agent", show_default=True)
    @click.pass_context
    def paper_template_export(ctx: click.Context, **values: Any) -> int:
        if values["observe"] and values.get("target") is None:
            raise click.UsageError("--observe requires --target")
        return _with_kaoju_service(ctx, values, lambda context: KaojuTemplateService(context, env=os.environ, cwd=Path.cwd()).observe_export(str(values["name"]), values["target"], actor=str(values["actor"])) if values["observe"] else KaojuTemplateService(context, env=os.environ, cwd=Path.cwd()).export(str(values["name"]), target=values.get("target"), actor=str(values["actor"])))

    @paper_template_group.command(name="migrate", help="Inspect or apply migration from legacy paper-template records.")
    @common_options
    @topic_selection_options
    @click.option("--apply", is_flag=True, help="Create a mutable named template from the selected legacy record.")
    @click.option("--record", "record_id", default=None, help="Explicit active legacy record ref.")
    @click.option("--name", default=None, help="Explicit target template name.")
    @click.option("--actor", default="agent", show_default=True)
    @click.pass_context
    def paper_template_migrate(ctx: click.Context, **values: Any) -> int:
        return _with_kaoju_service(ctx, values, lambda context: KaojuTemplateService(context, env=os.environ, cwd=Path.cwd()).migrate(record_id=values.get("record_id"), name=values.get("name"), actor=str(values["actor"])) if values["apply"] else KaojuTemplateService(context, env=os.environ, cwd=Path.cwd()).inspect_migration())

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

    @paper_group.command(name="export-template", help="Retired: use 'paper template export'.")
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
        return _with_kaoju_service(ctx, values, lambda _context: _retired_template_operation("export-template", "Use 'isomer-cli ext kaoju paper template export [--name NAME]' for stable named working copies."))

    @paper_group.command(name="apply-template", help="Retired: use the Kaoju agent and 'paper template update'.")
    @common_options
    @topic_selection_options
    @click.option("--confirm-orphans", is_flag=True, help="Confirm removal of reported optional grounded sections.")
    @click.argument("export_directory", type=click.Path(path_type=Path, exists=True, file_okay=False))
    @click.pass_context
    def paper_apply_template(ctx: click.Context, export_directory: Path, **values: Any) -> int:
        return _with_kaoju_service(ctx, values, lambda _context: _retired_template_operation("apply-template", "Use the Kaoju agent to inspect and prepare the arbitrary tree, then run 'isomer-cli ext kaoju paper template update --name NAME --from PATH --expected-state TOKEN'."))

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
    diagnostics = [*diagnostics, *_service_diagnostics(payload.pop("diagnostics", []))]
    operation = str(payload.get("operation") or "error")
    error = payload.get("error")
    if payload.get("ok") is False and isinstance(error, dict):
        lines = [str(error.get("message") or "Kaoju service command failed.")]
    else:
        refs = payload.get("affected_refs")
        suffix = f": {', '.join(str(value) for value in refs)}" if isinstance(refs, list) and refs else ""
        lines = [f"{operation} succeeded{suffix}"]
    return emit_output(f"ext.kaoju.{operation}", options, payload, diagnostics, lines)


def _service_diagnostics(value: object) -> list[Diagnostic]:
    if not isinstance(value, list):
        return []
    diagnostics: list[Diagnostic] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        severity: Literal["error", "warning"] = "error" if item.get("severity") == "error" else "warning"
        raw_path = item.get("path")
        raw_line = item.get("line")
        diagnostics.append(
            Diagnostic(
                code=str(item.get("code") or "kaoju_service_diagnostic"),
                severity=severity,
                concept=str(item.get("concept") or "Kaoju service"),
                message=str(item.get("message") or "The Kaoju service reported a diagnostic."),
                path=Path(str(raw_path)) if raw_path is not None else None,
                field=str(item["field"]) if item.get("field") is not None else None,
                line=raw_line if isinstance(raw_line, int) else None,
                hint=str(item["hint"]) if item.get("hint") is not None else None,
            )
        )
    return diagnostics


def _json_object_file(path: object, *, label: str) -> dict[str, object]:
    if path is None:
        return {}
    if not isinstance(path, Path):
        raise click.BadParameter(f"{label} path is invalid.")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise click.BadParameter(f"{label} must contain readable JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise click.BadParameter(f"{label} must contain a JSON object.")
    return value


def _retired_template_operation(operation: str, guidance: str) -> dict[str, object]:
    return {
        "ok": False,
        "mutated": False,
        "operation": f"paper.{operation}",
        "error": {
            "code": "paper_template_command_retired",
            "message": f"The flat paper {operation} workflow is retired. {guidance}",
        },
        "diagnostics": [],
        "recovery_actions": [guidance],
        "next_actions": [guidance],
    }
