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
import { DEFAULT_LAYOUT_CONFIGURATIONS } from "./layout-registry";

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
  it("supports ordered replace, modifier toggle, area replacement, seed removal, and clear", () => {
    const replaced = ideaLineageReducer(initialIdeaLineageState, { type: "selectionReplaced", nodeIds: ["idea:main", "idea:child", "idea:main"] });
    const toggledOff = ideaLineageReducer(replaced, { type: "selectionToggled", nodeId: "idea:main" });
    const toggledOn = ideaLineageReducer(toggledOff, { type: "selectionToggled", nodeId: "idea:parent" });
    const area = ideaLineageReducer(toggledOn, { type: "selectionReplaced", nodeIds: ["idea:parent", "idea:other"] });
    const removed = ideaLineageReducer(area, { type: "selectionRemoved", nodeId: "idea:parent" });
    const cleared = ideaLineageReducer(removed, { type: "selectionCleared" });

    expect(replaced.selectedNodeIds).toEqual(["idea:main", "idea:child"]);
    expect(toggledOff.selectedNodeIds).toEqual(["idea:child"]);
    expect(toggledOn.selectedNodeIds).toEqual(["idea:child", "idea:parent"]);
    expect(area.selectedNodeIds).toEqual(["idea:parent", "idea:other"]);
    expect(removed.selectedNodeIds).toEqual(["idea:other"]);
    expect(cleared.selectedNodeIds).toEqual([]);
  });

  it("repairs only missing selections and exits focus without clearing seeds", () => {
    const selected = ideaLineageReducer(initialIdeaLineageState, { type: "selectionReplaced", nodeIds: ["idea:main", "idea:child"] });
    const focused = ideaLineageReducer(selected, { type: "focusChanged", focus: { enabled: true, hopRadius: 2 } });
    const repaired = ideaLineageReducer(focused, { type: "graphDataLoaded", nodeIds: ["idea:child", "idea:other"] });
    const exited = ideaLineageReducer(repaired, { type: "focusExited" });

    expect(repaired.selectedNodeIds).toEqual(["idea:child"]);
    expect(repaired.focus).toEqual(expect.objectContaining({ enabled: true, hopRadius: 2 }));
    expect(exited.focus.enabled).toBe(false);
    expect(exited.selectedNodeIds).toEqual(["idea:child"]);
  });

  it("preserves focus and unapplied layout draft across benign graph refresh", () => {
    const selected = ideaLineageReducer(initialIdeaLineageState, { type: "selectionReplaced", nodeIds: ["idea:main"] });
    const focused = ideaLineageReducer(selected, { type: "focusChanged", focus: { enabled: true, hopRadius: 3 } });
    const drafted = ideaLineageReducer(focused, { type: "layoutDraftChanged", configuration: DEFAULT_LAYOUT_CONFIGURATIONS.grid });
    const refreshed = ideaLineageReducer(drafted, { type: "graphDataLoaded", nodeIds: ["idea:main", "idea:child"] });

    expect(refreshed.selectedNodeIds).toEqual(["idea:main"]);
    expect(refreshed.focus).toEqual(expect.objectContaining({ enabled: true, hopRadius: 3 }));
    expect(refreshed.layoutDraft.algorithm).toBe("grid");
    expect(refreshed.appliedLayout.algorithm).toBe("layered");
  });

  it("opens one target without replacing an existing multi-selection", () => {
    const selected = ideaLineageReducer(initialIdeaLineageState, { type: "selectionReplaced", nodeIds: ["idea:main", "idea:child"] });
    const opened = ideaLineageReducer(selected, { type: "nodeOpened", nodeId: "idea:child" });
    expect(opened.selectedNodeIds).toEqual(["idea:main", "idea:child"]);
    expect(opened.openIntent?.nodeId).toBe("idea:child");
  });

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
      sessionId: 1,
      preview: { nodeId: "idea:child", data: { label: "Child", title: "Child" }, x: 10, y: 20 },
    });
    const visible = ideaLineageReducer(pending, { type: "hoverDelayElapsed", sessionId: 1 });

    expect(visible.selectedNodeId).toBe("idea:main");
    expect(visibleHoverPreview(visible)?.nodeId).toBe("idea:child");
  });

  it("ignores stale hover delay and close events from old sessions", () => {
    const pending = ideaLineageReducer(initialIdeaLineageState, {
      type: "hoverStarted",
      sessionId: 1,
      preview: { nodeId: "idea:main", data: { label: "Main", title: "Main" }, x: 10, y: 20 },
    });

    const staleElapsed = ideaLineageReducer(pending, { type: "hoverDelayElapsed", sessionId: 2 });
    expect(staleElapsed.hover).toEqual(pending.hover);

    const staleMoved = ideaLineageReducer(pending, {
      type: "hoverMoved",
      sessionId: 2,
      preview: { nodeId: "idea:main", data: { label: "Main", title: "Main" }, x: 100, y: 120 },
    });
    expect(staleMoved.hover).toEqual(pending.hover);

    const staleClosed = ideaLineageReducer(pending, { type: "hoverClosed", sessionId: 2 });
    expect(staleClosed.hover).toEqual(pending.hover);

    const closed = ideaLineageReducer(pending, { type: "hoverClosed", sessionId: 1 });
    expect(closed.hover.status).toBe("idle");
  });

  it("clears hover and emits an open intent on double-click open", () => {
    const pending = ideaLineageReducer(initialIdeaLineageState, {
      type: "hoverStarted",
      sessionId: 1,
      preview: { nodeId: "idea:main", data: { label: "Main", title: "Main" }, x: 10, y: 20 },
    });
    const visible = ideaLineageReducer(pending, { type: "hoverDelayElapsed", sessionId: 1 });
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
    const elapsed = ideaLineageReducer(restarted, { type: "touchLongPressElapsed", pointerId: 6, sessionId: 2 });
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

  it("derives union highlights with selected styling precedence", () => {
    const selectedNodes = selectIdeaFlowNodes(nodes, edges, ["idea:parent", "idea:main"]);
    const selectedEdges = selectIdeaFlowEdges(edges, ["idea:parent", "idea:main"]);
    expect(selectedNodes.find((candidate) => candidate.id === "idea:parent")?.className).toContain("ui-selected");
    expect(selectedNodes.find((candidate) => candidate.id === "idea:main")?.className).toContain("ui-selected");
    expect(selectedNodes.find((candidate) => candidate.id === "idea:child")?.className).toContain("lineage-child");
    expect(selectedEdges.find((candidate) => candidate.id === "parent-to-main")?.className).toContain("lineage-outgoing");
    expect(selectedEdges.find((candidate) => candidate.id === "parent-to-main")?.className).toContain("lineage-incoming");
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
