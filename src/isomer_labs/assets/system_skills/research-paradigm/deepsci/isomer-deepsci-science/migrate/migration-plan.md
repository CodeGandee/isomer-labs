# Isomer Research Science Production DeepSci Refactor Migration Plan

## Scope

- Source skill: `extern/orphan/DeepScientist/src/skills/science`.
- Target skill: `skillset/research-paradigm/deepsci/isomer-rsch-science`.
- Migration mode: `refactor-migrate`.
- Source copy: every source file is copied unchanged into `org/src/`.
- Runtime support copy: every source file is copied and refactored under the target runtime tree with source-relative paths preserved, except the source entrypoint and `agents/openai.yaml`.
- Source files covered: `PROVENANCE.md`, `SKILL.md`, `references/artifact-science-tool.md`, `references/claim-type-discipline.md`, `references/domain-index.md`, `references/hpc-via-bash-exec.md`, `references/package-check-playbook.md`, `references/package-index.min.json`, `references/science-task-brief-template.md`, and all package cards under `references/packages/`.
- Source analysis: `org/analysis/analysis-of-science.md`.
- Exclusions from deep inspection: generated package cards, package index JSON, and provenance are passive catalog/provenance material. They are copied into the runtime tree and mechanically adapted for Isomer wording, while operative behavior is refactored in top-level pages.

## Term Substitutions

| Source Term | Isomer Labs Term or Treatment |
| --- | --- |
| quest | Research Topic, Research Inquiry, Research Task, or Topic Workspace, depending on the source meaning. |
| quest files and durable quest state | Workspace Runtime records, Artifacts, Evidence Items, Findings, Gates, Decision Records, Provenance Records, and user-provided Research Topic context. |
| stage | production DeepSci research skill route or Workflow Stage context inside a Topic Agent Team Profile. |
| companion skill | production DeepSci companion support skill for scientific evidence discipline. |
| next stage or next anchor | `DEEPSCI:SCIENCE-ROUTE-DECISION` or `DEEPSCI:SCIENCE-BLOCKER-RECORD`, later bound to production DeepSci skill routing. |
| source templates and fixed paths | Semantic placeholders in `migrate/placeholders.md` until Isomer storage bindings are finalized. |
| source package cards and package index | Isomer routing catalog material copied into `references/` and treated as knowledge pointers, not runtime availability proof. |

## Harness Substitutions

| Source Harness or Tool Rule | Isomer Labs Treatment |
| --- | --- |
| `memory.*` | Prefer Workspace Runtime-backed retrieval or recording. When compatibility is required, use `isomer-cli ext deepsci call memory.<tool> --input-json <json-object>` and status the result with the local placeholders. |
| `artifact.science(...)` and `artifact.*` | Prefer Isomer Evidence Items, Findings, Provenance Records, Gates, Decision Records, and science evidence graph placeholders. When compatibility is required, use `isomer-cli ext deepsci call artifact.<tool> --input-json <json-object>` and status semantic meaning with placeholders. |
| `bash_exec(...)` | Use an Execution Adapter Command Request or the DeepScientist-compatible extension call for shell, CLI, Python, git, package, scheduler, SSH, or environment work. Do not describe native shell calls as the final skill contract. |
| FermiLink runner, CLI, UI, backend, and HPC profile manager | Not migrated as runtime dependencies. Only generated package catalog material is copied. |

## Storage and Artifact Substitutions

The migrated runtime pages do not bind source artifacts to concrete paths. They use the local placeholders defined in `migrate/placeholders.md`:

- `DEEPSCI:SCIENCE-TASK-BRIEF`
- `DEEPSCI:SCIENCE-PACKAGE-CHECK`
- `DEEPSCI:SCIENCE-RUN-RECORD`
- `DEEPSCI:SCIENCE-VALIDATION-RESULT`
- `DEEPSCI:SCIENCE-CLAIM-RECORD`
- `DEEPSCI:SCIENCE-EVIDENCE-GRAPH-UPDATE`
- `DEEPSCI:SCIENCE-BLOCKER-RECORD`
- `DEEPSCI:SCIENCE-ROUTE-DECISION`

## Unmatched Skill-Route Substitutions

science maps to isomer-rsch-science. Source science evidence graph calls map to local science evidence placeholders and compatibility extension calls when required.

