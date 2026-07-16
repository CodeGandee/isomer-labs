import type { TopicGraphNode, TopicGraphView } from "../../types";

export const IDEA_PORTFOLIO_PRESETS = [
  {
    id: "current",
    label: "Current",
    description: "Active Primary Ideas whose decision remains unknown, open, shortlisted, or selected.",
    predicate: { archiveState: ["active"], visibility: ["primary"], decisionState: ["unknown", "open", "shortlisted", "selected"] },
  },
  { id: "all-proposed", label: "All proposed", description: "Every non-hidden canonical Research Idea, including supporting and archived ideas.", predicate: { visibility: ["primary", "supporting"] } },
  { id: "open-for-exploration", label: "Open for exploration", description: "Active non-hidden ideas explicitly open, shortlisted, or selected.", predicate: { archiveState: ["active"], visibility: ["primary", "supporting"], decisionState: ["open", "shortlisted", "selected"] } },
  { id: "unexplored", label: "Unexplored", description: "Non-hidden ideas whose exploration has not started.", predicate: { visibility: ["primary", "supporting"], explorationState: ["unexplored"] } },
  { id: "exploring", label: "Exploring", description: "Non-hidden ideas under active exploration.", predicate: { visibility: ["primary", "supporting"], explorationState: ["exploring"] } },
  { id: "explored", label: "Explored", description: "Non-hidden ideas whose exploration pass is complete.", predicate: { visibility: ["primary", "supporting"], explorationState: ["explored"] } },
  { id: "selected", label: "Selected", description: "Non-hidden ideas selected for further development.", predicate: { visibility: ["primary", "supporting"], decisionState: ["selected"] } },
  { id: "deferred", label: "Deferred", description: "Non-hidden ideas deferred for possible later reconsideration.", predicate: { visibility: ["primary", "supporting"], decisionState: ["deferred"] } },
  { id: "closed", label: "Closed", description: "Non-hidden ideas closed with a recorded reason when available.", predicate: { visibility: ["primary", "supporting"], decisionState: ["closed"] } },
  { id: "needs-classification", label: "Needs classification", description: "Non-hidden ideas with an unknown exploration, decision, or evidence facet.", predicate: { visibility: ["primary", "supporting"], needsClassification: true } },
] as const;

export type IdeaPortfolioPresetId = (typeof IDEA_PORTFOLIO_PRESETS)[number]["id"];

export type IdeaPortfolioViewState = {
  preset: IdeaPortfolioPresetId;
  explorationState?: string;
  decisionState?: string;
  evidenceState?: string;
  archiveState?: string;
  visibility?: string;
  generationId?: string;
  decisionRecordId?: string;
};

export const DEFAULT_IDEA_PORTFOLIO_VIEW: IdeaPortfolioViewState = { preset: "current" };

export const IDEA_FACET_OPTIONS = {
  explorationState: ["unknown", "unexplored", "exploring", "explored"],
  decisionState: ["unknown", "open", "shortlisted", "selected", "deferred", "closed"],
  evidenceState: ["unknown", "unassessed", "inconclusive", "supported", "mixed", "refuted"],
  archiveState: ["active", "archived"],
  visibility: ["primary", "supporting", "hidden"],
} as const;

type PresetPredicate = {
  explorationState?: readonly string[];
  decisionState?: readonly string[];
  evidenceState?: readonly string[];
  archiveState?: readonly string[];
  visibility?: readonly string[];
  needsClassification?: boolean;
};

const FACET_NODE_KEYS = {
  explorationState: "exploration_state",
  decisionState: "decision_state",
  evidenceState: "evidence_state",
  archiveState: "archive_state",
  visibility: "visibility",
} as const;

export function applyIdeaPortfolioView(graph: TopicGraphView | undefined, state: IdeaPortfolioViewState): TopicGraphView | undefined {
  if (!graph) {
    return graph;
  }
  const preset = IDEA_PORTFOLIO_PRESETS.find((item) => item.id === state.preset) || IDEA_PORTFOLIO_PRESETS[0];
  const nodes = graph.nodes.filter((node) => matchesPreset(node, preset.predicate) && matchesExplicitFilters(node, state));
  const nodeIds = new Set(nodes.map((node) => node.id));
  const edges = graph.edges.filter((edge) => nodeIds.has(edge.source) && nodeIds.has(edge.target));
  const groups = graph.groups
    .map((group) => ({ ...group, node_ids: group.node_ids.filter((nodeId) => nodeIds.has(nodeId)) }))
    .filter((group) => group.node_ids.length > 0);
  const explicitFilters = Object.fromEntries(
    Object.entries(state)
      .filter(([key, value]) => key !== "preset" && typeof value === "string" && value.length > 0)
      .map(([key, value]) => [toSnakeCase(key), splitValues(String(value))]),
  );
  const sourceCounts = graph.portfolio?.source_counts || {
    ideas: graph.nodes.length,
    edges: graph.edges.length,
    facets: facetCounts(graph.nodes),
  };
  const portfolio = {
    ...(graph.portfolio || {}),
    preset: {
      id: preset.id,
      label: preset.label,
      description: preset.description,
      predicate: presetPredicatePayload(preset.predicate),
    },
    available_presets: IDEA_PORTFOLIO_PRESETS.map((item) => ({ id: item.id, label: item.label, description: item.description, predicate: presetPredicatePayload(item.predicate) })),
    explicit_filters: explicitFilters,
    applied_predicate: {
      composition: "preset AND explicit_filters",
      composition_order: ["preset", "explicit_filters", "relation_filter", "text_filter", "paging"],
      preset: presetPredicatePayload(preset.predicate),
      explicit_filters: explicitFilters,
      applied_locally: true,
    },
    source_counts: sourceCounts,
    visible_counts: { ideas: nodes.length, edges: edges.length, facets: facetCounts(nodes) },
    omitted_cross_boundary_edge_count: graph.edges.filter((edge) => nodeIds.has(edge.source) !== nodeIds.has(edge.target)).length,
    source_topology_complete: graph.topology_complete === true,
  };
  return {
    ...graph,
    nodes,
    edges,
    groups,
    portfolio,
    facets: { ...graph.facets, portfolio },
    total_node_count: nodes.length,
    total_edge_count: edges.length,
  };
}

