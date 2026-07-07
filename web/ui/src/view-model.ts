import type { OpenableItemDescriptor, RecordSummary, ViewerDescriptor } from "./types";

export function filterRecords(records: RecordSummary[], search: string): RecordSummary[] {
  const haystack = search.toLowerCase().trim();
  if (!haystack) {
    return records;
  }
  return records.filter((record) =>
    [record.record_id, record.record_kind, record.status, record.title, record.summary, record.profile, record.producer, record.skill]
      .filter(Boolean)
      .join(" ")
      .toLowerCase()
      .includes(haystack),
  );
}

export function viewerSurface(descriptor: Partial<Pick<ViewerDescriptor, "viewer_kind" | "primary_content_url">> | undefined): "markdown" | "pdf" | "image" | "json" | "table" | "unknown" {
  if (!descriptor || !descriptor.viewer_kind) {
    return "unknown";
  }
  if (descriptor.viewer_kind === "pdf" && descriptor.primary_content_url) {
    return "pdf";
  }
  if (descriptor.viewer_kind === "image" && descriptor.primary_content_url) {
    return "image";
  }
  if (descriptor.viewer_kind === "markdown") {
    return "markdown";
  }
  if (descriptor.viewer_kind === "table") {
    return "table";
  }
  if (descriptor.viewer_kind === "json") {
    return "json";
  }
  return "unknown";
}

export type WorkbenchPanelOptions = {
  id: string;
  component: string;
  title: string;
  params: {
    topicId?: string;
    graphScope?: string;
    recordId?: string;
    ideaId?: string;
    contentUrl?: string | null;
    mediaType?: string | null;
    itemKind?: string;
  };
};

export type DockviewApiLike = {
  addPanel?: (options: WorkbenchPanelOptions) => unknown;
  getPanel?: (id: string) => DockviewPanelLike | undefined;
  removePanel?: (panel: DockviewPanelLike) => void;
  activePanel?: DockviewPanelLike;
  onDidRemovePanel?: (listener: (panel: DockviewPanelLike) => void) => { dispose?: () => void };
};

export type DockviewPanelLike = {
  id: string;
  api?: {
    close?: () => void;
    setActive?: () => void;
  };
};

export type OpenPanelResult = {
  status: "created" | "focused" | "ignored";
  panelId?: string;
};

export function panelOptionsFromDescriptor(descriptor: OpenableItemDescriptor): WorkbenchPanelOptions | null {
  if (!descriptor.ok || !descriptor.tab_id || !descriptor.preferred_tab_component) {
    return null;
  }
  return {
    id: descriptor.tab_id,
    component: descriptor.preferred_tab_component,
    title: descriptor.title || descriptor.openable_item_id,
    params: {
      topicId: descriptor.topic_id || undefined,
      graphScope: descriptor.graph_scope || undefined,
      recordId: descriptor.record_id || undefined,
      ideaId: descriptor.idea_id || undefined,
      contentUrl: descriptor.content_url || undefined,
      mediaType: descriptor.media_type || undefined,
      itemKind: descriptor.item_kind,
    },
  };
}

export function openPanelFromDescriptor(dockApi: DockviewApiLike | null | undefined, descriptor: OpenableItemDescriptor): OpenPanelResult {
  const panel = panelOptionsFromDescriptor(descriptor);
  if (!panel || !dockApi) {
    return { status: "ignored" };
  }
  const existing = dockApi.getPanel?.(panel.id);
  if (existing) {
    existing.api?.setActive?.();
    return { status: "focused", panelId: panel.id };
  }
  dockApi.addPanel?.(panel);
  return { status: "created", panelId: panel.id };
}
