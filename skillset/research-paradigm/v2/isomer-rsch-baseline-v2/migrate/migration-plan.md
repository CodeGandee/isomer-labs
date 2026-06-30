# Isomer Research Baseline V2 Refactor Migration Plan

## Scope

- Source skill: `extern/orphan/DeepScientist/src/skills/baseline`.
- Target skill: `skillset/research-paradigm/v2/isomer-rsch-baseline-v2`.
- Migration mode: `refactor-migrate`.
- Source copy: every source file is copied unchanged into `org/src/`.
- Source files covered: `SKILL.md`, `references/artifact-flow-examples.md`, `references/artifact-payload-examples.md`, `references/baseline-checklist-template.md`, `references/baseline-plan-template.md`, `references/boundary-cases.md`, `references/codebase-audit-checklist.md`, `references/comparability-contract.md`, `references/operational-guidance.md`, `references/route-selection.md`.
- Source analysis: `org/analysis/analysis-of-baseline.md`.
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
| `memory.*` | Prefer Workspace Runtime-backed retrieval or recording. When compatibility is required, use `isomer-cli ext deepsci call memory.<tool> --input-json <json-object>` and summarize the result with the local placeholders. |
| `artifact.*` | Prefer Isomer Artifacts, Evidence Items, Findings, Decision Records, Gates, and Workspace Runtime records. When compatibility is required, use `isomer-cli ext deepsci call artifact.<tool> --input-json <json-object>` and summarize semantic meaning with placeholders. |
| `bash_exec(...)` | Use an Execution Adapter Command Request or the DeepScientist-compatible extension call for shell, CLI, Python, git, package, scheduler, or environment work. Do not describe native shell calls as the final skill contract. |
| Quest files such as `SUMMARY.md`, `status.md`, `PLAN.md`, or source templates | Treat as source artifact-like records. Runtime pages use placeholders until Isomer storage bindings are finalized. |


## Storage and Artifact Substitutions

The migrated runtime pages do not bind source artifacts to concrete paths. They use the local placeholders defined in `migrate/placeholders.md`:

- `<BASELINE_CONTEXT_BRIEF>`
- `<COMPARATOR_ROUTE_RECORD>`
- `<COMPARABILITY_CONTRACT>`
- `<BASELINE_VERIFICATION_EVIDENCE>`
- `<ACCEPTED_BASELINE_RECORD>`
- `<BASELINE_WAIVER_RECORD>`
- `<BASELINE_BLOCKER_RECORD>`
- `<BASELINE_ROUTE_DECISION>`

## Unmatched Skill-Route Substitutions

baseline maps to isomer-rsch-baseline-v2. Source routes to idea, experiment, write, finalize, or blockers map to v2 route decisions.

Where a source route names a DeepScientist skill that has no v2 target in this batch, the runtime page records the route through a semantic decision or blocker placeholder rather than pretending the missing Isomer skill exists.

## Environment Substitutions

- Source `venv`, `uv`, shell, package, Git, scheduler, and environment assumptions map to Pixi-aware Project or Topic Workspace context plus Execution Adapter Command Requests.
- Runtime pages should not require a fixed filesystem layout, virtual environment, or command path unless later storage and execution binding work adds one.
- Compatibility harness examples are allowed only as transitional `isomer-cli ext deepsci call ... --input-json <json-object>` instructions.

## Placeholder Registry

`migrate/placeholders.md` defines every placeholder used by rewritten runtime pages. Every rewritten page that mentions placeholders references that registry.

## Rewrite Targets

- `SKILL.md`: native v2 control surface.
- `references/route-selection.md`: Route Selection.
- `references/comparability-contract.md`: Comparability Contract.
- `references/verification-record-template.md`: Verification Record Template.
- `references/operational-guidance.md`: Operational Guidance.

## Semantic Match Checks

The rewritten skill must preserve these source behaviors:

- Lightest trustworthy comparator route chosen.
- Comparability contract explicit.
- Verification precedes acceptance.
- Gate closes by confirmation, waiver, or blocker.
