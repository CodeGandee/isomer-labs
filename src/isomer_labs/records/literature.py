"""Canonical literature observations and their rebuildable local query projection."""

from __future__ import annotations

import json
from pathlib import Path
import sqlite3
from typing import Any, Mapping

from isomer_labs.artifact_formats.research_record_formats import (
    LITERATURE_OBSERVATION_PROFILE_REF,
)
from isomer_labs.core.diagnostics import Diagnostic
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.records.literature_contract import (
    LITERATURE_OBSERVATION_SCHEMA_VERSION,
    PAPER_KEY_RE,
    attachment_index_entries,
    mapping,
    normalized_arxiv_id,
    normalized_doi,
    normalized_paper_key as normalized_paper_key,
    object_array,
    read_payload_path,
    read_structured_payload,
    string_array,
    validate_observation_contract,
    validate_observation_schema,
)
from isomer_labs.records.literature_projection import (
    LITERATURE_QUERY_INDEX_SCHEMA_VERSION as LITERATURE_QUERY_INDEX_SCHEMA_VERSION,
    create_projection_tables,
    drop_projection_tables,
    projection_issues,
    projection_posture,
    projection_required_payload,
    projection_source,
    refresh_projection_after_commit,
    write_projection,
)
from isomer_labs.records.store import (
    ResearchRecordError,
    ResearchRecordRequest,
    create_record,
)
from isomer_labs.runtime.records import StructuredResearchPayloadRecord
from isomer_labs.runtime.store import WorkspaceRuntimeStore, open_workspace_runtime


