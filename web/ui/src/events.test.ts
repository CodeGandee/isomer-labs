import { beforeEach, describe, expect, it, vi } from "vitest";
import { manualRefresh$, topicEventInvalidationDecision, topicEvents, topicInvalidations } from "./events";
import type { TopicChangeEvent } from "./types";

class FakeEventSource {
  static instances: FakeEventSource[] = [];
  onmessage: ((event: MessageEvent) => void) | null = null;
  onerror: (() => void) | null = null;
  close = vi.fn();
  listeners = new Map<string, (event: MessageEvent) => void>();
  addEventListener = vi.fn((name: string, listener: (event: MessageEvent) => void) => {
    this.listeners.set(name, listener);
  });

  constructor(public url: string) {
    FakeEventSource.instances.push(this);
  }

  emit(payload: TopicChangeEvent, name = "topic.index.changed") {
    const event = { data: JSON.stringify(payload) } as MessageEvent;
    if (name === "message") {
      this.onmessage?.(event);
      return;
    }
    this.listeners.get(name)?.(event);
  }
}

describe("topic event stream", () => {
  beforeEach(() => {
    FakeEventSource.instances = [];
  });

  it("closes EventSource when subscribers unsubscribe", () => {
    vi.stubGlobal("EventSource", FakeEventSource);
    const subscription = topicEvents("alpha").subscribe();
    expect(FakeEventSource.instances[0].url).toBe("/api/events?topic_id=alpha");
    subscription.unsubscribe();
    expect(FakeEventSource.instances[0].close).toHaveBeenCalled();
    vi.unstubAllGlobals();
  });

  it("uses the first backend revision as baseline and invalidates on revision changes", () => {
    const first = topicEvent("alpha", "qidx:one");
    expect(topicEventInvalidationDecision(undefined, first)).toEqual({ invalidate: false, observedRevision: "qidx:one" });
    expect(topicEventInvalidationDecision("qidx:one", first)).toEqual({ invalidate: false, observedRevision: "qidx:one" });
    expect(topicEventInvalidationDecision("qidx:one", topicEvent("alpha", "qidx:two"))).toEqual({ invalidate: true, observedRevision: "qidx:two" });
  });

  it("does not emit idle invalidations for unchanged revisions but keeps manual refresh", () => {
    vi.stubGlobal("EventSource", FakeEventSource);
    const received: TopicChangeEvent[] = [];
    const subscription = topicInvalidations("alpha").subscribe((event) => received.push(event));
    const source = FakeEventSource.instances[0];

    source.emit(topicEvent("alpha", "qidx:one"));
    source.emit(topicEvent("alpha", "qidx:one"));
    expect(received).toEqual([]);

    source.emit(topicEvent("alpha", "qidx:two"));
    expect(received.map((event) => event.index_revision)).toEqual(["qidx:two"]);

    manualRefresh$.next({ topicId: "alpha" });
    expect(received.at(-1)?.event_type).toBe("topic.manual-refresh");

    subscription.unsubscribe();
    vi.unstubAllGlobals();
  });
});

function topicEvent(topicId: string, revision: string): TopicChangeEvent {
  return {
    event_id: `${topicId}:${revision}`,
    event_type: "topic.index.changed",
    topic_id: topicId,
    topic_workspace_id: topicId,
    index_revision: revision,
    graph_scopes: ["idea-lineage"],
    occurred_at: "2026-07-07T00:00:00Z",
  };
}
