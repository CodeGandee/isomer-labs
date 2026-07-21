"""Kaoju derived-intent Mindset Sources and Run-scoped Mindset Records."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from hashlib import sha256
from html import escape
from importlib.resources import files
import json
import os
from pathlib import Path
import re
from typing import Any, Callable, Mapping, Sequence
import uuid

from jsonschema import Draft202012Validator  # type: ignore[import-untyped]

from isomer_labs.models import EffectiveTopicContext
from isomer_labs.workspace.path_resolution import resolve_semantic_path


SOURCE_SCHEMA_VERSION = "isomer-kaoju-mindset-source.v1"
SOURCE_SEMANTIC_LABEL = "topic.intent.kaoju_mindsets"
SOURCE_SCHEMA_RESOURCE = "resources/mindset-source.v1.schema.json"
RECORD_SEMANTIC_ID = "KAOJU:MINDSET-RECORD"
DEFAULT_KEYS = ("paper.deep-dive", "paper.skimming", "source-code.ingest")
KEY_RE = re.compile(r"^[a-z0-9]+(?:[.-][a-z0-9]+)*$")
SHA256_RE = re.compile(r"^[a-f0-9]{64}$")
MAX_SOURCE_BYTES = 128 * 1024
MAX_RECORD_BYTES = 1024 * 1024
COLLECTOR_ID = "additional-questions"
COLLECTOR_PROMPT = "Did the user explicitly assign any additional questions to this Mindset Record that the fixed Mindset Source questions do not cover?"
COLLECTOR_ANSWER_EXPECTATION = "Register only questions explicitly targeted to the Mindset Record. Save ordinary paper or source-code questions and findings in the applicable reading Artifacts. If no additional questions were explicitly assigned, record none."
EXPECTED_DEFAULT_QUESTIONS = {
    "paper.deep-dive": (
        ("survey-role", "How does this paper relate to the active survey question, accepted boundary, and selected direction, and what role could it play in the survey?"),
        ("survey-relevant-claims", "Which of the paper's claims directly answer, support, challenge, refine, or fall outside the active survey question?"),
        ("portfolio-novelty", "Relative to works already represented in the survey, what is genuinely new, duplicative, complementary, or contradictory?"),
        ("comparison-mechanism", "Which mechanisms, assumptions, definitions, and method components matter to the survey's comparison dimensions?"),
        ("survey-claim-evidence", "Which exact sections, equations, figures, tables, or appendices support or challenge the survey-relevant claims, and what is my interpretation rather than a source statement?"),
        ("evaluation-transferability", "Do the datasets, metrics, baselines, controls, and ablations test the claims under conditions that fit the survey's scope and intended comparisons?"),
        ("boundary-limitations", "Which limitations, failure modes, contradictions, missing implementation details, or reproducibility gaps restrict how this paper can be used in the survey?"),
        ("survey-update-and-gaps", "What updates to the survey taxonomy, comparison structure, Claim-Evidence Ledger, or reading path should I recommend, and which survey questions remain unresolved?"),
    ),
    "paper.skimming": (
        ("survey-fit", "What exact work and version am I inspecting, and how does it fit the active survey question, boundary, and selected direction?"),
        ("topic-relevant-claim", "What survey-relevant problem and principal claim can I establish at the inspection depth actually achieved?"),
        ("portfolio-relation", "Does this work add a new contribution, duplicate known work, complement a current category, or challenge an existing survey claim?"),
        ("survey-evidence-signal", "What is the strongest visible evidence relevant to the survey, where is it located, and what evidence depth have I actually achieved?"),
        ("scope-and-credibility-risk", "Which assumptions, evaluation settings, missing comparisons, contradictions, or identity and access uncertainties limit its relevance to this survey?"),
        ("survey-triage", "What survey disposition should I recommend: deep dive, defer, or exclude from the current boundary, what gap would it fill, and what must be verified first?"),
    ),
    "source-code.ingest": (
        ("survey-role-and-identity", "How does this exact repository revision relate to the active survey question, selected direction, and associated works, and what are its source, license, and access posture?"),
        ("survey-relevant-architecture", "Which entrypoints and modules implement the concepts, methods, data paths, or evaluators that matter to the survey?"),
        ("claim-code-map", "Which survey-relevant paper claims, equations, or algorithms map to exact files and symbols, and what remains unmatched?"),
        ("behavior-path", "How do inputs, preprocessing, method logic, evaluation, and outputs connect for the behavior relevant to the survey?"),
        ("comparison-sensitive-configuration", "Which defaults, flags, seeds, thresholds, dependencies, hardware, datasets, or services could change the survey's interpretation or comparison?"),
        ("survey-evidence-surfaces", "What do tests, examples, benchmarks, and existing logs establish about the survey-relevant claims without executing the repository?"),
        ("paper-code-divergence", "What is missing, stale, stubbed, inconsistent, or divergent from the associated paper or the role assigned to this source in the survey?"),
        ("survey-readiness-and-risks", "What further source inspection, environment preparation, bounded trial, or reproduction should I recommend for the survey, and what blockers, side effects, or resource risks qualify that recommendation?"),
    ),
}


@dataclass(frozen=True)
class MindsetDiagnostic:
    """One stable Mindset Source or Record diagnostic."""

    code: str
    message: str
    location: str
    severity: str = "error"

    def to_json(self) -> dict[str, str]:
        return {
            "code": self.code,
            "message": self.message,
            "location": self.location,
            "severity": self.severity,
        }


def mindset_source_child(root: Path, mindset_key: str) -> Path:
    """Resolve one deterministic direct-child Source path without scanning."""

    if len(mindset_key) > 80 or KEY_RE.fullmatch(mindset_key) is None:
        raise ValueError("Mindset key must use lowercase alphanumerics separated by dots or hyphens.")
    selected_root = root.resolve(strict=False)
    child = (selected_root / f"{mindset_key}.json").resolve(strict=False)
    if child.parent != selected_root:
        raise ValueError("Mindset Source must be a direct child of the resolved semantic root.")
    return child


def canonical_digest(value: Mapping[str, Any]) -> str:
    """Return a deterministic semantic digest for JSON data."""

    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256(encoded).hexdigest()


def file_digest(path: Path) -> str:
    """Return the exact byte digest for an intent or Source file."""

    return sha256(path.read_bytes()).hexdigest()


def load_mindset_source(path: Path, *, expected_key: str | None = None) -> tuple[dict[str, Any] | None, list[MindsetDiagnostic]]:
    """Load and validate one directly editable Mindset Source."""

    try:
        raw_bytes = path.read_bytes()
    except OSError as exc:
        return None, [MindsetDiagnostic("mindset_source_unreadable", str(exc), str(path))]
    if len(raw_bytes) > MAX_SOURCE_BYTES:
        return None, [MindsetDiagnostic("mindset_source_too_large", f"Mindset Source exceeds {MAX_SOURCE_BYTES} bytes.", str(path))]
    try:
        raw = json.loads(raw_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        return None, [MindsetDiagnostic("mindset_source_json_invalid", str(exc), str(path))]
    diagnostics = mindset_source_diagnostics(raw, filename=path.name, expected_key=expected_key, serialized_size=len(raw_bytes))
    return (raw if isinstance(raw, dict) else None), diagnostics


def mindset_source_diagnostics(
    raw: object,
    *,
    filename: str | None = None,
    expected_key: str | None = None,
    serialized_size: int | None = None,
) -> list[MindsetDiagnostic]:
    """Validate the closed, bounded, non-Artifact Mindset Source contract."""

    diagnostics: list[MindsetDiagnostic] = []
    if serialized_size is not None and serialized_size > MAX_SOURCE_BYTES:
        diagnostics.append(MindsetDiagnostic("mindset_source_too_large", f"Mindset Source exceeds {MAX_SOURCE_BYTES} bytes.", "<root>"))
    schema = _load_json_resource(SOURCE_SCHEMA_RESOURCE)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(raw),
        key=lambda error: (tuple(str(part) for part in error.path), error.message),
    )
    diagnostics.extend(
        MindsetDiagnostic(
            "mindset_source_schema_invalid",
            error.message,
            "/".join(str(part) for part in error.path) or "<root>",
        )
        for error in errors
    )
    if not isinstance(raw, dict):
        return diagnostics
    key = raw.get("mindset_key")
    if filename is not None and isinstance(key, str) and filename != f"{key}.json":
        diagnostics.append(MindsetDiagnostic("mindset_source_filename_mismatch", f"Filename must be {key}.json.", "mindset_key"))
    if expected_key is not None and key != expected_key:
        diagnostics.append(MindsetDiagnostic("mindset_source_key_mismatch", f"mindset_key must be {expected_key!r}.", "mindset_key"))
    question_ids: list[str] = []
    questions = raw.get("questions")
    if isinstance(questions, list):
        for index, question in enumerate(questions):
            if not isinstance(question, dict):
                continue
            question_ids.append(str(question.get("question_id")))
            if "repeatable" in question:
                diagnostics.append(MindsetDiagnostic("mindset_fixed_question_repeatable_forbidden", "Only the additional-question collector may declare repeatable.", f"questions/{index}/repeatable"))
    collector = raw.get("additional_question_collector")
    if isinstance(collector, dict):
        question_ids.append(str(collector.get("question_id")))
        if collector.get("prompt") != COLLECTOR_PROMPT:
            diagnostics.append(MindsetDiagnostic("mindset_collector_prompt_invalid", "Collector prompt does not match the checked contract.", "additional_question_collector/prompt"))
        if collector.get("answer_expectation") != COLLECTOR_ANSWER_EXPECTATION:
            diagnostics.append(MindsetDiagnostic("mindset_collector_answer_invalid", "Collector answer expectation does not match the checked contract.", "additional_question_collector/answer_expectation"))
    duplicates = sorted({item for item in question_ids if question_ids.count(item) > 1})
    if duplicates:
        diagnostics.append(MindsetDiagnostic("mindset_question_id_duplicate", f"Question ids must be unique: {', '.join(duplicates)}.", "questions"))
    for location, key_name in _walk_keys(raw):
        normalized = key_name.lower().replace("-", "_")
        if normalized in {"command", "commands", "tool", "tools", "workflow_stage", "gate", "provider_payload", "system_prompt", "instruction_priority", "authority"}:
            diagnostics.append(MindsetDiagnostic("mindset_authority_field_forbidden", f"Mindset Source cannot declare authority-bearing field {key_name!r}.", location))
    return sorted({(item.code, item.message, item.location, item.severity): item for item in diagnostics}.values(), key=lambda item: (item.location, item.code, item.message))


def packaged_default_root() -> Path:
    """Return the installed protected skill's read-only seed root."""

    return Path(str(files("isomer_labs").joinpath(
        "assets/system_skills/research-paradigm/kaoju/isomer-ext-kaoju-entrypoint/subskills/"
        "isomer-kaoju-topic-creator/assets/defaults/mindsets"
    )))


