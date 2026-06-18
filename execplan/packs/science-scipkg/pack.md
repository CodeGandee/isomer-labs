# Pack: science-scipkg

- kind: reference (science / HPC **domain** pack; surfaced via `knowledge cards` / `knowledge query`)
- backs: knowledge cards
- status: **REAL adapter** (stdlib only; follows ../ADAPTER-CONTRACT.md)
- entrypoint: `adapter:cards`
- input: (none; catalog.json)
- output: scientific package cards (numpy/scipy/pandas/...) via the catalog; the full 169-card
  routing set + the Science Evidence Graph contract live under `references/`.

> Purpose: scientific-software routing + science-evidence discipline for natural-science / HPC
> quests. Pick the right package, check it before treating it as usable, follow evidence-path
> conventions, and record a typed Science Evidence Graph.

## Contents

- `references/packages/` — **169** FermiLink skilled-scipkg package cards.
- `references/package-index.min.json` — compact index of the 169 cards (search this first).
- `references/domain-index.md` — grouping by scientific domain.
- `references/package-check-playbook.md`, `references/hpc-via-bash-exec.md`,
  `references/claim-type-discipline.md`, `references/science-task-brief-template.md`,
  `references/artifact-science-tool.md` — the operational reference set.
- `references/science-evidence-graph.md` — the Science Evidence Graph contract (the 6 node types with
  field specs, claim-type discipline, HPC-via-shell workflow), with a header mapping
  `artifact.science(node_type=...)` nodes onto the Houmao `$HARNESS record apply` surface
  (`computational_run/dataset_analysis/parameter_sweep` → `experiment`/`result`/`analysis`;
  `validation_result` → `measurement`/`analysis`; `claim` → `claim`). `package_check` has **no
  direct Houmao equivalent** and is advisory.

There is **no `artifact.science` runtime** on Houmao; the DB stays canonical and these references are
advisory craft. Map any external tool calls (`artifact.*`, `memory.*`, `bash_exec`) or paths
(`artifacts/.../`) to the `$HARNESS <group> <verb>` command surface + DB records (`record apply`) and
`runs/<quest-id>/...`. Upstream attribution: see `references/PROVENANCE.md`.

## Adapter

`adapter.py:cards()` reads the colocated `catalog.json` (8 general scientific-Python cards) and
substring-filters by `query`. The catalog is a fast inline shortlist; the full domain catalog is the
169-card set under `references/packages/` (browse via `references/domain-index.md` /
`references/package-index.min.json`). `examples/cards.json` is a sample of the catalog output.

## Index (references/)
- `science-evidence-graph.md` — the Science Evidence Graph contract (node types, claim discipline,
  HPC-via-shell) + the node→`$HARNESS` mapping header. **Read this first.**
- `packages/<package_id>.md` — 169 per-package routing cards.
- `package-index.min.json` — compact searchable index of the 169 cards.
- `domain-index.md` — cards grouped by scientific domain.
- `package-check-playbook.md` — environment checks before computed work.
- `hpc-via-bash-exec.md` — SSH / scheduler / queue / remote-log discipline through the shell.
- `claim-type-discipline.md` — computed / parsed / digitized / hypothesis discipline.
- `science-task-brief-template.md` — startup-brief shape (context, not a required `goal.md`).
- `artifact-science-tool.md` — the original `artifact.science(...)` field spec + examples.

Enabled in `../../specs/state/seed.toml` for the `science` domain; point `quest.domain` at it for
domain-scoped selection.
