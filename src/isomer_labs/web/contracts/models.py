"""Schema checks for payloads consumed by the Project Web GUI.

These models describe UI read contracts, not canonical Workspace Runtime storage. They validate fields the GUI needs while allowing extra agent-authored metadata.
"""

from __future__ import annotations

from typing import Any, Literal, TypeVar

from pydantic import BaseModel, ConfigDict, Field, ValidationError


class GuiContractModel(BaseModel):
    """Base model that preserves room for richer read-model metadata."""

    model_config = ConfigDict(extra="allow")


class DiagnosticContract(GuiContractModel):
    severity: str | None = None
    code: str | None = None
    message: str | None = None


class ErrorContract(GuiContractModel):
    code: str
    message: str


class TopicOverviewSourceContract(GuiContractModel):
    semantic_label: str
    exists: bool
    content_markdown: str | None
    path: str | None = None
    content_bytes: int | None = None
    content_cap_bytes: int | None = None


class TopicOverviewResponseContract(GuiContractModel):
    ok: bool
    mutated: bool
    topic_id: str
    topic_workspace_id: str | None
    overview: TopicOverviewSourceContract
    topic_payload: Any | None
    runtime_payload: Any | None
    diagnostics: list[DiagnosticContract]
    error: ErrorContract | None = None


class TopicGraphNodeContract(GuiContractModel):
    id: str
    record_id: str
    material_kind: str
    density_class: str
    title: str
    summary: str | None = None
    status: str | None = None
    idea_id: str | None = None
    display_key: str | None = None
    exploration_state: Literal["unknown", "unexplored", "exploring", "explored"] | None = None
    decision_state: Literal["unknown", "open", "shortlisted", "selected", "deferred", "closed"] | None = None
    evidence_state: Literal["unknown", "unassessed", "inconclusive", "supported", "mixed", "refuted"] | None = None
    archive_state: Literal["active", "archived"] | None = None
    visibility: Literal["primary", "supporting", "hidden"] | None = None
    needs_classification: list[str] = Field(default_factory=list)
    decision_summary: dict[str, Any] | None = None
    transition_refs: list[str] = Field(default_factory=list)
    source: dict[str, Any] | None = None
    detail_refs: dict[str, Any] | None = None
    renderer_hints: dict[str, Any] | None = None


class CanonicalIdeaPortfolioNodeContract(TopicGraphNodeContract):
    """Required fields for a canonical portfolio node, separate from legacy fallback nodes."""

    idea_id: str
    exploration_state: Literal["unknown", "unexplored", "exploring", "explored"]
    decision_state: Literal["unknown", "open", "shortlisted", "selected", "deferred", "closed"]
    evidence_state: Literal["unknown", "unassessed", "inconclusive", "supported", "mixed", "refuted"]
    archive_state: Literal["active", "archived"]
    visibility: Literal["primary", "supporting", "hidden"]
    detail_refs: dict[str, Any]


class IdeaPortfolioPresetContract(GuiContractModel):
    id: Literal["current", "all-proposed", "open-for-exploration", "unexplored", "exploring", "explored", "selected", "deferred", "closed", "needs-classification"]
    label: str
    description: str
    predicate: dict[str, Any]


class IdeaPortfolioMetadataContract(GuiContractModel):
    preset: IdeaPortfolioPresetContract
    available_presets: list[IdeaPortfolioPresetContract]
    explicit_filters: dict[str, list[str]]
    applied_predicate: dict[str, Any]
    source_counts: dict[str, Any]
    visible_counts: dict[str, Any]
    omitted_cross_boundary_edge_count: int
    source_topology_complete: bool


class TopicGraphEdgeContract(GuiContractModel):
    id: str
    source: str
    target: str
    relation_kind: str
    canonical: bool
    lineage_kind: str | None = None
    generation_id: str | None = None
    source_record_refs: list[str] | None = None
    metadata: dict[str, Any] | None = None


class TopicGraphGroupContract(GuiContractModel):
    id: str
    group_kind: str
    title: str
    node_ids: list[str]
    diagnostics: list[DiagnosticContract] = Field(default_factory=list)


class TopicGraphPagingContract(GuiContractModel):
    cursor: str | None = None
    next_cursor: str | None = None
    truncated: bool


