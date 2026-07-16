import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import type React from "react";
import { afterEach, describe, expect, it, vi } from "vitest";

vi.mock("../../api", async (importOriginal) => ({
  ...(await importOriginal<typeof import("../../api")>()),
  steerIdea: vi.fn(),
}));

import { IdeaDecisionContextPanel } from "./IdeaDecisionContextPanel";
import { IdeaSteeringDialog } from "./IdeaSteeringDialog";
import { PortfolioControls } from "./PortfolioControls";
import type { IdeaDecisionContextResponse, TopicGraphNode, TopicGraphView } from "../../types";

afterEach(cleanup);

describe("idea portfolio components", () => {
  it("exposes accessible preset and facet controls with visible source counts", () => {
    const onChange = vi.fn();
    render(<PortfolioControls graph={portfolioGraph()} state={{ preset: "current" }} onChange={onChange} />);
    expect(screen.getByRole("region", { name: "Idea portfolio filters" })).toBeTruthy();
    expect(screen.getByText("2 visible / 4 source")).toBeTruthy();
    fireEvent.change(screen.getByLabelText("Idea portfolio preset"), { target: { value: "closed" } });
    expect(onChange).toHaveBeenCalledWith({ preset: "closed" });
    fireEvent.change(screen.getByLabelText("Evidence state"), { target: { value: "mixed" } });
    expect(onChange).toHaveBeenCalledWith({ preset: "current", evidenceState: "mixed" });
  });

  it("shows nested idea identity, closure reason, incomplete context, and reopen history", () => {
    render(
      <IdeaDecisionContextPanel
        response={decisionContext()}
        isLoading={false}
        error={null}
        onClose={vi.fn()}
      />,
    );
    expect(screen.getByRole("complementary", { name: "Idea decision history" })).toBeTruthy();
    expect(screen.getByText(/I-2 Closed alternative/)).toBeTruthy();
    expect(screen.getByText(/duplication/)).toBeTruthy();
    expect(screen.getByText("partial option set")).toBeTruthy();
    expect(screen.getByText(/closed → open/)).toBeTruthy();
    expect(screen.getByText("Historical option rationale is missing.")).toBeTruthy();
  });

  it("requires explicit reopening confirmation and previews every exact replacement transition", () => {
    renderWithQuery(
      <IdeaSteeringDialog
        topicId="alpha"
        action="explore_instead"
        target={ideaNode("target", "unexplored", "closed", "I-2")}
        replacements={[ideaNode("current", "exploring", "selected", "I-1")]}
        indexRevision="qidx:before"
        onClose={vi.fn()}
        onAccepted={vi.fn()}
      />,
    );
    expect(screen.getByRole("dialog")).toBeTruthy();
    expect(screen.getByText("I-2: decision closed → open")).toBeTruthy();
    expect(screen.getByText("I-2: decision open → selected")).toBeTruthy();
    expect(screen.getByText("I-1: decision selected → deferred")).toBeTruthy();
    const confirm = screen.getByRole("button", { name: "Confirm and route" }) as HTMLButtonElement;
    expect(confirm.disabled).toBe(true);
    fireEvent.change(screen.getByLabelText("Steering rationale"), { target: { value: "Reopen the target and replace the current route." } });
    fireEvent.click(screen.getByRole("checkbox"));
    expect(confirm.disabled).toBe(false);
  });
});

function renderWithQuery(element: React.ReactElement) {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false }, mutations: { retry: false } } });
  return render(<QueryClientProvider client={client}>{element}</QueryClientProvider>);
}

function ideaNode(ideaId: string, explorationState: string, decisionState: string, displayKey: string): TopicGraphNode {
  return {
    id: `idea:${ideaId}`,
    record_id: `record:${ideaId}`,
    material_kind: "idea",
    density_class: "sparse",
    title: `${displayKey} ${ideaId}`,
    idea_id: ideaId,
    display_key: displayKey,
    exploration_state: explorationState,
    decision_state: decisionState,
    evidence_state: "unassessed",
    archive_state: "active",
    visibility: "primary",
  };
}

function portfolioGraph(): TopicGraphView {
  return {
    ok: true,
    mutated: false,
    topic_id: "alpha",
    topic_workspace_id: "alpha",
    graph_scope: "idea-lineage",
    renderer_hint: "react-flow-detail",
    generated_at: "2026-07-17T00:00:00Z",
    nodes: [],
    edges: [],
    groups: [],
    facets: {},
    portfolio: {
      source_counts: { ideas: 4 },
      visible_counts: { ideas: 2 },
    },
    topology_complete: true,
    diagnostics: [],
  };
}

function decisionContext(): IdeaDecisionContextResponse {
  return {
    ok: true,
    mutated: false,
    topic_id: "alpha",
    topic_workspace_id: "alpha",
    operation: "ideas.decision-context",
    decisions: [
      {
        decision_record_id: "decision-1",
        option_set_complete: false,
        options: [
          {
            idea_id: "closed",
            outcome: "closed",
            reason_code: "duplication",
            idea: { idea_id: "closed", display_key: "I-2", title: "Closed alternative" },
          },
        ],
      },
    ],
    ideas: [],
    transitions: [],
    reopen_history: [{ id: "reopen-1", previous_value: "closed", next_value: "open", rationale: "New evidence warrants review." }],
    diagnostics: [{ severity: "warning", code: "idea_decision_context_incomplete", message: "Historical option rationale is missing." }],
  };
}
