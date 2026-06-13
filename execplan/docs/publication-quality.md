# Publication-grade output (parity with DeepScientist)

The write→review→finalize path now produces a **submittable paper package**, not a bare Markdown report.
This is the gap-closing layer identified by comparing q1's output to the DeepScientist counterpart.

## What's enabled
Publication knowledge packs are **on by default** (`specs/state/seed.toml`), resolved command-aware via
each pack's `pack.toml` `backs`:

| Command | Adapter (pack) | Output |
|---|---|---|
| `render report` | **paper-latex** (general, prio 90) | Markdown draft → **LaTeX article + compiled PDF** (XeLaTeX/TinyTeX auto-detect; `--bib` citations; CJK-aware; `.tex` fallback) |
| `render plot` | **paper-plot** (general, 100) | publication SVG figure from CSV/JSON result data |
| `render polish` | figure-polish (general, 110) | figure QA |
| `render figure` / `render slides` | nature-figure / nature-paper2ppt (**nature** domain) | venue figures / PPTX (bind only when `quest.domain="nature"`) |
| `manuscript polish` / `manuscript datastmt` | nature-polishing / nature-data (**nature** domain) | English polish / Data Availability |

(Strict resolution: a pack serves only the commands it `backs`; a command with no enabled backing pack
falls back to the generic stub — it never mis-binds an unrelated adapter.)

## New harness commands
- `lit bib --quest-id <q> --out runs/<q>/refs/references.bib` — BibTeX from recorded `reference` rows; the
  paper-latex `--bib` resolves `\cite`/[@key].
- `manuscript bundle --quest-id <q> --out-dir runs/<q>/report` — emits **evidence_ledger.md**,
  **claim_evidence_map.json**, and an auto-derived **submission_checklist.md** (figures present? compiled
  PDF present? every supported claim has evidence? no orphans?) — the DeepScientist-style audit bundle.

## Loop behavior (skills)
- **Writer (`write`)**: figures (`render plot`) → bibliography (`lit bib`) + Related Work → assemble a
  full Markdown manuscript (intro+contributions, method, setup, results+figures+tables, ablation, analysis,
  related work, limitations, conclusion) → compile (`render report` = paper-latex) → `manuscript validate`
  → `manuscript bundle`.
- **Analyst (`analysis`)**: run an **ablation / mechanism-isolation** when the result space admits it, so
  the paper can isolate the operative mechanism (the main rigor gap vs DeepScientist).
- **Outline**: paper-view + evidence-view + an ablation plan; gated by `outline validate`.
- **Reviewer (`review`)**: adversarial "objections raised → answered", reference audit, and a
  submission-checklist confirmation.
- **Orchestrator finalize gate**: `complete` is blocked until a **compiled PDF**, **≥1 figure**, a
  **bibliography**, and a **clean submission bundle** (no orphan supported claims, `evidence validate` clean)
  all exist; otherwise it routes back to `write`.

## Bilingual output (EN + ZH)
Every quest produces a **Chinese edition** alongside the English paper. The Writer translates the assembled
draft to `paper-zh.md` (preserving tables/numbers/formulas/figures/citations; technical proper nouns stay in
English) and compiles it with the same `render report` — paper-latex auto-detects CJK and uses `ctexart`.
The finalize gate requires `paper-zh.pdf`, and `submission_checklist.md` tracks "Chinese edition present".
CJK compilation needs `ctex`/`xecjk`/`fandol` in the LaTeX toolchain (TinyTeX: `tlmgr install ctex xecjk fandol`).

## Verifying parity on a new quest
After finalize, `runs/<q>/report/` should contain: `paper.pdf` (+ `paper.tex`), **`paper-zh.pdf` (+ `paper-zh.md`)**,
`figures/*.svg`, `refs/references.bib`, `evidence_ledger.md`, `claim_evidence_map.json`,
`submission_checklist.md`, and a `review/` note — matching the DeepScientist `paper/` package shape (LaTeX +
figures + bib + ledger + checklist + reviewer pass) **plus a bilingual EN/ZH paper**.

## Toolchain note
PDF compilation needs `pandoc` + a LaTeX engine. The adapter auto-detects a system install or a TinyTeX
under any home (and `pypandoc`'s bundled pandoc). If absent, it emits a standalone `.tex` and the finalize
gate will hold at `write` until a PDF is producible — install `pandoc` + TinyTeX (with `ctex`/`xecjk`/
`fandol` for Chinese) to enable end-to-end PDF.
