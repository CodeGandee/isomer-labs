# Style: `line_loss_with_inset`

Use this style when a loss or metric curve needs a zoomed inset to reveal a local difference that the full range would hide.

## Visual Contract

- Main panel shows the full curve range with the important local region marked by a rectangle.
- Inset panel zooms into the marked region and uses a clear border.
- Connectors between main panel and inset are thin, dashed, and dark enough to see without dominating the figure.
- Use an L-shaped main panel with left and bottom spines when the source style calls for axis-end emphasis.
- Keep the inset y-range tight enough to show the local structure but not so tight that it exaggerates noise.
- Use a light dotted grid on the main panel only when it improves curve reading.

## Input Shape

```python
steps = [0, 20, 40, 60]
series = {
    "Method A": [10.2, 8.1, 6.4, 5.7],
    "Method B": [10.1, 8.0, 6.0, 5.2],
}
zoom = {"x": [2400, 5500], "y": [1.8, 4.5]}
```

## Checks

- State why the inset is necessary.
- Ensure the inset does not hide the full-curve behavior or imply a larger effect than the numeric scale supports.
- If the local region defines a claim, link the claim to the same data Evidence Item.
