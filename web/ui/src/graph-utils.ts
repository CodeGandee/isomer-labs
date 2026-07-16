import { MarkerType, type Edge, type Node } from "@xyflow/react";
import type { GraphScope, RendererChoice, TopicGraphView } from "./types";
import { IDEA_GRAPH_NODE_HEIGHT, IDEA_GRAPH_NODE_WIDTH } from "./features/idea-lineage/layout-registry";

export type IdeaFlowNodeData = {
  [key: string]: unknown;
  label: string;
  title: string;
  summary?: string | null;
  status?: string | null;
  material_kind?: string | null;
  record_id?: string | null;
  idea_id?: string | null;
  display_key?: string | null;
  producer?: string | null;
  skill?: string | null;
  exploration_state?: string | null;
  decision_state?: string | null;
  evidence_state?: string | null;
  archive_state?: string | null;
  visibility?: string | null;
  backend_selected?: boolean;
  needs_classification?: string[];
};

export function ideaNodeVisibleLabel(node: Pick<TopicGraphView["nodes"][number], "display_key" | "idea_id" | "status" | "title">): string {
  const key = String(node.display_key || node.idea_id || "").trim();
  const title = String(node.title || "");
  const status = node.status ? String(node.status) : "";
  const heading = key ? `${key} ${title}` : title;
  return status ? `${heading}\n${status}` : heading;
}

export function selectRenderer(graphScope: GraphScope, rendererHint: string, _nodeCount: number): "react-flow" | "sigma" {
  if (graphScope === "idea-lineage") {
    return "react-flow";
  }
  if (rendererHint === "sigma-overview") {
    return "sigma";
  }
  return "sigma";
}

export function requestedRenderer(graphScope: GraphScope): RendererChoice {
  return graphScope === "idea-lineage" ? "react-flow" : "sigma";
}

export function toFlowNodes(graph: TopicGraphView): Node<IdeaFlowNodeData>[] {
  return graph.nodes.map((node, index) => ({
    id: node.id,
    type: "idea",
    className: [
      "idea-flow-node",
      `material-${flowClassToken(node.material_kind || "artifact")}`,
      `status-${flowClassToken(node.status || "unknown")}`,
      `exploration-${flowClassToken(node.exploration_state || "unknown")}`,
      `decision-${flowClassToken(node.decision_state || "unknown")}`,
      `evidence-${flowClassToken(node.evidence_state || "unknown")}`,
      `archive-${flowClassToken(node.archive_state || "active")}`,
      `visibility-${flowClassToken(node.visibility || "primary")}`,
      node.backend_selected || node.selected ? "backend-selected" : "",
      node.needs_classification?.length ? "needs-classification" : "",
    ].filter(Boolean).join(" "),
    position: { x: 40 + (index % 3) * 300, y: 40 + Math.floor(index / 3) * 160 },
    data: {
      label: ideaNodeVisibleLabel(node),
      title: node.title,
      summary: node.summary,
      status: node.status,
      material_kind: node.material_kind,
      record_id: node.record_id,
      idea_id: node.idea_id,
      display_key: node.display_key,
      producer: node.producer,
      skill: node.skill,
      exploration_state: node.exploration_state,
      decision_state: node.decision_state,
      evidence_state: node.evidence_state,
      archive_state: node.archive_state,
      visibility: node.visibility,
      backend_selected: node.backend_selected || Boolean(node.selected),
      needs_classification: node.needs_classification,
    },
    style: {
      fontSize: 12,
      whiteSpace: "pre-line",
      width: IDEA_GRAPH_NODE_WIDTH,
      height: IDEA_GRAPH_NODE_HEIGHT,
    },
  }));
}

export function graphContentSignature(graph: TopicGraphView): string {
  return JSON.stringify({
    graph_scope: graph.graph_scope,
    topology_complete: graph.topology_complete ?? false,
    total_node_count: graph.total_node_count ?? graph.nodes.length,
    total_edge_count: graph.total_edge_count ?? graph.edges.length,
    projection: graph.projection ? {
      seed_node_ids: graph.projection.seed_node_ids,
      hop_radius: graph.projection.hop_radius,
      direction: graph.projection.direction,
      relation_kinds: graph.projection.relation_kinds,
      edge_mode: graph.projection.edge_mode,
      source_index_revision: graph.projection.source_index_revision || null,
      topology_complete: graph.projection.topology_complete,
    } : null,
    nodes: graph.nodes.map((node) => ({
      id: node.id,
      record_id: node.record_id,
      material_kind: node.material_kind,
      density_class: node.density_class,
      title: node.title,
      summary: node.summary || null,
      status: node.status || null,
      selected: Boolean(node.selected),
      producer: node.producer || null,
      skill: node.skill || null,
      idea_id: node.idea_id || null,
      display_key: node.display_key || null,
      visibility: node.visibility || null,
      exploration_state: node.exploration_state || null,
      decision_state: node.decision_state || null,
      evidence_state: node.evidence_state || null,
      archive_state: node.archive_state || null,
      backend_selected: Boolean(node.backend_selected || node.selected),
      needs_classification: node.needs_classification || [],
    })).sort((left, right) => left.id.localeCompare(right.id)),
    edges: graph.edges.map((edge) => ({
      id: edge.id,
      source: edge.source,
      target: edge.target,
      relation_kind: edge.relation_kind,
      canonical: edge.canonical,
      lineage_kind: edge.lineage_kind || null,
      generation_id: edge.generation_id || null,
      status: edge.status || null,
    })).sort((left, right) => left.id.localeCompare(right.id)),
  });
}

export function toFlowEdges(graph: TopicGraphView): Edge[] {
  return graph.edges.map((edge) => ({
    id: edge.id,
    source: edge.source,
    target: edge.target,
    className: `idea-flow-edge relation-${flowClassToken(edge.relation_kind || "related")}`,
    label: edge.relation_kind,
    animated: false,
    markerEnd: {
      type: MarkerType.ArrowClosed,
      width: 16,
      height: 16,
      color: "var(--flow-edge-stroke)",
      strokeWidth: 1.7,
    },
    style: {
      strokeWidth: 1.7,
    },
  }));
}

function flowClassToken(value: string) {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "unknown";
}
