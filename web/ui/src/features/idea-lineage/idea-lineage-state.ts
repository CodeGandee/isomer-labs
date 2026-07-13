import type { Edge, Node } from "@xyflow/react";
import type { IdeaFlowNodeData } from "../../graph-utils";
import { createProjectWebStore, PanelScopedStoreRegistry, type ProjectWebStore } from "../../state/observable-store";
import { DEFAULT_IDEA_GRAPH_FOCUS, type IdeaGraphFocusConfiguration } from "./idea-graph-focus";
import { DEFAULT_LAYOUT_CONFIGURATIONS, cloneLayoutConfiguration, type IdeaGraphLayoutConfiguration } from "./layout-registry";

export type IdeaFlowNode = Node<IdeaFlowNodeData>;

export type IdeaNodeHoverPreview = {
  nodeId: string;
  data: IdeaFlowNodeData;
  x: number;
  y: number;
};

export type IdeaLineageHoverSessionId = number;

export type TouchLongPressState = {
  pointerId: number;
  nodeId: string;
  data: IdeaFlowNodeData;
  x: number;
  y: number;
} | null;

export type IdeaLineageHoverState =
  | { status: "idle" }
  | { status: "pending"; sessionId: IdeaLineageHoverSessionId; preview: IdeaNodeHoverPreview }
  | { status: "visible"; sessionId: IdeaLineageHoverSessionId; preview: IdeaNodeHoverPreview };

export type IdeaLineageOpenIntent = {
  intentId: number;
  nodeId: string;
};

export type IdeaLineageState = {
  selectedNodeIds: string[];
  /** Compatibility alias for consumers that only display the primary selection. */
  selectedNodeId: string | null;
  focus: IdeaGraphFocusConfiguration;
  layoutDraft: IdeaGraphLayoutConfiguration;
  appliedLayout: IdeaGraphLayoutConfiguration;
  appliedPresetId: string | null;
  positions: Record<string, { x: number; y: number }>;
  layoutJob: {
    status: "idle" | "running" | "succeeded" | "failed";
    jobId: number;
    fingerprint: string | null;
    durationMs: number | null;
    diagnostics: string[];
  };
  hover: IdeaLineageHoverState;
  touchLongPress: TouchLongPressState;
  openIntent: IdeaLineageOpenIntent | null;
  nextOpenIntentId: number;
};

export type IdeaLineageAction =
  | { type: "graphDataLoaded"; nodeIds: string[]; selectedNodeId?: string | null }
  | { type: "nodeSelected"; nodeId: string }
  | { type: "selectionReplaced"; nodeIds: string[] }
  | { type: "selectionToggled"; nodeId: string }
  | { type: "selectionRemoved"; nodeId: string }
  | { type: "selectionCleared" }
  | { type: "focusChanged"; focus: Partial<IdeaGraphFocusConfiguration> }
  | { type: "focusExited" }
  | { type: "layoutDraftChanged"; configuration: IdeaGraphLayoutConfiguration }
  | { type: "layoutDraftReverted" }
  | { type: "layoutPresetApplied"; presetId: string | null; configuration: IdeaGraphLayoutConfiguration }
  | { type: "layoutJobStarted"; jobId: number; fingerprint: string }
  | { type: "layoutJobSucceeded"; jobId: number; fingerprint: string; positions: Record<string, { x: number; y: number }>; durationMs: number; configuration: IdeaGraphLayoutConfiguration; diagnostics?: string[] }
  | { type: "layoutJobFailed"; jobId: number; fingerprint: string; diagnostics: string[] }
  | { type: "nodeOpened"; nodeId: string }
  | { type: "openIntentConsumed"; intentId: number }
  | { type: "hoverStarted"; sessionId: IdeaLineageHoverSessionId; preview: IdeaNodeHoverPreview }
  | { type: "hoverMoved"; sessionId: IdeaLineageHoverSessionId; preview: IdeaNodeHoverPreview }
  | { type: "hoverDelayElapsed"; sessionId: IdeaLineageHoverSessionId }
  | { type: "hoverClosed"; sessionId?: IdeaLineageHoverSessionId }
  | { type: "touchLongPressStarted"; pointerId: number; nodeId: string; data: IdeaFlowNodeData; x: number; y: number }
  | { type: "touchLongPressCanceled"; pointerId?: number }
  | { type: "touchLongPressElapsed"; pointerId: number; sessionId: IdeaLineageHoverSessionId };

