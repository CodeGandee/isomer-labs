import { describe, expect, it } from "vitest";
import { toFlowEdges, toFlowNodes } from "../../graph-utils";
import { projectIdeaGraphNeighborhood } from "./idea-graph-focus";
import { hundredsNodeIdeaGraphFixture } from "./idea-graph-performance-fixture";
import { selectIdeaFlowEdges, selectIdeaFlowNodes } from "./idea-lineage-state";
import { runLayoutRequest } from "./layout-engine";
import { layoutFingerprint } from "./layout-protocol";
import { DEFAULT_LAYOUT_CONFIGURATIONS } from "./layout-registry";

describe("Idea Graph hundreds-node performance smoke", () => {
  it("keeps focus, grid layout, conversion, and selection interaction within the smoke budget", async () => {
    const graph = hundredsNodeIdeaGraphFixture();
    const startedAt = performance.now();
    const focused = projectIdeaGraphNeighborhood(graph, ["idea:0000"], {
      enabled: true,
      hopRadius: 1,
      direction: "outgoing",
      relationKinds: [],
      edgeMode: "induced",
    });
    const projectionMs = performance.now() - startedAt;
    const flowNodes = toFlowNodes(graph);
    const flowEdges = toFlowEdges(graph);
    const conversionMs = performance.now() - startedAt - projectionMs;
    const selectedNodes = selectIdeaFlowNodes(flowNodes, flowEdges, ["idea:0000", "idea:0200"]);
    const selectedEdges = selectIdeaFlowEdges(flowEdges, ["idea:0000", "idea:0200"]);
    const interactionMs = performance.now() - startedAt - projectionMs - conversionMs;
    const layoutNodes = flowNodes.map((node) => ({ id: node.id, label: node.data.label }));
    const layoutEdges = flowEdges.map((edge) => ({ id: edge.id, source: edge.source, target: edge.target }));
    const configuration = DEFAULT_LAYOUT_CONFIGURATIONS.grid;
    const fingerprint = layoutFingerprint(layoutNodes, layoutEdges, configuration);
    const layout = await runLayoutRequest({ type: "layout", jobId: 1, fingerprint, nodes: layoutNodes, edges: layoutEdges, configuration });
    const totalMs = performance.now() - startedAt;

    console.info(JSON.stringify({ fixtureNodes: graph.nodes.length, fixtureEdges: graph.edges.length, focusedNodes: focused.nodes.length, projectionMs, conversionMs, interactionMs, layoutMs: layout.durationMs, totalMs }));
    expect(graph.nodes).toHaveLength(400);
    expect(graph.edges.length).toBeGreaterThan(500);
    expect(focused.nodes.length).toBeGreaterThan(150);
    expect(selectedNodes.filter((node) => node.selected)).toHaveLength(2);
    expect(selectedEdges.some((edge) => edge.className?.includes("lineage-outgoing"))).toBe(true);
    expect(layout.ok).toBe(true);
    expect(Object.keys(layout.positions)).toHaveLength(400);
    expect(totalMs).toBeLessThan(2000);
  });
});
