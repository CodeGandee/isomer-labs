import { hotkeysCoreFeature, selectionFeature, syncDataLoaderFeature, type ItemInstance } from "@headless-tree/core";
import { useTree } from "@headless-tree/react";
import { QueryClient, QueryClientProvider, useQuery, useQueryClient } from "@tanstack/react-query";
import { createRootRoute, createRouter, RouterProvider } from "@tanstack/react-router";
import { createColumnHelper, flexRender, getCoreRowModel, getSortedRowModel, useReactTable, type SortingState } from "@tanstack/react-table";
import { themeDark, themeLight } from "dockview";
import { DockviewReact, type DockviewReadyEvent, type IDockviewPanelProps } from "dockview-react";
import { Menu, RefreshCw, Settings } from "lucide-react";
import React, { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  getOpenableItemDescriptor,
  getProject,
  getProjectExplorer,
  getRecordDetail,
  getRecordFacets,
  getRecordFiles,
  getRecordLineage,
  getRecordRender,
  getRecordSiblings,
  getRecords,
  getIdeaDetail,
  getRuntime,
  getActors,
  getTopic,
  getTopicOverview,
  getTopicOverviewJson,
  getTopicGraph,
  getTopics,
  getViewerDescriptor,
} from "./api";
import { topicRelativeDisplayPath } from "./display-path";
import { buildJsonMarkdownPreview } from "./markdown-doc";
import { manualRefresh$, topicInvalidations, workbenchCommands$ } from "./events";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { TooltipProvider } from "@/components/ui/tooltip";
import { LinkButton, StatusBadge, StatusBadgeButton, ToolbarButton } from "@/components/workbench-controls";
import type { Diagnostic, ExplorerNode, GraphScope, IdeaDetailResponse, OpenableItemDescriptor, RecordSummary } from "./types";
import { ThemeProvider, useGuiTheme } from "./theme-provider";
import type { ThemeMode } from "./theme-mode";
import { ToastNotificationsProvider, useToastNotifications } from "./toast-notifications";
import { GuiSettingsProvider, useGuiSettings } from "./ui-settings";
import { filterRecords, openPanelFromDescriptor, viewerSurface, type DockviewApiLike, type OpenPanelResult } from "./view-model";
import { GraphSummary } from "./features/graph/GraphPanels";
import {
  coerceWorkbenchHistoryState,
  isGraphScope,
  readWorkbenchSearch,
  semanticOpenItemForState,
  writeWorkbenchHistory,
  type UrlSyncMode,
  type WorkbenchHistoryMetadata,
  type WorkbenchHistoryState,
  type WorkbenchSearchState,
} from "./workbench-history";
import "dockview/dist/styles/dockview.css";
import "@xyflow/react/dist/style.css";
import "./styles.css";

const LazyIdeaGraphPanel = React.lazy(() => import("./features/idea-lineage/IdeaLineagePanel").then((module) => ({ default: module.IdeaGraphPanel })));
const LazyIdeaTimelinePanel = React.lazy(() => import("./features/idea-timeline/IdeaTimelinePanel").then((module) => ({ default: module.IdeaTimelinePanel })));
const LazyMarkdownView = React.lazy(() => import("./markdown-view").then((module) => ({ default: module.MarkdownView })));

function MarkdownView(props: { content: string; state?: "loading" | "empty" | "ready" }) {
  return (
    <React.Suspense fallback={<div className="markdown-view markdown-view-status markdown-view-loading"><p>Loading Markdown preview.</p></div>}>
      <LazyMarkdownView {...props} />
    </React.Suspense>
  );
}

type PanelParams = {
  topicId?: string;
  graphScope?: string;
  recordId?: string;
  ideaId?: string;
  contentUrl?: string | null;
  mediaType?: string | null;
  itemKind?: string;
};

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5000,
      refetchOnWindowFocus: false,
    },
  },
});

const rootRoute = createRootRoute({
  component: Workbench,
});

const router = createRouter({ routeTree: rootRoute });

declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router;
  }
}

export function RootApp() {
  return (
    <ThemeProvider>
      <GuiSettingsProvider>
        <TooltipProvider>
          <ToastNotificationsProvider>
            <QueryClientProvider client={queryClient}>
              <RouterProvider router={router} />
            </QueryClientProvider>
          </ToastNotificationsProvider>
        </TooltipProvider>
      </GuiSettingsProvider>
    </ThemeProvider>
  );
}

