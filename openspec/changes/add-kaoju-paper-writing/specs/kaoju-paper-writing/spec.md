## ADDED Requirements

### Requirement: Dedicated Kaoju Paper Writing Skill
The Kaoju extension SHALL provide `isomer-kaoju-write` as the owner of publication-facing paper contracts, manuscripts, document builds, validation reports, and publication bundles derived from accepted Kaoju survey records.

#### Scenario: Accepted synthesis enters writing
- **WHEN** an accepted Audit Report and its accepted Kaoju synthesis records are submitted for paper writing
- **THEN** `isomer-kaoju-write` creates or revises a bound paper contract and manuscript from those exact parent refs
- **AND** it does not use rendered Markdown, prompt memory, or an untracked file as canonical survey state

#### Scenario: Writing is invoked independently
- **WHEN** a user requests a manuscript revision or rebuild for an existing accepted Kaoju paper contract
- **THEN** `isomer-kaoju-write` can operate directly from the current bound writing records and accepted survey parents
- **AND** the user does not need to rerun discovery, examination, comparison, audit, or synthesis unless the evidence boundary changes

#### Scenario: Evidence gap is detected during writing
- **WHEN** the writer finds that a requested claim, citation, figure, or comparison is not supported by accepted inputs
- **THEN** it records the gap and routes to the owning Kaoju stage with a resume point
- **AND** it does not discover, infer, execute, or strengthen evidence inside the writing stage

### Requirement: Kaoju Paper Pass Orchestration
`isomer-kaoju-pipeline` SHALL expose `paper-pass` as a bounded procedure that verifies writing prerequisites, invokes `isomer-kaoju-write`, routes document builds and publication-facing Gates, validates the result, and returns a Kaoju terminal report.

`isomer-kaoju-pipeline` SHALL also expose `create-paper-template` as a bounded procedure that generates an editable LaTeX template tree, compiles a proof-of-compilation PDF preview, and returns the accepted template ref so that `paper-pass` and direct `isomer-kaoju-write` invocations can bind it.

#### Scenario: Paper pass starts from accepted records
- **WHEN** a user invokes `paper-pass` with an accepted Audit Report and accepted synthesis refs
- **THEN** the procedure verifies record identity, latest and supersession posture, lineage, worker-output policy, format-profile support, build capability, and applicable Gate policy before drafting or building
- **AND** it passes the verified refs to `isomer-kaoju-write`

#### Scenario: Paper pass lacks accepted prerequisites
- **WHEN** the requested paper has no accepted Audit Report, has ambiguous latest synthesis records, or requires unsupported claims
- **THEN** `paper-pass` returns `paused` or `blocked` with the missing refs, responsible stage, and resume point
- **AND** it does not create an improvised manuscript or PDF

#### Scenario: Paper pass completes
- **WHEN** the manuscript, build attempt, and publication validation satisfy the paper contract
- **THEN** the terminal report includes the paper contract, manuscript, accepted build, validation, publication bundle, file, Gate, and Provenance refs
- **AND** it does not start another survey or publication procedure autonomously

### Requirement: Template Generation Produces an Editable Derived Template
`isomer-kaoju-pipeline` SHALL expose `create-paper-template` as a public procedure that generates a LaTeX template tree at `intent/derived/writing-template/<template-name>/`, compiles a proof-of-compilation PDF preview, records the template artifact and preview build, and returns the accepted template ref. `main` is the reserved default template name; when no name is specified, the procedure operates on `main`, and `paper-pass` resolves to `main` when no explicit template is named.

#### Scenario: Default template is generated
- **WHEN** a user invokes `create-paper-template` without naming a template
- **THEN** the procedure generates or revises the `main` template under `intent/derived/writing-template/main/`
- **AND** it records the template artifact with source digests, preview build refs, and provenance
- **AND** it returns the accepted `main` template ref

