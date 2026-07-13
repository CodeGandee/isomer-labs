import ELKModule from "elkjs/lib/elk-api.js";
import ELKWorker from "elkjs/lib/elk-worker.min.js?worker";
import {
  IDEA_GRAPH_NODE_HEIGHT,
  IDEA_GRAPH_NODE_WIDTH,
  elkLayoutOptions,
  normalizeLayoutConfiguration,
  type IdeaGraphLayoutConfiguration,
} from "./layout-registry";
import type { LayoutBounds, LayoutDiagnostic, LayoutPoint, LayoutWorkerEdge, LayoutWorkerNode, LayoutWorkerRequest, LayoutWorkerResult } from "./layout-protocol";

export type { LayoutWorkerRequest, LayoutWorkerResult } from "./layout-protocol";

export function deterministicGridLayout(nodes: LayoutWorkerNode[], configuration: Extract<IdeaGraphLayoutConfiguration, { algorithm: "grid" }>): Record<string, LayoutPoint> {
  const orderedNodes = nodes.slice().sort((left, right) => {
    const leftValue = configuration.parameters.sort === "label" ? left.label : left.id;
    const rightValue = configuration.parameters.sort === "label" ? right.label : right.id;
    return leftValue.localeCompare(rightValue) || left.id.localeCompare(right.id);
  });
  const columns = configuration.parameters.columns || Math.max(1, Math.ceil(Math.sqrt(orderedNodes.length)));
  return Object.fromEntries(orderedNodes.map((node, index) => [
    node.id,
    {
      x: (index % columns) * (IDEA_GRAPH_NODE_WIDTH + configuration.parameters.columnGap),
      y: Math.floor(index / columns) * (IDEA_GRAPH_NODE_HEIGHT + configuration.parameters.rowGap),
    },
  ]));
}

export function prepareRadialGraph(nodes: LayoutWorkerNode[], edges: LayoutWorkerEdge[]) {
  const nodeIds = new Set(nodes.map((node) => node.id));
  const incoming = new Set(edges.filter((edge) => nodeIds.has(edge.source) && nodeIds.has(edge.target)).map((edge) => edge.target));
  const roots = nodes.map((node) => node.id).filter((nodeId) => !incoming.has(nodeId)).sort();
  const radialRoots = roots.length > 0 ? roots : nodes.map((node) => node.id).sort().slice(0, 1);
  const virtualRootId = "__isomer_layout_virtual_root__";
  return {
    virtualRootId,
    nodes: [{ id: virtualRootId, label: "" }, ...nodes],
    edges: [
      ...radialRoots.map((target, index) => ({ id: `${virtualRootId}:${index}`, source: virtualRootId, target })),
      ...edges,
    ],
  };
}

export async function runLayoutRequest(request: LayoutWorkerRequest): Promise<LayoutWorkerResult> {
  const startedAt = performance.now();
  const parsed = normalizeLayoutConfiguration(request.configuration);
  if (!parsed.ok) {
    return failure(request, startedAt, "layout_configuration_invalid", parsed.diagnostics.join("; "));
  }
  try {
    let positions: Record<string, LayoutPoint>;
    if (parsed.configuration.algorithm === "grid") {
      positions = deterministicGridLayout(request.nodes, parsed.configuration);
    } else {
      const radial = parsed.configuration.algorithm === "radial" ? prepareRadialGraph(request.nodes, request.edges) : null;
      const engineNodes = radial?.nodes || request.nodes;
      const engineEdges = radial?.edges || request.edges;
      const elk = await createElk();
      const layout = await elk.layout({
        id: "root",
        layoutOptions: elkLayoutOptions(parsed.configuration),
        children: engineNodes.map((node) => ({ id: node.id, width: IDEA_GRAPH_NODE_WIDTH, height: IDEA_GRAPH_NODE_HEIGHT })),
        edges: engineEdges.map((edge) => ({ id: edge.id, sources: [edge.source], targets: [edge.target] })),
      }).finally(() => {
        if (typeof Worker !== "undefined") {
          elk.terminateWorker();
        }
      });
      const virtualRootId = radial?.virtualRootId;
      positions = Object.fromEntries((layout.children || [])
        .filter((node) => node.id !== virtualRootId)
        .map((node) => [node.id, { x: node.x || 0, y: node.y || 0 }]));
      if (parsed.configuration.algorithm === "radial") {
        positions = rotateRadialPositions(positions, parsed.configuration.parameters.startAngle, parsed.configuration.parameters.direction);
      }
    }
    return {
      type: "result",
      jobId: request.jobId,
      fingerprint: request.fingerprint,
      ok: true,
      positions,
      bounds: positionBounds(positions),
      durationMs: Math.max(0, performance.now() - startedAt),
      diagnostics: [],
    };
  } catch (error) {
    return failure(request, startedAt, "layout_engine_failed", error instanceof Error ? error.message : String(error));
  }
}

function resolveElkConstructor(moduleValue: unknown): typeof ELKModule {
  let candidate = moduleValue;
  for (let depth = 0; depth < 3 && typeof candidate === "object" && candidate && "default" in candidate; depth += 1) {
    candidate = (candidate as { default: unknown }).default;
  }
  if (typeof candidate !== "function") {
    throw new TypeError("ELK.js did not expose a layout constructor.");
  }
  return candidate as typeof ELKModule;
}

async function createElk(): Promise<InstanceType<typeof ELKModule>> {
  if (typeof Worker === "undefined") {
    const bundledModule = await import("elkjs/lib/elk.bundled.js");
    const BundledELK = resolveElkConstructor(bundledModule.default);
    return new BundledELK();
  }
  const ELK = resolveElkConstructor(ELKModule);
  return new ELK({ workerFactory: () => new ELKWorker() });
}

function rotateRadialPositions(positions: Record<string, LayoutPoint>, startAngle: number, direction: "clockwise" | "counterclockwise") {
  const entries = Object.entries(positions);
  if (entries.length === 0) {
    return positions;
  }
  const center = entries.reduce((result, [, point]) => ({ x: result.x + point.x / entries.length, y: result.y + point.y / entries.length }), { x: 0, y: 0 });
  const radians = (startAngle * Math.PI) / 180;
  const sign = direction === "clockwise" ? 1 : -1;
  return Object.fromEntries(entries.map(([nodeId, point]) => {
    const x = point.x - center.x;
    const y = (point.y - center.y) * sign;
    return [nodeId, { x: center.x + x * Math.cos(radians) - y * Math.sin(radians), y: center.y + x * Math.sin(radians) + y * Math.cos(radians) }];
  }));
}

function positionBounds(positions: Record<string, LayoutPoint>): LayoutBounds {
  const points = Object.values(positions);
  if (points.length === 0) {
    return { x: 0, y: 0, width: 0, height: 0 };
  }
  const minX = Math.min(...points.map((point) => point.x));
  const minY = Math.min(...points.map((point) => point.y));
  const maxX = Math.max(...points.map((point) => point.x + IDEA_GRAPH_NODE_WIDTH));
  const maxY = Math.max(...points.map((point) => point.y + IDEA_GRAPH_NODE_HEIGHT));
  return { x: minX, y: minY, width: maxX - minX, height: maxY - minY };
}

function failure(request: LayoutWorkerRequest, startedAt: number, code: string, message: string): LayoutWorkerResult {
  return {
    type: "result",
    jobId: request.jobId,
    fingerprint: request.fingerprint,
    ok: false,
    positions: {},
    bounds: { x: 0, y: 0, width: 0, height: 0 },
    durationMs: Math.max(0, performance.now() - startedAt),
    diagnostics: [{ severity: "error", code, message }],
  };
}
