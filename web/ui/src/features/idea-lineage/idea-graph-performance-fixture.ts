import type { TopicGraphView } from "../../types";

export function hundredsNodeIdeaGraphFixture(nodeCount = 400, highDegree = 180): TopicGraphView {
  const nodes = Array.from({ length: nodeCount }, (_, index) => ({
    id: `idea:${index.toString().padStart(4, "0")}`,
    record_id: `record-${index}`,
    material_kind: "idea",
    density_class: "sparse",
    title: `Performance idea ${index}`,
    status: "candidate",
    idea_id: `idea-${index}`,
    display_key: `I-${index + 1}`,
  }));
  const edges = [
    ...Array.from({ length: nodeCount - 1 }, (_, index) => ({
      id: `chain-${index}`,
      source: nodes[index].id,
      target: nodes[index + 1].id,
      relation_kind: "derived_from",
      canonical: true,
    })),
    ...Array.from({ length: Math.min(highDegree, nodeCount - 2) }, (_, index) => ({
      id: `hub-${index + 2}`,
      source: nodes[0].id,
      target: nodes[index + 2].id,
      relation_kind: "inspired_by",
      canonical: true,
    })),
  ];
  return {
    ok: true,
    mutated: false,
    topic_id: "performance",
    topic_workspace_id: "performance",
    graph_scope: "idea-lineage",
    renderer_hint: "react-flow-detail",
    index_revision: "qidx:performance",
    generated_at: "2026-07-13T00:00:00Z",
    nodes,
    edges,
    groups: [],
    facets: {},
    topology_complete: true,
    total_node_count: nodes.length,
    total_edge_count: edges.length,
    diagnostics: [],
  };
}
