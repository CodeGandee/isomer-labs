import {
  ProjectResponseSchema,
  ProjectExplorerResponseSchema,
  IdeaDecisionContextResponseSchema,
  IdeaDetailResponseSchema,
  IdeaSteeringResponseSchema,
  IdeaTraversalResponseSchema,
  OpenableItemDescriptorSchema,
  RecordDetailResponseSchema,
  RecordRenderResponseSchema,
  RecordsResponseSchema,
  RecentErrorsResponseSchema,
  TopicChangeEventSchema,
  TopicGraphViewSchema,
  TopicOverviewJsonResponseSchema,
  TopicOverviewResponseSchema,
  TopicsResponseSchema,
  ViewerDescriptorSchema,
  type GraphScope,
  type ResearchIdeaSteeringRequest,
  type RendererChoice,
} from "./types";

export type GraphFilters = {
  status?: string;
  relationKind?: string;
  producer?: string;
  timeRange?: string;
  search?: string;
  includeSecondary?: boolean;
  limit?: number;
  cursor?: string;
  seedNodeIds?: string[];
  hopRadius?: number;
  direction?: "incoming" | "outgoing" | "both";
  edgeMode?: "induced" | "traversal";
  preset?: string;
  explorationState?: string;
  decisionState?: string;
  evidenceState?: string;
  archiveState?: string;
  visibility?: string;
  generationId?: string;
  decisionRecordId?: string;
};

