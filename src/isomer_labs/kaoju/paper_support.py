"""Composition, manifest, and build helpers for Kaoju paper production."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from importlib import metadata
import json
from pathlib import Path
import re
import shutil
from typing import Mapping, Sequence

import yaml  # type: ignore[import-untyped]

from isomer_labs.kaoju.artifacts import KaojuServiceError
from isomer_labs.kaoju.content import DIRECTORY_MANIFEST_NAME
from isomer_labs.kaoju.contracts import load_binding_registry
from isomer_labs.kaoju.template_support import (
    TemplateSelection,
    TemplateState,
    validate_template_relative_path,
)
from isomer_labs.kaoju.template_validation import _VENUE_CONTRACTS


FRONTMATTER_RE = re.compile(r"\A---[ \t]*\n(.*?)\n---[ \t]*(?:\n|\Z)", re.S)


def myst_parser_version() -> str:
    """Return the installed MyST parser version for recorded provenance."""

    try:
        return metadata.version("myst-parser")
    except metadata.PackageNotFoundError:  # pragma: no cover
        return "unknown"


def _line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _digest_json(value: Mapping[str, object]) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


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


def _normalize_heading(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()


def _extract_frontmatter(text: str) -> tuple[dict[str, object], str]:
    """Split a leading MyST YAML frontmatter block from the body."""

    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    try:
        parsed = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        parsed = None
    frontmatter = parsed if isinstance(parsed, dict) else {}
    return dict(frontmatter), text[match.end():]


def _extract_abstract(body: str) -> tuple[str | None, str]:
    """Remove the Abstract section from the body and return its text."""

    lines = body.splitlines()
    start: int | None = None
    end = len(lines)
    for index, line in enumerate(lines):
        heading = re.fullmatch(r"(#{1,6})\s+(.+)", line)
        if not heading:
            continue
        if start is None:
            if _normalize_heading(heading.group(2)) == "abstract":
                start = index
            continue
        end = index
        break
    if start is None:
        return None, body
    abstract_lines = [line for line in lines[start + 1 : end] if line.strip()]
    abstract = "\n".join(abstract_lines).strip() or None
    remaining = lines[:start] + lines[end:]
    return abstract, "\n".join(remaining).strip("\n") + "\n"


def _strip_title_heading(body: str, title: str) -> str:
    """Remove a redundant Title heading and a paragraph repeating the frontmatter title."""

    lines = body.splitlines()
    for index, line in enumerate(lines):
        if not line.strip():
            continue
        heading = re.fullmatch(r"(#{1,6})\s+(.+)", line)
        if heading is None or _normalize_heading(heading.group(2)) != "title":
            return body
        del lines[index]
        break
    if title:
        normalized_title = _normalize_heading(title)
        for index, line in enumerate(lines):
            if not line.strip():
                continue
            if _normalize_heading(line) == normalized_title:
                del lines[index]
            break
    return "\n".join(lines).strip("\n") + "\n"


def _fill_obligations(
    *,
    frontmatter_title: str,
    frontmatter_authors: str,
    abstract_text: str | None,
    bibliography: list[dict[str, object]],
    conversion_diagnostics: Sequence[PaperDiagnostic],
    latex_contract: Mapping[str, object],
    entrypoint: str,
) -> list[dict[str, object]]:
    venue = latex_contract.get("venue")
    venue_spec = _VENUE_CONTRACTS.get(venue) if isinstance(venue, str) else None
    obligations: list[dict[str, object]] = [
        {
            "id": "title",
            "kind": "frontmatter-title",
            "status": "pending" if frontmatter_title else "blocked",
            "value": frontmatter_title or None,
            "tex_target": entrypoint,
            "detail": "Fill the venue title command from the MyST frontmatter title.",
        },
        {
            "id": "authors",
            "kind": "frontmatter-authors",
            "status": "pending" if frontmatter_authors else "blocked",
            "value": frontmatter_authors or None,
            "tex_target": entrypoint,
            "detail": "Fill the venue author block from the MyST frontmatter authors.",
        },
        {
            "id": "abstract",
            "kind": "abstract-environment",
            "status": "pending" if abstract_text else "blocked",
            "value": abstract_text,
            "tex_target": entrypoint,
            "detail": "Move the MyST abstract into the venue abstract environment.",
        },
        {
            "id": "keywords",
            "kind": "keywords-environment",
            "status": "pending",
            "value": None,
            "tex_target": entrypoint,
            "detail": "Add venue keywords consistent with the MyST content.",
        },
        {
            "id": "bibliography",
            "kind": "bibliography",
            "status": "pending" if bibliography else "blocked",
            "entries": bibliography,
            "tex_target": entrypoint,
            "detail": "Materialize the venue bibliography from citation-map entries so every \\cite key resolves.",
        },
    ]
    if venue_spec is not None:
        obligations.append(
            {
                "id": "venue-constructs",
                "kind": "venue-constructs",
                "status": "pending",
                "venue": venue,
                "constructs": list(venue_spec[1]),
                "tex_target": entrypoint,
                "detail": "Apply the declared venue's title, author, abstract, and keywords constructs.",
            }
        )
    table_lines = [diagnostic.line for diagnostic in conversion_diagnostics if diagnostic.code == "tex_repair_table"]
    if table_lines:
        obligations.append(
            {
                "id": "tables",
                "kind": "tables",
                "status": "pending",
                "source_lines": table_lines,
                "tex_target": entrypoint,
                "detail": "Convert each marked Markdown table into a real venue table; wording and numbers stay identical to MyST.",
            }
        )
    directive_lines = [diagnostic.line for diagnostic in conversion_diagnostics if diagnostic.code == "tex_repair_directive"]
    if directive_lines:
        obligations.append(
            {
                "id": "directives",
                "kind": "directives",
                "status": "pending",
                "source_lines": directive_lines,
                "tex_target": entrypoint,
                "detail": "Review each simplified MyST directive and map it to the appropriate venue environment.",
            }
        )
    return obligations


PLACEHOLDER_RE = re.compile(r"\{\{([a-zA-Z0-9_.:-]+)\}\}")
CITATION_RE = re.compile(r"\{cite(?::[a-z]+)?\}`([^`]+)`")


def _myst_to_tex(text: str) -> tuple[str, list[PaperDiagnostic]]:
    diagnostics: list[PaperDiagnostic] = []
    output: list[str] = []
    in_directive = False
    for line_number, line in enumerate(text.splitlines(), start=1):
        heading = re.fullmatch(r"(#{1,6})\s+(.+)", line)
        if heading:
            level = len(heading.group(1))
            command = "section" if level == 1 else "subsection" if level == 2 else "subsubsection"
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


def _tex_escape(value: str, *, preserve_commands: bool = False) -> str:
    replacements = {"&": "\\&", "%": "\\%", "$": "\\$", "#": "\\#", "_": "\\_", "~": "\\textasciitilde{}", "^": "\\textasciicircum{}"}
    if not preserve_commands:
        replacements.update({"\\": "\\textbackslash{}", "{": "\\{", "}": "\\}"})
    return "".join(replacements.get(character, character) for character in value)


def _unfilled_obligations(tree: Path, entrypoint: str) -> list[PaperDiagnostic]:
    """Scan composed TeX for mechanical pass-through signatures that block build readiness."""

    if not entrypoint:
        return []
    entry_path = tree.joinpath(*validate_template_relative_path(entrypoint).parts)
    if not entry_path.is_file():
        return []
    text = entry_path.read_text(encoding="utf-8")
    diagnostics: list[PaperDiagnostic] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if re.fullmatch(r"---\s*", line):
            diagnostics.append(PaperDiagnostic("tex_unfilled_frontmatter", "Raw MyST frontmatter remains in the composed TeX body.", line_number, severity="warning"))
        if line.startswith("% ISOMER_FILL"):
            diagnostics.append(PaperDiagnostic("tex_unfilled_marker", "Fill marker remains; resolve it against the MyST content and remove it.", line_number, severity="warning"))
        if line.startswith("% ISOMER_REPAIR_TABLE"):
            diagnostics.append(PaperDiagnostic("tex_unfilled_table", "Markdown table is still marked for repair instead of being a real venue table.", line_number, severity="warning"))
    if re.search(r"\\title\{(?:\s*|Survey Paper)\}", text):
        diagnostics.append(PaperDiagnostic("tex_unfilled_title", "The venue title is still a placeholder; fill it from the MyST frontmatter.", 1, severity="warning"))
    if re.search(r"\\author\{\s*\}", text):
        diagnostics.append(PaperDiagnostic("tex_unfilled_author", "The venue author block is still empty; fill it from the MyST frontmatter.", 1, severity="warning"))
    venue_section = re.search(r"\\section\{(Title|Abstract)\}", text)
    if venue_section:
        diagnostics.append(PaperDiagnostic("tex_unfilled_venue_section", f"Section '{venue_section.group(1)}' is a MyST scaffold heading, not venue structure; map it to the venue title or abstract constructs.", 1, severity="warning"))
    tex_texts = [path.read_text(encoding="utf-8") for path in sorted(tree.rglob("*.tex")) if path.is_file()]
    if any("\\cite{" in content for content in tex_texts) and not any("\\bibliography" in content or "thebibliography" in content for content in tex_texts):
        diagnostics.append(PaperDiagnostic("tex_unfilled_bibliography", "Citations are present but no bibliography exists; materialize it from the citation map.", 1, severity="warning"))
    return diagnostics


def _latex_state_identity(
    state: TemplateState | TemplateSelection,
) -> dict[str, object]:
    if isinstance(state, TemplateSelection):
        return {
            "kind": "latex",
            **state.to_json(),
        }
    return {
        "kind": "latex",
        "name": state.name,
        "selection_source": "topic-stock",
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
    frontmatter: Mapping[str, object] | None = None,
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
        title, authors = _frontmatter_title_authors(frontmatter)
        generated.write_text(
            preamble
            + f"% ISOMER_FILL_TITLE: {_single_line(title) or 'missing from MyST frontmatter'}\n"
            + f"% ISOMER_FILL_AUTHORS: {_single_line(authors) or 'missing from MyST frontmatter'}\n"
            + "\\title{}\n"
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


def _frontmatter_title_authors(frontmatter: Mapping[str, object] | None) -> tuple[str, str]:
    if not isinstance(frontmatter, Mapping):
        return "", ""
    title = frontmatter.get("title")
    authors_value = frontmatter.get("authors")
    names: list[str] = []
    if isinstance(authors_value, list):
        for entry in authors_value:
            if isinstance(entry, Mapping) and isinstance(entry.get("name"), str):
                names.append(entry["name"])
            elif isinstance(entry, str):
                names.append(entry)
    elif isinstance(authors_value, str):
        names.append(authors_value)
    return (title if isinstance(title, str) else ""), ", ".join(names)


def _single_line(value: str) -> str:
    return " ".join(value.split())


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