function Workbench() {
  const [urlState, setUrlState] = useUrlState();
  const [dockApi, setDockApi] = useState<unknown>(null);
  const [mobileExplorerOpen, setMobileExplorerOpen] = useState(false);
  const [expandedTopicIds, setExpandedTopicIds] = useState<string[]>([]);
  const [expandedItems, setExpandedItems] = useState<string[]>(["project", "project:topics"]);
  const startupItemRef = useRef<string | null>(null);
  const startupCompleteRef = useRef(false);
  const currentHistoryStateRef = useRef<WorkbenchHistoryState>(
    coerceWorkbenchHistoryState(typeof window !== "undefined" ? window.history.state : null, urlState),
  );
  const navigationIndexRef = useRef(currentHistoryStateRef.current.navigationIndex || 0);
  const panelStateByIdRef = useRef<Map<string, WorkbenchSearchState>>(new Map());
  const suppressPanelCloseUrlRef = useRef(false);
  const queryClientValue = useQueryClient();
  const project = useQuery({ queryKey: ["project"], queryFn: getProject });
  const topics = useQuery({ queryKey: ["topics"], queryFn: getTopics });
  const explorer = useQuery({
    queryKey: ["explorer", "project", expandedTopicIds],
    queryFn: () => getProjectExplorer(expandedTopicIds),
  });
  const topicList = topics.data?.topics || [];
  const selectedTopicId = urlState.topicId || topicList[0]?.id;
  const graphScope = urlState.graphScope;
  const { resolvedThemeMode } = useGuiTheme();
  const dockviewTheme = resolvedThemeMode === "dark" ? themeDark : themeLight;

  const commitUrlState = useCallback(
    (next: WorkbenchSearchState, mode: UrlSyncMode, metadata: WorkbenchHistoryMetadata = {}) => {
      const navigationIndex = mode === "push" ? navigationIndexRef.current + 1 : navigationIndexRef.current;
      const historyState = setUrlState(next, {
        mode,
        metadata: {
          ...metadata,
          navigationIndex,
        },
      });
      if (mode !== "silent") {
        navigationIndexRef.current = navigationIndex;
        currentHistoryStateRef.current = historyState;
      }
      return historyState;
    },
    [setUrlState],
  );

  useEffect(() => {
    if (!urlState.topicId && selectedTopicId) {
      commitUrlState({ topicId: selectedTopicId, graphScope, openItemId: urlState.openItemId }, "replace");
    }
  }, [commitUrlState, graphScope, selectedTopicId, urlState.openItemId, urlState.topicId]);

  useEffect(() => {
    if (!selectedTopicId) {
      return undefined;
    }
    const subscription = topicInvalidations(selectedTopicId).subscribe((event) => {
      queryClientValue.invalidateQueries({ queryKey: ["explorer", "project"] });
      queryClientValue.invalidateQueries({
        predicate: (query) => {
          const key = query.queryKey;
          return Array.isArray(key) && key[0] === "topic" && key[1] === selectedTopicId && intersectsEvent(key, event.graph_scopes || []);
        },
      });
    });
    return () => subscription.unsubscribe();
  }, [queryClientValue, selectedTopicId]);

  const openDescriptor = useCallback(
    (descriptor: OpenableItemDescriptor): OpenPanelResult => openPanelFromDescriptor(dockApi as DockviewApiLike | null, descriptor),
    [dockApi],
  );

  const openItem = useCallback(
    async (
      openableItemId: string,
      options: { historyMode?: UrlSyncMode; syncState?: boolean; sourceState?: WorkbenchSearchState } = {},
    ): Promise<OpenPanelResult> => {
      if (!dockApi) {
        return { status: "ignored" };
      }
      const descriptor = await queryClientValue.fetchQuery({
        queryKey: ["openable", openableItemId],
        queryFn: () => getOpenableItemDescriptor(openableItemId),
      });
      const historyMode = options.historyMode || "push";
      const syncState = options.syncState !== false;
      const representedState = {
        topicId: urlState.topicId || selectedTopicId,
        graphScope,
        openItemId: urlState.openItemId,
      };
      const activePanelId = (dockApi as DockviewApiLike).activePanel?.id;
      if (
        historyMode === "push" &&
        descriptor.ok &&
        descriptor.tab_id &&
        activePanelId === descriptor.tab_id &&
        semanticOpenItemForState(representedState) === descriptor.openable_item_id
      ) {
        return { status: "ignored", panelId: descriptor.tab_id };
      }

      const panelResult = openDescriptor(descriptor);
      if (descriptor.ok) {
        const nextGraphScope = asGraphScope(descriptor.graph_scope, options.sourceState?.graphScope || graphScope);
        const nextState: WorkbenchSearchState = {
          topicId: descriptor.topic_id || options.sourceState?.topicId || selectedTopicId,
          graphScope: nextGraphScope,
          openItemId: descriptor.openable_item_id,
        };
        if (panelResult.panelId) {
          panelStateByIdRef.current.set(panelResult.panelId, nextState);
        }
        if (syncState) {
          commitUrlState(nextState, historyMode, {
            activePanelId: panelResult.panelId,
            openedPanelId: panelResult.status === "created" ? panelResult.panelId : undefined,
            closeOnBack: panelResult.status === "created",
          });
        }
      }
      return panelResult;
    },
    [commitUrlState, dockApi, graphScope, openDescriptor, queryClientValue, selectedTopicId, urlState.openItemId, urlState.topicId],
  );

  useEffect(() => {
    if (!dockApi) {
      return undefined;
    }
    const subscription = workbenchCommands$.subscribe((command) => {
      if (command.type === "open-record") {
        void openItem(`record:${command.topicId}:${command.recordId}`);
      }
      if (command.type === "open-idea") {
        void openItem(`idea:${command.topicId}:${command.ideaId}`).then((result) => command.onOpenResult?.(result));
      }
      if (command.type === "open-file") {
        void openItem(`file:${command.topicId}:${command.recordId}:${command.fileId}`);
      }
      if (command.type === "open-graph") {
        void openItem(`topic:${command.topicId}:graph:${command.graphScope}`);
      }
      if (command.type === "refresh-topic") {
        manualRefresh$.next({ topicId: command.topicId });
      }
    });
    return () => subscription.unsubscribe();
  }, [dockApi, openItem]);

  useEffect(() => {
    if (!dockApi || startupCompleteRef.current) {
      return;
    }
    const startupItem = urlState.openItemId || (selectedTopicId ? `topic:${selectedTopicId}:overview` : undefined);
    if (!startupItem || startupItemRef.current === startupItem) {
      return;
    }
    startupItemRef.current = startupItem;
    startupCompleteRef.current = true;
    void openItem(startupItem, {
      historyMode: urlState.openItemId ? "replace" : "silent",
      syncState: Boolean(urlState.openItemId),
      sourceState: urlState,
    });
  }, [dockApi, openItem, selectedTopicId, urlState]);

  const closeHistoryCreatedPanel = useCallback(
    (poppedAway: WorkbenchHistoryState | undefined, targetPanelId?: string) => {
      const api = dockApi as DockviewApiLike | null;
      if (!api || !poppedAway?.closeOnBack || !poppedAway.openedPanelId || poppedAway.openedPanelId === targetPanelId) {
        return;
      }
      const panel = api.getPanel?.(poppedAway.openedPanelId);
      if (!panel) {
        return;
      }
      suppressPanelCloseUrlRef.current = true;
      if (panel.api?.close) {
        panel.api.close();
      } else {
        api.removePanel?.(panel);
      }
      window.setTimeout(() => {
        suppressPanelCloseUrlRef.current = false;
      }, 0);
    },
    [dockApi],
  );

  useEffect(() => {
    const onPopState = (event: PopStateEvent) => {
      const targetSearch = readWorkbenchSearch(window.location.search);
      const targetHistoryState = coerceWorkbenchHistoryState(event.state, targetSearch);
      const poppedAway = currentHistoryStateRef.current;
      const targetIndex = targetHistoryState.navigationIndex || 0;
      const poppedIndex = poppedAway.navigationIndex || 0;
      const isBack = targetIndex < poppedIndex;
      navigationIndexRef.current = targetIndex;
      currentHistoryStateRef.current = targetHistoryState;
      setUrlState(targetSearch, {
        mode: "silent",
        metadata: {
          activePanelId: targetHistoryState.activePanelId,
          openedPanelId: targetHistoryState.openedPanelId,
          closeOnBack: targetHistoryState.closeOnBack,
          navigationIndex: targetIndex,
        },
      });

      const targetOpenItem = semanticOpenItemForState(targetSearch);
      if (!targetOpenItem || !dockApi) {
        if (isBack) {
          closeHistoryCreatedPanel(poppedAway);
        }
        return;
      }

      void openItem(targetOpenItem, { historyMode: "silent", syncState: false, sourceState: targetSearch }).then((panelResult) => {
        if (isBack) {
          closeHistoryCreatedPanel(poppedAway, panelResult.panelId || targetHistoryState.activePanelId);
        }
      });
    };
    window.addEventListener("popstate", onPopState);
    return () => window.removeEventListener("popstate", onPopState);
  }, [closeHistoryCreatedPanel, dockApi, openItem, setUrlState]);

  useEffect(() => {
    const api = dockApi as DockviewApiLike | null;
    if (!api?.onDidRemovePanel) {
      return undefined;
    }
    const disposable = api.onDidRemovePanel((panel) => {
      const removedState = panelStateByIdRef.current.get(panel.id);
      panelStateByIdRef.current.delete(panel.id);
      if (suppressPanelCloseUrlRef.current) {
        return;
      }
      const current = currentHistoryStateRef.current;
      const removedUrlSelectedPanel = current.activePanelId === panel.id || current.openedPanelId === panel.id || current.openItemId === removedState?.openItemId;
      if (!removedUrlSelectedPanel) {
        return;
      }
      window.setTimeout(() => {
        const activePanelId = api.activePanel?.id;
        const fallbackState = (activePanelId && panelStateByIdRef.current.get(activePanelId)) || {
          topicId: current.topicId || selectedTopicId,
          graphScope: current.graphScope || graphScope,
        };
        commitUrlState(fallbackState, "replace", {
          activePanelId,
          closeOnBack: false,
        });
      }, 0);
    });
    return () => disposable.dispose?.();
  }, [commitUrlState, dockApi, graphScope, selectedTopicId]);

  const onDockReady = useCallback(
    (event: DockviewReadyEvent) => {
      setDockApi(event.api);
    },
    [],
  );

  const onExpandTopic = useCallback((topicId: string) => {
    setExpandedTopicIds((current) => (current.includes(topicId) ? current : [...current, topicId].sort()));
  }, []);

  const renderExplorer = useCallback(
    (options: { onOpenItem?: () => void } = {}) => (
      <>
        <header className="brand-row">
          <h1>Isomer</h1>
          <span>{project.data?.ok ? "ready" : "loading"}</span>
        </header>
        <div className="project-root">{String(project.data?.project?.root || "")}</div>
        <ExplorerPane
          key={explorer.data?.revision || "loading"}
          nodes={explorer.data?.nodes || []}
          rootNodeId={explorer.data?.root_node_ids[0] || "project"}
          expandedItems={expandedItems}
          selectedTopicId={selectedTopicId}
          onExpandedItemsChange={setExpandedItems}
          onExpandTopic={onExpandTopic}
          onOpenItem={(openableItemId) => {
            options.onOpenItem?.();
            void openItem(openableItemId);
          }}
        />
      </>
    ),
    [expandedItems, explorer.data?.nodes, explorer.data?.revision, explorer.data?.root_node_ids, onExpandTopic, openItem, project.data?.ok, project.data?.project?.root, selectedTopicId],
  );

  return (
    <div className="research-shell">
      <aside className="sidebar explorer-sidebar">
        {renderExplorer()}
      </aside>
      <main className="workbench">
        <div className="topbar">
          <div className="topbar-heading-group">
            <ToolbarButton className="mobile-explorer-trigger" type="button" onClick={() => setMobileExplorerOpen(true)}>
              <Menu aria-hidden="true" />
              Project
            </ToolbarButton>
            <div className="topic-heading">
              <span>Research Topic</span>
              <h2>{selectedTopicId || "Select a topic"}</h2>
            </div>
          </div>
          <div className="toolbar">
            <ToolbarButton type="button" onClick={() => void openItem("project:settings")}>
              <Settings aria-hidden="true" />
              Settings
            </ToolbarButton>
            <ToolbarButton type="button" onClick={() => selectedTopicId && manualRefresh$.next({ topicId: selectedTopicId })}>
              <RefreshCw aria-hidden="true" />
              Refresh
            </ToolbarButton>
          </div>
        </div>
        <div className={`dock-host dockview-theme-${resolvedThemeMode}`}>
          <DockviewReact components={dockComponents} onReady={onDockReady} theme={dockviewTheme} />
        </div>
      </main>
      <Dialog open={mobileExplorerOpen} onOpenChange={setMobileExplorerOpen}>
        <DialogContent className="mobile-explorer-sheet" showCloseButton={false}>
          <DialogHeader className="sr-only">
            <DialogTitle>Project Explorer</DialogTitle>
            <DialogDescription>Navigate Project topics and views.</DialogDescription>
          </DialogHeader>
          <aside className="sidebar explorer-sidebar mobile-explorer-sidebar">
            {renderExplorer({ onOpenItem: () => setMobileExplorerOpen(false) })}
          </aside>
        </DialogContent>
      </Dialog>
    </div>
  );
}

