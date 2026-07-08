## 1. Hover Preview Data and Rendering

- [x] 1.1 Add lazy idea-detail loading for idea lineage hover previews using existing frontend API helpers and TanStack Query caching.
- [x] 1.2 Render loaded hover preview content through the existing Markdown preview pipeline instead of the compact graph metadata-only builder.
- [x] 1.3 Show a fixed-size loading state with an icon while the Markdown preview is loading and keep the same shell size after content loads.

## 2. Hover Interaction Lifecycle

- [x] 2.1 Make the hover popup pointer-interactive and internally scrollable without resizing for long Markdown.
- [x] 2.2 Keep the popup open when the pointer moves from the node into the popup, then close it after the pointer leaves both areas.
- [x] 2.3 Clear the popup before node-open flows and prevent stale hover content from remaining or reappearing after navigation.

## 3. Validation

- [x] 3.1 Add or update unit tests for loading state, full Markdown rendering, popup retention while hovered, and cleanup on open.
- [x] 3.2 Add or update Playwright coverage for idea lineage tooltip loading, scrollable Markdown preview, and double-click cleanup.
- [x] 3.3 Run frontend tests, production build, and Playwright checks against the local Project Web service.

## 4. Follow-up Interaction Fixes

- [x] 4.1 Lock the hover popup position after it becomes visible so node mouse movement does not drag the popup away from the cursor path.
- [x] 4.2 Add touch long-press handling for idea nodes that opens the same Markdown-capable hover popup and cancels if the press ends early.
- [x] 4.3 Extend unit and Playwright coverage for locked popup position and touch long-press preview behavior.
