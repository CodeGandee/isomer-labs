import type { Edge, Node } from "@xyflow/react";
import type { IdeaFlowNodeData } from "../../graph-utils";
import { createProjectWebStore, PanelScopedStoreRegistry, type ProjectWebStore } from "../../state/observable-store";

export type IdeaFlowNode = Node<IdeaFlowNodeData>;

export type IdeaNodeHoverPreview = {
  nodeId: string;
  data: IdeaFlowNodeData;
  x: number;
  y: number;
};

export type TouchLongPressState = {
  pointerId: number;
  nodeId: string;
  data: IdeaFlowNodeData;
  x: number;
  y: number;
} | null;

export type IdeaLineageHoverState =
  | { status: "idle" }
  | { status: "pending"; preview: IdeaNodeHoverPreview }
  | { status: "visible"; preview: IdeaNodeHoverPreview };

export type IdeaLineageOpenIntent = {
  intentId: number;
  nodeId: string;
};

export type IdeaLineageState = {
  selectedNodeId: string | null;
  hover: IdeaLineageHoverState;
  touchLongPress: TouchLongPressState;
  openIntent: IdeaLineageOpenIntent | null;
  nextOpenIntentId: number;
};

export type IdeaLineageAction =
  | { type: "graphDataLoaded"; nodeIds: string[]; selectedNodeId?: string | null }
  | { type: "nodeSelected"; nodeId: string }
  | { type: "nodeOpened"; nodeId: string }
  | { type: "openIntentConsumed"; intentId: number }
  | { type: "hoverStarted"; preview: IdeaNodeHoverPreview }
  | { type: "hoverMoved"; preview: IdeaNodeHoverPreview }
  | { type: "hoverDelayElapsed" }
  | { type: "hoverClosed" }
  | { type: "touchLongPressStarted"; pointerId: number; nodeId: string; data: IdeaFlowNodeData; x: number; y: number }
  | { type: "touchLongPressCanceled"; pointerId?: number }
  | { type: "touchLongPressElapsed"; pointerId: number };

export type IdeaLineageStore = ProjectWebStore<IdeaLineageState, IdeaLineageAction>;

export const ideaLineageStoreRegistry = new PanelScopedStoreRegistry<IdeaLineageStore>();

export const initialIdeaLineageState: IdeaLineageState = {
  selectedNodeId: null,
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
    const selectedNodeId = state.selectedNodeId && action.nodeIds.includes(state.selectedNodeId) ? state.selectedNodeId : action.selectedNodeId || null;
    return selectedNodeId === state.selectedNodeId ? state : { ...state, selectedNodeId };
  }
  if (action.type === "nodeSelected") {
    return state.selectedNodeId === action.nodeId ? state : { ...state, selectedNodeId: action.nodeId };
  }
  if (action.type === "nodeOpened") {
    return {
      ...state,
      selectedNodeId: action.nodeId,
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
    return { ...state, hover: { status: "pending", preview: action.preview } };
  }
  if (action.type === "hoverMoved") {
    if (state.hover.status !== "pending" || state.hover.preview.nodeId !== action.preview.nodeId) {
      return state;
    }
    return { ...state, hover: { status: "pending", preview: action.preview } };
  }
  if (action.type === "hoverDelayElapsed") {
    if (state.hover.status !== "pending") {
      return state;
    }
    return { ...state, hover: { status: "visible", preview: state.hover.preview } };
  }
  if (action.type === "hoverClosed") {
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

const LINEAGE_NODE_STATE_CLASSES = ["selected", "lineage-parent", "lineage-child"];
const LINEAGE_EDGE_STATE_CLASSES = ["lineage-incoming", "lineage-outgoing"];

export type IdeaLineageNeighborhood = {
  selectedNodeId: string | null;
  parentNodeIds: Set<string>;
  childNodeIds: Set<string>;
  incomingEdgeIds: Set<string>;
  outgoingEdgeIds: Set<string>;
};

export function selectIdeaLineageNeighborhood(edges: Edge[], selectedNodeId: string | null): IdeaLineageNeighborhood {
  const parentNodeIds = new Set<string>();
  const childNodeIds = new Set<string>();
  const incomingEdgeIds = new Set<string>();
  const outgoingEdgeIds = new Set<string>();
  if (!selectedNodeId) {
    return { selectedNodeId, parentNodeIds, childNodeIds, incomingEdgeIds, outgoingEdgeIds };
  }
  for (const edge of edges) {
    if (edge.target === selectedNodeId) {
      parentNodeIds.add(edge.source);
      incomingEdgeIds.add(edge.id);
    }
    if (edge.source === selectedNodeId) {
      childNodeIds.add(edge.target);
      outgoingEdgeIds.add(edge.id);
    }
  }
  return { selectedNodeId, parentNodeIds, childNodeIds, incomingEdgeIds, outgoingEdgeIds };
}

export function selectIdeaFlowNodes(nodes: IdeaFlowNode[], edges: Edge[], selectedNodeId: string | null): IdeaFlowNode[] {
  const neighborhood = selectIdeaLineageNeighborhood(edges, selectedNodeId);
  let changed = false;
  const nextNodes = nodes.map((node) => {
    const selected = node.id === selectedNodeId;
    const className = withControlledClasses(node.className, LINEAGE_NODE_STATE_CLASSES, lineageNodeClassState(node.id, neighborhood));
    if (Boolean(node.selected) === selected && node.className === className) {
      return node;
    }
    changed = true;
    return { ...node, selected: selected || undefined, className };
  });
  return changed ? nextNodes : nodes;
}

export function selectIdeaFlowEdges(edges: Edge[], selectedNodeId: string | null): Edge[] {
  const neighborhood = selectIdeaLineageNeighborhood(edges, selectedNodeId);
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
    nodeId === neighborhood.selectedNodeId ? "selected" : "",
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
