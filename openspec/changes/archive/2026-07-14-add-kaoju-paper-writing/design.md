## Context

Kaoju currently ends at accepted survey synthesis: catalogs, claim status, field summaries, comparisons, and dossiers. Its pipeline has no writing procedure, its semantic registry has no manuscript or paper-build records, and its export helper only renders existing structured records. A request for a "final paper" therefore falls outside the owned workflow. The observed failure mode was an agent writing canonical-looking Markdown directly, skipping the required audit and research-record APIs, then invoking Pandoc with automatic numbering on already numbered headings and accepting the PDF after checking only that the file existed.

The platform already supplies the necessary lower-level concepts. Publication-facing output can use `document_build`, existing Execution Adapter Command Requests, worker-output policy, publication-facing Gate policy, Artifact and Run records, file refs, and Provenance Records. DeepSci also demonstrates the architectural split between a pipeline paper pass and a dedicated writing stage, but its inputs and profiles are specific to hypothesis-driven research and empirical analysis.

## Goals / Non-Goals

**Goals:**

- Give Kaoju one skill that owns paper contracts, reader-facing organization, citation state, manuscript revisions, document builds, PDF validation, and publication bundles.
- Expose that capability as a bounded `paper-pass` through `isomer-kaoju-pipeline` while keeping direct `isomer-kaoju-write` invocation valid.
- Reuse DeepSci's strongest writing disciplines while replacing empirical-paper novelty and experiment gates with survey-specific coverage, comparison, traceability, synthesis, and reporting gates.
- Make survey-paper quality inspectable as a contract-defined vector of measurements and findings rather than an unsupported claim of comprehensiveness or a single opaque score.
- Make `.tex` the publication manuscript source, prefer Tectonic for compilation, and let the LaTeX document class and compiler produce every section number.
- Preserve a strict boundary between audited survey meaning and publication representation.
- Make a compiled PDF insufficient for completion until structural, textual, visual, and provenance checks pass.
- Keep canonical state in managed JSON records while storing manuscript, bibliography, logs, previews, and PDF files through explicit file refs and worker-output policy.
- Reuse platform-neutral execution and Gate contracts, with no Kaoju-specific runtime or PDF CLI.

**Non-Goals:**

- Discovering sources, repairing evidence gaps, running experiments, or changing accepted claim verdicts during writing.
- Replacing DeepSci paper skills or migrating DeepSci profiles to Kaoju.
- Building a general-purpose typesetting service, browser editor, or submission portal.
- Guaranteeing conformance to every publisher template in the first implementation.
- Treating manuscript prose, a PDF, or a publication bundle as new Research Claim evidence.
- Requiring a method or theory novelty claim for a survey paper, or allowing the writer to manufacture one from presentation choices.
- Treating discovery saturation, source counts, or a composite quality score as proof that the literature universe is complete.
- Supporting Markdown-to-PDF as an accepted publication build path; Markdown can be an intermediate planning or intake format but is not the publication manuscript source.

## Decisions

### Use a dedicated writing skill and a pipeline procedure

Add `isomer-kaoju-write` as the capability owner and `paper-pass` as the orchestration recipe. The skill can be invoked for drafting or revision without rerunning a survey procedure. The pipeline command resolves context, checks prerequisites, dispatches the writing stage, applies build and Gate routing, and returns the existing Kaoju terminal report.

The alternative of expanding `isomer-kaoju-synthesize` was rejected because synthesis decides what the accepted evidence supports, while writing decides how to communicate that support to a target reader. Combining them would make presentation revisions look like evidence revisions. A subcommand without a dedicated skill was also rejected because it would leave no independently invokable owner for manuscript repair and rebuilds.

### Generate the LaTeX template as an editable derived artifact