export type IdeaLineageStore = ProjectWebStore<IdeaLineageState, IdeaLineageAction>;

export const ideaLineageStoreRegistry = new PanelScopedStoreRegistry<IdeaLineageStore>();

export const initialIdeaLineageState: IdeaLineageState = {
  selectedNodeIds: [],
  selectedNodeId: null,
  focus: { ...DEFAULT_IDEA_GRAPH_FOCUS },
  layoutDraft: cloneLayoutConfiguration(DEFAULT_LAYOUT_CONFIGURATIONS.layered),
  appliedLayout: cloneLayoutConfiguration(DEFAULT_LAYOUT_CONFIGURATIONS.layered),
  appliedPresetId: "builtin-layered",
  positions: {},
  layoutJob: { status: "idle", jobId: 0, fingerprint: null, durationMs: null, diagnostics: [] },
  hover: { status: "idle" },
  touchLongPress: null,
  openIntent: null,
  nextOpenIntentId: 1,
};

export function createIdeaLineageStore(initialState: IdeaLineageState = initialIdeaLineageState): IdeaLineageStore {
  return createProjectWebStore(initialState, ideaLineageReducer);
}

export function ideaLineageReducer(state: IdeaLineageState, action: IdeaLineageAction): IdeaLineageState {
  if (action.type === "graphDataLoaded") {
    const available = new Set(action.nodeIds);
    const selectedNodeIds = state.selectedNodeIds.filter((nodeId) => available.has(nodeId));
    if (selectedNodeIds.length === 0 && action.selectedNodeId && available.has(action.selectedNodeId)) {
      selectedNodeIds.push(action.selectedNodeId);
    }
    const selectedNodeId = selectedNodeIds[0] || null;
    const positions = Object.fromEntries(Object.entries(state.positions).filter(([nodeId]) => available.has(nodeId)));
    if (sameStrings(selectedNodeIds, state.selectedNodeIds) && selectedNodeId === state.selectedNodeId && Object.keys(positions).length === Object.keys(state.positions).length) {
      return state;
    }
    return { ...state, selectedNodeIds, selectedNodeId, positions };
  }
  if (action.type === "nodeSelected") {
    return sameStrings(state.selectedNodeIds, [action.nodeId]) ? state : { ...state, selectedNodeIds: [action.nodeId], selectedNodeId: action.nodeId };
  }
  if (action.type === "selectionReplaced") {
    const selectedNodeIds = [...new Set(action.nodeIds.filter(Boolean))];
    return sameStrings(state.selectedNodeIds, selectedNodeIds) ? state : { ...state, selectedNodeIds, selectedNodeId: selectedNodeIds[0] || null };
  }
  if (action.type === "selectionToggled") {
    const selectedNodeIds = state.selectedNodeIds.includes(action.nodeId)
      ? state.selectedNodeIds.filter((nodeId) => nodeId !== action.nodeId)
      : [...state.selectedNodeIds, action.nodeId];
    return { ...state, selectedNodeIds, selectedNodeId: selectedNodeIds[0] || null };
  }
  if (action.type === "selectionRemoved") {
    if (!state.selectedNodeIds.includes(action.nodeId)) {
      return state;
    }
    const selectedNodeIds = state.selectedNodeIds.filter((nodeId) => nodeId !== action.nodeId);
    return { ...state, selectedNodeIds, selectedNodeId: selectedNodeIds[0] || null };
  }
  if (action.type === "selectionCleared") {
    return state.selectedNodeIds.length === 0 ? state : { ...state, selectedNodeIds: [], selectedNodeId: null };
  }
  if (action.type === "focusChanged") {
    const focus = { ...state.focus, ...action.focus };
    return { ...state, focus };
  }
  if (action.type === "focusExited") {
    return state.focus.enabled ? { ...state, focus: { ...state.focus, enabled: false } } : state;
  }
  if (action.type === "layoutDraftChanged") {
    return { ...state, layoutDraft: cloneLayoutConfiguration(action.configuration) };
  }
  if (action.type === "layoutDraftReverted") {
    return { ...state, layoutDraft: cloneLayoutConfiguration(state.appliedLayout) };
  }
  if (action.type === "layoutPresetApplied") {
    return {
      ...state,
      appliedPresetId: action.presetId,
      layoutDraft: cloneLayoutConfiguration(action.configuration),
    };
  }
  if (action.type === "layoutJobStarted") {
    return { ...state, layoutJob: { status: "running", jobId: action.jobId, fingerprint: action.fingerprint, durationMs: null, diagnostics: [] } };
  }
  if (action.type === "layoutJobSucceeded") {
    if (state.layoutJob.jobId !== action.jobId || state.layoutJob.fingerprint !== action.fingerprint) {
      return state;
    }
    return {
      ...state,
      positions: action.positions,
      appliedLayout: cloneLayoutConfiguration(action.configuration),
      layoutJob: { status: "succeeded", jobId: action.jobId, fingerprint: action.fingerprint, durationMs: action.durationMs, diagnostics: action.diagnostics || [] },
    };
  }
  if (action.type === "layoutJobFailed") {
    if (state.layoutJob.jobId !== action.jobId || state.layoutJob.fingerprint !== action.fingerprint) {
      return state;
    }
    return { ...state, layoutJob: { status: "failed", jobId: action.jobId, fingerprint: action.fingerprint, durationMs: null, diagnostics: action.diagnostics } };
  }
  if (action.type === "nodeOpened") {
    const selectedNodeIds = state.selectedNodeIds.length > 0 ? state.selectedNodeIds : [action.nodeId];
    return {
      ...state,
      selectedNodeIds,
      selectedNodeId: selectedNodeIds[0] || null,
      hover: { status: "idle" },
      touchLongPress: null,
      openIntent: { intentId: state.nextOpenIntentId, nodeId: action.nodeId },
      nextOpenIntentId: state.nextOpenIntentId + 1,
    };
  }
  if (action.type === "openIntentConsumed") {
    if (state.openIntent?.intentId !== action.intentId) {
      return state;
    }
    return { ...state, openIntent: null };
  }
  if (action.type === "hoverStarted") {
    return { ...state, hover: { status: "pending", sessionId: action.sessionId, preview: action.preview } };
  }
  if (action.type === "hoverMoved") {
    if (state.hover.status !== "pending" || state.hover.sessionId !== action.sessionId || state.hover.preview.nodeId !== action.preview.nodeId) {
      return state;
    }
    return { ...state, hover: { status: "pending", sessionId: state.hover.sessionId, preview: action.preview } };
  }
  if (action.type === "hoverDelayElapsed") {
    if (state.hover.status !== "pending" || state.hover.sessionId !== action.sessionId) {
      return state;
    }
    return { ...state, hover: { status: "visible", sessionId: state.hover.sessionId, preview: state.hover.preview } };
  }
  if (action.type === "hoverClosed") {
    if (action.sessionId !== undefined && (state.hover.status === "idle" || state.hover.sessionId !== action.sessionId)) {
      return state;
    }
    if (state.hover.status === "idle" && !state.touchLongPress) {
      return state;
    }
    return { ...state, hover: { status: "idle" }, touchLongPress: null };
  }
  if (action.type === "touchLongPressStarted") {
    return {
      ...state,
      touchLongPress: {
        pointerId: action.pointerId,
        nodeId: action.nodeId,
        data: action.data,
        x: action.x,
        y: action.y,
      },
    };
  }
  if (action.type === "touchLongPressCanceled") {
    if (!state.touchLongPress) {
      return state;
    }
    if (action.pointerId !== undefined && state.touchLongPress.pointerId !== action.pointerId) {
      return state;
    }
    return { ...state, touchLongPress: null };
  }
  if (action.type === "touchLongPressElapsed") {
    const pending = state.touchLongPress;
    if (!pending || pending.pointerId !== action.pointerId) {
      return state;
    }
    return {
      ...state,
      touchLongPress: null,
      hover: {
        status: "visible",
        sessionId: action.sessionId,
        preview: {
          nodeId: pending.nodeId,
          data: pending.data,
          x: pending.x,
          y: pending.y,
        },
      },
    };
  }
  return state;
}

