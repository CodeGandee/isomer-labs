## Context

The web GUI is a single-user IDE-style workbench with a project explorer on the left and Dockview tabs on the right. The shadcn/Tailwind foundation already added a browser-local theme provider with `system`, `light`, and `dark` modes, but no GUI control exposes it yet.

## Goals / Non-Goals

**Goals:**

- Add a semantic `Project Settings` surface that opens as a workbench tab.
- Expose the existing theme mode as the first editable frontend setting.
- Keep the settings surface available at the project level instead of binding it to a topic.
- Preserve existing browser history behavior for openable workbench items.

**Non-Goals:**

- Do not add backend setting mutation APIs in this change.
- Do not persist theme preferences into project files.
- Do not introduce a new settings storage model beyond the existing local storage theme preference.

## Decisions

- Model settings as an openable project item named `project:settings`. This keeps navigation consistent with project overview, manifest, diagnostics, and topic items.
- Render settings as a Dockview tab using a new `settings` component. This preserves the IDE-style tab model and lets browser Back return to the prior workbench state.
- Add a topbar settings button that opens the same `project:settings` item. The explorer and toolbar paths share one descriptor and one tab identity.
- Treat `Global Theme` as a browser-local frontend preference. Theme is user presentation state, not research topic state, so it must not mutate backend project content.
- Use existing shadcn select/button controls for the first implementation slice. A more visual segmented control can replace the select later if the component set grows.

## Risks / Trade-offs

- Project-level tabs currently render only when a topic is selected. The implementation must allow the Dockview host to appear for project-level settings without forcing topic selection.
- Local theme persistence means the setting follows the browser profile, not every device or service instance. This is acceptable for the first slice because the GUI is single-user and current theme storage is already frontend-local.
- Backend settings are not editable yet. The settings page should make future sections visible without implying unavailable backend mutation support.

## Migration Plan

- No data migration is required.
- Existing users keep the default `system` theme unless they already have `isomer-web-gui-theme` in local storage.
- Rollback removes the settings openable item and panel without touching project data.