Where a source route names a DeepScientist skill that has no production DeepSci target in this batch, the runtime page records the route through a semantic decision or blocker placeholder rather than pretending the missing Isomer skill exists.

## Environment Substitutions

- Source `venv`, `uv`, shell, package, Git, scheduler, SSH, HPC module, license, and environment assumptions map to Pixi-aware Project or Topic Workspace context plus Execution Adapter Command Requests.
- Runtime pages should not require a fixed filesystem layout, virtual environment, command path, HPC profile, or package manager unless later storage and execution binding work adds one.
- Compatibility harness examples are allowed only as transitional `isomer-cli ext deepsci call ... --input-json <json-object>` instructions.

## Placeholder Registry

`migrate/placeholders.md` defines every placeholder used by rewritten runtime pages. Every rewritten page that mentions placeholders references that registry.

## Rewrite Targets

- `SKILL.md`: native production DeepSci control surface with workflow steps that reference the required support pages.
- `PROVENANCE.md`: copied provenance page with Isomer runtime wording.
- `references/artifact-science-tool.md`: source-preserved evidence graph page refactored into native recording support.
- `references/claim-type-discipline.md`: source-preserved claim discipline page refactored into computed, parsed, digitized, and hypothesis support.
- `references/hpc-via-bash-exec.md`: source-preserved HPC page refactored into Isomer Execution Adapter support.
- `references/package-check-playbook.md`: source-preserved package check page refactored into availability-check support.
- `references/science-task-brief-template.md`: source-preserved brief template refactored into task and scientific-code-optimization support.
- `references/domain-index.md`: copied generated domain index with added routing support blocks.
- `references/package-index.min.json`: copied generated package index with Isomer wording; passive catalog material.
- `references/packages/*.md`: copied generated package cards with Isomer runtime wording; passive package-routing material.
- `references/science-task-brief.md`, `references/evidence-recording.md`, `references/package-routing.md`, `references/hpc-execution-adapter.md`, `references/claim-discipline.md`: compatibility pages from the first production DeepSci draft pointing to source-preserved pages.

## Main Workflow Support Mapping

| Target Workflow Step | Source Support Material | Target Runtime Support |
| --- | --- | --- |
| Frame the science task | `SKILL.md` Match Signals, Workflow step 1, SetupAgent Usage, Validation; `references/science-task-brief-template.md`. | `references/science-task-brief-template.md` |
| Route through package or domain context | `SKILL.md` Progressive Disclosure, Package Catalog Provenance, AVOID, Validation; `references/domain-index.md`; `references/package-index.min.json`; `references/packages/*.md`; `references/package-check-playbook.md`. | `references/package-index.min.json`, `references/domain-index.md`, `references/packages/<package_id>.md`, `references/package-check-playbook.md` |
| Execute through Isomer command surfaces | `SKILL.md` Control Surface, Workflow steps 4 and 6, AVOID; `references/hpc-via-bash-exec.md`; `references/package-check-playbook.md`. | `references/hpc-via-bash-exec.md`, `references/package-check-playbook.md` |
| Record scientific evidence | `SKILL.md` Workflow steps 5, 7, 8, Science Node Types, Validation; `references/artifact-science-tool.md`; package cards expected science nodes. | `references/artifact-science-tool.md`, relevant package card |
| Classify claims conservatively | `SKILL.md` Claim Discipline, Science Node Types, AVOID; `references/claim-type-discipline.md`. | `references/claim-type-discipline.md` |
| Update the evidence graph or route | `SKILL.md` Workflow step 10, Science node id/update rules, Validation; `references/artifact-science-tool.md`; `references/hpc-via-bash-exec.md`. | `references/artifact-science-tool.md`, `references/hpc-via-bash-exec.md` |

## Semantic Match Checks

The rewritten skill must preserve these source behaviors:

- Science task is framed before execution.
- Package and domain catalog material is progressive-disclosure routing context, not availability proof.
- Package checks precede computed work when availability matters.
- HPC, SSH, scheduler, queue, and logs are handled through Isomer execution surfaces.
- Evidence records precede scientific claims.
- Science node ids are stable and updates are append-only in meaning.
- Claims are typed as computed, parsed, digitized, or hypothesis.
- Computed claims link to current-run evidence or validation records.
- Package checks, runs, validation results, claims, blockers, and route decisions are explicit.
