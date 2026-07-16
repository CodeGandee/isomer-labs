import { z } from "zod";

export const DiagnosticSchema = z
  .object({
    severity: z.string().optional(),
    code: z.string().optional(),
    message: z.string().optional(),
  })
  .passthrough();

export const TopicSchema = z
  .object({
    id: z.string(),
    status: z.string().optional(),
    topic_workspace_id: z.string().optional(),
    topic_workspace_path: z.string().optional(),
    topic_statement: z.string().nullable().optional(),
  })
  .passthrough();

export const TopicGraphNodeSchema = z
  .object({
    id: z.string(),
    record_id: z.string(),
    material_kind: z.string(),
    density_class: z.string(),
    title: z.string(),
    summary: z.string().nullable().optional(),
    status: z.string().nullable().optional(),
    selected: z.boolean().nullable().optional(),
    producer: z.string().nullable().optional(),
    skill: z.string().nullable().optional(),
    created_at: z.string().nullable().optional(),
    updated_at: z.string().nullable().optional(),
    source: z.record(z.string(), z.unknown()).optional(),
    detail_refs: z.record(z.string(), z.string().nullable()).optional(),
    renderer_hints: z.record(z.string(), z.unknown()).optional(),
    idea_id: z.string().optional(),
    display_key: z.string().nullable().optional(),
    exploration_state: z.string().nullable().optional(),
    decision_state: z.string().nullable().optional(),
    evidence_state: z.string().nullable().optional(),
    archive_state: z.string().nullable().optional(),
    visibility: z.string().nullable().optional(),
    backend_selected: z.boolean().optional(),
    needs_classification: z.array(z.string()).optional(),
    transition_refs: z.array(z.string()).optional(),
    decision_record_ids: z.array(z.string()).optional(),
    generation_ids: z.array(z.string()).optional(),
    decision_summary: z.record(z.string(), z.unknown()).optional(),
    steering_eligibility: z.record(z.string(), z.unknown()).optional(),
  })
  .passthrough();

export const TopicGraphEdgeSchema = z
  .object({
    id: z.string(),
    source: z.string(),
    target: z.string(),
    relation_kind: z.string(),
    canonical: z.boolean(),
    lineage_kind: z.string().nullable().optional(),
    generation_id: z.string().nullable().optional(),
    status: z.string().nullable().optional(),
    rationale: z.string().nullable().optional(),
    confidence: z.number().nullable().optional(),
    source_classification: z.string().nullable().optional(),
    collapsed: z.boolean().optional(),
    source_relationship_refs: z.array(z.string()).optional(),
    source_record_refs: z.array(z.string()).optional(),
    source_classifications: z.array(z.string()).optional(),
    projection_path: z.array(z.record(z.string(), z.unknown())).optional(),
    metadata: z.record(z.string(), z.unknown()).optional(),
  })
  .passthrough();

export const TopicGraphGroupSchema = z
  .object({
    id: z.string(),
    group_kind: z.string(),
    title: z.string(),
    purpose: z.string().nullable().optional(),
    parent_set_digest: z.string().nullable().optional(),
    node_ids: z.array(z.string()),
    diagnostics: z.array(DiagnosticSchema).optional(),
  })
  .passthrough();

