import { describe, expect, it } from "vitest";
import { selectRenderer, toFlowEdges, toFlowNodes } from "./graph-utils";
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
    expect(toFlowEdges(graph)[0].label).toBe("derived_from");
  });
});
