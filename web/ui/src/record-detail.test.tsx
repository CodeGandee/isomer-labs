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
  getViewerDescriptor: vi.fn(),
  getRecordDetail: vi.fn(),
  getRecordRender: vi.fn(),
  getRecordLineage: vi.fn(),
  getRecordSiblings: vi.fn(),
  getRecordFiles: vi.fn(),
  getRecordFacets: vi.fn(),
}));

import {
  getRecordDetail,
  getRecordFacets,
  getRecordFiles,
  getRecordLineage,
  getRecordRender,
  getRecordSiblings,
  getViewerDescriptor,
} from "./api";
import { parentIdeaNavigation, RecordDetailPanel } from "./App";
import { workbenchCommands$, type WorkbenchCommand } from "./events";
import { ToastNotificationsProvider } from "./toast-notifications";
import type { RecordDetailResponse, RecordRenderResponse, ViewerDescriptor } from "./types";

const getViewerDescriptorMock = vi.mocked(getViewerDescriptor);
const getRecordDetailMock = vi.mocked(getRecordDetail);
const getRecordRenderMock = vi.mocked(getRecordRender);
const getRecordLineageMock = vi.mocked(getRecordLineage);
const getRecordSiblingsMock = vi.mocked(getRecordSiblings);
const getRecordFilesMock = vi.mocked(getRecordFiles);
const getRecordFacetsMock = vi.mocked(getRecordFacets);

