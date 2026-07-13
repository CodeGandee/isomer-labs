/// <reference lib="webworker" />

import { runLayoutRequest } from "./layout-engine";
import type { LayoutWorkerCancelRequest, LayoutWorkerRequest } from "./layout-protocol";

const canceledJobs = new Set<number>();

self.onmessage = async (event: MessageEvent<LayoutWorkerRequest | LayoutWorkerCancelRequest>) => {
  if (event.data.type === "cancel") {
    canceledJobs.add(event.data.jobId);
    return;
  }
  const result = await runLayoutRequest(event.data);
  if (!canceledJobs.delete(result.jobId)) {
    self.postMessage(result);
  }
};
