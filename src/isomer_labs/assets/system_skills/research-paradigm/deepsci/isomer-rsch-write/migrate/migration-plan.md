# Write Refactor Migration Plan

## Scope

- Source skill: `extern/orphan/DeepScientist/src/skills/write`.
- Target skill: `skillset/research-paradigm/deepsci/isomer-rsch-write`.
- Migration mode: `refactor-migrate`.
- Source copy: every source file is copied unchanged into `org/src/`.
- Source analysis: `org/analysis/analysis-of-write.md`, copied from `context/explore/deepscientist-skill-analysis/write.md`.
- Exclusions from workflow-bearing deep inspection: passive templates, assets, plotting scripts, upstream licenses, eval fixtures, and source agent metadata were copied but not treated as control-flow instructions unless the entrypoint routed to them.

## Term Substitutions

| Source Term | Isomer Labs Term or Treatment |
| --- | --- |
| quest | Research Topic, Research Inquiry, Research Task, or Topic Workspace, depending on scope. |
| quest state, quest files, paper directory | Workspace Runtime records, Artifacts, Evidence Items, Findings, Decision Records, Topic Workspace material, or semantic placeholders. |
| stage or companion skill | production DeepSci Isomer research skill route. |
| memory cards | Workspace Runtime-backed continuity records or DeepScientist-compatible memory calls summarized through placeholders. |
| artifact paths and paper files | Semantic placeholders until storage binding is finalized. |
| operator/agent provenance in manuscript text | Excluded from paper-facing prose unless explicitly part of reproducibility material. |

## Harness Substitutions

| Source Harness or Tool Rule | Isomer Labs Treatment |
| --- | --- |
| `memory.*` | Use Workspace Runtime records when available; use `isomer-cli ext deepsci call memory.<tool> --input-json '{...}'` only for source-compatible behavior, then status durable meaning through placeholders. |
| `artifact.*` | Prefer Isomer Artifacts, Evidence Items, Findings, Decision Records, and Topic Workspace records; use `isomer-cli ext deepsci call artifact.<tool> --input-json '{...}'` only when preserving source-compatible behavior. |
| `bash_exec(...)` | Treat command execution as an Execution Adapter Command Request in the active Pixi-managed Project or Topic Workspace; use `isomer-cli ext deepsci call bash_exec.bash_exec --input-json '{...}'` only for compatibility. |
| concrete paper paths such as `paper/...` or `output/...` | Replace in migrated control text with semantic placeholders and leave storage binding to a later pass. |

## Storage and Artifact Substitutions

The migrated runtime entrypoint does not bind source artifacts to concrete paths. It uses placeholders defined in `migrate/placeholders.md`:

- `<PAPER_CONTROL_STATE>`
- `<PAPER_CONTRACT>`
- `<PAPER_OUTLINE>`
- `<WRITING_PLAN>`
- `<SOURCE_MATERIAL_LEDGER>`
- `<CITATION_LEDGER>`
- `<DISPLAY_PLAN>`
- `<DRAFT_SECTION_SET>`
- `<MANUSCRIPT_VALIDATION_REPORT>`
- `<PAPER_BUNDLE_CHECKPOINT>`
- `<WRITING_ROUTE_DECISION>`

## Unmatched Skill-Route Substitutions

- paper-outline maps to `isomer-rsch-paper-outline`.
- paper-plot maps to `isomer-rsch-paper-plot`.
- figure-polish maps to `isomer-rsch-figure-polish`.
- analysis-campaign maps to `isomer-rsch-analysis`.
- review maps to `isomer-rsch-review`.
- finalize maps to `isomer-rsch-finalize`.
- nature-data, nature-figure, nature-paper2ppt, and nature-polishing map to their production DeepSci companion skills.
- No paper-writing source route in this migration requires a `missing-isomer-skill` placeholder after the production DeepSci batch is present.

## Environment Substitutions

- Source assumptions about local files, shell execution, paper directories, and package availability are treated as Topic Workspace, Agent Workspace, Workspace Runtime, Artifact, provider binding, or Execution Adapter concerns.
- The active Project remains Pixi-managed; migrated instructions do not create a separate `venv` convention.
- Concrete source paths under `paper/`, `output/`, or source template directories are preserved only as source examples or passive copied material until storage binding is finalized.

## Placeholder Registry

