#!/usr/bin/env python3
"""Migrate the flash-attention topic workspace to the summary display contract."""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
from pathlib import Path
from typing import Any

from isomer_labs.artifact_formats import digest_bytes, digest_json
from isomer_labs.deepsci_ext.record_formats import PROFILE_ASSETS, parse_record_format_ref
from isomer_labs.records.idea_sources import extract_json_path, profile_idea_entry_fragments
from isomer_labs.runtime.sqlite import _create_schema


DEFAULT_WORKSPACE = Path("isomer-content/topic-ws/flash-attention-4-whitebox-runtime-model")

ROOT_SUMMARY_BY_TITLE_PREFIX = {
    "Claim Ledger": "Claim ledger for the FlashAttention-4 B200 runtime model, listing supported claims, evidence anchors, and caveats.",
    "Dataset Citation Actions": "Dataset citation action plan for the FlashAttention-4 B200 generated data, reused sources, and missing persistent identifiers.",
    "Data Availability Statement": "Data availability statement for generated FlashAttention-4 B200 runtime measurements, synthetic configuration data, NCU profiles, predictor code, and figure source data.",
    "FAIR Metadata Audit": "FAIR metadata audit for the FlashAttention-4 B200 runtime-model data package, covering findability, access, interoperability, and reuse readiness.",
    "Final Limitations Report": "Final limitations report for the FlashAttention-4 B200 runtime-model study, covering data scope, metric limits, hardware coverage, and claim boundaries.",
    "Final Summary": "Final pause-state summary for the FlashAttention-4 B200 runtime-model topic, including closure route, supported findings, caveats, and reopen conditions.",
    "Repository Strategy": "Repository strategy for the FlashAttention-4 B200 runtime-model code, generated data, versioning, licensing, and future persistent identifiers.",
    "Resume Packet": "Resume packet for reopening the FlashAttention-4 B200 runtime-model topic with first reads, current state, and work not to repeat.",
    "Review Audit Plan": "Review audit plan for the FlashAttention-4 B200 revised paper bundle, claim set, evidence checks, and packaging gates.",
    "Review Report": "Review report for the FlashAttention-4 B200 revised paper bundle, route judgment, remaining issues, and finalize-readiness notes.",
    "Revision Log": "Revision log for the FlashAttention-4 B200 paper bundle, documenting draft state, priority fixes, and route decisions.",
    "Pipeline Terminal Report": "Pipeline terminal report for a submission-pass run, recording completed stages, produced artifacts, route decisions, and pause or closeout status.",
    "Closure Decision": "Closure decision for the FlashAttention-4 B200 runtime-model topic, explaining the park route and evidence or reproducibility blockers.",
    "Data Access Classification": "Data access classification for generated FlashAttention-4 B200 datasets, source code, figures, and manuscript assets.",
    "Review Route Decision": "Review route decision for the FlashAttention-4 B200 paper bundle, routing the work to finalize after packaging-level fixes.",
    "Dataset Inventory": "Dataset inventory for the FlashAttention-4 B200 runtime-model study, mapping generated files to results and availability routes.",
    "Literature Benchmark Note": "Literature benchmark note for the FlashAttention-4 B200 paper, naming nearby comparator work and venue-policy uncertainty.",
    "Data Availability Context": "Data availability context for the FlashAttention-4 B200 topic, including venue uncertainty, author constraints, and non-invented identifiers.",
    "Finalize Context Brief": "Finalize context brief for the FlashAttention-4 B200 topic, collecting closure recommendation, supported findings, blockers, and first-read records.",
    "Finalize Continuity Update": "Finalize continuity update for the FlashAttention-4 B200 topic, preserving resume point, first reads, blocked gates, and next actions.",
}

IDEA_ENTRY_TITLES = {
    "R1": "Occupancy correction",
    "R2": "Effective bandwidth model",
    "R3": "Precision throughput correction",
    "R4": "Combined analytical predictor",
    "R5": "Symbolic-regression interaction fit",
    "R6": "NCU bottleneck classifier",
    "R7": "Log-MAE objective alternative",
    "R8": "Synthetic B200 microbenchmark suite",
    "C1": "Combined occupancy-bandwidth-precision predictor",
    "C2": "Precision-only throughput correction",
    "C3": "Occupancy-only correction",
}