export function restoreIdeaPortfolioView(topicId: string, view: "graph" | "timeline"): IdeaPortfolioViewState {
  if (typeof window === "undefined") {
    return DEFAULT_IDEA_PORTFOLIO_VIEW;
  }
  try {
    const payload = JSON.parse(window.localStorage.getItem(storageKey(topicId, view)) || "null") as Partial<IdeaPortfolioViewState> | null;
    if (!payload || !IDEA_PORTFOLIO_PRESETS.some((preset) => preset.id === payload.preset)) {
      return DEFAULT_IDEA_PORTFOLIO_VIEW;
    }
    return { ...DEFAULT_IDEA_PORTFOLIO_VIEW, ...payload } as IdeaPortfolioViewState;
  } catch {
    return DEFAULT_IDEA_PORTFOLIO_VIEW;
  }
}

export function persistIdeaPortfolioView(topicId: string, view: "graph" | "timeline", state: IdeaPortfolioViewState): void {
  if (typeof window === "undefined") {
    return;
  }
  window.localStorage.setItem(storageKey(topicId, view), JSON.stringify(state));
}

export function visiblePortfolioCount(graph: TopicGraphView | undefined): { visible: number; source: number } {
  const visible = numericCount(graph?.portfolio?.visible_counts, "ideas") ?? graph?.nodes.length ?? 0;
  const source = numericCount(graph?.portfolio?.source_counts, "ideas") ?? graph?.total_node_count ?? graph?.nodes.length ?? 0;
  return { visible, source };
}

function matchesPreset(node: TopicGraphNode, predicate: PresetPredicate): boolean {
  if (predicate.needsClassification && !needsClassification(node)) {
    return false;
  }
  return facetEntries(predicate).every(([key, accepted]) => accepted.length === 0 || accepted.includes(nodeFacet(node, key)));
}

function matchesExplicitFilters(node: TopicGraphNode, state: IdeaPortfolioViewState): boolean {
  for (const key of Object.keys(FACET_NODE_KEYS) as Array<keyof typeof FACET_NODE_KEYS>) {
    const accepted = splitValues(state[key]);
    if (accepted.length && !accepted.includes(nodeFacet(node, key))) {
      return false;
    }
  }
  const generationIds = Array.isArray(node.generation_ids) ? node.generation_ids : [];
  const requestedGenerations = splitValues(state.generationId);
  if (requestedGenerations.length && !requestedGenerations.some((value) => generationIds.includes(value))) {
    return false;
  }
  const decisionIds = Array.isArray(node.decision_record_ids) ? node.decision_record_ids : [];
  const requestedDecisions = splitValues(state.decisionRecordId);
  return requestedDecisions.length === 0 || requestedDecisions.some((value) => decisionIds.includes(value));
}

function needsClassification(node: TopicGraphNode): boolean {
  return [node.exploration_state, node.decision_state, node.evidence_state].some((value) => !value || value === "unknown");
}

function facetEntries(predicate: PresetPredicate): Array<[keyof typeof FACET_NODE_KEYS, readonly string[]]> {
  return (Object.keys(FACET_NODE_KEYS) as Array<keyof typeof FACET_NODE_KEYS>).map((key) => [key, predicate[key] || []]);
}

function nodeFacet(node: TopicGraphNode, key: keyof typeof FACET_NODE_KEYS): string {
  const value = node[FACET_NODE_KEYS[key]];
  if (key === "archiveState") {
    return String(value || "active");
  }
  if (key === "visibility") {
    return String(value || "primary");
  }
  return String(value || "unknown");
}

function facetCounts(nodes: TopicGraphNode[]): Record<string, Record<string, number>> {
  const result: Record<string, Record<string, number>> = {};
  for (const key of Object.keys(FACET_NODE_KEYS) as Array<keyof typeof FACET_NODE_KEYS>) {
    const facet = FACET_NODE_KEYS[key];
    result[facet] = {};
    for (const node of nodes) {
      const value = nodeFacet(node, key);
      result[facet][value] = (result[facet][value] || 0) + 1;
    }
  }
  return result;
}

function presetPredicatePayload(predicate: PresetPredicate): Record<string, unknown> {
  return Object.fromEntries(
    Object.entries(predicate).map(([key, value]) => [toSnakeCase(key), value]),
  );
}

function splitValues(value: string | undefined): string[] {
  return String(value || "").split(",").map((item) => item.trim()).filter(Boolean);
}

function numericCount(value: Record<string, unknown> | undefined, key: string): number | undefined {
  const item = value?.[key];
  return typeof item === "number" ? item : undefined;
}

function toSnakeCase(value: string): string {
  return value.replace(/[A-Z]/g, (letter) => `_${letter.toLowerCase()}`);
}

function storageKey(topicId: string, view: string): string {
  return `isomer:idea-portfolio:${topicId}:${view}`;
}
