## Why

The Project Web GUI is growing from a small viewer into an IDE-like research workbench, but its current hand-written CSS and ad hoc controls will not scale cleanly across explorers, tabs, graph tools, dialogs, tables, Markdown/JSON viewers, and future terminal controls. Adopt shadcn/ui with Tailwind as the shared UI foundation now so new GUI surfaces use one component vocabulary and one token system.

## What Changes

- Add shadcn/ui as the primary source for ordinary React UI components in the Project Web GUI.
- Add Tailwind CSS as the primary styling and design-token system for GUI application chrome, controls, dialogs, tables, and custom viewer UI.
- Use shadcn's copied-code model so Isomer owns the generated components under the frontend source tree.
- Use the Radix-backed shadcn component path for accessible primitives such as dialogs, menus, selects, checkboxes, tooltips, tabs, and scroll areas.
- Keep specialized renderers in place: Dockview owns dockable workbench layout, React Flow owns sparse graph canvases, Sigma owns dense graph canvases, Plotly owns charts, react-markdown owns Markdown rendering, and xterm owns terminal panes.
- Bridge Tailwind/shadcn tokens into React Flow, Dockview, Markdown, JSON, and other viewer wrappers through scoped classes and CSS variables instead of replacing those libraries.
- Migrate the current GUI shell and common controls to shadcn components incrementally, starting with shared primitives and high-traffic workbench surfaces.

## Capabilities

### New Capabilities
- `project-web-gui-component-system`: Component and styling contract for the TypeScript Project Web GUI, including shadcn/ui adoption, Tailwind tokens, component ownership, specialized viewer boundaries, and migration rules.

### Modified Capabilities
None.

## Impact

- Affects `web/ui` dependencies, Vite configuration, TypeScript path aliases, global CSS, copied UI components, app shell components, tests, and frontend build output.
- Adds Tailwind CSS, the shadcn CLI/config surface, common shadcn runtime helper dependencies, Lucide icons, and Radix component dependencies as individual components are added.
- Updates GUI design documentation in `context/features/2026-07-06-topic-idea-iteration-map/design/techstack.md` to make shadcn/ui and Tailwind the recommended app UI foundation.
- Does not change backend APIs, Workspace Runtime storage, research records, query-index ownership, or canonical topic data.
