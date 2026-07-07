import { act, cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { createProjectWebStore, PanelScopedStoreRegistry, PROJECT_WEB_STATE_OWNERSHIP, useStoreSelector } from "./observable-store";

type CounterState = {
  count: number;
  label: string;
};

type CounterAction =
  | { type: "increment" }
  | { type: "rename"; label: string }
  | { type: "noop" };

function counterReducer(state: CounterState, action: CounterAction): CounterState {
  if (action.type === "increment") {
    return { ...state, count: state.count + 1 };
  }
  if (action.type === "rename") {
    return { ...state, label: action.label };
  }
  return state;
}

describe("Project Web observable store", () => {
  afterEach(() => cleanup());

  it("dispatches typed actions through reducer transitions", () => {
    const store = createProjectWebStore<CounterState, CounterAction>({ count: 0, label: "ready" }, counterReducer);
    const states: CounterState[] = [];
    const subscription = store.state$.subscribe((state) => states.push(state));

    store.dispatch({ type: "increment" });
    store.dispatch({ type: "rename", label: "done" });
    store.dispatch({ type: "noop" });

    expect(store.getSnapshot()).toEqual({ count: 1, label: "done" });
    expect(states).toEqual([
      { count: 0, label: "ready" },
      { count: 1, label: "ready" },
      { count: 1, label: "done" },
    ]);
    subscription.unsubscribe();
    store.dispose();
  });

  it("subscribes React components to selected state only", () => {
    const store = createProjectWebStore<CounterState, CounterAction>({ count: 0, label: "ready" }, counterReducer);
    const renderSpy = vi.fn();

    function CounterLabel() {
      const label = useStoreSelector(store, (state) => state.label);
      renderSpy(label);
      return <div>{label}</div>;
    }

    render(<CounterLabel />);
    expect(screen.getByText("ready")).toBeTruthy();

    act(() => {
      store.dispatch({ type: "increment" });
    });
    expect(screen.getByText("ready")).toBeTruthy();
    expect(renderSpy).toHaveBeenCalledTimes(1);

    act(() => {
      store.dispatch({ type: "rename", label: "done" });
    });
    expect(screen.getByText("done")).toBeTruthy();
    expect(renderSpy).toHaveBeenCalledTimes(2);
    store.dispose();
  });

  it("cleans up panel-scoped stores when the owning panel closes", () => {
    const registry = new PanelScopedStoreRegistry<{ dispose: () => void }>();
    const dispose = vi.fn();
    const first = registry.getOrCreate("panel-a", () => ({ dispose }), { openableItemId: "topic:alpha:graph:idea-lineage" });
    const again = registry.getOrCreate("panel-a", () => ({ dispose: vi.fn() }), { custom: true });

    expect(again).toBe(first);
    expect(registry.size()).toBe(1);
    expect(registry.getMetadata("panel-a")).toEqual({ openableItemId: "topic:alpha:graph:idea-lineage", custom: true });

    registry.dispose("panel-a");

    expect(dispose).toHaveBeenCalledTimes(1);
    expect(registry.has("panel-a")).toBe(false);
  });

  it("documents the expected Project Web state ownership categories", () => {
    expect(PROJECT_WEB_STATE_OWNERSHIP.map((entry) => entry.category)).toEqual([
      "backend-data",
      "durable-navigation",
      "workbench-layout",
      "cross-component-events",
      "persisted-settings",
      "complex-interaction",
      "private-ui",
    ]);
  });
});
