import { z } from "zod";
import { DEFAULT_LAYOUT_CONFIGURATIONS, IdeaGraphLayoutConfigurationSchema, cloneLayoutConfiguration, type IdeaGraphLayoutConfiguration } from "./layout-registry";

export const IDEA_GRAPH_PRESET_STORAGE_KEY = "isomer-web-idea-graph-layout-presets-v1";
export const IDEA_GRAPH_PRESET_MAX_IMPORT_BYTES = 1024 * 1024;
export const IDEA_GRAPH_PRESET_SCHEMA_VERSION = 1 as const;

export const GraphLayoutPresetSchema = z.object({
  kind: z.literal("isomer.idea-graph-layout-preset"),
  schemaVersion: z.literal(IDEA_GRAPH_PRESET_SCHEMA_VERSION),
  id: z.string().min(1).max(128),
  name: z.string().min(1).max(120),
  builtin: z.boolean(),
  graphKind: z.literal("idea-lineage"),
  configuration: IdeaGraphLayoutConfigurationSchema,
  createdAt: z.string(),
  updatedAt: z.string(),
}).strict();

export const GraphLayoutPresetCatalogSchema = z.object({
  kind: z.literal("isomer.idea-graph-layout-preset-catalog"),
  schemaVersion: z.literal(IDEA_GRAPH_PRESET_SCHEMA_VERSION),
  presets: z.array(GraphLayoutPresetSchema).max(500),
}).strict();

export type GraphLayoutPreset = z.infer<typeof GraphLayoutPresetSchema>;
export type GraphLayoutPresetCatalog = z.infer<typeof GraphLayoutPresetCatalogSchema>;
export type PresetDiagnostic = { severity: "info" | "warning" | "error"; code: string; message: string };
export type PresetResult<T> = { ok: boolean; value: T; diagnostics: PresetDiagnostic[] };
type StorageLike = Pick<Storage, "getItem" | "setItem">;

const BUILTIN_TIME = "2026-01-01T00:00:00.000Z";
export const BUILTIN_GRAPH_LAYOUT_PRESETS: readonly GraphLayoutPreset[] = Object.freeze([
  frozenBuiltin("builtin-layered", "Layered", DEFAULT_LAYOUT_CONFIGURATIONS.layered),
  frozenBuiltin("builtin-force", "Force clusters", DEFAULT_LAYOUT_CONFIGURATIONS.force),
  frozenBuiltin("builtin-stress", "Stress map", DEFAULT_LAYOUT_CONFIGURATIONS.stress),
  frozenBuiltin("builtin-radial", "Radial", DEFAULT_LAYOUT_CONFIGURATIONS.radial),
  frozenBuiltin("builtin-grid", "Grid", DEFAULT_LAYOUT_CONFIGURATIONS.grid),
]);

export class GraphLayoutPresetStorage {
  constructor(private readonly storage: StorageLike | null = browserStorage()) {}

  read(): PresetResult<GraphLayoutPresetCatalog> {
    const empty = emptyCatalog();
    if (!this.storage) {
      return { ok: true, value: empty, diagnostics: [] };
    }
    let raw: string | null;
    try {
      raw = this.storage.getItem(IDEA_GRAPH_PRESET_STORAGE_KEY);
    } catch (error) {
      return failedCatalog(empty, "preset_storage_read_failed", error);
    }
    if (!raw) {
      return { ok: true, value: empty, diagnostics: [] };
    }
    if (raw.length > IDEA_GRAPH_PRESET_MAX_IMPORT_BYTES) {
      return failedCatalog(empty, "preset_storage_oversized", "Stored preset catalog exceeds the size limit.");
    }
    try {
      const parsed = GraphLayoutPresetCatalogSchema.safeParse(JSON.parse(raw));
      if (!parsed.success) {
        return failedCatalog(empty, "preset_storage_corrupt", parsed.error.issues.map((issue) => issue.message).join("; "));
      }
      return { ok: true, value: parsed.data, diagnostics: [] };
    } catch (error) {
      return failedCatalog(empty, "preset_storage_corrupt", error);
    }
  }

  write(catalog: GraphLayoutPresetCatalog): PresetResult<GraphLayoutPresetCatalog> {
    const parsed = GraphLayoutPresetCatalogSchema.safeParse(catalog);
    if (!parsed.success) {
      return failedCatalog(catalog, "preset_catalog_invalid", parsed.error.issues.map((issue) => issue.message).join("; "));
    }
    if (!this.storage) {
      return { ok: false, value: parsed.data, diagnostics: [{ severity: "error", code: "preset_storage_unavailable", message: "Browser-local storage is unavailable." }] };
    }
    try {
      this.storage.setItem(IDEA_GRAPH_PRESET_STORAGE_KEY, JSON.stringify(parsed.data));
      return { ok: true, value: parsed.data, diagnostics: [] };
    } catch (error) {
      return failedCatalog(parsed.data, "preset_storage_quota", error);
    }
  }
}