def validate_packaged_defaults(*, process: Mapping[str, Any] | None = None) -> list[MindsetDiagnostic]:
    """Validate seed identity, inventory, collector, and checked process coverage."""

    root = packaged_default_root()
    diagnostics: list[MindsetDiagnostic] = []
    seen: set[str] = set()
    sources: dict[str, dict[str, Any]] = {}
    expected_filenames = {f"{key}.json" for key in DEFAULT_KEYS}
    actual_filenames = {path.name for path in root.iterdir() if path.is_file()}
    if actual_filenames != expected_filenames:
        diagnostics.append(
            MindsetDiagnostic(
                "mindset_seed_file_inventory_invalid",
                f"Packaged default filenames must be exactly: {', '.join(sorted(expected_filenames))}.",
                str(root),
            )
        )
    for key in DEFAULT_KEYS:
        path = mindset_source_child(root, key)
        source, source_diagnostics = load_mindset_source(path, expected_key=key)
        diagnostics.extend(source_diagnostics)
        if source is None or source_diagnostics:
            continue
        seen.add(str(source["mindset_key"]))
        sources[key] = source
        questions = source["questions"]
        observed_questions = tuple((str(item.get("question_id")), str(item.get("prompt"))) for item in questions if isinstance(item, dict))
        if observed_questions != EXPECTED_DEFAULT_QUESTIONS[key]:
            diagnostics.append(MindsetDiagnostic("mindset_seed_questions_invalid", f"{key} question ids, order, or exact prompts differ from the checked inventory.", str(path)))
        for index, question in enumerate([*questions, source["additional_question_collector"]]):
            if question.get("additional_notes") != "":
                diagnostics.append(MindsetDiagnostic("mindset_seed_notes_not_empty", "Packaged default additional_notes must be empty.", f"{path}/questions/{index}"))
        canonical_digest(source)
    if seen != set(DEFAULT_KEYS):
        diagnostics.append(MindsetDiagnostic("mindset_seed_inventory_invalid", "Packaged default keys are incomplete or duplicated.", str(root)))
    if process is not None:
        mindset_config = process.get("mindsets")
        routes = mindset_config.get("routes") if isinstance(mindset_config, dict) else None
        route_items = [item for item in routes if isinstance(item, dict)] if isinstance(routes, list) else []
        route_keys = [str(item.get("mindset_key")) for item in route_items]
        if len(route_items) != len(DEFAULT_KEYS) or set(route_keys) != set(DEFAULT_KEYS):
            diagnostics.append(MindsetDiagnostic("mindset_process_route_mismatch", "Checked process routes must cover every packaged default key exactly.", "mindsets.routes"))
        for index, route in enumerate(route_items):
            key = str(route.get("mindset_key"))
            source = sources.get(key)
            if source is None:
                continue
            applicability = source.get("applicability")
            expected = {field: route.get(field) for field in ("actions", "source_kinds", "depths")}
            if applicability != expected:
                diagnostics.append(
                    MindsetDiagnostic(
                        "mindset_process_applicability_mismatch",
                        f"Checked process route applicability differs from packaged default {key!r}.",
                        f"mindsets.routes/{index}",
                    )
                )
    return diagnostics


