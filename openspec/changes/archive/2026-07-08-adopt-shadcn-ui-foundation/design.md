## Context

The current Project Web GUI is a Vite React TypeScript app under `web/ui`. It uses Dockview for the workbench, Headless Tree for the Project Explorer, React Flow and Sigma for graphs, Plotly for charts, react-markdown for Markdown, and one large hand-written stylesheet for most application chrome.

The GUI is expanding toward an IDE-like research workbench with explorer rows, dockable tabs, filters, graph tools, record detail panels, Markdown/JSON/PDF viewers, diagnostics, and future tmux controls. Continuing with ad hoc CSS and raw HTML controls will make the interface harder to keep consistent and harder for future agents to extend safely.

## Goals / Non-Goals

**Goals:**

- Make shadcn/ui the primary component source for ordinary Project Web GUI controls and app chrome.
- Make Tailwind CSS the primary styling and token system for GUI application UI.
- Keep shadcn components as copied source that Isomer can edit, review, and test.
- Preserve specialized viewer libraries and bridge them to the app token system with scoped CSS variables and wrapper classes.
- Convert existing GUI surfaces incrementally without rewriting backend APIs or canonical topic data.
- Update GUI tech-stack documentation so future changes follow the same component vocabulary.

**Non-Goals:**

- Do not replace Dockview, React Flow, Sigma, Plotly, react-markdown, Mermaid, KaTeX, or xterm with shadcn components.
- Do not make Tailwind classes the styling mechanism for generated Markdown content or third-party canvas internals.
- Do not introduce a public theme marketplace or user-editable theme editor in this change.
- Do not change Workspace Runtime, query-index, research records, or Project Web backend read models.
- Do not migrate every CSS selector in one risky pass if a narrower component-by-component migration preserves behavior better.

## Decisions

### Use Tailwind v4 with Vite integration

Add `tailwindcss` and `@tailwindcss/vite`, wire the Tailwind Vite plugin into the frontend config, and move the app toward Tailwind's CSS-first setup. This follows current shadcn Vite guidance and avoids old config-heavy Tailwind setup unless the implementation discovers a local need for explicit config.

Alternative considered: keep plain CSS and copy only shadcn component markup. That keeps dependency count down, but it loses the token system and class conventions that make shadcn components maintainable.

### Use shadcn/ui as owned source, not a black-box package

Add `components.json`, `src/lib/utils.ts`, and copied components under `src/components/ui`. The GUI imports local components such as `@/components/ui/button` and owns their code after generation.

Alternative considered: use a packaged component library such as MUI or Mantine. Those libraries are productive, but shadcn's copied-code model fits this repo because agents can inspect and edit component internals without fighting opaque theme APIs.

### Prefer the Radix-backed shadcn path

Initialize and add components using the Radix-backed shadcn component path. Radix primitives are mature and match the GUI's need for accessible dialogs, dropdowns, selects, checkboxes, tooltips, popovers, scroll areas, and tabs.

Alternative considered: adopt shadcn's newer Base UI default immediately. The ecosystem and examples around Radix remain stronger for the controls we need, so Radix is the conservative choice for this workbench.

### Define shadcn/Tailwind as the app UI layer

Use shadcn components for buttons, inputs, selects, checkboxes, badges, dialogs, tooltips, dropdown menus, scroll areas, separators, tabs, and tables. Use Tailwind tokens for app-shell color, spacing, borders, radius, focus rings, and dark/light styling.

Alternative considered: apply shadcn only to new screens. That would create two visual systems and leave the existing explorer, toolbar, filters, and modal code as examples future agents may copy.

### Keep specialized viewers behind token bridges

React Flow, Dockview, Sigma, Plotly, Markdown, JSON, PDF, and terminal viewers keep their own rendering APIs. The GUI wraps them in shadcn/Tailwind-styled panels and maps app tokens into each viewer through scoped classes and CSS variables such as React Flow `--xy-*` variables.

Alternative considered: try to restyle third-party internals entirely with Tailwind utility classes. That is brittle because those libraries own internal DOM, canvas, SVG, or generated HTML structures.

### Use restrained workbench visual defaults

Configure shadcn tokens for a dense research tool, not a marketing page. Keep default radii at or below 8px, use quiet neutral surfaces, reserve semantic colors for artifact kind and status, and avoid a one-hue palette.

Alternative considered: use shadcn defaults unchanged. They are a good starting point, but the Isomer GUI needs a compact IDE-like feel and must keep graph/status colors legible across many artifact kinds.

### Migrate by surfaces with tests

