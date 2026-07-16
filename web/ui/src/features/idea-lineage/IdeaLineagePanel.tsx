import { Background, Controls, Handle, Position, ReactFlow, ReactFlowProvider, SelectionMode, useReactFlow, type ColorMode, type NodeMouseHandler, type NodeProps, type Viewport } from "@xyflow/react";
import { useQuery } from "@tanstack/react-query";
import { LoaderCircle } from "lucide-react";
import React, { memo, useCallback, useEffect, useId, useMemo, useRef, useState } from "react";
import { getIdeaDecisionContext, getIdeaDetail, getTopicGraph, traverseIdeas } from "../../api";
import { GraphSummary } from "../graph/GraphPanels";
import { openRecordFromNode } from "../graph/open-record";
import { ideaNodeVisibleLabel, toFlowEdges, toFlowNodes, type IdeaFlowNodeData } from "../../graph-utils";
import { buildJsonMarkdownPreview } from "../../markdown-doc";
import { useGuiTheme } from "../../theme-provider";
import type { GraphScope, TopicGraphNode, TopicGraphView } from "../../types";
import { DEFAULT_HOVER_PREVIEW_DELAY_MS, useGuiSettings } from "../../ui-settings";
import { isGraphScope } from "../../workbench-history";
import { Input } from "@/components/ui/input";
import { ToolbarButton } from "@/components/workbench-controls";
import { useStoreSelector } from "../../state/observable-store";
import {
  createIdeaLineageStore,
  ideaLineageStoreRegistry,
  selectIdeaFlowEdges,
  selectIdeaFlowNodes,
  visibleHoverPreview,
  type IdeaFlowNode,
  type IdeaLineageOpenIntent,
  type IdeaLineageStore,
} from "./idea-lineage-state";
import { createIdeaLineageInteractionBoundary } from "./idea-lineage-interactions";
import { projectIdeaGraphNeighborhood } from "./idea-graph-focus";
import { IdeaGraphControls } from "./IdeaGraphControls";
import { layoutFingerprint } from "./layout-protocol";
import type { IdeaGraphLayoutConfiguration } from "./layout-registry";
import { IdeaGraphLayoutWorkerClient } from "./layout-worker-client";
import { IdeaDecisionContextPanel } from "../idea-portfolio/IdeaDecisionContextPanel";
import { IdeaSteeringDialog } from "../idea-portfolio/IdeaSteeringDialog";
import { PortfolioControls } from "../idea-portfolio/PortfolioControls";
import { applyIdeaPortfolioView, persistIdeaPortfolioView, restoreIdeaPortfolioView, type IdeaPortfolioViewState } from "../idea-portfolio/idea-portfolio";

const NODE_DOUBLE_CLICK_MS = 500;
const NODE_DOUBLE_CLICK_DISTANCE_PX = 72;
const HOVER_PREVIEW_CLOSE_DELAY_MS = 500;
const TOUCH_LONG_PRESS_MOVE_TOLERANCE_PX = 14;
const IDEA_LINEAGE_OVERVIEW_FILTERS = { includeSecondary: true, limit: 5000, preset: "all-proposed" };
const LazyIdeaHoverMarkdownView = React.lazy(() =>
  import("../../markdown-view").then((module) => ({ default: module.MarkdownView })),
);

export type IdeaGraphPanelProps = {
  topicId?: string;
  graphScope?: string;
  panelId?: string;
  openableItemId?: string;
};

export function IdeaGraphPanel({ topicId, graphScope = "idea-lineage", panelId, openableItemId }: IdeaGraphPanelProps) {
  const generatedPanelId = useId();
  const resolvedPanelId = panelId || `idea-lineage:${generatedPanelId}`;
  const store = useMemo(
    () => ideaLineageStoreRegistry.getOrCreate(resolvedPanelId, () => createIdeaLineageStore(), { openableItemId: openableItemId || (topicId ? `topic:${topicId}:graph:idea-lineage` : undefined) }),
    [openableItemId, resolvedPanelId, topicId],
  );

  useEffect(() => () => ideaLineageStoreRegistry.dispose(resolvedPanelId), [resolvedPanelId]);

  return <IdeaGraphPanelWithStore graphScope={graphScope} store={store} topicId={topicId} />;
}

