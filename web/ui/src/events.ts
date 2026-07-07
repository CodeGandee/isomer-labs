import { Observable, Subject, map, merge } from "rxjs";
import { filter } from "rxjs/operators";
import { parseTopicEvent } from "./api";
import type { GraphScope, TopicChangeEvent } from "./types";

export type WorkbenchCommand =
  | { type: "open-record"; topicId: string; recordId: string }
  | { type: "open-idea"; topicId: string; ideaId: string }
  | { type: "open-file"; topicId: string; recordId: string; fileId: string }
  | { type: "open-graph"; topicId: string; graphScope: GraphScope }
  | { type: "refresh-topic"; topicId: string };

export const workbenchCommands$ = new Subject<WorkbenchCommand>();
export const manualRefresh$ = new Subject<{ topicId: string }>();

const TOPIC_GRAPH_SCOPES: GraphScope[] = ["idea-lineage", "artifact-overview", "experiment-records", "paper-revisions"];

export type TopicInvalidationDecision = {
  invalidate: boolean;
  observedRevision: string | null | undefined;
};

export function topicEventInvalidationDecision(previousRevision: string | null | undefined, event: TopicChangeEvent): TopicInvalidationDecision {
  const revision = event.index_revision || null;
  if (!revision) {
    return { invalidate: true, observedRevision: previousRevision };
  }
  if (previousRevision === undefined) {
    return { invalidate: false, observedRevision: revision };
  }
  return { invalidate: revision !== previousRevision, observedRevision: revision };
}

export function topicEvents(topicId: string): Observable<TopicChangeEvent> {
  return new Observable<TopicChangeEvent>((subscriber) => {
    const source = new EventSource(`/api/events?topic_id=${encodeURIComponent(topicId)}`);
    source.onmessage = (event) => {
      try {
        subscriber.next(parseTopicEvent(event.data));
      } catch (error) {
        subscriber.error(error);
      }
    };
    source.addEventListener("topic.index.changed", (event) => {
      try {
        subscriber.next(parseTopicEvent((event as MessageEvent).data));
      } catch (error) {
        subscriber.error(error);
      }
    });
    source.onerror = () => {
      source.close();
      subscriber.complete();
    };
    return () => source.close();
  });
}

export function topicInvalidations(topicId: string) {
  const revision$ = new Observable<TopicChangeEvent>((subscriber) => {
    let observedRevision: string | null | undefined;
    const subscription = topicEvents(topicId).subscribe({
      next(event) {
        const decision = topicEventInvalidationDecision(observedRevision, event);
        observedRevision = decision.observedRevision;
        if (decision.invalidate) {
          subscriber.next(event);
        }
      },
      error(error) {
        subscriber.error(error);
      },
      complete() {
        subscriber.complete();
      },
    });
    return () => subscription.unsubscribe();
  });
  const manual$ = manualRefresh$.pipe(
    filter((event) => event.topicId === topicId),
    map(
      (): TopicChangeEvent => ({
        event_id: `${topicId}:manual`,
        event_type: "topic.manual-refresh",
        topic_id: topicId,
        index_revision: null,
        graph_scopes: TOPIC_GRAPH_SCOPES,
        occurred_at: new Date().toISOString(),
      }),
    ),
  );
  return merge(revision$, manual$);
}