const LINEAGE_NODE_STATE_CLASSES = ["ui-selected", "lineage-parent", "lineage-child"];
const LINEAGE_EDGE_STATE_CLASSES = ["lineage-incoming", "lineage-outgoing"];

export type IdeaLineageNeighborhood = {
  selectedNodeIds: string[];
  selectedNodeId: string | null;
  parentNodeIds: Set<string>;
  childNodeIds: Set<string>;
  incomingEdgeIds: Set<string>;
  outgoingEdgeIds: Set<string>;
};

export function selectIdeaLineageNeighborhood(edges: Edge[], selection: string | null | string[]): IdeaLineageNeighborhood {
  const selectedNodeIds = Array.isArray(selection) ? selection : selection ? [selection] : [];
  const selected = new Set(selectedNodeIds);
  const selectedNodeId = selectedNodeIds[0] || null;
  const parentNodeIds = new Set<string>();
  const childNodeIds = new Set<string>();
  const incomingEdgeIds = new Set<string>();
  const outgoingEdgeIds = new Set<string>();
  if (!selectedNodeId) {
    return { selectedNodeIds, selectedNodeId, parentNodeIds, childNodeIds, incomingEdgeIds, outgoingEdgeIds };
  }
  for (const edge of edges) {
    if (selected.has(edge.target)) {
      parentNodeIds.add(edge.source);
      incomingEdgeIds.add(edge.id);
    }
    if (selected.has(edge.source)) {
      childNodeIds.add(edge.target);
      outgoingEdgeIds.add(edge.id);
    }
  }
  return { selectedNodeIds, selectedNodeId, parentNodeIds, childNodeIds, incomingEdgeIds, outgoingEdgeIds };
}

