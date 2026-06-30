# Data Substitution

Use the source styles as visual contracts, not as fixed paper reproductions. Keep the data block, labels, and transformations explicit enough that another agent can regenerate the figure from the same Evidence Items.

## Before Substitution

- Identify the source Evidence Item, table, CSV, array, or parsed measurement that supports each plotted value.
- Record units, sample counts, uncertainty semantics, aggregation rule, and missing-value handling.
- State whether the plot shows measured values, parsed values, digitized values, or derived values.
- Confirm whether higher is better, lower is better, or the axis is descriptive.

## Edit Scope

- Replace data arrays, category names, method names, labels, legends, titles, and reference lines.
- Adjust figure size, axis limits, tick density, label rotation, color count, and legend placement only when the substituted data requires it.
- Keep the style's core visual grammar stable: paired bars stay paired, hatched primary methods stay emphasized, uncertainty bands stay bands, broken axes stay explicit.
- Record any deviation from the style contract as a Provenance Record or inspection note.

## Rendering and Inspection

- Render through an approved Execution Adapter Command Request and capture command, environment, and output paths when the host surface supports it.
- Inspect the actual raster or vector preview before reporting the figure as usable.
- If labels collide, uncertainty is ambiguous, or visual hierarchy misstates the evidence, revise the figure-generation Artifact and render again.
- For manuscript, appendix, review, or durable milestone figures, hand off to `$isomer-rsch-figure-polish-v1`.
