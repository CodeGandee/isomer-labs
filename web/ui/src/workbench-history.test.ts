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
    const state = readWorkbenchSearch("?topic=alpha&graph=artifact-overview&open=topic:alpha:records");
    expect(state).toEqual({
      topicId: "alpha",
      graphScope: "artifact-overview",
      openItemId: "topic:alpha:records",
    });
    expect(workbenchUrlForState(state)).toBe("/?topic=alpha&graph=artifact-overview&open=topic%3Aalpha%3Arecords");
  });

  it("falls back to idea-lineage for invalid graph scopes", () => {
    expect(readWorkbenchSearch("?topic=alpha&graph=nope")).toEqual({
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

    const silent = writeWorkbenchHistory({ topicId: "beta", graphScope: "paper-revisions" }, { mode: "silent", metadata: { navigationIndex: 3 } });
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