#### Scenario: Named template is generated
- **WHEN** a user invokes `create-paper-template --name <name>` for a Research Topic and target venue or paper type
- **THEN** the procedure generates `.tex` entry point, bibliography stub, style and included files, a `README.md`, and a proof-of-compilation PDF preview under `intent/derived/writing-template/<name>/`
- **AND** it records the template artifact with source digests, preview build refs, and provenance
- **AND** it does not treat the preview PDF as the final paper PDF

#### Scenario: Paper pass uses default template
- **WHEN** a user invokes `paper-pass` without an explicit template name or ref
- **THEN** the procedure resolves the latest accepted `main` template
- **AND** it returns `paused` or `blocked` if no `main` template exists or is not ready

#### Scenario: Template generation fails
- **WHEN** the generated LaTeX source cannot compile to a preview PDF
- **THEN** `create-paper-template` returns `blocked` with the compile log, diagnostic, and repair hint
- **AND** it does not produce a paper contract or manuscript from a broken template

#### Scenario: Template is edited before paper pass
- **WHEN** a user edits files under `intent/derived/writing-template/<template-name>/` after generation
- **THEN** the edits create a new template artifact revision with ordinary artifact semantics
- **AND** `paper-pass` consumes the latest accepted `main` template ref when no explicit name or ref is given
- **AND** `paper-pass` consumes the latest accepted named template ref when the user names a non-default template

### Requirement: Paper Contract Fixes the Publication Boundary
The writing skill SHALL record a paper contract that fixes the target reader or venue, survey questions, scope and contribution posture, evidence boundary, survey-quality measurements and thresholds, LaTeX document class or template, compiler-owned numbering and unnumbered-section policy, citation policy, display expectations, Tectonic-first build and fallback requirements, output format, validation requirements, resource limits, and applicable Gate policy before accepting a manuscript.

#### Scenario: Paper target is explicit
- **WHEN** a new manuscript is requested
- **THEN** the paper contract records the intended audience or venue, survey questions, paper type, contribution posture, `.tex` entry point, output format, LaTeX document class or template posture, length or structure constraints, and required front and back matter
- **AND** unresolved target choices that materially change the manuscript cause clarification, pause, or a documented draft-only default

#### Scenario: Evidence boundary is explicit
- **WHEN** the paper contract is created or revised
- **THEN** it records the accepted Audit Report, Field Summary, Claim Status Table, catalog, digest or ledger, dossier, comparison, Finding, and Run refs that the manuscript may use
- **AND** it preserves the accepted verification depths, verdicts, contradictions, failures, limitations, and coverage cutoff

### Requirement: Survey Writing Adapts Evidence-First Paper Practice
The writing skill SHALL apply evidence-first and reader-first paper practices to survey reporting without making method, theory, or empirical novelty a publication-readiness requirement.

#### Scenario: Survey paper view is separated from evidence view
- **WHEN** accepted survey inputs enter manuscript planning
- **THEN** the writer creates a reader-facing paper view with survey questions, organizing spine, section jobs, taxonomy or comparison frame, scoped conclusions, displays, limitations, and target-reader logic
- **AND** it maintains a separate evidence view containing source identities, discovery and screening accounting, verification depths, exact locators, comparison cells, contradictions, audit findings, and appendix support

#### Scenario: Survey contribution does not require novelty
- **WHEN** the writer states why the paper is useful
- **THEN** it may describe accepted coverage, taxonomy, comparative perspective, synthesis, dataset, or gap-mapping contributions supported by the survey records
- **AND** it does not invent a novelty claim, method contribution, consensus, or field-wide conclusion merely to imitate an empirical research paper

#### Scenario: Sections and displays have reader-facing jobs
- **WHEN** the writing plan is prepared
- **THEN** each main section has one dominant job and each table or figure names the question it answers, the accepted inputs it uses, and the takeaway permitted by those inputs
- **AND** prose interprets comparative patterns, contradictions, gaps, and limitations instead of narrating cells or listing papers chronologically

#### Scenario: Citations are prepared before prose is accepted
- **WHEN** a section or display requires external attribution
- **THEN** verified citation identities and exact accepted source refs are present before the prose is accepted
- **AND** remembered citations, hand-written bibliography facts, and unresolved identities remain blockers or explicit placeholders

