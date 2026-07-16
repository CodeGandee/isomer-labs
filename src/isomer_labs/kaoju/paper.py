"""MyST-first Kaoju paper production services."""

from __future__ import annotations

from dataclasses import dataclass
from contextlib import contextmanager
import hashlib
from importlib import metadata
import io
import json
from pathlib import Path
import re
import shutil
import tempfile
from typing import Iterator, Mapping, Sequence
import uuid

from docutils import nodes  # type: ignore[import-untyped]
from docutils.core import publish_doctree  # type: ignore[import-untyped]
from myst_parser.parsers.docutils_ import Parser as MystParser

from isomer_labs.kaoju.artifacts import KaojuArtifactService, KaojuServiceError
from isomer_labs.kaoju.content import checksum_file
from isomer_labs.kaoju.contracts import load_binding_registry
from isomer_labs.kaoju.execution import ExecutionAdapterCommandRequest, command_environment, execute_command_request
from isomer_labs.models import EffectiveTopicContext


REQUIRED_PAPER_SECTIONS = (
    "title",
    "abstract",
    "introduction",
    "background",
    "related work",
    "method comparison",
    "discussion",
    "conclusion",
    "references",
)
PLACEHOLDER_RE = re.compile(r"\{\{([a-zA-Z0-9_.:-]+)\}\}")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.M)
CITATION_RE = re.compile(r"\{cite(?::[a-z]+)?\}`([^`]+)`")
DIRECTIVE_RE = re.compile(r"(?m)^:::\{([^}]+)\}")


@dataclass(frozen=True)
class PaperDiagnostic:
    """Structured paper diagnostic tied to a file location."""

    code: str
    message: str
    line: int
    column: int = 1
    severity: str = "error"

    def to_json(self) -> dict[str, object]:
        return {
            "code": self.code,
            "message": self.message,
            "line": self.line,
            "column": self.column,
            "severity": self.severity,
        }


def validate_myst(
    text: str,
    *,
    required_sections: Sequence[str] = REQUIRED_PAPER_SECTIONS,
    allowed_placeholders: Sequence[str] | None = None,
    source_refs: Sequence[str] = (),
    display_refs: Sequence[str] | None = None,
) -> list[PaperDiagnostic]:
    """Validate MyST syntax, structure, placeholders, citations, displays, and refs."""

    diagnostics: list[PaperDiagnostic] = []
    warning_stream = io.StringIO()
    try:
        document = publish_doctree(
            text,
            parser=MystParser(),
            settings_overrides={"warning_stream": warning_stream, "halt_level": 5, "report_level": 1},
        )
    except Exception as exc:  # pragma: no cover - parser defensive boundary
        return [PaperDiagnostic("myst_parse_failed", str(exc), 1)]
    for message in document.findall(nodes.system_message):
        rendered = message.astext()
        if "Unknown interpreted text role \"cite" in rendered:
            continue
        level = int(message.get("level", 2))
        diagnostics.append(
            PaperDiagnostic(
                "myst_syntax",
                rendered.splitlines()[0],
                int(message.get("line") or 1),
                severity="error" if level >= 2 else "warning",
            )
        )
    headings = [(match.group(2).strip(), _normalize_heading(match.group(2)), _line_number(text, match.start())) for match in HEADING_RE.finditer(text)]
    normalized = {value for _raw, value, _line in headings}
    for section in required_sections:
        if _normalize_heading(section) not in normalized:
            diagnostics.append(PaperDiagnostic("myst_required_section_missing", f"Required section is missing: {section}", 1))
    placeholders = [(match.group(1), _line_number(text, match.start())) for match in PLACEHOLDER_RE.finditer(text)]
    if allowed_placeholders is not None:
        allowed = set(allowed_placeholders)
        for placeholder, placeholder_line in placeholders:
            if placeholder not in allowed and not placeholder.startswith(("figure:", "table:", "source:")):
                diagnostics.append(PaperDiagnostic("myst_placeholder_unknown", f"Unknown placeholder: {placeholder}", placeholder_line))
    known_sources = set(source_refs)
    known_displays = set(display_refs or ())
    for placeholder, placeholder_line in placeholders:
        if placeholder.startswith(("figure:", "table:", "source:")):
            kind, _separator, target = placeholder.partition(":")
            if not target:
                diagnostics.append(PaperDiagnostic("myst_typed_placeholder_invalid", f"Typed placeholder lacks a stable ref: {placeholder}", placeholder_line))
            elif kind == "source" and known_sources and target not in known_sources:
                diagnostics.append(PaperDiagnostic("myst_source_ref_unknown", f"Placeholder source ref is not in the accepted source set: {target}", placeholder_line))
            elif kind in {"figure", "table"} and display_refs is not None and target not in known_displays:
                diagnostics.append(PaperDiagnostic("myst_display_ref_unknown", f"Placeholder display ref is not in the accepted display set: {target}", placeholder_line))
            elif display_refs is None and known_sources and target not in known_sources:
                diagnostics.append(PaperDiagnostic("myst_source_ref_unknown", f"Placeholder Artifact ref is not in the accepted ref set: {target}", placeholder_line))
    for match in re.finditer(r"\{cite(?::[a-z]+)?\}`([^`]*)`", text):
        if not match.group(1).strip() or any(not key.strip() for key in match.group(1).split(",")):
            diagnostics.append(PaperDiagnostic("myst_citation_role_invalid", "Citation role requires one or more non-empty keys.", _line_number(text, match.start())))
    if text.count(":::") % 2:
        diagnostics.append(PaperDiagnostic("myst_directive_unclosed", "MyST directive fence is not closed.", max(1, text.count("\n"))))
    for line_number, line in enumerate(text.splitlines(), start=1):
        if "{{citation-needed}}" in line or "<!-- citation-needed" in line:
            diagnostics.append(PaperDiagnostic("myst_evidence_unresolved", "Claim remains visibly outside the accepted evidence boundary.", line_number, severity="warning"))
    return _deduplicate_diagnostics(diagnostics)


