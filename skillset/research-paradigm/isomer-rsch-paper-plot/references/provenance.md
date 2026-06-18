# Provenance

This skill adapts the DeepScientist `paper-plot` companion skill and its paper-style plotting references into a self-contained Isomer Labs skill.

The adaptation preserves reusable methodology: style routing, first-pass figure generation, data substitution discipline, render-inspect behavior, handoff to figure polishing, and per-style visual contracts for paired bars, grouped bars, confidence-band lines, training curves, inset loss curves, clustered scatter plots, broken-axis scatter plots, and dual-series radar charts.

Source-runtime concepts were intentionally translated:

- plotting workspaces became figure-generation Artifacts resolved by Workspace Path Resolution.
- bundled scripts became local style references and deferred resources rather than active runtime dependencies.
- source data paths became Source Data Artifacts or linked Evidence Items.
- script execution became Capability Binding through an Execution Adapter.
- final exports became Artifacts, Evidence Items, and Provenance Records rather than a source-specific export schema.

License context: the DeepScientist source project is licensed under Apache 2.0. Preserve this notice near this self-contained adaptation when copying, distributing, or materially revising the skill.
