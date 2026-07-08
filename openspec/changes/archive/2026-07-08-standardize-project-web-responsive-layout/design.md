## Context

The Project Web GUI is an IDE-like research workbench with a semantic Project Explorer, dockable tabs, graphs, Markdown, JSON, PDFs, tables, and future terminal or AG-UI panes. The current stack already uses React, TypeScript, Tailwind CSS, shadcn/ui, Radix primitives, Dockview, React Flow, Sigma, TanStack Query, TanStack Router, and Playwright.

## Goals / Non-Goals

**Goals:**
- Define mobile-first responsive rules for desktop, tablet, iPhone, and Android browser use.
- Keep dense desktop workbench behavior while providing narrow-screen alternatives for navigation, overlays, tables, and graph/detail inspection.
- Use Tailwind CSS, shadcn/ui, and Radix primitives as the app chrome foundation.
- Require viewport validation so regressions such as jumping controls, clipped text, or unreachable buttons are caught early.

**Non-Goals:**
- Do not replace Dockview, React Flow, Sigma, Markdown, PDF, terminal, or Plotly viewers with generic shadcn components.
- Do not add a second component framework such as MUI, Chakra, or Mantine.
- Do not redesign backend APIs or research data contracts.
- Do not require feature parity for every dense desktop interaction on phone in the first implementation; phone behavior can use focused fallback flows.

## Decisions

- Use viewport classes rather than platform branches. The GUI should adapt by width, height, pointer precision, hover availability, and safe-area insets instead of testing for PC, Mac, iPhone, or Android user agents.
- Keep CSS mobile-first. Base rules target narrow screens, then larger breakpoints add persistent sidebars, denser toolbars, Dockview splits, and wider graph canvases.
- Use Tailwind and shadcn-compatible CSS variables for ordinary chrome. Existing copied shadcn components remain editable and can be extended with local classes for app-specific behavior.
- Use Radix-backed primitives for overlays and controls. Dialog, Sheet, Tabs, Select, Tooltip, Dropdown Menu, Scroll Area, and related components provide accessibility semantics while the app controls responsive layout.
- Keep specialized viewers inside responsive wrappers. Dockview, React Flow, Sigma, Markdown, PDF, table, terminal, and AG-UI panes should receive stable container dimensions, scroll boundaries, and theme variables from wrapper components.
- Provide narrow-screen navigation fallbacks. The desktop Project Explorer stays persistent; tablet can collapse it; phone should open it through a Sheet or equivalent full-height drawer.
- Avoid hover-only workflows. Hover previews may exist on desktop, but tap, long-press, selection, or explicit open controls must cover touch devices.
- Stabilize overlay controls. Dialogs, sheets, popovers, and tabbed panes must keep headers, tab strips, and action controls in fixed tracks while content scrolls inside bounded panes.
- Validate with representative viewports. Use Playwright or equivalent browser checks for desktop, tablet, iPhone, and Android-sized layouts, including dark and light themes where practical.

## Risks / Trade-offs

- Responsive work can sprawl across many components -> Start with shared shell, overlay, and viewer wrapper patterns before polishing every panel.
- Dockview may not be ideal on phone -> Use single-panel or stacked fallback layouts on narrow screens while preserving desktop Dockview behavior.
- Touch alternatives can overload the UI -> Prefer explicit open buttons, selected-node panels, and full-screen sheets over hidden gestures.
- Viewport tests can be brittle -> Check stable layout properties, reachable controls, and absence of overflow rather than exact pixel screenshots unless visual review is needed.