describe("Record detail panel", () => {
  beforeEach(() => {
    getViewerDescriptorMock.mockResolvedValue(recordDescriptor());
    getRecordDetailMock.mockResolvedValue(recordDetail());
    getRecordRenderMock.mockResolvedValue(recordRender());
    getRecordLineageMock.mockResolvedValue({ ok: true, mutated: false, operation: "query.lineage", record_id: "record-1", nodes: [], edges: [], diagnostics: [] });
    getRecordSiblingsMock.mockResolvedValue({ ok: true, mutated: false, operation: "query.siblings", record_id: "record-1", nodes: [], edges: [], generation_groups: [], diagnostics: [] });
    getRecordFilesMock.mockResolvedValue({ ok: true, mutated: false, topic_id: "alpha", record_id: "record-1", files: [], diagnostics: [] });
    getRecordFacetsMock.mockResolvedValue({ ok: true, mutated: false, operation: "query.facets", record_id: "record-1", diagnostics: [], ideas: [] });
    Object.defineProperty(navigator, "clipboard", {
      configurable: true,
      value: { writeText: vi.fn().mockResolvedValue(undefined) },
    });
  });

  afterEach(() => {
    cleanup();
  });

  it("renders Markdown first, groups JSON in a modal, and copies Markdown and filepath", async () => {
    renderWithQuery(<RecordDetailPanel topicId="alpha" recordId="record-1" />);

    expect(await screen.findByRole("heading", { name: "Runtime Record" })).toBeTruthy();
    await waitFor(() => expect(document.body.textContent).toContain("Rendered record body."));
    expect(document.body.textContent).toContain("records/artifacts/record-1/payload.json");
    expect(document.body.textContent).toContain("parent idea: I-7 Parent idea");
    expect(screen.getByRole("button", { name: "Open parent idea I-7 Parent idea" })).toBeTruthy();
    expect(document.body.textContent).not.toContain("Idea Lineage");

    fireEvent.click(screen.getByRole("button", { name: "Copy Markdown" }));
    await waitFor(() => expect(navigator.clipboard.writeText).toHaveBeenCalledWith("# Runtime Record\n\nRendered record body."));
    expect(await screen.findByRole("status", { name: "Markdown copied." })).toBeTruthy();
    expect(document.querySelector(".copy-status")).toBeNull();

    fireEvent.click(screen.getByRole("button", { name: "Copy Filepath" }));
    await waitFor(() => expect(navigator.clipboard.writeText).toHaveBeenCalledWith("/tmp/project/topic/records/artifacts/record-1/payload.json"));
    expect(await screen.findByRole("status", { name: "Filepath copied." })).toBeTruthy();
    expect(document.querySelector(".copy-status")).toBeNull();

    fireEvent.click(screen.getByRole("button", { name: "View JSON" }));
    const dialog = await screen.findByRole("dialog", { name: "Runtime Record Data" });
    expect(dialog).toBeTruthy();
    expect(screen.getByRole("tab", { name: "Detail", selected: true })).toBeTruthy();
    expect(screen.getByRole("tab", { name: "Descriptor" })).toBeTruthy();
    expect(screen.getByRole("tab", { name: "Render" })).toBeTruthy();
    expect(screen.getByRole("tab", { name: "Lineage" })).toBeTruthy();
    expect(screen.getByRole("tab", { name: "Files" })).toBeTruthy();
    await waitFor(() => expect((screen.getByRole("button", { name: "Copy JSON" }) as HTMLButtonElement).disabled).toBe(false));
    fireEvent.click(screen.getByRole("button", { name: "Copy JSON" }));
    await waitFor(() => expect(navigator.clipboard.writeText).toHaveBeenCalledWith(expect.stringContaining('"record_id": "record-1"')));
  });

  it("opens parent idea links through the workbench command and reports stale link failures", async () => {
    const commands: WorkbenchCommand[] = [];
    const subscription = workbenchCommands$.subscribe((command) => commands.push(command));
    renderWithQuery(<RecordDetailPanel topicId="alpha" recordId="record-1" />);

    fireEvent.click(await screen.findByRole("button", { name: "Open parent idea I-7 Parent idea" }));
    expect(commands).toHaveLength(1);
    expect(commands[0]).toMatchObject({ type: "open-idea", topicId: "alpha", ideaId: "idea-7" });

    if (commands[0].type === "open-idea") {
      commands[0].onOpenResult?.({ status: "ignored" });
    }
    expect(await screen.findByRole("alert", { name: "Parent idea is no longer available." })).toBeTruthy();
    expect(document.body.textContent).toContain("I-7 Parent idea");
    subscription.unsubscribe();
  });

  it("keeps parent idea labels inert when no stable idea id exists", async () => {
    const parentWithoutIdeaId = { display_key: "I-7", title: "Parent idea" };
    getViewerDescriptorMock.mockResolvedValue({ ...recordDescriptor(), direct_parent_idea: parentWithoutIdeaId });
    getRecordDetailMock.mockResolvedValue({ ...recordDetail(), direct_parent_idea: parentWithoutIdeaId });
    getRecordRenderMock.mockResolvedValue({ ...recordRender(), direct_parent_idea: parentWithoutIdeaId });
    renderWithQuery(<RecordDetailPanel topicId="alpha" recordId="record-1" />);

    await screen.findByText("parent idea: I-7 Parent idea");
    expect(screen.queryByRole("button", { name: "Open parent idea I-7 Parent idea" })).toBeNull();
  });

  it("extracts parent idea navigation from structured metadata only", () => {
    expect(parentIdeaNavigation({ idea_id: "idea-7", display_key: "I-7", title: "Parent idea" })).toEqual({
      ideaId: "idea-7",
      label: "I-7 Parent idea",
    });
    expect(parentIdeaNavigation({ display_key: "I-7", title: "Parent idea" })).toEqual({
      ideaId: "",
      label: "I-7 Parent idea",
    });
    expect(parentIdeaNavigation(null)).toBeNull();
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

function recordDescriptor(): ViewerDescriptor {
  return {
    ok: true,
    mutated: false,
    topic_id: "alpha",
    record_id: "record-1",
    title: "Runtime Record",
    viewer_kind: "markdown",
    primary_content_url: "/api/topics/alpha/records/record-1/render",
    detail_url: "/api/topics/alpha/records/record-1",
    render_url: "/api/topics/alpha/records/record-1/render",
    files_url: "/api/topics/alpha/records/record-1/files",
    facets_url: "/api/topics/alpha/records/record-1/facets",
    media_type: "text/markdown",
    exists: true,
    topic_workspace_relative_path: "records/artifacts/record-1/payload.json",
    absolute_filepath: "/tmp/project/topic/records/artifacts/record-1/payload.json",
    direct_parent_idea: {
      idea_id: "idea-7",
      display_key: "I-7",
      title: "Parent idea",
      source: "canonical_realization",
    },
    diagnostics: [],
  };
}

function recordDetail(): RecordDetailResponse {
  return {
    ok: true,
    mutated: false,
    operation: "show",
    record: { id: "record-1", record_id: "record-1", title: "Runtime Record" },
    structured_payload: { payload: { title: "Runtime Record", summary: "Record summary" } },
    topic_workspace_relative_path: "records/artifacts/record-1/payload.json",
    absolute_filepath: "/tmp/project/topic/records/artifacts/record-1/payload.json",
    direct_parent_idea: { idea_id: "idea-7", display_key: "I-7", title: "Parent idea" },
    diagnostics: [],
  };
}

function recordRender(): RecordRenderResponse {
  return {
    ok: true,
    mutated: false,
    operation: "render",
    record: { id: "record-1", title: "Runtime Record" },
    render: { content: "# Runtime Record\n\nRendered record body." },
    topic_workspace_relative_path: "records/artifacts/record-1/payload.json",
    absolute_filepath: "/tmp/project/topic/records/artifacts/record-1/payload.json",
    direct_parent_idea: { idea_id: "idea-7", display_key: "I-7", title: "Parent idea" },
    diagnostics: [],
  };
}
