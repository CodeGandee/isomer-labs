import { useEffect, useMemo, useState } from "react";
import type { TopicGraphView } from "../../types";
import { useStoreSelector } from "../../state/observable-store";
import type { IdeaLineageStore } from "./idea-lineage-state";
import { DEFAULT_LAYOUT_CONFIGURATIONS, IDEA_GRAPH_LAYOUT_REGISTRY, cloneLayoutConfiguration, type IdeaGraphLayoutAlgorithm, type IdeaGraphLayoutConfiguration } from "./layout-registry";
import {
  GraphLayoutPresetStorage,
  createGraphLayoutPreset,
  deleteGraphLayoutPreset,
  downloadGraphLayoutPreset,
  duplicateGraphLayoutPreset,
  importGraphLayoutPresets,
  listGraphLayoutPresets,
  renameGraphLayoutPreset,
  subscribeToGraphLayoutPresetStorage,
  updateGraphLayoutPreset,
  type GraphLayoutPresetCatalog,
  type PresetDiagnostic,
} from "./layout-presets";

export function IdeaGraphControls({ store, graph, onPreview }: { store: IdeaLineageStore; graph?: TopicGraphView; onPreview: () => void }) {
  const selectedNodeIds = useStoreSelector(store, (state) => state.selectedNodeIds, sameStrings);
  const focus = useStoreSelector(store, (state) => state.focus);
  const draft = useStoreSelector(store, (state) => state.layoutDraft);
  const applied = useStoreSelector(store, (state) => state.appliedLayout);
  const appliedPresetId = useStoreSelector(store, (state) => state.appliedPresetId);
  const layoutJob = useStoreSelector(store, (state) => state.layoutJob);
  const storage = useMemo(() => new GraphLayoutPresetStorage(), []);
  const initialCatalog = useMemo(() => storage.read(), [storage]);
  const [catalog, setCatalog] = useState<GraphLayoutPresetCatalog>(initialCatalog.value);
  const [presetName, setPresetName] = useState("My layout");
  const [diagnostics, setDiagnostics] = useState<PresetDiagnostic[]>(initialCatalog.diagnostics);
  const presets = useMemo(() => listGraphLayoutPresets(catalog), [catalog]);
  const selectedPreset = presets.find((preset) => preset.id === appliedPresetId) || null;
  const relationKinds = useMemo(() => [...new Set((graph?.edges || []).map((edge) => edge.relation_kind))].sort(), [graph?.edges]);
  const draftChanged = JSON.stringify(draft) !== JSON.stringify(applied);
  const sourceNodeCount = graph?.projection?.source_node_count ?? graph?.total_node_count ?? graph?.nodes.length ?? 0;
  const sourceEdgeCount = graph?.projection?.source_edge_count ?? graph?.total_edge_count ?? graph?.edges.length ?? 0;
  const visibleNodeCount = graph?.projection?.visible_node_count ?? graph?.nodes.length ?? 0;
  const visibleEdgeCount = graph?.projection?.visible_edge_count ?? graph?.edges.length ?? 0;

  useEffect(() => subscribeToGraphLayoutPresetStorage(() => {
    const refreshed = storage.read();
    setCatalog(refreshed.value);
    setDiagnostics(refreshed.diagnostics);
  }), [storage]);

  useEffect(() => {
    if (appliedPresetId && !presets.some((preset) => preset.id === appliedPresetId)) {
      store.dispatch({ type: "layoutPresetApplied", presetId: null, configuration: draft });
    }
  }, [appliedPresetId, draft, presets, store]);

  const persist = (result: { ok: boolean; value: GraphLayoutPresetCatalog; diagnostics: PresetDiagnostic[] }) => {
    if (!result.ok) {
      setDiagnostics(result.diagnostics);
      return;
    }
    const written = storage.write(result.value);
    setCatalog(written.value);
    setDiagnostics([...result.diagnostics, ...written.diagnostics]);
  };

  const changeAlgorithm = (algorithm: IdeaGraphLayoutAlgorithm) => {
    store.dispatch({ type: "layoutDraftChanged", configuration: cloneLayoutConfiguration(DEFAULT_LAYOUT_CONFIGURATIONS[algorithm]) });
  };

  const changeParameter = (name: string, value: string | number) => {
    const configuration = {
      ...draft,
      parameters: { ...draft.parameters, [name]: value },
    } as IdeaGraphLayoutConfiguration;
    store.dispatch({ type: "layoutDraftChanged", configuration });
  };

  const choosePreset = (presetId: string) => {
    const preset = presets.find((candidate) => candidate.id === presetId);
    if (preset) {
      setPresetName(preset.name);
      store.dispatch({ type: "layoutPresetApplied", presetId: preset.id, configuration: preset.configuration });
    }
  };

  const exportSelected = () => {
    if (selectedPreset) {
      setDiagnostics(downloadGraphLayoutPreset(selectedPreset, `${safeFilename(selectedPreset.name)}.json`).diagnostics);
    }
  };

  const importFile = async (file: File | undefined) => {
    if (!file) {
      return;
    }
    persist(importGraphLayoutPresets(catalog, await file.text()));
  };

  return (
    <details className="idea-graph-controls">
      <summary>Graph Controls</summary>
      <div className="idea-graph-controls-grid">
        <fieldset className="idea-graph-control-section">
          <legend>Focus</legend>
          <label className="idea-graph-check">
            <input
              aria-label="Enable N-hop focus"
              checked={focus.enabled}
              disabled={selectedNodeIds.length === 0}
              onChange={(event) => store.dispatch({ type: "focusChanged", focus: { enabled: event.target.checked } })}
              type="checkbox"
            />
            Show N-hop graph from selected ideas
          </label>
          <label>
            Hop radius
            <input aria-label="Focus hop radius" max={8} min={0} onChange={(event) => store.dispatch({ type: "focusChanged", focus: { hopRadius: Number(event.target.value) } })} type="number" value={focus.hopRadius} />
          </label>
          <label>
            Direction
            <select aria-label="Focus direction" onChange={(event) => store.dispatch({ type: "focusChanged", focus: { direction: event.target.value as typeof focus.direction } })} value={focus.direction}>
              <option value="both">Both</option>
              <option value="incoming">Incoming</option>
              <option value="outgoing">Outgoing</option>
            </select>
          </label>
          <div className="idea-graph-relations" aria-label="Focus relation kinds">
            <span>Relations</span>
            {relationKinds.length === 0 ? <small>All relation kinds</small> : relationKinds.map((relationKind) => (
              <label className="idea-graph-check" key={relationKind}>
                <input
                  checked={focus.relationKinds.includes(relationKind)}
                  onChange={(event) => store.dispatch({
                    type: "focusChanged",
                    focus: { relationKinds: event.target.checked ? [...focus.relationKinds, relationKind] : focus.relationKinds.filter((value) => value !== relationKind) },
                  })}
                  type="checkbox"
                />
                {relationKind}
              </label>
            ))}
          </div>
          <div className="idea-graph-focus-seeds" aria-label="Selected focus seeds">
            {selectedNodeIds.map((nodeId) => <span key={nodeId}>{graph?.nodes.find((node) => node.id === nodeId)?.title || nodeId}</span>)}
          </div>
          <p className="idea-graph-counts">Visible {visibleNodeCount} nodes / {visibleEdgeCount} edges of {sourceNodeCount} / {sourceEdgeCount}</p>
          {selectedNodeIds.length === 0 ? <p role="status">Select one or more ideas to enable focus.</p> : <p>{selectedNodeIds.length} focus seed{selectedNodeIds.length === 1 ? "" : "s"}</p>}
          <button disabled={selectedNodeIds.length === 0} onClick={() => store.dispatch({ type: "selectionCleared" })} type="button">Clear Selection</button>
          <button disabled={!focus.enabled} onClick={() => store.dispatch({ type: "focusExited" })} type="button">Exit Focus</button>
        </fieldset>

        <fieldset className="idea-graph-control-section">
          <legend>Layout</legend>
          <label>
            Preset
            <select aria-label="Graph layout preset" onChange={(event) => choosePreset(event.target.value)} value={appliedPresetId || ""}>
              <option value="">Custom</option>
              {presets.map((preset) => <option key={preset.id} value={preset.id}>{preset.name}{preset.builtin ? " (built-in)" : ""}</option>)}
            </select>
          </label>
          <label>
            Algorithm
            <select aria-label="Graph layout algorithm" onChange={(event) => changeAlgorithm(event.target.value as IdeaGraphLayoutAlgorithm)} value={draft.algorithm}>
              {IDEA_GRAPH_LAYOUT_REGISTRY.map((algorithm) => <option key={algorithm.id} value={algorithm.id}>{algorithm.label}</option>)}
            </select>
          </label>
          <LayoutParameterFields configuration={draft} onChange={changeParameter} />
          {draftChanged ? <p className="idea-graph-draft">Draft changes have not been previewed.</p> : null}
          <div className="idea-graph-control-actions">
            <button disabled={layoutJob.status === "running"} onClick={onPreview} type="button">Preview Layout</button>
            <button disabled={!draftChanged} onClick={() => store.dispatch({ type: "layoutDraftReverted" })} type="button">Revert Draft</button>
          </div>
          <label>
            Preset name
            <input aria-label="Graph layout preset name" maxLength={120} onChange={(event) => setPresetName(event.target.value)} value={presetName} />
          </label>
          <div className="idea-graph-control-actions">
            <button onClick={() => persist(createGraphLayoutPreset(catalog, presetName, applied))} type="button">Save as New</button>
            <button disabled={!selectedPreset || selectedPreset.builtin} onClick={() => selectedPreset && persist(updateGraphLayoutPreset(catalog, selectedPreset.id, applied))} type="button">Update</button>
            <button disabled={!selectedPreset} onClick={() => selectedPreset && persist(duplicateGraphLayoutPreset(catalog, selectedPreset))} type="button">Duplicate</button>
            <button disabled={!selectedPreset || selectedPreset.builtin} onClick={() => selectedPreset && persist(renameGraphLayoutPreset(catalog, selectedPreset.id, presetName))} type="button">Rename</button>
            <button disabled={!selectedPreset || selectedPreset.builtin} onClick={() => selectedPreset && persist(deleteGraphLayoutPreset(catalog, selectedPreset.id))} type="button">Delete</button>
          </div>
          <div className="idea-graph-control-actions">
            <label className="idea-graph-file-button">
              Import JSON
              <input accept="application/json,.json" aria-label="Import graph layout presets" onChange={(event) => void importFile(event.target.files?.[0])} type="file" />
            </label>
            <button disabled={!selectedPreset} onClick={exportSelected} type="button">Export Preset</button>
            <button onClick={() => setDiagnostics(downloadGraphLayoutPreset(catalog, "idea-graph-layout-presets.json").diagnostics)} type="button">Export All</button>
          </div>
          <p aria-live="polite" role="status">
            {layoutJob.status === "running" ? "Computing layout…" : layoutJob.status === "succeeded" ? `Layout completed in ${Math.round(layoutJob.durationMs || 0)} ms.` : ""}
          </p>
          {[...layoutJob.diagnostics.map((message) => ({ severity: "error" as const, code: "layout", message })), ...diagnostics].map((diagnostic, index) => (
            <p key={`${diagnostic.code}:${index}`} role={diagnostic.severity === "error" ? "alert" : "status"}>{diagnostic.message}</p>
          ))}
        </fieldset>
      </div>
    </details>
  );
}

