## Why

The web GUI now has a theme system, but users cannot change it from the GUI. A project-level settings tab gives the workbench a durable place for frontend preferences now and backend/service configuration later.

## What Changes

- Add a project settings item to the project explorer and openable descriptor model.
- Add a `Project Settings` Dockview tab that can be opened through the explorer or topbar.
- Add an Appearance section with a global theme selector for `System`, `Light`, and `Dark`.
- Persist the theme as a browser-local frontend preference using the existing theme provider.
- Keep backend/project settings out of this first slice, but reserve clear UI sections and contracts for future settings.

## Capabilities

### New Capabilities

- `project-web-settings`: Covers the web GUI settings surface, including project-level navigation to settings and frontend theme preference control.

### Modified Capabilities

- None.

## Impact

- Frontend: `web/ui/src/App.tsx`, theme provider usage, styles, and workbench tests.
- Backend read model: project explorer nodes and openable descriptor handling in `src/isomer_labs/web/project_explorer.py`.
- OpenSpec: new capability spec for the project web settings surface.
