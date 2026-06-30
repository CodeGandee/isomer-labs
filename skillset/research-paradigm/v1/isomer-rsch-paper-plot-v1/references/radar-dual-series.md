# Style: `radar_dual_series`

Use this style for a two-method comparison across several benchmark dimensions when a compact radial overview is useful.

## Visual Contract

- Use exactly two primary series unless the Operator Agent explicitly accepts a crowded comparison.
- Normalize each dimension with a recorded range or transformation.
- Use octagonal or polygon grid rings for discrete dimensions rather than circular rings that imply continuous angle semantics.
- Give the primary method a thicker line and matched semi-transparent fill.
- Place value labels in small white boxes only if they remain readable and do not crowd the category labels.
- Put the legend outside the plot area when space allows.

## Input Shape

```python
categories = ["Task A", "Task B", "Task C", "Task D"]
primary_raw = [78.4, 6.0, 5.5, 67.6]
comparison_raw = [76.3, 5.7, 5.1, 66.9]
ranges = [(74.0, 80.0), (5.4, 6.2), (4.8, 5.7), (65.0, 70.0)]
```

## Checks

- Do not use radar when categories are incomparable or when absolute values matter more than shape.
- Record every normalization range.
- If a dimension has reversed direction, mark that explicitly and consider another chart.
