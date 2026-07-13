import { describe, expect, it } from "vitest";
import { ideaLineageReducer, initialIdeaLineageState } from "./idea-lineage-state";
import { deterministicGridLayout, prepareRadialGraph, runLayoutRequest } from "./layout-engine";
import { layoutFingerprint, type LayoutWorkerRequest } from "./layout-protocol";
import { DEFAULT_LAYOUT_CONFIGURATIONS, elkLayoutOptions, normalizeLayoutConfiguration } from "./layout-registry";
import { IdeaGraphLayoutWorkerClient } from "./layout-worker-client";

const nodes = [{ id: "c", label: "Gamma" }, { id: "a", label: "Alpha" }, { id: "b", label: "Beta" }];
const edges = [{ id: "a-b", source: "a", target: "b" }, { id: "b-c", source: "b", target: "c" }];

describe("Idea Graph layout registry and engine", () => {
  it("validates bounded public configuration and maps only supported ELK keys", () => {
    expect(normalizeLayoutConfiguration({ ...DEFAULT_LAYOUT_CONFIGURATIONS.force, parameters: { ...DEFAULT_LAYOUT_CONFIGURATIONS.force.parameters, iterations: 5000 } }).ok).toBe(false);
    expect(normalizeLayoutConfiguration({ ...DEFAULT_LAYOUT_CONFIGURATIONS.layered, arbitraryEngineKey: "unsafe" }).ok).toBe(false);
    expect(elkLayoutOptions(DEFAULT_LAYOUT_CONFIGURATIONS.layered)).toEqual({
      "elk.algorithm": "layered",
      "elk.direction": "RIGHT",
      "elk.spacing.nodeNode": "50",
      "elk.layered.spacing.nodeNodeBetweenLayers": "80",
      "elk.edgeRouting": "ORTHOGONAL",
    });
    expect(elkLayoutOptions(DEFAULT_LAYOUT_CONFIGURATIONS.force)["elk.randomSeed"]).toBe("1");
    expect(elkLayoutOptions(DEFAULT_LAYOUT_CONFIGURATIONS.stress)["elk.randomSeed"]).toBe("1");
    expect(elkLayoutOptions(DEFAULT_LAYOUT_CONFIGURATIONS.radial)["elk.randomSeed"]).toBe("1");
  });

  it("creates a deterministic normalized grid", () => {
    const first = deterministicGridLayout(nodes, { ...DEFAULT_LAYOUT_CONFIGURATIONS.grid, parameters: { ...DEFAULT_LAYOUT_CONFIGURATIONS.grid.parameters, columns: 2 } });
    const second = deterministicGridLayout([...nodes].reverse(), { ...DEFAULT_LAYOUT_CONFIGURATIONS.grid, parameters: { ...DEFAULT_LAYOUT_CONFIGURATIONS.grid.parameters, columns: 2 } });

    expect(first).toEqual(second);
    expect(first.a).toEqual({ x: 0, y: 0 });
    expect(first.b).toEqual({ x: 310, y: 0 });
    expect(first.c).toEqual({ x: 0, y: 140 });
  });

  it("uses a layout-only radial root and never returns it as graph data", async () => {
    const prepared = prepareRadialGraph(nodes, edges);
    expect(prepared.nodes[0].id).toBe(prepared.virtualRootId);
    expect(nodes.some((node) => node.id === prepared.virtualRootId)).toBe(false);

    const request = layoutRequest(1, DEFAULT_LAYOUT_CONFIGURATIONS.radial);
    const result = await runLayoutRequest(request);
    expect(result.ok).toBe(true);
    expect(result.positions).not.toHaveProperty(prepared.virtualRootId);
    expect(Object.keys(result.positions).sort()).toEqual(["a", "b", "c"]);
  });

  it("fingerprints stable identities independent of input ordering", () => {
    const first = layoutFingerprint(nodes, edges, DEFAULT_LAYOUT_CONFIGURATIONS.layered);
    const reordered = layoutFingerprint([...nodes].reverse(), [...edges].reverse(), DEFAULT_LAYOUT_CONFIGURATIONS.layered);
    const changed = layoutFingerprint(nodes, edges, DEFAULT_LAYOUT_CONFIGURATIONS.grid);
    expect(first).toBe(reordered);
    expect(first).not.toBe(changed);
  });

  it("supersedes stale worker jobs, rejects results after termination, and retains last-good positions on failure", async () => {
    const worker = new FakeWorker();
    const client = new IdeaGraphLayoutWorkerClient(() => worker as unknown as Worker);
    const first = client.run(layoutRequest(1, DEFAULT_LAYOUT_CONFIGURATIONS.grid));
    const secondRequest = layoutRequest(2, DEFAULT_LAYOUT_CONFIGURATIONS.grid);
    const second = client.run(secondRequest);
    await expect(first).rejects.toThrow("superseded");
    worker.resolve({
      type: "result",
      jobId: 2,
      fingerprint: secondRequest.fingerprint,
      ok: true,
      positions: { a: { x: 1, y: 2 } },
      bounds: { x: 1, y: 2, width: 250, height: 90 },
      durationMs: 3,
      diagnostics: [],
    });
    await expect(second).resolves.toEqual(expect.objectContaining({ ok: true, jobId: 2 }));
    client.terminate();
    expect(worker.terminated).toBe(true);
    await expect(client.run(layoutRequest(3, DEFAULT_LAYOUT_CONFIGURATIONS.grid))).rejects.toThrow("terminated");

    const running = ideaLineageReducer({ ...initialIdeaLineageState, positions: { a: { x: 1, y: 2 } } }, { type: "layoutJobStarted", jobId: 4, fingerprint: "current" });
    const stale = ideaLineageReducer(running, { type: "layoutJobSucceeded", jobId: 3, fingerprint: "old", positions: { a: { x: 9, y: 9 } }, durationMs: 1, configuration: DEFAULT_LAYOUT_CONFIGURATIONS.grid });
    const failed = ideaLineageReducer(stale, { type: "layoutJobFailed", jobId: 4, fingerprint: "current", diagnostics: ["failure"] });
    expect(failed.positions).toEqual({ a: { x: 1, y: 2 } });
    expect(failed.layoutJob.status).toBe("failed");
  });
});

function layoutRequest(jobId: number, configuration: LayoutWorkerRequest["configuration"]): LayoutWorkerRequest {
  return { type: "layout", jobId, fingerprint: layoutFingerprint(nodes, edges, configuration), nodes, edges, configuration };
}

class FakeWorker {
  onmessage: ((event: MessageEvent) => void) | null = null;
  onerror: ((event: ErrorEvent) => void) | null = null;
  terminated = false;
  messages: unknown[] = [];

  postMessage(value: unknown) {
    this.messages.push(value);
  }

  terminate() {
    this.terminated = true;
  }

  resolve(value: unknown) {
    this.onmessage?.({ data: value } as MessageEvent);
  }
}
