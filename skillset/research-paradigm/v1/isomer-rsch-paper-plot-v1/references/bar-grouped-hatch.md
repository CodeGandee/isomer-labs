# Style: `bar_grouped_hatch`

Use this style for small grouped bar comparisons where one primary method needs to stand out across benchmarks or ablations.

## Visual Contract

- Two to four bars per benchmark group.
- The primary method uses the strongest fill, often deep red such as `#C0392B`, and may use hatch strokes such as `//`.
- Comparison or ablation methods use lighter orange or gray fills.
- Bar borders use white or a light separating color so grouped bars stay legible.
- Show value labels above bars only when they fit without clutter; primary values may use bold text.
- Use a light y-grid only when it helps read bar height; remove top and right spines for an open-axis academic look.
- Keep the legend small, framed only if it improves readability, and visually match the hatch pattern.

## Input Shape

```python
benchmarks = ["Benchmark A", "Benchmark B", "Benchmark C"]
data = {
    "Baseline": [72.6, 12.3, 31.8],
    "Ablation": [68.2, 6.7, 26.3],
    "Primary": [78.0, 19.1, 39.4],
}
primary_method = "Primary"
ylabel = "Accuracy (%)"
```

## Checks

- Keep method ordering consistent across all groups.
- If the number of methods changes, update bar width, offsets, color count, hatches, legend labels, and value label placement together.
- If a primary method is not truly primary for the claim, do not give it visual dominance.