function IdeaGraphPanelWithStore({ topicId, graphScope = "idea-lineage", store }: { topicId?: string; graphScope?: string; store: IdeaLineageStore }) {
  const selectedGraphScope = asGraphScope(graphScope, "idea-lineage");
  const { resolvedThemeMode, themeMode } = useGuiTheme();
  const { hoverPreviewDelayMs = DEFAULT_HOVER_PREVIEW_DELAY_MS } = useGuiSettings();
  const reactFlowColorMode: ColorMode = themeMode === "system" ? "system" : resolvedThemeMode;
  const [searchText, setSearchText] = useState("");
  const [portfolioState, setPortfolioState] = useState<IdeaPortfolioViewState>(() => restoreIdeaPortfolioView(topicId || "", "graph"));
  const [traversalView, setTraversalView] = useState<{ rootIdeaIds: string[]; direction: "ancestors" | "descendants" } | null>(null);
  const [decisionIdeaId, setDecisionIdeaId] = useState<string | null>(null);
  const [steeringAction, setSteeringAction] = useState<{ action: "explore" | "explore_instead"; targetIdeaId: string } | null>(null);
  const [baseNodes, setBaseNodes] = useState<IdeaFlowNode[]>([]);
  const [baseEdges, setBaseEdges] = useState<ReturnType<typeof toFlowEdges>>([]);
  const [lowZoom, setLowZoom] = useState(false);
  const selectedNodeIds = useStoreSelector(store, (state) => state.selectedNodeIds, sameStrings);
  const focus = useStoreSelector(store, (state) => state.focus);
  const layoutDraft = useStoreSelector(store, (state) => state.layoutDraft);
  const appliedLayout = useStoreSelector(store, (state) => state.appliedLayout);
  const hoverPreview = useStoreSelector(store, visibleHoverPreview, sameHoverPreview);
  const openIntent = useStoreSelector(store, (state) => state.openIntent, sameOpenIntent);
  const flowNodes = useMemo(() => selectIdeaFlowNodes(baseNodes, baseEdges, selectedNodeIds), [baseEdges, baseNodes, selectedNodeIds]);
  const highlightedEdges = useMemo(() => selectIdeaFlowEdges(baseEdges, selectedNodeIds), [baseEdges, selectedNodeIds]);
  const flowEdges = useMemo(() => lowZoom ? highlightedEdges.map((edge) => edge.label === undefined ? edge : { ...edge, label: undefined }) : highlightedEdges, [highlightedEdges, lowZoom]);
  const hoverPreviewDelayMsRef = useRef(hoverPreviewDelayMs);
  const lastNodeClickRef = useRef<{ nodeId: string; at: number; x: number; y: number } | null>(null);
  const renderedGraphSignatureRef = useRef<string | null>(null);
  const renderedGraphRevisionRef = useRef<string | null>(null);
  const renderedGraphRef = useRef<TopicGraphView | null>(null);
  const nextLayoutJobIdRef = useRef(1);
  const layoutWorker = useMemo(() => new IdeaGraphLayoutWorkerClient(), []);
  hoverPreviewDelayMsRef.current = hoverPreviewDelayMs;
  const interactionBoundary = useMemo(
    () =>
      createIdeaLineageInteractionBoundary({
        store,
        getHoverPreviewDelayMs: () => hoverPreviewDelayMsRef.current,
        hoverPreviewCloseDelayMs: HOVER_PREVIEW_CLOSE_DELAY_MS,
        touchLongPressMoveTolerancePx: TOUCH_LONG_PRESS_MOVE_TOLERANCE_PX,
      }),
    [store],
  );

  useEffect(() => {
    setPortfolioState(restoreIdeaPortfolioView(topicId || "", "graph"));
    setTraversalView(null);
    setDecisionIdeaId(null);
    setSteeringAction(null);
  }, [topicId]);

  useEffect(() => {
    if (topicId) {
      persistIdeaPortfolioView(topicId, "graph", portfolioState);
    }
  }, [portfolioState, topicId]);

  const graph = useQuery({
    queryKey: ["topic", topicId, "graph", selectedGraphScope, "react-flow", "overview", IDEA_LINEAGE_OVERVIEW_FILTERS.limit],
    queryFn: () => getTopicGraph(topicId || "", selectedGraphScope, "react-flow", IDEA_LINEAGE_OVERVIEW_FILTERS),
    enabled: Boolean(topicId),
  });
  const portfolioGraph = useMemo(() => applyIdeaPortfolioView(graph.data, portfolioState), [graph.data, portfolioState]);
  const traversal = useQuery({
    queryKey: ["topic", topicId, "ideas", "traverse", traversalView?.rootIdeaIds, traversalView?.direction, focus.relationKinds],
    queryFn: () => traverseIdeas(topicId || "", {
      rootIdeaIds: traversalView?.rootIdeaIds || [],
      direction: traversalView?.direction || "descendants",
      relationKinds: focus.relationKinds,
      maxDepth: 8,
      maxNodes: 500,
      maxEdges: 1000,
    }),
    enabled: Boolean(topicId && traversalView),
  });
  const traversalGraph = useMemo(
    () => traversalView && traversal.data?.ok ? projectGraphToIdeaIds(portfolioGraph, traversal.data.nodes.map((node) => String(node.idea_id || "")).filter(Boolean)) : portfolioGraph,
    [portfolioGraph, traversal.data, traversalView],
  );
  const decisionContext = useQuery({
    queryKey: ["topic", topicId, "idea", decisionIdeaId, "decision-context"],
    queryFn: () => getIdeaDecisionContext(topicId || "", decisionIdeaId || ""),
    enabled: Boolean(topicId && decisionIdeaId),
  });
  const backendFocusGraph = useQuery({
    queryKey: ["topic", topicId, "graph", selectedGraphScope, "react-flow", "focus", selectedNodeIds, focus.hopRadius, focus.direction, focus.relationKinds, focus.edgeMode],
    queryFn: () => getTopicGraph(topicId || "", selectedGraphScope, "react-flow", {
      includeSecondary: true,
      seedNodeIds: selectedNodeIds,
      hopRadius: focus.hopRadius,
      direction: focus.direction,
      relationKind: focus.relationKinds.join(",") || undefined,
      edgeMode: focus.edgeMode,
      preset: portfolioState.preset,
      explorationState: portfolioState.explorationState,
      decisionState: portfolioState.decisionState,
      evidenceState: portfolioState.evidenceState,
      archiveState: portfolioState.archiveState,
      visibility: portfolioState.visibility,
      generationId: portfolioState.generationId,
      decisionRecordId: portfolioState.decisionRecordId,
    }),
    enabled: Boolean(topicId && focus.enabled && selectedNodeIds.length > 0 && traversalGraph && traversalGraph.topology_complete !== true),
  });
  const focusedGraph = useMemo(() => {
    if (!traversalGraph || !focus.enabled) {
      return traversalGraph;
    }
    if (traversalGraph.topology_complete === true) {
      return projectIdeaGraphNeighborhood(traversalGraph, selectedNodeIds, focus);
    }
    return backendFocusGraph.data;
  }, [backendFocusGraph.data, focus, selectedNodeIds, traversalGraph]);
  const filteredGraph = useMemo(() => filterIdeaLineageGraphForSearch(focusedGraph, searchText), [focusedGraph, searchText]);

  useEffect(() => () => interactionBoundary.dispose(), [interactionBoundary]);
  useEffect(() => () => layoutWorker.terminate(), [layoutWorker]);

  const openFlowNode = useCallback((nodeId: string) => {
    interactionBoundary.nodeOpen({ nodeId });
  }, [interactionBoundary]);

  const openRecentNodeClick = useCallback((event: React.MouseEvent<HTMLDivElement>) => {
    const lastClick = lastNodeClickRef.current;
    if (!lastClick) {
      return false;
    }
    const dx = event.clientX - lastClick.x;
    const dy = event.clientY - lastClick.y;
    const closeEnough = Math.hypot(dx, dy) <= NODE_DOUBLE_CLICK_DISTANCE_PX;
    const soonEnough = Date.now() - lastClick.at < NODE_DOUBLE_CLICK_MS;
    if (!closeEnough || !soonEnough) {
      return false;
    }
    event.preventDefault();
    event.stopPropagation();
    lastNodeClickRef.current = null;
    openFlowNode(lastClick.nodeId);
    return true;
  }, [openFlowNode]);

  const handleNodeClick = useCallback<NodeMouseHandler<IdeaFlowNode>>((event, node) => {
    const now = Date.now();
    const lastClick = lastNodeClickRef.current;
    const isSecondClick = event.detail >= 2 || (lastClick?.nodeId === node.id && now - lastClick.at < NODE_DOUBLE_CLICK_MS);
    if (isSecondClick) {
      event.preventDefault();
      lastNodeClickRef.current = null;
      openFlowNode(node.id);
      return;
    }
    interactionBoundary.nodeClick({ nodeId: node.id, toggle: event.ctrlKey || event.metaKey });
    lastNodeClickRef.current = { nodeId: node.id, at: now, x: event.clientX, y: event.clientY };
  }, [interactionBoundary, openFlowNode]);

  const handleNodeDoubleClick = useCallback<NodeMouseHandler<IdeaFlowNode>>((event, node) => {
    event.preventDefault();
    lastNodeClickRef.current = null;
    openFlowNode(node.id);
  }, [openFlowNode]);

  const handleFlowClickCapture = useCallback((event: React.MouseEvent<HTMLDivElement>) => {
    const target = event.target;
    if (!(target instanceof HTMLElement)) {
      return;
    }
    if (target.closest(".react-flow__node[data-id]")) {
      return;
    }
    if (event.detail >= 2) {
      openRecentNodeClick(event);
    }
  }, [openRecentNodeClick]);

  const handleFlowDoubleClickCapture = useCallback((event: React.MouseEvent<HTMLDivElement>) => {
    const target = event.target;
    if (!(target instanceof HTMLElement)) {
      return;
    }
    const nodeElement = target.closest(".react-flow__node[data-id]") as HTMLElement | null;
    const nodeId = nodeElement?.dataset.id;
    if (!nodeId) {
      openRecentNodeClick(event);
      return;
    }
    event.preventDefault();
    event.stopPropagation();
    lastNodeClickRef.current = null;
    openFlowNode(nodeId);
  }, [openFlowNode, openRecentNodeClick]);

  const handleFlowPointerDownCapture = useCallback((event: React.PointerEvent<HTMLDivElement>) => {
    if (event.pointerType === "mouse") {
      return;
    }
    const target = event.target;
    if (!(target instanceof HTMLElement)) {
      return;
    }
    const nodeElement = target.closest(".react-flow__node[data-id]") as HTMLElement | null;
    const nodeId = nodeElement?.dataset.id;
    const node = nodeId ? flowNodes.find((candidate) => candidate.id === nodeId) : undefined;
    if (!node) {
      return;
    }
    interactionBoundary.touchLongPressStart({ pointerId: event.pointerId, nodeId: node.id, data: node.data, x: event.clientX, y: event.clientY });
  }, [flowNodes, interactionBoundary]);

  const handleFlowPointerMoveCapture = useCallback((event: React.PointerEvent<HTMLDivElement>) => {
    interactionBoundary.touchLongPressMove({ pointerId: event.pointerId, x: event.clientX, y: event.clientY });
  }, [interactionBoundary]);

  const handleFlowPointerEndCapture = useCallback((event: React.PointerEvent<HTMLDivElement>) => {
    interactionBoundary.touchLongPressEnd({ pointerId: event.pointerId });
  }, [interactionBoundary]);

  const handleNodeMouseEnter = useCallback<NodeMouseHandler<IdeaFlowNode>>((event, node) => {
    interactionBoundary.nodeEnter({ nodeId: node.id, data: node.data, x: event.clientX, y: event.clientY });
  }, [interactionBoundary]);

  const handleNodeMouseMove = useCallback<NodeMouseHandler<IdeaFlowNode>>((event, node) => {
    interactionBoundary.nodeMove({ nodeId: node.id, data: node.data, x: event.clientX, y: event.clientY });
  }, [interactionBoundary]);

  const handleNodeMouseLeave = useCallback<NodeMouseHandler<IdeaFlowNode>>((_event, node) => {
    interactionBoundary.nodeLeave({ nodeId: node.id });
  }, [interactionBoundary]);

  const requestLayout = useCallback(async (targetGraph: TopicGraphView, configuration: IdeaGraphLayoutConfiguration, force = false) => {
    if (!targetGraph.ok || targetGraph.error) {
      return;
    }
    const nodes = toFlowNodes(targetGraph);
    const edges = toFlowEdges(targetGraph);
    const layoutNodes = nodes.map((node) => ({ id: node.id, label: node.data.label }));
    const layoutEdges = edges.map((edge) => ({ id: edge.id, source: edge.source, target: edge.target, relationKind: String(edge.label || "") }));
    const fingerprint = layoutFingerprint(layoutNodes, layoutEdges, configuration);
    const contentSignature = fingerprint;
    if (!force && renderedGraphSignatureRef.current === contentSignature) {
      return;
    }
    const jobId = nextLayoutJobIdRef.current++;
    store.dispatch({ type: "layoutJobStarted", jobId, fingerprint });
    try {
      const result = await layoutWorker.run({ type: "layout", jobId, fingerprint, nodes: layoutNodes, edges: layoutEdges, configuration });
      if (!result.ok) {
        store.dispatch({ type: "layoutJobFailed", jobId, fingerprint, diagnostics: result.diagnostics.map((diagnostic) => diagnostic.message) });
        return;
      }
      const layoutedNodes = nodes.map((node) => ({ ...node, position: result.positions[node.id] || node.position }));
      renderedGraphSignatureRef.current = contentSignature;
      renderedGraphRevisionRef.current = targetGraph.index_revision || null;
      renderedGraphRef.current = targetGraph;
      setBaseEdges(edges);
      setBaseNodes(layoutedNodes);
      store.dispatch({
        type: "layoutJobSucceeded",
        jobId,
        fingerprint,
        positions: result.positions,
        durationMs: result.durationMs,
        configuration,
        diagnostics: result.diagnostics.map((diagnostic) => diagnostic.message),
      });
    } catch (error) {
      store.dispatch({ type: "layoutJobFailed", jobId, fingerprint, diagnostics: [error instanceof Error ? error.message : String(error)] });
    }
  }, [layoutWorker, store]);

  useEffect(() => {
    if (!topicId) {
      renderedGraphSignatureRef.current = null;
      renderedGraphRevisionRef.current = null;
      renderedGraphRef.current = null;
      setBaseEdges([]);
      setBaseNodes([]);
      store.dispatch({ type: "graphDataLoaded", nodeIds: [] });
      return;
    }
    if (portfolioGraph?.ok && !portfolioGraph.error) {
      store.dispatch({ type: "graphDataLoaded", nodeIds: portfolioGraph.nodes.map((node) => node.id) });
    }
  }, [portfolioGraph, store, topicId]);

  useEffect(() => {
    if (!filteredGraph?.ok || filteredGraph.error) {
      return;
    }
    const revision = filteredGraph.index_revision || null;
    if (filteredGraph.nodes.length === 0 && !searchText.trim() && renderedGraphRef.current && revision && revision === renderedGraphRevisionRef.current) {
      return;
    }
    void requestLayout(filteredGraph, appliedLayout);
  }, [appliedLayout, filteredGraph, requestLayout, searchText]);

  const previewLayout = useCallback(() => {
    if (filteredGraph?.ok && !filteredGraph.error) {
      void requestLayout(filteredGraph, layoutDraft, true);
    }
  }, [filteredGraph, layoutDraft, requestLayout]);

  const handleSelectionChange = useCallback(({ nodes }: { nodes: IdeaFlowNode[] }) => {
    store.dispatch({ type: "selectionReplaced", nodeIds: nodes.map((node) => node.id) });
  }, [store]);

  const handleMoveEnd = useCallback((_event: MouseEvent | TouchEvent | null, viewport: Viewport) => {
    setLowZoom((current) => viewport.zoom < 0.45 ? true : viewport.zoom > 0.5 ? false : current);
  }, []);

  useEffect(() => {
    if (!openIntent) {
      return;
    }
    openRecordFromNode(topicId || "", renderedGraphRef.current || filteredGraph, openIntent.nodeId);
    store.dispatch({ type: "openIntentConsumed", intentId: openIntent.intentId });
  }, [filteredGraph, openIntent, store, topicId]);

  const selectedIdeaNodes = useMemo(
    () => selectedNodeIds.map((nodeId) => graph.data?.nodes.find((node) => node.id === nodeId)).filter((node): node is TopicGraphNode => Boolean(node?.idea_id)),
    [graph.data?.nodes, selectedNodeIds],
  );
  const steeringTarget = steeringAction ? graph.data?.nodes.find((node) => node.idea_id === steeringAction.targetIdeaId) : undefined;
  const steeringReplacements = steeringAction?.action === "explore_instead" ? selectedIdeaNodes.filter((node) => node.idea_id !== steeringAction.targetIdeaId) : [];

  return (
    <section className="panel-body idea-graph-panel">
      <IdeaLineageSearch value={searchText} onChange={setSearchText} />
      <PortfolioControls graph={portfolioGraph} state={portfolioState} onChange={setPortfolioState} />
      {traversalView ? (
        <div className="idea-traversal-banner" role="status">
          <span>
            Showing {traversalView.direction} for {traversalView.rootIdeaIds.join(", ")}.
            {traversal.data && !traversal.data.topology_complete ? ` Incomplete at ${traversal.data.limiting_bounds.join(", ")}.` : ""}
          </span>
          <ToolbarButton type="button" onClick={() => setTraversalView(null)}>Return to portfolio</ToolbarButton>
        </div>
      ) : null}
      <IdeaGraphControls graph={focusedGraph} onPreview={previewLayout} store={store} />
      <ReactFlowProvider>
          <div
            className="flow-frame idea-lineage-flow"
            onClickCapture={handleFlowClickCapture}
            onDoubleClickCapture={handleFlowDoubleClickCapture}
            onPointerDownCapture={handleFlowPointerDownCapture}
            onPointerMoveCapture={handleFlowPointerMoveCapture}
            onPointerUpCapture={handleFlowPointerEndCapture}
            onPointerCancelCapture={handleFlowPointerEndCapture}
          >
            <ReactFlow
              colorMode={reactFlowColorMode}
              nodes={flowNodes}
              edges={flowEdges}
              fitView
              multiSelectionKeyCode={["Meta", "Control"]}
              nodeTypes={IDEA_GRAPH_NODE_TYPES}
              onlyRenderVisibleElements
              onMoveEnd={handleMoveEnd}
              onNodeClick={handleNodeClick}
              onNodeDoubleClick={handleNodeDoubleClick}
              onNodeMouseEnter={handleNodeMouseEnter}
              onNodeMouseMove={handleNodeMouseMove}
              onNodeMouseLeave={handleNodeMouseLeave}
              onPaneClick={() => store.dispatch({ type: "selectionCleared" })}
              onSelectionChange={handleSelectionChange}
              panOnDrag={[1, 2]}
              selectionMode={SelectionMode.Partial}
              selectionOnDrag
            >
              <FlowAutoFit edgeCount={flowEdges.length} layoutSignature={renderedGraphSignatureRef.current || ""} nodeCount={flowNodes.length} />
              <Background />
              <Controls />
            </ReactFlow>
            <IdeaNodeHoverCard
              preview={hoverPreview}
              topicId={topicId || ""}
              onPointerEnter={interactionBoundary.tooltipEnter}
              onPointerLeave={interactionBoundary.tooltipLeave}
            />
          </div>
        </ReactFlowProvider>
      <GraphSummary graph={filteredGraph} isLoading={graph.isLoading || backendFocusGraph.isLoading || traversal.isLoading} />
      {selectedNodeIds.length > 0 ? (
        <div className="selected-node-actions">
          <span>{selectedNodeIds.length} selected</span>
          <div className="idea-graph-selection-chips">
            {selectedNodeIds.map((nodeId) => {
              const sourceNode = graph.data?.nodes.find((node) => node.id === nodeId);
              return (
                <span className="idea-graph-selection-chip" key={nodeId}>
                  {String(sourceNode?.title || nodeId)}
                  <ToolbarButton aria-label={`Open ${String(sourceNode?.title || nodeId)}`} onClick={() => openFlowNode(nodeId)} type="button">Open</ToolbarButton>
                  {sourceNode?.idea_id ? <ToolbarButton aria-label={`Show ancestry for ${sourceNode.title}`} onClick={() => setTraversalView({ rootIdeaIds: [String(sourceNode.idea_id)], direction: "ancestors" })} type="button">Ancestry</ToolbarButton> : null}
                  {sourceNode?.idea_id ? <ToolbarButton aria-label={`Show descendants for ${sourceNode.title}`} onClick={() => setTraversalView({ rootIdeaIds: [String(sourceNode.idea_id)], direction: "descendants" })} type="button">Descendants</ToolbarButton> : null}
                  {sourceNode?.idea_id ? <ToolbarButton aria-label={`Review decisions for ${sourceNode.title}`} onClick={() => setDecisionIdeaId(String(sourceNode.idea_id))} type="button">Why?</ToolbarButton> : null}
                  {sourceNode?.idea_id && sourceNode.steering_eligibility?.eligible !== false ? <ToolbarButton aria-label={`Explore ${sourceNode.title}`} onClick={() => setSteeringAction({ action: "explore", targetIdeaId: String(sourceNode.idea_id) })} type="button">Explore</ToolbarButton> : null}
                  {sourceNode?.idea_id && selectedIdeaNodes.length > 1 && sourceNode.steering_eligibility?.eligible !== false ? <ToolbarButton aria-label={`Explore ${sourceNode.title} instead`} onClick={() => setSteeringAction({ action: "explore_instead", targetIdeaId: String(sourceNode.idea_id) })} type="button">Explore instead</ToolbarButton> : null}
                  <ToolbarButton aria-label={`Remove ${String(sourceNode?.title || nodeId)} from selection`} onClick={() => store.dispatch({ type: "selectionRemoved", nodeId })} type="button">×</ToolbarButton>
                </span>
              );
            })}
          </div>
        </div>
      ) : null}
      {decisionIdeaId ? <IdeaDecisionContextPanel response={decisionContext.data} isLoading={decisionContext.isLoading} error={decisionContext.error} onClose={() => setDecisionIdeaId(null)} /> : null}
      {steeringAction && steeringTarget ? (
        <IdeaSteeringDialog
          topicId={topicId || ""}
          action={steeringAction.action}
          target={steeringTarget}
          replacements={steeringReplacements}
          indexRevision={graph.data?.index_revision}
          onClose={() => setSteeringAction(null)}
          onAccepted={() => {
            void graph.refetch();
          }}
        />
      ) : null}
    </section>
  );
}

