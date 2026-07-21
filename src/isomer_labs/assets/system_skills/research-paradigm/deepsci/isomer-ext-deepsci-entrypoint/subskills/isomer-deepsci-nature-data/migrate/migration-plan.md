# Nature Data Refactor Migration Plan

## Scope

- Source skill: `extern/orphan/DeepScientist/src/skills/nature-data`.
- Target skill: `skillset/research-paradigm/deepsci/isomer-rsch-nature-data`.
- Migration mode: `refactor-migrate`.
- Source copy: every source file is copied unchanged into `org/src/`.
- Source analysis: `org/analysis/analysis-of-nature-data.md`, copied from `context/explore/deepscientist-skill-analysis/nature-data.md`.
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

- `DEEPSCI:DATA-AVAILABILITY-CONTEXT`
- `DEEPSCI:DATASET-INVENTORY`
- `DEEPSCI:DATA-ACCESS-CLASSIFICATION`
- `DEEPSCI:REPOSITORY-STRATEGY`
- `DEEPSCI:DATA-AVAILABILITY-STATEMENT`
- `DEEPSCI:DATASET-CITATION-ACTIONS`
- `DEEPSCI:FAIR-METADATA-AUDIT`
- `DEEPSCI:DATA-AVAILABILITY-BLOCKER`

## Unmatched Skill-Route Substitutions

- write maps to `isomer-rsch-write` for manuscript integration.
- finalize maps to `isomer-rsch-finalize` for package closure.
- No paper-writing source route in this migration requires a `missing-isomer-skill` placeholder after the production DeepSci batch is present.

## Environment Substitutions

- Source assumptions about local files, shell execution, paper directories, and package availability are treated as Topic Workspace, Agent Workspace, Workspace Runtime, Artifact, provider binding, or Execution Adapter concerns.
- The active Project remains Pixi-managed; migrated instructions do not create a separate `venv` convention.
- Concrete source paths under `paper/`, `output/`, or source template directories are preserved only as source examples or passive copied material until storage binding is finalized.

## Placeholder Registry

`migrate/placeholders.md` defines every placeholder used by the migrated `SKILL-MAIN.md`. Runtime pages that use these placeholders should reference that registry near the first placeholder use.

## Rewrite Targets

- `SKILL-MAIN.md`: rewritten into native Isomer production DeepSci research language while preserving the source workflow states, constraints, outputs, and route decisions.
- `UPSTREAM_LICENSE.txt`: upstream license notice retained.
- `references/chinese-author-alignment.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.
- `references/fair-metadata-checklist.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.
- `references/policy-principles.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.
- `references/repository-and-identifiers.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.
- `references/source-basis.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.
- `references/statement-patterns.md`: runtime support page retained with source-derived guidance and consumed through the native entrypoint.

## Main Workflow Support Mapping

| Target Workflow Step | Source Sections and References | Runtime Support Pages |
| --- | --- | --- |
| Identify journal and article type | Source `SKILL-SOURCE.md`, source analysis, and copied source support pages relevant to this step. | `references/policy-principles.md`, `references/source-basis.md` |
| Inventory datasets | Source `SKILL-SOURCE.md`, source analysis, and copied source support pages relevant to this step. | `references/policy-principles.md`, `references/source-basis.md` |
| Classify access routes | Source `SKILL-SOURCE.md`, source analysis, and copied source support pages relevant to this step. | `references/policy-principles.md`, `references/source-basis.md` |
| Choose repository strategy | Source `SKILL-SOURCE.md`, source analysis, and copied source support pages relevant to this step. | `references/repository-and-identifiers.md` |
| Draft data availability text | Source `SKILL-SOURCE.md`, source analysis, and copied source support pages relevant to this step. | `references/statement-patterns.md` |
| Add dataset citation actions | Source `SKILL-SOURCE.md`, source analysis, and copied source support pages relevant to this step. | `references/policy-principles.md`, `references/source-basis.md` |
| Run FAIR metadata audit | Source `SKILL-SOURCE.md`, source analysis, and copied source support pages relevant to this step. | `references/fair-metadata-checklist.md` |
| Return ready text or blocker | Source `SKILL-SOURCE.md`, source analysis, and copied source support pages relevant to this step. | `references/chinese-author-alignment.md` |

## Semantic Match Checks

The rewritten skill must preserve these source behaviors:

- Produce DEEPSCI:DATA-AVAILABILITY-CONTEXT with target journal, article type, policy source, and author constraints.
- Produce DEEPSCI:DATASET-INVENTORY covering every dataset or source file supporting results, including raw, processed, figure source, secondary, restricted, model, table, image, and statistical-analysis data.
- Produce DEEPSCI:DATA-ACCESS-CLASSIFICATION for each dataset: public repository, controlled access, paper/supplement, reused public source, third-party restricted, request-based, or not applicable.
- Produce DEEPSCI:REPOSITORY-STRATEGY before drafting text, including repository candidates, identifiers, versioning, embargo, license, accession, and dataset citation needs.
- Produce DEEPSCI:DATA-AVAILABILITY-STATEMENT using references/statement-patterns.
- Produce DEEPSCI:DATASET-CITATION-ACTIONS for public and reused datasets, including formal dataset citations and missing identifier work.
- Produce DEEPSCI:FAIR-METADATA-AUDIT using references/fair-metadata-checklist.
- If fields are confirmed, return ready-to-paste text and actions.
- Keep source evidence boundaries, stop conditions, route decisions, and durable outputs visible.
- Preserve the source distinction between writing/presentation polish and evidence generation.
- Keep unresolved storage bindings as semantic placeholders rather than concrete paths.
