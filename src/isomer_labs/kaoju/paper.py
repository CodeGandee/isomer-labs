"""MyST-first Kaoju paper production services."""

from __future__ import annotations

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
import yaml  # type: ignore[import-untyped]

from isomer_labs.kaoju.artifacts import KaojuArtifactService, KaojuServiceError
from isomer_labs.kaoju.content import checksum_file
from isomer_labs.kaoju.execution import ExecutionAdapterCommandRequest, command_environment, execute_command_request
from isomer_labs.kaoju.paper_support import (
    CITATION_RE,
    FRONTMATTER_RE,
    PLACEHOLDER_RE,
    PaperDiagnostic,
    _compile_log,
    _compose_latex_tree,
    _extract_abstract,
    _extract_frontmatter,
    _fill_obligations,
    _frontmatter_title_authors,
    _latex_state_identity,
    _load_json,
    _load_tex_manifest,
    _myst_to_tex,
    _normalize_heading,
    _paper_tree_digest,
    _record_id,
    _relationships,
    _select_tex_toolchain,
    _semantic_id,
    _strip_title_heading,
    _structured_payload,
    _tex_command,
    _tree_files,
    _unfilled_obligations,
    _write_json,
)
from isomer_labs.kaoju.templates import KaojuTemplateService
from isomer_labs.kaoju.template_support import (
    TEX_DRAFT_MANIFEST_NAME,
    TEX_FILL_MANIFEST_NAME,
    TEX_SNAPSHOT_MANIFEST_NAME,
    validate_template_relative_path,
)
from isomer_labs.models import EffectiveTopicContext


