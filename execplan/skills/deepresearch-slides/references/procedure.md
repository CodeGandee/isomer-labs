# Nature-style paper→PPTX procedure

Build a complete but efficient Nature-style **simplified-Chinese** deck from a paper / preprint / PDF /
article text / abstract + figure legends / reading notes. The deliverable is a **real `.pptx`** (the
Houmao adapter emits one via python-pptx; it falls back to a self-contained HTML deck only when
python-pptx is unavailable). This file is both the authoring spec for slide content + figure logic and the
porting spec for the adapter pipeline.

The skill must NOT stop at an outline or talk script. The expected end product is a real `.pptx` deck plus
lightweight verification. Keep supporting files minimal unless the user asks for more traceability.

## Core principle — argument spine (answer before building)
Use the paper's scientific argument as the presentation spine; do not copy the paper's section order. The
default slide logic should let the audience answer, in order:
1. Why does this problem matter?
2. What gap / bottleneck does the paper address?
3. What did the authors do?
4. What is the key evidence?
5. Why should we trust the result?
6. What is new, reusable, or broadly meaningful?
7. Where are the boundaries and open questions?

## Lean Operating Mode
Default to the lowest-overhead workflow that still produces a usable PPTX. **Do:** read only the source
needed to understand the argument; extract only figures/tables that will actually appear; create the PPTX
as the primary deliverable; run lightweight structural checks on the package; write a short QA report.
**Avoid by default:** exhaustive extraction of every figure/page/table/supplement; full OCR unless text
extraction fails or the PDF is scanned; saving full raw extracted text; installing broad document suites;
GUI/desktop automation for previews; long markdown scripts when only a deck is needed; rendering every
slide when no reliable headless renderer exists.

## Toolchain Policy
Cross-platform Python-first stack (works on macOS, Linux, Windows):
- **PyMuPDF (`fitz`)** — metadata, text extraction, page rendering, page-level crops, embedded-image extraction.
- **Pillow** — figure crops, contact sheets, lightweight preview images, aspect-ratio fit.
- **python-pptx** — slide authoring and PPTX-safe editing (the real `.pptx`).
- **zipfile + a reopen pass through python-pptx** — package validation.

Use `pathlib` paths, project-local output dirs, and Office-safe / theme fonts. Do not hardcode OS font
paths or platform-specific locations. Treat LibreOffice/`soffice` as optional (only if already present and
a real rendered preview is worth the cost). Avoid Keynote/PowerPoint desktop automation, AppleScript,
Preview, Finder, `open`, and OS-specific font/path deps. Prefer previews from extracted slide objects/assets
over re-rendering the whole deck. Ask or document the tradeoff before expensive extras (full supplementary
processing, high-res recreation of many figures, full slide-by-slide rendered QA, very long decks).

## Accepted inputs
Full paper PDF; supplementary figures/tables; Word/Markdown-converted text; abstract + results + figure
legends; structured reading notes; pasted article content; an `input/source.md`; a user-provided PPTX
template. Default output language is **simplified Chinese** unless the user requests otherwise; preserve
technical terms, abbreviations, gene/protein names, model/dataset names, equations, and statistical terms
in English where Chinese would reduce precision.

## Default Fast Path (two-pass PDF reading)
For a normal selectable-text paper PDF, run the shortest complete path:
1. Extract metadata, abstract, headings, figure legends, table captions with PyMuPDF.
2. Identify paper type, argument, and candidate figures BEFORE rendering high-res pages.
3. Render low-res contact sheets only when figure locations are unclear.
4. Render high-res images only for selected figure/table pages; crop only assets that will appear.
5. Build the PPTX directly with python-pptx (native tables/charts when values are explicit; figure crops
   when the original visual carries the evidence).
6. Verify by reopening the PPTX and inspecting package structure; render slide previews only if a reliable
   cross-platform headless renderer is already available.

**Two-pass reading:** first capture metadata, abstract, headings, figure legends, table captions; then read
only the result/methods pages needed to support the slides. OCR, full supplementary extraction, all-page
high-res rendering, all-slide rendered QA, and long script files are opt-in exceptions, not defaults.
Do not invent missing numbers, mechanisms, datasets, or figure details.

## Step 1–3. Read → classify → plan

### Step 1 (extract source material)
When available: title, authors, journal/server, year, DOI; field/subfield; paper type; central problem and
gap; main claim/thesis; study design/workflow/model/dataset/system; key methods and controls; main results
and quantitative findings; key figures/tables/legends; validation/robustness/ablation/sensitivity; limits
and unresolved questions; broader meaning.