`migrate/placeholders.md` defines every placeholder used by the migrated `SKILL.md`. Runtime pages that use these placeholders should reference that registry near the first placeholder use.

## Rewrite Targets

- `SKILL.md`: rewritten into native Isomer production DeepSci research language while preserving the source workflow states, constraints, outputs, and route decisions.
- `references/experiments_analysis_patterns.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.
- `references/oral_package_patterns.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.
- `references/oral_writing_principles.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.
- `references/section_rewrite_checklist.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.
- `templates/DEEPSCIENTIST_NOTES.md`: passive venue/template material copied for audit and later storage binding.
- `templates/README.md`: passive venue/template material copied for audit and later storage binding.
- `templates/UPSTREAM_LICENSE.txt`: passive venue/template material copied for audit and later storage binding.
- `templates/aaai2026/README.md`: passive venue/template material copied for audit and later storage binding.
- `templates/aaai2026/aaai2026-unified-supp.tex`: passive venue/template material copied for audit and later storage binding.
- `templates/aaai2026/aaai2026-unified-template.tex`: passive venue/template material copied for audit and later storage binding.
- `templates/aaai2026/aaai2026.bib`: passive venue/template material copied for audit and later storage binding.
- `templates/aaai2026/aaai2026.bst`: passive venue/template material copied for audit and later storage binding.
- `templates/aaai2026/aaai2026.sty`: passive venue/template material copied for audit and later storage binding.
- `templates/acl/README.md`: passive venue/template material copied for audit and later storage binding.
- `templates/acl/acl.sty`: passive venue/template material copied for audit and later storage binding.
- `templates/acl/acl_latex.tex`: passive venue/template material copied for audit and later storage binding.
- `templates/acl/acl_lualatex.tex`: passive venue/template material copied for audit and later storage binding.
- `templates/acl/acl_natbib.bst`: passive venue/template material copied for audit and later storage binding.
- `templates/acl/anthology.bib.txt`: passive venue/template material copied for audit and later storage binding.
- `templates/acl/custom.bib`: passive venue/template material copied for audit and later storage binding.
- `templates/acl/formatting.md`: passive venue/template material copied for audit and later storage binding.
- `templates/asplos2027/main.tex`: passive venue/template material copied for audit and later storage binding.
- `templates/asplos2027/references.bib`: passive venue/template material copied for audit and later storage binding.
- `templates/colm2025/README.md`: passive venue/template material copied for audit and later storage binding.
- `templates/colm2025/colm2025_conference.bib`: passive venue/template material copied for audit and later storage binding.
- `templates/colm2025/colm2025_conference.bst`: passive venue/template material copied for audit and later storage binding.
- `templates/colm2025/colm2025_conference.sty`: passive venue/template material copied for audit and later storage binding.
- `templates/colm2025/colm2025_conference.tex`: passive venue/template material copied for audit and later storage binding.
- `templates/colm2025/fancyhdr.sty`: passive venue/template material copied for audit and later storage binding.
- `templates/colm2025/math_commands.tex`: passive venue/template material copied for audit and later storage binding.
- `templates/colm2025/natbib.sty`: passive venue/template material copied for audit and later storage binding.
- `templates/iclr2026/fancyhdr.sty`: passive venue/template material copied for audit and later storage binding.
- `templates/iclr2026/iclr2026_conference.bib`: passive venue/template material copied for audit and later storage binding.
- `templates/iclr2026/iclr2026_conference.bst`: passive venue/template material copied for audit and later storage binding.
- `templates/iclr2026/iclr2026_conference.sty`: passive venue/template material copied for audit and later storage binding.
- `templates/iclr2026/iclr2026_conference.tex`: passive venue/template material copied for audit and later storage binding.
- `templates/iclr2026/math_commands.tex`: passive venue/template material copied for audit and later storage binding.
- `templates/iclr2026/natbib.sty`: passive venue/template material copied for audit and later storage binding.
- `templates/icml2026/algorithm.sty`: passive venue/template material copied for audit and later storage binding.
- `templates/icml2026/algorithmic.sty`: passive venue/template material copied for audit and later storage binding.
- `templates/icml2026/example_paper.bib`: passive venue/template material copied for audit and later storage binding.
- `templates/icml2026/example_paper.tex`: passive venue/template material copied for audit and later storage binding.
- `templates/icml2026/fancyhdr.sty`: passive venue/template material copied for audit and later storage binding.
- `templates/icml2026/icml2026.bst`: passive venue/template material copied for audit and later storage binding.
- `templates/icml2026/icml2026.sty`: passive venue/template material copied for audit and later storage binding.
- `templates/neurips2025/Makefile`: passive venue/template material copied for audit and later storage binding.
- `templates/neurips2025/extra_pkgs.tex`: passive venue/template material copied for audit and later storage binding.
- `templates/neurips2025/main.tex`: passive venue/template material copied for audit and later storage binding.
- `templates/neurips2025/neurips.sty`: passive venue/template material copied for audit and later storage binding.
- `templates/nsdi2027/main.tex`: passive venue/template material copied for audit and later storage binding.
- `templates/nsdi2027/references.bib`: passive venue/template material copied for audit and later storage binding.
- `templates/nsdi2027/usenix-2020-09.sty`: passive venue/template material copied for audit and later storage binding.
- `templates/osdi2026/main.tex`: passive venue/template material copied for audit and later storage binding.
- `templates/osdi2026/references.bib`: passive venue/template material copied for audit and later storage binding.
- `templates/osdi2026/usenix-2020-09.sty`: passive venue/template material copied for audit and later storage binding.
- `templates/sosp2026/main.tex`: passive venue/template material copied for audit and later storage binding.
- `templates/sosp2026/references.bib`: passive venue/template material copied for audit and later storage binding.

