# Packs

## Purpose

Built-in optional `knowledge_pack` adapters (ported DeepScientist domain/publication helpers). Registered
in `../specs/state/seed.toml` but **disabled by default** so the core platform stays domain-neutral;
enable per quest/domain to activate the matching harness command / stage helper. All packs here ship a
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
