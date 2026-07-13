import { afterEach, describe, expect, it, vi } from "vitest";
import { getTopicGraph } from "./api";

describe("Idea Graph API client", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("encodes repeated focus seeds and bounded projection identity", async () => {
    const fetchMock = vi.fn(async (_input: RequestInfo | URL, _init?: RequestInit) => new Response(JSON.stringify({
      ok: true,
      mutated: false,
      topic_id: "alpha",
      topic_workspace_id: "alpha",
      graph_scope: "idea-lineage",
      renderer_hint: "react-flow-detail",
      generated_at: "2026-07-13T00:00:00Z",
      nodes: [],
      edges: [],
      groups: [],
      facets: {},
      topology_complete: true,
      total_node_count: 0,
      total_edge_count: 0,
      projection: null,
      diagnostics: [],
    }), { status: 200, headers: { "Content-Type": "application/json" } }));
    vi.stubGlobal("fetch", fetchMock);

    await getTopicGraph("alpha", "idea-lineage", "react-flow", {
      limit: 1000,
      seedNodeIds: ["idea:a", "idea:b"],
      hopRadius: 2,
      direction: "incoming",
      relationKind: "derived_from,follow_up_to",
      edgeMode: "induced",
    });

    const url = new URL(String(fetchMock.mock.calls[0][0]), "http://localhost");
    expect(url.searchParams.get("renderer")).toBe("react-flow");
    expect(url.searchParams.get("limit")).toBe("1000");
    expect(url.searchParams.getAll("seed_node_id")).toEqual(["idea:a", "idea:b"]);
    expect(url.searchParams.get("hop_radius")).toBe("2");
    expect(url.searchParams.get("direction")).toBe("incoming");
    expect(url.searchParams.get("relation_kind")).toBe("derived_from,follow_up_to");
    expect(url.searchParams.get("edge_mode")).toBe("induced");
  });
});