export function ExplorerPane({
  nodes,
  rootNodeId,
  expandedItems,
  selectedTopicId,
  onExpandedItemsChange,
  onExpandTopic,
  onOpenItem,
}: {
  nodes: ExplorerNode[];
  rootNodeId: string;
  expandedItems: string[];
  selectedTopicId?: string;
  onExpandedItemsChange: (items: string[] | ((old: string[]) => string[])) => void;
  onExpandTopic: (topicId: string) => void;
  onOpenItem: (openableItemId: string) => void;
}) {
  const nodeMap = useMemo(() => new Map(nodes.map((node) => [node.id, node])), [nodes]);
  const childrenByParent = useMemo(() => {
    const children = new Map<string, string[]>();
    for (const node of nodes) {
      if (!node.parent_id) {
        continue;
      }
      const existing = children.get(node.parent_id) || [];
      existing.push(node.id);
      children.set(node.parent_id, existing);
    }
    return children;
  }, [nodes]);
  const tree = useTree<ExplorerNode>({
    state: { expandedItems },
    setExpandedItems: onExpandedItemsChange,
    rootItemId: rootNodeId,
    getItemName: (item) => item.getItemData().label,
    isItemFolder: (item) => Boolean(item.getItemData().has_children),
    dataLoader: {
      getItem: (itemId) =>
        nodeMap.get(itemId) || {
          id: itemId,
          label: itemId,
          item_kind: "unknown",
        },
      getChildren: (itemId) => childrenByParent.get(itemId) || [],
    },
    indent: 16,
    features: [syncDataLoaderFeature, selectionFeature, hotkeysCoreFeature],
  });

  if (!nodes.length) {
    return <div className="explorer-empty">Loading Project Explorer.</div>;
  }

  return (
    <div {...tree.getContainerProps("Project Explorer")} className="explorer-tree">
      {tree.getItems().map((item) => (
        <ExplorerRow
          item={item}
          key={item.getId()}
          selectedTopicId={selectedTopicId}
          expandedItems={expandedItems}
          onExpandedItemsChange={onExpandedItemsChange}
          onExpandTopic={onExpandTopic}
          onOpenItem={onOpenItem}
        />
      ))}
    </div>
  );
}

function ExplorerRow({
  item,
  selectedTopicId,
  expandedItems,
  onExpandedItemsChange,
  onExpandTopic,
  onOpenItem,
}: {
  item: ItemInstance<ExplorerNode>;
  selectedTopicId?: string;
  expandedItems: string[];
  onExpandedItemsChange: (items: string[] | ((old: string[]) => string[])) => void;
  onExpandTopic: (topicId: string) => void;
  onOpenItem: (openableItemId: string) => void;
}) {
  const data = item.getItemData();
  const props = item.getProps();
  const isSelectedTopic = data.item_kind === "research_topic" && data.topic_id === selectedTopicId;
  const onClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    const wasExpanded = item.isExpanded();
    props.onClick?.(event);
    if (item.isFolder()) {
      const next = new Set(expandedItems);
      if (wasExpanded) {
        next.delete(item.getId());
      } else {
        next.add(item.getId());
        if (data.item_kind === "research_topic" && data.topic_id && !data.children_loaded) {
          next.add(`topic:${data.topic_id}:graphs`);
          onExpandTopic(data.topic_id);
        }
      }
      onExpandedItemsChange([...next]);
    }
    if (data.openable_item_id) {
      onOpenItem(data.openable_item_id);
    }
  };
  return (
    <Button
      {...props}
      className={`explorer-row ${item.isFolder() ? "folder" : "leaf"} ${item.isExpanded() ? "expanded" : ""} ${item.isFocused() ? "focused" : ""} ${isSelectedTopic ? "active-topic" : ""}`}
      data-testid={`explorer-row-${item.getId()}`}
      onClick={onClick}
      size="sm"
      style={{ paddingLeft: `${8 + item.getItemMeta().level * 14}px` }}
      type="button"
      variant="ghost"
    >
      <span className="explorer-twist">{item.isFolder() ? (item.isExpanded() ? "v" : ">") : ""}</span>
      <span className={`explorer-icon ${data.icon_hint || "item"}`} />
      <span className="explorer-label">{data.label}</span>
      {data.badge_text ? (
        <Badge className="explorer-badge" variant="outline">
          {data.badge_text}
        </Badge>
      ) : null}
      {data.diagnostics_count ? (
        <Badge className="explorer-warning" variant="outline">
          {data.diagnostics_count}
        </Badge>
      ) : null}
    </Button>
  );
}

const dockComponents = {
  ideaGraph: (props: IDockviewPanelProps<PanelParams>) => (
    <React.Suspense fallback={<div className="panel-body empty-state">Loading graph viewer.</div>}>
      <LazyIdeaGraphPanel {...props.params} panelId={props.api.id} openableItemId={props.params.topicId ? `topic:${props.params.topicId}:graph:${props.params.graphScope || "idea-lineage"}` : undefined} />
    </React.Suspense>
  ),
  ideaTimeline: (props: IDockviewPanelProps<PanelParams>) => (
    <React.Suspense fallback={<div className="panel-body empty-state">Loading timeline.</div>}>
      <LazyIdeaTimelinePanel topicId={props.params.topicId || ""} />
    </React.Suspense>
  ),
  records: (props: IDockviewPanelProps<PanelParams>) => <RecordsPanel topicId={props.params.topicId || ""} />,
  recordDetail: (props: IDockviewPanelProps<PanelParams>) => <RecordDetailPanel topicId={props.params.topicId || ""} recordId={props.params.recordId || ""} />,
  ideaDetail: (props: IDockviewPanelProps<PanelParams>) => <IdeaDetailPanel topicId={props.params.topicId || ""} ideaId={props.params.ideaId || ""} />,
  diagnostics: (props: IDockviewPanelProps<PanelParams>) => <DiagnosticsPanel topicId={props.params.topicId} graphScope={asGraphScope(props.params.graphScope, "idea-lineage")} />,
  settings: () => <ProjectSettingsPanel />,
  projectOverview: () => <ProjectOverviewPanel />,
  topicOverview: (props: IDockviewPanelProps<PanelParams>) => <TopicOverviewPanel topicId={props.params.topicId || ""} />,
  runtime: (props: IDockviewPanelProps<PanelParams>) => <RuntimePanel topicId={props.params.topicId || ""} />,
  actors: (props: IDockviewPanelProps<PanelParams>) => <ActorsPanel topicId={props.params.topicId || ""} />,
  repository: (props: IDockviewPanelProps<PanelParams>) => <RepositoryPanel topicId={props.params.topicId || ""} />,
  fileArtifact: (props: IDockviewPanelProps<PanelParams>) => <FileArtifactPanel contentUrl={props.params.contentUrl || ""} mediaType={props.params.mediaType || ""} />,
};

