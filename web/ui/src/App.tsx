import { hotkeysCoreFeature, selectionFeature, syncDataLoaderFeature, type ItemInstance } from "@headless-tree/core";
import { useTree } from "@headless-tree/react";
import { QueryClient, QueryClientProvider, useQuery, useQueryClient } from "@tanstack/react-query";
import { createRootRoute, createRouter, RouterProvider } from "@tanstack/react-router";
import { createColumnHelper, flexRender, getCoreRowModel, useReactTable } from "@tanstack/react-table";
import { Background, Controls, ReactFlow, ReactFlowProvider, useReactFlow, type Edge, type Node } from "@xyflow/react";
import { themeLight } from "dockview";
import { DockviewReact, type DockviewReadyEvent, type IDockviewPanelProps } from "dockview-react";
import Graphology from "graphology";
import mermaid from "mermaid";
import React, { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import ReactMarkdown from "react-markdown";
import rehypeKatex from "rehype-katex";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import Sigma from "sigma";
import { Subscription } from "rxjs";
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
  getTopicGraph,
  getTopics,
  getViewerDescriptor,
  type GraphFilters,
} from "./api";
import { layoutFlowGraph, requestedRenderer, selectRenderer, toFlowEdges, toFlowNodes } from "./graph-utils";
import { buildJsonMarkdownPreview } from "./markdown-doc";
import { manualRefresh$, topicInvalidations, workbenchCommands$ } from "./events";
import type { ExplorerNode, GraphScope, IdeaDetailResponse, OpenableItemDescriptor, RecordSummary, TopicGraphView } from "./types";
import { filterRecords, openPanelFromDescriptor, viewerSurface, type DockviewApiLike, type OpenPanelResult } from "./view-model";
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
import "katex/dist/katex.min.css";
import "./styles.css";

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
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  );
}

function Workbench() {
  const [urlState, setUrlState] = useUrlState();
  const [dockApi, setDockApi] = useState<unknown>(null);
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
      commitUrlState({ topicId: selectedTopicId, graphScope }, "replace");
    }
  }, [commitUrlState, graphScope, selectedTopicId, urlState.topicId]);

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
        const nextGraphScope = isGraphScope(descriptor.graph_scope || null) ? descriptor.graph_scope : options.sourceState?.graphScope || graphScope;
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
        void openItem(`idea:${command.topicId}:${command.ideaId}`);
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

  return (
    <div className="research-shell">
      <aside className="sidebar explorer-sidebar">
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
          onOpenItem={(openableItemId) => void openItem(openableItemId)}
        />
      </aside>
      <main className="workbench">
        <div className="topbar">
          <div className="topic-heading">
            <span>Research Topic</span>
            <h2>{selectedTopicId || "Select a topic"}</h2>
          </div>
          <div className="toolbar">
            <button type="button" onClick={() => selectedTopicId && manualRefresh$.next({ topicId: selectedTopicId })}>
              Refresh
            </button>
          </div>
        </div>
        {selectedTopicId ? (
          <div className="dock-host dockview-theme-light">
            <DockviewReact components={dockComponents} onReady={onDockReady} theme={themeLight} />
          </div>
        ) : (
          <div className="empty-state">No topic selected.</div>
        )}
      </main>
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
    <button
      {...props}
      className={`explorer-row ${item.isFolder() ? "folder" : "leaf"} ${item.isExpanded() ? "expanded" : ""} ${item.isFocused() ? "focused" : ""} ${isSelectedTopic ? "active-topic" : ""}`}
      data-testid={`explorer-row-${item.getId()}`}
      onClick={onClick}
      style={{ paddingLeft: `${8 + item.getItemMeta().level * 14}px` }}
      type="button"
    >
      <span className="explorer-twist">{item.isFolder() ? (item.isExpanded() ? "v" : ">") : ""}</span>
      <span className={`explorer-icon ${data.icon_hint || "item"}`} />
      <span className="explorer-label">{data.label}</span>
      {data.badge_text ? <span className="explorer-badge">{data.badge_text}</span> : null}
      {data.diagnostics_count ? <span className="explorer-warning">{data.diagnostics_count}</span> : null}
    </button>
  );
}

