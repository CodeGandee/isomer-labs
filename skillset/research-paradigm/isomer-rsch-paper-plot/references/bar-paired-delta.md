# Style: `bar_paired_delta`

Use this style for paired baseline-versus-method comparisons with explicit gain labels.

## Visual Contract

- Two bars per group: baseline and method.
- Baseline uses a light steel blue such as `#A8C8E8`; the method uses a deep navy such as `#1B3D6E`.
- Gain labels sit above the method bar and use a red emphasis color such as `#CC2200`.
- A dashed horizontal guide may connect the baseline value to the method side of the pair.
- Arrows can point from baseline height to method height when the y-scale makes the gain readable.
- A boxed academic frame is acceptable; keep all four spines visible when the chart needs a crisp panel boundary.

## Input Shape

```python
groups = ["Benchmark A", "Benchmark B", "Benchmark C"]
baseline = [58.1, 55.2, 58.7]
method = [62.3, 61.2, 65.5]
delta_labels = ["+7.1%", "+10.9%", "+11.9%"]
ylabel = "Accuracy (%)"
```

## Checks

- Ensure each group has exactly one baseline value and one method value.
- Compute delta labels from the same source values or mark them as supplied labels.
- Avoid this style when there are more than two methods per group; use `bar_grouped_hatch` instead.