Rather than shipping bundled venue templates or assuming host-provided templates exist, `isomer-kaoju-pipeline` exposes a public `create-paper-template` subcommand. The command generates a LaTeX template tree at `intent/derived/writing-template/<template-name>/`. `main` is the reserved default template name: when no name is specified, the command operates on `main`, and `paper-pass` resolves to `main` when no explicit template is named. Multiple named templates may coexist for different venues, paper types, or revision experiments, but there is only one default `main` template per topic at a time. The command compiles a proof-of-compilation PDF preview and writes a `README.md`. The generated files are an editable artifact: the user may modify them, and `paper-pass` consumes the latest accepted template ref before drafting. No dedicated Gate is opened for template edits; ordinary artifact revision semantics apply. Template generation failures are blockers, but accepted templates are not publication-facing output and therefore do not trigger the publication Gate.

Shipping bundled templates was rejected because of ongoing venue-specific maintenance. Relying solely on host-provided templates was rejected because it makes acceptance tests and CI non-deterministic. Treating the generated PDF as the final paper PDF was rejected because it would break the immutable `kaoju:paper-build-run` lineage.

### Expose templates through `isomer-cli ext research templates`

Template files under `intent/derived/writing-template/` are the canonical source, but the system also exposes a lightweight CLI surface under `isomer-cli ext research templates` for discoverability and automation. The CLI commands are `create`, `list`, `show`, `refresh`, `compile`, and `remove`. `create` and `refresh` generate files and compile a preview PDF; `list` and `show` read the template metadata record and file tree; `compile` re-runs the preview build without regenerating source; and `remove` archives the template record. The CLI reuses the transitional research record store for metadata, lineage, and provenance while keeping the file tree as the authoritative template content.

The alternative of a skill-only interface was rejected because users and CI need a stable way to list and inspect templates without invoking a full Kaoju skill. A generic `isomer-cli ext derived` namespace was rejected because the `research` extension already groups research-related derived artifacts and the command set is template-specific.

### Keep Kaoju writing independent of DeepSci records

The new skill follows the same architectural pattern as DeepSci paper writing but does not invoke `isomer-deepsci-write` or use DeepSci profiles. DeepSci expects analysis findings, experiment matrices, paper-outline placeholders, and DeepSci-specific binding rules. Kaoju instead consumes an accepted Audit Report and exact accepted Kaoju synthesis refs. Shared document-build mechanics remain platform capabilities and can later be factored into reusable guidance without cross-family record coupling.

### Adapt DeepSci writing practice to a survey-paper argument

The writer adopts DeepSci's evidence-first and reader-first disciplines: lock a paper contract, separate a reader-facing paper view from the evidence view, define one job for each section, map statements to accepted evidence, verify citations before use, plan tables and figures before prose, surround each display with its question and takeaway, keep implementation and audit detail out of the main narrative when an appendix can preserve it, calibrate conclusions, and perform a skeptical review before bundling.

The survey story is not an empirical novelty story. Its organizing spine is normally: why the surveyed area matters; what questions and scope the survey covers; how sources were discovered, identified, screened, and verified; what taxonomy or comparison frame makes the field legible; what the comparative evidence supports; where evidence conflicts or remains non-comparable; what gaps and limitations remain; and what a reader can responsibly conclude. The Paper Contract may name a taxonomy, dataset, synthesis, or comparative perspective as a contribution when accepted records support it, but readiness does not require a novelty claim.

Main survey sections receive explicit jobs. The introduction fixes motivation, audience, scope, questions, and contribution posture. Survey method reports discovery channels, cutoff, eligibility, screening, identity resolution, evidence depth, and known blind spots. Taxonomy or field map defines categories and boundary cases. Comparative study defines dimensions and comparability before presenting results. Synthesis interprets patterns, contradictions, negative evidence, and gaps without converting absence of evidence into evidence of absence. Limitations state coverage and method constraints. The conclusion answers the survey questions at the strength permitted by the accepted evidence.

### Measure survey-paper quality as a transparent profile

The Paper Contract defines applicable metrics, denominators, thresholds, warning policy, and `not-applicable` cases before publication validation. Every reported metric names its numerator, denominator or bounded population, exclusions, cutoff, source record refs, and unknown values. The validation report preserves the metric vector and qualitative findings; it does not collapse them into a single readiness score unless the contract defines and justifies weights, and a composite score can never replace a failed mandatory dimension.