export function listGraphLayoutPresets(catalog: GraphLayoutPresetCatalog): GraphLayoutPreset[] {
  return [...BUILTIN_GRAPH_LAYOUT_PRESETS, ...catalog.presets];
}

export function createGraphLayoutPreset(
  catalog: GraphLayoutPresetCatalog,
  name: string,
  configuration: IdeaGraphLayoutConfiguration,
  options: { id?: string; now?: string } = {},
): PresetResult<GraphLayoutPresetCatalog> {
  const now = options.now || new Date().toISOString();
  const preset = GraphLayoutPresetSchema.safeParse({
    kind: "isomer.idea-graph-layout-preset",
    schemaVersion: 1,
    id: uniquePresetId(catalog, options.id || generatedId()),
    name: name.trim(),
    builtin: false,
    graphKind: "idea-lineage",
    configuration,
    createdAt: now,
    updatedAt: now,
  });
  if (!preset.success) {
    return failedCatalog(catalog, "preset_invalid", preset.error.issues.map((issue) => issue.message).join("; "));
  }
  return { ok: true, value: { ...catalog, presets: [...catalog.presets, preset.data] }, diagnostics: [] };
}

export function duplicateGraphLayoutPreset(catalog: GraphLayoutPresetCatalog, preset: GraphLayoutPreset, options: { id?: string; now?: string } = {}) {
  return createGraphLayoutPreset(catalog, `${preset.name} copy`, cloneLayoutConfiguration(preset.configuration), options);
}

export function renameGraphLayoutPreset(catalog: GraphLayoutPresetCatalog, presetId: string, name: string, now = new Date().toISOString()): PresetResult<GraphLayoutPresetCatalog> {
  const preset = catalog.presets.find((candidate) => candidate.id === presetId);
  if (!preset) {
    return failedCatalog(catalog, "preset_builtin_immutable", "Built-in presets must be saved as user-defined copies.");
  }
  const trimmed = name.trim();
  if (!trimmed) {
    return failedCatalog(catalog, "preset_name_required", "Preset name is required.");
  }
  return { ok: true, value: { ...catalog, presets: catalog.presets.map((candidate) => candidate.id === presetId ? { ...candidate, name: trimmed, updatedAt: now } : candidate) }, diagnostics: [] };
}

export function updateGraphLayoutPreset(catalog: GraphLayoutPresetCatalog, presetId: string, configuration: IdeaGraphLayoutConfiguration, now = new Date().toISOString()): PresetResult<GraphLayoutPresetCatalog> {
  const preset = catalog.presets.find((candidate) => candidate.id === presetId);
  if (!preset) {
    return failedCatalog(catalog, "preset_builtin_immutable", "Built-in presets must be saved as user-defined copies.");
  }
  const parsed = IdeaGraphLayoutConfigurationSchema.safeParse(configuration);
  if (!parsed.success) {
    return failedCatalog(catalog, "preset_configuration_invalid", parsed.error.issues.map((issue) => issue.message).join("; "));
  }
  return { ok: true, value: { ...catalog, presets: catalog.presets.map((candidate) => candidate.id === presetId ? { ...candidate, configuration: parsed.data, updatedAt: now } : candidate) }, diagnostics: [] };
}

export function deleteGraphLayoutPreset(catalog: GraphLayoutPresetCatalog, presetId: string): PresetResult<GraphLayoutPresetCatalog> {
  if (!catalog.presets.some((candidate) => candidate.id === presetId)) {
    return failedCatalog(catalog, "preset_builtin_immutable", "Built-in presets cannot be deleted.");
  }
  return { ok: true, value: { ...catalog, presets: catalog.presets.filter((candidate) => candidate.id !== presetId) }, diagnostics: [] };
}

export function serializeGraphLayoutPreset(value: GraphLayoutPreset | GraphLayoutPresetCatalog): PresetResult<string> {
  const schema = value.kind === "isomer.idea-graph-layout-preset" ? GraphLayoutPresetSchema : GraphLayoutPresetCatalogSchema;
  const parsed = schema.safeParse(value);
  if (!parsed.success) {
    return { ok: false, value: "", diagnostics: [{ severity: "error", code: "preset_export_invalid", message: parsed.error.issues.map((issue) => issue.message).join("; ") }] };
  }
  const serialized = JSON.stringify(parsed.data, null, 2);
  if (serialized.length > IDEA_GRAPH_PRESET_MAX_IMPORT_BYTES) {
    return { ok: false, value: "", diagnostics: [{ severity: "error", code: "preset_export_oversized", message: "Preset export exceeds the size limit." }] };
  }
  return { ok: true, value: serialized, diagnostics: [] };
}