function LayoutParameterFields({ configuration, onChange }: { configuration: IdeaGraphLayoutConfiguration; onChange: (name: string, value: string | number) => void }) {
  if (configuration.algorithm === "layered") {
    return <>
      <SelectParameter label="Layer direction" name="direction" onChange={onChange} options={["RIGHT", "DOWN", "LEFT", "UP"]} value={configuration.parameters.direction} />
      <NumberParameter label="Node spacing" max={300} min={10} name="nodeSpacing" onChange={onChange} value={configuration.parameters.nodeSpacing} />
      <NumberParameter label="Layer spacing" max={500} min={10} name="layerSpacing" onChange={onChange} value={configuration.parameters.layerSpacing} />
      <SelectParameter label="Edge routing" name="edgeRouting" onChange={onChange} options={["ORTHOGONAL", "POLYLINE", "SPLINES"]} value={configuration.parameters.edgeRouting} />
    </>;
  }
  if (configuration.algorithm === "force") {
    return <>
      <NumberParameter label="Iterations" max={2000} min={20} name="iterations" onChange={onChange} value={configuration.parameters.iterations} />
      <NumberParameter label="Repulsion" max={10000} min={1} name="repulsion" onChange={onChange} value={configuration.parameters.repulsion} />
      <NumberParameter label="Ideal edge length" max={500} min={10} name="idealEdgeLength" onChange={onChange} value={configuration.parameters.idealEdgeLength} />
      <NumberParameter label="Seed" max={2147483647} min={0} name="seed" onChange={onChange} value={configuration.parameters.seed} />
    </>;
  }
  if (configuration.algorithm === "stress") {
    return <>
      <NumberParameter label="Iterations" max={2000} min={20} name="iterations" onChange={onChange} value={configuration.parameters.iterations} />
      <NumberParameter label="Desired edge length" max={500} min={10} name="desiredEdgeLength" onChange={onChange} value={configuration.parameters.desiredEdgeLength} />
      <NumberParameter label="Seed" max={2147483647} min={0} name="seed" onChange={onChange} value={configuration.parameters.seed} />
    </>;
  }
  if (configuration.algorithm === "radial") {
    return <>
      <NumberParameter label="Radius step" max={500} min={20} name="radiusStep" onChange={onChange} value={configuration.parameters.radiusStep} />
      <NumberParameter label="Start angle" max={360} min={-360} name="startAngle" onChange={onChange} value={configuration.parameters.startAngle} />
      <SelectParameter label="Radial direction" name="direction" onChange={onChange} options={["clockwise", "counterclockwise"]} value={configuration.parameters.direction} />
      <NumberParameter label="Seed" max={2147483647} min={0} name="seed" onChange={onChange} value={configuration.parameters.seed} />
    </>;
  }
  return <>
    <NumberParameter label="Columns (0 = auto)" max={100} min={0} name="columns" onChange={onChange} value={configuration.parameters.columns} />
    <NumberParameter label="Column gap" max={500} min={0} name="columnGap" onChange={onChange} value={configuration.parameters.columnGap} />
    <NumberParameter label="Row gap" max={500} min={0} name="rowGap" onChange={onChange} value={configuration.parameters.rowGap} />
    <SelectParameter label="Grid sort" name="sort" onChange={onChange} options={["id", "label"]} value={configuration.parameters.sort} />
  </>;
}

function NumberParameter({ label, max, min, name, onChange, value }: { label: string; max: number; min: number; name: string; onChange: (name: string, value: number) => void; value: number }) {
  return <label>{label}<input aria-label={label} max={max} min={min} onChange={(event) => onChange(name, Number(event.target.value))} type="number" value={value} /></label>;
}

function SelectParameter({ label, name, onChange, options, value }: { label: string; name: string; onChange: (name: string, value: string) => void; options: string[]; value: string }) {
  return <label>{label}<select aria-label={label} onChange={(event) => onChange(name, event.target.value)} value={value}>{options.map((option) => <option key={option} value={option}>{option}</option>)}</select></label>;
}

function sameStrings(left: string[], right: string[]) {
  return left.length === right.length && left.every((value, index) => value === right[index]);
}

function safeFilename(value: string) {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "layout-preset";
}
