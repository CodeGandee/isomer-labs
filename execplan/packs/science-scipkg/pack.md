# Pack: science-scipkg

- kind: reference
- backs: knowledge cards
- status: **REAL adapter** (stdlib only; follows ../ADAPTER-CONTRACT.md)
- source skill: DeepScientist `science`
- entrypoint: `adapter:cards`
- input: (none; catalog.json)
- output: scientific package cards (numpy/scipy/pandas/...)
- catalog: catalog.json (8 cards)
- scope: **PARTIAL port** — 8 general scientific-Python cards only. DeepScientist's full 169-card domain catalog and its `artifact.science(...)` Science Evidence Graph are NOT ported (deferred; see the project memo). This pack is a routing-card stub, not the full `science` skill.
Disabled by default in `../../specs/state/seed.toml`; enable per quest/domain to consume it.
