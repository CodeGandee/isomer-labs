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

## Scholarship bar (Related Work & citations)

> **Status note (Upgrade 1 shipped):** this bar is now **enforced**. `$HARNESS lit audit --quest-id <q>`
> checks it; the Reviewer **blocks** (`revise`) on a failing audit; and the harness **hard-gates** a
> `complete` finalize on it (`records.py::_finalize_scholarship_gate`). The hard teeth are: ≥ `min_refs`
> reference rows AND ≥1 claim positioned against a reference (`claim_evidence source_kind='reference'`).
> Thresholds are tunable via env (`DEEPRESEARCH_SCHOLARSHIP_MIN_REFS`, `DEEPRESEARCH_SCHOLARSHIP_MIN_REF_CLAIMS`;
> both `0` waives). "Academic vs. tool-doc" quality and Related-Work *positioning* remain Reviewer judgment
> (surfaced as `lit audit` warnings), since the harness cannot reliably classify a citation's nature.

A submittable paper is **positioned against external prior art**, not just internally consistent. The most
common shortfall (observed on a real quest) is a "Related Work" section that is actually a *provenance note*
— pointers to the quest's own runs, files, and evidence ledger — plus a bibliography of three tool-doc URLs.
That fails the bar.

**Genuine Related Work vs. internal provenance.**
- **Related Work (required):** situates *this* contribution against what *others* have done — prior methods,
  competing approaches, the closest baselines — and states the *delta* (how this work differs, improves, or
  complements them), each grounded in a real external citation.
- **Internal provenance (necessary but not Related Work):** the evidence ledger, claim→evidence map,
  artifact paths, and data-availability note. These document *your own* trail and belong in the appendix /
  reproducibility section — they do **not** count as scholarly positioning.

**Minimum expectations.**
- **Real external academic sources.** Peer-reviewed papers, preprints, books, or standards, each with a
  **resolvable identity** (DOI / arXiv id / stable URL), recorded via `lit fetch --source arxiv|doi|web`
  (not `manual` stubs). The bar is about the *source being real external literature* — `lit audit` flags a
  bibliography that is entirely `source='manual'` as a likely tool-doc-only list.
  *(Note: the current `lit bib` renders every entry as BibTeX `@misc`; richer typed entries
  — `@article`/`@inproceedings` with author/venue/year — need extra reference fields and are a tracked
  generator upgrade, not part of the enforced bar. See `execplan/packs/paper-latex/pack.md`.)*
- **Tool/infra docs are method citations, not positioning.** Vendor guides, profiler docs, a GitHub repo are
  legitimate to cite for *method/tooling*, but they do **not** count toward the scholarly-positioning
  minimum.
- **Citation quality.** Each citation supports a *specific* statement (background, a prior method, a
  comparison), is *resolvable* (DOI / arXiv / stable URL), and was actually read — no hallucinated or padded
  references.
- **Claim-to-reference linkage.** The novelty/positioning claims should be evidence-backed by references
  (the platform models this as `claim_evidence` with `source_kind='reference'`), so "we build on / differ
  from X" is traceable, not rhetorical.
- **A Related Work section** that groups prior art and states the contribution's delta.

**Enforced floor (tunable, domain-aware):** ≥ `min_refs` real reference rows **and** ≥1 reference-backed
positioning claim (the `lit audit` / finalize-gate teeth); a Related Work section is expected (warned when
absent). Defaults are modest (`min_refs=3`, one reference-backed claim) and tunable via the env knobs above;
the per-quest research contract (`execplan/docs/research-contract.md`, dimension 6) may raise the bar. The
minimum should scale with the quest's stakes and domain — a focused study cites fewer than a flagship one.

**Anti-pattern (fails the bar):** a bibliography of only tool/vendor docs (e.g. three vendor guides + one
repo, all `source='manual'`) and a "Related Work" that only lists internal artifact paths — and **zero**
claims linked to a reference. **Target:** a Related Work that engages the actual literature (the relevant
prior methods/results in the field) with real, resolvable, claim-linked citations.

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