class TopicGraphProjectionContract(GuiContractModel):
    seed_node_ids: list[str]
    resolved_seed_node_ids: list[str]
    unresolved_seed_node_ids: list[str]
    hop_radius: int
    direction: str
    relation_kinds: list[str]
    edge_mode: str
    source_node_count: int
    source_edge_count: int
    visible_node_count: int
    visible_edge_count: int
    source_index_revision: str | None = None
    topology_complete: bool


class TopicGraphResponseContract(GuiContractModel):
    ok: bool
    mutated: bool
    topic_id: str
    topic_workspace_id: str
    graph_scope: str
    renderer_hint: str
    generated_at: str
    nodes: list[TopicGraphNodeContract]
    edges: list[TopicGraphEdgeContract]
    groups: list[TopicGraphGroupContract]
    facets: dict[str, Any]
    diagnostics: list[DiagnosticContract]
    topology_complete: bool = False
    total_node_count: int = 0
    total_edge_count: int = 0
    source_node_count: int = 0
    source_edge_count: int = 0
    visible_node_count: int = 0
    visible_edge_count: int = 0
    portfolio: dict[str, Any] = Field(default_factory=dict)
    paging: TopicGraphPagingContract | None = None
    projection: TopicGraphProjectionContract | None = None
    error: ErrorContract | None = None


class IdeaSourceContract(GuiContractModel):
    source_kind: str
    source_record_id: str | None = None
    source_json_path: str | None = None
    source_json_available: bool
    source_json_truncated: bool
    source_json_bytes: int
    source_fragment_status: str | None = None
    source_classification: str | None = None
    source_json: Any | None = None


class IdeaDetailResponseContract(GuiContractModel):
    ok: bool
    mutated: bool
    topic_id: str
    topic_workspace_id: str
    idea_id: str
    idea: dict[str, Any] | None
    realizations: list[dict[str, Any]]
    generation_groups: list[dict[str, Any]]
    incoming_edges: list[dict[str, Any]]
    outgoing_edges: list[dict[str, Any]]
    source: IdeaSourceContract
    diagnostics: list[DiagnosticContract]
    exists: bool | None = None
    latest_realization: dict[str, Any] | None = None
    latest_record: dict[str, Any] | None = None
    idea_content: dict[str, Any] | None = None
    source_provenance: dict[str, Any] | None = None
    error: ErrorContract | None = None


class IdeaDecisionContextResponseContract(GuiContractModel):
    ok: bool
    mutated: Literal[False]
    topic_id: str
    topic_workspace_id: str
    operation: str
    idea_id: str | None = None
    decision_record_id: str | None = None
    decisions: list[dict[str, Any]]
    ideas: list[dict[str, Any]]
    transitions: list[dict[str, Any]]
    reopen_history: list[dict[str, Any]] = Field(default_factory=list)
    index_revision: str | None = None
    diagnostics: list[DiagnosticContract]
    error: ErrorContract | None = None


class IdeaTraversalResponseContract(GuiContractModel):
    ok: bool
    mutated: Literal[False]
    topic_id: str
    topic_workspace_id: str
    operation: str
    roots: list[str]
    resolved_roots: list[str]
    unresolved_roots: list[str]
    direction: Literal["ancestors", "descendants"]
    relation_kinds: list[str]
    nodes: list[dict[str, Any]]
    edges: list[dict[str, Any]]
    topology_complete: bool
    limiting_bounds: list[str]
    maximum_observed_depth: int
    counts: dict[str, int]
    bounds: dict[str, int]
    continuation: dict[str, Any] | None
    index_revision: str | None = None
    diagnostics: list[DiagnosticContract]
    error: ErrorContract | None = None


class IdeaSteeringResponseContract(GuiContractModel):
    ok: bool
    mutated: bool
    status: Literal["accepted", "conflict", "gate_required", "blocked"]
    topic_id: str | None = None
    topic_workspace_id: str | None = None
    operation_id: str | None = None
    replayed: bool = False
    canonical_accepted: bool = False
    decision_record_ref: str | None = None
    research_inquiry_ref: str | None = None
    research_task_ref: str | None = None
    provenance_record_ref: str | None = None
    handoff_ref: str | None = None
    transition_refs: list[str] = Field(default_factory=list)
    decision_option_refs: list[str] = Field(default_factory=list)
    resulting_ideas: list[dict[str, Any]] = Field(default_factory=list)
    current_ideas: list[dict[str, Any]] = Field(default_factory=list)
    new_index_revision: str | None = None
    current_index_revision: str | None = None
    pending_index_revision: bool | None = None
    dispatch_status: str | None = None
    dispatch_retry_ref: str | None = None
    dispatch: dict[str, Any] | None = None
    diagnostics: list[DiagnosticContract]
    error: ErrorContract | None = None