def derive_markdown_text(text: str) -> tuple[str, list[PaperDiagnostic]]:
    """Derive deterministic review Markdown while reporting lossy constructs."""

    diagnostics: list[PaperDiagnostic] = []
    output: list[str] = []
    in_directive = False
    for line_number, line in enumerate(text.splitlines(), start=1):
        opening = re.fullmatch(r"\s*:::\{([^}]+)\}\s*", line)
        if opening:
            in_directive = True
            output.append(f"**{opening.group(1).replace('-', ' ').title()}**")
            diagnostics.append(PaperDiagnostic("markdown_lossy_directive", f"MyST directive '{opening.group(1)}' was flattened for review.", line_number, severity="warning"))
            continue
        if in_directive and re.fullmatch(r"\s*:::\s*", line):
            in_directive = False
            continue
        converted = CITATION_RE.sub(lambda match: "[" + "; ".join(f"@{key.strip()}" for key in match.group(1).split(",")) + "]", line)
        converted = re.sub(r"\{\{(figure|table):([^}]+)\}\}", lambda match: f"[{match.group(1).title()} Artifact: `{match.group(2)}`]", converted)
        output.append(converted)
    rendered = "\n".join(output).rstrip() + "\n"
    return rendered, diagnostics


class KaojuPaperService:
    """Implement paper template exchange, derivation, TeX initialization, and PDF build."""

    def __init__(self, context: EffectiveTopicContext, *, env: Mapping[str, str], cwd: Path) -> None:
        self.context = context
        self.env = env
        self.cwd = cwd
        self.artifacts = KaojuArtifactService(context, env=env, cwd=cwd)

    def validate(
        self,
        source: Path,
        *,
        required_sections: Sequence[str] = REQUIRED_PAPER_SECTIONS,
        allowed_placeholders: Sequence[str] | None = None,
        source_refs: Sequence[str] = (),
    ) -> dict[str, object]:
        text = source.read_text(encoding="utf-8")
        diagnostics = validate_myst(text, required_sections=required_sections, allowed_placeholders=allowed_placeholders, source_refs=source_refs)
        return {
            "ok": not _errors(diagnostics),
            "mutated": False,
            "operation": "paper.validate",
            "source": str(source.resolve(strict=False)),
            "checksum": checksum_file(source),
            "diagnostics": [diagnostic.to_json() for diagnostic in diagnostics],
        }

    def export_template(
        self,
        *,
        source_ref: str,
        paper_line: str,
        draft_ref: str,
        citation_map_ref: str,
        source_digest_refs: Sequence[str],
        target: Path | None,
        target_policy: str,
        display_refs: Sequence[str] = (),
    ) -> dict[str, object]:
        raise KaojuServiceError(
            "paper_template_command_retired",
            "The versioned flat template export workflow is retired. Use the named 'ext kaoju paper template export' service.",
            ("Export canonical main or an explicit named template through the mutable named-template service.",),
        )

    def apply_template(self, export_directory: Path, *, confirm_orphans: bool = False) -> dict[str, object]:
        raise KaojuServiceError(
            "paper_template_command_retired",
            "The flat template apply workflow is retired. Use the Kaoju agent to prepare a clean candidate and call named template update with the current state token.",
            ("Inspect both arbitrary trees with the Kaoju agent before low-level replacement or merge.",),
        )

    def derive_markdown(self, *, source_ref: str, paper_line: str, output: Path | None = None) -> dict[str, object]:
        source_path, _record = self._record_file(source_ref, expected={"KAOJU:PAPER-DRAFT-MYST"})
        rendered, diagnostics = derive_markdown_text(source_path.read_text(encoding="utf-8"))
        with self._temporary_directory("paper-markdown-") as temporary:
            generated = output.resolve(strict=False) if output is not None else temporary / "paper-draft.md"
            generated.parent.mkdir(parents=True, exist_ok=True)
            generated.write_text(rendered, encoding="utf-8")
            result = self._upsert_current("KAOJU:PAPER-DRAFT-MD", generated, paper_line, relationships=_relationships(paper_draft_myst=source_ref))
        return {
            "ok": True,
            "mutated": True,
            "operation": "paper.derive-markdown",
            "source_ref": source_ref,
            "source_checksum": checksum_file(source_path),
            "markdown_ref": _record_id(result),
            "canonical": False,
            "output": str(output.resolve(strict=False)) if output is not None else None,
            "diagnostics": [diagnostic.to_json() for diagnostic in diagnostics],
            "affected_refs": [_record_id(result)],
        }

    def init_tex(
        self,
        *,
        draft_ref: str,
        template_myst_ref: str,
        paper_line: str,
        venue: str,
        document_class: str,
        toolchain_policy: str,
        citation_refs: Sequence[str],
    ) -> dict[str, object]:
        draft_path, _draft_record = self._record_file(draft_ref, expected={"KAOJU:PAPER-DRAFT-MYST"})
        template_path, template_record = self._record_file(template_myst_ref, expected={"KAOJU:PAPER-TEMPLATE-MYST", "KAOJU:PAPER-STRUCTURE-MYST"}, allow_directory=True)
        template_metadata_value = template_record.get("transition_metadata")
        template_metadata = template_metadata_value if isinstance(template_metadata_value, dict) else {}
        template_name = template_metadata.get("template_name") if isinstance(template_metadata.get("template_name"), str) else None
        template_digest = template_metadata.get("tree_digest") if isinstance(template_metadata.get("tree_digest"), str) else checksum_file(template_path)
        text = draft_path.read_text(encoding="utf-8")
        myst_diagnostics = validate_myst(text)
        if _errors(myst_diagnostics):
            raise KaojuServiceError("paper_myst_invalid", "Canonical MyST draft failed validation before TeX initialization.", tuple(diagnostic.message for diagnostic in _errors(myst_diagnostics)))
        constructs = sorted(set(DIRECTIVE_RE.findall(text)) | ({"table"} if "|" in text else set()) | ({"citation"} if CITATION_RE.search(text) else set()))
        fingerprint_payload = {"venue": venue, "document_class": document_class, "toolchain_policy": toolchain_policy, "required_constructs": constructs, "source_template_ref": template_myst_ref, "source_template_name": template_name, "source_template_observed_digest": template_digest}
        fingerprint = _digest_json(fingerprint_payload)
        existing_template_ref = self._latest_ref("KAOJU:PAPER-TEMPLATE-TEX", paper_line)
        reused = False
        if existing_template_ref is not None:
            existing_manifest = self._directory_member_json(existing_template_ref, "manifest.json")
            reused = existing_manifest.get("compatibility_fingerprint") == fingerprint

        with self._temporary_directory("paper-tex-") as temporary:
            if reused and existing_template_ref is not None:
                template_ref = existing_template_ref
            else:
                template_tree = temporary / "template"
                template_tree.mkdir()
                (template_tree / "template.tex").write_text(_tex_template(document_class, venue), encoding="utf-8")
                _write_json(template_tree / "manifest.json", {"schema_version": "isomer-kaoju-tex-manifest.v1", "kind": "template", "compatibility_fingerprint": fingerprint, "fingerprint_dimensions": fingerprint_payload, "source_ref": template_myst_ref, "source_template_name": template_name, "source_observed_digest": template_digest, "tool": "isomer-myst-initializer.v1", "included_files": ["template.tex"]})
                template_result = self._upsert_current("KAOJU:PAPER-TEMPLATE-TEX", template_tree, paper_line, relationships=_relationships(paper_template_myst=template_myst_ref))
                template_ref = _record_id(template_result)
            draft_tree = temporary / "draft"
            draft_tree.mkdir()
            converted, conversion_diagnostics = _myst_to_tex(text)
            (draft_tree / "main.tex").write_text(_tex_document(document_class, venue, converted), encoding="utf-8")
            _write_json(draft_tree / "manifest.json", {"schema_version": "isomer-kaoju-tex-manifest.v1", "kind": "draft", "compatibility_fingerprint": fingerprint, "source_ref": draft_ref, "source_checksum": checksum_file(draft_path), "template_ref": template_ref, "source_template_ref": template_myst_ref, "source_template_name": template_name, "source_template_observed_digest": template_digest, "citation_inputs": list(citation_refs), "included_files": ["main.tex"], "conversion_diagnostics": [diagnostic.to_json() for diagnostic in conversion_diagnostics], "agent_inspection": {"status": "required", "reason": "mechanical initialization does not establish build readiness"}})
            draft_result = self._upsert_current("KAOJU:PAPER-DRAFT-TEX", draft_tree, paper_line, relationships=_relationships(paper_draft_myst=draft_ref, paper_template_tex=template_ref))
        all_diagnostics = [*myst_diagnostics, *conversion_diagnostics]
        return {
            "ok": True,
            "mutated": True,
            "operation": "paper.init-tex",
            "template_ref": template_ref,
            "source_template_ref": template_myst_ref,
            "source_template_name": template_name,
            "source_template_observed_digest": template_digest,
            "template_reused": reused,
            "draft_ref": _record_id(draft_result),
            "compatibility_fingerprint": fingerprint,
            "build_ready": False,
            "agent_inspection_required": True,
            "diagnostics": [diagnostic.to_json() for diagnostic in all_diagnostics],
            "affected_refs": [template_ref, _record_id(draft_result)],
        }

    def build_pdf(
        self,
        *,
        draft_tex_ref: str,
        template_tex_ref: str,
        paper_line: str,
        audit_ref: str,
        inspected: bool,
        pdf_inspected: bool,
        publication_approved: bool,
        timeout_seconds: float,
        toolchain: str | None = None,
    ) -> dict[str, object]:
        if not inspected:
            raise KaojuServiceError("paper_tex_inspection_required", "Mechanically initialized TeX requires recorded agent inspection before build.")
        draft_manifest_path, _record = self._record_file(draft_tex_ref, expected={"KAOJU:PAPER-DRAFT-TEX"}, allow_directory=True)
        self._record_file(template_tex_ref, expected={"KAOJU:PAPER-TEMPLATE-TEX"}, allow_directory=True)
        _audit_path, audit_record = self._record_file(audit_ref, expected={"KAOJU:AUDIT-REPORT"})
        if audit_record.get("status") != "ready":
            raise KaojuServiceError("paper_audit_not_accepted", f"Audit Report {audit_ref} is not accepted and ready; PDF build is blocked.")
        source_tree = draft_manifest_path.parent
        selected, fallback = _select_tex_toolchain(toolchain)
        if selected is None:
            raise KaojuServiceError("paper_compiler_missing", "No supported TeX compiler is available.", ("Install Tectonic, latexmk, or pdflatex in the selected Topic Workspace environment.",))
        build_id = f"artifact-paper-build-run-{uuid.uuid4().hex[:12]}"
        with self._temporary_directory("paper-build-") as temporary:
            build_tree = temporary / "build"
            shutil.copytree(source_tree, build_tree)
            argv = _tex_command(selected)
            request = ExecutionAdapterCommandRequest.create(extension_point="document_build", argv=argv, cwd=build_tree, timeout_seconds=timeout_seconds, recording_refs=(draft_tex_ref, template_tex_ref, build_id))
            observation = execute_command_request(request, env=command_environment(self.env))
            log_path = temporary / "compile.log"
            log_path.write_text(_compile_log(selected, fallback, observation), encoding="utf-8")
            pdf_path = build_tree / "main.pdf"
            pdf_valid = pdf_path.is_file() and pdf_path.stat().st_size > 8 and pdf_path.read_bytes()[:4] == b"%PDF"
            terminal = "complete" if observation.get("status") == "succeeded" and pdf_valid else "failed"
            run_path = temporary / "paper-build-run.json"
            _write_json(run_path, _structured_payload("KAOJU:PAPER-BUILD-RUN", "Paper PDF build Run", "Immutable registered document-build attempt.", {"execution": {"command_request": observation.get("request"), "toolchain": selected, "fallback": fallback, "input_refs": [draft_tex_ref, template_tex_ref]}, "result": {"terminal_status": terminal, "returncode": observation.get("returncode"), "elapsed_seconds": observation.get("elapsed_seconds"), "pdf_magic_valid": pdf_valid}}))
            run_result = self.artifacts.put("KAOJU:PAPER-BUILD-RUN", run_path, producer="isomer-kaoju-write", scope_key=paper_line, record_id=build_id, status=terminal, relationships=_relationships(paper_draft_tex=draft_tex_ref, paper_template_tex=template_tex_ref))
            log_result = self.artifacts.put("KAOJU:PAPER-COMPILE-LOG", log_path, producer="isomer-kaoju-write", scope_key=paper_line, status="ready" if terminal == "complete" else "failed", relationships=_relationships(paper_build_run=build_id))
            affected = [_record_id(run_result), _record_id(log_result)]
            if terminal != "complete":
                return {"ok": False, "mutated": True, "operation": "paper.build-pdf", "terminal_status": terminal, "build_run_ref": build_id, "compile_log_ref": _record_id(log_result), "command_request": observation.get("request"), "fallback": fallback, "affected_refs": affected, "recovery_actions": ["Inspect the registered compile log and classify any repair as presentation-only or material before retrying."]}
            pdf_result = self.artifacts.put("KAOJU:PAPER-PDF", pdf_path, producer="isomer-kaoju-write", scope_key=paper_line, relationships=_relationships(paper_build_run=build_id, paper_draft_tex=draft_tex_ref))
            pdf_ref = _record_id(pdf_result)
            revision_path = temporary / "paper-pdf-revision-log.json"
            _write_json(revision_path, _structured_payload("KAOJU:PAPER-PDF-REVISION-LOG", "Paper PDF revision log", "Append-only build attempt and repair provenance.", {"builds": [{"build_run_ref": build_id, "compile_log_ref": _record_id(log_result), "pdf_ref": pdf_ref, "toolchain": selected, "fallback": fallback, "repair_class": "none"}]}))
            revision_result = self.artifacts.put("KAOJU:PAPER-PDF-REVISION-LOG", revision_path, producer="isomer-kaoju-write", scope_key=paper_line, relationships=_relationships(paper_pdf=pdf_ref, paper_build_run=build_id))
            validation_path = temporary / "paper-validation-report.json"
            accepted = publication_approved and pdf_inspected
            verdict = "ready" if accepted else "not-ready"
            _write_json(validation_path, _structured_payload("KAOJU:PAPER-VALIDATION-REPORT", "Paper validation report", "Structural, textual, visual, evidence, and publication assessment.", {"assessment": {"verdict": verdict, "compile": "passed", "pdf_magic": "passed", "textual_inspection": "passed" if pdf_inspected else "required", "visual_inspection": "passed" if pdf_inspected else "required", "publication_gate": "approved" if publication_approved else "pending", "known_limitations": [] if pdf_inspected else ["Direct textual and visual PDF inspection remains required."]}, "quality_profile": {"audit_ref": audit_ref, "canonical_myst_required": True, "publication_accepted": accepted}}))
            validation_result = self.artifacts.put("KAOJU:PAPER-VALIDATION-REPORT", validation_path, producer="isomer-kaoju-write", scope_key=paper_line, status="ready" if accepted else "blocked", relationships=_relationships(paper_build_run=build_id, paper_pdf=pdf_ref, audit_report=audit_ref))
            affected.extend([pdf_ref, _record_id(revision_result), _record_id(validation_result)])
        accepted = publication_approved and pdf_inspected
        return {"ok": True, "mutated": True, "operation": "paper.build-pdf", "terminal_status": "complete", "pdf_inspection": "passed" if pdf_inspected else "required", "publication_gate": "approved" if publication_approved else "pending", "accepted": accepted, "build_run_ref": build_id, "compile_log_ref": _record_id(log_result), "pdf_ref": pdf_ref, "revision_log_ref": _record_id(revision_result), "validation_ref": _record_id(validation_result), "command_request": observation.get("request"), "fallback": fallback, "affected_refs": affected}

    def _record_file(self, record_id: str, *, expected: set[str], allow_directory: bool = False) -> tuple[Path, dict[str, object]]:
        payload = self.artifacts.show(record_id, include_content=True)
        record = payload.get("record")
        if not isinstance(record, dict):
            raise KaojuServiceError("paper_input_missing", f"Paper input record not found: {record_id}")
        content_diagnostics = payload.get("content_diagnostics")
        if isinstance(content_diagnostics, list) and any(isinstance(item, dict) and item.get("severity") == "error" for item in content_diagnostics):
            raise KaojuServiceError("paper_input_content_stale", f"Paper input {record_id} has missing, stale, or corrupt authoritative content.")
        semantic_id = _semantic_id(record)
        if semantic_id not in expected:
            raise KaojuServiceError("paper_input_semantic_invalid", f"Record {record_id} has semantic id {semantic_id!r}; expected one of {sorted(expected)}.")
        raw_path = record.get("content_path")
        if not isinstance(raw_path, str):
            raise KaojuServiceError("paper_input_content_missing", f"Paper input {record_id} has no authoritative file content.")
        path = Path(raw_path)
        if not path.is_file():
            raise KaojuServiceError("paper_input_content_missing", f"Paper input content is missing: {path}")
        if not allow_directory and path.name == ".isomer-artifact-manifest.json":
            raise KaojuServiceError("paper_input_file_expected", f"Paper input {record_id} resolves to a directory manifest, not an ordinary file.")
        return path, record

    def _latest_ref(self, semantic_id: str, scope_key: str) -> str | None:
        payload = self.artifacts.latest(semantic_id, scope_key=scope_key)
        records = payload.get("records")
        if not isinstance(records, list) or not records:
            return None
        record_id = records[0].get("record_id") if isinstance(records[0], dict) else None
        return str(record_id) if record_id else None

    def _upsert_current(self, semantic_id: str, content: Path, scope_key: str, *, relationships: list[dict[str, object]]) -> dict[str, object]:
        current = self._latest_ref(semantic_id, scope_key)
        if current is None:
            return self.artifacts.put(semantic_id, content, producer="isomer-kaoju-write", scope_key=scope_key, relationships=relationships)
        return self.artifacts.revise(current, content, producer="isomer-kaoju-write", scope_key=scope_key, relationships=relationships)

    def _directory_member_json(self, record_id: str, name: str) -> dict[str, object]:
        manifest_path, _record = self._record_file(record_id, expected={"KAOJU:PAPER-TEMPLATE-TEX"}, allow_directory=True)
        member = manifest_path.parent / name
        return _load_json(member)

    @contextmanager
    def _temporary_directory(self, prefix: str) -> Iterator[Path]:
        root = self.context.topic_workspace_path / "tmp" / "kaoju-service"
        root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix=prefix, dir=root) as raw:
            yield Path(raw)


