# Isomer Research Baseline Production DeepSci Refactor Migration Plan

## Scope

- Source skill: `extern/orphan/DeepScientist/src/skills/baseline`.
- Target skill: `skillset/research-paradigm/deepsci/isomer-rsch-baseline`.
- Migration mode: `refactor-migrate`.
- Source copy: every source file is copied unchanged into `org/src/`.
- Runtime support copy: every source file is copied and refactored under the target runtime tree with source-relative paths preserved, except the source entrypoint and `agents/openai.yaml`.
- Source files covered: `SKILL-SOURCE.md`, `references/artifact-flow-examples.md`, `references/artifact-payload-examples.md`, `references/baseline-checklist-template.md`, `references/baseline-plan-template.md`, `references/boundary-cases.md`, `references/codebase-audit-checklist.md`, `references/comparability-contract.md`, `references/operational-guidance.md`, `references/route-selection.md`.
- Source analysis: `org/analysis/analysis-of-baseline.md`.
- Exclusions from deep inspection: package-card and static catalog files are treated as progressive-disclosure reference material when present; runtime behavior is summarized in the source analysis and native production DeepSci pages.

## Term Substitutions

| Source Term | Isomer Labs Term or Treatment |
| --- | --- |
| quest | Research Topic, Research Inquiry, Research Task, or Topic Workspace, depending on the source meaning. |
| quest files and durable quest state | Workspace Runtime records, Artifacts, Evidence Items, Findings, Gates, Decision Records, Provenance Records, and user-provided Research Topic context. |
| stage | production DeepSci research skill route or Workflow Stage context inside a Topic Agent Team Profile. |
| next stage or next anchor | `DEEPSCI:BASELINE-ROUTE-DECISION` or `DEEPSCI:BASELINE-BLOCKER-RECORD`, later bound to production DeepSci skill routing. |
| source templates and fixed paths | Semantic placeholders in `migrate/placeholders.md` until Isomer storage bindings are finalized. |
| `PLAN.md`, `CHECKLIST.md`, `setup.md`, `execution.md`, `verification.md`, `analysis_plan.md`, `REPRO_CHECKLIST.md` | `DEEPSCI:BASELINE-ROUTE-PLAN` or `DEEPSCI:BASELINE-GATE-CHECKLIST` depending on the control-surface role. |
| `<baseline_root>/json/metric_contract.json` | `DEEPSCI:COMPARABILITY-CONTRACT` until storage binding is finalized. |
| `attachment.yaml` | `DEEPSCI:BASELINE-PROVENANCE-RECORD` until storage binding is finalized. |

## Harness Substitutions

| Source Harness or Tool Rule | Isomer Labs Treatment |
| --- | --- |
| `memory.*` | Prefer Workspace Runtime-backed retrieval or recording. When compatibility is required, use `isomer-cli ext deepsci call memory.<tool> --input-json <json-object>` and status the result with the local placeholders. |
| `artifact.*` | Prefer Isomer Artifacts, Evidence Items, Findings, Decision Records, Gates, and Workspace Runtime records. When compatibility is required, use `isomer-cli ext deepsci call artifact.<tool> --input-json <json-object>` and status semantic meaning with placeholders. |
| `bash_exec(...)` | Use an Execution Adapter Command Request or the DeepScientist-compatible extension call for shell, CLI, Python, git, package, scheduler, or environment work. Do not describe native shell calls as the final skill contract. |
| Source baseline attach, import, publish, confirm, overwrite, waive, and git calls | Use `DEEPSCI:BASELINE-PROVENANCE-RECORD`, `DEEPSCI:BASELINE-VERIFICATION-EVIDENCE`, `DEEPSCI:BASELINE-PAYLOAD-RECORD`, `DEEPSCI:ACCEPTED-BASELINE-RECORD`, `DEEPSCI:BASELINE-WAIVER-RECORD`, and related placeholders until storage bindings are finalized. |

## Storage and Artifact Substitutions

The migrated runtime pages do not bind source artifacts to concrete paths. They use the local placeholders defined in `migrate/placeholders.md`:

- `DEEPSCI:BASELINE-CONTEXT-BRIEF`
- `DEEPSCI:COMPARATOR-ROUTE-RECORD`
- `DEEPSCI:BASELINE-ROUTE-PLAN`
- `DEEPSCI:BASELINE-GATE-CHECKLIST`
- `DEEPSCI:COMPARABILITY-CONTRACT`
- `DEEPSCI:CODEBASE-AUDIT-RECORD`
- `DEEPSCI:BASELINE-PROVENANCE-RECORD`
- `DEEPSCI:BASELINE-VERIFICATION-EVIDENCE`
- `DEEPSCI:BASELINE-PAYLOAD-RECORD`
- `DEEPSCI:ACCEPTED-BASELINE-RECORD`
- `DEEPSCI:BASELINE-WAIVER-RECORD`
- `DEEPSCI:BASELINE-BLOCKER-RECORD`
- `DEEPSCI:BASELINE-ROUTE-DECISION`

## Unmatched Skill-Route Substitutions

baseline maps to isomer-rsch-baseline. Source routes to idea, experiment, write, finalize, or blockers map to production DeepSci route decisions.