### Requirement: Survey Paper Quality Is a Transparent Metric Profile
The paper contract and validation report SHALL represent survey-paper quality as a multidimensional profile with explicit populations, exclusions, cutoffs, source refs, thresholds, and per-dimension verdicts rather than as an unsupported completeness claim or a single opaque score.

#### Scenario: Coverage and protocol execution are measured
- **WHEN** the survey-quality profile is evaluated
- **THEN** it reports required scope-cell coverage, planned discovery-channel execution, screening-disposition completeness, inclusion and exclusion accounting, temporal cutoff, and bounded discovery-saturation observations
- **AND** every measure names its numerator, denominator or bounded population, exclusions, unknown cases, and accepted source records
- **AND** it does not interpret discovery saturation or source count as proof that the literature universe is complete

#### Scenario: Source identity and evidence adequacy are measured
- **WHEN** included works and paper-facing claims are evaluated
- **THEN** the profile reports canonical identity and version resolution, unresolved or inaccessible sources, duplicate and variant handling, required verification-depth compliance, exact-locator coverage, and primary-source use where the contract requires it
- **AND** unresolved identity or evidence depth remains visible as uncertainty rather than being counted as successful coverage

#### Scenario: Comparative-study soundness is measured
- **WHEN** the paper compares methods, systems, theories, datasets, models, or other surveyed entities
- **THEN** the profile reports operationally defined dimensions, comparison-cell comparability status, matched evidence depth, missing and non-comparable cells, normalization posture, fairness findings, and material evidence asymmetries
- **AND** a comparison fails or warns according to the contract when its apparent conclusion depends on incompatible conditions, asymmetric verification, hidden missingness, or an undefined dimension

#### Scenario: Traceability, synthesis, balance, and reporting are measured
- **WHEN** the manuscript is assessed for publication readiness
- **THEN** the profile reports claim, citation, table, and figure traceability; survey-question coverage; taxonomy definitions and boundary cases; contradiction and negative-finding representation; gap calibration; material source or method-family skews; limitation propagation; section-job clarity; display interpretation; terminology consistency; and method reproducibility
- **AND** conclusions do not convert missing search, missing evidence, or non-comparability into a positive field-level finding

#### Scenario: Quality verdicts control readiness
- **WHEN** the profile is completed
- **THEN** every applicable dimension receives `pass`, `warning`, `fail`, `not-applicable`, or `unknown` with supporting refs and diagnostics
- **AND** a mandatory `fail` or `unknown` produces `not-ready`, while warnings require the authorization defined by the paper contract and applicable Gate
- **AND** a composite score, when explicitly defined, cannot override a mandatory failed or unknown dimension

### Requirement: Manuscript Preserves Claim and Citation Lineage
The writing skill SHALL keep every paper-facing claim, citation, table, and figure within the accepted evidence boundary and SHALL preserve traceable lineage from manuscript sections to accepted Kaoju records.

#### Scenario: Section is drafted from accepted claims
- **WHEN** a manuscript section states a conclusion
- **THEN** the structured manuscript maps that section and conclusion to accepted Research Claim, Evidence Item, Artifact, Finding, or Run refs
- **AND** the prose does not present source-stated, source-supported, executed, compared, inconclusive, contradicted, blocked, or not-comparable evidence more strongly than its accepted status

#### Scenario: Citation state is prepared
- **WHEN** the manuscript cites literature, documentation, repositories, datasets, models, or provider material
- **THEN** the writer builds citation state from verified Source Identities and accepted source locators
- **AND** it records unresolved citation keys, duplicate identities, inaccessible sources, and bibliography mismatches as blockers or named limitations rather than inventing entries

#### Scenario: Limitations remain visible
- **WHEN** an audited limitation, contradiction, failed Run, source blocker, or coverage boundary affects a paper claim
- **THEN** the manuscript keeps its effect visible in the applicable section and limitations material
- **AND** moving detail to an appendix does not erase its effect on the main-text conclusion

