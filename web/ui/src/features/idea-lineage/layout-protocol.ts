import { IDEA_GRAPH_NODE_HEIGHT, IDEA_GRAPH_NODE_WIDTH, type IdeaGraphLayoutConfiguration } from "./layout-registry";

export type LayoutWorkerNode = { id: string; label: string };
export type LayoutWorkerEdge = { id: string; source: string; target: string; relationKind?: string };
export type LayoutPoint = { x: number; y: number };
export type LayoutBounds = { x: number; y: number; width: number; height: number };
export type LayoutDiagnostic = { severity: "info" | "warning" | "error"; code: string; message: string };

export type LayoutWorkerRequest = {
  type: "layout";
  jobId: number;
  fingerprint: string;
  nodes: LayoutWorkerNode[];
  edges: LayoutWorkerEdge[];
  configuration: IdeaGraphLayoutConfiguration;
};

export type LayoutWorkerCancelRequest = { type: "cancel"; jobId: number };
export type LayoutWorkerResult = {
  type: "result";
  jobId: number;
  fingerprint: string;
  ok: boolean;
  positions: Record<string, LayoutPoint>;
  bounds: LayoutBounds;
  durationMs: number;
  diagnostics: LayoutDiagnostic[];
};

export function layoutFingerprint(nodes: LayoutWorkerNode[], edges: LayoutWorkerEdge[], configuration: IdeaGraphLayoutConfiguration): string {
  return JSON.stringify({
    dimensions: [IDEA_GRAPH_NODE_WIDTH, IDEA_GRAPH_NODE_HEIGHT],
    nodes: nodes.map(({ id, label }) => ({ id, label })).sort((left, right) => left.id.localeCompare(right.id)),
    edges: edges.map(({ id, source, target, relationKind }) => ({ id, source, target, relationKind: relationKind || null })).sort((left, right) => left.id.localeCompare(right.id)),
    configuration,
  });
}