| Quality Dimension | Required Measurements or Findings | Interpretation Boundary |
| --- | --- | --- |
| Protocol and scope coverage | Required scope cells covered, planned discovery channels executed, screening dispositions recorded, inclusion and exclusion accounting, temporal cutoff, and bounded discovery-saturation trend | Measures execution against the declared Survey Contract, not completeness of an unknowable literature universe |
| Source identity integrity | Included works with canonical identity and version posture, unresolved identities, duplicate or variant collapses, and inaccessible-source accounting | Counts unresolved identity as uncertainty and prevents variants from inflating coverage |
| Evidence adequacy | Paper claims meeting required verification depth, claims with exact source locators, primary-source use where required, and unresolved evidence blockers | Keeps source-stated, source-supported, executed, compared, contradicted, and inconclusive evidence distinct |
| Comparative-study soundness | Dimensions with operational definitions, comparison cells with comparability status, matched-depth comparisons, missing or non-comparable cells, normalization and fairness findings, and sensitivity to asymmetric evidence | A large matrix is not sound when methods were checked at different depths or under incompatible conditions |
| Traceability | Paper claims, citations, tables, and figures mapped to accepted records and source locators; citation keys and bibliography identities resolved | Measures whether a reviewer can audit each conclusion and display |
| Synthesis quality | Survey questions answered, taxonomy categories defined with boundary cases, contradictions and negative findings represented, gaps distinguished from missing search, and conclusions calibrated | Rewards useful organization and interpretation without inventing consensus or novelty |
| Balance and limitations | Material source-class, venue, time, provider, geographic, or method-family skews reported; audited limitations propagated into main conclusions | Reports observed imbalance and blind spots rather than hiding them behind aggregate counts |
| Reader-facing reporting | Section jobs are distinct, tables and figures state their question and takeaway, terminology remains consistent, methods are reproducible, and main-text detail is appropriately separated from appendices | Judges whether the survey is understandable and reviewable, not whether it sounds promotional |
| Document integrity | Numbering, citations, hierarchy, extracted text, layout, readability, accessibility, build provenance, and file integrity checks | Publication readiness still requires the separate rendered-document checks |

Each dimension receives `pass`, `warning`, `fail`, `not-applicable`, or `unknown` plus evidence and diagnostics. A mandatory `fail` or `unknown` yields `not-ready`; a warning is acceptable only under the Paper Contract and Gate rules. The profile may report counts and ratios, but it must keep the underlying missing, excluded, non-comparable, and unresolved cases visible.

### Introduce five publication-facing semantic records

The writing skill owns these semantics:

- `kaoju:paper-contract`: current target, audience or venue, survey questions, scope and contribution posture, evidence boundary, survey-quality metric definitions and thresholds, LaTeX document class and template ref, compiler-owned numbering and unnumbered-section policy, citation policy, display expectations, Tectonic-first build requirements, fallback policy, validation requirements, and accepted input refs. The template ref may point to a generated template produced by `create-paper-template` or to a user-supplied template.
- `kaoju:survey-manuscript`: current structured manuscript state, including reader-facing paper view, evidence view, outline, section jobs, claim-to-section mapping, citation ledger, comparison and display plan, `.tex`, bibliography, and included file refs, and revision notes.
- `kaoju:paper-build-run`: one immutable document-build attempt with source and template digests, command, engine, environment, warnings, logs, generated PDF and preview refs, terminal status, and Provenance Records.
- `kaoju:paper-validation-report`: one non-mutating assessment of a manuscript and build attempt, including the survey-paper quality profile plus structural, citation, compile, extracted-text, outline or table-of-contents, visual, accessibility, and file-integrity checks.
- `kaoju:publication-bundle`: the current navigable assembly of accepted contract, manuscript, build, validation, source, bibliography, PDF, limitations, and reproduction instructions.

The first two and the bundle are current-state records revised with history. Each build attempt and validation report is a separate descendant. Manuscript source, bibliography, logs, previews, and PDFs remain referenced files rather than embedded JSON or canonical state by themselves.

### Require accepted survey inputs before writing

