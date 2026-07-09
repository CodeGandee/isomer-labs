import { beforeEach, describe, expect, it } from "vitest";
import {
  coerceWorkbenchHistoryState,
  createWorkbenchHistoryState,
  readWorkbenchSearch,
  semanticOpenItemForState,
  workbenchUrlForState,
  writeWorkbenchHistory,
} from "./workbench-history";

describe("workbench history helpers", () => {
  beforeEach(() => {
    window.history.replaceState(null, "", "/");
  });

  it("reads and writes bookmarkable workbench query state", () => {
    const state = readWorkbenchSearch("?topic=alpha&graph=idea-timeline&open=topic:alpha:graph:idea-timeline");
    expect(state).toEqual({
      topicId: "alpha",
      graphScope: "idea-timeline",
      openItemId: "topic:alpha:graph:idea-timeline",
    });
    expect(workbenchUrlForState(state)).toBe("/?topic=alpha&graph=idea-timeline&open=topic%3Aalpha%3Agraph%3Aidea-timeline");
  });

  it("falls back to idea-lineage for invalid graph scopes", () => {
    expect(readWorkbenchSearch("?topic=alpha&graph=artifact-overview")).toEqual({
      topicId: "alpha",
      graphScope: "idea-lineage",
      openItemId: undefined,
    });
  });

  it("creates structured history state with panel provenance", () => {
    expect(
      createWorkbenchHistoryState(
        { topicId: "alpha", graphScope: "idea-lineage", openItemId: "record:alpha:idea" },
        { activePanelId: "panel-record", openedPanelId: "panel-record", closeOnBack: true, navigationIndex: 2 },
      ),
    ).toMatchObject({
      kind: "isomer-workbench",
      topicId: "alpha",
      openItemId: "record:alpha:idea",
      activePanelId: "panel-record",
      openedPanelId: "panel-record",
      closeOnBack: true,
      navigationIndex: 2,
    });
  });

  it("keeps silent writes local and push writes in browser history", () => {
    const replaced = writeWorkbenchHistory({ topicId: "alpha", graphScope: "idea-lineage" }, { mode: "replace", metadata: { navigationIndex: 0 } });
    expect(window.location.search).toBe("?topic=alpha&graph=idea-lineage");
    expect(window.history.state).toEqual(replaced);

    const pushed = writeWorkbenchHistory(
      { topicId: "alpha", graphScope: "idea-lineage", openItemId: "topic:alpha:records" },
      { mode: "push", metadata: { activePanelId: "records", openedPanelId: "records", closeOnBack: true, navigationIndex: 1 } },
    );
    expect(window.location.search).toContain("open=topic%3Aalpha%3Arecords");
    expect(window.history.state).toEqual(pushed);

    const silent = writeWorkbenchHistory({ topicId: "beta", graphScope: "idea-timeline" }, { mode: "silent", metadata: { navigationIndex: 3 } });
    expect(window.location.search).toContain("open=topic%3Aalpha%3Arecords");
    expect(window.history.state).toEqual(pushed);
    expect(silent.topicId).toBe("beta");
  });

  it("coerces bookmark entries and derives topic overview fallback targets", () => {
    const search = { topicId: "alpha", graphScope: "idea-lineage" as const };
    expect(coerceWorkbenchHistoryState(null, search)).toMatchObject({ kind: "isomer-workbench", topicId: "alpha" });
    expect(semanticOpenItemForState(search)).toBe("topic:alpha:overview");
  });
});
