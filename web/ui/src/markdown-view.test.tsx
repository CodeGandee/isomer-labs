import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

vi.mock("sigma", () => ({
  default: class {
    on() {}
    kill() {}
  },
}));

import { MarkdownView, ViewerContent } from "./App";

describe("Markdown viewer", () => {
  it("shows a loading state while Markdown render data is pending", () => {
    render(<ViewerContent descriptor={{ viewer_kind: "markdown" }} rendered={undefined} detail={undefined} renderIsPending />);

    expect(screen.getByText("Rendering Markdown.")).toBeTruthy();
    expect(screen.queryByText("No rendered Markdown available.")).toBeNull();
  });

  it("shows an empty fallback after a completed empty Markdown render", () => {
    render(<ViewerContent descriptor={{ viewer_kind: "markdown" }} rendered={{ render: { content: "" } }} detail={undefined} renderIsPending={false} />);

    expect(screen.getByText("No rendered Markdown available.")).toBeTruthy();
  });

  it("renders GitHub-style Markdown structures through the existing Markdown stack", () => {
    render(
      <MarkdownView
        content={[
          "# Runtime Model",
          "",
          "A [record](https://example.com) with `inline code`.",
          "",
          "- First idea",
          "- Second idea",
          "",
          "> Keep this review human-readable.",
          "",
          "```python",
          "print('hello')",
          "```",
          "",
          "| Field | Value |",
          "| --- | --- |",
          "| Outcome | Better preview |",
        ].join("\n")}
      />,
    );

    expect(screen.getByRole("heading", { level: 1, name: "Runtime Model" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "record" })).toBeTruthy();
    expect(screen.getByText("inline code")).toBeTruthy();
    expect(screen.getByText("Keep this review human-readable.")).toBeTruthy();
    expect(screen.getByText("print('hello')")).toBeTruthy();
    expect(screen.getByRole("cell", { name: "Better preview" })).toBeTruthy();
  });
});