`paper-pass` requires an accepted Audit Report plus the exact accepted synthesis records needed by the paper, normally a Field Summary, Claim Status Table, Related-Work Catalog, Source Digests or Claim-Evidence Ledger, and optionally a Kaoju Dossier or comparison records. Missing or ambiguous latest records produce `paused` or `blocked`, not ad hoc recovery from rendered Markdown.

Writing may reorganize, shorten, or restate accepted material, but it cannot strengthen verdicts, hide audited limitations, or add unsupported literature claims. A detected evidence gap routes back to the owning Kaoju stage and records a resume point.

Before drafting, the writer converts the accepted survey records into a reader-facing paper view and a separate evidence view. It defines the survey questions, section jobs, claim limits, comparison plan, citation needs, display jobs, appendix material, and draft-stop criteria. This prevents the manuscript from becoming a chronological dump of discovery records or a table-by-table narration.

### Use LaTeX source and compiler-owned document structure

The accepted publication manuscript is a LaTeX `.tex` source tree with explicit bibliography and included-file refs. The paper contract references a generated or supplied template; `create-paper-template` produces the default derived template when one is not supplied. Markdown may be used for notes, outlining, or imported source material, but `paper-pass` does not accept Pandoc, browser print-to-PDF, or another Markdown-to-PDF conversion as the publication build. The writer must first produce and validate `.tex` against the selected document class or venue template.

The LaTeX document class and compiler are the only section-numbering authority. Authors write `\section{Introduction}`, `\subsection{Scope}`, and corresponding structural commands without numeric prefixes. They do not write `\section{1. Introduction}`, place number text beside a starred heading, or disable compiler numbering to preserve manually authored numbers. The contract records which front and back matter is unnumbered, using the template's native structure or commands such as `\section*{Acknowledgments}`; appendices use the template's supported `\appendix` posture rather than authored letter or number prefixes.

Title and author information use LaTeX metadata and template commands such as `\title{}`, `\author{}`, `\date{}`, and `\maketitle`, not a numbered section. Citations use verified bibliography data through the template's supported citation commands and bibliography workflow. Pre-build validation rejects authored numeric prefixes, malformed section hierarchy, unresolved title metadata, invalid citation or display refs, direct Markdown-to-PDF commands, and template-incompatible structural commands.

### Route builds through existing execution and Gate contracts

Document compilation uses the existing `document_build` Research Operation Extension Point and an Execution Adapter Command Request when execution is required. The paper contract records the `.tex` entry point, document class or template, bibliography and included-file refs, Tectonic preference, allowed LaTeX fallback, output form, resource boundary, and Gate policy. The builder attempts Tectonic first when compatible and records its command, version, logs, and result. A fallback to `latexmk`, `pdflatex`, `xelatex`, `lualatex`, BibTeX, Biber, or a venue-required LaTeX workflow records the unavailable tool, template constraint, venue requirement, or concrete Tectonic failure before execution.

Publication-facing Gate policy remains authoritative for externally released or submission-facing output. Local draft builds can proceed only when the resolved policy permits them. The skill does not directly publish, upload, or push a paper merely because a local bundle passes validation.

### Separate compilation from publication validation

A successful build creates a `paper-build-run`; it does not mark the paper ready. `paper-validation-report` applies all available checks and records unavailable checks explicitly:

- contract-defined survey quality metrics and qualitative findings for coverage, identity, evidence depth, comparison soundness, traceability, synthesis, balance, limitations, and reader-facing reporting;
- source structure and numbering policy;
- citation resolution and bibliography consistency;
- engine exit status, missing references, missing glyphs, overfull content, and material warnings;
- PDF existence, media type, digest, page count, extractability, metadata, and outline or table-of-contents consistency;
- duplicate or shifted section numbering, title-as-section, incorrectly numbered front or back matter, broken URLs, and suspicious replacement glyphs in extracted text;
- visual inspection of the title or first page, table of contents when present, and every page containing figures, tables, or reported overflow risk;
- readable figures and tables, clipping, overlap, margins, and target-specific accessibility checks when required.

