# Chart Selection

Choose the chart form by the research issue, not by visual novelty.

| Question | Preferred Chart | Avoid |
| --- | --- | --- |
| Trend over steps, epochs, time, ordered budgets, or scale | line chart | bar chart with too many ordered categories |
| Small categorical endpoint comparison with meaningful zero | bar chart | bar chart for nonzero-baseline deltas unless clearly labeled |
| Comparison with uncertainty, confidence intervals, or seed spread | point-range, dot plot, or line with band | single bars that hide variation |
| True distribution with enough samples | box, violin, histogram, or empirical distribution | decorative distribution plots with too few samples |
| Matrix structure is itself the result | heatmap | heatmap used only to look rich |
| Cluster or projection structure is exploratory evidence | annotated scatter | claims that overstate projection distance |

## Split Rule

Use one dominant message per figure. If unrelated claims compete inside one image, split panels or create separate figures and record the split rationale.

## Color Rules

- Ordered magnitude uses a sequential muted palette.
- Signed deltas around zero or a reference use a diverging muted palette with a neutral midpoint.
- Categories use a discrete palette and should not imply ordering unless the data has one.
- Avoid colormaps with uneven lightness or hue jumps that obscure numeric order.