export const TopicGraphViewSchema = z
  .object({
    ok: z.boolean(),
    mutated: z.boolean(),
    topic_id: z.string(),
    topic_workspace_id: z.string(),
    graph_scope: z.string(),
    renderer_hint: z.string(),
    index_revision: z.string().nullable().optional(),
    generated_at: z.string(),
    nodes: z.array(TopicGraphNodeSchema),
    edges: z.array(TopicGraphEdgeSchema),
    groups: z.array(TopicGraphGroupSchema),
    facets: z.record(z.string(), z.unknown()),
    portfolio: z
      .object({
        preset: z
          .object({
            id: z.string(),
            label: z.string(),
            description: z.string().optional(),
            predicate: z.record(z.string(), z.unknown()),
          })
          .passthrough()
          .nullable()
          .optional(),
        available_presets: z.array(z.record(z.string(), z.unknown())).optional(),
        explicit_filters: z.record(z.string(), z.unknown()).optional(),
        applied_predicate: z.record(z.string(), z.unknown()).optional(),
        source_counts: z.record(z.string(), z.unknown()).optional(),
        visible_counts: z.record(z.string(), z.unknown()).optional(),
        omitted_cross_boundary_edge_count: z.number().int().nonnegative().optional(),
        source_topology_complete: z.boolean().optional(),
      })
      .passthrough()
      .optional(),
    topology_complete: z.boolean().optional(),
    total_node_count: z.number().int().nonnegative().optional(),
    total_edge_count: z.number().int().nonnegative().optional(),
    paging: z
      .object({
        cursor: z.string().nullable().optional(),
        next_cursor: z.string().nullable().optional(),
        truncated: z.boolean(),
      })
      .optional(),
    projection: z
      .object({
        seed_node_ids: z.array(z.string()),
        resolved_seed_node_ids: z.array(z.string()),
        unresolved_seed_node_ids: z.array(z.string()),
        hop_radius: z.number().int().nonnegative(),
        direction: z.enum(["incoming", "outgoing", "both"]),
        relation_kinds: z.array(z.string()),
        edge_mode: z.enum(["induced", "traversal"]),
        source_node_count: z.number().int().nonnegative(),
        source_edge_count: z.number().int().nonnegative(),
        visible_node_count: z.number().int().nonnegative(),
        visible_edge_count: z.number().int().nonnegative(),
        source_index_revision: z.string().nullable().optional(),
        topology_complete: z.boolean(),
      })
      .passthrough()
      .nullable()
      .optional(),
    diagnostics: z.array(DiagnosticSchema),
    error: z
      .object({
        code: z.string(),
        message: z.string(),
      })
      .passthrough()
      .optional(),
  })
  .passthrough();

export const IdeaDecisionContextResponseSchema = z
  .object({
    ok: z.boolean(),
    mutated: z.boolean(),
    topic_id: z.string(),
    topic_workspace_id: z.string(),
    operation: z.string(),
    idea_id: z.string().nullable().optional(),
    decision_record_id: z.string().nullable().optional(),
    decisions: z.array(z.record(z.string(), z.unknown())),
    ideas: z.array(z.record(z.string(), z.unknown())),
    transitions: z.array(z.record(z.string(), z.unknown())),
    reopen_history: z.array(z.record(z.string(), z.unknown())).optional(),
    index_revision: z.string().nullable().optional(),
    diagnostics: z.array(DiagnosticSchema),
    error: z.object({ code: z.string(), message: z.string() }).passthrough().optional(),
  })
  .passthrough();

export const IdeaTraversalResponseSchema = z
  .object({
    ok: z.boolean(),
    mutated: z.boolean(),
    topic_id: z.string(),
    topic_workspace_id: z.string(),
    operation: z.string(),
    roots: z.array(z.string()),
    resolved_roots: z.array(z.string()),
    unresolved_roots: z.array(z.string()),
    direction: z.enum(["ancestors", "descendants"]),
    relation_kinds: z.array(z.string()),
    nodes: z.array(z.record(z.string(), z.unknown())),
    edges: z.array(z.record(z.string(), z.unknown())),
    topology_complete: z.boolean(),
    limiting_bounds: z.array(z.string()),
    maximum_observed_depth: z.number().int().nonnegative(),
    counts: z.record(z.string(), z.number().int().nonnegative()),
    bounds: z.record(z.string(), z.number().int().nonnegative()),
    continuation: z.record(z.string(), z.unknown()).nullable(),
    index_revision: z.string().nullable().optional(),
    diagnostics: z.array(DiagnosticSchema),
    error: z.object({ code: z.string(), message: z.string() }).passthrough().optional(),
  })
  .passthrough();

export const IdeaSteeringResponseSchema = z
  .object({
    ok: z.boolean(),
    mutated: z.boolean(),
    status: z.enum(["accepted", "conflict", "gate_required", "blocked"]),
    topic_id: z.string().nullable().optional(),
    topic_workspace_id: z.string().nullable().optional(),
    operation_id: z.string().nullable().optional(),
    replayed: z.boolean().optional(),
    canonical_accepted: z.boolean().optional(),
    decision_record_ref: z.string().nullable().optional(),
    research_inquiry_ref: z.string().nullable().optional(),
    research_task_ref: z.string().nullable().optional(),
    provenance_record_ref: z.string().nullable().optional(),
    handoff_ref: z.string().nullable().optional(),
    transition_refs: z.array(z.string()).optional(),
    decision_option_refs: z.array(z.string()).optional(),
    resulting_ideas: z.array(z.record(z.string(), z.unknown())).optional(),
    current_ideas: z.array(z.record(z.string(), z.unknown())).optional(),
    new_index_revision: z.string().nullable().optional(),
    current_index_revision: z.string().nullable().optional(),
    dispatch_status: z.string().nullable().optional(),
    dispatch: z.record(z.string(), z.unknown()).nullable().optional(),
    diagnostics: z.array(DiagnosticSchema),
    error: z.object({ code: z.string(), message: z.string() }).passthrough().optional(),
  })
  .passthrough();