The report uses `ready`, `ready-with-warnings`, or `not-ready`. A publication bundle can be accepted only from `ready`, or from `ready-with-warnings` when the paper contract and applicable Gate explicitly permit those named warnings. Missing mandatory visual or extraction capability yields `not-ready` or a draft-only bundle rather than silent success.

### Extend existing package and validation inventories

The Kaoju extension grows from eleven to twelve production skills. The packaged manifest adds the skill path, begin and end callback insertion points, and `paper-pass` command metadata. Family validators and tests check the exact inventory, command page, skill identity, direct resources, binding coverage, profile resolution, and forbidden direct Markdown or untracked publication state. Extension discovery remains manifest-derived.

## Risks / Trade-offs

- [Writing records become too numerous] → Keep only five stable semantics and store detailed intermediate planning inside the paper contract or manuscript payload rather than adding a record for every drafting note.
- [Visual validation depends on host tools] → Record tool and capability availability, require a blocked or draft-only status when mandatory checks cannot run, and avoid claiming publication readiness from compilation alone.
- [Venue templates need incompatible engines or structures] → Let the paper contract select template and engine constraints, record every fallback, and keep initial guidance format-aware rather than pretending one command fits all venues.
- [An agent takes a convenient Markdown-to-PDF shortcut] → Require `.tex` as the bound manuscript source, reject Markdown conversion commands in publication builds, and test the exact source and command recorded by each build Run.
- [An agent manually numbers headings inside LaTeX] → Make compiler-owned numbering invariant, scan structural command arguments before build, and verify the extracted PDF heading sequence after build.
- [Kaoju and DeepSci writing guidance drifts] → Reuse platform terms and execution contracts, add regression tests for both families, and factor only genuinely common mechanics into shared support in a later change.
- [A writer silently changes evidence meaning] → Require exact accepted parents, claim-to-section mapping, citation lineage, preservation of limitations, and a non-mutating validation report.
- [A PDF passes automated text checks but remains visually poor] → Require page-image inspection for publication readiness and preserve visual findings as explicit validation results.
- [Agents game survey quality with large source counts or a single score] → Require declared denominators, exclusions, cutoffs, source refs, per-dimension verdicts, and visible unresolved cases; prohibit a composite score from overriding a mandatory failure.
- [Survey prose imitates an empirical paper by inventing novelty] → Make novelty optional, define survey-specific section jobs and contribution postures, and reject claims that are not present in accepted synthesis records.

## Migration Plan

1. Add the new skill directory, command page, LaTeX writing and validation references, agent metadata, and Kaoju documentation entry.
2. Add the `create-paper-template` procedural subcommand to `isomer-kaoju-pipeline`, including its command page, template generation and preview-build behavior, output path under `intent/derived/writing-template/main/`, and template ref binding.
3. Register the five semantics and producer bindings, then add family-neutral profiles, schemas, and Markdown render templates for their canonical records.
4. Extend the packaged manifest, extension discovery metadata, callback metadata, validators, and tests from eleven to twelve skills and add `paper-pass` and `create-paper-template`.
5. Add focused tests for writing prerequisites, binding coverage, lineage, survey-quality metric accounting, comparison-soundness findings, novelty-optional guidance, `.tex` source enforcement, compiler-owned numbering, Tectonic-first build recording, fallback disclosure, template generation, and validation readiness.
6. Run repository lint, type checking, unit tests, Kaoju validator tests, and manual fixtures that exercise a survey-quality profile, reject Markdown-to-PDF, reject manually numbered LaTeX sections, validate a Tectonic-built PDF, and validate generated template preview compilation.

Existing Kaoju records require no migration. Previously generated Markdown or PDF files remain non-canonical files unless a later authorized intake creates the new records with explicit provenance. Rollback removes the new manifest entries, skill assets, profiles, and tests; existing survey records remain valid because no current semantic meaning is changed.

## Open Questions

- Whether `ready-with-warnings` should always require a user Gate or may be accepted automatically when every warning class was pre-authorized by the paper contract. The design defaults to explicit contract and Gate authorization.