function IdeaLineageSearch({ value, onChange }: { value: string; onChange: (value: string) => void }) {
  return (
    <div className="filters idea-lineage-search">
      <Input aria-label="Search ideas" placeholder="Search ideas" type="search" value={value} onChange={(event) => onChange(event.target.value)} />
    </div>
  );
}

export function filterIdeaLineageGraphForSearch(graph: TopicGraphView | undefined, searchText: string): TopicGraphView | undefined {
  const queryTokens = normalizedSearchTokens(searchText);
  if (!graph || queryTokens.length === 0) {
    return graph;
  }
  const visibleNodeIds = new Set(
    graph.nodes
      .filter((node) => visibleLabelMatches(node, queryTokens))
      .map((node) => node.id),
  );
  const nodes = graph.nodes.filter((node) => visibleNodeIds.has(node.id));
  const nodeIds = new Set(nodes.map((node) => node.id));
  const edges = graph.edges.filter((edge) => nodeIds.has(edge.source) && nodeIds.has(edge.target));
  const groups = graph.groups
    .map((group) => ({ ...group, node_ids: group.node_ids.filter((nodeId) => nodeIds.has(nodeId)) }))
    .filter((group) => group.node_ids.length > 0);
  return {
    ...graph,
    nodes,
    edges,
    groups,
    facets: {
      ...graph.facets,
      idea_lineage_search: searchText.trim(),
    },
  };
}