export type ResearchIdeaSteeringRequest = {
  action: "explore" | "explore_instead";
  target_idea_id: string;
  actor_ref: string;
  idempotency_key: string;
  expected_index_revision?: string;
  expected_states?: Record<string, Record<string, string>>;
  replaced_idea_ids?: string[];
  replacement_dispositions?: Record<string, "deferred" | "closed">;
  replacement_closure_reasons?: Record<string, string>;
  rationale?: string;
  user_prompt?: string;
  reopen_confirmed?: boolean;
  gate_policy?: "none" | "reopen" | "replace" | "all";
  gate_resolution_ref?: string;
  agent_team_instance_id?: string;
  source_agent_instance_id?: string;
  target_agent_instance_id?: string;
  dispatch?: boolean;
};

export const TopicsResponseSchema = z
  .object({
    ok: z.boolean(),
    mutated: z.boolean(),
    topics: z.array(TopicSchema),
    diagnostics: z.array(DiagnosticSchema).optional(),
  })
  .passthrough();

export const ProjectResponseSchema = z
  .object({
    ok: z.boolean(),
    mutated: z.boolean(),
    project: z.record(z.string(), z.unknown()).nullable().optional(),
    diagnostics: z.array(DiagnosticSchema).optional(),
  })
  .passthrough();

export const TopicOverviewSourceSchema = z
  .object({
    semantic_label: z.string(),
    path: z.string().optional(),
    exists: z.boolean(),
    content_markdown: z.string().nullable().optional(),
    content_bytes: z.number().optional(),
    content_cap_bytes: z.number().optional(),
  })
  .passthrough();

export const TopicOverviewResponseSchema = z
  .object({
    ok: z.boolean(),
    mutated: z.boolean(),
    topic_id: z.string(),
    topic_workspace_id: z.string().nullable().optional(),
    overview: TopicOverviewSourceSchema,
    topic_payload: z.unknown().nullable().optional(),
    runtime_payload: z.unknown().nullable().optional(),
    diagnostics: z.array(DiagnosticSchema).optional(),
    error: z
      .object({
        code: z.string(),
        message: z.string(),
      })
      .passthrough()
      .optional(),
  })
  .passthrough();

export const TopicOverviewJsonResponseSchema = z
  .object({
    ok: z.boolean(),
    mutated: z.boolean(),
    topic_id: z.string(),
    topic_workspace_id: z.string().nullable().optional(),
    topic_payload: z.unknown().nullable().optional(),
    runtime_payload: z.unknown().nullable().optional(),
    diagnostics: z.array(DiagnosticSchema).optional(),
    error: z
      .object({
        code: z.string(),
        message: z.string(),
      })
      .passthrough()
      .optional(),
  })
  .passthrough();

export const RecordSummarySchema = z
  .object({
    record_id: z.string(),
    record_kind: z.string().optional(),
    status: z.string().optional(),
    title: z.string().nullable().optional(),
    summary: z.string().nullable().optional(),
    profile: z.string().nullable().optional(),
    producer: z.string().nullable().optional(),
    skill: z.string().nullable().optional(),
    updated_at: z.string().optional(),
  })
  .passthrough();

export const IdeaDetailSourceSchema = z
  .object({
    source_kind: z.string(),
    source_record_id: z.string().nullable().optional(),
    source_json_path: z.string().nullable().optional(),
    source_json_available: z.boolean().optional(),
    source_json_truncated: z.boolean().optional(),
    source_json_bytes: z.number().optional(),
    source_json_cap_bytes: z.number().optional(),
    source_fragment_status: z.string().nullable().optional(),
    source_classification: z.string().nullable().optional(),
    full_source_url: z.string().optional(),
    payload_digest: z.string().optional(),
    payload_file_path: z.string().nullable().optional(),
    payload_media_type: z.string().optional(),
    source_json: z.unknown().optional(),
  })
  .passthrough();