const dockComponents = {
  ideaGraph: (props: IDockviewPanelProps<PanelParams>) => <IdeaGraphPanel {...props.params} />,
  denseGraph: (props: IDockviewPanelProps<PanelParams>) => <DenseGraphPanel topicId={props.params.topicId || ""} graphScope={asGraphScope(props.params.graphScope, "artifact-overview")} />,
  records: (props: IDockviewPanelProps<PanelParams>) => <RecordsPanel topicId={props.params.topicId || ""} />,
  recordDetail: (props: IDockviewPanelProps<PanelParams>) => <RecordDetailPanel topicId={props.params.topicId || ""} recordId={props.params.recordId || ""} />,
  ideaDetail: (props: IDockviewPanelProps<PanelParams>) => <IdeaDetailPanel topicId={props.params.topicId || ""} ideaId={props.params.ideaId || ""} />,
  diagnostics: (props: IDockviewPanelProps<PanelParams>) => <DiagnosticsPanel topicId={props.params.topicId} graphScope={asGraphScope(props.params.graphScope, "idea-lineage")} />,
  projectOverview: () => <ProjectOverviewPanel />,
  topicOverview: (props: IDockviewPanelProps<PanelParams>) => <TopicOverviewPanel topicId={props.params.topicId || ""} />,
  runtime: (props: IDockviewPanelProps<PanelParams>) => <RuntimePanel topicId={props.params.topicId || ""} />,
  actors: (props: IDockviewPanelProps<PanelParams>) => <ActorsPanel topicId={props.params.topicId || ""} />,
  repository: (props: IDockviewPanelProps<PanelParams>) => <RepositoryPanel topicId={props.params.topicId || ""} />,
  fileArtifact: (props: IDockviewPanelProps<PanelParams>) => <FileArtifactPanel contentUrl={props.params.contentUrl || ""} mediaType={props.params.mediaType || ""} />,
};

function IdeaGraphPanel({ topicId, graphScope = "idea-lineage" }: PanelParams) {
  const selectedGraphScope = asGraphScope(graphScope, "idea-lineage");
  const [filters, setFilters] = useState<GraphFilters>({ includeSecondary: false });
  const graph = useQuery({
    queryKey: ["topic", topicId, "graph", selectedGraphScope, requestedRenderer(selectedGraphScope), filters],
    queryFn: () => getTopicGraph(topicId || "", selectedGraphScope, requestedRenderer(selectedGraphScope), filters),
    enabled: Boolean(topicId),
  });
  const [flowNodes, setFlowNodes] = useState<Node[]>([]);
  const flowEdges = useMemo(() => (graph.data ? toFlowEdges(graph.data) : []), [graph.data]);

  useEffect(() => {
    let subscription = new Subscription();
    if (graph.data) {
      const nodes = toFlowNodes(graph.data);
      layoutFlowGraph(nodes, flowEdges).then((layouted) => {
        if (!subscription.closed) {
          setFlowNodes(layouted);
        }
      });
    }
    return () => subscription.unsubscribe();
  }, [flowEdges, graph.data]);

  return (
    <section className="panel-body">
      <GraphFiltersBar filters={filters} onChange={setFilters} />
      {graph.data && selectRenderer(selectedGraphScope, graph.data.renderer_hint, graph.data.nodes.length) === "sigma" ? (
        <SigmaGraph graph={graph.data} />
      ) : (
        <ReactFlowProvider>
          <div className="flow-frame">
            <ReactFlow nodes={flowNodes} edges={flowEdges} fitView onNodeClick={(_event, node) => openRecordFromNode(topicId, graph.data, node.id)}>
              <FlowAutoFit edgeCount={flowEdges.length} nodeCount={flowNodes.length} />
              <Background />
              <Controls />
            </ReactFlow>
          </div>
        </ReactFlowProvider>
      )}
      <GraphSummary graph={graph.data} isLoading={graph.isLoading} />
    </section>
  );
}

function FlowAutoFit({ edgeCount, nodeCount }: { edgeCount: number; nodeCount: number }) {
  const { fitView } = useReactFlow();
  useEffect(() => {
    if (!nodeCount) {
      return undefined;
    }
    const fit = () => fitView({ padding: 0.2, duration: 0 });
    const animationFrame = window.requestAnimationFrame(fit);
    window.addEventListener("resize", fit);
    return () => {
      window.cancelAnimationFrame(animationFrame);
      window.removeEventListener("resize", fit);
    };
  }, [edgeCount, fitView, nodeCount]);
  return null;
}

