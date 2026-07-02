# Isomer Research Experiment V2 Refactor Migration Plan

## Scope

- Source skill: `extern/orphan/DeepScientist/src/skills/experiment`.
- Target skill: `skillset/research-paradigm/v2/isomer-rsch-experiment-v2`.
- Migration mode: `refactor-migrate`.
- Source copy: every source file is copied unchanged into `org/src/`.
- Runtime support copy: every source file is copied and refactored under the target runtime tree with source-relative paths preserved, except the source entrypoint and `agents/openai.yaml`.
- Source files covered: `SKILL.md`, `references/evidence-ladder.md`, `references/execution-playbook.md`, `references/main-experiment-checklist-template.md`, `references/main-experiment-plan-template.md`, `references/operational-guidance.md`.
- Source analysis: `org/analysis/analysis-of-experiment.md`.
- Exclusions from deep inspection: package-card and static catalog files are treated as progressive-disclosure reference material when present; runtime behavior is summarized in the source analysis and native v2 pages.

## Term Substitutions

| Source Term | Isomer Labs Term or Treatment |
| --- | --- |
| quest | Research Topic, Research Inquiry, Research Task, or Topic Workspace, depending on the source meaning. |
| quest files and durable quest state | Workspace Runtime records, Artifacts, Evidence Items, Findings, Gates, Decision Records, Provenance Records, and user-provided Research Topic context. |
| stage | v2 research skill route or Workflow Stage context inside a Topic Agent Team Profile. |
| next stage or next anchor | `<EXPERIMENT_ROUTE_DECISION>` or `<EXPERIMENT_BLOCKER_RECORD>`, later bound to v2 skill routing. |
| source templates and fixed paths | Semantic placeholders in `migrate/placeholders.md` until Isomer storage bindings are finalized. |
| `PLAN.md` | `<EXPERIMENT_PLAN>` until Isomer storage bindings are finalized. |
| `CHECKLIST.md` | `<EXPERIMENT_CHECKLIST>` until Isomer storage bindings are finalized. |

## Harness Substitutions

| Source Harness or Tool Rule | Isomer Labs Treatment |
| --- | --- |
| `memory.*` | Prefer Workspace Runtime-backed retrieval or recording. When compatibility is required, use `isomer-cli ext deepsci call memory.<tool> --input-json <json-object>` and status the result with the local placeholders. |
| `artifact.*` | Prefer Isomer Artifacts, Evidence Items, Findings, Decision Records, Gates, and Workspace Runtime records. When compatibility is required, use `isomer-cli ext deepsci call artifact.<tool> --input-json <json-object>` and status semantic meaning with placeholders. |
| `bash_exec(...)` | Use an Execution Adapter Command Request or the DeepScientist-compatible extension call for shell, CLI, Python, git, package, scheduler, or environment work. Do not describe native shell calls as the final skill contract. |
| Source durable run directories, summaries, metric files, and logs | Use `<EXPERIMENT_ARTIFACT_MANIFEST>`, `<MAIN_RUN_RECORD>`, `<EXPERIMENT_RESULT_SUMMARY>`, and related placeholders until storage bindings are finalized. |

## Storage and Artifact Substitutions

The migrated runtime pages do not bind source artifacts to concrete paths. They use the local placeholders defined in `migrate/placeholders.md`:

- `<EXPERIMENT_CONTEXT_BRIEF>`
- `<EXPERIMENT_CONTRACT>`
- `<EXPERIMENT_PLAN>`
- `<EXPERIMENT_CHECKLIST>`
- `<IMPLEMENTATION_CHANGE_MAP>`
- `<SMOKE_CHECK_RECORD>`
- `<MAIN_RUN_RECORD>`
- `<EXPERIMENT_ARTIFACT_MANIFEST>`
- `<CLAIM_VALIDATION_RECORD>`
- `<EXPERIMENT_RESULT_SUMMARY>`
- `<EXPERIMENT_ROUTE_DECISION>`
- `<EXPERIMENT_BLOCKER_RECORD>`

## Unmatched Skill-Route Substitutions

experiment maps to isomer-rsch-experiment-v2. Source routes to optimize, analysis-campaign, idea, write, decision, or finalize map to v2 route decisions.

Where a source route names a DeepScientist skill that has no v2 target in this batch, the runtime page records the route through a semantic decision or blocker placeholder rather than pretending the missing Isomer skill exists.

## Environment Substitutions

- Source `venv`, `uv`, shell, package, Git, scheduler, and environment assumptions map to Pixi-aware Project or Topic Workspace context plus Execution Adapter Command Requests.
- Runtime pages should not require a fixed filesystem layout, virtual environment, or command path unless later storage and execution binding work adds one.
- Compatibility harness examples are allowed only as transitional `isomer-cli ext deepsci call ... --input-json <json-object>` instructions.