Start with the shared foundation, then convert common controls and high-traffic surfaces: app shell, Explorer rows, toolbar controls, graph filters, JSON dialog, records table, and detail-panel actions. Keep behavior tests and Playwright checks close to each migrated surface.

Alternative considered: rewrite `App.tsx` and `styles.css` in one large migration. That would be faster visually but riskier because the current GUI combines routing, Dockview tabs, live invalidation, graph layout, and viewer behavior.

### Default to system theme with local browser persistence

Use `system` as the initial GUI theme mode. When a user explicitly chooses light, dark, or system in a future visible selector, persist that preference in browser-local storage instead of backend state, because theme selection is local presentation state and should not mutate the Project or Topic Workspace.

Alternative considered: store theme preference in the backend or Project configuration. That would make a local visual preference look like research project state and create unnecessary write paths in an otherwise read-only GUI.

### Clean up legacy global element selectors early

Once shadcn controls are introduced, remove or narrow global `button`, `input`, and `select` styling in the legacy stylesheet. Those selectors can override copied component styles and make the migration look unpredictable.

Alternative considered: leave legacy element selectors in place until the end of migration. That is lower churn, but it makes every converted shadcn control inherit old assumptions.

### Add local frontend contributor guidance

Add a short GUI source note or nearby documentation that says ordinary controls should use local shadcn components, while Dockview, React Flow, Sigma, Plotly, Markdown, PDF, and terminal surfaces remain specialized renderers. This gives future agents a durable rule to follow after the initial migration.

Alternative considered: rely only on OpenSpec artifacts. OpenSpec captures the change, but contributors working directly in `web/ui` need a nearby convention to prevent drift.

## Risks / Trade-offs

- Dependency and build complexity grows → Add only the baseline shadcn/Tailwind dependencies first, then let individual components add Radix packages as needed.
- Old CSS and Tailwind may conflict during migration → Scope legacy CSS under existing wrappers, migrate one surface at a time, and remove obsolete selectors as each component lands.
- Tailwind utilities can make JSX noisy → Keep reusable UI primitives and workbench components small, and use `cn()` plus component variants instead of long repeated class lists.
- Viewer internals may ignore app tokens → Use explicit CSS variable bridges for React Flow and Dockview, and keep viewer-specific tests or Playwright checks for contrast and layout.
- shadcn generated code may change over time → Commit copied components and treat future updates as deliberate code changes, not automatic dependency upgrades.

## Migration Plan

1. Add Tailwind v4, shadcn baseline dependencies, Vite plugin wiring, path aliases, `components.json`, `cn()` utility, and global token CSS.
2. Add the first shadcn UI primitives needed by the current GUI: Button, Input, Select, Checkbox, Badge, Dialog, Tooltip, DropdownMenu, ScrollArea, Separator, Tabs, and Table.
3. Bridge tokens into current viewer wrappers, especially React Flow color mode and CSS variables, Dockview container surfaces, Markdown view colors, JSON modal colors, and table borders.
4. Migrate app shell and shared controls from raw elements and legacy CSS to shadcn components while preserving existing API calls and Dockview behavior.
5. Migrate graph filter controls, idea lineage custom node styling, record tables, diagnostics, detail actions, and JSON modal controls.
6. Update `context/features/2026-07-06-topic-idea-iteration-map/design/techstack.md` and any nearby GUI design notes to name shadcn/ui and Tailwind as the primary app UI foundation.
7. Validate with frontend unit tests, Playwright GUI smoke checks, and `npm run build`; keep backend tests unchanged unless implementation touches serving behavior.

Rollback is straightforward before component migration: remove the Tailwind/shadcn setup and keep existing CSS. After component migration, rollback by reverting the specific migrated surface because canonical data and backend APIs are unchanged.

## Open Questions

Resolved for the first adoption slice:

- Use the Radix-backed shadcn component path rather than the newer Base UI default.
- Use Tailwind v4 with `@tailwindcss/vite`.
- Use the shadcn CLI to generate copied source, then review and commit the generated components as Isomer-owned code.
- Default theme mode to `system`; persist explicit user theme choice in local browser storage, not backend state.
- Migrate shared controls, toolbar, graph filters, explorer rows, tables, and JSON dialog first; defer broad `App.tsx` decomposition unless migration pressure requires it.
- Remove or narrow legacy global `button`, `input`, and `select` selectors early.
- Style React Flow through `colorMode`, custom node components, and scoped CSS-variable bridges rather than Tailwind utilities applied to internals.
- Add local frontend contributor guidance so future GUI work follows the shadcn/Tailwind component-system boundary.

Future work can decide whether to expose richer user-selectable themes beyond light, dark, and system modes.
