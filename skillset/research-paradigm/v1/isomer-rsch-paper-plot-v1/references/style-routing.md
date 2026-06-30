# Style Routing

Choose the closest standard style before creating new plotting logic. If two styles fit, prefer the style whose visual contract makes the claim easier to inspect rather than the one that looks more elaborate.

| Style | Chart Family | Best Fit | Read |
| --- | --- | --- | --- |
| `bar_paired_delta` | paired bar | Exactly two values per group where the story is baseline-versus-method gain. | `bar-paired-delta.md` |
| `bar_grouped_hatch` | grouped bar | Two to four methods per benchmark, with one primary method that needs emphasis. | `bar-grouped-hatch.md` |
| `line_confidence_band` | line with band | Training, scaling, or ordered curves with uncertainty or seed spread. | `line-confidence-band.md` |
| `line_training_curve` | line with markers | Ordered curves that need vertical breakpoints, phase markers, or a horizontal reference. | `line-training-curve.md` |
| `line_loss_with_inset` | line with inset | Loss or metric curves where a local region must be magnified to see differences. | `line-loss-with-inset.md` |
| `scatter_tsne_cluster` | annotated scatter | Embedding or dimensionality-reduction plots with clusters and labels. | `scatter-tsne-cluster.md` |
| `scatter_broken_axis` | broken-axis scatter | Scatter plots where one continuous x-axis would waste space or hide low-range structure. | `scatter-broken-axis.md` |
| `radar_dual_series` | radar | Two-method comparison across several normalized dimensions. | `radar-dual-series.md` |

## Routing Rules

- Use bar styles for small categorical comparisons with meaningful group labels and clear y-units.
- Use line styles for ordered x-axes such as steps, epochs, budgets, model sizes, or time.
- Use scatter styles only when point location itself carries the evidence.
- Use radar only when the dimensions are comparable enough to share one normalized display and when the user accepts the limitations of radial comparison.
- If the asked-for chart needs many panels, custom layout, image overlays, maps, domain-specific axes, or interactive inspection, create a custom figure-generation Artifact and route final QA to `$isomer-rsch-figure-polish-v1`.
