## 1. Responsive Audit

- [ ] 1.1 Audit current Project Web shell, sidebar, Dockview host, toolbar, modal, graph, table, Markdown, and file viewer layouts for narrow viewport risks.
- [ ] 1.2 Define shared CSS tokens or utility classes for safe viewport bounds, stable overlay rows, touch target spacing, and scroll-contained panes.

## 2. Shell and Navigation

- [ ] 2.1 Convert the main workbench shell to mobile-first layout rules with desktop breakpoints for persistent sidebar and docked tabs.
- [ ] 2.2 Add a narrow-screen Project Explorer access path using a Sheet, drawer, or equivalent full-height navigation surface.
- [ ] 2.3 Ensure toolbar controls wrap, collapse, or move into menus without overlapping at phone and tablet widths.

## 3. Overlay and Interaction Surfaces

- [ ] 3.1 Apply stable shell sizing to dialogs and tabbed overlays so headers, tabs, and action buttons do not move when content changes.
- [ ] 3.2 Add touch-compatible alternatives for hover or double-click-only interactions in idea graph inspection and detail opening.
- [ ] 3.3 Ensure dialogs and sheets respect dynamic viewport height and safe-area insets on mobile browsers.

## 4. Viewer Wrappers

- [ ] 4.1 Wrap React Flow, Sigma, Markdown, PDF, image, JSON, and table viewers in bounded responsive containers with internal scrolling where needed.
- [ ] 4.2 Add narrow-screen table behavior through horizontal scroll, compact list/card fallback, or another bounded presentation.
- [ ] 4.3 Preserve desktop density for IDE-style workbench use while avoiding page-level horizontal scrolling on phone-sized viewports.

## 5. Validation

- [ ] 5.1 Add Playwright or equivalent browser checks for desktop, tablet, iPhone-sized, and Android-sized viewports.
- [ ] 5.2 Validate representative surfaces: project navigation, topic graph, idea detail, JSON dialog, Markdown viewer, records table, and settings.
- [ ] 5.3 Run frontend tests and build, then update packaged static assets if the build output is committed.
