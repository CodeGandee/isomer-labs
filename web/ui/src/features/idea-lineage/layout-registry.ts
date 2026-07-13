import { z } from "zod";

export const IDEA_GRAPH_NODE_WIDTH = 250;
export const IDEA_GRAPH_NODE_HEIGHT = 90;
export const IDEA_GRAPH_LAYOUT_SCHEMA_VERSION = 1 as const;

const viewportSchema = z.object({ fitViewPadding: z.number().min(0).max(1).default(0.2) }).strict();
const baseConfiguration = {
  schemaVersion: z.literal(IDEA_GRAPH_LAYOUT_SCHEMA_VERSION),
  viewport: viewportSchema.default({ fitViewPadding: 0.2 }),
};

export const LayeredLayoutConfigurationSchema = z.object({
  ...baseConfiguration,
  algorithm: z.literal("layered"),
  parameters: z.object({
    direction: z.enum(["RIGHT", "DOWN", "LEFT", "UP"]),
    nodeSpacing: z.number().min(10).max(300),
    layerSpacing: z.number().min(10).max(500),
    edgeRouting: z.enum(["ORTHOGONAL", "POLYLINE", "SPLINES"]),
  }).strict(),
}).strict();

export const ForceLayoutConfigurationSchema = z.object({
  ...baseConfiguration,
  algorithm: z.literal("force"),
  parameters: z.object({
    iterations: z.number().int().min(20).max(2000),
    repulsion: z.number().min(1).max(10000),
    idealEdgeLength: z.number().min(10).max(500),
    seed: z.number().int().min(0).max(2147483647),
  }).strict(),
}).strict();

export const StressLayoutConfigurationSchema = z.object({
  ...baseConfiguration,
  algorithm: z.literal("stress"),
  parameters: z.object({
    iterations: z.number().int().min(20).max(2000),
    desiredEdgeLength: z.number().min(10).max(500),
    seed: z.number().int().min(0).max(2147483647),
  }).strict(),
}).strict();

export const RadialLayoutConfigurationSchema = z.object({
  ...baseConfiguration,
  algorithm: z.literal("radial"),
  parameters: z.object({
    radiusStep: z.number().min(20).max(500),
    startAngle: z.number().min(-360).max(360),
    direction: z.enum(["clockwise", "counterclockwise"]),
    seed: z.number().int().min(0).max(2147483647),
  }).strict(),
}).strict();

export const GridLayoutConfigurationSchema = z.object({
  ...baseConfiguration,
  algorithm: z.literal("grid"),
  parameters: z.object({
    columns: z.number().int().min(0).max(100),
    columnGap: z.number().min(0).max(500),
    rowGap: z.number().min(0).max(500),
    sort: z.enum(["id", "label"]),
  }).strict(),
}).strict();

export const IdeaGraphLayoutConfigurationSchema = z.discriminatedUnion("algorithm", [
  LayeredLayoutConfigurationSchema,
  ForceLayoutConfigurationSchema,
  StressLayoutConfigurationSchema,
  RadialLayoutConfigurationSchema,
  GridLayoutConfigurationSchema,
]);

export type IdeaGraphLayoutConfiguration = z.infer<typeof IdeaGraphLayoutConfigurationSchema>;
export type IdeaGraphLayoutAlgorithm = IdeaGraphLayoutConfiguration["algorithm"];

export const DEFAULT_LAYOUT_CONFIGURATIONS = {
  layered: {
    schemaVersion: 1,
    algorithm: "layered",
    parameters: { direction: "RIGHT", nodeSpacing: 50, layerSpacing: 80, edgeRouting: "ORTHOGONAL" },
    viewport: { fitViewPadding: 0.2 },
  },
  force: {
    schemaVersion: 1,
    algorithm: "force",
    parameters: { iterations: 300, repulsion: 1000, idealEdgeLength: 120, seed: 1 },
    viewport: { fitViewPadding: 0.2 },
  },
  stress: {
    schemaVersion: 1,
    algorithm: "stress",
    parameters: { iterations: 300, desiredEdgeLength: 120, seed: 1 },
    viewport: { fitViewPadding: 0.2 },
  },
  radial: {
    schemaVersion: 1,
    algorithm: "radial",
    parameters: { radiusStep: 140, startAngle: -90, direction: "clockwise", seed: 1 },
    viewport: { fitViewPadding: 0.2 },
  },
  grid: {
    schemaVersion: 1,
    algorithm: "grid",
    parameters: { columns: 0, columnGap: 60, rowGap: 50, sort: "id" },
    viewport: { fitViewPadding: 0.2 },
  },
} satisfies Record<IdeaGraphLayoutAlgorithm, IdeaGraphLayoutConfiguration>;

