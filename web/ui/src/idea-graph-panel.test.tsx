import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { act, cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import type React from "react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

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
  ReactFlow: ({ nodes = [], edges = [], onNodeClick, onNodeDoubleClick, onNodeMouseEnter, onNodeMouseMove, onNodeMouseLeave, children }: MockFlowProps) => (
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
  ),
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

import { getIdeaDetail, getTopicGraph } from "./api";
import { IdeaGraphPanel } from "./App";
import { workbenchCommands$ } from "./events";
import type { TopicGraphView } from "./types";

const getIdeaDetailMock = vi.mocked(getIdeaDetail);
const getTopicGraphMock = vi.mocked(getTopicGraph);

describe("Idea graph panel interactions", () => {
  beforeEach(() => {
    getIdeaDetailMock.mockResolvedValue(ideaDetailPayload());
    getTopicGraphMock.mockResolvedValue(graphPayload());
  });

  afterEach(() => {
    cleanup();
    vi.useRealTimers();
    getIdeaDetailMock.mockReset();
    getTopicGraphMock.mockReset();
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
      vi.advanceTimersByTime(1999);
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

  it("keeps the hover tooltip open while the pointer is inside it", async () => {
    getIdeaDetailMock.mockReturnValue(new Promise(() => {}));
    renderWithQuery(<IdeaGraphPanel topicId="alpha" />);
    const node = await screen.findByTestId("graph-node-idea:idea-1");

    vi.useFakeTimers();
    fireEvent.mouseEnter(node, { clientX: 120, clientY: 140 });
    act(() => {
      vi.advanceTimersByTime(2000);
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
      vi.advanceTimersByTime(2000);
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
      vi.advanceTimersByTime(2000);
    });
    expect(screen.queryByRole("tooltip")).toBeNull();

    fireEvent.pointerDown(node, { pointerId: 12, pointerType: "touch", clientX: 155, clientY: 165 });
    act(() => {
      vi.advanceTimersByTime(2000);
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
      vi.advanceTimersByTime(2000);
    });
    expect(screen.getByRole("tooltip").textContent).toContain("Loading preview");

    fireEvent.doubleClick(node);
    expect(screen.queryByRole("tooltip")).toBeNull();
    expect(events).toEqual([{ type: "open-idea", topicId: "alpha", ideaId: "idea-1" }]);
    subscription.unsubscribe();
  });

  it("highlights selected node parents, children, and adjacent edges", async () => {
    renderWithQuery(<IdeaGraphPanel topicId="alpha" />);
    const node = await screen.findByTestId("graph-node-idea:idea-1");

    fireEvent.click(node);

    expect(screen.getByTestId("graph-node-idea:parent").className).toContain("lineage-parent");
    expect(screen.getByTestId("graph-node-idea:idea-1").className).toContain("selected");
    expect(screen.getByTestId("graph-node-idea:child").className).toContain("lineage-child");
    expect(screen.getByTestId("graph-edge-parent-to-main").className).toContain("lineage-incoming");
    expect(screen.getByTestId("graph-edge-main-to-child").className).toContain("lineage-outgoing");
  });
});

function renderWithQuery(element: React.ReactElement) {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return render(<QueryClientProvider client={client}>{element}</QueryClientProvider>);
}

function ideaDetailPayload() {
  return {
    ok: true,
    mutated: false,
    topic_id: "alpha",
    topic_workspace_id: "alpha",
    idea: {
      idea_id: "idea-1",
      title: "Precision Idea",
      one_liner: "Separate launch overhead.",
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
        title: "Parent Idea",
        one_liner: "Parent branch.",
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
        one_liner: "Separate launch overhead.",
        summary: "Compare corrected runtime curves.",
        status: "candidate",
        idea_id: "idea-1",
      },
      {
        id: "idea:child",
        record_id: "record-child",
        material_kind: "idea",
        density_class: "sparse",
        title: "Child Idea",
        one_liner: "Child branch.",
        summary: "Child summary.",
        status: "candidate",
        idea_id: "child",
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
    ],
    groups: [],
    facets: {},
    diagnostics: [],
  };
}
