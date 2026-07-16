import { describe, expect, it } from "vitest";
import fixture from "../../../../../tests/fixtures/research_idea_portfolio.json";
import { IdeaDecisionContextResponseSchema, IdeaTraversalResponseSchema, TopicGraphViewSchema } from "../../types";
import { applyIdeaPortfolioView, IDEA_PORTFOLIO_PRESETS, persistIdeaPortfolioView, restoreIdeaPortfolioView } from "./idea-portfolio";

const graph = TopicGraphViewSchema.parse({
  ok: true,
  mutated: false,
  topic_id: fixture.topic_id,
  topic_workspace_id: fixture.topic_id,
  graph_scope: "idea-lineage",
  renderer_hint: "react-flow-detail",
  index_revision: fixture.index_revision,
  generated_at: "2026-07-17T00:00:00Z",
  nodes: fixture.canonical_ideas
    .filter((idea) => idea.visibility !== "hidden")
    .map((idea) => ({
      ...idea,
      id: `idea:${idea.idea_id}`,
      record_id: `record:${idea.idea_id}`,
      material_kind: "idea",
      density_class: "sparse",
      backend_selected: idea.decision_state === "selected",
      needs_classification: ["exploration_state", "decision_state", "evidence_state"].filter((facet) => idea[facet as keyof typeof idea] === "unknown"),
    })),
  edges: fixture.canonical_idea_edges.map((edge) => ({
    ...edge,
    source: `idea:${edge.parent_idea_id}`,
    target: `idea:${edge.child_idea_id}`,
    relation_kind: edge.lineage_kind,
    canonical: true,
  })),
  groups: [],
  facets: {},
  portfolio: {
    source_counts: { ideas: fixture.canonical_ideas.length, edges: fixture.canonical_idea_edges.length },
    visible_counts: { ideas: fixture.canonical_ideas.length - 1, edges: fixture.canonical_idea_edges.length },
    source_topology_complete: true,
  },
  topology_complete: true,
  diagnostics: [],
});

const kaojuOnlyGraph = TopicGraphViewSchema.parse({
  ok: true,
  mutated: false,
  topic_id: fixture.kaoju_only.topic_id,
  topic_workspace_id: fixture.kaoju_only.topic_id,
  graph_scope: "idea-lineage",
  renderer_hint: "react-flow-detail",
  index_revision: fixture.kaoju_only.index_revision,
  generated_at: "2026-07-17T00:00:00Z",
  nodes: fixture.kaoju_only.canonical_ideas.map((idea) => {
    const latestRealization = fixture.kaoju_only.canonical_idea_realizations.find((item) => item.idea_id === idea.idea_id);
    return {
      ...idea,
      id: `idea:${idea.idea_id}`,
      record_id: latestRealization?.record_id || "",
      material_kind: "idea",
      density_class: "sparse",
      backend_selected: idea.decision_state === "selected",
      needs_classification: [],
      steering_eligibility: { eligible: true, reopening_required: idea.decision_state === "closed" || idea.decision_state === "deferred" },
      source: { latest_realization: latestRealization },
    };
  }),
  edges: fixture.kaoju_only.canonical_idea_edges.map((edge) => ({
    ...edge,
    source: `idea:${edge.parent_idea_id}`,
    target: `idea:${edge.child_idea_id}`,
    relation_kind: edge.lineage_kind,
    canonical: true,
  })),
  groups: [],
  facets: {},
  portfolio: {
    source_counts: { ideas: fixture.kaoju_only.canonical_ideas.length, edges: fixture.kaoju_only.canonical_idea_edges.length },
    visible_counts: { ideas: fixture.kaoju_only.canonical_ideas.length, edges: fixture.kaoju_only.canonical_idea_edges.length },
    source_topology_complete: true,
  },
  topology_complete: true,
  diagnostics: [],
});

