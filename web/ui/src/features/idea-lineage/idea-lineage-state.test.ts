import type { Edge } from "@xyflow/react";
import { describe, expect, it } from "vitest";
import {
  createIdeaLineageStore,
  ideaLineageReducer,
  initialIdeaLineageState,
  selectIdeaFlowEdges,
  selectIdeaFlowNodes,
  selectIdeaLineageNeighborhood,
  visibleHoverPreview,
  type IdeaFlowNode,
} from "./idea-lineage-state";

const edges: Edge[] = [
  { id: "parent-to-main", source: "idea:parent", target: "idea:main" },
  { id: "main-to-child", source: "idea:main", target: "idea:child" },
  { id: "unrelated", source: "idea:other", target: "idea:other-child" },
];

const nodes: IdeaFlowNode[] = [
  node("idea:parent"),
  node("idea:main"),
  node("idea:child"),
  node("idea:other"),
];

describe("idea lineage interaction state", () => {
  it("records single-click selection and derives the selected neighborhood", () => {
    const state = ideaLineageReducer(initialIdeaLineageState, { type: "nodeSelected", nodeId: "idea:main" });
    const neighborhood = selectIdeaLineageNeighborhood(edges, state.selectedNodeId);

    expect(state.selectedNodeId).toBe("idea:main");
    expect([...neighborhood.parentNodeIds]).toEqual(["idea:parent"]);
    expect([...neighborhood.childNodeIds]).toEqual(["idea:child"]);
    expect([...neighborhood.incomingEdgeIds]).toEqual(["parent-to-main"]);
    expect([...neighborhood.outgoingEdgeIds]).toEqual(["main-to-child"]);
  });

  it("transitions hover from pending to visible without changing selection", () => {
    const selected = ideaLineageReducer(initialIdeaLineageState, { type: "nodeSelected", nodeId: "idea:main" });
    const pending = ideaLineageReducer(selected, {
      type: "hoverStarted",
      preview: { nodeId: "idea:child", data: { label: "Child", title: "Child" }, x: 10, y: 20 },
    });
    const visible = ideaLineageReducer(pending, { type: "hoverDelayElapsed" });

    expect(visible.selectedNodeId).toBe("idea:main");
    expect(visibleHoverPreview(visible)?.nodeId).toBe("idea:child");
  });

  it("clears hover and emits an open intent on double-click open", () => {
    const pending = ideaLineageReducer(initialIdeaLineageState, {
      type: "hoverStarted",
      preview: { nodeId: "idea:main", data: { label: "Main", title: "Main" }, x: 10, y: 20 },
    });
    const visible = ideaLineageReducer(pending, { type: "hoverDelayElapsed" });
    const opened = ideaLineageReducer(visible, { type: "nodeOpened", nodeId: "idea:main" });

    expect(opened.hover.status).toBe("idle");
    expect(opened.selectedNodeId).toBe("idea:main");
    expect(opened.openIntent).toEqual({ intentId: 1, nodeId: "idea:main" });

    const consumed = ideaLineageReducer(opened, { type: "openIntentConsumed", intentId: 1 });
    expect(consumed.openIntent).toBeNull();
  });

  it("supports touch long press cancellation and completion", () => {
    const started = ideaLineageReducer(initialIdeaLineageState, {
      type: "touchLongPressStarted",
      pointerId: 5,
      nodeId: "idea:main",
      data: { label: "Main", title: "Main" },
      x: 10,
      y: 20,
    });
    const canceled = ideaLineageReducer(started, { type: "touchLongPressCanceled", pointerId: 5 });
    expect(canceled.touchLongPress).toBeNull();
    expect(canceled.hover.status).toBe("idle");

    const restarted = ideaLineageReducer(initialIdeaLineageState, {
      type: "touchLongPressStarted",
      pointerId: 6,
      nodeId: "idea:main",
      data: { label: "Main", title: "Main" },
      x: 15,
      y: 25,
    });
    const elapsed = ideaLineageReducer(restarted, { type: "touchLongPressElapsed", pointerId: 6 });
    expect(visibleHoverPreview(elapsed)).toEqual({ nodeId: "idea:main", data: { label: "Main", title: "Main" }, x: 15, y: 25 });
  });

  it("preserves unaffected node and edge object identity", () => {
    const selectedNodes = selectIdeaFlowNodes(nodes, edges, "idea:main");
    const selectedEdges = selectIdeaFlowEdges(edges, "idea:main");

    expect(selectedNodes.find((candidate) => candidate.id === "idea:other")).toBe(nodes[3]);
    expect(selectedNodes.find((candidate) => candidate.id === "idea:main")).not.toBe(nodes[1]);
    expect(selectedEdges.find((candidate) => candidate.id === "unrelated")).toBe(edges[2]);
    expect(selectedEdges.find((candidate) => candidate.id === "parent-to-main")).not.toBe(edges[0]);
    expect(selectedEdges.find((candidate) => candidate.id === "parent-to-main")?.className).toContain("lineage-incoming");
    expect(selectedEdges.find((candidate) => candidate.id === "main-to-child")?.className).toContain("lineage-outgoing");
  });

  it("exposes typed store dispatch for idea lineage state", () => {
    const store = createIdeaLineageStore();
    store.dispatch({ type: "nodeSelected", nodeId: "idea:main" });
    expect(store.getSnapshot().selectedNodeId).toBe("idea:main");
    store.dispose();
  });
});

function node(id: string): IdeaFlowNode {
  return {
    id,
    className: "idea-flow-node",
    position: { x: 0, y: 0 },
    data: {
      label: id,
      title: id,
    },
  };
}