def record_literature_observation(
    context: EffectiveTopicContext,
    payload_file: Path,
    *,
    env: Mapping[str, str],
    cwd: Path,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    """Validate and commit one immutable canonical observation before projection work."""

    selected_path = payload_file if payload_file.is_absolute() else cwd / payload_file
    selected_path = selected_path.resolve(strict=False)
    payload = read_payload_path(selected_path)
    validate_observation_contract(payload, attachment_base=selected_path.parent, check_attachments=True)
    validate_observation_schema(payload)
    observation_id = str(payload["observation_id"])
    provider = payload["provider"]
    assert isinstance(provider, Mapping)
    raw_attachments = payload.get("raw_attachments", [])
    attachments = attachment_index_entries(raw_attachments, selected_path.parent)
    metadata: dict[str, object] = {
        "immutable": True,
        "observation_schema_version": LITERATURE_OBSERVATION_SCHEMA_VERSION,
        "artifact_family": "literature",
        "artifact_type": "provider-output",
        "action": str(payload["action"]),
        "research_purpose": str(payload["research_purpose"]),
        "evidence_use_intent": str(payload["evidence_use_intent"]),
        "provider_binding_ref": str(payload["provider_binding_ref"]),
        "provider": str(provider["name"]),
        "access_method": str(payload["access_method"]),
        "actor_ref": str(payload["actor_ref"]),
        "source_refs": list(string_array(payload["source_refs"])),
        "provenance_refs": list(string_array(payload["provenance_refs"])),
        "completeness_status": str(mapping(payload["completeness"])["status"]),
        "canonical_member_posture": "papers-and-citation-edges-are-observation-members",
    }
    result, diagnostics = create_record(
        context,
        ResearchRecordRequest(
            record_kind="artifact",
            record_id=observation_id,
            profile="literature.provider-output",
            producer=str(payload["producer"]),
            topic_actor_name=str(payload["actor_ref"]),
            semantic_label="topic.records.artifacts",
            payload_file=selected_path,
            format_profile_ref=LITERATURE_OBSERVATION_PROFILE_REF,
            metadata=metadata,
            file_attachments=attachments,
        ),
        env=env,
        cwd=cwd,
    )
    if result.get("ok") is not True:
        return result, diagnostics
    projection = refresh_projection_after_commit(context, env=env)
    return {
        **result,
        "operation": "literature.record",
        "observation_id": observation_id,
        "canonical_commit": {
            "status": "committed",
            "record_id": observation_id,
            "one_logical_action": True,
            "member_counts": {
                "papers": len(object_array(payload["papers"])),
                "citation_edges": len(object_array(payload["citation_edges"])),
            },
        },
        "projection": projection,
    }, diagnostics


def list_literature_observations(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    limit: int | None = None,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    """List canonical literature observations without provider or network access."""

    selected_limit = _validated_limit(limit)
    store, diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    if store is None:
        return _runtime_unavailable("literature.observations.list", diagnostics), diagnostics
    try:
        structured = store.list_structured_payloads(
            topic_workspace_id=context.topic_workspace_id,
            format_profile_ref=LITERATURE_OBSERVATION_PROFILE_REF,
            limit=selected_limit,
        )
        observations = [
            _observation_summary(store, item, include_payload=False)
            for item in structured
            if store.get_lifecycle_record(item.record_id) is not None
        ]
        return {
            "ok": True,
            "mutated": False,
            "operation": "literature.observations.list",
            "count": len(observations),
            "observations": observations,
            "projection": projection_posture(store, context),
            "provider_io": False,
        }, diagnostics
    finally:
        store.close()


def show_literature_observation(
    context: EffectiveTopicContext,
    observation_id: str,
    *,
    env: Mapping[str, str],
) -> tuple[dict[str, Any], list[Diagnostic]]:
    """Show one canonical literature observation without provider or network access."""

    store, diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    if store is None:
        return _runtime_unavailable("literature.observations.show", diagnostics), diagnostics
    try:
        structured = store.get_structured_payload(observation_id)
        record = store.get_lifecycle_record(observation_id)
        if (
            structured is None
            or record is None
            or structured.format_profile_ref != LITERATURE_OBSERVATION_PROFILE_REF
            or record.topic_workspace_id != context.topic_workspace_id
        ):
            raise ResearchRecordError(
                f"Literature observation not found: {observation_id}",
                code="literature_observation_not_found",
            )
        return {
            "ok": True,
            "mutated": False,
            "operation": "literature.observations.show",
            "observation": _observation_summary(store, structured, include_payload=True),
            "projection": projection_posture(store, context),
            "provider_io": False,
        }, diagnostics
    finally:
        store.close()


def query_literature_papers(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    doi: str | None = None,
    arxiv_id: str | None = None,
    provider_id: str | None = None,
    title: str | None = None,
    year: int | None = None,
    observation_ref: str | None = None,
    limit: int | None = None,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    """Query derived paper occurrences by at least one provider-neutral selector."""

    if all(value is None for value in (doi, arxiv_id, provider_id, title, year, observation_ref)):
        raise ResearchRecordError(
            "Paper queries require at least one DOI, arXiv id, provider-qualified id, title, year, or observation selector.",
            code="literature_query_selector_required",
        )
    selected_limit = _validated_limit(limit)
    store, diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    if store is None:
        return _runtime_unavailable("literature.papers.query", diagnostics), diagnostics
    try:
        posture = projection_posture(store, context)
        if not posture["schema_compatible"]:
            return projection_required_payload("literature.papers.query", posture), diagnostics
        clauses: list[str] = []
        params: list[object] = []
        if doi is not None:
            clauses.append("doi = ?")
            params.append(normalized_doi(doi))
        if arxiv_id is not None:
            clauses.append("arxiv_id = ?")
            params.append(normalized_arxiv_id(arxiv_id))
        if provider_id is not None:
            provider_name, qualified_value = _parse_provider_selector(provider_id)
            clauses.extend(("provider_name = ?", "provider_id = ?"))
            params.extend((provider_name, qualified_value))
        if title is not None:
            clauses.append("lower(title) = lower(?)")
            params.append(title)
        if year is not None:
            clauses.append("publication_year = ?")
            params.append(year)
        if observation_ref is not None:
            clauses.append("source_record_id = ?")
            params.append(observation_ref)
        query = "SELECT * FROM literature_paper_occurrences WHERE " + " AND ".join(clauses)
        query += " ORDER BY observation_time DESC, source_record_id, paper_key, occurrence_id LIMIT ?"
        params.append(selected_limit)
        rows = [_paper_row(row) for row in store.connection.execute(query, params)]
        return {
            "ok": True,
            "mutated": False,
            "operation": "literature.papers.query",
            "count": len(rows),
            "occurrences": rows,
            "canonical_paper_records_created": False,
            "projection": posture,
            "provider_io": False,
        }, diagnostics
    finally:
        store.close()


def query_literature_citations(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    paper_key: str | None = None,
    observation_ref: str | None = None,
    direction: str | None = None,
    limit: int | None = None,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    """Query provider-reported derived citation edges."""

    if paper_key is None and observation_ref is None:
        raise ResearchRecordError(
            "Citation queries require a normalized paper key or source observation selector.",
            code="literature_query_selector_required",
        )
    if direction is not None and direction not in {"forward", "backward"}:
        raise ResearchRecordError(
            f"Unsupported citation direction: {direction}",
            code="literature_direction_invalid",
        )
    selected_limit = _validated_limit(limit)
    store, diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    if store is None:
        return _runtime_unavailable("literature.citations.query", diagnostics), diagnostics
    try:
        posture = projection_posture(store, context)
        if not posture["schema_compatible"]:
            return projection_required_payload("literature.citations.query", posture), diagnostics
        clauses: list[str] = []
        params: list[object] = []
        if paper_key is not None:
            if PAPER_KEY_RE.fullmatch(paper_key) is None:
                raise ResearchRecordError(
                    f"Malformed normalized paper key: {paper_key}",
                    code="literature_paper_key_invalid",
                )
            clauses.append("(citing_paper_key = ? OR cited_paper_key = ?)")
            params.extend((paper_key, paper_key))
        if observation_ref is not None:
            clauses.append("source_record_id = ?")
            params.append(observation_ref)
        if direction is not None:
            clauses.append("route_direction = ?")
            params.append(direction)
        query = "SELECT * FROM literature_citation_edges WHERE " + " AND ".join(clauses)
        query += " ORDER BY observation_time DESC, source_record_id, citing_paper_key, cited_paper_key, edge_id LIMIT ?"
        params.append(selected_limit)
        rows = [_citation_row(row) for row in store.connection.execute(query, params)]
        return {
            "ok": True,
            "mutated": False,
            "operation": "literature.citations.query",
            "count": len(rows),
            "edges": rows,
            "edge_posture": "provider-reported-not-full-text-verified",
            "canonical_citation_records_created": False,
            "projection": posture,
            "provider_io": False,
        }, diagnostics
    finally:
        store.close()


def rebuild_literature_index(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
) -> tuple[dict[str, Any], list[Diagnostic]]:
    """Explicitly replace only the derived literature query projection."""

    store, diagnostics = open_workspace_runtime(context, env=env, read_only=False)
    if store is None:
        return _runtime_unavailable("literature.index.rebuild", diagnostics), diagnostics
    try:
        source, skipped = projection_source(store, context)
        store.connection.execute("BEGIN IMMEDIATE")
        try:
            drop_projection_tables(store.connection)
            create_projection_tables(store.connection)
            counts = write_projection(store, context, source)
        except Exception:
            store.connection.rollback()
            raise
        store.connection.commit()
        return {
            "ok": True,
            "mutated": True,
            "operation": "literature.index.rebuild",
            "schema_version": LITERATURE_QUERY_INDEX_SCHEMA_VERSION,
            "counts": counts,
            "skipped_observations": skipped,
            "projection": projection_posture(store, context),
            "canonical_records_mutated": 0,
            "provider_io": False,
        }, diagnostics
    except sqlite3.Error as exc:
        raise ResearchRecordError(
            f"Literature projection rebuild failed: {exc}",
            code="literature_projection_rebuild_failed",
        ) from exc
    finally:
        store.close()


def validate_literature_index(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
) -> tuple[dict[str, Any], list[Diagnostic]]:
    """Validate the literature projection without creating or repairing tables."""

    store, diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    if store is None:
        return _runtime_unavailable("literature.index.validate", diagnostics), diagnostics
    try:
        posture = projection_posture(store, context)
        if not posture["schema_compatible"]:
            return projection_required_payload("literature.index.validate", posture), diagnostics
        issues = projection_issues(store, context)
        return {
            "ok": not issues,
            "mutated": False,
            "operation": "literature.index.validate",
            "status": "valid" if not issues else "invalid",
            "issue_count": len(issues),
            "issues": issues,
            "projection": posture,
            "provider_io": False,
        }, diagnostics
    finally:
        store.close()


def _observation_summary(
    store: WorkspaceRuntimeStore,
    structured: StructuredResearchPayloadRecord,
    *,
    include_payload: bool,
) -> dict[str, object]:
    record = store.get_lifecycle_record(structured.record_id)
    assert record is not None
    payload: dict[str, object] | None = None
    read_error: str | None = None
    try:
        payload = read_structured_payload(structured)
    except ResearchRecordError as exc:
        read_error = exc.message
    result: dict[str, object] = {
        "observation_id": structured.record_id,
        "record": record.to_json(),
        "validation": {
            "status": structured.validation_status,
            "diagnostics": structured.validation_diagnostics,
            "payload_read_error": read_error,
        },
        "payload_digest": structured.payload_digest,
        "format_profile_ref": structured.format_profile_ref,
        "schema_ref": structured.schema_ref,
        "schema_version": structured.schema_version,
        "provenance_refs": (
            list(string_array(payload.get("provenance_refs", [])))
            if payload is not None
            else structured.provenance_refs
        ),
        "completeness": payload.get("completeness") if payload is not None else None,
    }
    if include_payload:
        result["payload"] = payload
    return result


def _paper_row(row: sqlite3.Row) -> dict[str, object]:
    return {
        "occurrence_id": row["occurrence_id"],
        "source_observation_ref": row["source_record_id"],
        "payload_digest": row["payload_digest"],
        "observation_time": row["observation_time"],
        "paper_key": row["paper_key"],
        "doi": row["doi"],
        "arxiv_id": row["arxiv_id"],
        "provider_qualified_id": (
            {"provider": row["provider_name"], "id": row["provider_id"]}
            if row["provider_name"] is not None and row["provider_id"] is not None
            else None
        ),
        "title": row["title"],
        "publication_year": row["publication_year"],
        "locator": row["locator"],
        "normalized_paper": json.loads(row["paper_json"]),
        "canonical_record": False,
    }


def _citation_row(row: sqlite3.Row) -> dict[str, object]:
    return {
        "edge_id": row["edge_id"],
        "source_observation_ref": row["source_record_id"],
        "payload_digest": row["payload_digest"],
        "observation_time": row["observation_time"],
        "citing_paper_key": row["citing_paper_key"],
        "cited_paper_key": row["cited_paper_key"],
        "route_direction": row["route_direction"],
        "parent_seed_key": row["parent_seed_key"],
        "provider_reported": bool(row["provider_reported"]),
        "evidence_posture": "provider-reported-not-full-text-verified",
        "canonical_record": False,
    }


def _runtime_unavailable(operation: str, diagnostics: list[Diagnostic]) -> dict[str, object]:
    return {
        "ok": False,
        "mutated": False,
        "operation": operation,
        "error": {
            "code": "workspace_runtime_unavailable",
            "message": "The selected Topic Workspace Runtime is unavailable.",
        },
        "diagnostics": [item.to_json() for item in diagnostics],
    }


def _parse_provider_selector(value: str) -> tuple[str, str]:
    selected = value.removeprefix("provider:")
    provider, separator, provider_id = selected.partition(":")
    if not separator or not provider or not provider_id:
        raise ResearchRecordError(
            "Provider-qualified paper selectors must use PROVIDER:ID or provider:PROVIDER:ID.",
            code="literature_provider_selector_invalid",
        )
    return provider.lower(), provider_id


def _validated_limit(limit: int | None) -> int:
    selected = 100 if limit is None else limit
    if selected < 1 or selected > 10000:
        raise ResearchRecordError(
            "Literature query limit must be between 1 and 10000.",
            code="literature_limit_invalid",
        )
    return selected