def render_mindset_source(source: Mapping[str, Any], *, path: Path | None = None, packaged_seed: bool = False) -> str:
    """Render escaped Source data without registering an Artifact."""

    kind = "Packaged Seed" if packaged_seed else "Topic-Derived Mindset Source"
    lines = [f"# {kind}: {escape(str(source.get('mindset_key', 'unknown')))}", "", escape(str(source.get("purpose", "")))]
    if path is not None:
        lines.extend(("", f"- Current path: `{escape(str(path))}`"))
    lines.append(f"- Digest: `{canonical_digest(source)}`")
    applicability = source.get("applicability")
    if isinstance(applicability, dict):
        for label, field in (("Actions", "actions"), ("Source kinds", "source_kinds"), ("Depths", "depths")):
            values = applicability.get(field)
            if isinstance(values, list):
                lines.append(f"- {label}: {', '.join(f'`{escape(str(value))}`' for value in values)}")
    derivation = source.get("derivation")
    if isinstance(derivation, dict):
        lines.append(f"- Derived from: `{escape(str(derivation.get('overview_semantic_label', 'unknown')))}` at `{escape(str(derivation.get('overview_digest', 'unknown')))}`")
    lines.extend(("", "## Fixed Questions", ""))
    for index, question in enumerate(source.get("questions", []), start=1):
        if not isinstance(question, dict):
            continue
        lines.append(f"{index}. **{escape(str(question.get('question_id', 'unknown')))}:** {escape(str(question.get('prompt', '')))}")
        notes = str(question.get("additional_notes", ""))
        lines.append(f"   Notes: {escape(notes) if notes else '_none_'}")
        lines.append(f"   Answer expectation: {escape(str(question.get('answer_expectation', '')))}")
        lines.append(f"   Evidence expectation: {escape(str(question.get('evidence_expectation', '')))}")
    collector = source.get("additional_question_collector")
    if isinstance(collector, dict):
        lines.extend(("", "## Additional-Question Collector", "", f"**{escape(str(collector.get('question_id', 'unknown')))}:** {escape(str(collector.get('prompt', '')))}", f"Notes: {escape(str(collector.get('additional_notes', ''))) or '_none_'}"))
    return "\n".join(lines) + "\n"


