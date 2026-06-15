# Pack: paper-plot

- kind: compiler
- backs: render plot
- status: **REAL adapter** (reference implementation of the pack adapter contract; stdlib only)
- source skill: DeepScientist `deepscientist-paper-plot`
- entrypoint: `adapter:render` (see `pack.toml`)
- input: CSV (x + named series columns) or JSON (`{x_label,x,series}` / `{x,y}` / `[{x,y}]`)
- output: self-contained `.svg` line+marker plot with axes, ticks, title, legend
- example input: `examples/sample.csv`

Enabled by default in `../../specs/state/seed.toml` (general/compiler, priority 100), so `render plot`
consumes this adapter instead of the generic stub. See `../ADAPTER-CONTRACT.md`.
