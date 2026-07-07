import { useEffect, useRef } from "react";
import Graphology from "graphology";
import Sigma from "sigma";
import type { TopicGraphView } from "../../types";
import { openRecordFromNode } from "./open-record";

export function SigmaGraph({ graph }: { graph: TopicGraphView }) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  useEffect(() => {
    if (!containerRef.current) {
      return undefined;
    }
    const graphology = new Graphology({ multi: true });
    for (const node of graph.nodes) {
      graphology.addNode(node.id, {
        label: node.title,
        x: Math.random(),
        y: Math.random(),
        size: Number(node.renderer_hints?.size || 8),
        color: String(node.renderer_hints?.color || "#64748b"),
      });
    }
    for (const edge of graph.edges) {
      if (graphology.hasNode(edge.source) && graphology.hasNode(edge.target) && !graphology.hasEdge(edge.id)) {
        graphology.addEdgeWithKey(edge.id, edge.source, edge.target, { label: edge.relation_kind, color: "#94a3b8" });
      }
    }
    const renderer = new Sigma(graphology, containerRef.current, { allowInvalidContainer: true });
    renderer.on("doubleClickNode", ({ node }) => openRecordFromNode(graph.topic_id, graph, node));
    return () => renderer.kill();
  }, [graph]);
  return <div className="sigma-frame" ref={containerRef} />;
}