export function ProjectSettingsPanel() {
  const { resolvedThemeMode, setThemeMode, themeMode } = useGuiTheme();
  const {
    hoverPreviewDelayMs,
    ideaTimelinePrimaryColor,
    ideaTimelineRowColorsEnabled,
    ideaTimelineSupportingColor,
    refreshGuiSettings,
    setHoverPreviewDelayMs,
    setIdeaTimelinePrimaryColor,
    setIdeaTimelineRowColorsEnabled,
    setIdeaTimelineSupportingColor,
  } = useGuiSettings();
  const [hoverPreviewDelaySeconds, setHoverPreviewDelaySeconds] = useState(() => formatDelaySeconds(hoverPreviewDelayMs));
  const onThemeChange = useCallback((value: string) => {
    setThemeMode(value as ThemeMode);
  }, [setThemeMode]);
  const onHoverPreviewDelayChange = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const nextValue = event.target.value;
    setHoverPreviewDelaySeconds(nextValue);
    if (!nextValue.trim()) {
      return;
    }
    const parsedSeconds = Number(nextValue);
    if (Number.isFinite(parsedSeconds)) {
      setHoverPreviewDelayMs(parsedSeconds * 1000);
    }
  }, [setHoverPreviewDelayMs]);

  useEffect(() => {
    setHoverPreviewDelaySeconds(formatDelaySeconds(hoverPreviewDelayMs));
  }, [hoverPreviewDelayMs]);

  useEffect(() => {
    refreshGuiSettings();
  }, [refreshGuiSettings]);

  return (
    <section className="panel-body settings-panel">
      <div className="detail-heading">
        <div>
          <h3>Project Settings</h3>
          <span>Frontend preferences and future service settings</span>
        </div>
      </div>
      <div className="settings-sections">
        <section className="settings-section">
          <div className="settings-copy">
            <h4>Appearance</h4>
            <p>Choose the theme used across the workbench. This preference is stored in this browser.</p>
          </div>
          <label className="settings-field">
            <span>Global Theme</span>
            <Select value={themeMode} onValueChange={onThemeChange}>
              <SelectTrigger aria-label="Global Theme" className="settings-select">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="system">System</SelectItem>
                <SelectItem value="light">Light</SelectItem>
                <SelectItem value="dark">Dark</SelectItem>
              </SelectContent>
            </Select>
          </label>
          <p className="settings-note">Resolved theme: {resolvedThemeMode}</p>
        </section>
        <section className="settings-section muted-section">
          <div className="settings-copy">
            <h4>Idea Graph</h4>
            <p>Tune graph inspection behavior for this browser.</p>
          </div>
          <label className="settings-field">
            <span>Hover Popup Delay</span>
            <Input
              aria-label="Hover Popup Delay"
              className="settings-number-input"
              type="number"
              min={0.25}
              max={5}
              step={0.25}
              value={hoverPreviewDelaySeconds}
              onChange={onHoverPreviewDelayChange}
            />
          </label>
          <p className="settings-note">Current delay: {formatDelaySeconds(hoverPreviewDelayMs)}s</p>
        </section>
        <section className="settings-section muted-section">
          <div className="settings-copy">
            <h4>Idea Timeline</h4>
            <p>Choose row colors used by the idea timeline table in this browser.</p>
          </div>
          <label className="settings-field checkbox-setting">
            <Checkbox aria-label="Color Idea Timeline Rows" checked={ideaTimelineRowColorsEnabled} onCheckedChange={(checked) => setIdeaTimelineRowColorsEnabled(checked === true)} />
            <span>Color Idea Timeline Rows</span>
          </label>
          <div className="settings-color-grid">
            <label className="settings-field">
              <span>Primary Row</span>
              <Input aria-label="Primary Idea Row Color" className="settings-color-input" type="color" value={ideaTimelinePrimaryColor} onChange={(event) => setIdeaTimelinePrimaryColor(event.target.value)} />
            </label>
            <label className="settings-field">
              <span>Supporting Row</span>
              <Input aria-label="Supporting Idea Row Color" className="settings-color-input" type="color" value={ideaTimelineSupportingColor} onChange={(event) => setIdeaTimelineSupportingColor(event.target.value)} />
            </label>
          </div>
        </section>
      </div>
    </section>
  );
}

function formatDelaySeconds(delayMs: number) {
  return Number((delayMs / 1000).toFixed(2)).toString();
}

function ProjectOverviewPanel() {
  const project = useQuery({ queryKey: ["project"], queryFn: getProject });
  return (
    <section className="panel-body overview-panel">
      <div className="detail-heading">
        <h3>Project Overview</h3>
        <span>{project.data?.ok ? "ready" : "loading"}</span>
      </div>
      <JsonBlock title="Project" value={project.data} />
    </section>
  );
}

export function TopicOverviewPanel({ topicId }: { topicId: string }) {
  const viewJsonButtonRef = useRef<HTMLButtonElement | null>(null);
  const [jsonModalOpen, setJsonModalOpen] = useState(false);
  const { notify } = useToastNotifications();
  const overview = useQuery({
    queryKey: ["topic", topicId, "overview"],
    queryFn: () => getTopicOverview(topicId),
    enabled: Boolean(topicId),
  });
  const overviewJson = useQuery({
    queryKey: ["topic", topicId, "overview", "json"],
    queryFn: () => getTopicOverviewJson(topicId),
    enabled: Boolean(topicId) && jsonModalOpen,
  });
  const markdown = overview.data?.overview?.content_markdown || "";
  const diagnostics = useMemo(
    () => [...(overview.data?.diagnostics || []), ...(overviewJson.data?.diagnostics || [])],
    [overview.data?.diagnostics, overviewJson.data?.diagnostics],
  );
  const sourceMetadata = useMemo(() => overviewSourceMetadata(overview.data?.overview), [overview.data?.overview]);
  const jsonTabs = useMemo<JsonModalTab[]>(() => {
    const topicJson = overviewJson.isError
      ? { error: String(overviewJson.error) }
      : overviewJson.isPending || overviewJson.isFetching
        ? { loading: true }
        : overviewJson.data?.topic_payload || {};
    const runtimeJson = overviewJson.isError
      ? { error: String(overviewJson.error) }
      : overviewJson.isPending || overviewJson.isFetching
        ? { loading: true }
        : overviewJson.data?.runtime_payload || {};
    const tabs: JsonModalTab[] = [
      { id: "topic", label: "Topic", jsonText: buildJsonMarkdownPreview(topicJson).jsonText },
      { id: "runtime", label: "Runtime", jsonText: buildJsonMarkdownPreview(runtimeJson).jsonText },
    ];
    if (diagnostics.length > 0) {
      tabs.push({ id: "diagnostics", label: "Diagnostics", jsonText: buildJsonMarkdownPreview(diagnostics).jsonText });
    } else {
      tabs.push({ id: "source", label: "Source", jsonText: buildJsonMarkdownPreview(sourceMetadata || {}).jsonText });
    }
    return tabs;
  }, [diagnostics, overviewJson.data?.runtime_payload, overviewJson.data?.topic_payload, overviewJson.error, overviewJson.isError, overviewJson.isFetching, overviewJson.isPending, sourceMetadata]);

  const copyText = useCallback(async (target: "json" | "markdown", textValue: string | null | undefined) => {
    if (!textValue) {
      notify({ title: target === "markdown" ? "No Markdown available." : "Nothing to copy.", tone: "error" });
      return;
    }
    try {
      await navigator.clipboard.writeText(textValue);
      notify({ title: target === "json" ? "JSON copied." : "Markdown copied.", tone: "success" });
    } catch {
      notify({ title: "Clipboard write failed.", description: "Content remains selectable.", tone: "error" });
    }
  }, [notify]);

  const closeJsonModal = useCallback(() => {
    setJsonModalOpen(false);
    window.requestAnimationFrame(() => viewJsonButtonRef.current?.focus());
  }, []);

  const markdownState: "loading" | "empty" | "ready" = overview.isPending || overview.isFetching ? "loading" : markdown ? "ready" : "empty";
  const markdownContent = overview.isPending
    ? "Loading topic overview."
    : markdown || missingOverviewMarkdown(overview.data?.overview?.semantic_label || "topic.intent.overview", diagnostics);
  const overviewExists = overview.data?.overview?.exists === true;
  const overviewMissing = overview.data?.overview?.exists === false;
  const overviewPath = topicRelativeDisplayPath(overview.data?.overview?.path, { topicId });

  return (
    <section className="panel-body overview-panel idea-detail-panel">
      <div className="detail-heading">
        <div>
          <h3>{topicId || "Topic Overview"}</h3>
          <span>{overview.data?.overview?.semantic_label || "topic.intent.overview"}</span>
        </div>
        <div className="toolbar idea-toolbar">
          <ToolbarButton
            ref={viewJsonButtonRef}
            type="button"
            disabled={!overview.data}
            onClick={() => setJsonModalOpen(true)}
          >
            View JSON
          </ToolbarButton>
          <ToolbarButton type="button" disabled={!markdown} onClick={() => void copyText("markdown", markdown)}>
            Copy Markdown
          </ToolbarButton>
          <ToolbarButton type="button" onClick={() => void overview.refetch()}>
            <RefreshCw aria-hidden="true" />
            Refresh
          </ToolbarButton>
        </div>
      </div>
      <div className="idea-status-row">
        <StatusBadge tone={overviewExists ? "success" : overviewMissing ? "warning" : "muted"}>
          {overviewExists ? "overview ready" : overviewMissing ? "topic.intent.overview missing" : "loading overview"}
        </StatusBadge>
        {overviewPath ? <StatusBadge>{overviewPath}</StatusBadge> : null}
        {overview.data?.overview?.content_bytes !== undefined ? <StatusBadge>{overview.data.overview.content_bytes} bytes</StatusBadge> : null}
      </div>
      {diagnostics.length > 0 ? <OverviewDiagnostics diagnostics={diagnostics} /> : null}
      <MarkdownView content={markdownContent} state={markdownState} />
      {jsonModalOpen ? (
        <JsonModal
          title={`${topicId || "Topic"} Overview Data`}
          description="JSON data for the topic overview."
          tabs={jsonTabs}
          defaultTabId="topic"
          onClose={closeJsonModal}
          onCopy={(jsonText) => void copyText("json", jsonText)}
        />
      ) : null}
    </section>
  );
}