function visibleLabelMatches(node: TopicGraphView["nodes"][number], queryTokens: string[]): boolean {
  const label = normalizeVisibleLabel(ideaNodeVisibleLabel(node));
  return queryTokens.every((token) => label.includes(token));
}

function normalizedSearchTokens(value: string): string[] {
  return normalizeVisibleLabel(value).split(" ").filter(Boolean);
}

function normalizeVisibleLabel(value: string): string {
  return value
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, " ")
    .trim();
}

const IdeaFlowCard = memo(function IdeaFlowCard({ data }: NodeProps<IdeaFlowNode>) {
  return (
    <div className="idea-flow-card">
      <Handle aria-hidden="true" position={Position.Left} type="target" />
      <span className="idea-flow-label">{data.label}</span>
      <span className="idea-flow-facets" aria-label="Idea states">
        <small title="Exploration state">{data.exploration_state || "unknown"}</small>
        <small title="Decision state">{data.decision_state || "unknown"}</small>
        <small title="Evidence state">{data.evidence_state || "unknown"}</small>
        {data.archive_state === "archived" ? <small title="Archive state">archived</small> : null}
        {data.visibility === "supporting" ? <small title="Visibility">supporting</small> : null}
      </span>
      <Handle aria-hidden="true" position={Position.Right} type="source" />
    </div>
  );
});

