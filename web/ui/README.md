# Isomer Project Web GUI

Use local shadcn/ui components from `src/components/ui` for ordinary app controls such as buttons, inputs, selects, checkboxes, badges, dialogs, tooltips, menus, scroll areas, tabs, and tables. Add small Isomer wrappers when a workbench-specific variant becomes common.

Use Tailwind CSS tokens and shadcn-compatible CSS variables for app chrome and control styling. Theme choice is browser-local presentation state; default to `system` and do not write theme preference into Project or Topic Workspace data.

Keep specialized viewers specialized. Dockview, React Flow, Sigma, Plotly, Markdown, PDF, and terminal panes keep their renderer APIs, with app tokens bridged through wrapper classes or scoped CSS variables.
