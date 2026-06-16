# Pack: figure-polish

- kind: compiler
- backs: render polish
- status: **REAL adapter** (stdlib only; follows ../ADAPTER-CONTRACT.md)
- source skill: DeepScientist `figure-polish`
- entrypoint: `adapter:render`
- input: an existing .svg figure
- output: polished .svg (white bg, frame, normalized font, optional title/caption)
- example: use paper-plot/examples/sample.svg as --input
Enabled by default in `../../specs/state/seed.toml` (publication set); disable per quest/domain if not needed.

## Self-review checklist + house style (ported from DeepScientist `figure-polish`)
Run `references/checklist.md` (render-inspect-revise + the 5 self-review questions) and apply `assets/deepscientist-academic.mplstyle`. The 1px frame is OFF by default (set params.frame=true to opt in) — the house style removes frames/spines.
