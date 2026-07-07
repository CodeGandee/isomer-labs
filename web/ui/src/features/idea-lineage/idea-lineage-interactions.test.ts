import { afterEach, describe, expect, it, vi } from "vitest";
import { createIdeaLineageInteractionBoundary } from "./idea-lineage-interactions";
import { createIdeaLineageStore, visibleHoverPreview } from "./idea-lineage-state";

describe("idea lineage interaction boundary", () => {
  afterEach(() => {
    vi.useRealTimers();
  });

  it("cancels a pending hover preview when the node is clicked before the delay", () => {
    vi.useFakeTimers();
    const { boundary, store } = createBoundary();

    boundary.nodeEnter(hoverEvent("idea:main", 10, 20));
    vi.advanceTimersByTime(1499);
    boundary.nodeClick({ nodeId: "idea:main" });
    vi.advanceTimersByTime(2000);

    expect(store.getSnapshot().selectedNodeId).toBe("idea:main");
    expect(visibleHoverPreview(store.getSnapshot())).toBeNull();
    boundary.dispose();
  });

  it("closes a visible hover preview when the node is clicked", () => {
    vi.useFakeTimers();
    const { boundary, store } = createBoundary();

    boundary.nodeEnter(hoverEvent("idea:main", 10, 20));
    vi.advanceTimersByTime(1500);
    expect(visibleHoverPreview(store.getSnapshot())?.nodeId).toBe("idea:main");

    boundary.nodeClick({ nodeId: "idea:main" });

    expect(store.getSnapshot().selectedNodeId).toBe("idea:main");
    expect(visibleHoverPreview(store.getSnapshot())).toBeNull();
    boundary.dispose();
  });

  it("does not rearm hover from mouse movement after click until leave and enter", () => {
    vi.useFakeTimers();
    const { boundary, store } = createBoundary();

    boundary.nodeEnter(hoverEvent("idea:main", 10, 20));
    boundary.nodeClick({ nodeId: "idea:main" });
    boundary.nodeMove(hoverEvent("idea:main", 40, 60));
    vi.advanceTimersByTime(2000);

    expect(visibleHoverPreview(store.getSnapshot())).toBeNull();

    boundary.nodeLeave({ nodeId: "idea:main" });
    boundary.nodeEnter(hoverEvent("idea:main", 40, 60));
    vi.advanceTimersByTime(1500);

    expect(visibleHoverPreview(store.getSnapshot())?.nodeId).toBe("idea:main");
    boundary.dispose();
  });

  it("keeps a visible hover preview open while the pointer moves into the tooltip", () => {
    vi.useFakeTimers();
    const { boundary, store } = createBoundary();

    boundary.nodeEnter(hoverEvent("idea:main", 10, 20));
    vi.advanceTimersByTime(1500);
    boundary.nodeLeave({ nodeId: "idea:main" });
    vi.advanceTimersByTime(250);
    boundary.tooltipEnter();
    vi.advanceTimersByTime(1000);

    expect(visibleHoverPreview(store.getSnapshot())?.nodeId).toBe("idea:main");

    boundary.tooltipLeave();
    vi.advanceTimersByTime(500);

    expect(visibleHoverPreview(store.getSnapshot())).toBeNull();
    boundary.dispose();
  });
});

function createBoundary() {
  const store = createIdeaLineageStore();
  const boundary = createIdeaLineageInteractionBoundary({
    store,
    getHoverPreviewDelayMs: () => 1500,
    hoverPreviewCloseDelayMs: 500,
    touchLongPressMoveTolerancePx: 14,
  });
  return { boundary, store };
}

function hoverEvent(nodeId: string, x: number, y: number) {
  return {
    nodeId,
    data: { label: nodeId, title: nodeId },
    x,
    y,
  };
}
