import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

vi.mock("sigma", () => ({
  default: class {
    on() {}
    kill() {}
  },
}));

import { ExplorerPane } from "./App";
import type { ExplorerNode } from "./types";

describe("ExplorerPane", () => {
  it("renders semantic tree rows and expands collapsed Research Topics", () => {
    const nodes: ExplorerNode[] = [
      {
        id: "project",
        parent_id: null,
        label: "demo",
        item_kind: "project",
        icon_hint: "project",
        openable_item_id: "project:overview",
        has_children: true,
        children_loaded: true,
      },
      {
        id: "project:topics",
        parent_id: "project",
        label: "Research Topics",
        item_kind: "research_topics",
        icon_hint: "topics",
        has_children: true,
        children_loaded: true,
      },
      {
        id: "topic:alpha",
        parent_id: "project:topics",
        label: "alpha",
        item_kind: "research_topic",
        icon_hint: "topic",
        openable_item_id: "topic:alpha:overview",
        topic_id: "alpha",
        has_children: true,
        children_loaded: false,
      },
    ];
    const onExpandTopic = vi.fn();
    const onOpenItem = vi.fn();
    const onExpandedItemsChange = vi.fn();

    render(
      <ExplorerPane
        nodes={nodes}
        rootNodeId="project"
        expandedItems={["project", "project:topics"]}
        selectedTopicId="alpha"
        onExpandedItemsChange={onExpandedItemsChange}
        onExpandTopic={onExpandTopic}
        onOpenItem={onOpenItem}
      />,
    );

    fireEvent.click(screen.getByTestId("explorer-row-topic:alpha"));

    expect(onExpandTopic).toHaveBeenCalledWith("alpha");
    expect(onOpenItem).toHaveBeenCalledWith("topic:alpha:overview");
    expect(onExpandedItemsChange).toHaveBeenCalledWith(expect.arrayContaining(["topic:alpha"]));
    expect(onExpandedItemsChange).toHaveBeenCalledWith(expect.arrayContaining(["topic:alpha:graphs"]));
  });
});
