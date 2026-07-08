## Why

The Project Web GUI is becoming a daily research workbench used on desktop, tablet, and phone screens. It needs explicit responsive layout rules so IDE-like desktop workflows stay dense while iPhone and Android use remains readable, stable, and tappable.

## What Changes

- Define the Project Web responsive layout contract across desktop, tablet, and phone viewport classes.
- Standardize on Tailwind CSS, shadcn/ui, and Radix-backed primitives for ordinary responsive app chrome and accessibility behavior.
- Require mobile-safe alternatives for hover-only interactions, narrow-screen sidebars, modals, tabs, tables, and graph/detail viewers.
- Add viewport-focused validation with Playwright screenshots or DOM checks for representative desktop, tablet, iPhone, and Android sizes.
- Keep specialized viewers such as Dockview, React Flow, Sigma, Markdown, PDF, and terminal panes, but wrap them in responsive shells.

## Capabilities

### New Capabilities
- `project-web-responsive-layout`: Defines responsive shell, overlay, navigation, interaction, and validation requirements for the Project Web GUI.

### Modified Capabilities

## Impact

- Affects TypeScript frontend layout and styling under `web/ui/src/`.
- May add shadcn/ui components such as Sheet or Scroll Area when needed, using copied source in the existing component tree.
- Extends frontend test coverage with viewport-specific validation.
- Does not change backend APIs, topic data contracts, research records, or query-index behavior.
