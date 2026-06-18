# Packs

## Purpose

Built-in `knowledge_pack` adapters (domain/publication helper packs). Registered in
`../specs/state/seed.toml`; the **publication set is ENABLED by default** (paper-latex, paper-plot,
figure-polish, and the nature-* figure/slides/data/polishing packs) so output quality matches the reference counterparts. `science-scipkg` is enabled; only `mentor-standards` stays
**disabled** (the core control plane remains domain-neutral — packs only add render/manuscript adapters).
Enable/disable per quest/domain to change the matching harness command / stage helper. All packs here ship a
**real stdlib adapter** (`adapter.py`) plus a committed `examples/` input+output; see `ADAPTER-CONTRACT.md`
for how the harness loads and consumes them.

## Directory README exception (validate-execplan)

Each pack directory and its `examples/` are **self-documenting** and therefore intentionally omit a local
`README.md`: a pack dir carries `pack.toml` (machine manifest) + `pack.md` (human description) + an
`adapter.py`, and `examples/` holds the sample input/output named in `pack.md`. This `packs/README.md`
indexes the whole subtree. This is the same exception applied to generated skill dirs (self-documented by
`SKILL.md`). So `validate-execplan` / the readiness gate treat `packs/<name>/` and `packs/<name>/examples/`
as covered, requiring no per-directory README.

## Contents

- `ADAPTER-CONTRACT.md` — the pack adapter contract (layout, manifest, entrypoint, harness boundary).
- `paper-plot/` — compiler adapter (`render plot`): CSV/JSON → SVG. Reference implementation.
- `figure-polish/`, `nature-figure/`, `nature-paper2ppt/` — real compiler adapters (`render polish|figure|plot|slides`).
- `nature-data/`, `nature-polishing/` — real template adapters (`manuscript datastmt|polish`).
- `science-scipkg/` — reference catalog (FermiLink scipkg package cards).
- `mentor-standards/` — reference (repo-owner standards/taste, read by deepresearch-mentor).
