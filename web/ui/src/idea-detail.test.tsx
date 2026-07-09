import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import type React from "react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

vi.mock("sigma", () => ({
  default: class {
    on() {}
    kill() {}
  },
}));

vi.mock("./api", async (importOriginal) => ({
  ...(await importOriginal<typeof import("./api")>()),
  getIdeaDetail: vi.fn(),
}));

import { getIdeaDetail } from "./api";
import { buildIdeaNodeHoverMarkdown, IdeaDetailPanel, openRecordFromNode } from "./App";
import { workbenchCommands$ } from "./events";
import { ToastNotificationsProvider } from "./toast-notifications";
import type { IdeaDetailResponse, TopicGraphView } from "./types";

const getIdeaDetailMock = vi.mocked(getIdeaDetail);

describe("Idea detail panel", () => {
  beforeEach(() => {
    getIdeaDetailMock.mockReset();
    Object.defineProperty(navigator, "clipboard", {
      configurable: true,
      value: { writeText: vi.fn().mockResolvedValue(undefined) },
    });
  });

  afterEach(() => {
    cleanup();
  });

  it("renders JSON as Markdown, opens the JSON modal, and copies exact JSON", async () => {
    getIdeaDetailMock.mockResolvedValue(ideaDetailPayload());
    renderWithQuery(<IdeaDetailPanel topicId="alpha" ideaId="idea-1" />);

    expect((await screen.findAllByRole("heading", { name: "Precision Idea" })).length).toBeGreaterThan(0);
    expect(document.body.textContent).toContain("Separate launch overhead.");
    expect(document.body.textContent).not.toContain("filter notes");
    expect(screen.getByRole("button", { name: "Open Source Record" })).toBeTruthy();
    expect(document.querySelector(".idea-status-row")?.textContent).not.toContain("latest_realization_source_path");
    expect(document.querySelector(".idea-status-row")?.textContent).not.toContain("sections.raw_ideas");

    expect(screen.queryByRole("button", { name: "Copy JSON" })).toBeNull();

    fireEvent.click(screen.getByRole("button", { name: "View JSON" }));
    const dialog = await screen.findByRole("dialog", { name: "Precision Idea Data" });
    expect(dialog).toBeTruthy();
    expect(screen.getByRole("tab", { name: "Main Record", selected: true })).toBeTruthy();
    expect(screen.getByRole("tab", { name: "Lineage" })).toBeTruthy();
    expect(screen.getByRole("tab", { name: "Realizations" })).toBeTruthy();
    expect(screen.getByRole("tab", { name: "Diagnostics" })).toBeTruthy();
    expect(document.querySelector(".json-modal-code")?.textContent).toContain("Separate launch overhead.");
    fireEvent.click(screen.getByRole("button", { name: "Copy JSON" }));
    await waitFor(() => expect(navigator.clipboard.writeText).toHaveBeenCalledWith(expect.stringContaining('"summary": "Separate launch overhead."')));
    expect(await screen.findByRole("status", { name: "JSON copied." })).toBeTruthy();
    expect(document.querySelector(".copy-status")).toBeNull();
    fireEvent.keyDown(dialog, { key: "Escape" });
    await waitFor(() => expect(screen.queryByRole("dialog")).toBeNull());
  });

  it("disables JSON actions when exact JSON is unavailable", async () => {
    getIdeaDetailMock.mockResolvedValue({
      ...ideaDetailPayload(),
      source: {
        source_kind: "missing",
        source_json_available: false,
        source_json_truncated: false,
      },
      idea_content: undefined,
      source_provenance: {
        source_kind: "missing",
      },
      diagnostics: [{ code: "source_json_unavailable", severity: "warning", message: "No source JSON." }],
    });
    renderWithQuery(<IdeaDetailPanel topicId="alpha" ideaId="idea-1" />);

    expect((await screen.findAllByRole("heading", { name: "Precision Idea" })).length).toBeGreaterThan(0);
    expect((screen.getByRole("button", { name: "View JSON" }) as HTMLButtonElement).disabled).toBe(true);
    expect(screen.queryByRole("button", { name: "Copy JSON" })).toBeNull();
  });

  it("builds compact Markdown for idea node hover previews", () => {
    expect(
      buildIdeaNodeHoverMarkdown({
        label: "Precision Idea",
        title: "Precision Idea",
        summary: "Compare corrected runtime curves.",
        status: "candidate",
        material_kind: "idea",
        record_id: "record-1",
        idea_id: "idea-1",
      }),
    ).toContain("- **Record:** record-1");
  });

  it("routes canonical idea graph nodes to idea detail and non-idea nodes to records", () => {
    const events: unknown[] = [];
    const subscription = workbenchCommands$.subscribe((event) => events.push(event));
    const graph = {
      nodes: [
        { id: "idea:idea-1", material_kind: "idea", record_id: "record-1", idea_id: "idea-1" },
        { id: "record:run-1", material_kind: "run", record_id: "run-1" },
      ],
    } as TopicGraphView;

    openRecordFromNode("alpha", graph, "idea:idea-1");
    openRecordFromNode("alpha", graph, "record:run-1");
    subscription.unsubscribe();

    expect(events).toEqual([
      { type: "open-idea", topicId: "alpha", ideaId: "idea-1" },
      { type: "open-record", topicId: "alpha", recordId: "run-1" },
    ]);
  });
});

function renderWithQuery(element: React.ReactElement) {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return render(
    <ToastNotificationsProvider>
      <QueryClientProvider client={client}>{element}</QueryClientProvider>
    </ToastNotificationsProvider>,
  );
}

function ideaDetailPayload(): IdeaDetailResponse {
  return {
    ok: true,
    mutated: false,
    topic_id: "alpha",
    topic_workspace_id: "alpha",
    idea_id: "idea-1",
    exists: true,
    idea: { idea_id: "idea-1", title: "Precision Idea", summary: "Separate launch overhead.", status: "candidate" },
    realizations: [{ idea_id: "idea-1", record_id: "record-1", latest: true }],
    latest_realization: { idea_id: "idea-1", record_id: "record-1", latest: true },
    latest_record: { record_id: "record-1", title: "Record 1" },
    generation_groups: [],
    incoming_edges: [],
    outgoing_edges: [],
    idea_content: {
      idea_id: "idea-1",
      title: "Precision Idea",
      summary: "Separate launch overhead.",
      evidence: ["A", "B"],
      source_json_path: "sections.raw_ideas[0]",
    },
    source_provenance: {
      source_kind: "latest_realization_source_path",
      source_record_id: "record-1",
      source_json_path: "sections.raw_ideas[0]",
      source_fragment_status: "exact",
      source_classification: "canonical_idea_source",
      payload_digest: "sha256:abc",
      source_json_bytes: 120,
    },
    source: {
      source_kind: "latest_realization_source_path",
      source_record_id: "record-1",
      source_json_path: "sections.raw_ideas[0]",
      source_json_available: true,
      source_json_truncated: false,
      source_json_bytes: 120,
      source_fragment_status: "exact",
      source_classification: "canonical_idea_source",
      payload_digest: "sha256:abc",
      source_json: {
        sections: {
          filter_notes: ["filter notes should stay in the source record"],
          raw_ideas: [
            {
              idea_id: "idea-1",
              title: "Precision Idea",
              summary: "Separate launch overhead.",
              evidence: ["A", "B"],
            },
          ],
        },
      },
    },
    diagnostics: [],
  };
}
