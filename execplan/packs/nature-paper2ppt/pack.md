# Pack: nature-paper2ppt

- kind: compiler
- backs: render slides
- status: **REAL adapter** — emits a true `.pptx` (follows ../ADAPTER-CONTRACT.md)
- entrypoint: `adapter:render`
- input: outline JSON or Markdown
- output: a real **`.pptx`** 16:9 deck (one slide per outline section: title, bullets, speaker notes,
  embedded hero figure + source label)
- example input: examples/outline.json
Enabled by default in `../../specs/state/seed.toml` (nature-domain publication set); disable per quest/domain if not needed.

## Output package (written alongside the deck at the `--ref` dir)
- `<ref>.pptx` — the deck (primary deliverable)
- `qa_report.md` — reopen/inspect QA: slide count, embedded-media count, speaker-note count
- `asset_manifest.md` — figure traceability (asset → slide → source → extraction method), when figures are used
- `assets/figures/` — PDF-extracted figure crops (when a source PDF is supplied)

## Optional dependencies (graceful degradation)
- **python-pptx** (primary): produces the real `.pptx`. If unavailable at runtime, the adapter falls back
  to a self-contained **HTML deck** at the same `--ref` (no contract change; mirrors `paper-latex`).
- **PyMuPDF / `fitz`** (figure extraction): extracts embedded images from a source paper PDF
  (`paper_pdf`). If absent, PDF extraction is skipped and the adapter uses figures already under
  `runs/<quest>/figures/` (or an explicit `figures_dir`).
- **Pillow** (already available): used for figure aspect-ratio fit when laying figures on slides.

Declare both in `pack.toml` `deps`. Neither is a hard requirement — every path still records an artifact.

## Input schema
JSON: `{"title", "author", "paper_pdf"?, "figures_dir"?, "slides": [{"title", "bullets":[...], "notes"?,
"figure"?, "caption"?, "takeaway"?, "source"?}]}`.
Markdown: `# Deck title`, `## Slide title`, `- bullet`, `> speaker note`, `![](figure.png)`.

## Deck procedure
`references/procedure.md` — Toolchain Policy, Lean Operating Mode, two-pass Default Fast Path,
figure-extraction + asset-manifest mechanics, render/inspect/verify QA, the 6 paper-type archetype arcs,
Nature-style page composition, citation rules, the output-files package spec, and fallback rules.
Preserves the argument spine, 12–16 slide structure, and per-slide schema.
