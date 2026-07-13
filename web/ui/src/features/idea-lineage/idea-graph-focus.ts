import type { TopicGraphView } from "../../types";

export type IdeaGraphFocusDirection = "incoming" | "outgoing" | "both";
export type IdeaGraphFocusEdgeMode = "induced" | "traversal";

export type IdeaGraphFocusConfiguration = {
  enabled: boolean;
  hopRadius: number;
  direction: IdeaGraphFocusDirection;
  relationKinds: string[];
  edgeMode: IdeaGraphFocusEdgeMode;
};

export const DEFAULT_IDEA_GRAPH_FOCUS: IdeaGraphFocusConfiguration = {
  enabled: false,
  hopRadius: 1,
  direction: "both",
  relationKinds: [],
  edgeMode: "induced",
};

export function projectIdeaGraphNeighborhood(
  graph: TopicGraphView,
  selectedNodeIds: string[],
  configuration: IdeaGraphFocusConfiguration,
): TopicGraphView {
  if (!configuration.enabled) {
    return graph;
  }
  const uniqueSeeds = [...new Set(selectedNodeIds.filter(Boolean))];
  const sourceNodeIds = new Set(graph.nodes.map((node) => node.id));
  const resolvedSeeds = uniqueSeeds.filter((nodeId) => sourceNodeIds.has(nodeId));
  const unresolvedSeeds = uniqueSeeds.filter((nodeId) => !sourceNodeIds.has(nodeId));
  const selectedRelations = new Set(configuration.relationKinds);
  const eligibleEdges = graph.edges
    .filter((edge) => sourceNodeIds.has(edge.source) && sourceNodeIds.has(edge.target))
    .filter((edge) => selectedRelations.size === 0 || selectedRelations.has(edge.relation_kind))
    .slice()
    .sort(compareGraphEdges);
  const adjacency = new Map<string, Array<{ nodeId: string; edgeId: string }>>(
    [...sourceNodeIds].map((nodeId) => [nodeId, []]),
  );
  for (const edge of eligibleEdges) {
    if (configuration.direction === "outgoing" || configuration.direction === "both") {
      adjacency.get(edge.source)?.push({ nodeId: edge.target, edgeId: edge.id });
    }
    if (configuration.direction === "incoming" || configuration.direction === "both") {
      adjacency.get(edge.target)?.push({ nodeId: edge.source, edgeId: edge.id });
    }
  }
  for (const neighbors of adjacency.values()) {
    neighbors.sort((left, right) => left.nodeId.localeCompare(right.nodeId) || left.edgeId.localeCompare(right.edgeId));
  }

  const distances = new Map(resolvedSeeds.map((nodeId) => [nodeId, 0]));
  const queue = [...resolvedSeeds];
  const traversalEdgeIds = new Set<string>();
  for (let index = 0; index < queue.length; index += 1) {
    const current = queue[index];
    const distance = distances.get(current) || 0;
    if (distance >= configuration.hopRadius) {
      continue;
    }
    for (const neighbor of adjacency.get(current) || []) {
      if (distances.has(neighbor.nodeId)) {
        continue;
      }
      distances.set(neighbor.nodeId, distance + 1);
      traversalEdgeIds.add(neighbor.edgeId);
      queue.push(neighbor.nodeId);
    }
  }

  const visibleNodeIds = new Set(distances.keys());
  const nodes = graph.nodes.filter((node) => visibleNodeIds.has(node.id)).slice().sort((left, right) => left.id.localeCompare(right.id));
  const edges = eligibleEdges.filter((edge) =>
    configuration.edgeMode === "traversal"
      ? traversalEdgeIds.has(edge.id)
      : visibleNodeIds.has(edge.source) && visibleNodeIds.has(edge.target),
  );
  const groups = graph.groups
    .map((group) => ({ ...group, node_ids: group.node_ids.filter((nodeId) => visibleNodeIds.has(nodeId)) }))
    .filter((group) => group.node_ids.length > 0);
  const sourceNodeCount = graph.total_node_count ?? graph.nodes.length;
  const sourceEdgeCount = graph.total_edge_count ?? graph.edges.length;
  return {
    ...graph,
    nodes,
    edges,
    groups,
    topology_complete: true,
    total_node_count: sourceNodeCount,
    total_edge_count: sourceEdgeCount,
    projection: {
      seed_node_ids: uniqueSeeds,
      resolved_seed_node_ids: resolvedSeeds,
      unresolved_seed_node_ids: unresolvedSeeds,
      hop_radius: configuration.hopRadius,
      direction: configuration.direction,
      relation_kinds: [...selectedRelations].sort(),
      edge_mode: configuration.edgeMode,
      source_node_count: sourceNodeCount,
      source_edge_count: sourceEdgeCount,
      visible_node_count: nodes.length,
      visible_edge_count: edges.length,
      source_index_revision: graph.index_revision || null,
      topology_complete: graph.topology_complete !== false,
    },
    diagnostics: [
      ...graph.diagnostics,
      ...unresolvedSeeds.map((seedNodeId) => ({
        severity: "warning",
        code: "graph_projection_seed_not_found",
        message: `Idea Graph projection seed does not exist: ${seedNodeId}`,
        seed_node_id: seedNodeId,
      })),
    ],
  };
}

function compareGraphEdges(left: TopicGraphView["edges"][number], right: TopicGraphView["edges"][number]) {
  return left.id.localeCompare(right.id) || left.source.localeCompare(right.source) || left.target.localeCompare(right.target);
}