class RecordViewerDescriptorContract(GuiContractModel):
    ok: bool
    mutated: bool
    record_id: str
    viewer_kind: str
    exists: bool
    diagnostics: list[DiagnosticContract]
    topic_id: str | None = None
    title: str | None = None
    primary_content_url: str | None = None
    detail_url: str | None = None
    render_url: str | None = None
    files_url: str | None = None
    facets_url: str | None = None
    media_type: str | None = None
    topic_workspace_relative_path: str | None = None
    absolute_filepath: str | None = None
    direct_parent_idea: dict[str, Any] | None = None
    record_inspection: dict[str, Any] | None = None
    error: ErrorContract | None = None


class RecordFileContract(GuiContractModel):
    file_role: str
    exists: bool
    openable: bool
    id: str | None = None
    path: str | None = None
    resolved_path: str | None = None
    open_blocked_reason: str | None = None


class RecordFilesResponseContract(GuiContractModel):
    ok: bool
    mutated: bool
    topic_id: str
    record_id: str
    files: list[RecordFileContract]
    diagnostics: list[DiagnosticContract]
    operation: str | None = None
    error: ErrorContract | None = None


class RecordDetailResponseContract(GuiContractModel):
    ok: bool
    mutated: bool
    operation: str
    record: dict[str, Any]
    topic_workspace_relative_path: str | None = None
    absolute_filepath: str | None = None
    direct_parent_idea: dict[str, Any] | None = None
    record_inspection: dict[str, Any] | None = None
    diagnostics: list[DiagnosticContract] = Field(default_factory=list)


class RecordRenderResponseContract(GuiContractModel):
    ok: bool
    mutated: bool
    operation: str
    record: dict[str, Any]
    render: dict[str, Any]
    topic_workspace_relative_path: str | None = None
    absolute_filepath: str | None = None
    direct_parent_idea: dict[str, Any] | None = None
    record_inspection: dict[str, Any] | None = None
    diagnostics: list[DiagnosticContract] = Field(default_factory=list)


class RecordLineageResponseContract(GuiContractModel):
    ok: bool
    mutated: bool
    operation: str
    record_id: str
    nodes: list[dict[str, Any]]
    edges: list[dict[str, Any]]
    diagnostics: list[DiagnosticContract]


class RecordSiblingsResponseContract(GuiContractModel):
    ok: bool
    mutated: bool
    operation: str
    record_id: str
    nodes: list[dict[str, Any]]
    edges: list[dict[str, Any]]
    generation_groups: list[dict[str, Any]]
    diagnostics: list[DiagnosticContract]


class RecordFacetsResponseContract(GuiContractModel):
    ok: bool
    mutated: bool
    operation: str
    record_id: str
    diagnostics: list[DiagnosticContract]


T = TypeVar("T", bound=GuiContractModel)


def validate_gui_payload(payload: Any, schema: type[T]) -> T:
    """Validate a GUI payload and raise Pydantic validation errors on failure."""

    return schema.model_validate(payload)


def ensure_gui_payload(payload: dict[str, Any], schema: type[GuiContractModel], *, contract_name: str) -> dict[str, Any]:
    """Return payload if it matches the UI contract, otherwise return a diagnostic-safe payload."""

    try:
        validate_gui_payload(payload, schema)
    except ValidationError as exc:
        diagnostics = list(payload.get("diagnostics", [])) if isinstance(payload.get("diagnostics"), list) else []
        diagnostics.append(
            {
                "severity": "error",
                "code": "gui_contract_validation_failed",
                "concept": "Project Web UI Contract",
                "message": f"Payload does not satisfy Project Web UI contract `{contract_name}`.",
                "details": exc.errors(include_url=False),
            }
        )
        return {
            **payload,
            "ok": False,
            "mutated": bool(payload.get("mutated", False)),
            "diagnostics": diagnostics,
        }
    return payload
