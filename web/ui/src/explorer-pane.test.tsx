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

  it("renders topic navigation without low-level implementation rows", () => {
    const nodes: ExplorerNode[] = [
      {
        id: "project",
        parent_id: null,
        label: "demo",
        item_kind: "project",
        icon_hint: "project",
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
        children_loaded: true,
      },
      {
        id: "topic:alpha:overview",
        parent_id: "topic:alpha",
        label: "Overview",
        item_kind: "topic_overview",
        icon_hint: "overview",
        openable_item_id: "topic:alpha:overview",
        topic_id: "alpha",
      },
      {
        id: "topic:alpha:graphs",
        parent_id: "topic:alpha",
        label: "Graphs",
        item_kind: "graph_collection",
        icon_hint: "graph",
        has_children: true,
        children_loaded: true,
      },
      {
        id: "topic:alpha:graph:idea-lineage",
        parent_id: "topic:alpha:graphs",
        label: "Idea Lineage",
        item_kind: "graph",
        icon_hint: "graph",
        openable_item_id: "topic:alpha:graph:idea-lineage",
        topic_id: "alpha",
      },
      {
        id: "topic:alpha:records",
        parent_id: "topic:alpha",
        label: "Records",
        item_kind: "record_collection",
        icon_hint: "records",
        openable_item_id: "topic:alpha:records",
        topic_id: "alpha",
      },
    ];

    render(
      <ExplorerPane
        nodes={nodes}
        rootNodeId="project"
        expandedItems={["project", "project:topics", "topic:alpha", "topic:alpha:graphs"]}
        selectedTopicId="alpha"
        onExpandedItemsChange={vi.fn()}
        onExpandTopic={vi.fn()}
        onOpenItem={vi.fn()}
      />,
    );

    expect(screen.getByText("Overview")).toBeTruthy();
    expect(screen.getByText("Graphs")).toBeTruthy();
    expect(screen.getByText("Records")).toBeTruthy();
    expect(screen.queryByText("Workspace Runtime")).toBeNull();
    expect(screen.queryByText("Topic Actors")).toBeNull();
    expect(screen.queryByText("Repositories")).toBeNull();
  });
});
