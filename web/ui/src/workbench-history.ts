import type { GraphScope } from "./types";

export const WORKBENCH_HISTORY_KIND = "isomer-workbench";

export type WorkbenchSearchState = {
  topicId?: string;
  graphScope: GraphScope;
  openItemId?: string;
};

export type WorkbenchHistoryState = WorkbenchSearchState & {
  kind: typeof WORKBENCH_HISTORY_KIND;
  activePanelId?: string;
  openedPanelId?: string;
  closeOnBack?: boolean;
  navigationIndex?: number;
};

export type WorkbenchHistoryMetadata = Partial<Omit<WorkbenchHistoryState, "kind" | "topicId" | "graphScope" | "openItemId">>;

export type UrlSyncMode = "push" | "replace" | "silent";

export function isGraphScope(value: string | null | undefined): value is GraphScope {
  return value === "idea-lineage" || value === "idea-timeline";
}

export function readWorkbenchSearch(search: string): WorkbenchSearchState {
  const params = new URLSearchParams(search);
  const graph = params.get("graph");
  return {
    topicId: params.get("topic") || undefined,
    graphScope: isGraphScope(graph) ? graph : "idea-lineage",
    openItemId: params.get("open") || undefined,
  };
}

export function workbenchUrlForState(next: WorkbenchSearchState): string {
  const params = new URLSearchParams();
  if (next.topicId) {
    params.set("topic", next.topicId);
  }
  params.set("graph", next.graphScope);
  if (next.openItemId) {
    params.set("open", next.openItemId);
  }
  return `/?${params.toString()}`;
}

export function createWorkbenchHistoryState(next: WorkbenchSearchState, metadata: WorkbenchHistoryMetadata = {}): WorkbenchHistoryState {
  return {
    kind: WORKBENCH_HISTORY_KIND,
    topicId: next.topicId,
    graphScope: next.graphScope,
    openItemId: next.openItemId,
    activePanelId: metadata.activePanelId,
    openedPanelId: metadata.openedPanelId,
    closeOnBack: metadata.closeOnBack,
    navigationIndex: metadata.navigationIndex,
  };
}

export function isWorkbenchHistoryState(value: unknown): value is WorkbenchHistoryState {
  const candidate = value as Partial<WorkbenchHistoryState> | null | undefined;
  return Boolean(candidate && candidate.kind === WORKBENCH_HISTORY_KIND && isGraphScope(candidate.graphScope));
}

export function coerceWorkbenchHistoryState(value: unknown, next: WorkbenchSearchState): WorkbenchHistoryState {
  if (!isWorkbenchHistoryState(value)) {
    return createWorkbenchHistoryState(next);
  }
  return createWorkbenchHistoryState(next, {
    activePanelId: value.activePanelId,
    openedPanelId: value.openedPanelId,
    closeOnBack: value.closeOnBack,
    navigationIndex: value.navigationIndex,
  });
}

export function semanticOpenItemForState(state: WorkbenchSearchState): string | undefined {
  if (state.openItemId) {
    return state.openItemId;
  }
  return state.topicId ? `topic:${state.topicId}:overview` : undefined;
}

export function writeWorkbenchHistory(
  next: WorkbenchSearchState,
  options: { mode?: UrlSyncMode; metadata?: WorkbenchHistoryMetadata } = {},
): WorkbenchHistoryState {
  const mode = options.mode || "replace";
  const historyState = createWorkbenchHistoryState(next, options.metadata || {});
  if (mode !== "silent") {
    const method = mode === "push" ? "pushState" : "replaceState";
    window.history[method](historyState, "", workbenchUrlForState(next));
  }
  return historyState;
}