function overviewSourceMetadata(overview: Record<string, unknown> | null | undefined) {
  if (!overview) {
    return null;
  }
  const { content_markdown: _contentMarkdown, ...metadata } = overview;
  return {
    ...metadata,
    content_markdown: overview.content_markdown ? "[available in Markdown preview]" : null,
  };
}

function missingOverviewMarkdown(label: string, diagnostics: Diagnostic[]) {
  const message = diagnostics.find((diagnostic) => diagnostic.code === "topic_overview_missing")?.message || "Topic overview Markdown is unavailable.";
  return `> ${message}\n\nCreate or restore \`${label}\` to show the topic overview here.`;
}

function OverviewDiagnostics({ diagnostics }: { diagnostics: Diagnostic[] }) {
  return (
    <div className="diagnostics-list overview-diagnostics">
      {diagnostics.map((diagnostic, index) => (
        <div className={`diagnostic ${diagnostic.severity || "info"}`} key={`${diagnostic.code}-${index}`}>
          <strong>{diagnostic.code || "diagnostic"}</strong>
          <span>{diagnostic.message || ""}</span>
        </div>
      ))}
    </div>
  );
}

function RuntimePanel({ topicId }: { topicId: string }) {
  const runtime = useQuery({ queryKey: ["topic", topicId, "runtime"], queryFn: () => getRuntime(topicId), enabled: Boolean(topicId) });
  return (
    <section className="panel-body overview-panel">
      <div className="detail-heading">
        <h3>Workspace Runtime</h3>
        <span>{topicId}</span>
      </div>
      <JsonBlock title="Runtime" value={runtime.data} />
    </section>
  );
}

function ActorsPanel({ topicId }: { topicId: string }) {
  const actors = useQuery({ queryKey: ["topic", topicId, "actors"], queryFn: () => getActors(topicId), enabled: Boolean(topicId) });
  return (
    <section className="panel-body overview-panel">
      <div className="detail-heading">
        <h3>Topic Actors</h3>
        <span>{topicId}</span>
      </div>
      <JsonBlock title="Actors" value={actors.data} />
    </section>
  );
}

function RepositoryPanel({ topicId }: { topicId: string }) {
  const topic = useQuery({ queryKey: ["topic", topicId, "repository"], queryFn: () => getTopic(topicId), enabled: Boolean(topicId) });
  return (
    <section className="panel-body overview-panel">
      <div className="detail-heading">
        <h3>Repositories</h3>
        <span>{topicId}</span>
      </div>
      <JsonBlock title="Repository Context" value={topic.data} />
    </section>
  );
}

function FileArtifactPanel({ contentUrl, mediaType }: { contentUrl: string; mediaType: string }) {
  const content = useQuery({
    queryKey: ["file-artifact", contentUrl],
    queryFn: async () => {
      const response = await fetch(contentUrl);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      return response.text();
    },
    enabled: Boolean(contentUrl) && !mediaType.startsWith("image/") && mediaType !== "application/pdf",
  });
  if (!contentUrl) {
    return <div className="empty-state">No file content URL.</div>;
  }
  if (mediaType === "application/pdf") {
    return <iframe className="pdf-frame" title="File artifact" src={contentUrl} />;
  }
  if (mediaType.startsWith("image/")) {
    return <img className="image-viewer" alt="" src={contentUrl} />;
  }
  return <JsonBlock title={mediaType || "File"} value={content.data || "Loading file."} />;
}

