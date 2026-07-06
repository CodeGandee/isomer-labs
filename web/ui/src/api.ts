import {
  ProjectResponseSchema,
  ProjectExplorerResponseSchema,
  OpenableItemDescriptorSchema,
  RecordsResponseSchema,
  TopicChangeEventSchema,
  TopicGraphViewSchema,
  TopicsResponseSchema,
  ViewerDescriptorSchema,
  type GraphScope,
  type RendererChoice,
} from "./types";

export type GraphFilters = {
  status?: string;
  relationKind?: string;
  producer?: string;
  timeRange?: string;
  search?: string;
  includeSecondary?: boolean;
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

function params(values: Record<string, string | number | boolean | undefined>): string {
  const search = new URLSearchParams();
  for (const [key, value] of Object.entries(values)) {
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
      })}`,
    ),
  );
}

export async function getViewerDescriptor(topicId: string, recordId: string) {
  return ViewerDescriptorSchema.parse(await fetchJson(`/api/topics/${encodeURIComponent(topicId)}/viewer/records/${encodeURIComponent(recordId)}`));
}

export async function getRecordDetail(topicId: string, recordId: string, includePayload = false) {
  return fetchJson(`/api/topics/${encodeURIComponent(topicId)}/records/${encodeURIComponent(recordId)}${params({ include_payload: includePayload })}`);
}

export async function getRecordRender(topicId: string, recordId: string) {
  return fetchJson(`/api/topics/${encodeURIComponent(topicId)}/records/${encodeURIComponent(recordId)}/render`);
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