export const IdeaDetailResponseSchema = z
  .object({
    ok: z.boolean(),
    mutated: z.boolean(),
    topic_id: z.string(),
    topic_workspace_id: z.string().optional(),
    idea_id: z.string(),
    exists: z.boolean().optional(),
    idea: z.record(z.string(), z.unknown()).nullable().optional(),
    realizations: z.array(z.record(z.string(), z.unknown())).optional(),
    latest_realization: z.record(z.string(), z.unknown()).nullable().optional(),
    latest_record: z.record(z.string(), z.unknown()).nullable().optional(),
    generation_groups: z.array(z.record(z.string(), z.unknown())).optional(),
    incoming_edges: z.array(z.record(z.string(), z.unknown())).optional(),
    outgoing_edges: z.array(z.record(z.string(), z.unknown())).optional(),
    idea_content: z.record(z.string(), z.unknown()).nullable().optional(),
    source_provenance: z.record(z.string(), z.unknown()).nullable().optional(),
    source: IdeaDetailSourceSchema.optional(),
    diagnostics: z.array(DiagnosticSchema).optional(),
    error: z
      .object({
        code: z.string(),
        message: z.string(),
      })
      .passthrough()
      .optional(),
  })
  .passthrough();

export const RecordsResponseSchema = z
  .object({
    ok: z.boolean(),
    mutated: z.boolean(),
    records: z.array(RecordSummarySchema).optional(),
    projection: z.record(z.string(), z.unknown()).optional(),
    limit: z.number().nullable().optional(),
    returned_count: z.number().optional(),
    diagnostics: z.array(DiagnosticSchema).optional(),
  })
  .passthrough();

export const ViewerDescriptorSchema = z
  .object({
    ok: z.boolean(),
    mutated: z.boolean(),
    topic_id: z.string().optional(),
    record_id: z.string(),
    title: z.string().optional(),
    viewer_kind: z.string(),
    primary_content_url: z.string().nullable().optional(),
    detail_url: z.string().optional(),
    render_url: z.string().nullable().optional(),
    files_url: z.string().nullable().optional(),
    facets_url: z.string().nullable().optional(),
    media_type: z.string().nullable().optional(),
    topic_workspace_relative_path: z.string().nullable().optional(),
    absolute_filepath: z.string().nullable().optional(),
    direct_parent_idea: z.record(z.string(), z.unknown()).nullable().optional(),
    record_inspection: z.record(z.string(), z.unknown()).nullable().optional(),
    exists: z.boolean(),
    diagnostics: z.array(DiagnosticSchema).optional(),
    error: z
      .object({
        code: z.string(),
        message: z.string(),
      })
      .passthrough()
      .optional(),
  })
  .passthrough();

export const RecordDetailResponseSchema = z
  .object({
    ok: z.boolean(),
    mutated: z.boolean(),
    operation: z.string(),
    record: z.record(z.string(), z.unknown()),
    structured_payload: z.record(z.string(), z.unknown()).nullable().optional(),
    topic_workspace_relative_path: z.string().nullable().optional(),
    absolute_filepath: z.string().nullable().optional(),
    direct_parent_idea: z.record(z.string(), z.unknown()).nullable().optional(),
    record_inspection: z.record(z.string(), z.unknown()).nullable().optional(),
    diagnostics: z.array(DiagnosticSchema).optional(),
    error: z
      .object({
        code: z.string(),
        message: z.string(),
      })
      .passthrough()
      .optional(),
  })
  .passthrough();

export const RecordRenderResponseSchema = z
  .object({
    ok: z.boolean(),
    mutated: z.boolean(),
    operation: z.string(),
    record: z.record(z.string(), z.unknown()),
    render: z.record(z.string(), z.unknown()),
    topic_workspace_relative_path: z.string().nullable().optional(),
    absolute_filepath: z.string().nullable().optional(),
    direct_parent_idea: z.record(z.string(), z.unknown()).nullable().optional(),
    record_inspection: z.record(z.string(), z.unknown()).nullable().optional(),
    diagnostics: z.array(DiagnosticSchema).optional(),
    error: z
      .object({
        code: z.string(),
        message: z.string(),
      })
      .passthrough()
      .optional(),
  })
  .passthrough();

export const ExplorerNodeSchema = z
  .object({
    id: z.string(),
    parent_id: z.string().nullable().optional(),
    label: z.string(),
    item_kind: z.string(),
    icon_hint: z.string().nullable().optional(),
    badge_text: z.string().nullable().optional(),
    diagnostics_count: z.number().optional(),
    warning: z.boolean().optional(),
    openability_state: z.string().optional(),
    openable_item_id: z.string().nullable().optional(),
    topic_id: z.string().nullable().optional(),
    has_children: z.boolean().optional(),
    children_loaded: z.boolean().optional(),
    expanded_by_default: z.boolean().optional(),
    metadata: z.record(z.string(), z.unknown()).optional(),
  })
  .passthrough();

