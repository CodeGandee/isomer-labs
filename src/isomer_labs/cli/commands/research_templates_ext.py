"""Click registration for Isomer research paper-writing template commands."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import textwrap
from pathlib import Path
from typing import Any, Callable

import click

from isomer_labs.cli.options import (
    common_options as _common_options,
    topic_selection_options as _topic_selection_options,
)
from isomer_labs.project.context import EffectiveTopicContext
from isomer_labs.records.store import (
    ResearchRecordRequest,
    archive_record,
    create_record,
    list_records,
    revise_record,
    show_record,
)


DEFAULT_TEMPLATE_NAME = "main"
TEMPLATE_RELATIVE_ROOT = Path("intent") / "derived" / "writing-template"
TEMPLATE_SEMANTIC_ID = "kaoju:writing-template"
TEMPLATE_PROFILE_REF = "isomer:research/record-format/profile/kaoju/control/writing-template/v1"

WithContext = Callable[..., int]
JsonErrorPayload = Callable[[Exception], dict[str, object]]


def register_research_templates_commands(
    research_group: click.Group,
    *,
    with_context: WithContext,
    json_error_payload: JsonErrorPayload,
) -> None:
    @research_group.group(name="templates", help="Manage paper-writing LaTeX templates.")
    def templates_group() -> None:
        pass

    @templates_group.command(name="create", help="Generate a LaTeX writing template and compile a preview PDF.")
    @_common_options
    @_topic_selection_options
    @click.option("--name", "template_name", default=DEFAULT_TEMPLATE_NAME, show_default=True, help="Template name.")
    @click.option("--venue", default=None, help="Target venue or conference.")
    @click.option("--paper-type", default="survey", show_default=True, help="Paper type, e.g. survey or empirical.")
    @click.option("--from-record", default=None, help="Parent writing-template record id to seed from.")
    @click.pass_context
    def create_command(ctx: click.Context, template_name: str, venue: str | None, paper_type: str, from_record: str | None, **kwargs: Any) -> int:
        def callback(context: EffectiveTopicContext, _request: ResearchRecordRequest | None) -> tuple[dict[str, Any], list[Any]]:
            template_dir = _template_dir(context, template_name)
            if template_dir.exists():
                return _error_payload("template_already_exists", f"Template directory already exists: {template_dir}")
            _generate_template_files(template_dir, template_name, venue, paper_type)
            build_result = _compile_preview(template_dir)
            payload_path = _write_payload_file(template_dir, template_name, venue, paper_type, build_result)
            request = ResearchRecordRequest(
                record_kind="artifact",
                status="ready" if build_result["ok"] else "blocked",
                semantic_id=TEMPLATE_SEMANTIC_ID,
                format_profile_ref=TEMPLATE_PROFILE_REF,
                skill="isomer-kaoju-pipeline",
                producer="isomer-kaoju-pipeline",
                consumer="isomer-kaoju-pipeline, isomer-kaoju-write",
                payload_file=payload_path,
                metadata={
                    "actor_metadata": "isomer-kaoju-pipeline",
                    "template_name": template_name,
                    "venue": venue,
                    "paper_type": paper_type,
                },
                parents=_parents_json(from_record) if from_record else [],
                lineage_kind="derived_from",
            )
            payload, diagnostics = create_record(context, request, env=os.environ, cwd=Path.cwd())
            payload["template_dir"] = str(template_dir)
            payload["preview_build"] = build_result
            return payload, diagnostics

        return with_context(ctx, kwargs, callback, build_request=False)

    @templates_group.command(name="list", help="List writing-template records.")
    @_common_options
    @_topic_selection_options
    @click.option("--venue", default=None, help="Filter by venue.")
    @click.option("--paper-type", default=None, help="Filter by paper type.")
    @click.pass_context
    def list_command(ctx: click.Context, venue: str | None, paper_type: str | None, **kwargs: Any) -> int:
        def callback(context: EffectiveTopicContext, _request: ResearchRecordRequest | None) -> tuple[dict[str, Any], list[Any]]:
            payload, diagnostics = list_records(
                context,
                env=os.environ,
                semantic_id=TEMPLATE_SEMANTIC_ID,
                limit=None,
            )
            records = payload.get("records", [])
            filtered: list[dict[str, Any]] = []
            for record in records:
                meta = record.get("transition_metadata", {}) or {}
                is_default = meta.get("template_name") == DEFAULT_TEMPLATE_NAME
                record["is_default"] = is_default
                if venue is not None and meta.get("venue") != venue:
                    continue
                if paper_type is not None and meta.get("paper_type") != paper_type:
                    continue
                filtered.append(record)
            payload["records"] = filtered
            return payload, diagnostics

        return with_context(ctx, kwargs, callback, build_request=False)

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

        return with_context(ctx, kwargs, callback, build_request=False)

    @templates_group.command(name="refresh", help="Regenerate template files and create a descendant record.")
    @_common_options
    @_topic_selection_options
    @click.option("--name", "template_name", default=None, help="Template name; defaults to 'main'.")
    @click.option("--preserve-edits", is_flag=True, help="Keep manually edited files when regenerating.")
    @click.pass_context
    def refresh_command(ctx: click.Context, template_name: str | None, preserve_edits: bool, **kwargs: Any) -> int:
        def callback(context: EffectiveTopicContext, _request: ResearchRecordRequest | None) -> tuple[dict[str, Any], list[Any]]:
            name = template_name or DEFAULT_TEMPLATE_NAME
            parent_record = _find_template_record(context, name)
            if parent_record is None:
                return _error_payload("template_not_found", f"No writing template named '{name}' to refresh.")
            template_dir = _template_dir(context, name)
            venue = (parent_record.get("transition_metadata") or {}).get("venue")
            paper_type = (parent_record.get("transition_metadata") or {}).get("paper_type", "survey")
            if preserve_edits:
                _regenerate_preserve_edits(template_dir, name, parent_record)
            else:
                if template_dir.exists():
                    shutil.rmtree(template_dir)
                _generate_template_files(template_dir, name, venue, paper_type)
            build_result = _compile_preview(template_dir)
            payload_path = _write_payload_file(template_dir, name, venue, paper_type, build_result)
            request = ResearchRecordRequest(
                record_kind="artifact",
                status="ready" if build_result["ok"] else "blocked",
                semantic_id=TEMPLATE_SEMANTIC_ID,
                format_profile_ref=TEMPLATE_PROFILE_REF,
                skill="isomer-kaoju-pipeline",
                producer="isomer-kaoju-pipeline",
                consumer="isomer-kaoju-pipeline, isomer-kaoju-write",
                payload_file=payload_path,
                metadata={
                    "actor_metadata": "isomer-kaoju-pipeline",
                    "template_name": name,
                    "venue": venue,
                    "paper_type": paper_type,
                },
            )
            payload, diagnostics = revise_record(context, parent_record["id"], request, env=os.environ, cwd=Path.cwd())
            payload["template_dir"] = str(template_dir)
            payload["preview_build"] = build_result
            return payload, diagnostics

        return with_context(ctx, kwargs, callback, build_request=False)

    @templates_group.command(name="compile", help="Recompile the preview PDF for an existing template.")
    @_common_options
    @_topic_selection_options
    @click.option("--name", "template_name", default=None, help="Template name; defaults to 'main'.")
    @click.pass_context
    def compile_command(ctx: click.Context, template_name: str | None, **kwargs: Any) -> int:
        def callback(context: EffectiveTopicContext, _request: ResearchRecordRequest | None) -> tuple[dict[str, Any], list[Any]]:
            name = template_name or DEFAULT_TEMPLATE_NAME
            record = _find_template_record(context, name)
            if record is None:
                return _error_payload("template_not_found", f"No writing template named '{name}'.")
            template_dir = _template_dir(context, name)
            if not template_dir.exists():
                return _error_payload("template_dir_missing", f"Template directory missing: {template_dir}")
            build_result = _compile_preview(template_dir)
            request = ResearchRecordRequest(
                record_kind="artifact",
                record_id=record["id"],
                status="ready" if build_result["ok"] else "blocked",
                semantic_id=TEMPLATE_SEMANTIC_ID,
                format_profile_ref=TEMPLATE_PROFILE_REF,
                skill="isomer-kaoju-pipeline",
                producer="isomer-kaoju-pipeline",
                consumer="isomer-kaoju-pipeline, isomer-kaoju-write",
                metadata={
                    "preview_status": "ready" if build_result["ok"] else "failed",
                    "template_name": name,
                },
            )
            payload, diagnostics = revise_record(context, record["id"], request, env=os.environ, cwd=Path.cwd())
            payload["template_dir"] = str(template_dir)
            payload["preview_build"] = {
                "ok": "ready" if build_result["ok"] else "failed",
                "engine": build_result.get("engine"),
                "fallback": build_result.get("fallback"),
                "fallback_reason": build_result.get("fallback_reason"),
                "attempts": build_result.get("attempts", []),
                "preview_pdf": build_result.get("preview_pdf"),
            }
            if not build_result["ok"]:
                payload["ok"] = False
            return payload, diagnostics

        return with_context(ctx, kwargs, callback, build_request=False)

    @templates_group.command(name="remove", help="Archive a writing-template record.")
    @_common_options
    @_topic_selection_options
    @click.option("--name", "template_name", default=None, help="Template name; defaults to 'main'.")
    @click.option("--delete-files", is_flag=True, help="Also remove the template directory.")
    @click.pass_context
    def remove_command(ctx: click.Context, template_name: str | None, delete_files: bool, **kwargs: Any) -> int:
        def callback(context: EffectiveTopicContext, _request: ResearchRecordRequest | None) -> tuple[dict[str, Any], list[Any]]:
            name = template_name or DEFAULT_TEMPLATE_NAME
            record = _find_template_record(context, name)
            if record is None:
                return _error_payload("template_not_found", f"No writing template named '{name}'.")
            payload, diagnostics = archive_record(context, record["id"], env=os.environ, reason="template removed")
            if delete_files:
                template_dir = _template_dir(context, name)
                if template_dir.exists():
                    shutil.rmtree(template_dir)
                payload["template_dir_removed"] = str(template_dir)
            return payload, diagnostics

        return with_context(ctx, kwargs, callback, build_request=False)


def _template_dir(context: EffectiveTopicContext, template_name: str) -> Path:
    return Path(context.topic_workspace_path) / TEMPLATE_RELATIVE_ROOT / template_name


def _generate_template_files(template_dir: Path, template_name: str, venue: str | None, paper_type: str) -> None:
    template_dir.mkdir(parents=True, exist_ok=True)
    document_class = "article"
    class_options = "11pt"
    if venue is not None and venue.lower() in ("acl", "emnlp", "naacl"):
        document_class = "acl"
        class_options = "11pt"
    elif venue is not None and venue.lower() in ("iclr", "icml", "neurips", "colm"):
        document_class = "article"
        class_options = "10pt"
    main_tex = template_dir / "main.tex"
    main_tex.write_text(
        textwrap.dedent(
            f"""\
            \\documentclass[{class_options}]{{{document_class}}}
            \\usepackage[utf8]{{inputenc}}
            \\usepackage[T1]{{fontenc}}
            \\usepackage{{hyperref}}
            \\usepackage{{natbib}}
            \\usepackage{{graphicx}}
            \\usepackage{{xcolor}}

            \\title{{{_escape_latex((venue or 'Survey').capitalize())} Paper Title}}
            \\author{{Author Names}}
            \\date{{\\today}}

            \\begin{{document}}
            \\maketitle

            \\begin{{abstract}}
            Abstract text for the {paper_type} paper.
            \\end{{abstract}}

            \\section{{Introduction}}
            \\label{{sec:intro}}
            Introduction text.

            \\section{{Related Work}}
            \\label{{sec:related}}
            Related work summary.

            \\section{{Methods}}
            \\label{{sec:methods}}
            Method description.

            \\section{{Results}}
            \\label{{sec:results}}
            Results.

            \\section{{Discussion}}
            \\label{{sec:discussion}}
            Discussion.

            \\section{{Conclusion}}
            \\label{{sec:conclusion}}
            Conclusion.

            \\bibliographystyle{{plainnat}}
            \\bibliography{{references}}

            \\end{{document}}
            """
        ),
        encoding="utf-8",
    )
    (template_dir / "references.bib").write_text(
        textwrap.dedent(
            """\
            @article{example2024,
              title={An Example Survey Paper},
              author={Author, A.},
              journal={Journal of Examples},
              year={2024},
            }
            """
        ),
        encoding="utf-8",
    )
    (template_dir / "README.md").write_text(
        textwrap.dedent(
            f"""\
            # Writing Template: {template_name}

            This LaTeX template was generated for a `{paper_type}` paper.
            {f"Target venue: `{venue}`." if venue else "No target venue specified."}

            ## Files

            - `main.tex` — entry point and manuscript structure.
            - `references.bib` — bibliography stub.
            - `preview.pdf` — proof-of-compilation preview when the build succeeds.

            ## Build

            The CLI attempts Tectonic first, then falls back to `pdflatex`/`latexmk`.
            """
        ),
        encoding="utf-8",
    )


def _escape_latex(value: str) -> str:
    return value.replace("&", "\\&").replace("%", "\\%").replace("$", "\\$").replace("#", "\\#").replace("_", "\\_").replace("{", "\\{").replace("}", "\\}").replace("~", "\\textasciitilde{}").replace("^", "\\textasciicircum{}")


def _regenerate_preserve_edits(template_dir: Path, template_name: str, parent_record: dict[str, Any]) -> None:
    preserved = [path for path in sorted(template_dir.rglob("*")) if path.is_file() and path.name not in {"main.tex", "README.md", "preview.pdf"}]
    backup_dir = template_dir.with_name(f"{template_dir.name}.backup")
    if backup_dir.exists():
        shutil.rmtree(backup_dir)
    template_dir.rename(backup_dir)
    _generate_template_files(
        template_dir,
        template_name,
        (parent_record.get("transition_metadata") or {}).get("venue"),
        (parent_record.get("transition_metadata") or {}).get("paper_type", "survey"),
    )
    for path in preserved:
        rel = path.relative_to(backup_dir)
        dest = template_dir / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)
    shutil.rmtree(backup_dir)


def _compile_preview(template_dir: Path) -> dict[str, Any]:
    main_tex = template_dir / "main.tex"
    preview_pdf = template_dir / "preview.pdf"
    engines: list[tuple[str, list[str]]] = [
        ("tectonic", ["tectonic", str(main_tex), "--outfmt", "pdf", "--outfile", str(preview_pdf)]),
    ]
    if shutil.which("pdflatex"):
        engines.append(("pdflatex", ["pdflatex", "-interaction=nonstopmode", "-output-directory", str(template_dir), str(main_tex)]))
    if shutil.which("latexmk"):
        engines.append(("latexmk", ["latexmk", "-pdf", "-outdir=" + str(template_dir), str(main_tex)]))
    attempts: list[dict[str, Any]] = []
    for engine_name, command in engines:
        try:
            result = subprocess.run(
                command,
                cwd=template_dir,
                capture_output=True,
                text=True,
                timeout=120,
            )
            attempts.append({
                "engine": engine_name,
                "command": " ".join(command),
                "exit_code": result.returncode,
                "stdout_tail": result.stdout[-2000:],
                "stderr_tail": result.stderr[-2000:],
            })
            if result.returncode == 0:
                generated = template_dir / "main.pdf"
                if generated.exists() and engine_name != "tectonic":
                    shutil.move(str(generated), str(preview_pdf))
                if preview_pdf.exists():
                    return {
                        "ok": True,
                        "engine": engine_name,
                        "fallback": engine_name != "tectonic",
                        "fallback_reason": None if engine_name == "tectonic" else "tectonic not available or failed",
                        "attempts": attempts,
                        "preview_pdf": str(preview_pdf),
                    }
        except (subprocess.TimeoutExpired, FileNotFoundError) as exc:
            attempts.append({
                "engine": engine_name,
                "command": " ".join(command),
                "exit_code": None,
                "error": str(exc),
            })
    return {
        "ok": False,
        "engine": None,
        "fallback": False,
        "attempts": attempts,
        "preview_pdf": None,
    }


def _write_payload_file(
    template_dir: Path,
    template_name: str,
    venue: str | None,
    paper_type: str,
    build_result: dict[str, Any],
) -> Path:
    payload: dict[str, Any] = {
        "title": f"Writing template: {template_name}",
        "summary": f"Editable LaTeX template for a {paper_type} paper" + (f" targeting {venue}" if venue else ""),
        "artifact_family": "kaoju",
        "semantic_id": TEMPLATE_SEMANTIC_ID,
        "artifact_type": "writing-template",
        "procedure": "create-paper-template",
        "sections": {
            "template": {
                "template_name": template_name,
                "venue": venue,
                "paper_type": paper_type,
                "files": ["main.tex", "references.bib", "README.md"],
            },
            "preview": {
                "status": "ready" if build_result["ok"] else "failed",
                "engine": build_result.get("engine"),
                "fallback": build_result.get("fallback"),
                "fallback_reason": build_result.get("fallback_reason"),
                "preview_pdf_ref": build_result.get("preview_pdf"),
            },
            "status": "ready" if build_result["ok"] else "blocked",
        },
    }
    payload_path = template_dir / "template-payload.json"
    payload_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload_path


def _parents_json(record_id: str) -> list[dict[str, Any]]:
    return [{"record_id": record_id, "lineage_kind": "derived_from", "status": "ready"}]


def _find_template_record(context: EffectiveTopicContext, template_name: str) -> dict[str, Any] | None:
    payload, _ = list_records(context, env=os.environ, semantic_id=TEMPLATE_SEMANTIC_ID, limit=None)
    for record in payload.get("records", []):
        meta = record.get("transition_metadata", {}) or {}
        if meta.get("template_name") == template_name and record.get("status") != "archived":
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
