import type { Edge, Node } from "@xyflow/react";
import ELK from "elkjs/lib/elk.bundled.js";
import type { GraphScope, RendererChoice, TopicGraphView } from "./types";

export function selectRenderer(graphScope: GraphScope, rendererHint: string, nodeCount: number): "react-flow" | "sigma" {
  if (rendererHint === "sigma-overview") {
    return "sigma";
  }
  if (graphScope === "idea-lineage" && nodeCount <= 120) {
    return "react-flow";
  }
  return "sigma";
}

export function requestedRenderer(graphScope: GraphScope): RendererChoice {
  return graphScope === "idea-lineage" ? "auto" : "sigma";
}

export function toFlowNodes(graph: TopicGraphView): Node[] {
  return graph.nodes.map((node, index) => ({
    id: node.id,
    className: `idea-flow-node material-${flowClassToken(node.material_kind || "artifact")} status-${flowClassToken(node.status || "unknown")} ${node.selected ? "selected" : ""}`,
    position: { x: 40 + (index % 3) * 300, y: 40 + Math.floor(index / 3) * 160 },
    data: {
      label: `${node.title}${node.status ? `\n${node.status}` : ""}`,
    },
    style: {
      fontSize: 12,
      whiteSpace: "pre-line",
      width: 240,
    },
  }));
}

export function toFlowEdges(graph: TopicGraphView): Edge[] {
  return graph.edges.map((edge) => ({
    id: edge.id,
    source: edge.source,
    target: edge.target,
    className: `idea-flow-edge relation-${flowClassToken(edge.relation_kind || "related")}`,
    label: edge.relation_kind,
    animated: false,
  }));
}

function flowClassToken(value: string) {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "unknown";
}

export async function layoutFlowGraph(nodes: Node[], edges: Edge[]): Promise<Node[]> {
  const elk = new ELK();
  const layout = await elk.layout({
    id: "root",
    layoutOptions: {
      "elk.algorithm": "layered",
      "elk.direction": "RIGHT",
      "elk.spacing.nodeNode": "50",
      "elk.layered.spacing.nodeNodeBetweenLayers": "80",
    },
    children: nodes.map((node) => ({ id: node.id, width: 250, height: 90 })),
    edges: edges.map((edge) => ({ id: edge.id, sources: [edge.source], targets: [edge.target] })),
  });
  const positions = new Map((layout.children || []).map((child) => [child.id, { x: child.x || 0, y: child.y || 0 }]));
  return nodes.map((node) => ({
    ...node,
    position: positions.get(node.id) || node.position,
  }));
}
