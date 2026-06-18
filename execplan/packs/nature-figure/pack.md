# Pack: nature-figure

- kind: compiler
- backs: render figure
- status: **REAL adapter** (stdlib only; follows ../ADAPTER-CONTRACT.md)
- entrypoint: `adapter:render`
- input: CSV/JSON data
- output: Nature-style .svg (Wong palette, despined axes, panel label, Arial)
- example input: examples/sample.csv
Enabled by default in `../../specs/state/seed.toml` (nature-domain publication set); disable per quest/domain if not needed.

## Methodology references
Read before plotting: `references/figure-contract.md`, `qa-contract.md`, `design-theory.md`, `backend-selection.md`, `chart-types.md`. Fill the figure contract + run the QA checklist around the adapter call. Also: `r-workflow.md`, `r-template-index.md`, `api.md`, `tutorials.md`, `nature-2026-observations.md` (R backend + API + tutorials + venue observations).

These references use external tool names (`artifact.*`, `memory.*`, `bash_exec`); map them to the Houmao `$HARNESS <group> <verb>` surface (`record apply`, `knowledge`, `state query`). The pack is the source of truth; the loop drives it via `render figure`.