export const OpenableItemDescriptorSchema = z
  .object({
    ok: z.boolean(),
    mutated: z.boolean(),
    openable_item_id: z.string(),
    tab_id: z.string().optional(),
    item_kind: z.string(),
    title: z.string().optional(),
    preferred_tab_component: z.string().optional(),
    topic_id: z.string().nullable().optional(),
    record_id: z.string().nullable().optional(),
    idea_id: z.string().nullable().optional(),
    graph_scope: z.string().nullable().optional(),
    content_url: z.string().nullable().optional(),
    detail_urls: z.record(z.string(), z.string()).optional(),
    media_type: z.string().nullable().optional(),
    viewer_kind: z.string().nullable().optional(),
    exists: z.boolean().optional(),
    diagnostics: z.array(DiagnosticSchema).optional(),
    error: z
      .object({
        code: z.string(),
        message: z.string(),
      })
      .passthrough()
      .optional(),
  })
  .passthrough();

export const ProjectExplorerResponseSchema = z
  .object({
    ok: z.boolean(),
    mutated: z.boolean(),
    revision: z.string(),
    root_node_ids: z.array(z.string()),
    nodes: z.array(ExplorerNodeSchema),
    descriptors: z.array(OpenableItemDescriptorSchema).optional(),
    diagnostics: z.array(DiagnosticSchema).optional(),
  })
  .passthrough();

export const TopicChangeEventSchema = z
  .object({
    ok: z.boolean().optional(),
    mutated: z.boolean().optional(),
    event_id: z.string(),
    event_type: z.string(),
    topic_id: z.string(),
    topic_workspace_id: z.string().nullable().optional(),
    index_revision: z.string().nullable().optional(),
    changed_record_ids: z.array(z.string()).optional(),
    changed_material_kinds: z.array(z.string()).optional(),
    graph_scopes: z.array(z.string()).optional(),
    diagnostics_count: z.number().optional(),
    occurred_at: z.string(),
    diagnostics: z.array(DiagnosticSchema).optional(),
  })
  .passthrough();

export const RecentErrorsResponseSchema = z
  .object({
    ok: z.boolean(),
    mutated: z.boolean(),
    topic_id: z.string(),
    errors: z.array(
      z
        .object({
          occurred_at: z.string(),
          topic_id: z.string(),
          source_view: z.string(),
          severity: z.string(),
          code: z.string().nullable().optional(),
          message: z.string().nullable().optional(),
        })
        .passthrough(),
    ),
    diagnostics: z.array(DiagnosticSchema).optional(),
  })
  .passthrough();

export type Diagnostic = z.infer<typeof DiagnosticSchema>;
export type Topic = z.infer<typeof TopicSchema>;
export type TopicGraphNode = z.infer<typeof TopicGraphNodeSchema>;
export type TopicGraphEdge = z.infer<typeof TopicGraphEdgeSchema>;
export type TopicGraphView = z.infer<typeof TopicGraphViewSchema>;
export type TopicGraphGroup = z.infer<typeof TopicGraphGroupSchema>;
export type IdeaDecisionContextResponse = z.infer<typeof IdeaDecisionContextResponseSchema>;
export type IdeaTraversalResponse = z.infer<typeof IdeaTraversalResponseSchema>;
export type IdeaSteeringResponse = z.infer<typeof IdeaSteeringResponseSchema>;
export type TopicChangeEvent = z.infer<typeof TopicChangeEventSchema>;
export type RecentErrorsResponse = z.infer<typeof RecentErrorsResponseSchema>;
export type TopicOverviewResponse = z.infer<typeof TopicOverviewResponseSchema>;
export type TopicOverviewJsonResponse = z.infer<typeof TopicOverviewJsonResponseSchema>;
export type RecordSummary = z.infer<typeof RecordSummarySchema>;
export type IdeaDetailResponse = z.infer<typeof IdeaDetailResponseSchema>;
export type ViewerDescriptor = z.infer<typeof ViewerDescriptorSchema>;
export type RecordDetailResponse = z.infer<typeof RecordDetailResponseSchema>;
export type RecordRenderResponse = z.infer<typeof RecordRenderResponseSchema>;
export type ExplorerNode = z.infer<typeof ExplorerNodeSchema>;
export type ProjectExplorerResponse = z.infer<typeof ProjectExplorerResponseSchema>;
export type OpenableItemDescriptor = z.infer<typeof OpenableItemDescriptorSchema>;

export type GraphScope = "idea-lineage" | "idea-timeline";
export type RendererChoice = "auto" | "react-flow" | "sigma";
