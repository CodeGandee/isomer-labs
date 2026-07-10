"""SQLAlchemy schema for the research record query index."""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import Column, Float, Integer, MetaData, Table, Text

SOURCE_AUTHORED = "authored"
SOURCE_PAYLOAD = "payload-derived"
SOURCE_FILE = "file-derived"
SOURCE_BODY = "body-inferred"
SOURCE_CANONICAL_LINEAGE = "canonical-lineage"

QUERY_INDEX_TABLE_NAMES = (
    "research_record_index",
    "research_record_edges",
    "research_record_files",
    "research_record_ideas",
    "research_record_routes",
    "research_record_metrics",
    "research_record_claims",
    "research_record_json_facts",
)

RELATION_KINDS = {
    "uses_input",
    "evidence_basis",
    "routes_to",
    "supports_claim",
    "derived_from",
    "revision_of",
    "selected_from",
    "merged_from",
    "follow_up_to",
    "supersedes",
    "produces",
    "materializes_file",
    "blocks",
    "cites",
    "summarizes",
}

EXPORT_VIEWS = {"graph", "dashboard", "timeline", "ideas", "experiments", "claims"}
QUERY_FACETS = {"ideas", "routes", "metrics", "claims", "facts"}
QUERY_INDEX_RECORD_KINDS = {
    "research_inquiry",
    "research_task",
    "run",
    "artifact",
    "gate",
    "finding",
    "research_claim",
    "evidence_item",
    "decision_record",
    "view_manifest",
}

metadata = MetaData()

record_index = Table(
    "research_record_index",
    metadata,
    Column("record_id", Text, primary_key=True),
    Column("research_topic_id", Text, nullable=False),
    Column("topic_workspace_id", Text, nullable=False),
    Column("record_kind", Text, nullable=False),
    Column("status", Text, nullable=False),
    Column("placeholder", Text),
    Column("artifact_family", Text),
    Column("semantic_id", Text),
    Column("semantic_id_source", Text),
    Column("artifact_type", Text),
    Column("procedure", Text),
    Column("terminal_status", Text),
    Column("revision_of_record_id", Text),
    Column("supersedes_record_id", Text),
    Column("profile", Text),
    Column("skill", Text),
    Column("producer", Text),
    Column("consumer", Text),
    Column("format_profile_ref", Text),
    Column("profile_family", Text),
    Column("profile_name", Text),
    Column("title", Text),
    Column("summary", Text),
    Column("content_path", Text),
    Column("payload_file_path", Text),
    Column("payload_media_type", Text),
    Column("payload_manifest_path", Text),
    Column("latest_for_semantic_id", Text),
    Column("rendered_markdown_path", Text),
    Column("validation_status", Text),
    Column("render_status", Text),
    Column("payload_digest", Text),
    Column("source_classification", Text, nullable=False),
    Column("stale", Integer, nullable=False, default=0),
    Column("created_at", Text, nullable=False),
    Column("updated_at", Text, nullable=False),
    Column("indexed_at", Text, nullable=False),
    Column("metadata_json", Text, nullable=False),
)

record_edges = Table(
    "research_record_edges",
    metadata,
    Column("id", Text, primary_key=True),
    Column("research_topic_id", Text, nullable=False),
    Column("topic_workspace_id", Text, nullable=False),
    Column("source_record_id", Text, nullable=False),
    Column("target_record_id", Text, nullable=False),
    Column("relation_kind", Text, nullable=False),
    Column("relation_role", Text),
    Column("source_field", Text),
    Column("source_classification", Text, nullable=False),
    Column("confidence", Float),
    Column("status", Text, nullable=False),
    Column("rationale", Text),
    Column("metadata_json", Text, nullable=False),
    Column("created_at", Text, nullable=False),
    Column("updated_at", Text, nullable=False),
)

