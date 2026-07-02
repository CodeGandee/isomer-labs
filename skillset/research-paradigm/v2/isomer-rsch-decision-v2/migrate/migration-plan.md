# Isomer Research Decision V2 Refactor Migration Plan

## Scope

- Source skill: `extern/orphan/DeepScientist/src/skills/decision`.
- Target skill: `skillset/research-paradigm/v2/isomer-rsch-decision-v2`.
- Migration mode: `refactor-migrate`.
- Source copy: every source file is copied unchanged into `org/src/`.
- Source files covered: `SKILL.md`, `references/checkpoint-memory-template.md`, `references/operational-guidance.md`, `references/research-route-criteria.md`, `references/strategic-decision-template.md`.
- Source analysis: `org/analysis/analysis-of-decision.md`.
- Exclusions from deep inspection: package-card and static catalog files are treated as progressive-disclosure reference material when present; runtime behavior is summarized in the source analysis and native v2 pages.

## Term Substitutions

| Source Term | Isomer Labs Term or Treatment |
| --- | --- |
| quest | Research Topic, Research Inquiry, Research Task, or Topic Workspace, depending on the source meaning. |
| quest files and durable quest state | Workspace Runtime records, Artifacts, Evidence Items, Findings, Gates, Decision Records, Provenance Records, and user-provided Research Topic context. |
| stage | v2 research skill route or Workflow Stage context inside a Topic Agent Team Profile. |
| next stage or next anchor | `<...ROUTE_DECISION>` placeholder in this migration, later bound to v2 skill routing. |
| source templates and fixed paths | Semantic placeholders in `migrate/placeholders.md` until Isomer storage bindings are finalized. |

## Harness Substitutions

| Source Harness or Tool Rule | Isomer Labs Treatment |
| --- | --- |
| `memory.*` | Prefer Workspace Runtime-backed retrieval or recording. When compatibility is required, use `isomer-cli ext deepsci call memory.<tool> --input-json <json-object>` and status the result with the local placeholders. |
| `artifact.*` | Prefer Isomer Artifacts, Evidence Items, Findings, Decision Records, Gates, and Workspace Runtime records. When compatibility is required, use `isomer-cli ext deepsci call artifact.<tool> --input-json <json-object>` and status semantic meaning with placeholders. |
| `bash_exec(...)` | Use an Execution Adapter Command Request or the DeepScientist-compatible extension call for shell, CLI, Python, git, package, scheduler, or environment work. Do not describe native shell calls as the final skill contract. |
| Quest files such as `SUMMARY.md`, `status.md`, `PLAN.md`, or source templates | Treat as source artifact-like records. Runtime pages use placeholders until Isomer storage bindings are finalized. |


## Storage and Artifact Substitutions

The migrated runtime pages do not bind source artifacts to concrete paths. They use the local placeholders defined in `migrate/placeholders.md`:

- `<DECISION_CONTEXT_BRIEF>`
- `<ROUTE_QUESTION>`
- `<DECISION_EVIDENCE_PACKET>`
- `<ROUTE_DECISION_RECORD>`
- `<DECISION_CHECKPOINT_MEMORY>`
- `<USER_DECISION_REQUEST>`
- `<DECISION_BLOCKER_RECORD>`

## Unmatched Skill-Route Substitutions

decision maps to isomer-rsch-decision-v2. Source canonical actions map to v2 skills or placeholders for missing paper/write/review surfaces.

Where a source route names a DeepScientist skill that has no v2 target in this batch, the runtime page records the route through a semantic decision or blocker placeholder rather than pretending the missing Isomer skill exists.

## Environment Substitutions

- Source `venv`, `uv`, shell, package, Git, scheduler, and environment assumptions map to Pixi-aware Project or Topic Workspace context plus Execution Adapter Command Requests.
- Runtime pages should not require a fixed filesystem layout, virtual environment, or command path unless later storage and execution binding work adds one.
- Compatibility harness examples are allowed only as transitional `isomer-cli ext deepsci call ... --input-json <json-object>` instructions.

## Placeholder Registry

`migrate/placeholders.md` defines every placeholder used by rewritten runtime pages. Every rewritten page that mentions placeholders references that registry.

## Rewrite Targets

- `SKILL.md`: native v2 control surface.
- `references/operational-guidance.md`: source-preserved tactical decision guidance.
- `references/research-route-criteria.md`: source-preserved route-selection criteria.
- `references/strategic-decision-template.md`: source-preserved decision record template.
- `references/checkpoint-memory-template.md`: Checkpoint Memory Template.
- `references/canonical-actions.md`: extracted source-entrypoint canonical action vocabulary.
- `references/route-criteria.md`: compatibility redirect to `references/research-route-criteria.md`.
- `references/decision-record-template.md`: compatibility redirect to `references/strategic-decision-template.md`.

## Main Workflow Support Mapping

| Target Workflow Step | Source Sections and References | Runtime Support Pages |
| --- | --- | --- |
| Check decision readiness | `SKILL.md` Match signals, Do not use when, Control workflow step 1, Preconditions implied by truth sources, Operational guidance. | `references/operational-guidance.md` |
| State the route question | `SKILL.md` Control workflow step 2, Truth sources, Required decision record; `references/research-route-criteria.md`. | `references/research-route-criteria.md` |
| Choose the smallest canonical action | `SKILL.md` Control workflow step 3, Canonical actions, Constraints, AVOID/pitfalls; `references/research-route-criteria.md`; `references/operational-guidance.md`. | `references/canonical-actions.md`, `references/research-route-criteria.md`, `references/operational-guidance.md` |
| Record the verdict | `SKILL.md` Control workflow step 4, Required decision record, Decision-quality rules; `references/strategic-decision-template.md`. | `references/strategic-decision-template.md` |
| Preserve the resume point | `SKILL.md` Control workflow step 5, Interaction discipline, Memory note, Exit criteria; `references/checkpoint-memory-template.md`; `references/operational-guidance.md`. | `references/checkpoint-memory-template.md`, `references/operational-guidance.md` |

## Semantic Match Checks

The rewritten skill must preserve these source behaviors:

- Decision readiness checked.
- Route question explicit.
- Smallest canonical action selected.
- Decision recorded durably.
- User asked only for real preference or scope choices.
- Source operational rules for baseline reuse, paper-route stop loss, optimization-frontier routing, package selection, and checkpoint memory remain discoverable from runtime support pages.