def _myst_to_tex(text: str) -> tuple[str, list[PaperDiagnostic]]:
    diagnostics: list[PaperDiagnostic] = []
    output: list[str] = []
    in_directive = False
    for line_number, line in enumerate(text.splitlines(), start=1):
        heading = re.fullmatch(r"(#{1,6})\s+(.+)", line)
        if heading:
            level = len(heading.group(1))
            command = "section" if level <= 2 else "subsection" if level == 3 else "subsubsection"
            output.append(f"\\{command}{{{_tex_escape(heading.group(2))}}}")
            continue
        directive = re.fullmatch(r"\s*:::\{([^}]+)\}\s*", line)
        if directive:
            in_directive = True
            output.append(f"\\begin{{quote}}\\textbf{{{_tex_escape(directive.group(1).title())}.}}")
            diagnostics.append(PaperDiagnostic("tex_repair_directive", f"Directive '{directive.group(1)}' was simplified and requires inspection.", line_number, severity="warning"))
            continue
        if in_directive and re.fullmatch(r"\s*:::\s*", line):
            in_directive = False
            output.append("\\end{quote}")
            continue
        if line.lstrip().startswith("|"):
            diagnostics.append(PaperDiagnostic("tex_repair_table", "Markdown table requires direct TeX table inspection and repair.", line_number, severity="warning"))
            output.append(f"% ISOMER_REPAIR_TABLE: {_tex_escape(line)}")
            continue
        converted = CITATION_RE.sub(lambda match: "\\cite{" + ",".join(key.strip() for key in match.group(1).split(",")) + "}", line)
        converted = PLACEHOLDER_RE.sub(lambda match: f"\\textbf{{[UNRESOLVED { _tex_escape(match.group(1)) }]}}", converted)
        if not converted.startswith("\\"):
            converted = _tex_escape(converted, preserve_commands=True)
        output.append(converted)
    return "\n\n".join(output).rstrip() + "\n", diagnostics


