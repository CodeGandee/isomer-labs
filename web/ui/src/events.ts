import { Observable, Subject, interval, map, merge } from "rxjs";
import { filter } from "rxjs/operators";
import { parseTopicEvent } from "./api";
import type { GraphScope, TopicChangeEvent } from "./types";

export type WorkbenchCommand =
  | { type: "open-record"; topicId: string; recordId: string }
  | { type: "open-file"; topicId: string; recordId: string; fileId: string }
  | { type: "open-graph"; topicId: string; graphScope: GraphScope }
  | { type: "refresh-topic"; topicId: string };

export const workbenchCommands$ = new Subject<WorkbenchCommand>();
export const manualRefresh$ = new Subject<{ topicId: string }>();

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
  const polling$ = interval(15000).pipe(
    map(
      (): TopicChangeEvent => ({
        event_id: `${topicId}:poll`,
        event_type: "topic.runtime.changed",
        topic_id: topicId,
        graph_scopes: ["idea-lineage", "artifact-overview", "experiment-records", "paper-revisions"],
        occurred_at: new Date().toISOString(),
      }),
    ),
  );
  const manual$ = manualRefresh$.pipe(
    filter((event) => event.topicId === topicId),
    map(
      (): TopicChangeEvent => ({
        event_id: `${topicId}:manual`,
        event_type: "topic.runtime.changed",
        topic_id: topicId,
        graph_scopes: ["idea-lineage", "artifact-overview", "experiment-records", "paper-revisions"],
        occurred_at: new Date().toISOString(),
      }),
    ),
  );
  return merge(topicEvents(topicId), polling$, manual$);
}
