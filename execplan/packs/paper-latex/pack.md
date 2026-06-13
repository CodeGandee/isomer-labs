# paper-latex — publication-grade `render report` (Markdown → LaTeX → PDF)

**Kind:** compiler · **Backs:** `render report` · **Entry:** `adapter:render` · **Out:** PDF (+ `.tex`)

The publication override of the default Markdown `render report`. When enabled, the Writer's
`$HARNESS render report` produces a compiled **LaTeX article + PDF** instead of raw Markdown — the single
biggest step toward DeepScientist-grade deliverables.

## What it does
- Compiles a Markdown manuscript draft (`--input`) to a LaTeX article and a **compiled PDF** (`--ref`),
  writing the intermediate standalone `.tex` alongside.
- Auto-detects the toolchain: `pandoc` (or `pypandoc`'s bundled binary) + a LaTeX engine
  (`xelatex`/`pdflatex`/`lualatex`, system **or** a TinyTeX install under any home).
- **Citations:** pass `params.bib` (a `.bib` produced by `$HARNESS lit bib`) → resolved via `--citeproc`.
- **CJK:** if the draft contains Chinese/Japanese/Korean text, compiles with `documentclass=ctexart`.
- **Unicode math glyphs** (`≤ β κ ×`): uses a glyph-rich main font (DejaVu Serif / TeX Gyre Termes) when present.
- **Always records an artifact:** if no LaTeX toolchain is found (or a compile fails), it emits a
  standalone `.tex` and reports `format:"tex"` with a hint — the stage never hard-fails.

## Inputs / params
| arg | meaning |
|---|---|
| `--input` | Markdown manuscript draft (Writer's assembled paper, with figure includes + tables) |
| `--ref` | output PDF path (a sibling `.tex` is written too) |
| `params.title` | manuscript title (optional; else taken from the draft) |
| `params.bib` | path to a `.bib` for `\cite` resolution (optional) |
| `params.engine` | force `xelatex`/`pdflatex` (optional; default auto) |

## Return
`{ok, out_path, format: "pdf"|"tex", summary, meta:{engine, pandoc, tex_path, bytes, cjk, mainfont}}`

## Activation
Enabled in `seed.toml` (general/compiler, priority 90). Because resolution is **command-aware**
(`backs = ["render report"]`), it wins `render report` regardless of other enabled compiler packs
(`paper-plot` backs `render plot`, etc.), so there is no priority clash.

## Upgrade path
Drop a richer `adapter.py` at this ref (e.g. a structured claims→sectioned-LaTeX generator with a venue
template) to raise quality further — no harness/contract change.
