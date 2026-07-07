import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { act, cleanup, fireEvent, render, screen } from "@testing-library/react";
import type React from "react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

type MockNode = {
  id: string;
  className?: string;
  data?: {
    label?: unknown;
  };
};

type MockFlowProps = {
  nodes?: MockNode[];
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
  ReactFlowProvider: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  useReactFlow: () => ({ fitView: vi.fn() }),
  ReactFlow: ({ nodes = [], onNodeClick, onNodeDoubleClick, onNodeMouseEnter, onNodeMouseMove, onNodeMouseLeave, children }: MockFlowProps) => (
    <div data-testid="react-flow">
      {nodes.map((node) => (
        <button
          className={node.className}
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
  getTopicGraph: vi.fn(),
}));

import { getTopicGraph } from "./api";
import { IdeaGraphPanel } from "./App";
import { workbenchCommands$ } from "./events";
import type { TopicGraphView } from "./types";

const getTopicGraphMock = vi.mocked(getTopicGraph);

describe("Idea graph panel interactions", () => {
  beforeEach(() => {
    getTopicGraphMock.mockResolvedValue(graphPayload());
  });

  afterEach(() => {
    cleanup();
    vi.useRealTimers();
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

  it("shows a delayed hover tooltip from graph payload metadata", async () => {
    renderWithQuery(<IdeaGraphPanel topicId="alpha" />);
    const node = await screen.findByTestId("graph-node-idea:idea-1");

    vi.useFakeTimers();
    fireEvent.mouseEnter(node, { clientX: 120, clientY: 140 });
    expect(screen.queryByRole("tooltip")).toBeNull();

    act(() => {
      vi.advanceTimersByTime(600);
    });

    expect(screen.getByRole("tooltip").textContent).toContain("Compare corrected runtime curves.");
    fireEvent.mouseLeave(node);
    expect(screen.queryByRole("tooltip")).toBeNull();
  });
});

function renderWithQuery(element: React.ReactElement) {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return render(<QueryClientProvider client={client}>{element}</QueryClientProvider>);
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
    ],
    edges: [],
    groups: [],
    facets: {},
    diagnostics: [],
  };
}
