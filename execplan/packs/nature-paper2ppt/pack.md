# Pack: nature-paper2ppt

- kind: compiler
- backs: render slides
- status: **REAL adapter** (stdlib only; follows ../ADAPTER-CONTRACT.md)
- source skill: DeepScientist `nature-paper2ppt`
- entrypoint: `adapter:render`
- input: outline JSON or Markdown
- output: self-contained .html slide deck (pptx upgrade path documented)
- example input: examples/outline.json
Enabled by default in `../../specs/state/seed.toml` (nature-domain publication set); disable per quest/domain if not needed.

## Deck procedure (ported from DeepScientist `nature-paper2ppt`)
`references/procedure.md` — argument spine, 12–16 slide structure, per-slide schema, figure-selection logic.
