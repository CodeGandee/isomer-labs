# Pack: figure-polish

- kind: compiler
- backs: render polish / render figure
- status: **REAL adapter** (stdlib only; follows ../ADAPTER-CONTRACT.md)
- source skill: DeepScientist `deepscientist-figure-polish`
- entrypoint: `adapter:render`
- input: an existing .svg figure
- output: polished .svg (white bg, frame, normalized font, optional title/caption)
- example: use paper-plot/examples/sample.svg as --input
Enabled by default in `../../specs/state/seed.toml` (publication set); disable per quest/domain if not needed.
