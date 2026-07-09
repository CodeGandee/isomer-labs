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
  getTopicOverview: vi.fn(),
}));

import { getTopicOverview } from "./api";
import { TopicOverviewPanel } from "./App";
import { ToastNotificationsProvider } from "./toast-notifications";
import type { TopicOverviewResponse } from "./types";

const getTopicOverviewMock = vi.mocked(getTopicOverview);

describe("Topic overview panel", () => {
  beforeEach(() => {
    getTopicOverviewMock.mockReset();
    Object.defineProperty(navigator, "clipboard", {
      configurable: true,
      value: { writeText: vi.fn().mockResolvedValue(undefined) },
    });
  });

  afterEach(() => {
    cleanup();
  });

  it("renders topic overview Markdown first and moves Topic and Runtime JSON into the modal", async () => {
    getTopicOverviewMock.mockResolvedValue(topicOverviewPayload());
    renderWithQuery(<TopicOverviewPanel topicId="alpha" />);

    expect(await screen.findByRole("heading", { level: 1, name: "Alpha Overview" })).toBeTruthy();
    expect(document.body.textContent).toContain("Human-readable topic summary.");
    expect(document.body.textContent).not.toContain("topic_json_only");
    expect(document.body.textContent).not.toContain("runtime_json_only");

    fireEvent.click(screen.getByRole("button", { name: "Copy Markdown" }));
    await waitFor(() => expect(navigator.clipboard.writeText).toHaveBeenCalledWith(expect.stringContaining("# Alpha Overview")));
    expect(await screen.findByRole("status", { name: "Markdown copied." })).toBeTruthy();
    expect(document.querySelector(".copy-status")).toBeNull();

    fireEvent.click(screen.getByRole("button", { name: "View JSON" }));
    const dialog = await screen.findByRole("dialog", { name: "alpha Overview Data" });
    expect(dialog).toBeTruthy();
    expect(screen.getByRole("tab", { name: "Topic", selected: true })).toBeTruthy();
    expect(screen.getByRole("tab", { name: "Runtime" })).toBeTruthy();
    expect(screen.getByRole("tab", { name: "Source" })).toBeTruthy();
    expect(document.querySelector(".json-modal-code")?.textContent).toContain("topic_json_only");

    fireEvent.click(screen.getByRole("button", { name: "Copy JSON" }));
    await waitFor(() => expect(navigator.clipboard.writeText).toHaveBeenCalledWith(expect.stringContaining("topic_json_only")));
    expect(await screen.findByRole("status", { name: "JSON copied." })).toBeTruthy();
    expect(document.querySelector(".copy-status")).toBeNull();
  });

  it("shows a warning and disables Markdown copy when the overview file is missing", async () => {
    getTopicOverviewMock.mockResolvedValue({
      ...topicOverviewPayload(),
      overview: {
        semantic_label: "topic.intent.overview",
        path: "/workspace/intent/src/topic-overview.md",
        exists: false,
        content_markdown: null,
      },
      diagnostics: [
        {
          severity: "warning",
          code: "topic_overview_missing",
          message: "Topic overview Markdown is missing.",
        },
      ],
    });
    renderWithQuery(<TopicOverviewPanel topicId="alpha" />);

    expect((await screen.findAllByText("Topic overview Markdown is missing.")).length).toBeGreaterThan(0);
    expect((screen.getByRole("button", { name: "Copy Markdown" }) as HTMLButtonElement).disabled).toBe(true);

    fireEvent.click(screen.getByRole("button", { name: "View JSON" }));
    expect(await screen.findByRole("dialog", { name: "alpha Overview Data" })).toBeTruthy();
    expect(screen.getByRole("tab", { name: "Diagnostics" })).toBeTruthy();
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

function topicOverviewPayload(): TopicOverviewResponse {
  return {
    ok: true,
    mutated: false,
    topic_id: "alpha",
    topic_workspace_id: "alpha",
    overview: {
      semantic_label: "topic.intent.overview",
      path: "/workspace/intent/src/topic-overview.md",
      exists: true,
      content_markdown: "# Alpha Overview\n\nHuman-readable topic summary.",
      content_bytes: 46,
      content_cap_bytes: 524288,
    },
    topic_payload: {
      ok: true,
      mutated: false,
      topic_config: { topic_statement: "topic_json_only" },
      diagnostics: [],
    },
    runtime_payload: {
      ok: true,
      mutated: false,
      runtime: { status: "runtime_json_only" },
      diagnostics: [],
    },
    diagnostics: [],
  };
}
