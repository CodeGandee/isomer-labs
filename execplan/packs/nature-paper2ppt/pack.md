# Pack: nature-paper2ppt

- kind: compiler
- backs: render slides
- status: **REAL adapter** (stdlib only; follows ../ADAPTER-CONTRACT.md)
- source skill: DeepScientist `deepscientist-nature-paper2ppt`
- entrypoint: `adapter:render`
- input: outline JSON or Markdown
- output: self-contained .html slide deck (pptx upgrade path documented)
- example input: examples/outline.json
Disabled by default in `../../specs/state/seed.toml`; enable per quest/domain to consume it.