const IDEA_GRAPH_NODE_TYPES = { idea: IdeaFlowCard };

function FlowAutoFit({ edgeCount, layoutSignature, nodeCount }: { edgeCount: number; layoutSignature: string; nodeCount: number }) {
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
  }, [edgeCount, fitView, layoutSignature, nodeCount]);
  return null;
}

export function buildIdeaNodeHoverMarkdown(data: IdeaFlowNodeData): string {
  const title = String(data.title || data.label || "Idea");
  const lines = [`### ${title}`];
  const summary = typeof data.summary === "string" ? data.summary.trim() : "";
  if (summary) {
    lines.push("", summary);
  }
  const facts = [
    ["Exploration", data.exploration_state],
    ["Decision", data.decision_state],
    ["Evidence", data.evidence_state],
    ["Archive", data.archive_state],
    ["Visibility", data.visibility],
    ["Compatibility status", data.status],
    ["Kind", data.material_kind],
    ["Idea", data.idea_id],
    ["Record", data.record_id],
    ["Producer", data.producer || data.skill],
  ].filter((entry): entry is [string, string] => typeof entry[1] === "string" && entry[1].trim().length > 0);
  if (facts.length) {
    lines.push("", ...facts.map(([label, value]) => `- **${label}:** ${value}`));
  }
  return lines.join("\n");
}