def _tex_template(document_class: str, venue: str) -> str:
    return f"\\documentclass{{{_tex_identifier(document_class)}}}\n\\usepackage[utf8]{{inputenc}}\n\\usepackage{{hyperref,graphicx,booktabs,longtable,tabularx}}\n% Venue: {_tex_escape(venue)}\n"


def _tex_document(document_class: str, venue: str, body: str) -> str:
    return _tex_template(document_class, venue) + "\\title{Survey Paper}\n\\author{}\n\\begin{document}\n\\maketitle\n" + body + "\\end{document}\n"


def _select_tex_toolchain(requested: str | None) -> tuple[str | None, str | None]:
    supported = ["tectonic", "latexmk", "pdflatex"]
    if requested is not None:
        if requested not in supported:
            raise KaojuServiceError("paper_toolchain_invalid", f"Unsupported TeX toolchain: {requested}")
        return (requested, None) if shutil.which(requested) else (None, None)
    for index, candidate in enumerate(supported):
        if shutil.which(candidate):
            return candidate, None if index == 0 else f"preferred tectonic unavailable; selected {candidate}"
    return None, None


def _tex_command(toolchain: str) -> tuple[str, ...]:
    if toolchain == "tectonic":
        return ("tectonic", "--keep-logs", "--synctex", "main.tex")
    if toolchain == "latexmk":
        return ("latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "main.tex")
    return ("pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex")


def _compile_log(toolchain: str, fallback: str | None, observation: Mapping[str, object]) -> str:
    request = observation.get("request")
    return json.dumps({"schema_version": "isomer-kaoju-paper-compile-log.v1", "toolchain": toolchain, "fallback_rationale": fallback, "command_request": request, "status": observation.get("status"), "returncode": observation.get("returncode"), "elapsed_seconds": observation.get("elapsed_seconds"), "stdout": observation.get("stdout"), "stderr": observation.get("stderr")}, indent=2, sort_keys=True) + "\n"


def _structured_payload(semantic_id: str, title: str, summary: str, sections: dict[str, object]) -> dict[str, object]:
    return {"title": title, "summary": summary, "artifact_family": "kaoju", "semantic_id": semantic_id, "artifact_type": load_binding_registry()[semantic_id].artifact_type, "sections": sections}


def _relationships(**values: str) -> list[dict[str, object]]:
    return [{"role": role, "target_ref": target} for role, target in values.items()]


def _record_id(payload: Mapping[str, object]) -> str:
    record = payload.get("record")
    if isinstance(record, dict) and isinstance(record.get("id"), str):
        return record["id"]
    affected = payload.get("affected_refs")
    if isinstance(affected, list) and affected:
        return str(affected[0])
    raise KaojuServiceError("paper_record_ref_missing", "Artifact service did not return a stable record ref.")


def _semantic_id(record: Mapping[str, object]) -> str:
    metadata_value = record.get("transition_metadata")
    metadata_map = metadata_value if isinstance(metadata_value, dict) else {}
    return str(metadata_map.get("semantic_id") or "")


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def _load_json(path: Path) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise KaojuServiceError("paper_manifest_unreadable", f"Paper manifest is unreadable: {exc}") from exc
    if not isinstance(value, dict):
        raise KaojuServiceError("paper_manifest_invalid", "Paper manifest must be a JSON object.")
    return value


def _errors(diagnostics: Sequence[PaperDiagnostic]) -> list[PaperDiagnostic]:
    return [diagnostic for diagnostic in diagnostics if diagnostic.severity == "error"]


def _deduplicate_diagnostics(diagnostics: Sequence[PaperDiagnostic]) -> list[PaperDiagnostic]:
    seen: set[tuple[object, ...]] = set()
    result: list[PaperDiagnostic] = []
    for diagnostic in diagnostics:
        key = (diagnostic.code, diagnostic.message, diagnostic.line, diagnostic.column, diagnostic.severity)
        if key not in seen:
            seen.add(key)
            result.append(diagnostic)
    return result


def _line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _normalize_heading(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()


def _digest_json(value: Mapping[str, object]) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def _tex_identifier(value: str) -> str:
    selected = re.sub(r"[^A-Za-z0-9_-]", "", value)
    return selected or "article"


def _tex_escape(value: str, *, preserve_commands: bool = False) -> str:
    replacements = {"&": "\\&", "%": "\\%", "$": "\\$", "#": "\\#", "_": "\\_", "~": "\\textasciitilde{}", "^": "\\textasciicircum{}"}
    if not preserve_commands:
        replacements.update({"\\": "\\textbackslash{}", "{": "\\{", "}": "\\}"})
    return "".join(replacements.get(character, character) for character in value)


def myst_parser_version() -> str:
    try:
        return metadata.version("myst-parser")
    except metadata.PackageNotFoundError:  # pragma: no cover
        return "unknown"