## Placeholder Registry

`migrate/placeholders.md` defines every placeholder used by rewritten runtime pages. Every rewritten page that mentions placeholders references that registry.

## Rewrite Targets

- `SKILL.md`: native v2 control surface with workflow steps that reference the required support pages.
- `references/evidence-ladder.md`: source-preserved evidence target support page refactored into guidance, preferences, constraints, and quality gates.
- `references/execution-playbook.md`: source-preserved execution support page refactored into preflight, workspace, implementation, smoke, long-run monitoring, diagnosis, validation, and routing support.
- `references/main-experiment-plan-template.md`: source-preserved plan template refactored into native plan guidance and template fields.
- `references/main-experiment-checklist-template.md`: source-preserved checklist template refactored into native live-control guidance and template fields.
- `references/operational-guidance.md`: source-preserved operational support page refactored into planning, boundary, resource, durable-output, memory, evidence-record, and charting rules.
- `references/experiment-contract.md`: v2 support page distilled from source entrypoint run-contract and planning rules.
- `references/run-record-template.md`: v2 support page distilled from source entrypoint and execution-playbook recording rules.

## Main Workflow Support Mapping

| Target Workflow Step | Source Support Material | Target Runtime Support |
| --- | --- | --- |
| Lock the run contract | `SKILL.md` Quick workflow, Required plan and checklist, Control workflow step 1, Truth sources, Evidence ladder note, Planning note; `references/evidence-ladder.md`; `references/main-experiment-plan-template.md`; `references/execution-playbook.md` section 1. | `references/experiment-contract.md`, `references/main-experiment-plan-template.md`, `references/evidence-ladder.md` |
| Prepare the control surface | `SKILL.md` Required plan and checklist, Planning note, Operational guidance; `references/main-experiment-plan-template.md`; `references/main-experiment-checklist-template.md`; `references/operational-guidance.md`. | `references/main-experiment-plan-template.md`, `references/main-experiment-checklist-template.md`, `references/operational-guidance.md` |
| Map and implement the minimum change | `SKILL.md` Quick workflow, Control workflow step 2, AVOID, Constraints, Non-negotiable rules, Truth sources; `references/execution-playbook.md` sections 2-4; `references/main-experiment-plan-template.md` code translation section. | `references/execution-playbook.md`, `references/main-experiment-plan-template.md` |
| Run only useful smoke checks | `SKILL.md` Control workflow step 3, Run-quality rules, Acceptance gate; `references/execution-playbook.md` sections 2, 5, and 5.1; `references/main-experiment-checklist-template.md` smoke section. | `references/execution-playbook.md`, `references/main-experiment-checklist-template.md` |
| Execute and monitor honestly | `SKILL.md` Control workflow step 4, Interaction discipline, Tool discipline, Operational guidance, Required durable outputs; `references/execution-playbook.md` sections 5, 5.1, 5.2; `references/operational-guidance.md`. | `references/execution-playbook.md`, `references/operational-guidance.md` |
| Validate and record the result | `SKILL.md` Validation, Required durable outputs, Run-quality rules, Acceptance gate, Failure and blocked handling; `references/execution-playbook.md` sections 6-7; `references/operational-guidance.md`; `references/evidence-ladder.md`. | `references/run-record-template.md`, `references/evidence-ladder.md`, `references/operational-guidance.md` |
| Route from evidence | `SKILL.md` Control workflow step 5, Acceptance gate, Failure and blocked handling, Exit criteria; `references/execution-playbook.md` section 8. | `references/run-record-template.md`, `references/execution-playbook.md` |

## Semantic Match Checks

The rewritten skill must preserve these source behaviors:

- Run contract locked before code or compute work starts.
- Planning and checklist surfaces used when run complexity, cost, branch sensitivity, or duration requires them.
- Comparator basis remains read-only unless a recorded route says otherwise.
- Minimal hypothesis-bound change replaces broad cleanup or hidden scope expansion.
- Smoke or pilot checks reduce uncertainty but never count as main evidence.
- Real run preserves commands, configs, logs, outputs, seeds, metric files, environment facts, and last-known-good state.
- Long-running work is monitored from durable signals and invalid or superseded work is stopped and recorded.
- Metrics are complete, finite, traceable, and comparable or deviations are explicit.
- Source failure and blocked states remain first-class outcomes.
- Durable result records include evaluation summary, claim update, baseline relation, failure mode, and next action.
- Next route is explicit and chosen from evidence.