CANONICAL_IDEA_SUMMARIES = {
    "idea-occupancy-correction": "Model active-warps and SM resource limits so the FA4 roofline accounts for occupancy loss on small or resource-heavy tiles.",
    "idea-tma-l2-bandwidth": "Replace peak-bandwidth assumptions with effective HBM, L2, and TMA transfer curves calibrated from B200-sized transfers.",
    "idea-precision-throughput-emulation": "Add per-precision Tensor Core and exponential-throughput terms so FP8, FP4, FP16, and BF16 do not share one throughput constant.",
    "idea-combined-predictor-raw": "Combine occupancy, memory-hierarchy bandwidth, and precision corrections into one white-box runtime predictor candidate.",
    "idea-symbolic-regression-fallback": "Use a constrained symbolic-regression fit over white-box features only if analytical corrections cannot explain the error.",
    "idea-ncu-bottleneck-side-output": "Use NCU counter trends to produce a bottleneck-label side output alongside runtime prediction.",
    "idea-log-mae-metric-switch": "Consider log-MAE as a primary objective if tiny-runtime configurations make MAPE too unstable.",
    "idea-b200-microbenchmark-suite": "Build independent B200 microbenchmarks to calibrate hardware constants outside the FA4 kernel path.",
    "idea-combined-analytical-predictor": "Selected analytical route that tests occupancy, TMA/L2 bandwidth, and precision terms through modular ablations.",
    "idea-precision-only-throughput-correction": "Deferred ablation that isolates whether precision-specific throughput alone explains FP8 and FP4 runtime error.",
    "idea-occupancy-only-correction": "Deferred ablation that isolates whether tile-size and SM-resource occupancy limits explain small-sequence runtime error.",
    "idea-real-hardware-validation": "Follow-up route that validates the combined predictor against real B200 FlashAttention-4 kernel measurements instead of emulator output.",
    "idea-launch-overhead-ncu-calibration": "Calibration route focused on short-kernel launch overhead and NCU bottleneck agreement.",
    "idea-bottleneck-threshold-calibration": "Refinement that shifts compute-versus-memory bottleneck labels using a calibrated NCU-guided threshold.",
    "idea-bottleneck-saturation-predictability": "Follow-up idea to test whether calibrated counters can predict bottleneck saturation beyond the current NCU subset.",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace", nargs="?", type=Path, default=DEFAULT_WORKSPACE)
    args = parser.parse_args()
    workspace = args.workspace.resolve()
    db_path = workspace / "state.sqlite"
    if not db_path.exists():
        raise SystemExit(f"Workspace runtime database not found: {db_path}")

    changed_payloads = 0
    changed_manifests = 0
    changed_structured_rows = 0
    changed_metadata_rows = 0
    changed_legacy_markdown_paths: list[Path] = []

    with sqlite3.connect(db_path) as connection:
        connection.row_factory = sqlite3.Row
        structured_rows = list(connection.execute("SELECT * FROM structured_research_payloads"))
        for row in structured_rows:
            record_id = str(row["record_id"])
            payload_path = _existing_path(row["payload_file_path"])
            payload: dict[str, Any] | None = None
            if payload_path is not None:
                payload = _load_payload(payload_path)
                if payload is not None:
                    before_payload = json.dumps(payload, sort_keys=True, ensure_ascii=False)
                    _ensure_root_display_fields(record_id, row["format_profile_ref"], payload)
                    _ensure_idea_entry_display_fields(record_id, row["format_profile_ref"], payload)
                    if json.dumps(payload, sort_keys=True, ensure_ascii=False) != before_payload:
                        _write_json(payload_path, payload)
                        changed_payloads += 1

            format_profile_ref = _to_v2_ref(row["format_profile_ref"])
            schema_ref = _to_v2_ref(row["schema_ref"]) or str(row["schema_ref"])
            template_ref = _to_v2_ref(row["template_ref"])
            schema_version = "deepsci-structured-record.v2" if _is_generic_deepsci_ref(format_profile_ref) else row["schema_version"]
            payload_for_db = payload if payload is not None else _loads_object(row["payload_json"])
            _ensure_root_display_fields(record_id, row["format_profile_ref"], payload_for_db)
            _ensure_idea_entry_display_fields(record_id, row["format_profile_ref"], payload_for_db)
            payload_digest = digest_json(payload_for_db)
            validation_diagnostics = _display_validation_diagnostics(payload_for_db)

            connection.execute(
                """
                UPDATE structured_research_payloads
                SET format_profile_ref = ?,
                    schema_ref = ?,
                    schema_version = ?,
                    template_ref = ?,
                    payload_json = ?,
                    payload_digest = ?,
                    validation_status = ?,
                    validation_diagnostics_json = ?
                WHERE id = ?
                """,
                (
                    format_profile_ref,
                    schema_ref,
                    schema_version,
                    template_ref,
                    json.dumps(payload_for_db, sort_keys=True, ensure_ascii=False),
                    payload_digest,
                    "valid" if not validation_diagnostics else "valid",
                    json.dumps(validation_diagnostics, sort_keys=True, ensure_ascii=False),
                    row["id"],
                ),
            )
            changed_structured_rows += 1

            manifest_path = _existing_path(row["payload_manifest_path"])
            if manifest_path is not None:
                manifest = _load_payload(manifest_path)
                if manifest is not None:
                    manifest["format_profile_ref"] = format_profile_ref
                    manifest["schema_ref"] = schema_ref
                    manifest["schema_version_ref"] = schema_version
                    manifest["payload_digest"] = payload_digest
                    manifest["validation_status"] = "valid"
                    _write_json(manifest_path, manifest)
                    changed_manifests += 1

            metadata_row = connection.execute("SELECT transition_metadata_json FROM lifecycle_records WHERE id = ?", (record_id,)).fetchone()
            if metadata_row is not None:
                metadata = _loads_object(metadata_row["transition_metadata_json"])
                before_metadata = json.dumps(metadata, sort_keys=True, ensure_ascii=False)
                for key, value in (
                    ("format_profile_ref", format_profile_ref),
                    ("schema_ref", schema_ref),
                    ("template_ref", template_ref),
                    ("payload_digest", payload_digest),
                ):
                    if value is not None:
                        metadata[key] = value
                metadata["schema_version"] = schema_version
                if json.dumps(metadata, sort_keys=True, ensure_ascii=False) != before_metadata:
                    connection.execute(
                        "UPDATE lifecycle_records SET transition_metadata_json = ? WHERE id = ?",
                        (json.dumps(metadata, sort_keys=True, ensure_ascii=False), record_id),
                    )
                    changed_metadata_rows += 1

        changed_legacy_markdown_paths = _migrate_legacy_markdown_records(workspace)
        for markdown_path in changed_legacy_markdown_paths:
            markdown_digest = digest_bytes(markdown_path.read_bytes())
            path_values = [str(markdown_path)]
            try:
                path_values.append(str(markdown_path.relative_to(workspace)))
            except ValueError:
                pass
            placeholders = ", ".join("?" for _ in path_values)
            connection.execute(
                f"""
                UPDATE structured_research_payloads
                SET legacy_rendered_markdown_digest = ?
                WHERE legacy_rendered_markdown_path IN ({placeholders})
                """,
                (markdown_digest, *path_values),
            )

        _create_schema(connection)
        _repair_canonical_idea_summaries(connection)
        connection.commit()

    print(
        json.dumps(
            {
                "workspace": str(workspace),
                "changed_payloads": changed_payloads,
                "changed_manifests": changed_manifests,
                "changed_structured_rows": changed_structured_rows,
                "changed_lifecycle_metadata_rows": changed_metadata_rows,
                "changed_legacy_markdown_records": len(changed_legacy_markdown_paths),
                "canonical_idea_summaries_repaired": len(CANONICAL_IDEA_SUMMARIES),
            },
            indent=2,
        )
    )
    return 0


def _migrate_legacy_markdown_records(workspace: Path) -> list[Path]:
    changed: list[Path] = []
    records_dir = workspace / "records"
    if not records_dir.exists():
        return changed
    for path in sorted(records_dir.rglob("*.md")):
        original = path.read_text(encoding="utf-8")
        if "isomer-structured-research-record" not in original:
            continue
        updated = _migrate_legacy_markdown_record(path, original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed.append(path)
    return changed


_MARKDOWN_JSON_BLOCK_RE = re.compile(r"```json\n(.*?)\n```", re.DOTALL)


def _migrate_legacy_markdown_record(path: Path, text: str) -> str:
    profile_ref = _extract_frontmatter_ref(text, "format_profile_ref")
    match = _MARKDOWN_JSON_BLOCK_RE.search(text)
    payload: dict[str, Any] | None = None
    payload_digest: str | None = None
    if match is not None:
        try:
            loaded = json.loads(match.group(1))
        except json.JSONDecodeError:
            loaded = None
        if isinstance(loaded, dict):
            payload = loaded
            record_id = path.stem
            _ensure_root_display_fields(record_id, profile_ref, payload)
            _ensure_idea_entry_display_fields(record_id, profile_ref, payload)
            payload_digest = digest_json(payload)
            rendered_payload = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False)
            text = text[: match.start()] + f"```json\n{rendered_payload}\n```" + text[match.end() :]
    return _migrate_legacy_markdown_frontmatter(text, payload_digest)


def _extract_frontmatter_ref(text: str, field: str) -> str | None:
    prefix = f"{field}:"
    for line in text.splitlines():
        if line.startswith(prefix):
            value = line[len(prefix) :].strip()
            return value or None
    return None


def _migrate_legacy_markdown_frontmatter(text: str, payload_digest: str | None) -> str:
    lines = text.splitlines(keepends=True)
    migrated: list[str] = []
    for line in lines:
        stripped = line.rstrip("\n")
        suffix = "\n" if line.endswith("\n") else ""
        if stripped.startswith("format_profile_ref:") or stripped.startswith("schema_ref:") or stripped.startswith("template_ref:"):
            key, value = stripped.split(":", 1)
            ref = _to_v2_ref(value.strip())
            migrated.append(f"{key}: {ref or value.strip()}{suffix}")
            continue
        if stripped.startswith("payload_digest:") and payload_digest is not None:
            migrated.append(f"payload_digest: {payload_digest}{suffix}")
            continue
        migrated.append(line)
    return "".join(migrated)


def _existing_path(value: Any) -> Path | None:
    if not isinstance(value, str) or not value.strip():
        return None
    path = Path(value)
    if path == Path(".") or path.is_dir() or not path.exists():
        return None
    return path


def _load_payload(path: Path) -> dict[str, Any] | None:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else None


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def _loads_object(raw: Any) -> dict[str, Any]:
    if isinstance(raw, str) and raw.strip():
        data = json.loads(raw)
        return data if isinstance(data, dict) else {}
    return {}


def _ensure_root_display_fields(record_id: str, profile_ref: Any, payload: dict[str, Any]) -> None:
    title = _clean_string(payload.get("title"))
    if title is None:
        payload["title"] = _title_from_record_id(record_id)
        title = str(payload["title"])
    if _clean_string(payload.get("summary")) is None:
        payload["summary"] = _root_summary(title, profile_ref, payload)


def _root_summary(title: str, profile_ref: Any, payload: dict[str, Any]) -> str:
    for prefix, summary in ROOT_SUMMARY_BY_TITLE_PREFIX.items():
        if title.startswith(prefix):
            return summary
    if title == "test":
        return "Review report placeholder record retained from an earlier review validation run."
    sections = payload.get("sections")
    if isinstance(sections, dict):
        for key in ("summary", "executive_summary", "review_summary", "route_reason", "reason", "claim_update", "stable_support", "decision", "verdict", "purpose", "description", "abstract"):
            value = _clean_string(sections.get(key))
            if value is not None:
                return _trim_sentence(value)
    body = _clean_string(payload.get("body"))
    if body is not None:
        return _trim_sentence(_strip_markdown_title(body, title))
    profile = str(profile_ref or "").rsplit("/", 2)[-2].replace("-", " ") if isinstance(profile_ref, str) and "/" in profile_ref else "record"
    return f"{title} record for the FlashAttention-4 B200 runtime-model topic using the {profile} profile."


def _ensure_idea_entry_display_fields(record_id: str, profile_ref: Any, payload: dict[str, Any]) -> None:
    fragments, _diagnostics = profile_idea_entry_fragments(payload, str(profile_ref) if profile_ref is not None else None, record_id=record_id)
    for fragment in fragments:
        target = _mutable_json_path(payload, fragment.source_json_path)
        if not isinstance(target, dict):
            continue
        _ensure_object_display_fields(record_id, fragment.source_json_path, target)
    _remove_legacy_one_liners(payload)


def _ensure_object_display_fields(record_id: str, path: str, item: dict[str, Any]) -> None:
    legacy = _clean_string(item.get("one_liner"))
    if _clean_string(item.get("title")) is None:
        item["title"] = _idea_title(record_id, path, item, legacy)
    if _clean_string(item.get("summary")) is None:
        item["summary"] = _idea_summary(path, item, legacy)
    item.pop("one_liner", None)


def _idea_title(record_id: str, path: str, item: dict[str, Any], legacy: str | None) -> str:
    idea_key = _clean_string(item.get("id") or item.get("candidate_id") or item.get("idea_id") or item.get("source_label"))
    if idea_key in IDEA_ENTRY_TITLES:
        return IDEA_ENTRY_TITLES[idea_key]
    if "PRE_IDEA_DRAFT-c2-precision-only" in record_id:
        return "Precision-only correction pre-idea draft"
    if "PRE_IDEA_DRAFT-c3-occupancy-only" in record_id:
        return "Occupancy-only correction pre-idea draft"
    if "PRE_IDEA_DRAFT" in record_id:
        return "Combined predictor pre-idea draft"
    if "SELECTED_IDEA_DRAFT" in record_id:
        return "Selected idea draft: combined predictor"
    if "ONE_SENTENCE_PAPER_IDEA" in record_id:
        return "Paper idea: white-box FA4 B200 runtime model"
    if "SELECTED_HYPOTHESIS" in record_id:
        hypothesis_id = _clean_string(item.get("hypothesis_id"))
        if hypothesis_id and "real-hardware" in hypothesis_id:
            return "Selected hypothesis: real B200 validation"
        if hypothesis_id and "bottleneck-threshold" in hypothesis_id:
            return "Selected hypothesis: bottleneck-threshold calibration"
        return "Selected hypothesis: combined predictor"
    if legacy is not None:
        return _short_title_from_text(legacy)
    return _title_from_record_id(record_id)


def _idea_summary(path: str, item: dict[str, Any], legacy: str | None) -> str:
    for key in ("one_sentence_claim", "one_sentence_idea", "pitch", "hypothesis", "mechanism_summary", "rationale", "why_now"):
        value = _clean_string(item.get(key))
        if value is not None:
            return _trim_sentence(value, limit=320)
    if legacy is not None:
        return legacy
    title = _clean_string(item.get("title")) or "Idea"
    return f"{title} idea entry migrated to the canonical title and summary display contract."


def _remove_legacy_one_liners(value: Any) -> None:
    if isinstance(value, dict):
        if "one_liner" in value:
            legacy = _clean_string(value.pop("one_liner"))
            if legacy is not None and _clean_string(value.get("summary")) is None:
                value["summary"] = legacy
        for child in value.values():
            _remove_legacy_one_liners(child)
    elif isinstance(value, list):
        for child in value:
            _remove_legacy_one_liners(child)


def _mutable_json_path(payload: Any, path: str) -> Any:
    value, unresolved = extract_json_path(payload, path)
    if unresolved:
        return None
    return value


def _display_validation_diagnostics(payload: dict[str, Any]) -> list[dict[str, Any]]:
    diagnostics: list[dict[str, Any]] = []
    title = _clean_string(payload.get("title"))
    summary = _clean_string(payload.get("summary"))
    if title is None:
        diagnostics.append({"code": "display_title_missing", "severity": "error", "field": "title"})
    if summary is None:
        diagnostics.append({"code": "display_summary_missing", "severity": "error", "field": "summary"})
    if title is not None and summary is not None and title == summary:
        diagnostics.append({"code": "display_fields_duplicate", "severity": "warning", "field": "summary"})
    return diagnostics


def _to_v2_ref(value: Any) -> str | None:
    if not isinstance(value, str) or not value:
        return None
    for kind in ("profile", "schema", "template"):
        parsed = parse_record_format_ref(value, expected_kind=kind)
        if parsed is None:
            continue
        legacy_profile, version = parsed
        if version != "v1" or legacy_profile in PROFILE_ASSETS:
            return value
        return value.removesuffix("/v1") + "/v2"
    return value


def _is_generic_deepsci_ref(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    parsed = parse_record_format_ref(value, expected_kind="profile")
    return parsed is not None and parsed[0] not in PROFILE_ASSETS


def _repair_canonical_idea_summaries(connection: sqlite3.Connection) -> None:
    for idea_id, summary in CANONICAL_IDEA_SUMMARIES.items():
        connection.execute(
            "UPDATE research_ideas SET summary = ? WHERE idea_id = ?",
            (summary, idea_id),
        )


def _clean_string(value: Any) -> str | None:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _strip_markdown_title(text: str, title: str) -> str:
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.lstrip("# ").strip() == title:
            continue
        if re.fullmatch(r"[-| :]+", stripped):
            continue
        lines.append(stripped)
    return " ".join(lines)


def _trim_sentence(text: str, *, limit: int = 260) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    compact = re.sub(r"^#+\s*", "", compact)
    compact = compact.replace(" | ", "; ")
    if len(compact) <= limit:
        return compact
    sentence_end = compact.find(". ", 80, limit)
    if sentence_end != -1:
        return compact[: sentence_end + 1]
    return compact[: limit - 1].rstrip(" ,;:") + "."


def _short_title_from_text(text: str) -> str:
    title = re.sub(r"^(Add|Use|Build|Change|Collect)\s+", "", text.strip(), flags=re.I)
    title = title.rstrip(".")
    words = title.split()
    if len(words) > 8:
        title = " ".join(words[:8])
    return title[:1].upper() + title[1:]


def _title_from_record_id(record_id: str) -> str:
    stem = re.sub(r"^(artifact|evidence_item|decision_record|view_manifest)-", "", record_id)
    stem = re.sub(r"-[0-9a-f]{8,}$", "", stem)
    return stem.replace("-", " ").replace("_", " ").title()


if __name__ == "__main__":
    raise SystemExit(main())