function DenseGraphPanel({ topicId, graphScope }: { topicId: string; graphScope: GraphScope }) {
  const [filters, setFilters] = useState<GraphFilters>({ includeSecondary: true });
  const graph = useQuery({
    queryKey: ["topic", topicId, "graph", graphScope, "sigma", filters],
    queryFn: () => getTopicGraph(topicId, graphScope, "sigma", filters),
    enabled: Boolean(topicId),
  });
  return (
    <section className="panel-body">
      <GraphFiltersBar filters={filters} onChange={setFilters} />
      {graph.data ? <SigmaGraph graph={graph.data} /> : <div className="empty-state">Loading graph.</div>}
      <GraphSummary graph={graph.data} isLoading={graph.isLoading} />
    </section>
  );
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

function TopicOverviewPanel({ topicId }: { topicId: string }) {
  const topic = useQuery({ queryKey: ["topic", topicId, "overview"], queryFn: () => getTopic(topicId), enabled: Boolean(topicId) });
  const runtime = useQuery({ queryKey: ["topic", topicId, "runtime", "overview"], queryFn: () => getRuntime(topicId), enabled: Boolean(topicId) });
  return (
    <section className="panel-body overview-panel">
      <div className="detail-heading">
        <h3>{topicId || "Topic Overview"}</h3>
        <span>{topic.data ? "overview" : "loading"}</span>
      </div>
      <div className="overview-grid">
        <JsonBlock title="Topic" value={topic.data} />
        <JsonBlock title="Runtime" value={runtime.data} />
      </div>
    </section>
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

function SigmaGraph({ graph }: { graph: TopicGraphView }) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  useEffect(() => {
    if (!containerRef.current) {
      return undefined;
    }
    const graphology = new Graphology({ multi: true });
    for (const node of graph.nodes) {
      graphology.addNode(node.id, {
        label: node.title,
        x: Math.random(),
        y: Math.random(),
        size: Number(node.renderer_hints?.size || 8),
        color: String(node.renderer_hints?.color || "#64748b"),
      });
    }
    for (const edge of graph.edges) {
      if (graphology.hasNode(edge.source) && graphology.hasNode(edge.target) && !graphology.hasEdge(edge.id)) {
        graphology.addEdgeWithKey(edge.id, edge.source, edge.target, { label: edge.relation_kind, color: "#94a3b8" });
      }
    }
    const renderer = new Sigma(graphology, containerRef.current, { allowInvalidContainer: true });
    renderer.on("clickNode", ({ node }) => openRecordFromNode(graph.topic_id, graph, node));
    return () => renderer.kill();
  }, [graph]);
  return <div className="sigma-frame" ref={containerRef} />;
}

export function GraphFiltersBar({ filters, onChange }: { filters: GraphFilters; onChange: (filters: GraphFilters) => void }) {
  return (
    <div className="filters">
      <input aria-label="Search graph" placeholder="search" value={filters.search || ""} onChange={(event) => onChange({ ...filters, search: event.target.value })} />
      <input aria-label="Status filter" placeholder="status" value={filters.status || ""} onChange={(event) => onChange({ ...filters, status: event.target.value })} />
      <input aria-label="Relation filter" placeholder="relation" value={filters.relationKind || ""} onChange={(event) => onChange({ ...filters, relationKind: event.target.value })} />
      <label className="checkbox">
        <input aria-label="Show supporting records" type="checkbox" checked={Boolean(filters.includeSecondary)} onChange={(event) => onChange({ ...filters, includeSecondary: event.target.checked })} />
        Supporting Records
      </label>
    </div>
  );
}

function RecordsPanel({ topicId }: { topicId: string }) {
  const [search, setSearch] = useState("");
  const [facet, setFacet] = useState("");
  const records = useQuery({
    queryKey: ["topic", topicId, "records", facet],
    queryFn: () => getRecords(topicId, { facet: facet || undefined, limit: 500 }),
    enabled: Boolean(topicId),
  });
  const filteredRecords = useMemo(() => filterRecords(records.data?.records || [], search), [records.data?.records, search]);
  const table = useRecordsTable(filteredRecords, topicId);
  return (
    <section className="panel-body">
      <div className="filters">
        <input aria-label="Search records" placeholder="search records" value={search} onChange={(event) => setSearch(event.target.value)} />
        <select aria-label="Facet" value={facet} onChange={(event) => setFacet(event.target.value)}>
          <option value="">all facets</option>
          <option value="ideas">ideas</option>
          <option value="routes">routes</option>
          <option value="metrics">metrics</option>
          <option value="claims">claims</option>
          <option value="facts">facts</option>
        </select>
      </div>
      <div className="table-wrap">
        <table>
          <thead>
            {table.getHeaderGroups().map((group) => (
              <tr key={group.id}>
                {group.headers.map((header) => (
                  <th key={header.id}>{flexRender(header.column.columnDef.header, header.getContext())}</th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody>
            {table.getRowModel().rows.map((row) => (
              <tr key={row.id} onClick={() => workbenchCommands$.next({ type: "open-record", topicId, recordId: row.original.record_id })}>
                {row.getVisibleCells().map((cell) => (
                  <td key={cell.id}>{flexRender(cell.column.columnDef.cell, cell.getContext())}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

type CopyState = {
  target: "json" | "markdown" | null;
  status: "idle" | "success" | "error";
  message?: string;
};

export function IdeaDetailPanel({ topicId, ideaId }: { topicId: string; ideaId: string }) {
  const queryClientValue = useQueryClient();
  const viewJsonButtonRef = useRef<HTMLButtonElement | null>(null);
  const previousDigestRef = useRef<string | undefined>(undefined);
  const [jsonModalOpen, setJsonModalOpen] = useState(false);
  const [copyState, setCopyState] = useState<CopyState>({ target: null, status: "idle" });
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
  const diagnostics = [...(detail.data?.diagnostics || []), ...(fullDetail.data?.diagnostics || [])];
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

  const fetchExactSourceJson = useCallback(async (): Promise<unknown | undefined> => {
    if (detail.data?.idea_content !== undefined) {
      return detail.data.idea_content;
    }
    if (detail.data?.source?.source_json !== undefined) {
      return detail.data.source.source_json;
    }
    if (!detail.data?.source?.source_json_truncated) {
      return undefined;
    }
    const fetched = await queryClientValue.fetchQuery({
      queryKey: ["topic", topicId, "idea-lineage", "idea", ideaId, "detail", true],
      queryFn: () => getIdeaDetail(topicId, ideaId, { includeSourceJson: true }),
    });
    return fetched.idea_content ?? fetched.source?.source_json;
  }, [detail.data?.idea_content, detail.data?.source, ideaId, queryClientValue, topicId]);

  const copyText = useCallback(async (target: "json" | "markdown", textValue: string | null | undefined) => {
    if (!textValue) {
      setCopyState({ target, status: "error", message: "Nothing to copy." });
      return;
    }
    try {
      await navigator.clipboard.writeText(textValue);
      setCopyState({ target, status: "success", message: target === "json" ? "JSON copied." : "Markdown copied." });
    } catch {
      setCopyState({ target, status: "error", message: "Clipboard write failed. Content remains selectable." });
    }
  }, []);

  const copyJson = useCallback(async () => {
    try {
      const exact = await fetchExactSourceJson();
      await copyText("json", exact === undefined ? null : buildJsonMarkdownPreview(exact).jsonText);
    } catch {
      setCopyState({ target: "json", status: "error", message: "Full JSON fetch failed." });
    }
  }, [copyText, fetchExactSourceJson]);

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
          <button
            ref={viewJsonButtonRef}
            type="button"
            disabled={!detail.data?.source?.source_json_available}
            onClick={() => setJsonModalOpen(true)}
          >
            View JSON
          </button>
          <button type="button" disabled={!detail.data?.source?.source_json_available} onClick={() => void copyJson()}>
            Copy JSON
          </button>
          <button type="button" disabled={!preview?.markdown} onClick={() => void copyText("markdown", preview?.markdown)}>
            Copy Markdown
          </button>
          <button type="button" onClick={() => void detail.refetch()}>
            Refresh
          </button>
        </div>
      </div>
      <div className="idea-status-row">
        <span>{String(provenance?.source_kind || "source pending")}</span>
        {provenance?.source_fragment_status ? <span>{String(provenance.source_fragment_status)}</span> : null}
        {provenance?.source_json_path ? <span>{String(provenance.source_json_path)}</span> : null}
        {sourceTruncated ? <span>source JSON over default cap</span> : null}
        {digestNotice ? <span>{digestNotice}</span> : null}
        {copyState.status !== "idle" ? <span className={`copy-status ${copyState.status}`}>{copyState.message}</span> : null}
        <button
          type="button"
          className="link-button source-record-button"
          disabled={!sourceRecordId}
          onClick={() => workbenchCommands$.next({ type: "open-record", topicId, recordId: sourceRecordId })}
        >
          Open Source Record
        </button>
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
      <div className="detail-columns">
        <JsonBlock
          title="Lineage"
          value={{
            incoming_edges: detail.data?.incoming_edges || [],
            outgoing_edges: detail.data?.outgoing_edges || [],
            generation_groups: detail.data?.generation_groups || [],
          }}
        />
        <JsonBlock title="Realizations" value={detail.data?.realizations || []} />
        <JsonBlock title="Diagnostics" value={diagnostics} />
      </div>
      {jsonModalOpen ? (
        <JsonModal
          title={`${title} JSON`}
          jsonText={modalJsonText || exactJsonText || ""}
          loading={Boolean(sourceTruncated && fullDetail.isFetching && !modalJsonText)}
          copyStatus={copyState.target === "json" ? copyState.message : undefined}
          onClose={closeJsonModal}
          onCopy={() => void copyJson()}
        />
      ) : null}
    </section>
  );
}

function RecordDetailPanel({ topicId, recordId }: { topicId: string; recordId: string }) {
  const descriptor = useQuery({
    queryKey: ["topic", topicId, "record", recordId, "descriptor"],
    queryFn: () => getViewerDescriptor(topicId, recordId),
    enabled: Boolean(topicId && recordId),
  });
  const detail = useQuery({
    queryKey: ["topic", topicId, "record", recordId, "detail", descriptor.data?.viewer_kind === "json"],
    queryFn: () => getRecordDetail(topicId, recordId, descriptor.data?.viewer_kind === "json"),
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
  return (
    <section className="panel-body detail-viewer">
      <div className="detail-heading">
        <h3>{descriptor.data?.title || recordId}</h3>
        <span>{descriptor.data?.viewer_kind || "loading"}</span>
      </div>
      <ViewerContent
        descriptor={descriptor.data}
        rendered={rendered.data}
        detail={detail.data}
        renderIsPending={Boolean(descriptor.data?.viewer_kind === "markdown" && (rendered.isPending || rendered.isFetching))}
      />
      <div className="detail-columns">
        <JsonBlock title="Idea Lineage" value={{ lineage: lineage.data, siblings: siblings.data }} />
        <FilesBlock value={files.data} topicId={topicId} recordId={recordId} />
        <JsonBlock title="Supporting Details" value={facets.data} />
      </div>
    </section>
  );
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

type MarkdownViewState = "loading" | "empty" | "ready";

export function MarkdownView({ content, state = "ready" }: { content: string; state?: MarkdownViewState }) {
  if (state !== "ready") {
    return (
      <div className={`markdown-view markdown-view-status markdown-view-${state}`}>
        <p>{content}</p>
      </div>
    );
  }
  return (
    <div className="markdown-view">
      <ReactMarkdown
        remarkPlugins={[remarkGfm, remarkMath]}
        rehypePlugins={[rehypeKatex]}
        components={{
          code(props) {
            const className = props.className || "";
            const value = String(props.children || "");
            if (className.includes("language-mermaid")) {
              return <MermaidBlock chart={value} />;
            }
            return <code className={className}>{props.children}</code>;
          },
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}

function MermaidBlock({ chart }: { chart: string }) {
  const [svg, setSvg] = useState("");
  useEffect(() => {
    let cancelled = false;
    mermaid.initialize({ startOnLoad: false, securityLevel: "strict" });
    mermaid.render(`mmd-${crypto.randomUUID()}`, chart).then((result) => {
      if (!cancelled) {
        setSvg(result.svg);
      }
    });
    return () => {
      cancelled = true;
    };
  }, [chart]);
  return <div className="mermaid" dangerouslySetInnerHTML={{ __html: svg }} />;
}

export function JsonModal({
  title,
  jsonText,
  loading,
  copyStatus,
  onClose,
  onCopy,
}: {
  title: string;
  jsonText: string;
  loading?: boolean;
  copyStatus?: string;
  onClose: () => void;
  onCopy: () => void;
}) {
  const closeButtonRef = useRef<HTMLButtonElement | null>(null);
  useEffect(() => {
    closeButtonRef.current?.focus();
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        onClose();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [onClose]);
  return (
    <div className="json-modal-backdrop" role="presentation" onMouseDown={onClose}>
      <section
        className="json-modal"
        role="dialog"
        aria-modal="true"
        aria-label={title}
        onMouseDown={(event) => event.stopPropagation()}
      >
        <div className="json-modal-heading">
          <h3>{title}</h3>
          <div className="toolbar">
            <button type="button" onClick={onCopy} disabled={!jsonText}>
              Copy JSON
            </button>
            <button ref={closeButtonRef} type="button" onClick={onClose}>
              Close
            </button>
          </div>
        </div>
        {copyStatus ? <div className="status-line">{copyStatus}</div> : null}
        {loading ? <div className="empty-state">Loading full JSON.</div> : <pre className="json-modal-code">{jsonText || "No JSON content available."}</pre>}
      </section>
    </div>
  );
}

function DiagnosticsPanel({ topicId, graphScope }: { topicId?: string; graphScope: GraphScope }) {
  const project = useQuery({ queryKey: ["project", "diagnostics"], queryFn: getProject, enabled: !topicId });
  const graph = useQuery({
    queryKey: ["topic", topicId, "graph", graphScope, "diagnostics"],
    queryFn: () => getTopicGraph(topicId || "", graphScope, requestedRenderer(graphScope), { includeSecondary: true }),
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

function GraphSummary({ graph, isLoading }: { graph?: TopicGraphView; isLoading: boolean }) {
  if (isLoading) {
    return <div className="status-line">Loading.</div>;
  }
  if (!graph) {
    return <div className="status-line">No graph data.</div>;
  }
  return (
    <div className="graph-summary">
      <span>{graph.nodes.length} nodes</span>
      <span>{graph.edges.length} edges</span>
      <span>{graph.renderer_hint}</span>
      {graph.paging?.truncated ? <span>truncated</span> : null}
      {graph.error ? <span>{graph.error.code}</span> : null}
    </div>
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
            <span>{String(file.path || "")}</span>
            <small>{file.openable ? "openable" : `not openable: ${String(file.open_blocked_reason || "unknown")}`}</small>
            {file.openable && file.id ? (
              <button
                type="button"
                onClick={(event) => {
                  event.stopPropagation();
                  workbenchCommands$.next({ type: "open-file", topicId, recordId, fileId: String(file.id) });
                }}
              >
                Open
              </button>
            ) : null}
          </div>
        ))}
      </div>
    </div>
  );
}

function useRecordsTable(records: RecordSummary[], topicId: string) {
  const columnHelper = createColumnHelper<RecordSummary>();
  const columns = useMemo(
    () => [
      columnHelper.accessor("record_id", {
        header: "Record",
        cell: (info) => (
          <button
            type="button"
            className="link-button"
            onClick={(event) => {
              event.stopPropagation();
              workbenchCommands$.next({ type: "open-record", topicId, recordId: info.getValue() });
            }}
          >
            {info.getValue()}
          </button>
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
  return useReactTable({ data: records, columns, getCoreRowModel: getCoreRowModel() });
}

export function openRecordFromNode(topicId: string, graph: TopicGraphView | undefined, nodeId: string) {
  const node = graph?.nodes.find((candidate) => candidate.id === nodeId);
  if (!node) {
    return;
  }
  const sourceIdeaId = typeof node.source?.idea_id === "string" ? node.source.idea_id : undefined;
  const ideaId = node.idea_id || sourceIdeaId;
  if (node.material_kind === "idea" && ideaId) {
    workbenchCommands$.next({ type: "open-idea", topicId, ideaId });
    return;
  }
  if (node.record_id) {
    workbenchCommands$.next({ type: "open-record", topicId, recordId: node.record_id });
  }
}

function graphTitle(scope: GraphScope): string {
  return `${scopeLabel(scope)} Graph`;
}

function scopeLabel(scope: GraphScope): string {
  return {
    "idea-lineage": "Ideas",
    "artifact-overview": "Artifacts",
    "experiment-records": "Experiments",
    "paper-revisions": "Papers",
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
  return isGraphScope(value || null) ? value : fallback;
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