### Step 2 (classify before designing)
Pick the closest paper type — discovery/mechanism; translational/applied; clinical/population;
methods/algorithm/tool; resource/dataset/atlas; omics/single-cell/spatial/multimodal; materials/chemistry/
engineering performance; environmental/ecological/earth-system; benchmark/evaluation; review/perspective;
meta-analysis. Then pick a presentation logic: `claim-first` (one strong central claim);
`question-to-evidence` (mechanism/discovery); `problem-to-solution` (methods/tools/engineering);
`workflow-to-validation` (datasets/atlases/omics/benchmarks); `evidence-map` (reviews/perspectives).

### Step 3 (Chinese presentation plan — 12–16 slides)
Default length 12–16 slides for a 15–20 min report. Default structure:
1. 标题页
2. 研究背景：为什么这个问题重要
3. 知识缺口 / 技术瓶颈
4. 论文核心问题与主张
5. 研究设计 / 技术路线 / 分析框架
6. 关键证据①
7. 关键证据②
8. 关键证据③
9. 验证、对照或稳健性证据
10. 机制模型 / 方法优势 / 综合框架
11. 创新点与可复用价值
12. 局限性与未解决问题
13. 总结与讨论

Adapt to the paper type; do not force every paper into one template. For a quick/unspecified request prefer
10–14 slides; expand past 16 only for a detailed seminar deck or when the paper genuinely needs the space.

## Step 4–5. Figure extraction + asset-manifest mechanics

### Step 4 (select figures as evidence, not decoration)
Inspect for: graphical abstracts/summary models; design/workflow diagrams; central result figures;
microscopy/imaging panels; heatmaps/dim-reduction/networks/maps/spatial plots; survival/forest/calibration/
statistical plots; materials characterization & performance plots; architecture/benchmark/ablation/error
figures; key tables; validation/control figures. Prioritize figures that carry the argument: (1) design/
workflow, (2) main evidence, (3) validation/robustness, (4) mechanism/model/synthesis, (5) implication.
Prefer a few readable key panels over many unreadable full figures (**select only story figures / a hero
panel per slide**).

### Step 5 (extract + prepare assets)
When the source has usable figures: extract original images from the PDF/source package, but only for
selected figures; render high-res page images only for pages with selected figures/tables; crop dense full
figures to relevant panels; keep original data visuals unchanged; save under `assets/figures/`; use clear
filenames (`fig1_workflow.png`, `fig2b_main_result.png`, `fig4ef_validation.png`); record source page,
figure number, panel, crop status, and intended slide in **`asset_manifest.md`**. For a 10–14 slide deck,
usually select 4–8 figure/table assets. For tables/simple quantitative comparisons prefer editable
PPT-native tables/charts when values are explicit; use table screenshots only when recreating would risk
transcription errors or layout itself is the evidence. If extraction fails, fall back to a rendered page
screenshot with careful crop, a recreated editable table (only when values are explicit), or a clearly
labeled placeholder (only when the visual is unavailable).

### Adapter mechanics (how the render adapter implements Step 4–5)
- PDF figure extraction via PyMuPDF (`fitz`): iterate pages, pull embedded images by `xref`, skip tiny
  assets (`< 120×90` px or `< 30000` px²: logos/rules/bullets), CMYK→RGB convert, save as PNG under
  `assets/figures/`, then sort hero-first by pixel area. Degrades to **skip** (`fitz-absent`) when PyMuPDF
  is missing and (`no-pdf`) when no readable PDF is supplied.
- On-disk pool: figures already under `runs/<quest>/figures/` (or an explicit `figures_dir`) are used
  regardless of PDF extraction — this is the graceful path when `fitz` is absent.
- Selection/placement: honor explicit per-slide `figure` references first; then auto-assign remaining
  story figures (pool first, then PDF-extracted; both hero-first) to body/evidence slides that lack one
  (skip the cover and already-figured slides). Aspect ratio is fit via Pillow so figures are not distorted.
- `asset_manifest.md` is written **alongside the deck** (beside `qa_report.md`) with columns: asset, slide,
  slide title, source, how (explicit/auto). Omitted when no external figure/table assets are used.

## Step 6. Slide-by-slide content
For each slide write: Chinese title; slide purpose; suggested layout; 3–4 concise Chinese bullets; the
selected figure/table asset (if any); Chinese caption + interpretation; one core takeaway sentence; a
concise Chinese speaker note when oral explanation helps. Each slide makes ONE point. Result slides answer:
what does this figure show? why does it matter for the claim? what should the audience believe after seeing
it? Keep speaker notes useful but concise; do not narrate self-explanatory slides.

**Per-slide schema:** `{中文标题, purpose, layout, 3–4 bullets, figure_asset, caption, takeaway, speaker_note}`
(adapter JSON keys: `title, bullets, notes, figure, caption, takeaway, source`).

