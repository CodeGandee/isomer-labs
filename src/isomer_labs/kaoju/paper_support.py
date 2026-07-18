"""Composition, manifest, and build helpers for Kaoju paper production."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
from typing import Mapping

from isomer_labs.kaoju.artifacts import KaojuServiceError
from isomer_labs.kaoju.content import DIRECTORY_MANIFEST_NAME
from isomer_labs.kaoju.contracts import load_binding_registry
from isomer_labs.kaoju.template_support import TemplateState, validate_template_relative_path


def _latex_state_identity(state: TemplateState) -> dict[str, object]:
    return {
        "kind": "latex",
        "name": state.name,
        "stable_ref": state.record.id,
        "state_token": state.state_token,
        "tree_digest": state.tree_digest,
        "authored_metadata": state.authored_metadata,
    }


def _compose_latex_tree(
    root: Path,
    *,
    stock_entrypoint: str,
    contract: Mapping[str, object],
    converted_body: str,
) -> str:
    entrypoint_path = validate_template_relative_path(stock_entrypoint)
    entrypoint = root.joinpath(*entrypoint_path.parts)
    mode = contract.get("composition_mode")
    if mode == "preamble":
        generated_value = contract.get("generated_entrypoint", "main.tex")
        if not isinstance(generated_value, str):
            raise KaojuServiceError("latex_template_generated_entrypoint_invalid", "generated_entrypoint must be a safe .tex path.")
        generated_path = validate_template_relative_path(generated_value)
        generated = root.joinpath(*generated_path.parts)
        generated.parent.mkdir(parents=True, exist_ok=True)
        preamble = entrypoint.read_text(encoding="utf-8").rstrip() + "\n"
        generated.write_text(
            preamble
            + "\\title{Survey Paper}\n"
            + "\\author{}\n"
            + "\\begin{document}\n"
            + "\\maketitle\n"
            + converted_body
            + "\\end{document}\n",
            encoding="utf-8",
        )
        return generated_path.as_posix()
    if mode == "marker":
        marker = contract.get("marker")
        if not isinstance(marker, str) or entrypoint.read_text(encoding="utf-8").count(marker) != 1:
            raise KaojuServiceError("latex_template_marker_invalid", "The LaTeX entrypoint does not contain its declared marker exactly once.")
        entrypoint.write_text(entrypoint.read_text(encoding="utf-8").replace(marker, converted_body), encoding="utf-8")
        return entrypoint_path.as_posix()
    if mode == "include":
        body_value = contract.get("body_path")
        if not isinstance(body_value, str):
            raise KaojuServiceError("latex_template_body_path_required", "Include composition requires a safe body_path.")
        body_path = validate_template_relative_path(body_value)
        body = root.joinpath(*body_path.parts)
        body.parent.mkdir(parents=True, exist_ok=True)
        body.write_text(converted_body, encoding="utf-8")
        return entrypoint_path.as_posix()
    raise KaojuServiceError("latex_template_composition_mode_invalid", "Unsupported LaTeX composition mode.")


def _paper_tree_digest(root: Path, *, excluded: set[str]) -> str:
    digest = hashlib.sha256()
    member_count = 0
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            raise KaojuServiceError("paper_tree_symlink_forbidden", f"Paper TeX trees cannot contain symbolic links: {relative}")
        if not path.is_file() or relative in excluded or relative == DIRECTORY_MANIFEST_NAME:
            continue
        encoded_path = relative.encode("utf-8")
        digest.update(len(encoded_path).to_bytes(8, "big"))
        digest.update(encoded_path)
        size = path.stat().st_size
        digest.update(size.to_bytes(8, "big"))
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        member_count += 1
    if member_count == 0:
        raise KaojuServiceError("paper_tree_empty", "Paper TeX tree contains no files.")
    return f"sha256:{digest.hexdigest()}"


def _tree_files(root: Path) -> list[str]:
    return sorted(
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and path.relative_to(root).as_posix() != DIRECTORY_MANIFEST_NAME
    )


def _load_tex_manifest(root: Path, preferred_name: str) -> dict[str, object]:
    preferred = root / preferred_name
    if preferred.is_file():
        return _load_json(preferred)
    legacy = root / "manifest.json"
    if legacy.is_file():
        return _load_json(legacy)
    raise KaojuServiceError("paper_manifest_missing", f"Paper TeX tree has no {preferred_name} manifest.")


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


def _tex_command(toolchain: str, entrypoint: str) -> tuple[str, ...]:
    if toolchain == "tectonic":
        return ("tectonic", "--keep-logs", "--synctex", entrypoint)
    if toolchain == "latexmk":
        return ("latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", entrypoint)
    return ("pdflatex", "-interaction=nonstopmode", "-halt-on-error", entrypoint)


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