record_files = Table(
    "research_record_files",
    metadata,
    Column("id", Text, primary_key=True),
    Column("research_topic_id", Text, nullable=False),
    Column("topic_workspace_id", Text, nullable=False),
    Column("record_id", Text, nullable=False),
    Column("path", Text, nullable=False),
    Column("file_role", Text, nullable=False),
    Column("semantic_label", Text),
    Column("operation_set_id", Text),
    Column("digest", Text),
    Column("size_bytes", Integer),
    Column("media_type", Text),
    Column("exists_flag", Integer, nullable=False),
    Column("status", Text, nullable=False),
    Column("source_field", Text),
    Column("source_classification", Text, nullable=False),
    Column("metadata_json", Text, nullable=False),
    Column("created_at", Text, nullable=False),
    Column("updated_at", Text, nullable=False),
)

record_ideas = Table(
    "research_record_ideas",
    metadata,
    Column("id", Text, primary_key=True),
    Column("research_topic_id", Text, nullable=False),
    Column("topic_workspace_id", Text, nullable=False),
    Column("record_id", Text, nullable=False),
    Column("idea_id", Text),
    Column("title", Text),
    Column("family", Text),
    Column("summary", Text),
    Column("status", Text),
    Column("selected", Integer, nullable=False),
    Column("source_json_path", Text),
    Column("metadata_json", Text, nullable=False),
    Column("created_at", Text, nullable=False),
)

record_routes = Table(
    "research_record_routes",
    metadata,
    Column("id", Text, primary_key=True),
    Column("research_topic_id", Text, nullable=False),
    Column("topic_workspace_id", Text, nullable=False),
    Column("record_id", Text, nullable=False),
    Column("decision", Text),
    Column("next_route", Text),
    Column("reason", Text),
    Column("selected_hypothesis_id", Text),
    Column("source_json_path", Text),
    Column("metadata_json", Text, nullable=False),
    Column("created_at", Text, nullable=False),
)

record_metrics = Table(
    "research_record_metrics",
    metadata,
    Column("id", Text, primary_key=True),
    Column("research_topic_id", Text, nullable=False),
    Column("topic_workspace_id", Text, nullable=False),
    Column("record_id", Text, nullable=False),
    Column("metric_key", Text, nullable=False),
    Column("metric_value", Text),
    Column("unit", Text),
    Column("comparator", Text),
    Column("scope", Text),
    Column("source_json_path", Text),
    Column("metadata_json", Text, nullable=False),
    Column("created_at", Text, nullable=False),
)

record_claims = Table(
    "research_record_claims",
    metadata,
    Column("id", Text, primary_key=True),
    Column("research_topic_id", Text, nullable=False),
    Column("topic_workspace_id", Text, nullable=False),
    Column("record_id", Text, nullable=False),
    Column("claim", Text),
    Column("metric_key", Text),
    Column("observed_value", Text),
    Column("expected", Text),
    Column("verdict", Text),
    Column("caveat", Text),
    Column("source_json_path", Text),
    Column("metadata_json", Text, nullable=False),
    Column("created_at", Text, nullable=False),
)

record_json_facts = Table(
    "research_record_json_facts",
    metadata,
    Column("id", Text, primary_key=True),
    Column("research_topic_id", Text, nullable=False),
    Column("topic_workspace_id", Text, nullable=False),
    Column("record_id", Text, nullable=False),
    Column("json_path", Text, nullable=False),
    Column("value_type", Text, nullable=False),
    Column("value_text", Text),
    Column("source_classification", Text, nullable=False),
    Column("metadata_json", Text, nullable=False),
    Column("created_at", Text, nullable=False),
)


@dataclass(frozen=True)
class IndexedRecordParts:
    index_row: dict[str, object]
    edge_rows: list[dict[str, object]]
    file_rows: list[dict[str, object]]
    idea_rows: list[dict[str, object]]
    route_rows: list[dict[str, object]]
    metric_rows: list[dict[str, object]]
    claim_rows: list[dict[str, object]]
    fact_rows: list[dict[str, object]]