async function fetchJson(path: string, init?: RequestInit): Promise<unknown> {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${JSON.stringify(payload)}`);
  }
  return payload;
}

function params(values: Record<string, string | number | boolean | readonly string[] | undefined>): string {
  const search = new URLSearchParams();
  for (const [key, value] of Object.entries(values)) {
    if (Array.isArray(value)) {
      for (const item of value) {
        if (item) {
          search.append(key, item);
        }
      }
      continue;
    }
    if (value !== undefined && value !== "") {
      search.set(key, String(value));
    }
  }
  const encoded = search.toString();
  return encoded ? `?${encoded}` : "";
}

function arrayParams(values: Record<string, string[] | undefined>): string {
  const search = new URLSearchParams();
  for (const [key, items] of Object.entries(values)) {
    for (const item of items || []) {
      if (item) {
        search.append(key, item);
      }
    }
  }
  const encoded = search.toString();
  return encoded ? `?${encoded}` : "";
}

export async function getProject() {
  return ProjectResponseSchema.parse(await fetchJson("/api/project"));
}

export async function getTopics() {
  return TopicsResponseSchema.parse(await fetchJson("/api/topics"));
}

export async function getTopic(topicId: string) {
  return fetchJson(`/api/topics/${encodeURIComponent(topicId)}`);
}

export async function getTopicOverview(topicId: string) {
  return TopicOverviewResponseSchema.parse(await fetchJson(`/api/topics/${encodeURIComponent(topicId)}/overview`));
}

export async function getTopicOverviewJson(topicId: string) {
  return TopicOverviewJsonResponseSchema.parse(await fetchJson(`/api/topics/${encodeURIComponent(topicId)}/overview/json`));
}

export async function getRuntime(topicId: string) {
  return fetchJson(`/api/topics/${encodeURIComponent(topicId)}/runtime`);
}

export async function getActors(topicId: string) {
  return fetchJson(`/api/topics/${encodeURIComponent(topicId)}/actors`);
}

export async function getProjectExplorer(expandedTopicIds: string[] = []) {
  return ProjectExplorerResponseSchema.parse(
    await fetchJson(`/api/explorer/project${arrayParams({ expanded_topic_id: expandedTopicIds })}`),
  );
}

export async function getOpenableItemDescriptor(openableItemId: string) {
  return OpenableItemDescriptorSchema.parse(await fetchJson(`/api/openable/${encodeURIComponent(openableItemId)}`));
}

export async function getRecords(topicId: string, options: { facet?: string; limit?: number } = {}) {
  return RecordsResponseSchema.parse(
    await fetchJson(`/api/topics/${encodeURIComponent(topicId)}/records${params({ facet: options.facet, limit: options.limit ?? 500 })}`),
  );
}

export async function getTopicGraph(topicId: string, graphScope: GraphScope, renderer: RendererChoice, filters: GraphFilters) {
  return TopicGraphViewSchema.parse(
    await fetchJson(
      `/api/topics/${encodeURIComponent(topicId)}/graphs/${encodeURIComponent(graphScope)}${params({
        renderer,
        status: filters.status,
        relation_kind: filters.relationKind,
        producer: filters.producer,
        time_range: filters.timeRange,
        search: filters.search,
        include_secondary: filters.includeSecondary,
        limit: filters.limit,
        cursor: filters.cursor,
        seed_node_id: filters.seedNodeIds,
        hop_radius: filters.hopRadius,
        direction: filters.direction,
        edge_mode: filters.edgeMode,
        preset: filters.preset,
        exploration_state: filters.explorationState,
        decision_state: filters.decisionState,
        evidence_state: filters.evidenceState,
        archive_state: filters.archiveState,
        visibility: filters.visibility,
        generation_id: filters.generationId,
        decision_record_id: filters.decisionRecordId,
      })}`,
    ),
  );
}

export async function getRecentErrors(topicId: string, limit = 50) {
  return RecentErrorsResponseSchema.parse(await fetchJson(`/api/topics/${encodeURIComponent(topicId)}/recent-errors${params({ limit })}`));
}

export async function getViewerDescriptor(topicId: string, recordId: string) {
  return ViewerDescriptorSchema.parse(await fetchJson(`/api/topics/${encodeURIComponent(topicId)}/viewer/records/${encodeURIComponent(recordId)}`));
}

export async function getRecordDetail(topicId: string, recordId: string, includePayload = false) {
  return RecordDetailResponseSchema.parse(
    await fetchJson(`/api/topics/${encodeURIComponent(topicId)}/records/${encodeURIComponent(recordId)}${params({ include_payload: includePayload })}`),
  );
}

export async function getIdeaDetail(topicId: string, ideaId: string, options: { includeSourceJson?: boolean } = {}) {
  return IdeaDetailResponseSchema.parse(
    await fetchJson(
      `/api/topics/${encodeURIComponent(topicId)}/ideas/${encodeURIComponent(ideaId)}${params({
        include_source_json: options.includeSourceJson,
      })}`,
    ),
  );
}

export async function getIdeaDecisionContext(topicId: string, ideaId: string) {
  return IdeaDecisionContextResponseSchema.parse(
    await fetchJson(`/api/topics/${encodeURIComponent(topicId)}/ideas/${encodeURIComponent(ideaId)}/decisions`),
  );
}

export async function getDecisionContext(topicId: string, decisionRecordId: string) {
  return IdeaDecisionContextResponseSchema.parse(
    await fetchJson(`/api/topics/${encodeURIComponent(topicId)}/idea-decisions/${encodeURIComponent(decisionRecordId)}`),
  );
}

export async function traverseIdeas(
  topicId: string,
  options: {
    rootIdeaIds: string[];
    direction: "ancestors" | "descendants";
    relationKinds?: string[];
    maxDepth?: number;
    maxNodes?: number;
    maxEdges?: number;
  },
) {
  return IdeaTraversalResponseSchema.parse(
    await fetchJson(
      `/api/topics/${encodeURIComponent(topicId)}/ideas/traverse${params({
        root_idea_id: options.rootIdeaIds,
        direction: options.direction,
        relation_kind: options.relationKinds,
        max_depth: options.maxDepth,
        max_nodes: options.maxNodes,
        max_edges: options.maxEdges,
      })}`,
    ),
  );
}

export async function steerIdea(topicId: string, request: ResearchIdeaSteeringRequest) {
  return IdeaSteeringResponseSchema.parse(
    await fetchJson(`/api/topics/${encodeURIComponent(topicId)}/ideas/steer`, {
      method: "POST",
      body: JSON.stringify(request),
    }),
  );
}

export async function getRecordRender(topicId: string, recordId: string) {
  return RecordRenderResponseSchema.parse(await fetchJson(`/api/topics/${encodeURIComponent(topicId)}/records/${encodeURIComponent(recordId)}/render`));
}

export async function getRecordLineage(topicId: string, recordId: string) {
  return fetchJson(`/api/topics/${encodeURIComponent(topicId)}/records/${encodeURIComponent(recordId)}/lineage`);
}

export async function getRecordSiblings(topicId: string, recordId: string) {
  return fetchJson(`/api/topics/${encodeURIComponent(topicId)}/records/${encodeURIComponent(recordId)}/siblings`);
}

export async function getRecordFiles(topicId: string, recordId: string) {
  return fetchJson(`/api/topics/${encodeURIComponent(topicId)}/records/${encodeURIComponent(recordId)}/files`);
}

export async function getRecordFacets(topicId: string, recordId: string) {
  return fetchJson(`/api/topics/${encodeURIComponent(topicId)}/records/${encodeURIComponent(recordId)}/facets`);
}

export function parseTopicEvent(raw: string) {
  return TopicChangeEventSchema.parse(JSON.parse(raw));
}
