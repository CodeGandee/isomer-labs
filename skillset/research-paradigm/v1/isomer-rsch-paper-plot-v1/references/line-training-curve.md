# Style: `line_training_curve`

Use this style for training-process curves or ordered performance curves with reference lines and phase markers.

## Visual Contract

- Use a restrained sans-serif style when the source data benefits from a technical training-curve look.
- Use vertical dashed lines for phase transitions, sampling changes, or breakpoints only when those events are part of the evidence.
- Use a horizontal dashed line for a baseline or target threshold only when the Evidence Item identifies it.
- Keep all four spines visible for a compact box-frame plot, or record why an open-axis variant is clearer.
- Place the legend in an empty region of the plot and use a white background with a light frame if overlap risk is high.

## Input Shape

```python
steps_primary = [0, 500, 1000, 1500, 2000]
y_primary = [0.03, 0.18, 0.29, 0.37, 0.42]
steps_comparison = [0, 1000, 2000, 4000, 6000]
y_comparison = [0.02, 0.20, 0.31, 0.39, 0.41]
breakpoints = {"primary_phase_end": 2200, "comparison_peak": 6050}
reference_y = 0.43
```

## Checks

- Verify step, epoch, budget, or time units before plotting.
- Do not smooth training curves unless the smoothing rule is recorded.
- If random variation matters, prefer `line_confidence_band`.
