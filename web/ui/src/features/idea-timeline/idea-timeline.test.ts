import { describe, expect, it } from "vitest";
import { TopicGraphViewSchema } from "../../types";
import { buildIdeaTimelineRows, filterIdeaTimelineRows, sortIdeaTimelineRows } from "./idea-timeline";

const graph = TopicGraphViewSchema.parse({
  ok: true,
  mutated: false,
  topic_id: "alpha",
  topic_workspace_id: "alpha",
  graph_scope: "idea-lineage",
  renderer_hint: "react-flow-detail",
  generated_at: "2026-07-09T00:00:00Z",
  nodes: [
    {
      id: "idea:root",
      record_id: "record-root",
      material_kind: "idea",
      density_class: "sparse",
      title: "Root Idea",
      status: "selected",
      idea_id: "root",
      display_key: "I-1",
      visibility: "primary",
      created_at: "2026-07-01T00:00:00Z",
      updated_at: "2026-07-02T00:00:00Z",
      source: { aliases: ["seed"], family: "main" },
    },
    {
      id: "idea:child",
      record_id: "record-child",
      material_kind: "idea",
      density_class: "sparse",
      title: "Child Idea",
      status: "candidate",
      idea_id: "child",
      display_key: "I-4",
      visibility: "supporting",
      created_at: "2026-07-03T00:00:00Z",
      updated_at: "2026-07-04T00:00:00Z",
      source: { aliases: ["branch"], family: "support" },
    },
    {
      id: "idea:hidden",
      record_id: "record-hidden",
      material_kind: "idea",
      density_class: "sparse",
      title: "Hidden Idea",
      status: "candidate",
      idea_id: "hidden",
      display_key: "I-2",
      visibility: "hidden",
      created_at: "2026-07-02T00:00:00Z",
      updated_at: "2026-07-02T00:00:00Z",
    },
  ],
  edges: [
    {
      id: "edge-root-child",
      source: "idea:root",
      target: "idea:child",
      relation_kind: "derived_from",
      lineage_kind: "derived_from",
      canonical: true,
    },
  ],
  groups: [],
  facets: {},
  diagnostics: [],
});

describe("idea timeline rows", () => {
  it("builds rows with stable display keys and parent display keys", () => {
    const rows = buildIdeaTimelineRows(graph);

    expect(rows.map((row) => row.displayKey)).toEqual(["I-1", "I-4"]);
    expect(rows[1].parents.map((parent) => parent.displayKey)).toEqual(["I-1"]);
    expect(rows[1].category).toBe("supporting");
  });

  it("uses one fuzzy text query across fields while preserving supporting visibility", () => {
    const rows = buildIdeaTimelineRows(graph);

    expect(filterIdeaTimelineRows(rows, { search: "I-1" }).map((row) => row.ideaId)).toEqual(["root"]);
    expect(filterIdeaTimelineRows(rows, { search: "I-1", includeSecondary: true }).map((row) => row.ideaId)).toEqual(["root", "child"]);
    expect(filterIdeaTimelineRows(rows, { search: "drv", includeSecondary: true }).map((row) => row.ideaId)).toEqual(["child"]);
    expect(filterIdeaTimelineRows(rows, { search: "support", includeSecondary: false }).map((row) => row.ideaId)).toEqual([]);
    expect(filterIdeaTimelineRows(rows, { search: "support", includeSecondary: true }).map((row) => row.ideaId)).toEqual(["child"]);
  });

  it("sorts by display key without forcing consecutive numbering", () => {
    const rows = sortIdeaTimelineRows(buildIdeaTimelineRows(graph), "display_key", "desc");

    expect(rows.map((row) => row.displayKey)).toEqual(["I-4", "I-1"]);
  });
});