Where a source route names a DeepScientist skill that has no production DeepSci target in this batch, the runtime page records the route through a semantic decision or blocker placeholder rather than pretending the missing Isomer skill exists.

## Environment Substitutions

- Source `venv`, `uv`, shell, package, Git, scheduler, and environment assumptions map to Pixi-aware Project or Topic Workspace context plus Execution Adapter Command Requests.
- Runtime pages should not require a fixed filesystem layout, virtual environment, or command path unless later storage and execution binding work adds one.
- Compatibility harness examples are allowed only as transitional `isomer-cli ext deepsci call ... --input-json <json-object>` instructions.

## Placeholder Registry

`migrate/placeholders.md` defines every placeholder used by rewritten runtime pages. Every rewritten page that mentions placeholders references that registry.

## Rewrite Targets

- `SKILL-MAIN.md`: native production DeepSci control surface with workflow steps that reference the required support pages.
- `references/route-selection.md`: source-preserved route selection page refactored into trust-per-cost route guidance, preferences, constraints, and quality gates.
- `references/comparability-contract.md`: source-preserved comparability contract page refactored into comparator identity, data, metric, deviation, verdict, and handoff support.
- `references/verification-record-template.md`: production DeepSci support page distilled from source verification, objective evidence, and acceptance-gate rules.
- `references/operational-guidance.md`: source-preserved operational support page refactored into route record, provenance, execution, environment, reuse, and memory rules.
- `references/codebase-audit-checklist.md`: source-preserved audit checklist refactored into focused source-audit support.
- `references/baseline-plan-template.md`: source-preserved route record template refactored into native plan support and template fields.
- `references/baseline-checklist-template.md`: source-preserved gate checklist refactored into acceptance-boundary support and template fields.
- `references/boundary-cases.md`: source-preserved boundary cases refactored into comparison-ready, caveat, weak-provenance, local-path, heavy-route, and repeated-failure support.
- `references/artifact-flow-examples.md`: source-preserved flow examples refactored into native evidence-flow sequences.
- `references/artifact-payload-examples.md`: source-preserved payload examples refactored into accepted, waived, blocked, and route-decision payload support.

## Main Workflow Support Mapping

| Target Workflow Step | Source Support Material | Target Runtime Support |
| --- | --- | --- |
| Choose the acceptance target | `SKILL-SOURCE.md` Match signals, Control workflow step 1, Acceptance targets, Comparator-first rule, Boundary cases, Exit criteria. | `references/route-selection.md`, `references/boundary-cases.md` |
| Select the lightest trustworthy route | `SKILL-SOURCE.md` Control workflow step 1, Comparator-first rule, Route success criteria, Authority and freedom; `references/route-selection.md`; `references/artifact-flow-examples.md`; `references/baseline-plan-template.md`; `references/baseline-checklist-template.md`. | `references/route-selection.md`, `references/artifact-flow-examples.md`, `references/baseline-plan-template.md`, `references/baseline-checklist-template.md` |
| Make comparability explicit | `SKILL-SOURCE.md` Control workflow step 2, Hard acceptance gates, Objective evidence requirements, Core metric contract, Baseline id and variant rules; `references/comparability-contract.md`; `references/artifact-payload-examples.md`. | `references/comparability-contract.md`, `references/artifact-payload-examples.md` |
| Audit only what the route needs | `SKILL-SOURCE.md` Comparator-first rule, Authority and freedom, Operational guidance; `references/codebase-audit-checklist.md`; `references/operational-guidance.md`. | `references/codebase-audit-checklist.md`, `references/operational-guidance.md` |
| Collect and verify necessary evidence | `SKILL-SOURCE.md` Control workflow steps 3-4, AVOID, Constraints, Validation, Verification, Objective evidence requirements, Negative cases; `references/comparability-contract.md`; `references/operational-guidance.md`. | `references/verification-record-template.md`, `references/comparability-contract.md`, `references/operational-guidance.md` |
| Close the baseline gate | `SKILL-SOURCE.md` Control workflow step 5, Hard acceptance gates, Core metric contract, Route success criteria, Negative cases; `references/artifact-flow-examples.md`; `references/artifact-payload-examples.md`; `references/baseline-checklist-template.md`. | `references/artifact-payload-examples.md`, `references/artifact-flow-examples.md`, `references/baseline-checklist-template.md` |
| Route and stop | `SKILL-SOURCE.md` Acceptance targets, Hard acceptance gates, Negative cases and stop rules, Exit criteria; `references/boundary-cases.md`; `references/route-selection.md`. | `references/boundary-cases.md`, `references/route-selection.md` |

## Semantic Match Checks

The rewritten skill must preserve these source behaviors:

- Lightest trustworthy comparator route is chosen before reproduction.
- Comparator identity and acceptance target are explicit.
- Attach, import, or publish alone do not open the gate.
- Comparability contract is explicit before acceptance.
- Verification precedes acceptance.
- Metrics trace to real evidence, not copied or fabricated values.
- Source audit is used only when lighter routes cannot establish trust.
- Caveats and deviations remain visible.
- Baseline id and variant names are stable enough for later citation.
- Gate closes by confirmation, waiver, blocker, or route change.
- Next route is explicit, and baseline work stops once the current acceptance target is satisfied.
