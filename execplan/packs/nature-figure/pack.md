# Pack: nature-figure

- kind: compiler
- backs: render figure / render plot / polish
- status: **REAL adapter** (stdlib only; follows ../ADAPTER-CONTRACT.md)
- source skill: DeepScientist `deepscientist-nature-figure`
- entrypoint: `adapter:render`
- input: CSV/JSON data
- output: Nature-style .svg (Wong palette, despined axes, panel label, Arial)
- example input: examples/sample.csv
Enabled by default in `../../specs/state/seed.toml` (nature-domain publication set); disable per quest/domain if not needed.
