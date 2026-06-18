# science-scipkg — Provenance

The `science-scipkg` pack vendors scientific-software package-routing cards derived
from the FermiLink `skilled-scipkg` catalog. It vendors **routing/knowledge pointers
only** — no solver runtimes, no package source trees. (See the repository `NOTICE`
for the consolidated upstream license/attribution.)

## Upstream source
- FermiLink repository: https://github.com/TaoELi/FermiLink
- Audited commit: `93f089a333a43089fb1a08a73c37d05fd6683214`
- Catalog channel: `skilled-scipkg`

## What is included (vendored here)
- `references/packages/*.md` — 169 package routing cards
  (package id, domains, tags, knowledge URL, source-archive URL, upstream URL).
- `references/package-index.min.json` — compact 169-package index (the source of
  truth the adapter's `cards()` surfaces).
- `references/domain-index.md` — progressive-disclosure domain index.
- `references/{package-check-playbook,hpc-via-bash-exec,claim-type-discipline,science-task-brief-template,artifact-science-tool}.md`.
- `references/science-evidence-graph.md` — the Science Evidence Graph contract,
  adapted to the Houmao record surface (see that file's header).

## What is NOT included
- The FermiLink runner / CLI / FastAPI backend / Chainlit UI / HPC profile manager.
- Package source trees from `github.com/skilled-scipkg/*`.
- Scientific solver runtimes or compiled executables.
- Any guarantee that a package can run in the user's environment — the cards are
  routing and knowledge pointers only.

## Houmao runtime boundary
Science evidence is recorded via the `$HARNESS record apply` surface
(`experiment`/`result`/`measurement`/`analysis`/`claim`) per
`references/science-evidence-graph.md`. If a quest downloads a package knowledge base
or scientific source from an upstream URL, it must preserve that URL and its license
context in its own `runs/<quest-id>/` evidence files / DB records.