def ensure_mindset_sources(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    cwd: Path,
    specialize: Callable[[Mapping[str, Any], str], Mapping[str, Any]] | None = None,
) -> dict[str, object]:
    """Create only missing topic Sources after a concrete topic overview resolves."""

    overview_resolution, overview_diagnostics = resolve_semantic_path(context, "topic.intent.overview", env=env, cwd=cwd)
    root_resolution, root_diagnostics = resolve_semantic_path(context, SOURCE_SEMANTIC_LABEL, env=env, cwd=cwd)
    diagnostic_messages = [item.message for item in [*overview_diagnostics, *root_diagnostics]]
    if overview_resolution is None or root_resolution is None:
        return {"ok": False, "mutated": False, "created": [], "preserved": [], "invalid": [], "missing": list(DEFAULT_KEYS), "diagnostics": diagnostic_messages}
    overview_path = overview_resolution.path
    try:
        overview_text = overview_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return {"ok": False, "mutated": False, "created": [], "preserved": [], "invalid": [], "missing": list(DEFAULT_KEYS), "diagnostics": [f"Concrete topic.intent.overview is unreadable: {overview_path}: {exc}"]}
    if not overview_text.strip():
        return {"ok": False, "mutated": False, "created": [], "preserved": [], "invalid": [], "missing": list(DEFAULT_KEYS), "diagnostics": [f"Concrete topic.intent.overview is required: {overview_path}"]}
    package_diagnostics = validate_packaged_defaults()
    if package_diagnostics:
        return {"ok": False, "mutated": False, "created": [], "preserved": [], "invalid": [], "missing": list(DEFAULT_KEYS), "diagnostics": [f"Packaged Mindset Default is invalid at {item.location}: {item.message}" for item in package_diagnostics]}
    root = root_resolution.path
    try:
        root.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        return {"ok": False, "mutated": False, "created": [], "preserved": [], "invalid": [], "missing": list(DEFAULT_KEYS), "diagnostics": [f"Mindset Source semantic root cannot be materialized: {root}: {exc}"]}
    created: list[dict[str, str]] = []
    preserved: list[dict[str, str]] = []
    invalid: list[dict[str, object]] = []
    drift: list[dict[str, str]] = []
    overview_digest = file_digest(overview_path)
    for key in DEFAULT_KEYS:
        target = mindset_source_child(root, key)
        if target.exists():
            source, diagnostics = load_mindset_source(target, expected_key=key)
            if source is None or diagnostics:
                try:
                    digest = file_digest(target)
                except OSError:
                    digest = "unavailable"
                invalid.append({"mindset_key": key, "path": str(target), "digest": digest, "diagnostics": [item.to_json() for item in diagnostics]})
                continue
            preserved.append({"mindset_key": key, "path": str(target), "digest": canonical_digest(source)})
            derivation = source.get("derivation")
            if isinstance(derivation, dict) and derivation.get("overview_digest") != overview_digest:
                drift.append({"mindset_key": key, "path": str(target), "observed_overview_digest": str(derivation.get("overview_digest")), "current_overview_digest": overview_digest})
            continue
        seed_path = mindset_source_child(packaged_default_root(), key)
        seed, diagnostics = load_mindset_source(seed_path, expected_key=key)
        if seed is None or diagnostics:
            invalid.append({"mindset_key": key, "path": str(seed_path), "diagnostics": [item.to_json() for item in diagnostics]})
            continue
        candidate = dict(specialize(deepcopy(seed), overview_text)) if specialize is not None else deepcopy(seed)
        candidate_diagnostics = mindset_source_diagnostics(candidate, filename=target.name, expected_key=key)
        if candidate_diagnostics:
            invalid.append({"mindset_key": key, "path": str(target), "diagnostics": [item.to_json() for item in candidate_diagnostics]})
            continue
        _atomic_write_json(target, candidate)
        created.append({"mindset_key": key, "path": str(target), "digest": canonical_digest(candidate)})
    missing = [key for key in DEFAULT_KEYS if not mindset_source_child(root, key).exists()]
    return {"ok": not invalid and not missing, "mutated": bool(created), "semantic_label": SOURCE_SEMANTIC_LABEL, "created": created, "preserved": preserved, "invalid": invalid, "missing": missing, "derivation_drift": drift, "diagnostics": diagnostic_messages}


