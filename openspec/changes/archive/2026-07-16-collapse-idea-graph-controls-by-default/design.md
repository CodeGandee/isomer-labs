## Context

`IdeaGraphControls` renders a native HTML `details` element inside each Idea Graph panel. The component currently supplies the boolean `open` attribute, so every newly mounted panel expands its Focus and Layout sections even when the user only wants to inspect the graph.

## Goals / Non-Goals

**Goals:**

- Start each newly mounted Graph Controls surface collapsed.
- Preserve the visible summary trigger and native expansion and collapse behavior.
- Verify both the default state and the ability to use the controls after expansion.

**Non-Goals:**

- Persist the expanded or collapsed state across panel mounts or browser sessions.
- Change Focus, Layout, preset, or graph-rendering behavior.
- Replace the native `details` and `summary` interaction with a custom drawer state model.

## Decisions

Remove the `open` attribute from the native `details` element and leave it uncontrolled. Native `details` semantics already provide the required collapsed default, keyboard-accessible summary trigger, and user-controlled toggling without new React state.

Component coverage will assert that the `details` element is closed after initial render. Browser smoke coverage will also verify the closed default and explicitly activate the summary before interacting with controls hidden inside the element.

A controlled React state variable was considered but rejected because no other component needs to observe or control this transient UI state. Browser-local persistence was also rejected because the requested behavior is a default for each new panel, not a user preference.

## Risks / Trade-offs

- [Existing tests assume controls are immediately interactive] → Expand Graph Controls explicitly before interacting with Focus or Layout fields.
- [A closed native `details` element keeps its descendants in the DOM] → Assert the element's `open` property rather than relying only on DOM queries for descendant controls.
- [Users who frequently edit layouts need one additional activation after each mount] → Keep the summary visible and use native keyboard and pointer behavior.
