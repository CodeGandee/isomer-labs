# Style: `scatter_tsne_cluster`

Use this style for clustered embedding plots, dimensionality-reduction displays, or similar two-dimensional projections where cluster identity and annotation are the main readable structure.

## Visual Contract

- Use one discrete muted color per cluster.
- Keep point size modest and alpha below full opacity when clusters are dense.
- Use annotation boxes with translucent fills derived from the cluster color and a shared dark border.
- Keep grid lines light and dotted when they help orient the projection.
- Keep all four spines visible for a contained projection panel.
- Rasterize dense scatter points when exporting vector files, but keep text vector when possible.

## Input Shape

```python
points = {
    "Cluster A": {"x": [...], "y": [...], "color": "#6A4C93"},
    "Cluster B": {"x": [...], "y": [...], "color": "#D651A0"},
}
annotations = [{"label": "Cluster A", "xy": [10, 12]}]
```

## Checks

- Identify how the projection was computed and where that Artifact lives.
- Do not imply that distance in the projection is a validated scientific distance unless the method and interpretation support it.
- If the plot supports a claim, state whether the claim is qualitative, exploratory, or validated by a separate metric.
