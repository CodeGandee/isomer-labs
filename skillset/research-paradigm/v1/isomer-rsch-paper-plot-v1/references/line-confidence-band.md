# Style: `line_confidence_band`

Use this style for ordered curves with uncertainty bands, such as training progress, scaling curves, or repeated-seed measurements.

## Visual Contract

- Plot mean or central estimate as a line and uncertainty as a semi-transparent band using `fill_between`.
- Use muted method colors such as green `#3A8B3A`, blue `#3B6BB5`, and gray `#999999`.
- Keep line widths balanced; the primary method may be slightly thicker or use a bold legend entry.
- Use an unframed legend inside the plot only when it does not block the data.
- Remove top and right spines for an open-axis look unless the selected publication style requires a full frame.
- Use a horizontal baseline reference line only when the Evidence Item supports the reference value.

## Input Shape

```python
x = [0, 5000, 10000, 15000, 20000]
primary_mean = [0.31, 0.37, 0.42, 0.46, 0.49]
primary_std = [0.02, 0.018, 0.014, 0.012, 0.01]
comparison_mean = [0.30, 0.34, 0.38, 0.41, 0.43]
comparison_std = [0.018, 0.016, 0.015, 0.014, 0.013]
```

## Checks

- Name the uncertainty statistic: standard deviation, standard error, confidence interval, quantile range, or supplied envelope.
- Do not draw a band if the source data only contains a single run and no uncertainty estimate.
- Use markers for sparse discrete x-values; omit markers for dense continuous curves unless they clarify sampled points.