def replace_mindset_source(path: Path, candidate: Mapping[str, Any], *, observed_digest: str) -> dict[str, str]:
    """Atomically replace an explicitly targeted Source after an optimistic check."""

    current, diagnostics = load_mindset_source(path)
    if not path.is_file():
        raise ValueError("Existing Mindset Source is missing; use create-missing before replacement.")
    old_digest = canonical_digest(current) if current is not None and not diagnostics else file_digest(path)
    if old_digest != observed_digest:
        raise ValueError("Mindset Source changed after it was read; re-read before replacing it.")
    expected_key = path.name.removesuffix(".json") if path.name.endswith(".json") else ""
    candidate_diagnostics = mindset_source_diagnostics(candidate, filename=path.name, expected_key=expected_key)
    if candidate_diagnostics:
        raise ValueError("Replacement Mindset Source is invalid: " + "; ".join(item.message for item in candidate_diagnostics))
    _atomic_write_json(path, candidate)
    return {"path": str(path), "mindset_key": str(candidate["mindset_key"]), "old_digest": old_digest, "new_digest": canonical_digest(candidate)}


def select_mindset_key(*, action: str, source_kind: str, depth: str, process: Mapping[str, Any], explicit_key: str | None = None) -> str | None:
    """Select one checked route; reject explicit keys outside route applicability."""

    config = process.get("mindsets")
    routes = config.get("routes") if isinstance(config, dict) else None
    if not isinstance(routes, list):
        raise ValueError("Kaoju process contract has no checked mindset routes.")
    matches = [item for item in routes if isinstance(item, dict) and action in item.get("actions", []) and source_kind in item.get("source_kinds", []) and depth in item.get("depths", [])]
    if explicit_key is not None:
        explicit_matches = [item for item in matches if item.get("mindset_key") == explicit_key]
        if not explicit_matches:
            raise ValueError(f"Explicit mindset key {explicit_key!r} does not apply to the selected action, source kind, and depth.")
        return explicit_key
    keys = {str(item.get("mindset_key")) for item in matches}
    if not keys:
        return None
    if len(keys) != 1:
        raise ValueError("Mindset route is ambiguous; select the inspection depth or an applicable key explicitly.")
    return next(iter(keys))


def materialize_record_payload(
    source: Mapping[str, Any],
    *,
    relative_path: str,
    topic_id: str,
    run_ref: str,
    survey_contract_ref: str,
    survey_context_refs: Sequence[str],
) -> dict[str, Any]:
    """Create an independently readable, initially active Mindset Record snapshot."""

    source_diagnostics = mindset_source_diagnostics(source, filename=relative_path, expected_key=str(source.get("mindset_key", "")))
    if source_diagnostics:
        raise ValueError("Cannot materialize an invalid Mindset Source: " + "; ".join(item.message for item in source_diagnostics))
    if not survey_context_refs:
        raise ValueError("Mindset Record requires a selected Direction Set or direction-scoped Reading List context ref.")
    rows = [_materialized_question(question) for question in source.get("questions", []) if isinstance(question, dict)]
    collector = _materialized_question(source["additional_question_collector"])
    collector["checked"] = False
    payload = {
        "title": f"Mindset Record: {source['mindset_key']}",
        "summary": "Run-scoped answers to an immutable snapshot of a topic Mindset Source.",
        "artifact_family": "kaoju",
        "semantic_id": RECORD_SEMANTIC_ID,
        "artifact_type": "mindset-record",
        "sections": {
            "source_snapshot": {
                "semantic_label": SOURCE_SEMANTIC_LABEL,
                "relative_path": relative_path,
                "mindset_key": source["mindset_key"],
                "digest": canonical_digest(source),
                **({"derivation": source["derivation"]} if isinstance(source.get("derivation"), dict) else {}),
                "questions": rows,
                "additional_question_collector": collector,
            },
            "survey_context": {"topic_id": topic_id, "run_ref": run_ref, "survey_contract_ref": survey_contract_ref, "context_refs": list(survey_context_refs)},
            "supplemental_questions": [],
            "source_update": {"disposition": "record_only"},
            "unresolved_questions": [],
            "terminal_status": "active",
        },
    }
    record_diagnostics = validate_mindset_record(payload)
    if record_diagnostics:
        raise ValueError("Materialized Mindset Record is invalid: " + "; ".join(item.message for item in record_diagnostics))
    return payload