function IdeaNodeHoverCard({
  preview,
  topicId,
  onPointerEnter,
  onPointerLeave,
}: {
  preview: ReturnType<typeof visibleHoverPreview>;
  topicId: string;
  onPointerEnter: () => void;
  onPointerLeave: () => void;
}) {
  const ideaId = typeof preview?.data.idea_id === "string" && preview.data.idea_id.trim() ? preview.data.idea_id : "";
  const detail = useQuery({
    queryKey: ["topic", topicId, "idea-lineage", "idea-hover-preview", ideaId],
    queryFn: () => getIdeaDetail(topicId, ideaId, { includeSourceJson: true }),
    enabled: Boolean(preview && topicId && ideaId),
    staleTime: 30_000,
  });
  const markdown = useMemo(() => {
    if (!preview) {
      return "";
    }
    const ideaContent = detail.data?.idea_content ?? detail.data?.source?.source_json;
    const previewSource = ideaContent === undefined && detail.data?.idea ? { idea: detail.data.idea, latest_realization: detail.data.latest_realization } : ideaContent;
    if (previewSource !== undefined) {
      return buildJsonMarkdownPreview(previewSource).markdown;
    }
    const fallback = buildIdeaNodeHoverMarkdown(preview.data);
    if (detail.error) {
      return `${fallback}\n\n_Preview detail failed to load. Showing graph summary._`;
    }
    return fallback;
  }, [detail.data, detail.error, preview]);
  if (!preview) {
    return null;
  }
  const loading = Boolean(ideaId && detail.isPending && !detail.data && !detail.error);
  const viewportWidth = typeof window === "undefined" ? 1024 : window.innerWidth;
  const viewportHeight = typeof window === "undefined" ? 768 : window.innerHeight;
  const left = Math.max(16, Math.min(preview.x + 16, viewportWidth - 440));
  const top = Math.max(16, Math.min(preview.y + 18, viewportHeight - 340));
  const stopGraphInteraction = (event: React.SyntheticEvent<HTMLDivElement>) => {
    event.stopPropagation();
  };
  return (
    <div
      className="idea-node-hover-card"
      style={{ left, top }}
      role="tooltip"
      onPointerEnter={onPointerEnter}
      onPointerLeave={onPointerLeave}
      onMouseEnter={onPointerEnter}
      onMouseLeave={onPointerLeave}
      onPointerDown={stopGraphInteraction}
      onWheel={stopGraphInteraction}
    >
      {loading ? (
        <div className="idea-node-hover-loading">
          <LoaderCircle aria-hidden="true" />
          <span>Loading preview</span>
        </div>
      ) : (
        <React.Suspense
          fallback={(
            <div className="idea-node-hover-loading">
              <LoaderCircle aria-hidden="true" />
              <span>Loading preview</span>
            </div>
          )}
        >
          <LazyIdeaHoverMarkdownView content={markdown} />
        </React.Suspense>
      )}
    </div>
  );
}