export function selectIdeaFlowNodes(nodes: IdeaFlowNode[], edges: Edge[], selection: string | null | string[]): IdeaFlowNode[] {
  const neighborhood = selectIdeaLineageNeighborhood(edges, selection);
  const selectedNodeIds = new Set(neighborhood.selectedNodeIds);
  let changed = false;
  const nextNodes = nodes.map((node) => {
    const selected = selectedNodeIds.has(node.id);
    const className = withControlledClasses(node.className, LINEAGE_NODE_STATE_CLASSES, lineageNodeClassState(node.id, neighborhood));
    if (Boolean(node.selected) === selected && node.className === className) {
      return node;
    }
    changed = true;
    return { ...node, selected: selected || undefined, className };
  });
  return changed ? nextNodes : nodes;
}

export function selectIdeaFlowEdges(edges: Edge[], selection: string | null | string[]): Edge[] {
  const neighborhood = selectIdeaLineageNeighborhood(edges, selection);
  let changed = false;
  const nextEdges = edges.map((edge) => {
    const className = withControlledClasses(edge.className, LINEAGE_EDGE_STATE_CLASSES, lineageEdgeClassState(edge, neighborhood));
    if (edge.className === className) {
      return edge;
    }
    changed = true;
    return { ...edge, className };
  });
  return changed ? nextEdges : edges;
}

export function visibleHoverPreview(state: IdeaLineageState): IdeaNodeHoverPreview | null {
  return state.hover.status === "visible" ? state.hover.preview : null;
}

function lineageNodeClassState(nodeId: string, neighborhood: IdeaLineageNeighborhood) {
  if (!neighborhood.selectedNodeId) {
    return [];
  }
  return [
    neighborhood.selectedNodeIds.includes(nodeId) ? "ui-selected" : "",
    neighborhood.parentNodeIds.has(nodeId) ? "lineage-parent" : "",
    neighborhood.childNodeIds.has(nodeId) ? "lineage-child" : "",
  ].filter(Boolean);
}

function lineageEdgeClassState(edge: Edge, neighborhood: IdeaLineageNeighborhood) {
  if (!neighborhood.selectedNodeId) {
    return [];
  }
  return [
    neighborhood.incomingEdgeIds.has(edge.id) ? "lineage-incoming" : "",
    neighborhood.outgoingEdgeIds.has(edge.id) ? "lineage-outgoing" : "",
  ].filter(Boolean);
}

function withControlledClasses(className: string | undefined, controlledClasses: string[], enabledClasses: string[]) {
  const tokens = new Set((className || "").split(/\s+/).filter(Boolean));
  for (const token of controlledClasses) {
    tokens.delete(token);
  }
  for (const token of enabledClasses) {
    tokens.add(token);
  }
  const nextClassName = Array.from(tokens).join(" ");
  return nextClassName || undefined;
}

function sameStrings(left: string[], right: string[]) {
  return left.length === right.length && left.every((value, index) => value === right[index]);
}
