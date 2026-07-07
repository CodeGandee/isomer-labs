import { useCallback, useSyncExternalStore } from "react";
import { Observable, Subject, Subscription } from "rxjs";

export type ProjectWebStateCategory =
  | "backend-data"
  | "durable-navigation"
  | "workbench-layout"
  | "cross-component-events"
  | "persisted-settings"
  | "complex-interaction"
  | "private-ui";

export type ProjectWebStateOwnership = {
  category: ProjectWebStateCategory;
  owner: string;
  examples: string[];
};

// State ownership taxonomy for Project Web. Add new shared GUI state only after
// choosing one of these owners; private disposable UI state can stay local.
export const PROJECT_WEB_STATE_OWNERSHIP: ProjectWebStateOwnership[] = [
  { category: "backend-data", owner: "TanStack Query", examples: ["project summary", "topic graph", "records", "idea detail"] },
  { category: "durable-navigation", owner: "URL/history state", examples: ["topic id", "graph scope", "open item"] },
  { category: "workbench-layout", owner: "Dockview adapter", examples: ["tabs", "active panel", "panel close/focus"] },
  { category: "cross-component-events", owner: "RxJS event boundaries", examples: ["open record", "refresh topic", "SSE invalidation"] },
  { category: "persisted-settings", owner: "settings provider/store", examples: ["theme", "hover preview delay"] },
  { category: "complex-interaction", owner: "feature store/reducer", examples: ["selected graph node", "hover preview state", "touch long press"] },
  { category: "private-ui", owner: "component-local state", examples: ["modal tab", "search draft", "focus flag"] },
];

export type ProjectWebStore<State, Action> = {
  readonly actions$: Observable<Action>;
  readonly state$: Observable<State>;
  dispatch: (action: Action) => void;
  getSnapshot: () => State;
  subscribe: (listener: () => void) => () => void;
  dispose: () => void;
};

export function createProjectWebStore<State, Action>(
  initialState: State,
  reducer: (state: State, action: Action) => State,
): ProjectWebStore<State, Action> {
  let currentState = initialState;
  let disposed = false;
  const actionsSubject = new Subject<Action>();
  const changesSubject = new Subject<State>();
  const actionSubscription = actionsSubject.subscribe((action) => {
    const nextState = reducer(currentState, action);
    if (Object.is(nextState, currentState)) {
      return;
    }
    currentState = nextState;
    changesSubject.next(currentState);
  });

  const state$ = new Observable<State>((subscriber) => {
    subscriber.next(currentState);
    return changesSubject.subscribe(subscriber);
  });

  return {
    actions$: actionsSubject.asObservable(),
    state$,
    dispatch(action) {
      if (!disposed) {
        actionsSubject.next(action);
      }
    },
    getSnapshot() {
      return currentState;
    },
    subscribe(listener) {
      const subscription = changesSubject.subscribe(() => listener());
      return () => subscription.unsubscribe();
    },
    dispose() {
      if (disposed) {
        return;
      }
      disposed = true;
      actionSubscription.unsubscribe();
      actionsSubject.complete();
      changesSubject.complete();
    },
  };
}

export function useStoreSelector<State, Action, Selected>(
  store: ProjectWebStore<State, Action>,
  selector: (state: State) => Selected,
  isEqual: (left: Selected, right: Selected) => boolean = Object.is,
): Selected {
  const subscribe = useCallback(
    (listener: () => void) => {
      let previous = selector(store.getSnapshot());
      return store.subscribe(() => {
        const next = selector(store.getSnapshot());
        if (!isEqual(previous, next)) {
          previous = next;
          listener();
        }
      });
    },
    [isEqual, selector, store],
  );
  const getSnapshot = useCallback(() => selector(store.getSnapshot()), [selector, store]);
  return useSyncExternalStore(subscribe, getSnapshot, getSnapshot);
}

export type PanelScopedStoreMetadata = {
  openableItemId?: string;
  [key: string]: unknown;
};

export type DisposableFeatureStore = {
  dispose?: () => void;
};

export class PanelScopedStoreRegistry<Store extends DisposableFeatureStore> {
  private readonly entries = new Map<string, { store: Store; metadata: PanelScopedStoreMetadata }>();

  getOrCreate(panelId: string, create: () => Store, metadata: PanelScopedStoreMetadata = {}): Store {
    const existing = this.entries.get(panelId);
    if (existing) {
      existing.metadata = { ...existing.metadata, ...metadata };
      return existing.store;
    }
    const store = create();
    this.entries.set(panelId, { store, metadata });
    return store;
  }

  get(panelId: string): Store | undefined {
    return this.entries.get(panelId)?.store;
  }

  getMetadata(panelId: string): PanelScopedStoreMetadata | undefined {
    return this.entries.get(panelId)?.metadata;
  }

  has(panelId: string): boolean {
    return this.entries.has(panelId);
  }

  size(): number {
    return this.entries.size;
  }

  dispose(panelId: string): void {
    const entry = this.entries.get(panelId);
    if (!entry) {
      return;
    }
    entry.store.dispose?.();
    this.entries.delete(panelId);
  }

  disposeAll(): void {
    for (const panelId of this.entries.keys()) {
      this.dispose(panelId);
    }
  }
}