export const IDEA_GRAPH_LAYOUT_REGISTRY = [
  { id: "layered", label: "Layered", engine: "elk", description: "Directed layers for lineage and dependency reading." },
  { id: "force", label: "Force", engine: "elk", description: "Force-directed spacing for dense relationship clusters." },
  { id: "stress", label: "Stress", engine: "elk", description: "Distance-preserving layout for connected graphs." },
  { id: "radial", label: "Radial", engine: "elk", description: "Concentric arrangement around deterministic roots." },
  { id: "grid", label: "Grid", engine: "native", description: "Fast deterministic rows and columns." },
] as const;

export type LayoutConfigurationParseResult =
  | { ok: true; configuration: IdeaGraphLayoutConfiguration; diagnostics: string[] }
  | { ok: false; configuration: IdeaGraphLayoutConfiguration; diagnostics: string[] };

export function normalizeLayoutConfiguration(value: unknown): LayoutConfigurationParseResult {
  const parsed = IdeaGraphLayoutConfigurationSchema.safeParse(value);
  if (parsed.success) {
    return { ok: true, configuration: parsed.data, diagnostics: [] };
  }
  const algorithm = typeof value === "object" && value && "algorithm" in value
    ? String((value as { algorithm?: unknown }).algorithm)
    : "layered";
  const fallback = algorithm in DEFAULT_LAYOUT_CONFIGURATIONS
    ? DEFAULT_LAYOUT_CONFIGURATIONS[algorithm as IdeaGraphLayoutAlgorithm]
    : DEFAULT_LAYOUT_CONFIGURATIONS.layered;
  return {
    ok: false,
    configuration: structuredClone(fallback),
    diagnostics: parsed.error.issues.map((issue) => `${issue.path.join(".") || "configuration"}: ${issue.message}`),
  };
}

export function elkLayoutOptions(configuration: Exclude<IdeaGraphLayoutConfiguration, { algorithm: "grid" }>): Record<string, string> {
  if (configuration.algorithm === "layered") {
    return {
      "elk.algorithm": "layered",
      "elk.direction": configuration.parameters.direction,
      "elk.spacing.nodeNode": String(configuration.parameters.nodeSpacing),
      "elk.layered.spacing.nodeNodeBetweenLayers": String(configuration.parameters.layerSpacing),
      "elk.edgeRouting": configuration.parameters.edgeRouting,
    };
  }
  if (configuration.algorithm === "force") {
    return {
      "elk.algorithm": "force",
      "elk.force.iterations": String(configuration.parameters.iterations),
      "elk.force.repulsion": String(configuration.parameters.repulsion),
      "elk.spacing.nodeNode": String(configuration.parameters.idealEdgeLength),
      "elk.randomSeed": String(configuration.parameters.seed),
    };
  }
  if (configuration.algorithm === "stress") {
    return {
      "elk.algorithm": "stress",
      "elk.stress.iterationLimit": String(configuration.parameters.iterations),
      "elk.stress.desiredEdgeLength": String(configuration.parameters.desiredEdgeLength),
      "elk.randomSeed": String(configuration.parameters.seed),
    };
  }
  return {
    "elk.algorithm": "radial",
    "elk.spacing.nodeNode": String(configuration.parameters.radiusStep),
    "elk.radial.compactor": "RADIAL",
    "elk.randomSeed": String(configuration.parameters.seed),
  };
}

export function cloneLayoutConfiguration(configuration: IdeaGraphLayoutConfiguration): IdeaGraphLayoutConfiguration {
  return structuredClone(configuration);
}