REQUIRED_PAPER_SECTIONS = (
    "abstract",
    "introduction",
    "background",
    "related work",
    "method comparison",
    "discussion",
    "conclusion",
    "references",
)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.M)
DIRECTIVE_RE = re.compile(r"(?m)^:::\{([^}]+)\}")


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
    frontmatter_match = FRONTMATTER_RE.match(text)
    if frontmatter_match:
        try:
            parsed_frontmatter = yaml.safe_load(frontmatter_match.group(1))
        except yaml.YAMLError as exc:
            diagnostics.append(PaperDiagnostic("myst_frontmatter_invalid", f"MyST frontmatter is not valid YAML: {exc}", 1))
        else:
            if not isinstance(parsed_frontmatter, dict):
                diagnostics.append(PaperDiagnostic("myst_frontmatter_invalid", "MyST frontmatter must be a YAML mapping.", 1))
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
    """Implement paper derivation, LaTeX composition, drift inspection, and PDF build."""

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
            ("Export content/main or latex/main, or an explicit role-local name, through the mutable named-template service.",),
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
        paper_line: str,
        content_template_ref: str | None = None,
        template_myst_ref: str | None = None,
        latex_template_name: str | None = None,
        latex_template_ref: str | None = None,
        venue: str | None = None,
        document_class: str | None = None,
        toolchain_policy: str | None = None,
        citation_refs: Sequence[str] = (),
    ) -> dict[str, object]:
        if content_template_ref and template_myst_ref and content_template_ref != template_myst_ref:
            raise KaojuServiceError(
                "paper_content_template_selector_mismatch",
                "content_template_ref and the deprecated template_myst_ref alias identify different records.",
            )
        selected_content_ref = content_template_ref or template_myst_ref
        if not selected_content_ref:
            raise KaojuServiceError(
                "paper_content_template_required",
                "TeX composition requires the exact observed content-template ref.",
            )
        draft_path, _draft_record = self._record_file(draft_ref, expected={"KAOJU:PAPER-DRAFT-MYST"})
        template_path, template_record = self._record_file(
            selected_content_ref,
            expected={"KAOJU:PAPER-TEMPLATE-MYST", "KAOJU:PAPER-STRUCTURE-MYST"},
            allow_directory=True,
        )
        template_metadata_value = template_record.get("transition_metadata")
        template_metadata = template_metadata_value if isinstance(template_metadata_value, dict) else {}
        content_template = {
            "kind": "content",
            "ref": selected_content_ref,
            "name": template_metadata.get("template_name") if isinstance(template_metadata.get("template_name"), str) else None,
            "state_token": template_metadata.get("state_token") if isinstance(template_metadata.get("state_token"), str) else None,
            "tree_digest": template_metadata.get("tree_digest") if isinstance(template_metadata.get("tree_digest"), str) else checksum_file(template_path),
        }
        latex_service = KaojuTemplateService(self.context, env=self.env, cwd=self.cwd, kind="latex")
        try:
            latex_state = latex_service.resolve_state(name=latex_template_name, stable_ref=latex_template_ref)
        except KaojuServiceError as exc:
            if exc.code == "template_not_found" and latex_template_name is None and latex_template_ref is None:
                raise KaojuServiceError(
                    "paper_latex_template_default_missing",
                    "TeX composition omitted a LaTeX selector, but latex/main does not exist.",
                    (
                        "Create latex/main from a prepared directory.",
                        "Adopt an exact KAOJU:PAPER-TEMPLATE-TEX source through template migration.",
                    ),
                ) from exc
            raise
        latex_metadata = latex_state.authored_metadata
        extensions = latex_metadata.get("extensions")
        latex_contract = extensions.get("latex") if isinstance(extensions, dict) else None
        if not isinstance(latex_contract, dict):
            raise KaojuServiceError(
                "latex_template_contract_required",
                f"Named LaTeX template {latex_state.name!r} has no checked composition contract.",
            )
        stock_entrypoint = latex_metadata.get("entrypoint")
        if not isinstance(stock_entrypoint, str):
            raise KaojuServiceError("latex_template_entrypoint_required", "Named LaTeX stock has no entrypoint.")
        build_profile = latex_contract.get("build_profile")
        if not isinstance(build_profile, str):
            raise KaojuServiceError("latex_template_build_profile_invalid", "Named LaTeX stock has no registered build profile.")
        text = draft_path.read_text(encoding="utf-8")
        myst_diagnostics = validate_myst(text)
        if _errors(myst_diagnostics):
            raise KaojuServiceError("paper_myst_invalid", "Canonical MyST draft failed validation before TeX initialization.", tuple(diagnostic.message for diagnostic in _errors(myst_diagnostics)))
        frontmatter, body = _extract_frontmatter(text)
        frontmatter_title, frontmatter_authors = _frontmatter_title_authors(frontmatter)
        abstract_text, body = _extract_abstract(body)
        body = _strip_title_heading(body, frontmatter_title)
        bibliography = self._bibliography_entries(citation_refs)
        constructs = sorted(set(DIRECTIVE_RE.findall(text)) | ({"table"} if "|" in text else set()) | ({"citation"} if CITATION_RE.search(text) else set()))
        fingerprint_payload = {
            "latex_template_ref": latex_state.record.id,
            "latex_template_name": latex_state.name,
            "latex_template_state_token": latex_state.state_token,
            "latex_template_tree_digest": latex_state.tree_digest,
            "composition_contract": latex_contract,
            "converter": {"id": "isomer-myst-to-tex.v3", "myst_parser_version": myst_parser_version()},
            "required_constructs": constructs,
            "build_profile": build_profile,
        }
        fingerprint = _digest_json(fingerprint_payload)
        existing_template_ref = self._latest_ref("KAOJU:PAPER-TEMPLATE-TEX", paper_line)
        reused = False
        if existing_template_ref is not None:
            existing_manifest = self._directory_member_json(existing_template_ref, TEX_SNAPSHOT_MANIFEST_NAME)
            reused = (
                existing_manifest.get("compatibility_fingerprint") == fingerprint
                and existing_manifest.get("stock_tree_digest") == latex_state.tree_digest
            )

        with self._temporary_directory("paper-tex-") as temporary:
            if reused and existing_template_ref is not None:
                template_ref = existing_template_ref
            else:
                template_tree = temporary / "template"
                latex_service._copy_canonical_tree(latex_state.root, template_tree)
                observed_snapshot_digest = _paper_tree_digest(template_tree, excluded={TEX_SNAPSHOT_MANIFEST_NAME})
                if observed_snapshot_digest != latex_state.tree_digest:
                    raise KaojuServiceError(
                        "paper_latex_snapshot_digest_mismatch",
                        "Copied LaTeX snapshot bytes do not match the selected named stock digest.",
                    )
                snapshot_manifest = {
                    "schema_version": "isomer-kaoju-tex-snapshot.v2",
                    "kind": "latex-template-snapshot",
                    "compatibility_fingerprint": fingerprint,
                    "fingerprint_dimensions": fingerprint_payload,
                    "stocked_latex_template": _latex_state_identity(latex_state),
                    "stock_tree_digest": latex_state.tree_digest,
                    "stock_entrypoint": stock_entrypoint,
                    "composition_contract": latex_contract,
                    "build_profile": build_profile,
                    "source_provenance": latex_contract.get("source_provenance"),
                    "included_files": _tree_files(template_tree),
                }
                _write_json(template_tree / TEX_SNAPSHOT_MANIFEST_NAME, snapshot_manifest)
                template_result = self._upsert_current(
                    "KAOJU:PAPER-TEMPLATE-TEX",
                    template_tree,
                    paper_line,
                    relationships=_relationships(paper_template_latex=latex_state.record.id),
                )
                template_ref = _record_id(template_result)
            draft_tree = temporary / "draft"
            latex_service._copy_canonical_tree(latex_state.root, draft_tree)
            converted, conversion_diagnostics = _myst_to_tex(body)
            composed_entrypoint = _compose_latex_tree(
                draft_tree,
                stock_entrypoint=stock_entrypoint,
                contract=latex_contract,
                converted_body=converted,
                frontmatter=frontmatter,
            )
            fill_obligations = _fill_obligations(
                frontmatter_title=frontmatter_title,
                frontmatter_authors=frontmatter_authors,
                abstract_text=abstract_text,
                bibliography=bibliography,
                conversion_diagnostics=conversion_diagnostics,
                latex_contract=latex_contract,
                entrypoint=composed_entrypoint,
            )
            fill_manifest = {
                "schema_version": "isomer-kaoju-tex-fill.v1",
                "kind": "tex-fill-contract",
                "source_ref": draft_ref,
                "entrypoint": composed_entrypoint,
                "frontmatter": json.loads(json.dumps(frontmatter, default=str)),
                "abstract": abstract_text,
                "obligations": fill_obligations,
            }
            _write_json(draft_tree / TEX_FILL_MANIFEST_NAME, fill_manifest)
            composed_tree_digest = _paper_tree_digest(draft_tree, excluded={TEX_DRAFT_MANIFEST_NAME, TEX_FILL_MANIFEST_NAME})
            draft_manifest = {
                "schema_version": "isomer-kaoju-tex-draft.v2",
                "kind": "composed-tex-draft",
                "compatibility_fingerprint": fingerprint,
                "source_ref": draft_ref,
                "source_checksum": checksum_file(draft_path),
                "content_template": content_template,
                "template_ref": template_ref,
                "template_snapshot_tree_digest": latex_state.tree_digest,
                "latex_template": _latex_state_identity(latex_state),
                "stock_entrypoint": stock_entrypoint,
                "entrypoint": composed_entrypoint,
                "composition_contract": latex_contract,
                "build_profile": build_profile,
                "citation_inputs": list(citation_refs),
                "fill_manifest": TEX_FILL_MANIFEST_NAME,
                "included_files": _tree_files(draft_tree),
                "initial_composed_tree_digest": composed_tree_digest,
                "paper_local_repair": False,
                "conversion_diagnostics": [diagnostic.to_json() for diagnostic in conversion_diagnostics],
                "legacy_presentation_hints": {
                    "venue": venue,
                    "document_class": document_class,
                    "toolchain_policy": toolchain_policy,
                },
                "agent_inspection": {
                    "status": "required",
                    "reason": "mechanical composition does not establish build readiness",
                },
            }
            _write_json(draft_tree / TEX_DRAFT_MANIFEST_NAME, draft_manifest)
            draft_result = self._upsert_current("KAOJU:PAPER-DRAFT-TEX", draft_tree, paper_line, relationships=_relationships(paper_draft_myst=draft_ref, paper_template_tex=template_ref))
        all_diagnostics = [*myst_diagnostics, *conversion_diagnostics]
        return {
            "ok": True,
            "mutated": True,
            "operation": "paper.init-tex",
            "template_ref": template_ref,
            "content_template": content_template,
            "latex_template": _latex_state_identity(latex_state),
            "entrypoint": composed_entrypoint,
            "composition_mode": latex_contract.get("composition_mode"),
            "build_profile": build_profile,
            "template_reused": reused,
            "draft_ref": _record_id(draft_result),
            "compatibility_fingerprint": fingerprint,
            "build_ready": False,
            "agent_inspection_required": True,
            "fill_obligations": fill_obligations,
            "diagnostics": [diagnostic.to_json() for diagnostic in all_diagnostics],
            "affected_refs": [template_ref, _record_id(draft_result)],
        }

    def tex_status(self, *, draft_tex_ref: str) -> dict[str, object]:
        draft_manifest_path, _record = self._record_file(
            draft_tex_ref,
            expected={"KAOJU:PAPER-DRAFT-TEX"},
            allow_directory=True,
        )
        draft_tree = draft_manifest_path.parent
        manifest = _load_tex_manifest(draft_tree, TEX_DRAFT_MANIFEST_NAME)
        recorded_composed_digest = manifest.get("initial_composed_tree_digest")
        current_composed_digest = _paper_tree_digest(draft_tree, excluded={TEX_DRAFT_MANIFEST_NAME, TEX_FILL_MANIFEST_NAME})
        paper_local_repair = current_composed_digest != recorded_composed_digest
        content_identity = manifest.get("content_template")
        content_posture = "unknown"
        current_content: dict[str, object] | None = None
        if isinstance(content_identity, dict):
            content_ref = content_identity.get("ref")
            content_name = content_identity.get("name")
            if isinstance(content_name, str):
                content_service = KaojuTemplateService(self.context, env=self.env, cwd=self.cwd, kind="content")
                try:
                    content_state = content_service.resolve_state(
                        name=content_name,
                        stable_ref=str(content_ref) if isinstance(content_ref, str) else None,
                    )
                except KaojuServiceError as exc:
                    content_posture = "missing" if exc.code in {"template_not_found", "template_record_not_found"} else "invalid"
                else:
                    current_content = {
                        "kind": "content",
                        "name": content_state.name,
                        "ref": content_state.record.id,
                        "state_token": content_state.state_token,
                        "tree_digest": content_state.tree_digest,
                    }
                    content_posture = (
                        "current"
                        if content_state.state_token == content_identity.get("state_token")
                        and content_state.tree_digest == content_identity.get("tree_digest")
                        else "content-stale"
                    )
            else:
                content_posture = "fixed"
        latex_identity = manifest.get("latex_template")
        stocked_posture = "unknown"
        current_latex: dict[str, object] | None = None
        if isinstance(latex_identity, dict):
            stable_ref = latex_identity.get("stable_ref")
            name = latex_identity.get("name")
            service = KaojuTemplateService(self.context, env=self.env, cwd=self.cwd, kind="latex")
            try:
                state = service.resolve_state(
                    name=str(name) if isinstance(name, str) else None,
                    stable_ref=str(stable_ref) if isinstance(stable_ref, str) else None,
                )
            except KaojuServiceError as exc:
                stocked_posture = "missing" if exc.code in {"template_not_found", "template_record_not_found"} else "invalid"
            else:
                current_latex = _latex_state_identity(state)
                stocked_posture = (
                    "current"
                    if state.state_token == latex_identity.get("state_token") and state.tree_digest == latex_identity.get("tree_digest")
                    else "presentation-stale"
                )
        return {
            "ok": True,
            "mutated": False,
            "operation": "paper.tex-status",
            "draft_ref": draft_tex_ref,
            "template_ref": manifest.get("template_ref"),
            "content_template": manifest.get("content_template"),
            "observed_content_template": content_identity,
            "current_content_template": current_content,
            "content_template_posture": content_posture,
            "observed_latex_template": latex_identity,
            "current_latex_template": current_latex,
            "stocked_template_posture": stocked_posture,
            "paper_local_repair": paper_local_repair,
            "recorded_composed_tree_digest": recorded_composed_digest,
            "current_composed_tree_digest": current_composed_digest,
            "entrypoint": manifest.get("entrypoint"),
            "diagnostics": [
                diagnostic.to_json()
                for diagnostic in _unfilled_obligations(draft_tree, str(manifest.get("entrypoint") or ""))
            ],
            "next_actions": [],
        }

    def build_pdf(
        self,
        *,
        draft_tex_ref: str,
        template_tex_ref: str | None,
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
        source_tree = draft_manifest_path.parent
        draft_manifest = _load_tex_manifest(source_tree, TEX_DRAFT_MANIFEST_NAME)
        pinned_template_ref = draft_manifest.get("template_ref")
        if not isinstance(pinned_template_ref, str):
            raise KaojuServiceError("paper_template_pin_missing", "TeX draft manifest has no pinned template snapshot ref.")
        if template_tex_ref is not None and template_tex_ref != pinned_template_ref:
            raise KaojuServiceError(
                "paper_template_ref_mismatch",
                f"Build supplied template ref {template_tex_ref}, but the TeX draft pins {pinned_template_ref}.",
            )
        selected_template_ref = template_tex_ref or pinned_template_ref
        snapshot_manifest_path, _template_record = self._record_file(
            selected_template_ref,
            expected={"KAOJU:PAPER-TEMPLATE-TEX"},
            allow_directory=True,
        )
        snapshot_tree = snapshot_manifest_path.parent
        snapshot_manifest = _load_tex_manifest(snapshot_tree, TEX_SNAPSHOT_MANIFEST_NAME)
        recorded_snapshot_digest = snapshot_manifest.get("stock_tree_digest")
        actual_snapshot_digest = _paper_tree_digest(snapshot_tree, excluded={TEX_SNAPSHOT_MANIFEST_NAME})
        if actual_snapshot_digest != recorded_snapshot_digest or draft_manifest.get("template_snapshot_tree_digest") != recorded_snapshot_digest:
            raise KaojuServiceError(
                "paper_template_snapshot_mismatch",
                "Pinned LaTeX snapshot bytes, snapshot manifest, and TeX draft manifest do not agree.",
            )
        entrypoint_value = draft_manifest.get("entrypoint")
        if not isinstance(entrypoint_value, str):
            raise KaojuServiceError("paper_entrypoint_missing", "TeX draft manifest has no declared entrypoint.")
        entrypoint = validate_template_relative_path(entrypoint_value)
        source_entrypoint = source_tree.joinpath(*entrypoint.parts)
        if source_entrypoint.suffix.lower() != ".tex" or not source_entrypoint.is_file():
            raise KaojuServiceError("paper_entrypoint_invalid", f"Declared TeX entrypoint is missing or invalid: {entrypoint_value}")
        build_profile = draft_manifest.get("build_profile")
        if not isinstance(build_profile, str):
            raise KaojuServiceError("paper_build_profile_missing", "TeX draft manifest has no registered build profile.")
        if toolchain is not None and toolchain != build_profile:
            raise KaojuServiceError(
                "paper_build_profile_mismatch",
                f"Requested toolchain {toolchain!r} differs from the pinned build profile {build_profile!r}.",
            )
        _audit_path, audit_record = self._record_file(audit_ref, expected={"KAOJU:AUDIT-REPORT"})
        if audit_record.get("status") != "ready":
            raise KaojuServiceError("paper_audit_not_accepted", f"Audit Report {audit_ref} is not accepted and ready; PDF build is blocked.")
        unfilled = _unfilled_obligations(source_tree, entrypoint.as_posix())
        if unfilled:
            raise KaojuServiceError(
                "paper_tex_unfilled_obligations",
                "TeX draft has unfilled composition obligations; complete the recorded agent fill before build.",
                tuple(f"{diagnostic.code} at line {diagnostic.line}: {diagnostic.message}" for diagnostic in unfilled),
            )
        drift = self.tex_status(draft_tex_ref=draft_tex_ref)
        selected, fallback = _select_tex_toolchain(build_profile)
        if selected is None:
            raise KaojuServiceError("paper_compiler_missing", "No supported TeX compiler is available.", ("Install Tectonic, latexmk, or pdflatex in the selected Topic Workspace environment.",))
        build_id = f"artifact-paper-build-run-{uuid.uuid4().hex[:12]}"
        with self._temporary_directory("paper-build-") as temporary:
            build_tree = temporary / "build"
            shutil.copytree(source_tree, build_tree)
            argv = _tex_command(selected, entrypoint.as_posix())
            request = ExecutionAdapterCommandRequest.create(extension_point="document_build", argv=argv, cwd=build_tree, timeout_seconds=timeout_seconds, recording_refs=(draft_tex_ref, selected_template_ref, build_id))
            observation = execute_command_request(request, env=command_environment(self.env))
            log_path = temporary / "compile.log"
            log_path.write_text(_compile_log(selected, fallback, observation), encoding="utf-8")
            pdf_candidates = [
                build_tree.joinpath(*entrypoint.with_suffix(".pdf").parts),
                build_tree / entrypoint.with_suffix(".pdf").name,
            ]
            pdf_path = next((candidate for candidate in pdf_candidates if candidate.is_file()), pdf_candidates[0])
            pdf_valid = pdf_path.is_file() and pdf_path.stat().st_size > 8 and pdf_path.read_bytes()[:4] == b"%PDF"
            terminal = "complete" if observation.get("status") == "succeeded" and pdf_valid else "failed"
            run_path = temporary / "paper-build-run.json"
            _write_json(run_path, _structured_payload("KAOJU:PAPER-BUILD-RUN", "Paper PDF build Run", "Immutable registered document-build attempt.", {"execution": {"command_request": observation.get("request"), "toolchain": selected, "fallback": fallback, "entrypoint": entrypoint.as_posix(), "input_refs": [draft_tex_ref, selected_template_ref]}, "result": {"terminal_status": terminal, "returncode": observation.get("returncode"), "elapsed_seconds": observation.get("elapsed_seconds"), "pdf_magic_valid": pdf_valid, "stocked_template_posture": drift.get("stocked_template_posture"), "paper_local_repair": drift.get("paper_local_repair")}}))
            run_result = self.artifacts.put("KAOJU:PAPER-BUILD-RUN", run_path, producer="isomer-kaoju-write", scope_key=paper_line, record_id=build_id, status=terminal, relationships=_relationships(paper_draft_tex=draft_tex_ref, paper_template_tex=selected_template_ref))
            log_result = self.artifacts.put("KAOJU:PAPER-COMPILE-LOG", log_path, producer="isomer-kaoju-write", scope_key=paper_line, status="ready" if terminal == "complete" else "failed", relationships=_relationships(paper_build_run=build_id))
            affected = [_record_id(run_result), _record_id(log_result)]
            if terminal != "complete":
                return {"ok": False, "mutated": True, "operation": "paper.build-pdf", "terminal_status": terminal, "entrypoint": entrypoint.as_posix(), "template_ref": selected_template_ref, "template_drift": drift, "build_run_ref": build_id, "compile_log_ref": _record_id(log_result), "command_request": observation.get("request"), "fallback": fallback, "affected_refs": affected, "recovery_actions": ["Inspect the registered compile log and classify any repair as presentation-only or material before retrying."]}
            pdf_result = self.artifacts.put("KAOJU:PAPER-PDF", pdf_path, producer="isomer-kaoju-write", scope_key=paper_line, relationships=_relationships(paper_build_run=build_id, paper_draft_tex=draft_tex_ref))
            pdf_ref = _record_id(pdf_result)
            revision_path = temporary / "paper-pdf-revision-log.json"
            repair_class = "paper-local" if drift.get("paper_local_repair") is True else "none"
            _write_json(revision_path, _structured_payload("KAOJU:PAPER-PDF-REVISION-LOG", "Paper PDF revision log", "Append-only build attempt and repair provenance.", {"builds": [{"build_run_ref": build_id, "compile_log_ref": _record_id(log_result), "pdf_ref": pdf_ref, "toolchain": selected, "fallback": fallback, "repair_class": repair_class}]}))
            revision_result = self.artifacts.put("KAOJU:PAPER-PDF-REVISION-LOG", revision_path, producer="isomer-kaoju-write", scope_key=paper_line, relationships=_relationships(paper_pdf=pdf_ref, paper_build_run=build_id))
            validation_path = temporary / "paper-validation-report.json"
            accepted = publication_approved and pdf_inspected
            verdict = "ready" if accepted else "not-ready"
            _write_json(validation_path, _structured_payload("KAOJU:PAPER-VALIDATION-REPORT", "Paper validation report", "Structural, textual, visual, evidence, and publication assessment.", {"assessment": {"verdict": verdict, "compile": "passed", "pdf_magic": "passed", "textual_inspection": "passed" if pdf_inspected else "required", "visual_inspection": "passed" if pdf_inspected else "required", "publication_gate": "approved" if publication_approved else "pending", "known_limitations": [] if pdf_inspected else ["Direct textual and visual PDF inspection remains required."]}, "quality_profile": {"audit_ref": audit_ref, "canonical_myst_required": True, "publication_accepted": accepted}}))
            validation_result = self.artifacts.put("KAOJU:PAPER-VALIDATION-REPORT", validation_path, producer="isomer-kaoju-write", scope_key=paper_line, status="ready" if accepted else "blocked", relationships=_relationships(paper_build_run=build_id, paper_pdf=pdf_ref, audit_report=audit_ref))
            affected.extend([pdf_ref, _record_id(revision_result), _record_id(validation_result)])
        accepted = publication_approved and pdf_inspected
        return {"ok": True, "mutated": True, "operation": "paper.build-pdf", "terminal_status": "complete", "entrypoint": entrypoint.as_posix(), "template_ref": selected_template_ref, "template_drift": drift, "pdf_inspection": "passed" if pdf_inspected else "required", "publication_gate": "approved" if publication_approved else "pending", "accepted": accepted, "build_run_ref": build_id, "compile_log_ref": _record_id(log_result), "pdf_ref": pdf_ref, "revision_log_ref": _record_id(revision_result), "validation_ref": _record_id(validation_result), "command_request": observation.get("request"), "fallback": fallback, "affected_refs": affected}

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
        if not member.is_file():
            return {}
        return _load_json(member)

    def _bibliography_entries(self, citation_refs: Sequence[str]) -> list[dict[str, object]]:
        entries: list[dict[str, object]] = []
        missing: list[str] = []
        for ref in citation_refs:
            path, _record = self._record_file(ref, expected={"KAOJU:CITATION-MAP"})
            payload = _load_json(path)
            sections = payload.get("sections")
            citations = sections.get("citations") if isinstance(sections, dict) else None
            if not isinstance(citations, list):
                raise KaojuServiceError("paper_citation_map_invalid", f"Citation map {ref} has no sections.citations list.")
            for entry in citations:
                if not isinstance(entry, dict):
                    continue
                key = entry.get("cite_key")
                if not isinstance(key, str) or not key.strip():
                    continue
                title = entry.get("title")
                identity = entry.get("source_identity")
                if not isinstance(title, str) or not title.strip() or not isinstance(identity, str) or not identity.strip():
                    missing.append(key)
                    continue
                entries.append(
                    {
                        "cite_key": key,
                        "title": title,
                        "source_identity": identity,
                        "source_digest_ref": entry.get("source_digest_ref"),
                        "citation_map_ref": ref,
                    }
                )
        if missing:
            raise KaojuServiceError(
                "paper_citation_metadata_missing",
                f"Citation-map entries lack usable bibliographic metadata (title and source identity): {', '.join(sorted(set(missing)))}.",
                ("Record title and source identity for the affected keys in the citation map before TeX composition.",),
            )
        return entries

    @contextmanager
    def _temporary_directory(self, prefix: str) -> Iterator[Path]:
        root = self.context.topic_workspace_path / "tmp" / "kaoju-service"
        root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix=prefix, dir=root) as raw:
            yield Path(raw)


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


def _digest_json(value: Mapping[str, object]) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def myst_parser_version() -> str:
    try:
        return metadata.version("myst-parser")
    except metadata.PackageNotFoundError:  # pragma: no cover
        return "unknown"