function RecordsPanel({ topicId }: { topicId: string }) {
  const [search, setSearch] = useState("");
  const [facet, setFacet] = useState("");
  const [recordLimit, setRecordLimit] = useState(100);
  const records = useQuery({
    queryKey: ["topic", topicId, "records", facet, recordLimit],
    queryFn: () => getRecords(topicId, { facet: facet || undefined, limit: recordLimit }),
    enabled: Boolean(topicId),
  });
  const filteredRecords = useMemo(() => filterRecords(records.data?.records || [], search), [records.data?.records, search]);
  const table = useRecordsTable(filteredRecords, topicId);
  const facetValue = facet || "all";
  return (
    <section className="panel-body">
      <div className="filters">
        <Input aria-label="Search records" placeholder="search records" value={search} onChange={(event) => setSearch(event.target.value)} />
        <Select value={facetValue} onValueChange={(value) => setFacet(value === "all" ? "" : value)}>
          <SelectTrigger aria-label="Facet" className="facet-select">
            <SelectValue placeholder="all facets" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">all facets</SelectItem>
            <SelectItem value="ideas">ideas</SelectItem>
            <SelectItem value="routes">routes</SelectItem>
            <SelectItem value="metrics">metrics</SelectItem>
            <SelectItem value="claims">claims</SelectItem>
            <SelectItem value="facts">facts</SelectItem>
          </SelectContent>
        </Select>
        <Select value={String(recordLimit)} onValueChange={(value) => setRecordLimit(Number(value))}>
          <SelectTrigger aria-label="Records shown" className="facet-select">
            <SelectValue placeholder="records" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="50">50 rows</SelectItem>
            <SelectItem value="100">100 rows</SelectItem>
            <SelectItem value="250">250 rows</SelectItem>
            <SelectItem value="500">500 rows</SelectItem>
          </SelectContent>
        </Select>
        <StatusBadge>{records.data?.returned_count ?? filteredRecords.length} shown</StatusBadge>
      </div>
      <div className="table-wrap">
        <Table>
          <TableHeader>
            {table.getHeaderGroups().map((group) => (
              <TableRow key={group.id}>
                {group.headers.map((header) => (
                  <TableHead key={header.id}>
                    {header.column.getCanSort() ? (
                      <button className="table-sort-button" type="button" onClick={header.column.getToggleSortingHandler()}>
                        {flexRender(header.column.columnDef.header, header.getContext())}
                        <span aria-hidden="true">{header.column.getIsSorted() === "asc" ? " ^" : header.column.getIsSorted() === "desc" ? " v" : ""}</span>
                      </button>
                    ) : (
                      flexRender(header.column.columnDef.header, header.getContext())
                    )}
                  </TableHead>
                ))}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows.map((row) => (
              <TableRow key={row.id} onClick={() => workbenchCommands$.next({ type: "open-record", topicId, recordId: row.original.record_id })}>
                {row.getVisibleCells().map((cell) => (
                  <TableCell key={cell.id}>{flexRender(cell.column.columnDef.cell, cell.getContext())}</TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </section>
  );
}

export function IdeaDetailPanel({ topicId, ideaId }: { topicId: string; ideaId: string }) {
  const viewJsonButtonRef = useRef<HTMLButtonElement | null>(null);
  const previousDigestRef = useRef<string | undefined>(undefined);
  const [jsonModalOpen, setJsonModalOpen] = useState(false);
  const { notify } = useToastNotifications();
  const [digestNotice, setDigestNotice] = useState("");
  const detail = useQuery({
    queryKey: ["topic", topicId, "idea-lineage", "idea", ideaId, "detail", false],
    queryFn: () => getIdeaDetail(topicId, ideaId),
    enabled: Boolean(topicId && ideaId),
  });
  const fullDetail = useQuery({
    queryKey: ["topic", topicId, "idea-lineage", "idea", ideaId, "detail", true],
    queryFn: () => getIdeaDetail(topicId, ideaId, { includeSourceJson: true }),
    enabled: Boolean(jsonModalOpen && detail.data?.source?.source_json_truncated),
  });
  const activeDetail = fullDetail.data || detail.data;
  const title = String(detail.data?.idea?.title || ideaId || "Idea Detail");
  const ideaContent = detail.data?.idea_content ?? detail.data?.source?.source_json;
  const sourceTruncated = Boolean(detail.data?.source?.source_json_truncated);
  const previewSource = ideaContent === undefined && detail.data?.idea ? { idea: detail.data.idea, latest_realization: detail.data.latest_realization } : ideaContent;
  const preview = useMemo(() => (previewSource === undefined ? null : buildJsonMarkdownPreview(previewSource, { title })), [previewSource, title]);
  const exactJsonText = useMemo(() => (ideaContent === undefined ? null : buildJsonMarkdownPreview(ideaContent).jsonText), [ideaContent]);
  const modalSourceJson = activeDetail?.idea_content ?? activeDetail?.source?.source_json;
  const modalJsonText = useMemo(() => (modalSourceJson === undefined ? null : buildJsonMarkdownPreview(modalSourceJson).jsonText), [modalSourceJson]);
  const diagnostics = useMemo(() => [...(detail.data?.diagnostics || []), ...(fullDetail.data?.diagnostics || [])], [detail.data?.diagnostics, fullDetail.data?.diagnostics]);
  const lineageJsonText = useMemo(
    () =>
      buildJsonMarkdownPreview({
        incoming_edges: detail.data?.incoming_edges || [],
        outgoing_edges: detail.data?.outgoing_edges || [],
        generation_groups: detail.data?.generation_groups || [],
      }).jsonText,
    [detail.data?.generation_groups, detail.data?.incoming_edges, detail.data?.outgoing_edges],
  );
  const realizationsJsonText = useMemo(() => buildJsonMarkdownPreview(detail.data?.realizations || []).jsonText, [detail.data?.realizations]);
  const diagnosticsJsonText = useMemo(() => buildJsonMarkdownPreview(diagnostics).jsonText, [diagnostics]);
  const jsonTabs = useMemo<JsonModalTab[]>(
    () => [
      {
        id: "main-record",
        label: "Main Record",
        jsonText: modalJsonText || exactJsonText || "",
        loading: Boolean(sourceTruncated && fullDetail.isFetching && !modalJsonText),
      },
      { id: "lineage", label: "Lineage", jsonText: lineageJsonText },
      { id: "realizations", label: "Realizations", jsonText: realizationsJsonText },
      { id: "diagnostics", label: "Diagnostics", jsonText: diagnosticsJsonText },
    ],
    [diagnosticsJsonText, exactJsonText, fullDetail.isFetching, lineageJsonText, modalJsonText, realizationsJsonText, sourceTruncated],
  );
  const provenance = detail.data?.source_provenance || detail.data?.source;
  const sourceRecordId = String(provenance?.source_record_id || detail.data?.latest_realization?.record_id || detail.data?.source?.source_record_id || "");
  const sourceDigest = detail.data?.source ? detail.data.source.payload_digest || `${detail.data.source.source_kind}:${detail.data.source.source_json_bytes || 0}` : undefined;

  useEffect(() => {
    if (!sourceDigest) {
      return;
    }
    if (previousDigestRef.current && previousDigestRef.current !== sourceDigest) {
      setDigestNotice("Source payload changed. Refresh if you want to compare the new preview.");
    }
    previousDigestRef.current = sourceDigest;
  }, [sourceDigest]);

  const copyText = useCallback(async (target: "json" | "markdown", textValue: string | null | undefined) => {
    if (!textValue) {
      notify({ title: "Nothing to copy.", tone: "error" });
      return;
    }
    try {
      await navigator.clipboard.writeText(textValue);
      notify({ title: target === "json" ? "JSON copied." : "Markdown copied.", tone: "success" });
    } catch {
      notify({ title: "Clipboard write failed.", description: "Content remains selectable.", tone: "error" });
    }
  }, [notify]);

  const closeJsonModal = useCallback(() => {
    setJsonModalOpen(false);
    window.requestAnimationFrame(() => viewJsonButtonRef.current?.focus());
  }, []);

  if (!ideaId) {
    return <div className="empty-state">No idea selected.</div>;
  }
  if (detail.isPending) {
    return <div className="empty-state">Loading idea.</div>;
  }

  return (
    <section className="panel-body idea-detail-panel">
      <div className="detail-heading">
        <div>
          <h3>{title}</h3>
          <span>{detail.data?.idea?.status ? String(detail.data.idea.status) : ideaId}</span>
        </div>
        <div className="toolbar idea-toolbar">
          <ToolbarButton
            ref={viewJsonButtonRef}
            type="button"
            disabled={!detail.data?.source?.source_json_available}
            onClick={() => setJsonModalOpen(true)}
          >
            View JSON
          </ToolbarButton>
          <ToolbarButton type="button" disabled={!preview?.markdown} onClick={() => void copyText("markdown", preview?.markdown)}>
            Copy Markdown
          </ToolbarButton>
          <ToolbarButton type="button" onClick={() => void detail.refetch()}>
            <RefreshCw aria-hidden="true" />
            Refresh
          </ToolbarButton>
        </div>
      </div>
      <div className="idea-status-row">
        {sourceTruncated ? <StatusBadge tone="warning">source JSON over default cap</StatusBadge> : null}
        {digestNotice ? <StatusBadge tone="info">{digestNotice}</StatusBadge> : null}
        <LinkButton
          type="button"
          className="source-record-button"
          disabled={!sourceRecordId}
          onClick={() => workbenchCommands$.next({ type: "open-record", topicId, recordId: sourceRecordId })}
        >
          Open Source Record
        </LinkButton>
      </div>
      {detail.data?.error ? (
        <div className="diagnostic error">
          <strong>{detail.data.error.code}</strong>
          <span>{detail.data.error.message}</span>
        </div>
      ) : null}
      {preview?.markdown ? (
        <MarkdownView content={preview.markdown} />
      ) : (
        <MarkdownView content="No source JSON is available for this idea." state="empty" />
      )}
      {jsonModalOpen ? (
        <JsonModal
          title={`${title} Data`}
          description="JSON data for the selected idea."
          tabs={jsonTabs}
          defaultTabId="main-record"
          onClose={closeJsonModal}
          onCopy={(jsonText) => void copyText("json", jsonText)}
        />
      ) : null}
    </section>
  );
}

export function RecordDetailPanel({ topicId, recordId }: { topicId: string; recordId: string }) {
  const viewJsonButtonRef = useRef<HTMLButtonElement | null>(null);
  const [jsonModalOpen, setJsonModalOpen] = useState(false);
  const { notify } = useToastNotifications();
  const descriptor = useQuery({
    queryKey: ["topic", topicId, "record", recordId, "descriptor"],
    queryFn: () => getViewerDescriptor(topicId, recordId),
    enabled: Boolean(topicId && recordId),
  });
  const detail = useQuery({
    queryKey: ["topic", topicId, "record", recordId, "detail", Boolean(jsonModalOpen || descriptor.data?.viewer_kind === "json")],
    queryFn: () => getRecordDetail(topicId, recordId, Boolean(jsonModalOpen || descriptor.data?.viewer_kind === "json")),
    enabled: Boolean(descriptor.data?.ok),
  });
  const rendered = useQuery({
    queryKey: ["topic", topicId, "record", recordId, "render", "markdown"],
    queryFn: () => getRecordRender(topicId, recordId),
    enabled: descriptor.data?.viewer_kind === "markdown",
  });
  const lineage = useQuery({ queryKey: ["topic", topicId, "record", recordId, "lineage"], queryFn: () => getRecordLineage(topicId, recordId), enabled: Boolean(descriptor.data?.ok) });
  const siblings = useQuery({ queryKey: ["topic", topicId, "record", recordId, "siblings"], queryFn: () => getRecordSiblings(topicId, recordId), enabled: Boolean(descriptor.data?.ok) });
  const files = useQuery({ queryKey: ["topic", topicId, "record", recordId, "files"], queryFn: () => getRecordFiles(topicId, recordId), enabled: Boolean(descriptor.data?.ok) });
  const facets = useQuery({ queryKey: ["topic", topicId, "record", recordId, "facets"], queryFn: () => getRecordFacets(topicId, recordId), enabled: Boolean(descriptor.data?.ok) });
  const title = descriptor.data?.title || String(detail.data?.record?.title || recordId);
  const surface = descriptor.data ? viewerSurface(descriptor.data) : "unknown";
  const markdownContent = String(rendered.data?.render?.content || "");
  const relativePath = descriptor.data?.topic_workspace_relative_path || detail.data?.topic_workspace_relative_path || rendered.data?.topic_workspace_relative_path || "";
  const absoluteFilepath = descriptor.data?.absolute_filepath || detail.data?.absolute_filepath || rendered.data?.absolute_filepath || "";
  const parentIdea = descriptor.data?.direct_parent_idea || detail.data?.direct_parent_idea || rendered.data?.direct_parent_idea;
  const diagnostics = useMemo(
    () => [
      ...(descriptor.data?.diagnostics || []),
      ...(detail.data?.diagnostics || []),
      ...(rendered.data?.diagnostics || []),
      ...(((lineage.data as { diagnostics?: unknown[] } | undefined)?.diagnostics as []) || []),
      ...(((siblings.data as { diagnostics?: unknown[] } | undefined)?.diagnostics as []) || []),
      ...(((files.data as { diagnostics?: unknown[] } | undefined)?.diagnostics as []) || []),
      ...(((facets.data as { diagnostics?: unknown[] } | undefined)?.diagnostics as []) || []),
    ],
    [descriptor.data?.diagnostics, detail.data?.diagnostics, facets.data, files.data, lineage.data, rendered.data?.diagnostics, siblings.data],
  );
  const jsonTabs = useMemo<JsonModalTab[]>(
    () => [
      { id: "descriptor", label: "Descriptor", jsonText: buildJsonMarkdownPreview(descriptor.data || {}).jsonText, loading: descriptor.isFetching },
      { id: "detail", label: "Detail", jsonText: buildJsonMarkdownPreview(detail.data || {}).jsonText, loading: detail.isFetching },
      { id: "render", label: "Render", jsonText: buildJsonMarkdownPreview(rendered.data || {}).jsonText, loading: rendered.isFetching },
      { id: "lineage", label: "Lineage", jsonText: buildJsonMarkdownPreview(lineage.data || {}).jsonText, loading: lineage.isFetching },
      { id: "siblings", label: "Siblings", jsonText: buildJsonMarkdownPreview(siblings.data || {}).jsonText, loading: siblings.isFetching },
      { id: "files", label: "Files", jsonText: buildJsonMarkdownPreview(files.data || {}).jsonText, loading: files.isFetching },
      { id: "facets", label: "Facets", jsonText: buildJsonMarkdownPreview(facets.data || {}).jsonText, loading: facets.isFetching },
      { id: "diagnostics", label: "Diagnostics", jsonText: buildJsonMarkdownPreview(diagnostics).jsonText },
    ],
    [
      descriptor.data,
      descriptor.isFetching,
      detail.data,
      detail.isFetching,
      diagnostics,
      facets.data,
      facets.isFetching,
      files.data,
      files.isFetching,
      lineage.data,
      lineage.isFetching,
      rendered.data,
      rendered.isFetching,
      siblings.data,
      siblings.isFetching,
    ],
  );
  const copyText = useCallback(async (target: "json" | "markdown" | "filepath", textValue: string | null | undefined) => {
    if (!textValue) {
      notify({ title: target === "filepath" ? "No filepath available." : "Nothing to copy.", tone: "error" });
      return;
    }
    try {
      await navigator.clipboard.writeText(textValue);
      notify({ title: target === "json" ? "JSON copied." : target === "filepath" ? "Filepath copied." : "Markdown copied.", tone: "success" });
    } catch {
      notify({ title: "Clipboard write failed.", description: "Content remains selectable.", tone: "error" });
    }
  }, [notify]);
  const refreshRecord = useCallback(() => {
    void descriptor.refetch();
    void detail.refetch();
    void rendered.refetch();
    void lineage.refetch();
    void siblings.refetch();
    void files.refetch();
    void facets.refetch();
  }, [descriptor, detail, facets, files, lineage, rendered, siblings]);
  const closeJsonModal = useCallback(() => {
    setJsonModalOpen(false);
    window.requestAnimationFrame(() => viewJsonButtonRef.current?.focus());
  }, []);
  const parentIdeaTarget = useMemo(() => parentIdeaNavigation(parentIdea), [parentIdea]);
  const openParentIdea = useCallback(() => {
    if (!parentIdeaTarget?.ideaId) {
      return;
    }
    workbenchCommands$.next({
      type: "open-idea",
      topicId,
      ideaId: parentIdeaTarget.ideaId,
      onOpenResult: (result) => {
        if (result.status === "ignored") {
          notify({
            title: "Parent idea is no longer available.",
            description: parentIdeaTarget.label,
            tone: "error",
          });
        }
      },
    });
  }, [notify, parentIdeaTarget, topicId]);
  const showSpecialViewer = surface === "pdf" || surface === "image" || surface === "table";
  return (
    <section className="panel-body detail-viewer idea-detail-panel">
      <div className="detail-heading">
        <div>
          <h3>{title}</h3>
          <span>{relativePath || recordId}</span>
        </div>
        <div className="toolbar idea-toolbar">
          <ToolbarButton ref={viewJsonButtonRef} type="button" disabled={!descriptor.data} onClick={() => setJsonModalOpen(true)}>
            View JSON
          </ToolbarButton>
          <ToolbarButton type="button" disabled={!markdownContent} onClick={() => void copyText("markdown", markdownContent)}>
            Copy Markdown
          </ToolbarButton>
          <ToolbarButton type="button" onClick={refreshRecord}>
            <RefreshCw aria-hidden="true" />
            Refresh
          </ToolbarButton>
          <ToolbarButton type="button" disabled={!absoluteFilepath} onClick={() => void copyText("filepath", absoluteFilepath)}>
            Copy Filepath
          </ToolbarButton>
        </div>
      </div>
      <div className="idea-status-row">
        <StatusBadge>{descriptor.data?.viewer_kind || "loading"}</StatusBadge>
        {parentIdeaTarget ? (
          parentIdeaTarget.ideaId && topicId ? (
            <StatusBadgeButton
              aria-label={`Open parent idea ${parentIdeaTarget.label}`}
              className="parent-idea-button"
              onClick={openParentIdea}
            >
              parent idea: {parentIdeaTarget.label}
            </StatusBadgeButton>
          ) : (
            <StatusBadge>parent idea: {parentIdeaTarget.label}</StatusBadge>
          )
        ) : null}
      </div>
      {showSpecialViewer ? (
        <ViewerContent descriptor={descriptor.data} rendered={rendered.data} detail={detail.data} renderIsPending={Boolean(rendered.isPending || rendered.isFetching)} />
      ) : rendered.isPending && !markdownContent && descriptor.data?.viewer_kind === "markdown" ? (
        <MarkdownView content="Rendering Markdown." state="loading" />
      ) : (
        <MarkdownView content={markdownContent || "No rendered Markdown available for this record."} state={markdownContent ? "ready" : "empty"} />
      )}
      {jsonModalOpen ? (
        <JsonModal
          title={`${title} Data`}
          description="JSON data for the selected record."
          tabs={jsonTabs}
          defaultTabId="detail"
          onClose={closeJsonModal}
          onCopy={(jsonText) => void copyText("json", jsonText)}
        />
      ) : null}
    </section>
  );
}

export type ParentIdeaNavigation = {
  ideaId: string;
  label: string;
};

export function parentIdeaNavigation(parentIdea: unknown): ParentIdeaNavigation | null {
  if (!parentIdea || typeof parentIdea !== "object") {
    return null;
  }
  const value = parentIdea as Record<string, unknown>;
  const displayKey = typeof value.display_key === "string" ? value.display_key : "";
  const title = typeof value.title === "string" ? value.title : "";
  const ideaId = typeof value.idea_id === "string" ? value.idea_id : "";
  const label = displayKey && title ? `${displayKey} ${title}` : displayKey || title || ideaId;
  if (!label) {
    return null;
  }
  return { ideaId, label };
}

export function ViewerContent({
  descriptor,
  rendered,
  detail,
  renderIsPending = false,
}: {
  descriptor: unknown;
  rendered: unknown;
  detail: unknown;
  renderIsPending?: boolean;
}) {
  const data = descriptor as { viewer_kind?: string; primary_content_url?: string | null; media_type?: string | null } | undefined;
  if (!data) {
    return <div className="empty-state">Loading record.</div>;
  }
  const surface = viewerSurface(data);
  if (surface === "pdf" && data.primary_content_url) {
    return <iframe className="pdf-frame" title="PDF viewer" src={data.primary_content_url} />;
  }
  if (surface === "image" && data.primary_content_url) {
    return <img className="image-viewer" alt="" src={data.primary_content_url} />;
  }
  if (surface === "markdown") {
    const content = String(((rendered as { render?: { content?: string | null } })?.render?.content) || "");
    if (renderIsPending && !content) {
      return <MarkdownView content="Rendering Markdown." state="loading" />;
    }
    return <MarkdownView content={content || "No rendered Markdown available."} state={content ? "ready" : "empty"} />;
  }
  if (surface === "table") {
    return <JsonBlock title="Table" value={detail} />;
  }
  return <JsonBlock title={surface === "json" ? "JSON" : "Record"} value={detail} />;
}

type JsonModalTab = {
  id: string;
  label: string;
  jsonText: string;
  loading?: boolean;
};

export function JsonModal({
  title,
  description,
  tabs,
  defaultTabId,
  onClose,
  onCopy,
}: {
  title: string;
  description?: string;
  tabs: JsonModalTab[];
  defaultTabId: string;
  onClose: () => void;
  onCopy: (jsonText: string) => void;
}) {
  const [activeTabId, setActiveTabId] = useState(defaultTabId);
  const activeTab = tabs.find((tab) => tab.id === activeTabId) || tabs[0];
  return (
    <Dialog open onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="json-modal max-w-[min(1040px,calc(100vw-2rem))] sm:max-w-[min(1040px,calc(100vw-2rem))]" showCloseButton={false}>
        <div className="json-modal-heading">
          <DialogHeader>
            <DialogTitle>{title}</DialogTitle>
            <DialogDescription className="sr-only">{description || "JSON data for the selected item."}</DialogDescription>
          </DialogHeader>
          <DialogFooter className="toolbar">
            <ToolbarButton type="button" onClick={() => onCopy(activeTab?.jsonText || "")} disabled={!activeTab?.jsonText || activeTab.loading}>
              Copy JSON
            </ToolbarButton>
            <ToolbarButton type="button" onClick={onClose}>
              Close
            </ToolbarButton>
          </DialogFooter>
        </div>
        <Tabs value={activeTab?.id || defaultTabId} onValueChange={setActiveTabId} className="json-modal-tabs">
          <TabsList className="json-modal-tabs-list">
            {tabs.map((tab) => (
              <TabsTrigger key={tab.id} value={tab.id}>
                {tab.label}
              </TabsTrigger>
            ))}
          </TabsList>
          {tabs.map((tab) => (
            <TabsContent key={tab.id} value={tab.id} className="json-modal-tab-content">
              {tab.loading ? <div className="empty-state">Loading full JSON.</div> : <pre className="json-modal-code">{tab.jsonText || "No JSON content available."}</pre>}
            </TabsContent>
          ))}
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}

function DiagnosticsPanel({ topicId, graphScope }: { topicId?: string; graphScope: GraphScope }) {
  const project = useQuery({ queryKey: ["project", "diagnostics"], queryFn: getProject, enabled: !topicId });
  const graph = useQuery({
    queryKey: ["topic", topicId, "graph", graphScope, "diagnostics"],
    queryFn: () => getTopicGraph(topicId || "", graphScope, graphScope === "idea-lineage" ? "auto" : "sigma", { includeSecondary: true }),
    enabled: Boolean(topicId),
  });
  const diagnostics = topicId ? graph.data?.diagnostics || [] : project.data?.diagnostics || [];
  return (
    <section className="panel-body">
      {topicId ? <GraphSummary graph={graph.data} isLoading={graph.isLoading} /> : <div className="status-line">Project diagnostics</div>}
      <div className="diagnostics-list">
        {diagnostics.map((diagnostic, index) => (
          <div className={`diagnostic ${diagnostic.severity || "info"}`} key={`${diagnostic.code}-${index}`}>
            <strong>{diagnostic.code || "diagnostic"}</strong>
            <span>{diagnostic.message || ""}</span>
          </div>
        ))}
        {(graph.data?.groups || []).flatMap((group) =>
          (group.diagnostics || []).map((diagnostic, index) => (
            <div className={`diagnostic ${diagnostic.severity || "info"}`} key={`${group.id}-${diagnostic.code}-${index}`}>
              <strong>{diagnostic.code || group.title}</strong>
              <span>{diagnostic.message || group.purpose || ""}</span>
            </div>
          )),
        )}
      </div>
    </section>
  );
}

function JsonBlock({ title, value }: { title: string; value: unknown }) {
  return (
    <div className="json-block">
      <h4>{title}</h4>
      <pre>{JSON.stringify(value || {}, null, 2)}</pre>
    </div>
  );
}

function FilesBlock({ value, topicId, recordId }: { value: unknown; topicId: string; recordId: string }) {
  const files = ((value as { files?: Array<Record<string, unknown>> })?.files || []) as Array<Record<string, unknown>>;
  return (
    <div className="json-block">
      <h4>Files</h4>
      <div className="file-list">
        {files.map((file) => (
          <div className="file-row" key={String(file.id || file.path)}>
            <strong>{String(file.file_role || "file")}</strong>
            <span>{topicRelativeDisplayPath(file.path || "", { topicId })}</span>
            <small>{file.openable ? "openable" : `not openable: ${String(file.open_blocked_reason || "unknown")}`}</small>
            {file.openable && file.id ? (
              <ToolbarButton
                type="button"
                onClick={(event) => {
                  event.stopPropagation();
                  workbenchCommands$.next({ type: "open-file", topicId, recordId, fileId: String(file.id) });
                }}
              >
                Open
              </ToolbarButton>
            ) : null}
          </div>
        ))}
      </div>
    </div>
  );
}

function useRecordsTable(records: RecordSummary[], topicId: string) {
  const columnHelper = createColumnHelper<RecordSummary>();
  const [sorting, setSorting] = useState<SortingState>([]);
  const columns = useMemo(
    () => [
      columnHelper.accessor("record_id", {
        header: "Record",
        cell: (info) => (
          <LinkButton
            type="button"
            onClick={(event) => {
              event.stopPropagation();
              workbenchCommands$.next({ type: "open-record", topicId, recordId: info.getValue() });
            }}
          >
            {info.getValue()}
          </LinkButton>
        ),
      }),
      columnHelper.accessor("record_kind", { header: "Kind", cell: (info) => info.getValue() || "" }),
      columnHelper.accessor("status", { header: "Status", cell: (info) => info.getValue() || "" }),
      columnHelper.accessor("title", { header: "Title", cell: (info) => info.getValue() || "" }),
      columnHelper.accessor("summary", { header: "Summary", cell: (info) => info.getValue() || "" }),
      columnHelper.accessor("updated_at", { header: "Updated", cell: (info) => info.getValue() || "" }),
    ],
    [columnHelper, topicId],
  );
  return useReactTable({
    data: records,
    columns,
    state: { sorting },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
  });
}

function graphTitle(scope: GraphScope): string {
  return scopeLabel(scope);
}

function scopeLabel(scope: GraphScope): string {
  return {
    "idea-lineage": "Idea Graph",
    "idea-timeline": "Idea Timeline",
  }[scope];
}

function useUrlState(): [
  WorkbenchSearchState,
  (next: WorkbenchSearchState, options?: { mode?: UrlSyncMode; metadata?: WorkbenchHistoryMetadata }) => WorkbenchHistoryState,
] {
  const read = useCallback((): WorkbenchSearchState => {
    return readWorkbenchSearch(window.location.search);
  }, []);
  const [state, setState] = useState(read);
  const write = useCallback((next: WorkbenchSearchState, options: { mode?: UrlSyncMode; metadata?: WorkbenchHistoryMetadata } = {}) => {
    const historyState = writeWorkbenchHistory(next, options);
    setState(next);
    return historyState;
  }, []);
  return [state, write];
}

function asGraphScope(value: string | null | undefined, fallback: GraphScope): GraphScope {
  return isGraphScope(value) ? value : fallback;
}

function intersectsEvent(queryKey: readonly unknown[], graphScopes: string[]) {
  if (graphScopes.length === 0) {
    return true;
  }
  return queryKey.some((part) => typeof part === "string" && graphScopes.includes(part));
}

export function mountApp(element: HTMLElement) {
  createRoot(element).render(
    <React.StrictMode>
      <RootApp />
    </React.StrictMode>,
  );
}
