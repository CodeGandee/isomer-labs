import { describe, expect, it } from "vitest";
import { MarkerType } from "@xyflow/react";
import { graphContentSignature, selectRenderer, toFlowEdges, toFlowNodes } from "./graph-utils";
import { TopicGraphViewSchema } from "./types";

const graph = TopicGraphViewSchema.parse({
  ok: true,
  mutated: false,
  topic_id: "alpha",
  topic_workspace_id: "alpha",
  graph_scope: "idea-lineage",
  renderer_hint: "react-flow-detail",
  index_revision: "qidx:test",
  generated_at: "2026-07-06T00:00:00Z",
  nodes: [
    {
      id: "idea:one",
      record_id: "record-one",
      material_kind: "idea",
      density_class: "sparse",
      title: "One",
      one_liner: "One line.",
      summary: "Summary for hover.",
      status: "candidate",
      idea_id: "one",
    },
  ],
  edges: [
    {
      id: "edge-one",
      source: "idea:one",
      target: "idea:one",
      relation_kind: "derived_from",
      canonical: false,
    },
  ],
  groups: [],
  facets: {},
  diagnostics: [],
});

describe("graph utilities", () => {
  it("selects React Flow only for sparse detail graphs", () => {
    expect(selectRenderer("idea-lineage", "react-flow-detail", 12)).toBe("react-flow");
    expect(selectRenderer("artifact-overview", "sigma-overview", 12)).toBe("sigma");
    expect(selectRenderer("idea-lineage", "react-flow-detail", 121)).toBe("sigma");
  });

  it("converts graph API payloads into React Flow objects", () => {
    const node = toFlowNodes(graph)[0];
    expect(node.id).toBe("idea:one");
    expect(node.data.summary).toBe("Summary for hover.");
    expect(node.data.record_id).toBe("record-one");
    const edge = toFlowEdges(graph)[0];
    expect(edge.label).toBe("derived_from");
    expect(edge.markerEnd).toEqual(expect.objectContaining({ type: MarkerType.ArrowClosed }));
  });

  it("keeps backend selected styling separate from UI selection", () => {
    const node = toFlowNodes({ ...graph, nodes: [{ ...graph.nodes[0], selected: true, status: "selected" }] })[0];
    expect(node.className).toContain("backend-selected");
    expect(node.className).toContain("status-selected");
    expect(node.className).not.toMatch(/(^|\s)selected(\s|$)/);
    expect(node.selected).toBeUndefined();
  });

  it("builds a stable graph content signature that ignores response metadata and ordering", () => {
    const changedMetadata = {
      ...graph,
      index_revision: "qidx:other",
      generated_at: "2026-07-07T00:00:00Z",
      nodes: [...graph.nodes].reverse(),
      edges: [...graph.edges].reverse(),
    };
    expect(graphContentSignature(changedMetadata)).toBe(graphContentSignature(graph));
    expect(graphContentSignature({ ...graph, nodes: [{ ...graph.nodes[0], title: "Changed" }] })).not.toBe(graphContentSignature(graph));
  });
});
