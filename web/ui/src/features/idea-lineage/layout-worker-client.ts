import type { LayoutWorkerRequest, LayoutWorkerResult } from "./layout-protocol";

type PendingJob = { resolve: (result: LayoutWorkerResult) => void; reject: (error: Error) => void };

export class IdeaGraphLayoutWorkerClient {
  private worker: Worker | null = null;
  private pending = new Map<number, PendingJob>();
  private activeJobId: number | null = null;
  private cache = new Map<string, LayoutWorkerResult>();
  private terminated = false;

  constructor(workerFactory: (() => Worker) | null = defaultWorkerFactory()) {
    if (workerFactory) {
      this.worker = workerFactory();
      this.worker.onmessage = (event: MessageEvent<LayoutWorkerResult>) => this.finish(event.data);
      this.worker.onerror = (event) => this.failAll(new Error(event.message || "Idea Graph layout worker failed."));
    }
  }

  async run(request: LayoutWorkerRequest): Promise<LayoutWorkerResult> {
    if (this.terminated) {
      throw new Error("Idea Graph layout worker has been terminated.");
    }
    const cached = this.cache.get(request.fingerprint);
    if (cached) {
      return { ...cached, jobId: request.jobId, durationMs: 0 };
    }
    this.cancelActive();
    this.activeJobId = request.jobId;
    if (!this.worker) {
      const { runLayoutRequest } = await import("./layout-engine");
      const result = await runLayoutRequest(request);
      if (this.activeJobId !== request.jobId) {
        throw new Error("Idea Graph layout job was superseded.");
      }
      this.activeJobId = null;
      if (result.ok) {
        this.cache.set(result.fingerprint, result);
      }
      return result;
    }
    return new Promise<LayoutWorkerResult>((resolve, reject) => {
      this.pending.set(request.jobId, { resolve, reject });
      this.worker?.postMessage(request);
    });
  }

  cancelActive() {
    if (this.activeJobId === null) {
      return;
    }
    this.worker?.postMessage({ type: "cancel", jobId: this.activeJobId });
    const pending = this.pending.get(this.activeJobId);
    pending?.reject(new Error("Idea Graph layout job was superseded."));
    this.pending.delete(this.activeJobId);
    this.activeJobId = null;
  }

  terminate() {
    this.cancelActive();
    this.terminated = true;
    this.worker?.terminate();
    this.worker = null;
    this.failAll(new Error("Idea Graph layout worker was terminated."));
    this.cache.clear();
  }

  private finish(result: LayoutWorkerResult) {
    const pending = this.pending.get(result.jobId);
    if (!pending) {
      return;
    }
    this.pending.delete(result.jobId);
    if (this.activeJobId === result.jobId) {
      this.activeJobId = null;
    }
    if (result.ok) {
      this.cache.set(result.fingerprint, result);
    }
    pending.resolve(result);
  }

  private failAll(error: Error) {
    for (const pending of this.pending.values()) {
      pending.reject(error);
    }
    this.pending.clear();
    this.activeJobId = null;
  }
}

function defaultWorkerFactory(): (() => Worker) | null {
  if (typeof Worker === "undefined") {
    return null;
  }
  return () => new Worker(new URL("./layout-worker.ts", import.meta.url), { type: "module", name: "idea-graph-layout" });
}
