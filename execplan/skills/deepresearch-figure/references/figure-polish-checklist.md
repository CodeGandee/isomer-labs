# Figure self-review checklist + style contract

A figure is not final until a **render → inspect → revise** pass is done: open the rendered figure and
inspect the actual result, not the code.

## Mandatory self-review (if any answer is "no", revise)
- Is the main message obvious within a few seconds?
- Are axis labels, units, and baselines explicit?
- Is it still readable after downscaling to column width?
- Does the primary method/result visually dominate the comparisons?
- Is it grayscale- and color-blind-safe (color is not the only encoding)?

## Style contract (house theme — see `assets/deepscientist-academic.mplstyle`)
- Muted/Morandi palette only; **no neon, no rainbow/jet** colormaps.
- Remove top and right spines; prefer direct labeling over dense legends; frameless legend.
- Do NOT add thick black borders/boxes around the plot area (the house style removes frames).
- Surface classes: connector (rough) / paper_main / appendix — set export discipline accordingly.
- Export vector (pdf/svg) + a png preview; embed TrueType fonts (`pdf.fonttype:42`, `svg.fonttype:none`);
  ≥220–300 dpi for raster previews.