export function downloadGraphLayoutPreset(value: GraphLayoutPreset | GraphLayoutPresetCatalog, filename: string): PresetResult<string> {
  const serialized = serializeGraphLayoutPreset(value);
  if (!serialized.ok || typeof document === "undefined") {
    return serialized;
  }
  const url = URL.createObjectURL(new Blob([serialized.value], { type: "application/json" }));
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  anchor.click();
  URL.revokeObjectURL(url);
  return serialized;
}

export function importGraphLayoutPresets(catalog: GraphLayoutPresetCatalog, raw: string, now = new Date().toISOString()): PresetResult<GraphLayoutPresetCatalog> {
  if (new Blob([raw]).size > IDEA_GRAPH_PRESET_MAX_IMPORT_BYTES) {
    return failedCatalog(catalog, "preset_import_oversized", "Preset import exceeds the size limit.");
  }
  let value: unknown;
  try {
    value = JSON.parse(raw);
  } catch (error) {
    return failedCatalog(catalog, "preset_import_invalid_json", error);
  }
  const candidates = GraphLayoutPresetSchema.safeParse(value).success
    ? [GraphLayoutPresetSchema.parse(value)]
    : GraphLayoutPresetCatalogSchema.safeParse(value).success
      ? GraphLayoutPresetCatalogSchema.parse(value).presets
      : null;
  if (!candidates) {
    return failedCatalog(catalog, "preset_import_unsupported", "Import is not a supported Graph Layout Preset or preset catalog version.");
  }
  let next = catalog;
  const diagnostics: PresetDiagnostic[] = [];
  for (const candidate of candidates) {
    const result = createGraphLayoutPreset(next, candidate.name, candidate.configuration, { id: candidate.id, now });
    if (!result.ok) {
      return result;
    }
    if (result.value.presets.at(-1)?.id !== candidate.id || candidate.builtin) {
      diagnostics.push({ severity: "info", code: "preset_imported_as_copy", message: `${candidate.name} was imported as a user-defined copy.` });
    }
    next = result.value;
  }
  return { ok: true, value: next, diagnostics };
}

export function subscribeToGraphLayoutPresetStorage(callback: () => void): () => void {
  if (typeof window === "undefined") {
    return () => {};
  }
  const listener = (event: StorageEvent) => {
    if (event.key === IDEA_GRAPH_PRESET_STORAGE_KEY) {
      callback();
    }
  };
  window.addEventListener("storage", listener);
  return () => window.removeEventListener("storage", listener);
}

export function emptyCatalog(): GraphLayoutPresetCatalog {
  return { kind: "isomer.idea-graph-layout-preset-catalog", schemaVersion: 1, presets: [] };
}

function frozenBuiltin(id: string, name: string, configuration: IdeaGraphLayoutConfiguration): GraphLayoutPreset {
  return Object.freeze({
    kind: "isomer.idea-graph-layout-preset" as const,
    schemaVersion: 1 as const,
    id,
    name,
    builtin: true,
    graphKind: "idea-lineage",
    configuration: deepFreeze(structuredClone(configuration)),
    createdAt: BUILTIN_TIME,
    updatedAt: BUILTIN_TIME,
  });
}

function deepFreeze<T>(value: T): T {
  if (value && typeof value === "object") {
    for (const child of Object.values(value)) {
      deepFreeze(child);
    }
    Object.freeze(value);
  }
  return value;
}

function failedCatalog(catalog: GraphLayoutPresetCatalog, code: string, error: unknown): PresetResult<GraphLayoutPresetCatalog> {
  return { ok: false, value: catalog, diagnostics: [{ severity: "error", code, message: error instanceof Error ? error.message : String(error) }] };
}

function browserStorage(): StorageLike | null {
  try {
    return typeof window === "undefined" ? null : window.localStorage;
  } catch {
    return null;
  }
}

function generatedId(): string {
  return typeof crypto !== "undefined" && "randomUUID" in crypto ? `preset-${crypto.randomUUID()}` : `preset-${Date.now().toString(36)}`;
}

function uniquePresetId(catalog: GraphLayoutPresetCatalog, desiredId: string): string {
  const existing = new Set([...BUILTIN_GRAPH_LAYOUT_PRESETS.map((preset) => preset.id), ...catalog.presets.map((preset) => preset.id)]);
  if (!existing.has(desiredId)) {
    return desiredId;
  }
  let suffix = 2;
  while (existing.has(`${desiredId}-copy-${suffix}`)) {
    suffix += 1;
  }
  return `${desiredId}-copy-${suffix}`;
}
