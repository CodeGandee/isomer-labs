# Pack: nature-figure

- kind: compiler
- backs: render figure
- status: **REAL adapter** (stdlib only; follows ../ADAPTER-CONTRACT.md)
- source skill: DeepScientist `nature-figure`
- entrypoint: `adapter:render`
- input: CSV/JSON data
- output: Nature-style .svg (Wong palette, despined axes, panel label, Arial)
- example input: examples/sample.csv
Enabled by default in `../../specs/state/seed.toml` (nature-domain publication set); disable per quest/domain if not needed.

## Methodology references (ported from DeepScientist `nature-figure`)
Read before plotting: `references/figure-contract.md`, `qa-contract.md`, `design-theory.md`, `backend-selection.md`, `chart-types.md`. Fill the figure contract + run the QA checklist around the adapter call.
