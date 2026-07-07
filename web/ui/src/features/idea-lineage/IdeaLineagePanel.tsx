import { Background, Controls, ReactFlow, ReactFlowProvider, useReactFlow, type ColorMode, type NodeMouseHandler } from "@xyflow/react";
import { useQuery } from "@tanstack/react-query";
import { LoaderCircle } from "lucide-react";
import React, { useCallback, useEffect, useId, useMemo, useRef, useState } from "react";
import { getIdeaDetail, getTopicGraph, type GraphFilters } from "../../api";
import { GraphFiltersBar, GraphSummary } from "../graph/GraphPanels";
import { openRecordFromNode } from "../graph/open-record";
import { SigmaGraph } from "../graph/SigmaGraph";
import { graphContentSignature, layoutFlowGraph, requestedRenderer, selectRenderer, toFlowEdges, toFlowNodes, type IdeaFlowNodeData } from "../../graph-utils";
import { buildJsonMarkdownPreview } from "../../markdown-doc";
import { MarkdownView } from "../../markdown-view";
import { useGuiTheme } from "../../theme-provider";
import type { GraphScope, TopicGraphView } from "../../types";
import { DEFAULT_HOVER_PREVIEW_DELAY_MS, useGuiSettings } from "../../ui-settings";
import { isGraphScope } from "../../workbench-history";
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