describe("shared idea portfolio predicates", () => {
  it("matches the Python fixture for every fixed preset", () => {
    expect(IDEA_PORTFOLIO_PRESETS.map((preset) => preset.id)).toEqual(Object.keys(fixture.expected_presets));
    for (const [preset, expected] of Object.entries(fixture.expected_presets)) {
      const result = applyIdeaPortfolioView(graph, { preset: preset as (typeof IDEA_PORTFOLIO_PRESETS)[number]["id"] });
      expect(result?.nodes.map((node) => node.idea_id), preset).toEqual(expected);
      expect(result?.edges.every((edge) => result.nodes.some((node) => node.id === edge.source) && result.nodes.some((node) => node.id === edge.target))).toBe(true);
    }
  });

  it("composes explicit independent facets and preserves source counts", () => {
    const result = applyIdeaPortfolioView(graph, { preset: "all-proposed", explorationState: "explored", decisionState: "selected,deferred" });
    expect(result?.nodes.map((node) => node.idea_id)).toEqual(["deepsci-explored-deferred", "deepsci-archived-selected"]);
    expect(result?.portfolio?.source_counts?.ideas).toBe(8);
    expect(result?.portfolio?.visible_counts?.ideas).toBe(2);
  });

  it("restores state independently for graph and timeline", () => {
    window.localStorage.clear();
    persistIdeaPortfolioView(fixture.topic_id, "graph", { preset: "closed", evidenceState: "mixed" });
    persistIdeaPortfolioView(fixture.topic_id, "timeline", { preset: "unexplored" });
    expect(restoreIdeaPortfolioView(fixture.topic_id, "graph")).toEqual({ preset: "closed", evidenceState: "mixed" });
    expect(restoreIdeaPortfolioView(fixture.topic_id, "timeline")).toEqual({ preset: "unexplored" });
  });

  it("uses the same presets and exact realization details for a Kaoju-only portfolio", () => {
    for (const [preset, expected] of Object.entries(fixture.kaoju_only.expected_presets)) {
      const result = applyIdeaPortfolioView(kaojuOnlyGraph, { preset: preset as (typeof IDEA_PORTFOLIO_PRESETS)[number]["id"] });
      expect(result?.nodes.map((node) => node.idea_id), preset).toEqual(expected);
    }
    expect(kaojuOnlyGraph.nodes.map((node) => (node.source?.latest_realization as { source_json_path?: string }).source_json_path)).toEqual([
      "$.research_idea_effects.ideas[0]",
      "$.research_idea_effects.ideas[1]",
      "$.research_idea_effects.ideas[2]",
      "$.research_idea_effects.ideas[3]",
    ]);
    expect(kaojuOnlyGraph.nodes.every((node) => node.steering_eligibility?.eligible)).toBe(true);
  });

  it("validates shared decision and complete or incomplete traversal payloads", () => {
    const expectedDecision = fixture.expected_decision_context;
    const options = fixture.canonical_idea_decision_options.filter((option) => option.decision_record_id === expectedDecision.decision_record_id);
    const decision = IdeaDecisionContextResponseSchema.parse({
      ok: true,
      mutated: false,
      topic_id: fixture.topic_id,
      topic_workspace_id: fixture.topic_id,
      operation: "ideas.decision-context",
      decision_record_id: expectedDecision.decision_record_id,
      decisions: [{ ...expectedDecision, options, missing_fields: [] }],
      ideas: fixture.canonical_ideas.filter((idea) => options.some((option) => option.idea_id === idea.idea_id)),
      transitions: fixture.canonical_idea_transitions.filter((transition) => transition.decision_record_id === expectedDecision.decision_record_id),
      reopen_history: [],
      index_revision: fixture.index_revision,
      diagnostics: [],
    });
    expect(decision.decisions[0].options).toEqual(options);

    const expectedTraversal = fixture.expected_traversal;
    const complete = IdeaTraversalResponseSchema.parse({
      ok: true,
      mutated: false,
      topic_id: fixture.topic_id,
      topic_workspace_id: fixture.topic_id,
      operation: "ideas.traverse",
      roots: expectedTraversal.root_idea_ids,
      resolved_roots: expectedTraversal.root_idea_ids,
      unresolved_roots: [],
      direction: expectedTraversal.direction,
      relation_kinds: ["alternative_to", "derived_from", "follow_up_to"],
      nodes: graph.nodes.filter((node) => expectedTraversal.complete_node_ids.includes(String(node.idea_id))),
      edges: graph.edges.filter((edge) => expectedTraversal.complete_edge_ids.includes(edge.id)),
      topology_complete: true,
      limiting_bounds: [],
      maximum_observed_depth: 2,
      counts: { nodes: expectedTraversal.complete_node_ids.length, edges: expectedTraversal.complete_edge_ids.length },
      bounds: { max_depth: 8, max_nodes: 500, max_edges: 1000 },
      continuation: null,
      index_revision: fixture.index_revision,
      diagnostics: [],
    });
    expect(complete.topology_complete).toBe(true);
    const incomplete = IdeaTraversalResponseSchema.parse({
      ...complete,
      topology_complete: false,
      limiting_bounds: expectedTraversal.incomplete_limiting_bounds,
      continuation: { action: "increase_max_depth", suggested_max_depth: 2 },
      diagnostics: [{ severity: "warning", code: "idea_traversal_incomplete", message: "Increase max depth." }],
    });
    expect(incomplete.limiting_bounds).toEqual(["max_depth"]);
  });

  it("preserves an unprojected legacy Kaoju diagnostic without transient idea nodes", () => {
    const diagnosticGraph = TopicGraphViewSchema.parse({
      ...kaojuOnlyGraph,
      nodes: [],
      edges: [],
      diagnostics: [{
        severity: "warning",
        code: fixture.legacy_unprojected.diagnostic_code,
        message: "Legacy Direction Set requires migration.",
        portfolio_complete: false,
        repair: { action: fixture.legacy_unprojected.repair_action },
      }],
    });
    expect(diagnosticGraph.nodes).toEqual([]);
    expect(diagnosticGraph.diagnostics[0].code).toBe("idea_bearing_record_unprojected");
  });
});