- **Evidence hierarchy on a slide:** (1) hero figure / main table crop, (2) narrow interpretation rail or
  short annotation band, (3) only the minimum labels to read the evidence, (4) deeper explanation moves to
  speaker notes or the next slide. The interpretation block must not become as large/loud as the evidence.
- **Layout adaptation rule:** do NOT default to a fixed 50/50 split. Choose layout from the figure's aspect
  ratio, density, and role — full/near-full-width for wide/complex/main-evidence figures; tall image + a
  narrow text rail for vertical figures or short captions; top/bottom stack when the figure needs horizontal
  room; asymmetric 70/30, 75/25, 65/35 when one side dominates; compact visual-plus-callout for a few
  annotations; a crop instead of shrinking a dense graphic. Treat 1:1 layouts as the exception. (The render
  adapter renders an asymmetric hero layout: figure ≈62% on the left, narrow interpretation rail on the
  right; text-only slides get a full-width body.)
- **Slide archetype defaults:** Cover — one dominant visual/typographic idea, no balanced split. Background/
  problem — short setup + one compact context visual. Workflow/method — full-width or top-to-bottom process
  diagram. Result/evidence — one dominant figure/table crop + narrow interpretation rail. Comparison/table
  — full-width table, or split across slides if cramped. Model/summary — a large central model + a brief
  takeaway strip. Conclusion/discussion — text-led, open, 2–4 bullets, no unnecessary containers.
- **Title writing rule:** conclusion-style titles that state the slide's point, not its topic (prefer
  "PathAgent 主动识别信息不足并补充证据" over "Case Study" or "Figure 3").
- **Visual density rule:** never downscale a dense figure/table/multi-panel graphic into a tiny slot for
  symmetry; if it cannot be read at presentation scale, crop, split, or give it its own slide.

## Step 7. Build the actual PPTX deck
Create a real `.pptx` as the primary deliverable, with python-pptx as the default authoring tool (editable;
cross-platform). Use a user-provided PPTX template if supplied. The PPTX should: use 16:9 widescreen;
include the selected original figures; use Chinese titles/bullets/captions/speaker notes; include source
labels on figure slides; keep slide text concise; avoid text-only result slides when visuals exist;
maintain consistent typography, spacing, titles, captions, and transitions. Use compact, evidence-first
composition; avoid rigid two-column templates and balanced 1:1 scaffolds; let geometry follow the figure.
When a slide has one dominant figure, let it own the page; keep the rail narrow; push secondary explanation
to speaker notes or a follow-up slide.

## Step 8. Render, inspect, and verify (QA)
After creating the PPTX, render previews only when a reliable headless renderer is readily available. If
previews exist, inspect for: missing images; distorted/low-res figures; unreadable panels; text overflow;
overlapping captions/bullets/figures; excessive bullet density; wrong slide order; missing source labels;
missing/unhelpful speaker notes. If no reliable renderer exists, perform lightweight verification instead:
- **reopen the PPTX with the generation library**,
- check **slide count**,
- check **embedded media count**,
- check **speaker-notes presence** when notes were planned,
- check obvious shape bounds if tooling supports it,
- create a contact sheet from selected assets only if helpful (not a full-deck screenshot set).

Revise obvious defects; document any remaining limitation in **`qa_report.md`**. (The render adapter
reopens the produced `.pptx` via python-pptx, counts slides + speaker-noted slides, counts embedded media by
inspecting `ppt/media/` in the OOXML zip, and writes `qa_report.md`. No headless renderer is used.)

## Paper-Type Guidance (archetype arcs)

### Discovery / mechanism papers — question-to-evidence arc
1. phenomenon and importance, 2. unknown mechanism, 3. hypothesis/question, 4. experimental design,
5. evidence chain, 6. model, 7. limitations and next experiments.

### Methods, AI, tool, or algorithm papers — problem-to-solution arc
1. current bottleneck, 2. proposed method, 3. workflow/architecture, 4. evaluation design,
5. performance vs baselines, 6. ablation/robustness/failure cases, 7. reuse scenarios and limitations.

### Resource, dataset, atlas, omics, or benchmark papers — workflow-to-validation arc
1. why the resource is needed, 2. dataset/cohort/sample design, 3. generation + QC workflow,
4. main landscape/map, 5. validation and reproducibility, 6. example biological/technical insights,
7. access, reuse, and boundaries.

### Clinical, population, or intervention studies — design-to-inference arc
1. clinical/public-health problem, 2. study question, 3. cohort/trial/design, 4. endpoints and variables,
5. primary result, 6. subgroup/sensitivity/secondary analyses, 7. bias, limitations, practical implication.

