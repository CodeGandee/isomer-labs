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
    one_liner: z.string().nullable().optional(),
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
    paging: z
      .object({
        cursor: z.string().nullable().optional(),
        next_cursor: z.string().nullable().optional(),
        truncated: z.boolean(),
      })
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

export const RecordsResponseSchema = z
  .object({
    ok: z.boolean(),
    mutated: z.boolean(),
    records: z.array(RecordSummarySchema).optional(),
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

export type Diagnostic = z.infer<typeof DiagnosticSchema>;
export type Topic = z.infer<typeof TopicSchema>;
export type TopicGraphNode = z.infer<typeof TopicGraphNodeSchema>;
export type TopicGraphEdge = z.infer<typeof TopicGraphEdgeSchema>;
export type TopicGraphView = z.infer<typeof TopicGraphViewSchema>;
export type TopicGraphGroup = z.infer<typeof TopicGraphGroupSchema>;
export type TopicChangeEvent = z.infer<typeof TopicChangeEventSchema>;
export type RecordSummary = z.infer<typeof RecordSummarySchema>;
export type ViewerDescriptor = z.infer<typeof ViewerDescriptorSchema>;

export type GraphScope = "idea-lineage" | "artifact-overview" | "experiment-records" | "paper-revisions";
export type RendererChoice = "auto" | "react-flow" | "sigma";