const NODE_DOUBLE_CLICK_MS = 500;
const NODE_DOUBLE_CLICK_DISTANCE_PX = 72;
const HOVER_PREVIEW_CLOSE_DELAY_MS = 500;
const TOUCH_LONG_PRESS_MOVE_TOLERANCE_PX = 14;

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
  const [filters, setFilters] = useState<GraphFilters>({ includeSecondary: false });
  const [baseNodes, setBaseNodes] = useState<IdeaFlowNode[]>([]);
  const [baseEdges, setBaseEdges] = useState<ReturnType<typeof toFlowEdges>>([]);
  const selectedNodeId = useStoreSelector(store, (state) => state.selectedNodeId);
  const hoverPreview = useStoreSelector(store, visibleHoverPreview, sameHoverPreview);
  const openIntent = useStoreSelector(store, (state) => state.openIntent, sameOpenIntent);
  const flowNodes = useMemo(() => selectIdeaFlowNodes(baseNodes, baseEdges, selectedNodeId), [baseEdges, baseNodes, selectedNodeId]);
  const flowEdges = useMemo(() => selectIdeaFlowEdges(baseEdges, selectedNodeId), [baseEdges, selectedNodeId]);
  const selectedFlowNode = useMemo(() => flowNodes.find((node) => node.selected), [flowNodes]);
  const hoverPreviewDelayMsRef = useRef(hoverPreviewDelayMs);
  const lastNodeClickRef = useRef<{ nodeId: string; at: number; x: number; y: number } | null>(null);
  const renderedGraphSignatureRef = useRef<string | null>(null);
  const renderedGraphRevisionRef = useRef<string | null>(null);
  const renderedGraphRef = useRef<TopicGraphView | null>(null);
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
  const graph = useQuery({
    queryKey: ["topic", topicId, "graph", selectedGraphScope, requestedRenderer(selectedGraphScope), filters],
    queryFn: () => getTopicGraph(topicId || "", selectedGraphScope, requestedRenderer(selectedGraphScope), filters),
    enabled: Boolean(topicId),
  });

  useEffect(() => () => interactionBoundary.dispose(), [interactionBoundary]);

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
    interactionBoundary.nodeClick({ nodeId: node.id });
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

  const openSelectedFlowNode = useCallback(() => {
    if (selectedFlowNode) {
      openFlowNode(selectedFlowNode.id);
    }
  }, [openFlowNode, selectedFlowNode]);

  const handleNodeMouseEnter = useCallback<NodeMouseHandler<IdeaFlowNode>>((event, node) => {
    interactionBoundary.nodeEnter({ nodeId: node.id, data: node.data, x: event.clientX, y: event.clientY });
  }, [interactionBoundary]);

  const handleNodeMouseMove = useCallback<NodeMouseHandler<IdeaFlowNode>>((event, node) => {
    interactionBoundary.nodeMove({ nodeId: node.id, data: node.data, x: event.clientX, y: event.clientY });
  }, [interactionBoundary]);

  const handleNodeMouseLeave = useCallback<NodeMouseHandler<IdeaFlowNode>>((_event, node) => {
    interactionBoundary.nodeLeave({ nodeId: node.id });
  }, [interactionBoundary]);

  useEffect(() => {
    let cancelled = false;
    if (!topicId) {
      renderedGraphSignatureRef.current = null;
      renderedGraphRevisionRef.current = null;
      renderedGraphRef.current = null;
      setBaseEdges([]);
      setBaseNodes([]);
      store.dispatch({ type: "graphDataLoaded", nodeIds: [], selectedNodeId: null });
      return () => {
        cancelled = true;
      };
    }
    if (!graph.data) {
      return () => {
        cancelled = true;
      };
    }
    if (!graph.data.ok || graph.data.error) {
      if (renderedGraphRef.current) {
        return () => {
          cancelled = true;
        };
      }
      renderedGraphSignatureRef.current = null;
      renderedGraphRevisionRef.current = null;
      setBaseEdges([]);
      setBaseNodes([]);
      store.dispatch({ type: "graphDataLoaded", nodeIds: [], selectedNodeId: null });
      return () => {
        cancelled = true;
      };
    }
    const revision = graph.data.index_revision || null;
    const signature = graphContentSignature(graph.data);
    if (signature === renderedGraphSignatureRef.current) {
      return () => {
        cancelled = true;
      };
    }
    const nodes = toFlowNodes(graph.data);
    const edges = toFlowEdges(graph.data);
    if (nodes.length === 0 && renderedGraphRef.current && revision && revision === renderedGraphRevisionRef.current) {
      return () => {
        cancelled = true;
      };
    }
    layoutFlowGraph(nodes, edges).then((layouted) => {
      if (cancelled) {
        return;
      }
      renderedGraphSignatureRef.current = signature;
      renderedGraphRevisionRef.current = revision;
      renderedGraphRef.current = graph.data || null;
      setBaseEdges(edges);
      setBaseNodes(layouted);
      store.dispatch({
        type: "graphDataLoaded",
        nodeIds: nodes.map((node) => node.id),
      });
    });
    return () => {
      cancelled = true;
    };
  }, [graph.data, store, topicId]);

  useEffect(() => {
    if (!openIntent) {
      return;
    }
    openRecordFromNode(topicId || "", renderedGraphRef.current || graph.data, openIntent.nodeId);
    store.dispatch({ type: "openIntentConsumed", intentId: openIntent.intentId });
  }, [graph.data, openIntent, store, topicId]);

  return (
    <section className="panel-body">
      <GraphFiltersBar filters={filters} onChange={setFilters} />
      {graph.data && selectRenderer(selectedGraphScope, graph.data.renderer_hint, graph.data.nodes.length) === "sigma" ? (
        <SigmaGraph graph={graph.data} />
      ) : (
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
              onNodeClick={handleNodeClick}
              onNodeDoubleClick={handleNodeDoubleClick}
              onNodeMouseEnter={handleNodeMouseEnter}
              onNodeMouseMove={handleNodeMouseMove}
              onNodeMouseLeave={handleNodeMouseLeave}
            >
              <FlowAutoFit edgeCount={flowEdges.length} nodeCount={flowNodes.length} />
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
      )}
      <GraphSummary graph={graph.data} isLoading={graph.isLoading} />
      {selectedFlowNode ? (
        <div className="selected-node-actions">
          <span>Selected: {String(selectedFlowNode.data.title || selectedFlowNode.id)}</span>
          <ToolbarButton type="button" onClick={openSelectedFlowNode}>
            Open
          </ToolbarButton>
        </div>
      ) : null}
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

export function buildIdeaNodeHoverMarkdown(data: IdeaFlowNodeData): string {
  const title = String(data.title || data.label || "Idea");
  const lines = [`### ${title}`];
  const oneLiner = typeof data.one_liner === "string" ? data.one_liner.trim() : "";
  const summary = typeof data.summary === "string" ? data.summary.trim() : "";
  if (oneLiner) {
    lines.push("", oneLiner);
  }
  if (summary && summary !== oneLiner) {
    lines.push("", summary);
  }
  const facts = [
    ["Status", data.status],
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
        <MarkdownView content={markdown} />
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
