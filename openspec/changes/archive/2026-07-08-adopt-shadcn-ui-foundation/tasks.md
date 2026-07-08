## 1. Frontend Foundation

- [x] 1.1 Add Tailwind v4, `@tailwindcss/vite`, shadcn baseline helper dependencies, Lucide icons, animation support, and the first Radix dependencies required by selected components.
- [x] 1.2 Wire the Tailwind Vite plugin into `web/ui/vite.config.ts` without changing the existing static build output path.
- [x] 1.3 Add TypeScript and Vite path aliases for `@/components`, `@/components/ui`, `@/lib`, and related shadcn imports.
- [x] 1.4 Add `web/ui/components.json` configured for a Vite React TypeScript app, Tailwind CSS variables, Radix-backed components, and Lucide icons.
- [x] 1.5 Add `src/lib/utils.ts` with the shadcn-compatible `cn()` helper.
- [x] 1.6 Add a small local theme-mode helper that defaults to `system`, resolves light/dark from browser preference, and persists explicit user choice in local storage only.

## 2. Tokens and Global Styling

- [x] 2.1 Replace or layer the current global CSS foundation with Tailwind imports and shadcn-compatible light/dark CSS variables.
- [x] 2.2 Configure restrained workbench tokens, including radius at or below 8px, readable neutral surfaces, semantic chart/status colors, sidebar tokens, and focus ring colors.
- [x] 2.3 Preserve existing third-party CSS imports for React Flow, Dockview, KaTeX, and other viewer libraries.
- [x] 2.4 Add scoped token bridges for Dockview, React Flow, Markdown view, JSON modal, tables, and viewer wrapper surfaces.
- [x] 2.5 Remove or narrow legacy global `button`, `input`, and `select` selectors once shadcn controls cover the migrated surfaces.

## 3. shadcn Component Set

- [x] 3.1 Add local copied shadcn UI components for Button, Input, Select, Checkbox, Badge, Dialog, Tooltip, DropdownMenu, ScrollArea, Separator, Tabs, and Table.
- [x] 3.2 Verify each copied component builds with the repo's React 19, TypeScript, Vite, and strict compiler settings.
- [x] 3.3 Add or update small wrapper components only where Isomer needs stable domain-specific variants, such as toolbar buttons, status badges, or viewer action buttons.

## 4. Workbench Migration

- [x] 4.1 Migrate app shell controls, topbar controls, and shared toolbar actions from raw controls to shadcn components.
- [x] 4.2 Migrate Project Explorer rows and badges while preserving Headless Tree behavior, topic selection, openable item ids, and keyboard/focus behavior.
- [x] 4.3 Migrate graph filter controls while preserving graph query keys, include-secondary behavior, and open-tab resource policy.
- [x] 4.4 Migrate records tables, diagnostics tables, and detail-panel action controls to shadcn components or Isomer wrappers around them.
- [x] 4.5 Migrate the JSON modal to shadcn Dialog while preserving darkened backdrop behavior, JSON view, copy JSON, and copy Markdown actions.

## 5. Viewer Integration

- [x] 5.1 Pass an explicit React Flow `colorMode` derived from GUI theme preference into the idea lineage React Flow view.
- [x] 5.2 Style idea lineage custom nodes, selected states, edge labels, controls, and background through scoped classes or React Flow CSS variables.
- [x] 5.3 Keep generated Markdown body styling scoped to the Markdown viewer wrapper and avoid requiring Tailwind classes inside generated Markdown content.
- [x] 5.4 Keep Sigma, Plotly, PDF, and terminal viewer surfaces behind wrappers that receive app tokens without replacing their renderer APIs.

## 6. Documentation

- [x] 6.1 Update `context/features/2026-07-06-topic-idea-iteration-map/design/techstack.md` to name shadcn/ui and Tailwind as the primary app UI foundation.
- [x] 6.2 Document specialized viewer exceptions and token-bridge expectations in the same tech stack notes.
- [x] 6.3 Add brief frontend contributor guidance near the GUI source or existing docs so future GUI code prefers shadcn components for ordinary controls.
- [x] 6.4 Document that light/dark/system theme choice is local browser presentation state, not Project or Topic Workspace state.

## 7. Tests and Validation

- [x] 7.1 Update frontend component tests affected by migrated controls and keep existing API behavior assertions intact.
- [x] 7.2 Update Playwright smoke checks for the Project Explorer, idea detail, Markdown preview, and JSON modal after component migration.
- [x] 7.3 Run `npm test` and `npm run build` in `web/ui`.
- [x] 7.4 Run repo-level `pixi run lint`, `pixi run typecheck`, and `pixi run test` if implementation changes TypeScript build output, Python serving code, or packaged assets.
- [x] 7.5 Run `openspec validate adopt-shadcn-ui-foundation --strict` and resolve any proposal/spec/task issues.
