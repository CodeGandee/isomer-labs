import { describe, expect, it } from "vitest";
import fixture from "../../../../../tests/fixtures/idea_graph_neighborhood.json";
import type { TopicGraphView } from "../../types";
import { filterIdeaLineageGraphForSearch } from "./IdeaLineagePanel";
import { DEFAULT_IDEA_GRAPH_FOCUS, projectIdeaGraphNeighborhood, type IdeaGraphFocusConfiguration } from "./idea-graph-focus";

const graph: TopicGraphView = {
  ok: true,
  mutated: false,
  topic_id: "alpha",
  topic_workspace_id: "alpha",
  graph_scope: "idea-lineage",
  renderer_hint: "react-flow-detail",
  index_revision: "qidx:fixture",
  generated_at: "2026-07-13T00:00:00Z",
  nodes: fixture.nodes,
  edges: fixture.edges,
  groups: [],
  facets: {},
  topology_complete: true,
  total_node_count: fixture.nodes.length,
  total_edge_count: fixture.edges.length,
  diagnostics: [],
};

describe("Idea Graph client neighborhood projection", () => {
  it("matches the shared backend projection cases", () => {
    for (const testCase of fixture.cases) {
      const projected = projectIdeaGraphNeighborhood(graph, testCase.seed_node_ids, {
        enabled: true,
        hopRadius: testCase.hop_radius,
        direction: testCase.direction as IdeaGraphFocusConfiguration["direction"],
        relationKinds: testCase.relation_kinds,
        edgeMode: testCase.edge_mode as IdeaGraphFocusConfiguration["edgeMode"],
      });
      expect(projected.nodes.map((node) => node.id), testCase.name).toEqual(testCase.expected_node_ids);
      expect(projected.edges.map((edge) => edge.id), testCase.name).toEqual(testCase.expected_edge_ids);
    }
  });

  it("supports zero hops, every direction, unknown seeds, and source counts", () => {
    const zero = projectIdeaGraphNeighborhood(graph, ["idea:b", "idea:missing"], { ...DEFAULT_IDEA_GRAPH_FOCUS, enabled: true, hopRadius: 0 });
    const incoming = projectIdeaGraphNeighborhood(graph, ["idea:b"], { ...DEFAULT_IDEA_GRAPH_FOCUS, enabled: true, direction: "incoming" });
    const outgoing = projectIdeaGraphNeighborhood(graph, ["idea:b"], { ...DEFAULT_IDEA_GRAPH_FOCUS, enabled: true, direction: "outgoing" });

    expect(zero.nodes.map((node) => node.id)).toEqual(["idea:b"]);
    expect(zero.edges).toEqual([]);
    expect(zero.projection).toEqual(expect.objectContaining({
      resolved_seed_node_ids: ["idea:b"],
      unresolved_seed_node_ids: ["idea:missing"],
      source_node_count: 5,
      source_edge_count: 5,
      visible_node_count: 1,
      visible_edge_count: 0,
    }));
    expect(incoming.nodes.map((node) => node.id)).toEqual(["idea:a", "idea:b"]);
    expect(outgoing.nodes.map((node) => node.id)).toEqual(["idea:b", "idea:c"]);
  });

  it("applies visible-label search after focus without changing hop reachability", () => {
    const focused = projectIdeaGraphNeighborhood(graph, ["idea:a"], { ...DEFAULT_IDEA_GRAPH_FOCUS, enabled: true, hopRadius: 2, direction: "outgoing" });
    const searched = filterIdeaLineageGraphForSearch(focused, "Gamma");
    const restored = filterIdeaLineageGraphForSearch(focused, "");

    expect(focused.nodes.map((node) => node.id)).toEqual(["idea:a", "idea:b", "idea:c"]);
    expect(searched?.nodes.map((node) => node.id)).toEqual(["idea:c"]);
    expect(restored).toBe(focused);
    expect(restored?.nodes.map((node) => node.id)).toEqual(["idea:a", "idea:b", "idea:c"]);
  });
});
