import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { act, cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import type React from "react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

const settingsMock = vi.hoisted(() => ({
  hoverPreviewDelayMs: 1500,
  refreshGuiSettings: vi.fn(),
  setHoverPreviewDelayMs: vi.fn(),
}));

const flowRenderMock = vi.hoisted(() => ({
  snapshots: [] as Array<{ nodes: unknown[]; edges: unknown[] }>,
}));

type MockNode = {
  id: string;
  className?: string;
  data?: {
    idea_id?: unknown;
    label?: unknown;
    title?: unknown;
  };
};

type MockEdge = {
  id: string;
  className?: string;
  markerEnd?: unknown;
  source?: string;
  target?: string;
};

type MockFlowProps = {
  nodes?: MockNode[];
  edges?: MockEdge[];
  onNodeClick?: (event: React.MouseEvent<HTMLButtonElement>, node: MockNode) => void;
  onNodeDoubleClick?: (event: React.MouseEvent<HTMLButtonElement>, node: MockNode) => void;
  onNodeMouseEnter?: (event: React.MouseEvent<HTMLButtonElement>, node: MockNode) => void;
  onNodeMouseMove?: (event: React.MouseEvent<HTMLButtonElement>, node: MockNode) => void;
  onNodeMouseLeave?: (event: React.MouseEvent<HTMLButtonElement>, node: MockNode) => void;
  children?: React.ReactNode;
};

vi.mock("@xyflow/react", () => ({
  Background: () => null,
  Controls: () => null,
  MarkerType: {
    Arrow: "arrow",
    ArrowClosed: "arrowclosed",
  },
  ReactFlowProvider: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  useReactFlow: () => ({ fitView: vi.fn() }),
  ReactFlow: ({ nodes = [], edges = [], onNodeClick, onNodeDoubleClick, onNodeMouseEnter, onNodeMouseMove, onNodeMouseLeave, children }: MockFlowProps) => {
    flowRenderMock.snapshots.push({ nodes, edges });
    return (
      <div data-testid="react-flow">
        {nodes.map((node) => (
          <button
            className={`react-flow__node ${node.className || ""}`}
            data-id={node.id}
            data-testid={`graph-node-${node.id}`}
            key={node.id}
            onClick={(event) => onNodeClick?.(event, node)}
            onDoubleClick={(event) => onNodeDoubleClick?.(event, node)}
            onMouseEnter={(event) => onNodeMouseEnter?.(event, node)}
            onMouseLeave={(event) => onNodeMouseLeave?.(event, node)}
            onMouseMove={(event) => onNodeMouseMove?.(event, node)}
            type="button"
          >
            {String(node.data?.label || node.id)}
          </button>
        ))}
        {edges.map((edge) => (
          <div
            className={`react-flow__edge ${edge.className || ""}`}
            data-id={edge.id}
            data-marker-end={JSON.stringify(edge.markerEnd || null)}
            data-testid={`graph-edge-${edge.id}`}
            key={edge.id}
          />
        ))}
        {children}
      </div>
    );
  },
}));

vi.mock("sigma", () => ({
  default: class {
    on() {}
    kill() {}
  },
}));

vi.mock("./graph-utils", async (importOriginal) => ({
  ...(await importOriginal<typeof import("./graph-utils")>()),
  layoutFlowGraph: vi.fn(async (nodes: unknown) => nodes),
}));

vi.mock("./api", async (importOriginal) => ({
  ...(await importOriginal<typeof import("./api")>()),
  getIdeaDetail: vi.fn(),
  getTopicGraph: vi.fn(),
}));

vi.mock("./ui-settings", () => ({
  DEFAULT_HOVER_PREVIEW_DELAY_MS: 1500,
  GuiSettingsProvider: ({ children }: { children: unknown }) => children,
  useGuiSettings: () => ({
    hoverPreviewDelayMs: settingsMock.hoverPreviewDelayMs,
    refreshGuiSettings: settingsMock.refreshGuiSettings,
    setHoverPreviewDelayMs: settingsMock.setHoverPreviewDelayMs,
  }),
}));

import { getIdeaDetail, getTopicGraph } from "./api";
import { workbenchCommands$ } from "./events";
import { filterIdeaLineageGraphForSearch, IdeaGraphPanel } from "./features/idea-lineage/IdeaLineagePanel";
import { layoutFlowGraph } from "./graph-utils";
import type { TopicGraphView } from "./types";

const getIdeaDetailMock = vi.mocked(getIdeaDetail);
const getTopicGraphMock = vi.mocked(getTopicGraph);
const layoutFlowGraphMock = vi.mocked(layoutFlowGraph);

describe("Idea graph panel interactions", () => {
  beforeEach(() => {
    settingsMock.hoverPreviewDelayMs = 1500;
    flowRenderMock.snapshots = [];
    getIdeaDetailMock.mockResolvedValue(ideaDetailPayload());
    getTopicGraphMock.mockResolvedValue(graphPayload());
    layoutFlowGraphMock.mockClear();
  });

  afterEach(() => {
    cleanup();
    vi.useRealTimers();
    getIdeaDetailMock.mockReset();
    getTopicGraphMock.mockReset();
    layoutFlowGraphMock.mockClear();
    settingsMock.refreshGuiSettings.mockReset();
    settingsMock.setHoverPreviewDelayMs.mockReset();
  });

  it("uses one local idea search and requests the backend overview graph", async () => {
    renderWithQuery(<IdeaGraphPanel topicId="alpha" />);

    expect(await screen.findByRole("searchbox", { name: "Search ideas" })).toBeTruthy();
    expect(screen.queryByLabelText("Search graph")).toBeNull();
    expect(screen.queryByLabelText("Status filter")).toBeNull();
    expect(screen.queryByLabelText("Relation filter")).toBeNull();
    expect(screen.queryByLabelText("Show supporting records")).toBeNull();
    await waitFor(() => {
      expect(getTopicGraphMock).toHaveBeenCalledWith("alpha", "idea-lineage", "auto", { includeSecondary: false });
    });
  });

  it("filters idea nodes locally and restores the overview when search is cleared", async () => {
    renderWithQuery(<IdeaGraphPanel topicId="alpha" />);
    const search = await screen.findByRole("searchbox", { name: "Search ideas" });
    await screen.findByTestId("graph-node-idea:parent");
    const backendCallCount = getTopicGraphMock.mock.calls.length;

    fireEvent.change(search, { target: { value: "Precision" } });

    await waitFor(() => {
      expect(screen.getByTestId("graph-node-idea:idea-1")).toBeTruthy();
      expect(screen.queryByTestId("graph-node-idea:parent")).toBeNull();
      expect(screen.queryByTestId("graph-node-idea:child")).toBeNull();
      expect(screen.queryByTestId("graph-edge-parent-to-main")).toBeNull();
    });
    expect(getTopicGraphMock).toHaveBeenCalledTimes(backendCallCount);

    fireEvent.change(search, { target: { value: "" } });

    await waitFor(() => {
      expect(screen.getByTestId("graph-node-idea:parent")).toBeTruthy();
      expect(screen.getByTestId("graph-node-idea:child")).toBeTruthy();
      expect(screen.getByTestId("graph-edge-parent-to-main")).toBeTruthy();
    });
    expect(getTopicGraphMock).toHaveBeenCalledTimes(backendCallCount);
  });

  it("filters NCU by visible node labels only", async () => {
    renderWithQuery(<IdeaGraphPanel topicId="alpha" />);
    const search = await screen.findByRole("searchbox", { name: "Search ideas" });
    await screen.findByTestId("graph-node-idea:parent");

    fireEvent.change(search, { target: { value: "ncu" } });

    await waitFor(() => {
      expect(screen.getByTestId("graph-node-idea:parent")).toBeTruthy();
      expect(screen.getByTestId("graph-node-idea:child")).toBeTruthy();
      expect(screen.queryByTestId("graph-node-idea:idea-1")).toBeNull();
      expect(screen.queryByTestId("graph-node-idea:unrelated")).toBeNull();
      expect(screen.queryByTestId("graph-edge-parent-to-main")).toBeNull();
      expect(screen.queryByTestId("graph-edge-main-to-child")).toBeNull();
      expect(screen.queryByTestId("graph-edge-unrelated-self")).toBeNull();
    });
  });

  it("filters visible label tokens and prunes edges outside the visible nodes", () => {
    const graph = graphPayload();

    const ncu = filterIdeaLineageGraphForSearch(graph, "ncu");
    expect(ncu?.nodes.map((node) => node.id)).toEqual(["idea:parent", "idea:child"]);
    expect(ncu?.edges).toEqual([]);

    const ncuSide = filterIdeaLineageGraphForSearch(graph, "ncu side");
    expect(ncuSide?.nodes.map((node) => node.id)).toEqual(["idea:parent"]);

    const launchCalibration = filterIdeaLineageGraphForSearch(graph, "launch calibration");
    expect(launchCalibration?.nodes.map((node) => node.id)).toEqual(["idea:child"]);

    const hiddenMetadataOnly = filterIdeaLineageGraphForSearch(graph, "hiddenpath");
    expect(hiddenMetadataOnly?.nodes).toEqual([]);
    expect(hiddenMetadataOnly?.edges).toEqual([]);

    expect(filterIdeaLineageGraphForSearch(graph, "")).toBe(graph);
  });

  it("selects on single click and opens on double click", async () => {
    const events: unknown[] = [];
    const subscription = workbenchCommands$.subscribe((event) => events.push(event));
    renderWithQuery(<IdeaGraphPanel topicId="alpha" />);

    const node = await screen.findByTestId("graph-node-idea:idea-1");
    fireEvent.click(node);
    expect(events).toEqual([]);

    fireEvent.doubleClick(node);
    expect(events).toEqual([{ type: "open-idea", topicId: "alpha", ideaId: "idea-1" }]);
    subscription.unsubscribe();
  });

  it("shows loading before rendering the full Markdown hover preview", async () => {
    let resolveDetail: (value: ReturnType<typeof ideaDetailPayload>) => void = () => {};
    getIdeaDetailMock.mockReturnValueOnce(new Promise((resolve) => {
      resolveDetail = resolve;
    }));
    renderWithQuery(<IdeaGraphPanel topicId="alpha" />);
    const node = await screen.findByTestId("graph-node-idea:idea-1");

    vi.useFakeTimers();
    fireEvent.mouseEnter(node, { clientX: 120, clientY: 140 });
    expect(screen.queryByRole("tooltip")).toBeNull();

    act(() => {
      vi.advanceTimersByTime(1499);
    });
    expect(screen.queryByRole("tooltip")).toBeNull();

    act(() => {
      vi.advanceTimersByTime(1);
    });

    expect(screen.getByRole("tooltip").textContent).toContain("Loading preview");
    vi.useRealTimers();
    await waitFor(() => {
      expect(getIdeaDetailMock).toHaveBeenCalledWith("alpha", "idea-1", { includeSourceJson: true });
    });

    await act(async () => {
      resolveDetail(ideaDetailPayload());
    });

    await waitFor(() => {
      const tooltip = screen.getByRole("tooltip");
      expect(tooltip.textContent).toContain("Full correction rationale that is not present in graph metadata.");
      expect(tooltip.querySelector("h1")).toBeNull();
    });
  });

  it("uses the configured hover popup delay", async () => {
    settingsMock.hoverPreviewDelayMs = 1250;
    getIdeaDetailMock.mockReturnValue(new Promise(() => {}));
    renderWithQuery(<IdeaGraphPanel topicId="alpha" />);
    const node = await screen.findByTestId("graph-node-idea:idea-1");

    vi.useFakeTimers();
    fireEvent.mouseEnter(node, { clientX: 120, clientY: 140 });
    act(() => {
      vi.advanceTimersByTime(1249);
    });
    expect(screen.queryByRole("tooltip")).toBeNull();

    act(() => {
      vi.advanceTimersByTime(1);
    });
    expect(screen.getByRole("tooltip").textContent).toContain("Loading preview");
  });

  it("does not show the hover tooltip after a single click until the node is re-entered", async () => {
    getIdeaDetailMock.mockReturnValue(new Promise(() => {}));
    renderWithQuery(<IdeaGraphPanel topicId="alpha" />);
    const node = await screen.findByTestId("graph-node-idea:idea-1");

    vi.useFakeTimers();
    fireEvent.mouseEnter(node, { clientX: 120, clientY: 140 });
    act(() => {
      vi.advanceTimersByTime(1000);
    });
    fireEvent.click(node);
    act(() => {
      vi.advanceTimersByTime(2000);
    });
    expect(screen.queryByRole("tooltip")).toBeNull();

    fireEvent.mouseMove(node, { clientX: 180, clientY: 200 });
    act(() => {
      vi.advanceTimersByTime(2000);
    });
    expect(screen.queryByRole("tooltip")).toBeNull();

    fireEvent.mouseLeave(node);
    fireEvent.mouseEnter(node, { clientX: 130, clientY: 150 });
    act(() => {
      vi.advanceTimersByTime(1500);
    });
    expect(screen.getByRole("tooltip").textContent).toContain("Loading preview");
  });

  it("closes the visible hover tooltip when the node is single-clicked", async () => {
    getIdeaDetailMock.mockReturnValue(new Promise(() => {}));
    renderWithQuery(<IdeaGraphPanel topicId="alpha" />);
    const node = await screen.findByTestId("graph-node-idea:idea-1");

    vi.useFakeTimers();
    fireEvent.mouseEnter(node, { clientX: 120, clientY: 140 });
    act(() => {
      vi.advanceTimersByTime(1500);
    });
    expect(screen.getByRole("tooltip").textContent).toContain("Loading preview");

    fireEvent.click(node);

    expect(screen.queryByRole("tooltip")).toBeNull();
  });

  it("keeps the hover tooltip open while the pointer is inside it", async () => {
    getIdeaDetailMock.mockReturnValue(new Promise(() => {}));
    renderWithQuery(<IdeaGraphPanel topicId="alpha" />);
    const node = await screen.findByTestId("graph-node-idea:idea-1");

    vi.useFakeTimers();
    fireEvent.mouseEnter(node, { clientX: 120, clientY: 140 });
    act(() => {
      vi.advanceTimersByTime(1500);
    });

    const tooltip = screen.getByRole("tooltip");
    fireEvent.mouseLeave(node);
    fireEvent.pointerEnter(tooltip);
    act(() => {
      vi.advanceTimersByTime(300);
    });
    expect(screen.queryByRole("tooltip")).not.toBeNull();

    fireEvent.pointerLeave(tooltip);
    act(() => {
      vi.advanceTimersByTime(600);
    });
    expect(screen.queryByRole("tooltip")).toBeNull();
  });

  it("does not move the visible tooltip when the mouse moves over the node", async () => {
    getIdeaDetailMock.mockReturnValue(new Promise(() => {}));
    renderWithQuery(<IdeaGraphPanel topicId="alpha" />);
    const node = await screen.findByTestId("graph-node-idea:idea-1");

    vi.useFakeTimers();
    fireEvent.mouseEnter(node, { clientX: 120, clientY: 140 });
    act(() => {
      vi.advanceTimersByTime(1500);
    });

    const tooltip = screen.getByRole("tooltip");
    const initialLeft = tooltip.style.left;
    const initialTop = tooltip.style.top;
    fireEvent.mouseMove(node, { clientX: 260, clientY: 280 });
    expect(tooltip.style.left).toBe(initialLeft);
    expect(tooltip.style.top).toBe(initialTop);
  });

  it("opens the hover tooltip from a touch long press and cancels early release", async () => {
    getIdeaDetailMock.mockReturnValue(new Promise(() => {}));
    renderWithQuery(<IdeaGraphPanel topicId="alpha" />);
    const node = await screen.findByTestId("graph-node-idea:idea-1");

    vi.useFakeTimers();
    fireEvent.pointerDown(node, { pointerId: 11, pointerType: "touch", clientX: 150, clientY: 160 });
    act(() => {
      vi.advanceTimersByTime(300);
    });
    fireEvent.pointerUp(node, { pointerId: 11, pointerType: "touch", clientX: 150, clientY: 160 });
    act(() => {
      vi.advanceTimersByTime(1500);
    });
    expect(screen.queryByRole("tooltip")).toBeNull();

    fireEvent.pointerDown(node, { pointerId: 12, pointerType: "touch", clientX: 155, clientY: 165 });
    act(() => {
      vi.advanceTimersByTime(1500);
    });
    expect(screen.getByRole("tooltip").textContent).toContain("Loading preview");
  });

  it("clears the hover tooltip when opening the node", async () => {
    getIdeaDetailMock.mockReturnValue(new Promise(() => {}));
    const events: unknown[] = [];
    const subscription = workbenchCommands$.subscribe((event) => events.push(event));
    renderWithQuery(<IdeaGraphPanel topicId="alpha" />);
    const node = await screen.findByTestId("graph-node-idea:idea-1");

    vi.useFakeTimers();
    fireEvent.mouseEnter(node, { clientX: 120, clientY: 140 });
    act(() => {
      vi.advanceTimersByTime(1500);
    });
    expect(screen.getByRole("tooltip").textContent).toContain("Loading preview");

    fireEvent.doubleClick(node);
    expect(screen.queryByRole("tooltip")).toBeNull();
    expect(events).toEqual([{ type: "open-idea", topicId: "alpha", ideaId: "idea-1" }]);

    fireEvent.mouseEnter(node, { clientX: 122, clientY: 142 });
    act(() => {
      vi.advanceTimersByTime(1500);
    });
    expect(screen.queryByRole("tooltip")).toBeNull();

    fireEvent.mouseLeave(node);
    fireEvent.mouseEnter(node, { clientX: 130, clientY: 150 });
    act(() => {
      vi.advanceTimersByTime(1500);
    });
    expect(screen.getByRole("tooltip").textContent).toContain("Loading preview");
    subscription.unsubscribe();
  });

  it("highlights selected node parents, children, and adjacent edges", async () => {
    renderWithQuery(<IdeaGraphPanel topicId="alpha" />);
    const node = await screen.findByTestId("graph-node-idea:idea-1");

    fireEvent.click(node);

    expect(screen.getByTestId("graph-node-idea:parent").className).toContain("lineage-parent");
    expect(screen.getByTestId("graph-node-idea:idea-1").className).toContain("ui-selected");
    expect(screen.getByTestId("graph-node-idea:child").className).toContain("lineage-child");
    expect(screen.getByTestId("graph-edge-parent-to-main").className).toContain("lineage-incoming");
    expect(screen.getByTestId("graph-edge-main-to-child").className).toContain("lineage-outgoing");
  });

  it("keeps unaffected graph objects stable and applies affected edge classes declaratively when selecting", async () => {
    renderWithQuery(<IdeaGraphPanel topicId="alpha" />);
    const node = await screen.findByTestId("graph-node-idea:idea-1");
    const before = lastFlowSnapshot();
    const unrelatedNodeBefore = findSnapshotNode(before, "idea:unrelated");
    const selectedNodeBefore = findSnapshotNode(before, "idea:idea-1");
    const unrelatedEdgeBefore = findSnapshotEdge(before, "unrelated-self");
    const incomingEdgeBefore = findSnapshotEdge(before, "parent-to-main");
    expect(incomingEdgeBefore.className || "").not.toContain("lineage-incoming");

    fireEvent.click(node);

    const after = lastFlowSnapshot();
    expect(findSnapshotNode(after, "idea:unrelated")).toBe(unrelatedNodeBefore);
    expect(findSnapshotNode(after, "idea:idea-1")).not.toBe(selectedNodeBefore);
    expect(findSnapshotEdge(after, "unrelated-self")).toBe(unrelatedEdgeBefore);
    expect(findSnapshotEdge(after, "parent-to-main")).not.toBe(incomingEdgeBefore);
    expect(findSnapshotEdge(after, "parent-to-main").className).toContain("lineage-incoming");
    expect(findSnapshotEdge(after, "main-to-child").className).toContain("lineage-outgoing");
    expect(screen.getByTestId("graph-edge-parent-to-main").className).toContain("lineage-incoming");
    expect(screen.getByTestId("graph-edge-unrelated-self").className).not.toContain("lineage-incoming");
    expect(screen.getByTestId("graph-edge-unrelated-self").className).not.toContain("lineage-outgoing");
  });

  it("keeps selected lineage highlights visible when hover preview rerenders", async () => {
    getIdeaDetailMock.mockReturnValue(new Promise(() => {}));
    renderWithQuery(<IdeaGraphPanel topicId="alpha" />);
    const node = await screen.findByTestId("graph-node-idea:idea-1");

    fireEvent.click(node);
    const afterSelect = lastFlowSnapshot();

    vi.useFakeTimers();
    fireEvent.mouseEnter(node, { clientX: 120, clientY: 140 });
    act(() => {
      vi.advanceTimersByTime(1500);
    });

    expect(screen.getByRole("tooltip").textContent).toContain("Loading preview");
    expect(screen.getByTestId("graph-node-idea:parent").className).toContain("lineage-parent");
    expect(screen.getByTestId("graph-node-idea:child").className).toContain("lineage-child");
    expect(screen.getByTestId("graph-edge-parent-to-main").className).toContain("lineage-incoming");
    expect(screen.getByTestId("graph-edge-main-to-child").className).toContain("lineage-outgoing");
    expect(lastFlowSnapshot().edges).toBe(afterSelect.edges);
  });

  it("keeps selected lineage highlights and layout stable when refetch only changes metadata", async () => {
    getTopicGraphMock.mockResolvedValueOnce(graphPayload()).mockResolvedValueOnce({ ...graphPayload(), generated_at: "2026-07-07T00:00:00Z" });
    const { client } = renderWithQuery(<IdeaGraphPanel topicId="alpha" />);
    const node = await screen.findByTestId("graph-node-idea:idea-1");

    fireEvent.click(node);
    const afterSelect = lastFlowSnapshot();
    expect(screen.getByTestId("graph-node-idea:parent").className).toContain("lineage-parent");

    await act(async () => {
      await client.refetchQueries({ queryKey: ["topic", "alpha", "graph"] });
    });

    expect(getTopicGraphMock).toHaveBeenCalledTimes(2);
    expect(layoutFlowGraphMock).toHaveBeenCalledTimes(1);
    expect(lastFlowSnapshot().nodes).toBe(afterSelect.nodes);
    expect(lastFlowSnapshot().edges).toBe(afterSelect.edges);
    expect(screen.getByTestId("graph-node-idea:parent").className).toContain("lineage-parent");
    expect(screen.getByTestId("graph-node-idea:idea-1").className).toContain("ui-selected");
    expect(screen.getByTestId("graph-node-idea:child").className).toContain("lineage-child");
  });

  it("clears selected lineage highlights when changed graph content removes the selected node", async () => {
    getTopicGraphMock.mockResolvedValueOnce(graphPayload()).mockResolvedValueOnce(graphPayloadWithout("idea:idea-1"));
    const { client } = renderWithQuery(<IdeaGraphPanel topicId="alpha" />);
    const node = await screen.findByTestId("graph-node-idea:idea-1");

    fireEvent.click(node);
    expect(screen.getByTestId("graph-node-idea:idea-1").className).toContain("ui-selected");

    await act(async () => {
      await client.refetchQueries({ queryKey: ["topic", "alpha", "graph"] });
    });

    await waitFor(() => {
      expect(screen.queryByTestId("graph-node-idea:idea-1")).toBeNull();
    });
    expect(lastFlowSnapshot().nodes.some((candidate) => candidate.id === "idea:idea-1")).toBe(false);
    expect(lastFlowSnapshot().nodes.some((candidate) => (candidate.className || "").includes("ui-selected"))).toBe(false);
  });
});

function renderWithQuery(element: React.ReactElement) {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return { client, ...render(<QueryClientProvider client={client}>{element}</QueryClientProvider>) };
}

function lastFlowSnapshot() {
  return flowRenderMock.snapshots.at(-1) as { nodes: MockNode[]; edges: MockEdge[] };
}

function findSnapshotNode(snapshot: { nodes: MockNode[] }, id: string) {
  const node = snapshot.nodes.find((candidate) => candidate.id === id);
  if (!node) {
    throw new Error(`Missing node snapshot for ${id}`);
  }
  return node;
}

function findSnapshotEdge(snapshot: { edges: MockEdge[] }, id: string) {
  const edge = snapshot.edges.find((candidate) => candidate.id === id);
  if (!edge) {
    throw new Error(`Missing edge snapshot for ${id}`);
  }
  return edge;
}

function ideaDetailPayload() {
  return {
    ok: true,
    mutated: false,
    topic_id: "alpha",
    topic_workspace_id: "alpha",
    idea_id: "idea-1",
    idea: {
      idea_id: "idea-1",
      title: "Precision Idea",
      summary: "Separate launch overhead.",
      status: "candidate",
    },
    idea_content: {
      title: "Precision Idea",
      rationale: "Full correction rationale that is not present in graph metadata.",
      notes: ["Preserve markdown tables.", "Preserve long preview content."],
    },
    source: {
      source_kind: "exact",
      source_json_available: true,
      source_json_truncated: false,
      source_json_bytes: 240,
    },
    diagnostics: [],
    incoming_edges: [],
    outgoing_edges: [],
    generation_groups: [],
    realizations: [],
  };
}

function graphPayload(): TopicGraphView {
  return {
    ok: true,
    mutated: false,
    topic_id: "alpha",
    topic_workspace_id: "alpha",
    graph_scope: "idea-lineage",
    renderer_hint: "react-flow-detail",
    generated_at: "2026-07-07T00:00:00Z",
    nodes: [
      {
        id: "idea:parent",
        record_id: "record-parent",
        material_kind: "idea",
        density_class: "sparse",
        title: "NCU counter trend and bottleneck classifier side output",
        summary: "Parent summary.",
        status: "candidate",
        idea_id: "parent",
      },
      {
        id: "idea:idea-1",
        record_id: "record-1",
        material_kind: "idea",
        density_class: "sparse",
        title: "Precision Idea",
        summary: "Compare corrected runtime curves.",
        status: "candidate",
        idea_id: "idea-1",
      },
      {
        id: "idea:child",
        record_id: "record-child",
        material_kind: "idea",
        density_class: "sparse",
        title: "Launch-overhead and NCU calibration for short-kernel runtime",
        summary: "Child summary.",
        status: "candidate",
        idea_id: "child",
      },
      {
        id: "idea:unrelated",
        record_id: "record-unrelated",
        material_kind: "idea",
        density_class: "sparse",
        title: "Unrelated Idea",
        summary: "Unrelated summary.",
        status: "candidate",
        idea_id: "unrelated",
        source: { source_json_path: "records/hiddenpath-ncu-source.json" },
        detail_refs: { record_detail: "/api/topics/alpha/records/hiddenpath-ncu-record" },
        renderer_hints: { cluster: "hiddenpath-ncu-cluster" },
        realizations: [{ note: "hiddenpath ncu realization metadata" }],
      },
    ],
    edges: [
      {
        id: "parent-to-main",
        source: "idea:parent",
        target: "idea:idea-1",
        relation_kind: "derived_from",
        canonical: true,
      },
      {
        id: "main-to-child",
        source: "idea:idea-1",
        target: "idea:child",
        relation_kind: "derived_from",
        canonical: true,
      },
      {
        id: "unrelated-self",
        source: "idea:unrelated",
        target: "idea:unrelated",
        relation_kind: "self",
        canonical: true,
      },
    ],
    groups: [],
    facets: {},
    diagnostics: [],
  };
}

function graphPayloadWithout(nodeId: string): TopicGraphView {
  const payload = graphPayload();
  return {
    ...payload,
    index_revision: "qidx:changed",
    nodes: payload.nodes.filter((node) => node.id !== nodeId),
    edges: payload.edges.filter((edge) => edge.source !== nodeId && edge.target !== nodeId),
  };
}
