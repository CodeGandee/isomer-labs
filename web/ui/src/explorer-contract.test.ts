import { describe, expect, it } from "vitest";
import { OpenableItemDescriptorSchema, ProjectExplorerResponseSchema } from "./types";
import { openPanelFromDescriptor, panelOptionsFromDescriptor } from "./view-model";

describe("Project Explorer contract", () => {
  it("validates semantic Project Explorer responses", () => {
    const parsed = ProjectExplorerResponseSchema.parse({
      ok: true,
      mutated: false,
      revision: "pexp:abc",
      root_node_ids: ["project"],
      nodes: [
        {
          id: "project",
          parent_id: null,
          label: "demo",
          item_kind: "project",
          icon_hint: "project",
          openability_state: "openable",
          openable_item_id: "project:overview",
          diagnostics_count: 0,
          has_children: true,
          children_loaded: true,
        },
        {
          id: "topic:alpha",
          parent_id: "project:topics",
          label: "alpha",
          item_kind: "research_topic",
          icon_hint: "topic",
          topic_id: "alpha",
          has_children: true,
          children_loaded: false,
        },
      ],
      diagnostics: [],
    });

    expect(parsed.nodes[1].item_kind).toBe("research_topic");
    expect(parsed.nodes[1].children_loaded).toBe(false);
  });

  it("maps openable descriptors to deterministic Dockview panel options", () => {
    const descriptor = OpenableItemDescriptorSchema.parse({
      ok: true,
      mutated: false,
      openable_item_id: "topic:alpha:graph:idea-lineage",
      tab_id: "topic-alpha-graph-idea-lineage",
      item_kind: "graph",
      title: "Idea Lineage Graph",
      preferred_tab_component: "ideaGraph",
      topic_id: "alpha",
      graph_scope: "idea-lineage",
      exists: true,
      diagnostics: [],
    });

    expect(panelOptionsFromDescriptor(descriptor)).toMatchObject({
      id: "topic-alpha-graph-idea-lineage",
      component: "ideaGraph",
      title: "Idea Lineage Graph",
      params: {
        topicId: "alpha",
        graphScope: "idea-lineage",
        itemKind: "graph",
      },
    });
  });

  it("creates new tabs, focuses existing tabs, and ignores invalid descriptors", () => {
    const descriptor = OpenableItemDescriptorSchema.parse({
      ok: true,
      mutated: false,
      openable_item_id: "topic:alpha:records",
      tab_id: "topic-alpha-records",
      item_kind: "record_collection",
      title: "Records",
      preferred_tab_component: "records",
      topic_id: "alpha",
      exists: true,
      diagnostics: [],
    });
    const added: unknown[] = [];
    const focused = { count: 0 };

    expect(openPanelFromDescriptor({ addPanel: (panel) => added.push(panel) }, descriptor)).toEqual({ status: "created", panelId: "topic-alpha-records" });
    expect(added).toHaveLength(1);
    expect(openPanelFromDescriptor({ getPanel: () => ({ id: "topic-alpha-records", api: { setActive: () => focused.count += 1 } }) }, descriptor)).toEqual({
      status: "focused",
      panelId: "topic-alpha-records",
    });
    expect(focused.count).toBe(1);
    expect(openPanelFromDescriptor(null, { ...descriptor, ok: false })).toEqual({ status: "ignored" });
  });
});