## Main Workflow Support Mapping

| Target Workflow Step | Source Sections and References | Runtime Support Pages |
| --- | --- | --- |
| Refresh control state | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/experiments_analysis_patterns.md` |
| Lock the paper contract | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/oral_package_patterns.md` |
| Validate the outline before drafting | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/oral_package_patterns.md`, `references/oral_writing_principles.md` |
| Compile the writing plan | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/oral_writing_principles.md` |
| Sort source material | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/oral_package_patterns.md`, `references/oral_writing_principles.md` |
| Refresh citations and references | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/oral_package_patterns.md`, `references/oral_writing_principles.md` |
| Plan displays before prose | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/oral_package_patterns.md`, `references/oral_writing_principles.md` |
| Draft or revise sections | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/section_rewrite_checklist.md` |
| Validate the manuscript state | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/oral_package_patterns.md`, `references/oral_writing_principles.md` |
| Checkpoint or route next | Source `SKILL.md`, source analysis, and copied source support pages relevant to this step. | `references/oral_package_patterns.md`, `references/oral_writing_principles.md` |

## Semantic Match Checks

The rewritten skill must preserve these source behaviors:

- Build <PAPER_CONTROL_STATE> from the Research Topic, paper contract, current outline, evidence ledger, experiment matrix, figures, references, Workspace Runtime records, and active draft surfaces.
- Produce or update <PAPER_CONTRACT> with the central claim, venue or report target, evidence boundary, required figures, citation state, and bundle status.
- Check <PAPER_OUTLINE> for a real reader-facing thesis, scoped claims, method abstraction, evaluation plan, analysis plan, and evidence map.
- Turn a valid outline into <WRITING_PLAN> with section jobs, source inputs, claim limits, figure needs, citation needs, and draft-stop criteria.
- Create <SOURCE_MATERIAL_LEDGER> separating manuscript claims, experiment settings, reproducibility details, implementation details, artifact history, and appendix-only material.
- Create <CITATION_LEDGER> from verified sources before citing.
- Create <DISPLAY_PLAN> for figures, tables, and appendix displays.
- Produce <DRAFT_SECTION_SET> from the section jobs, using references/section_rewrite_checklist.
- Produce <MANUSCRIPT_VALIDATION_REPORT> covering claim support, citation legitimacy, figure readiness, section coverage, language hygiene, bundle readiness, and remaining blockers.
- Submit <PAPER_BUNDLE_CHECKPOINT> when the draft, review package, or submission package is coherent; otherwise produce <WRITING_ROUTE_DECISION> to analysis, review, finalize, paper-outline, or a Nature companion skill as justified.
- Keep source evidence boundaries, stop conditions, route decisions, and durable outputs visible.
- Preserve the source distinction between writing/presentation polish and evidence generation.
- Keep unresolved storage bindings as semantic placeholders rather than concrete paths.
