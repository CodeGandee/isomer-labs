# Style Contract

Academic figures should be restrained, readable, and claim-faithful. The goal is to make the intended comparison obvious without adding visual clutter.

## Default Visual Rules

- Use a white or near-white background.
- Prefer muted palettes and avoid neon colors, rainbow maps, heavy shadows, glossy gradients, and thick decorative borders.
- Remove top and right spines unless a special chart truly needs a full frame.
- Use light grids only when they help the reader recover values.
- Keep legends small; direct labels are better when they reduce eye travel.
- Make the primary method visually dominant only when the claim warrants that hierarchy.
- Keep baselines or comparison lines slightly more neutral than the primary method.
- Keep labels, units, baselines, and uncertainty semantics explicit.

## Matplotlib Style Asset

For Python Matplotlib figures, prefer `assets/isomer-academic.mplstyle` unless a project or venue style asset is already accepted. Apply it as a starting contract, then make figure-specific adjustments in the figure-generation Artifact.

```python
plt.style.use("assets/isomer-academic.mplstyle")
```

## Practical Sizes

- Milestone summary: about `5.2 x 3.2 in`.
- Single-column paper figure: about `3.5 x 2.4 in`.
- Double-column paper figure: about `7.2 x 3.2 in`.

Adjust size when the content requires it, but record the reason if the surface is paper-facing.