#### Scenario: Survey gap language is calibrated
- **WHEN** the manuscript reports an underexplored area, missing comparison, apparent consensus, or research gap
- **THEN** the statement identifies whether it follows from bounded discovery coverage, inaccessible evidence, explicit negative findings, contradictory sources, or a sound comparison result
- **AND** the prose does not treat absence from the accepted catalog as proof that no relevant work exists

### Requirement: Publication Manuscript Is LaTeX Source
Every publication-ready Kaoju manuscript SHALL bind a LaTeX `.tex` source tree and SHALL use the selected document class or venue template rather than a Markdown-to-PDF conversion path.

#### Scenario: Writer prepares publication source
- **WHEN** accepted survey content is prepared for a paper build
- **THEN** the writer creates or revises a `.tex` entry point plus explicit bibliography, figure, table, style, and included-file refs required by the selected template
- **AND** Markdown notes or imported prose remain intermediate material rather than the bound publication manuscript

#### Scenario: Markdown conversion is requested
- **WHEN** a proposed publication build invokes Pandoc, browser printing, or another Markdown-to-PDF path
- **THEN** pre-build validation rejects the build and routes the content through `.tex` manuscript preparation
- **AND** no PDF from that conversion can satisfy publication readiness

### Requirement: LaTeX Compiler Owns Section Numbering
Every Kaoju paper SHALL rely on the LaTeX document class and compiler for section numbering, and manuscript validation SHALL reject authored numeric prefixes or manual numbering schemes.

#### Scenario: Compiler owns numbering
- **WHEN** the writer creates section structure
- **THEN** it uses LaTeX structural commands such as `\section{Introduction}` and `\subsection{Scope}` without authored numeric prefixes
- **AND** the selected document class and compiler generate the visible numbers

#### Scenario: Author writes section numbers
- **WHEN** a structural command contains an authored prefix such as `\section{1. Introduction}` or a starred heading is paired with manual number text
- **THEN** pre-build validation marks the manuscript `not-ready` and identifies the source location
- **AND** the writer removes the authored number instead of disabling compiler numbering

#### Scenario: LaTeX title and special sections are structured correctly
- **WHEN** a LaTeX manuscript is prepared
- **THEN** title and author information use the template's metadata and title commands rather than a numbered section
- **AND** abstract, acknowledgments, references, appendices, and other target-defined material use the template's native unnumbered or appendix structure without authored numeric or letter prefixes

#### Scenario: Heading hierarchy is malformed
- **WHEN** pre-build inspection finds malformed structural nesting, a title treated as a section, authored or duplicate numeric prefixes, manual appendix labels, or special sections with conflicting numbering
- **THEN** the manuscript is `not-ready` and the diagnostic identifies the source location and required repair

### Requirement: Document Builds Are Reproducible Runs
Every paper compilation attempt SHALL build the bound `.tex` source through a Tectonic-first LaTeX workflow and SHALL be recorded as an immutable `kaoju:paper-build-run` through existing document-build execution and provenance contracts.

#### Scenario: Build capability is available
- **WHEN** the paper contract requests a local document build and preflight permits it
- **THEN** the writer routes the build through the resolved `document_build` Research Operation Extension Point or applicable owner
- **AND** the Run records the `.tex` entry point, source, bibliography, included-file and template digests, exact command, engine and version, environment, output and log refs, warnings, resource use, terminal status, and Provenance Records

#### Scenario: Tectonic is compatible
- **WHEN** the selected LaTeX source and template are compatible with Tectonic
- **THEN** the builder attempts Tectonic before another LaTeX engine and records its command, version, logs, warnings, outputs, and terminal result
- **AND** it does not invoke a Markdown converter as a compilation substitute

#### Scenario: Engine fallback is required
- **WHEN** Tectonic is unavailable, incompatible with the template, prohibited by the venue, or fails for a concrete reason
- **THEN** the build Run records that reason before using `latexmk`, `pdflatex`, `xelatex`, `lualatex`, BibTeX, Biber, or another venue-required LaTeX workflow
- **AND** the fallback command and result remain reproducible

