# Style: `scatter_broken_axis`

Use this style when a scatter plot has a discontinuous x-range and a single continuous axis would hide the important low-range pattern or waste most of the panel.

## Visual Contract

- Use two adjacent axes with unequal widths when most points are in one range and a few outliers live far away.
- Show axis break marks on the broken axis edge and do not hide the discontinuity.
- Keep marker encodings stable across panels.
- Use black marker outlines for highlighted methods and lighter fill with no outline for background clouds.
- Put the legend in the denser panel only if it does not hide important points.
- Use a light frame or L-shaped spines according to the selected style, but make the break explicit.

## Input Shape

```python
series = {
    "Primary": {"x": [0, 5000, 20000], "y": [40.3, 40.3, 40.7], "marker": "*"},
    "Reference": {"x": [115000, 200000], "y": [39.6, 41.0], "marker": "^"},
}
left_xlim = [0, 50000]
right_xlim = [95000, 220000]
```

## Checks

- Record why the broken axis is necessary.
- Do not connect lines across the axis break unless the discontinuity is visually explicit.
- Prefer a normal scatter plot when the discontinuity is small or when a transformed axis would be more honest.
