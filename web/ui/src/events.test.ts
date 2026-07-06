import { describe, expect, it, vi } from "vitest";
import { topicEvents } from "./events";

class FakeEventSource {
  static instances: FakeEventSource[] = [];
  onmessage: ((event: MessageEvent) => void) | null = null;
  onerror: (() => void) | null = null;
  close = vi.fn();
  addEventListener = vi.fn();

  constructor(public url: string) {
    FakeEventSource.instances.push(this);
  }
}

describe("topic event stream", () => {
  it("closes EventSource when subscribers unsubscribe", () => {
    vi.stubGlobal("EventSource", FakeEventSource);
    const subscription = topicEvents("alpha").subscribe();
    expect(FakeEventSource.instances[0].url).toBe("/api/events?topic_id=alpha");
    subscription.unsubscribe();
    expect(FakeEventSource.instances[0].close).toHaveBeenCalled();
    vi.unstubAllGlobals();
  });
});