### Materials, chemistry, physics, engineering papers — design-to-performance arc
1. target property/technical challenge, 2. design principle, 3. synthesis/fabrication/setup,
4. characterization, 5. performance evidence, 6. mechanism / structure–property relationship,
7. scalability, stability, or application boundary.

### Reviews and perspectives — evidence-map arc
1. why the topic matters now, 2. conceptual framework, 3. theme 1, 4. theme 2, 5. theme 3,
6. controversy / unresolved problem, 7. author's synthesis, 8. future directions.

## Style Rules
Restrained Nature-style academic design: clean white / very light background; dark readable text; one or
two muted accent colors; compact but not crowded layouts; figure-first result slides; concise captions; no
decorative stock images; no decorative gradients; no exaggerated marketing-style section pages. Chinese
suitable for oral academic reporting: avoid rigid translation, long paragraphs, jargon stacking; preserve
technical terms where Chinese would reduce precision; prefer evidence-based interpretation over vague
praise. Treat each slide like a publication figure page: one dominant idea, one clear evidence hierarchy,
asymmetry when the story needs it.

### Nature-style page composition
- Prefer one hero visual per slide when evidence is complex or the claim is central.
- Use asymmetric layouts by default when visual and text are not equally important.
- Keep gutters real and tight; use whitespace to separate roles, not to build a balanced grid.
- Use small panel labels (`a`, `b`, `c`) for multiple visual subpanels; direct labels or a shared legend
  strip when categories repeat across panels.
- Reuse one restrained palette across a slide/slide-family; reserve green/red for gains/drops/direction.
- If a slide has a schematic and data, let one dominate and the other validate.
- Use dark backgrounds only when the dominant visual is an image plate; keep normal chart slides light.
- Avoid decorative boxes, fake cards, symmetrical two-column scaffolds unless content truly calls for them.
- If a figure becomes unreadable when scaled down, crop it, split it, or move it to its own slide.

## Citation and Attribution Rules
Include source info: title slide — paper title, authors if useful, journal/server, year, DOI if available;
figure slides — small labels such as `Source: Fig. 2b, Nature, 2024`; adapted/redrawn content — label as
`整理自` or `改绘自`; do not remove original figure labels or alter scientific data. (The adapter renders a
slide's `source` field as a small italic "Source: …" label under the figure.)

## Output Files (package spec)
Generate a minimal but complete package by default:
1. **`final_presentation_cn.pptx`** (here: the `--ref` `.pptx`) — the main deliverable: a complete Chinese
   deck with figures, captions, takeaways, source labels, and speaker notes.
2. **`qa_report.md`** — PPTX creation status, slide count, figures inserted, missing/placeholder figures,
   verification method used, known limitations, manual follow-up if needed.
3. **`assets/figures/`** — extracted/cropped figure assets used in the deck.
4. **`asset_manifest.md`** — figure traceability (asset filename, original figure/panel, source page/file,
   extraction method, slide placement, quality notes), generated only when external figure/table assets are
   extracted. If none are extracted, omit it or write a one-line note in `qa_report.md`.

Optional (only when they materially reduce back-and-forth, help verify a complex paper, or are requested):
- **`ppt_outline_cn.md`** — paper info, paper type, central argument, slide structure, slide purpose.
- **`figure_plan.md`** — figure/panel, what it shows, why it matters, recommended slide, Chinese caption,
  interpretation.
- **`ppt_script_cn_with_figures.md`** — slide-by-slide script: `## Slide X. [中文标题]` with Purpose,
  Layout, On-slide bullets, Figure/Table, Chinese caption, Core takeaway, Speaker note.
- **`rendered/`** — rendered slide previews, only when a reliable headless renderer is available or the user
  requests visual QA.

Skip the optional outline/script/figure-plan files by default.

## Quality Rules
Build the `.pptx` whenever tooling is available; do not stop at a markdown outline/script; do not fabricate
results/methods/numbers/figure details; do not add expensive steps unless they improve the deck or were
requested; do not overload slides with text; do not make result slides text-only when figures are
available; make every slide serve the argument; ensure figures are readable at presentation scale; ensure
text/captions/figures do not overlap; document uncertainty and missing source material clearly.

## Fallback Rules
If only partial content is available: still create a useful PPTX structure; clearly mark uncertain slides or
missing details; use placeholders only when a required figure is unavailable; do not invent exact values or
claims; write `qa_report.md` explaining what could not be verified.

If PPTX tooling is unavailable: the render adapter emits a **self-contained HTML deck** at the same `--ref`
(figures embedded as `file://` URIs, same per-slide content, asset_manifest still written) so the output
stays structured enough for a downstream PPTX builder to run without re-reading the paper. More generally:
generate a concise outline + figure plan, prepare figure assets if possible, and explain why the PPTX could
not be built in the current environment.
