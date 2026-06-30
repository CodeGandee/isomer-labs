# Isomer Research Analysis V2 Refactor Migration Plan

## Scope

- Source skill: `extern/orphan/DeepScientist/src/skills/analysis-campaign`.
- Target skill: `skillset/research-paradigm/v2/isomer-rsch-analysis-v2`.
- Migration mode: `refactor-migrate`.
- Source copy: every source file is copied unchanged into `org/src/`.
- Source files covered: `SKILL.md`, `references/artifact-flow-examples.md`, `references/boundary-cases.md`, `references/campaign-checklist-template.md`, `references/campaign-design.md`, `references/campaign-plan-template.md`, `references/operational-guidance.md`, `references/writing-facing-slice-examples.md`.
- Source analysis: `org/analysis/analysis-of-analysis-campaign.md`.
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

- `<ANALYSIS_CONTEXT_BRIEF>`
- `<PARENT_RESULT_EVIDENCE>`
- `<ANALYSIS_SLICE_PLAN>`
- `<ANALYSIS_SLICE_RECORD>`
- `<ANALYSIS_CAMPAIGN_SUMMARY>`
- `<ANALYSIS_ROUTE_DECISION>`
- `<ANALYSIS_BLOCKER_RECORD>`
- `<ANALYSIS_CONTINUITY_UPDATE>`

## Unmatched Skill-Route Substitutions

analysis-campaign maps to isomer-rsch-analysis-v2. Source routes to experiment, idea, write, decision, review, or rebuttal map to v2 route decisions where matching v2 skills exist, otherwise to semantic route placeholders in the local registry.

Where a source route names a DeepScientist skill that has no v2 target in this batch, the runtime page records the route through a semantic decision or blocker placeholder rather than pretending the missing Isomer skill exists.

## Environment Substitutions

- Source `venv`, `uv`, shell, package, Git, scheduler, and environment assumptions map to Pixi-aware Project or Topic Workspace context plus Execution Adapter Command Requests.
- Runtime pages should not require a fixed filesystem layout, virtual environment, or command path unless later storage and execution binding work adds one.
- Compatibility harness examples are allowed only as transitional `isomer-cli ext deepsci call ... --input-json <json-object>` instructions.

## Placeholder Registry

`migrate/placeholders.md` defines every placeholder used by rewritten runtime pages. Every rewritten page that mentions placeholders references that registry.

## Rewrite Targets

- `SKILL.md`: native v2 control surface.
- `references/campaign-design.md`: Campaign Design.
- `references/slice-record-template.md`: Analysis Slice Record Template.
- `references/evidence-gate.md`: Analysis Evidence Gate.
- `references/operational-guidance.md`: Operational Guidance.

## Semantic Match Checks

The rewritten skill must preserve these source behaviors:

- Parent result exists.
- Slice plan is bounded.
- Comparability is explicit.
- Slice records precede campaign claims.
- Next route or blocker is explicit.