def validate_mindset_record(payload: Mapping[str, Any], *, prior_payload: Mapping[str, Any] | None = None) -> list[MindsetDiagnostic]:
    """Validate Mindset Record semantics and immutable snapshot inventory."""

    diagnostics: list[MindsetDiagnostic] = []
    try:
        serialized_size = len(json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
    except (TypeError, ValueError):
        serialized_size = 0
    if serialized_size > MAX_RECORD_BYTES:
        diagnostics.append(MindsetDiagnostic("mindset_record_too_large", f"Mindset Record exceeds {MAX_RECORD_BYTES} bytes.", "<root>"))
    schema = _load_json_artifact_resource("assets/research_record_formats/schemas/mindset-record.v1.schema.json")
    errors = sorted(Draft202012Validator(schema).iter_errors(payload), key=lambda error: (tuple(str(part) for part in error.path), error.message))
    diagnostics.extend(MindsetDiagnostic("mindset_record_schema_invalid", error.message, "/".join(str(part) for part in error.path) or "<root>") for error in errors)
    sections = payload.get("sections")
    if not isinstance(sections, dict):
        return diagnostics
    source = sections.get("source_snapshot")
    if isinstance(source, dict):
        relative = source.get("relative_path")
        key = source.get("mindset_key")
        if isinstance(key, str) and relative != f"{key}.json":
            diagnostics.append(MindsetDiagnostic("mindset_record_locator_mismatch", "Source relative_path must equal <mindset_key>.json.", "sections/source_snapshot/relative_path"))
        rows = source.get("questions")
        collector = source.get("additional_question_collector")
        ids = [str(row.get("question_id")) for row in rows if isinstance(row, dict)] if isinstance(rows, list) else []
        if isinstance(collector, dict):
            ids.append(str(collector.get("question_id")))
        supplements = sections.get("supplemental_questions")
        if isinstance(supplements, list):
            ids.extend(str(row.get("question_id")) for row in supplements if isinstance(row, dict))
        duplicates = sorted({question_id for question_id in ids if ids.count(question_id) > 1})
        if duplicates:
            diagnostics.append(MindsetDiagnostic("mindset_record_question_id_duplicate", f"All Source, collector, and supplemental question ids must be unique: {', '.join(duplicates)}.", "sections/source_snapshot/questions"))
        for index, row in enumerate(rows if isinstance(rows, list) else []):
            if isinstance(row, dict):
                diagnostics.extend(_question_state_diagnostics(row, f"sections/source_snapshot/questions/{index}"))
                forbidden = {"checked", "origin", "association_basis", "introduction_stage", "disposition"} & set(row)
                for field in sorted(forbidden):
                    diagnostics.append(MindsetDiagnostic("mindset_record_snapshot_field_invalid", f"Fixed Source question cannot contain supplemental field {field!r}.", f"sections/source_snapshot/questions/{index}/{field}"))
        if isinstance(collector, dict):
            diagnostics.extend(_question_state_diagnostics(collector, "sections/source_snapshot/additional_question_collector"))
            forbidden = {"origin", "association_basis", "introduction_stage", "disposition"} & set(collector)
            for field in sorted(forbidden):
                diagnostics.append(MindsetDiagnostic("mindset_record_collector_field_invalid", f"Collector cannot contain supplemental field {field!r}.", f"sections/source_snapshot/additional_question_collector/{field}"))
            if collector.get("prompt") != COLLECTOR_PROMPT or collector.get("answer_expectation") != COLLECTOR_ANSWER_EXPECTATION:
                diagnostics.append(MindsetDiagnostic("mindset_record_collector_contract_invalid", "Materialized collector must preserve the checked prompt and answer expectation.", "sections/source_snapshot/additional_question_collector"))
    supplements = sections.get("supplemental_questions")
    if isinstance(supplements, list):
        for index, row in enumerate(supplements):
            if isinstance(row, dict):
                diagnostics.extend(_question_state_diagnostics(row, f"sections/supplemental_questions/{index}"))
                if "checked" in row:
                    diagnostics.append(MindsetDiagnostic("mindset_record_supplemental_field_invalid", "Supplemental question cannot declare collector field 'checked'.", f"sections/supplemental_questions/{index}/checked"))
                if row.get("required_posture") == "collect-explicit-only":
                    diagnostics.append(MindsetDiagnostic("mindset_record_supplemental_posture_invalid", "Supplemental question must use an answer posture, not collector posture.", f"sections/supplemental_questions/{index}/required_posture"))
    if prior_payload is not None and _record_snapshot(payload) != _record_snapshot(prior_payload):
        diagnostics.append(MindsetDiagnostic("mindset_record_snapshot_changed", "A Mindset Record revision cannot change its materialized Source snapshot or pinned survey context.", "sections/source_snapshot"))
    source_update = sections.get("source_update")
    if isinstance(source_update, dict):
        disposition = source_update.get("disposition")
        updated_supplements = [row for row in supplements if isinstance(row, dict) and row.get("disposition") == "source_updated"] if isinstance(supplements, list) else []
        requested_supplements = [row for row in supplements if isinstance(row, dict) and row.get("disposition") == "source_update_requested"] if isinstance(supplements, list) else []
        if disposition == "record_only" and (updated_supplements or requested_supplements):
            diagnostics.append(MindsetDiagnostic("mindset_record_source_update_mismatch", "Record-only Source posture cannot contain Source-update supplemental rows.", "sections/source_update/disposition"))
        if disposition == "source_update_requested" and not requested_supplements:
            diagnostics.append(MindsetDiagnostic("mindset_record_source_update_mismatch", "Source-update-requested posture requires an explicitly associated supplemental row.", "sections/source_update/disposition"))
        if disposition == "source_updated":
            if not updated_supplements:
                diagnostics.append(MindsetDiagnostic("mindset_record_source_update_mismatch", "Source-updated posture requires a supplemental row marked source_updated.", "sections/source_update/disposition"))
            source_key = source.get("mindset_key") if isinstance(source, dict) else None
            if isinstance(source_key, str) and source_update.get("new_relative_path") != f"{source_key}.json":
                diagnostics.append(MindsetDiagnostic("mindset_record_source_update_locator_mismatch", "Updated Source path must retain the snapshotted mindset key filename.", "sections/source_update/new_relative_path"))
    terminal = sections.get("terminal_status")
    if terminal in {"complete", "paused", "blocked"}:
        source_map = source if isinstance(source, dict) else {}
        rows = source_map.get("questions", [])
        collector = source_map.get("additional_question_collector", {})
        supplements = sections.get("supplemental_questions", [])
        all_rows = [*rows, *supplements] if isinstance(rows, list) and isinstance(supplements, list) else []
        unfinished = [str(row.get("question_id")) for row in all_rows if isinstance(row, dict) and row.get("answer_state") not in {"answered", "unresolved", "not_applicable"}]
        if isinstance(collector, dict) and collector.get("answer_state") not in {"answered", "unresolved", "not_applicable"}:
            unfinished.append(str(collector.get("question_id")))
        if unfinished:
            diagnostics.append(MindsetDiagnostic("mindset_record_terminal_unanswered", f"Terminal Record has unfinished questions: {', '.join(unfinished)}.", "sections/source_snapshot/questions"))
        if not isinstance(collector, dict) or collector.get("checked") is not True:
            diagnostics.append(MindsetDiagnostic("mindset_record_collector_unchecked", "Terminal Record must mark the additional-question collector checked.", "sections/source_snapshot/additional_question_collector/checked"))
        unresolved = {str(row.get("question_id")) for row in [*all_rows, collector] if isinstance(row, dict) and row.get("answer_state") == "unresolved"}
        declared_unresolved = {str(value) for value in sections.get("unresolved_questions", [])} if isinstance(sections.get("unresolved_questions"), list) else set()
        if unresolved != declared_unresolved:
            diagnostics.append(MindsetDiagnostic("mindset_record_unresolved_inventory_mismatch", "Terminal unresolved_questions must exactly name every unresolved materialized and supplemental row.", "sections/unresolved_questions"))
    return diagnostics


def render_mindset_record(payload: Mapping[str, Any]) -> str:
    """Render a historical Record entirely from its immutable snapshot."""

    sections = payload.get("sections", {})
    source = sections.get("source_snapshot", {}) if isinstance(sections, dict) else {}
    lines = [f"# {escape(str(payload.get('title', 'Mindset Record')))}", "", escape(str(payload.get("summary", ""))), "", f"- Source: `{escape(str(source.get('semantic_label', '')))}/{escape(str(source.get('relative_path', '')))}`", f"- Mindset key: `{escape(str(source.get('mindset_key', '')))}`", f"- Snapshotted digest: `{escape(str(source.get('digest', '')))}`"]
    context = sections.get("survey_context", {}) if isinstance(sections, dict) else {}
    if isinstance(context, dict):
        lines.extend((f"- Research Topic: `{escape(str(context.get('topic_id', '')))}`", f"- Run: `{escape(str(context.get('run_ref', '')))}`", f"- Survey Contract: `{escape(str(context.get('survey_contract_ref', '')))}`", f"- Survey context refs: {', '.join(f'`{escape(str(item))}`' for item in context.get('context_refs', [])) or '_none_'}"))
    lines.extend(("", "## Materialized Source Questions", ""))
    for row in source.get("questions", []) if isinstance(source, dict) else []:
        if isinstance(row, dict):
            lines.extend(_render_record_row(row))
    collector = source.get("additional_question_collector") if isinstance(source, dict) else None
    if isinstance(collector, dict):
        lines.extend(("", "## Collector Posture", "", f"Checked: `{str(collector.get('checked', False)).lower()}`"))
        lines.extend(_render_record_row(collector))
    lines.extend(("", "## Explicitly Assigned Supplemental Questions", ""))
    supplements = sections.get("supplemental_questions", []) if isinstance(sections, dict) else []
    if supplements:
        for row in supplements:
            if isinstance(row, dict):
                lines.extend(_render_record_row(row))
    else:
        lines.append("None.")
    update = sections.get("source_update", {}) if isinstance(sections, dict) else {}
    lines.extend(("", "## Source Update Status", "", f"Disposition: `{escape(str(update.get('disposition', 'record_only')))}`"))
    if update.get("new_relative_path"):
        lines.append(f"New Source: `{escape(str(update.get('new_relative_path')))}` at `{escape(str(update.get('new_digest', '')))}`")
    lines.extend(("", "## Unresolved Questions", ""))
    unresolved = sections.get("unresolved_questions", []) if isinstance(sections, dict) else []
    lines.extend(f"- `{escape(str(item))}`" for item in unresolved)
    if not unresolved:
        lines.append("None.")
    return "\n".join(lines) + "\n"


def target_for_question(*, explicit_target: str | None, asks_to_persist: bool) -> str:
    """Route ordinary follow-ups and explicit Source/Record/both requests."""

    if explicit_target in {"source", "record", "both"}:
        return explicit_target
    if asks_to_persist:
        return "clarify"
    return "reading_artifact"


def _materialized_question(question: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "question_id": question["question_id"],
        "prompt": question["prompt"],
        "additional_notes": question["additional_notes"],
        "answer_expectation": question["answer_expectation"],
        "required_posture": question["required_posture"],
        "evidence_expectation": question["evidence_expectation"],
        "answer_state": "unanswered",
        "answer": None,
        "rationale": None,
        "evidence_refs": [],
    }


def _record_snapshot(payload: Mapping[str, Any]) -> str:
    sections = payload.get("sections")
    source = sections.get("source_snapshot") if isinstance(sections, dict) else None
    if not isinstance(source, dict):
        return ""
    assert isinstance(sections, dict)
    snapshot = {
        key: source.get(key)
        for key in ("semantic_label", "relative_path", "mindset_key", "digest", "derivation")
        if key in source
    }
    snapshot["questions"] = [_question_contract(row) for row in source.get("questions", []) if isinstance(row, dict)]
    collector = source.get("additional_question_collector")
    snapshot["additional_question_collector"] = _question_contract(collector) if isinstance(collector, dict) else None
    snapshot["survey_context"] = sections.get("survey_context")
    return canonical_digest(snapshot)


def _question_contract(row: Mapping[str, Any]) -> dict[str, Any]:
    return {key: row.get(key) for key in ("question_id", "prompt", "additional_notes", "answer_expectation", "required_posture", "evidence_expectation")}


def _render_record_row(row: Mapping[str, Any]) -> list[str]:
    notes = escape(str(row.get("additional_notes", ""))) or "_none_"
    answer = row.get("answer") or row.get("rationale") or "_not recorded_"
    evidence = ", ".join(f"`{escape(str(item))}`" for item in row.get("evidence_refs", [])) or "_none_"
    return [f"### {escape(str(row.get('question_id', 'unknown')))}", "", escape(str(row.get("prompt", ""))), "", f"Notes: {notes}", f"Required posture: `{escape(str(row.get('required_posture', '')))}`", f"Answer expectation: {escape(str(row.get('answer_expectation', '')))}", f"Evidence expectation: {escape(str(row.get('evidence_expectation', '')))}", f"State: `{escape(str(row.get('answer_state', 'unanswered')))}`", f"Answer or rationale: {escape(str(answer))}", f"Evidence: {evidence}"]


def _question_state_diagnostics(row: Mapping[str, Any], location: str) -> list[MindsetDiagnostic]:
    diagnostics: list[MindsetDiagnostic] = []
    state = row.get("answer_state")
    answer = row.get("answer")
    rationale = row.get("rationale")
    if state == "answered" and (not isinstance(answer, str) or not answer.strip()):
        diagnostics.append(MindsetDiagnostic("mindset_record_answer_missing", "Answered question requires a non-empty answer.", f"{location}/answer"))
    if state in {"unresolved", "not_applicable"} and (not isinstance(rationale, str) or not rationale.strip()):
        diagnostics.append(MindsetDiagnostic("mindset_record_rationale_missing", f"{state} question requires a non-empty rationale.", f"{location}/rationale"))
    if state == "unanswered" and (answer is not None or rationale is not None):
        diagnostics.append(MindsetDiagnostic("mindset_record_unanswered_content_invalid", "Unanswered question cannot claim an answer or rationale.", location))
    posture = row.get("required_posture")
    if posture == "answer-or-unresolved" and state == "not_applicable":
        diagnostics.append(MindsetDiagnostic("mindset_record_answer_posture_invalid", "Question posture requires answered or unresolved, not not_applicable.", f"{location}/answer_state"))
    if posture == "answer-or-not-applicable" and state == "unresolved":
        diagnostics.append(MindsetDiagnostic("mindset_record_answer_posture_invalid", "Question posture requires answered or not_applicable, not unresolved.", f"{location}/answer_state"))
    return diagnostics


def _load_json_resource(relative: str) -> dict[str, Any]:
    value = json.loads(files("isomer_labs.kaoju").joinpath(relative).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Packaged Kaoju resource must be an object: {relative}")
    return value


def _load_json_artifact_resource(relative: str) -> dict[str, Any]:
    value = json.loads(files("isomer_labs.artifact_formats").joinpath(relative).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Packaged Artifact Format resource must be an object: {relative}")
    return value


def _walk_keys(value: object, prefix: str = "<root>") -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            location = f"{prefix}/{key}"
            found.append((location, str(key)))
            found.extend(_walk_keys(child, location))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(_walk_keys(child, f"{prefix}/{index}"))
    return found


def _atomic_write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    try:
        temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()
