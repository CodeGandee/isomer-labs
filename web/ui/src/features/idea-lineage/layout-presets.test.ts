import { afterEach, describe, expect, it, vi } from "vitest";
import { DEFAULT_LAYOUT_CONFIGURATIONS } from "./layout-registry";
import {
  BUILTIN_GRAPH_LAYOUT_PRESETS,
  GraphLayoutPresetStorage,
  IDEA_GRAPH_PRESET_MAX_IMPORT_BYTES,
  IDEA_GRAPH_PRESET_STORAGE_KEY,
  createGraphLayoutPreset,
  deleteGraphLayoutPreset,
  duplicateGraphLayoutPreset,
  emptyCatalog,
  importGraphLayoutPresets,
  renameGraphLayoutPreset,
  serializeGraphLayoutPreset,
  subscribeToGraphLayoutPresetStorage,
  updateGraphLayoutPreset,
} from "./layout-presets";

describe("browser-local Graph Layout Presets", () => {
  afterEach(() => {
    vi.restoreAllMocks();
    window.localStorage.clear();
  });

  it("round-trips a validated catalog and falls back safely on corrupt storage", () => {
    const storage = new GraphLayoutPresetStorage(window.localStorage);
    const created = createGraphLayoutPreset(emptyCatalog(), "Wide lineage", DEFAULT_LAYOUT_CONFIGURATIONS.layered, { id: "wide", now: "2026-07-13T00:00:00Z" });
    expect(created.ok).toBe(true);
    expect(storage.write(created.value).ok).toBe(true);
    expect(storage.read().value).toEqual(created.value);

    window.localStorage.setItem(IDEA_GRAPH_PRESET_STORAGE_KEY, "{broken");
    const corrupt = storage.read();
    expect(corrupt.ok).toBe(false);
    expect(corrupt.value).toEqual(emptyCatalog());
    expect(corrupt.diagnostics[0].code).toBe("preset_storage_corrupt");
  });

  it("reports quota failure without replacing the prior catalog", () => {
    const storage = new GraphLayoutPresetStorage({
      getItem: () => null,
      setItem: () => { throw new DOMException("quota", "QuotaExceededError"); },
    });
    const result = storage.write(emptyCatalog());
    expect(result.ok).toBe(false);
    expect(result.value).toEqual(emptyCatalog());
    expect(result.diagnostics[0].code).toBe("preset_storage_quota");
  });

  it("supports CRUD while keeping built-ins deeply immutable", () => {
    const created = createGraphLayoutPreset(emptyCatalog(), "Custom", DEFAULT_LAYOUT_CONFIGURATIONS.grid, { id: "custom", now: "2026-07-13T00:00:00Z" });
    const renamed = renameGraphLayoutPreset(created.value, "custom", "Renamed", "2026-07-13T00:01:00Z");
    const updated = updateGraphLayoutPreset(renamed.value, "custom", DEFAULT_LAYOUT_CONFIGURATIONS.force, "2026-07-13T00:02:00Z");
    const duplicated = duplicateGraphLayoutPreset(updated.value, updated.value.presets[0], { id: "duplicate", now: "2026-07-13T00:03:00Z" });
    const deleted = deleteGraphLayoutPreset(duplicated.value, "custom");

    expect(deleted.value.presets.map((preset) => preset.id)).toEqual(["duplicate"]);
    expect(deleted.value.presets[0].name).toBe("Renamed copy");
    expect(deleteGraphLayoutPreset(deleted.value, "builtin-layered").diagnostics[0].code).toBe("preset_builtin_immutable");
    expect(updateGraphLayoutPreset(deleted.value, "builtin-layered", DEFAULT_LAYOUT_CONFIGURATIONS.grid).ok).toBe(false);
    expect(Object.isFrozen(BUILTIN_GRAPH_LAYOUT_PRESETS[0])).toBe(true);
    expect(Object.isFrozen(BUILTIN_GRAPH_LAYOUT_PRESETS[0].configuration.parameters)).toBe(true);
  });

  it("exports bounded JSON and imports valid files with conflicts as copies", () => {
    const created = createGraphLayoutPreset(emptyCatalog(), "Custom", DEFAULT_LAYOUT_CONFIGURATIONS.grid, { id: "custom", now: "2026-07-13T00:00:00Z" });
    const serializedPreset = serializeGraphLayoutPreset(created.value.presets[0]);
    const serializedCatalog = serializeGraphLayoutPreset(created.value);
    expect(serializedPreset.ok).toBe(true);
    expect(serializedCatalog.ok).toBe(true);
    expect(JSON.parse(serializedPreset.value).kind).toBe("isomer.idea-graph-layout-preset");

    const imported = importGraphLayoutPresets(created.value, serializedPreset.value, "2026-07-13T00:05:00Z");
    expect(imported.ok).toBe(true);
    expect(imported.value.presets.map((preset) => preset.id)).toEqual(["custom", "custom-copy-2"]);
    expect(imported.diagnostics[0].code).toBe("preset_imported_as_copy");
  });

  it("rejects unknown versions, discriminators, invalid parameters, and oversized files", () => {
    const valid = createGraphLayoutPreset(emptyCatalog(), "Custom", DEFAULT_LAYOUT_CONFIGURATIONS.grid, { id: "custom" }).value.presets[0];
    expect(importGraphLayoutPresets(emptyCatalog(), JSON.stringify({ ...valid, schemaVersion: 2 })).diagnostics[0].code).toBe("preset_import_unsupported");
    expect(importGraphLayoutPresets(emptyCatalog(), JSON.stringify({ ...valid, kind: "unknown" })).diagnostics[0].code).toBe("preset_import_unsupported");
    expect(importGraphLayoutPresets(emptyCatalog(), JSON.stringify({ ...valid, configuration: { ...valid.configuration, parameters: { columns: 1000 } } })).diagnostics[0].code).toBe("preset_import_unsupported");
    expect(importGraphLayoutPresets(emptyCatalog(), "x".repeat(IDEA_GRAPH_PRESET_MAX_IMPORT_BYTES + 1)).diagnostics[0].code).toBe("preset_import_oversized");
  });

  it("notifies open panels when another tab updates the catalog", () => {
    const callback = vi.fn();
    const unsubscribe = subscribeToGraphLayoutPresetStorage(callback);
    window.dispatchEvent(new StorageEvent("storage", { key: IDEA_GRAPH_PRESET_STORAGE_KEY }));
    window.dispatchEvent(new StorageEvent("storage", { key: "other" }));
    expect(callback).toHaveBeenCalledTimes(1);
    unsubscribe();
  });
});