#### Scenario: Publication-facing policy requires a Gate
- **WHEN** the build, export, upload, or release action is governed by a publication-facing Gate policy
- **THEN** the operation waits for or references the required Gate decision
- **AND** a successful local build does not authorize external publication, upload, push, or submission

#### Scenario: Build fails
- **WHEN** the document engine exits unsuccessfully or required outputs are missing
- **THEN** the failed build remains a separate Run with its logs and diagnostics
- **AND** a repaired attempt creates a new descendant Run instead of rewriting the failed attempt

### Requirement: Compiled Output Requires Post-Render Validation
A successful paper build SHALL NOT be considered publication-ready until a bound paper validation report checks the required source, compile, extracted-document, and visual properties.

#### Scenario: Structural and textual checks run
- **WHEN** a build produces a PDF
- **THEN** validation checks `.tex` source identity, absence of authored section numbers, citation resolution, material compile warnings, PDF media type and digest, page count, extractability, metadata, outline or table-of-contents consistency, missing glyphs, broken URLs, and suspicious duplicate or shifted section labels
- **AND** the report records the tool, command, result, and diagnostic location for each check

#### Scenario: Survey-content quality checks run
- **WHEN** a manuscript and build are evaluated for publication readiness
- **THEN** validation evaluates every survey-quality dimension and threshold selected by the paper contract against the exact accepted audit, synthesis, catalog, comparison, claim, citation, and manuscript refs
- **AND** the report preserves the metric values, qualitative findings, missing cases, per-dimension verdicts, and repair or route-back diagnostics

#### Scenario: Visual checks run
- **WHEN** the paper contract requires publication-ready PDF output
- **THEN** validation visually inspects the title or first page, table of contents when present, and pages containing figures, tables, or reported overflow risk
- **AND** it checks clipping, overlap, margins, readability, figure and table placement, and target-required accessibility properties

#### Scenario: Compilation succeeds but validation fails
- **WHEN** the PDF exists but duplicate numbering, malformed hierarchy, overflow, clipping, unreadable content, missing citations, or another mandatory defect is found
- **THEN** the validation verdict is `not-ready`
- **AND** neither the terminal report nor publication bundle describes the paper as complete or publication-ready

#### Scenario: Mandatory inspection capability is unavailable
- **WHEN** required text extraction, PDF metadata, page rendering, or visual inspection cannot be performed
- **THEN** validation records the missing capability and returns `not-ready` or an explicitly draft-only result according to the paper contract
- **AND** compilation success does not substitute for the missing check

#### Scenario: Warnings are accepted explicitly
- **WHEN** validation returns `ready-with-warnings`
- **THEN** each warning is named and can be accepted only when the paper contract and applicable Gate policy permit that warning class
- **AND** the publication bundle preserves the warning and acceptance refs

### Requirement: Publication Bundle Is a Derived Assembly
The writing skill SHALL produce a publication bundle only as a navigable assembly of accepted writing records and file refs, without turning presentation output into new survey evidence.

#### Scenario: Ready bundle is assembled
- **WHEN** a paper validation report is `ready`, or explicitly accepted as `ready-with-warnings`
- **THEN** the bundle references the exact paper contract, manuscript revision, build Run, validation report, source, bibliography, figures, tables, PDF, reproduction instructions, limitations, and Provenance Records
- **AND** every file ref resolves through the accepted binding and worker-output policy

#### Scenario: Paper representation changes
- **WHEN** prose, organization, template, numbering, bibliography formatting, or layout changes without changing evidence meaning
- **THEN** the writer revises the manuscript or paper contract and creates new build and validation descendants
- **AND** the accepted survey evidence records are not revised merely because their representation changed

#### Scenario: Evidence meaning changes
- **WHEN** a requested paper revision changes a claim boundary, verdict, comparison meaning, or accepted evidence set
- **THEN** the writer routes the change back through the applicable audit and synthesis stages before incorporating it
- **AND** the earlier publication bundle remains historical