function asGraphScope(value: string | null | undefined, fallback: GraphScope): GraphScope {
  return isGraphScope(value) ? value : fallback;
}

function sameHoverPreview(left: ReturnType<typeof visibleHoverPreview>, right: ReturnType<typeof visibleHoverPreview>) {
  return left?.nodeId === right?.nodeId && left?.x === right?.x && left?.y === right?.y && left?.data === right?.data;
}

function sameOpenIntent(left: IdeaLineageOpenIntent | null, right: IdeaLineageOpenIntent | null) {
  return left?.intentId === right?.intentId && left?.nodeId === right?.nodeId;
}

function sameStrings(left: string[], right: string[]) {
  return left.length === right.length && left.every((value, index) => value === right[index]);
}

function projectGraphToIdeaIds(graph: TopicGraphView | undefined, ideaIds: string[]): TopicGraphView | undefined {
  if (!graph) {
    return graph;
  }
  const acceptedIdeas = new Set(ideaIds);
  const nodes = graph.nodes.filter((node) => node.idea_id && acceptedIdeas.has(String(node.idea_id)));
  const nodeIds = new Set(nodes.map((node) => node.id));
  return {
    ...graph,
    nodes,
    edges: graph.edges.filter((edge) => nodeIds.has(edge.source) && nodeIds.has(edge.target)),
    groups: graph.groups
      .map((group) => ({ ...group, node_ids: group.node_ids.filter((nodeId) => nodeIds.has(nodeId)) }))
      .filter((group) => group.node_ids.length > 0),
  };
}
