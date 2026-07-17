"""Authored-metadata and LaTeX composition validation for named templates."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Mapping

from isomer_labs.kaoju.artifacts import KaojuServiceError
from isomer_labs.kaoju.template_support import (
    TemplateKindSpec,
    _AUTHORED_METADATA_KEYS,
    template_tree_digest,
    validate_template_relative_path,
)


def validate_authored_metadata(
    value: Mapping[str, object],
    *,
    root: Path,
    template_kind: TemplateKindSpec,
    allow_internal_manifest: bool = False,
) -> dict[str, object]:
    unknown = sorted(set(value) - _AUTHORED_METADATA_KEYS)
    if unknown:
        raise KaojuServiceError("template_metadata_unknown", f"Template authored metadata contains unsupported fields: {', '.join(unknown)}")
    result: dict[str, object] = {}
    entrypoint = value.get("entrypoint")
    if entrypoint is not None:
        if not isinstance(entrypoint, str):
            raise KaojuServiceError("template_entrypoint_invalid", "Template entrypoint metadata must be a safe relative file path.")
        relative = validate_template_relative_path(entrypoint)
        candidate = root.joinpath(*relative.parts)
        if not candidate.is_file() or candidate.is_symlink():
            raise KaojuServiceError("template_entrypoint_missing", f"Template entrypoint does not exist in the prepared tree: {entrypoint}")
        result["entrypoint"] = relative.as_posix()
    guidance = value.get("use_guidance")
    if guidance is not None:
        if not isinstance(guidance, str) or not guidance.strip() or len(guidance) > 20_000:
            raise KaojuServiceError("template_use_guidance_invalid", "Template use guidance must be a non-empty string of at most 20,000 characters.")
        result["use_guidance"] = guidance
    extensions = value.get("extensions")
    if extensions is not None:
        if not isinstance(extensions, dict):
            raise KaojuServiceError("template_extensions_invalid", "Template extension metadata must be a JSON object.")
        encoded = json.dumps(extensions, sort_keys=True, ensure_ascii=False)
        if len(encoded.encode("utf-8")) > 64 * 1024:
            raise KaojuServiceError("template_extensions_too_large", "Template extension metadata exceeds 64 KiB.")
        result["extensions"] = dict(extensions)
    if template_kind.requires_latex_contract:
        _validate_latex_contract(result, root=root)
    if allow_internal_manifest:
        template_tree_digest(root, allow_internal_manifest=True)
    return result


def _validate_latex_contract(metadata: Mapping[str, object], *, root: Path) -> None:
    entrypoint_value = metadata.get("entrypoint")
    if not isinstance(entrypoint_value, str):
        raise KaojuServiceError(
            "latex_template_entrypoint_required",
            "LaTeX template metadata requires an entrypoint.",
        )
    entrypoint = root.joinpath(*validate_template_relative_path(entrypoint_value).parts)
    if entrypoint.suffix.lower() != ".tex":
        raise KaojuServiceError("latex_template_entrypoint_invalid", "LaTeX template entrypoint must be a .tex file.")
    extensions = metadata.get("extensions")
    latex = extensions.get("latex") if isinstance(extensions, dict) else None
    if not isinstance(latex, dict):
        raise KaojuServiceError(
            "latex_template_contract_required",
            "LaTeX template metadata requires an extensions.latex composition contract.",
        )
    mode = latex.get("composition_mode")
    if mode not in {"preamble", "marker", "include"}:
        raise KaojuServiceError(
            "latex_template_composition_mode_invalid",
            "LaTeX composition_mode must be preamble, marker, or include.",
        )
    build_profile = latex.get("build_profile")
    if build_profile not in {"tectonic", "latexmk", "pdflatex"}:
        raise KaojuServiceError(
            "latex_template_build_profile_invalid",
            "LaTeX build_profile must be tectonic, latexmk, or pdflatex.",
        )
    source_provenance = latex.get("source_provenance")
    if not isinstance(source_provenance, (str, dict)) or not source_provenance:
        raise KaojuServiceError(
            "latex_template_source_provenance_required",
            "LaTeX composition metadata requires non-empty source_provenance.",
        )
    license_posture = latex.get("license_posture")
    if not isinstance(license_posture, str) or not license_posture.strip():
        raise KaojuServiceError(
            "latex_template_license_posture_required",
            "LaTeX composition metadata requires a non-empty license_posture.",
        )
    text = entrypoint.read_text(encoding="utf-8")
    if mode == "preamble":
        if "\\begin{document}" in text or "\\end{document}" in text:
            raise KaojuServiceError(
                "latex_template_preamble_invalid",
                "A preamble-mode entrypoint must be a preamble fragment without a document body.",
            )
        generated = latex.get("generated_entrypoint", "main.tex")
        if not isinstance(generated, str):
            raise KaojuServiceError("latex_template_generated_entrypoint_invalid", "generated_entrypoint must be a safe .tex path.")
        generated_path = validate_template_relative_path(generated)
        if generated_path.suffix.lower() != ".tex" or generated_path.as_posix() == entrypoint_value:
            raise KaojuServiceError(
                "latex_template_generated_entrypoint_invalid",
                "generated_entrypoint must be a safe .tex path distinct from the preamble entrypoint.",
            )
    elif mode == "marker":
        marker = latex.get("marker")
        if not isinstance(marker, str) or not marker:
            raise KaojuServiceError("latex_template_marker_required", "Marker composition requires a non-empty marker string.")
        if text.count(marker) != 1:
            raise KaojuServiceError("latex_template_marker_invalid", "The LaTeX entrypoint must contain the declared marker exactly once.")
        _require_complete_latex_document(text)
    else:
        body_path = latex.get("body_path")
        if not isinstance(body_path, str):
            raise KaojuServiceError("latex_template_body_path_required", "Include composition requires a safe body_path.")
        relative_body = validate_template_relative_path(body_path)
        if relative_body.suffix.lower() != ".tex" or relative_body.as_posix() == entrypoint_value:
            raise KaojuServiceError("latex_template_body_path_invalid", "body_path must be a safe .tex path distinct from the entrypoint.")
        body_stem = relative_body.as_posix()[:-4]
        accepted_includes = {
            f"\\input{{{relative_body.as_posix()}}}",
            f"\\input{{{body_stem}}}",
            f"\\include{{{body_stem}}}",
        }
        if not any(include in text for include in accepted_includes):
            raise KaojuServiceError(
                "latex_template_body_include_missing",
                "The LaTeX entrypoint does not include the declared generated body path.",
            )
        _require_complete_latex_document(text)


def _require_complete_latex_document(text: str) -> None:
    if "\\begin{document}" not in text or "\\end{document}" not in text:
        raise KaojuServiceError(
            "latex_template_document_incomplete",
            "Marker and include composition entrypoints must contain a complete LaTeX document.",
        )
