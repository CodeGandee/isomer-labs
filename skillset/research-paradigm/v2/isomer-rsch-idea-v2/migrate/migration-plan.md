# Isomer Research Idea V2 Refactor Migration Plan

## Scope

- Source skill: `extern/orphan/DeepScientist/src/skills/idea`.
- Target skill: `skillset/research-paradigm/v2/isomer-rsch-idea-v2`.
- Migration mode: `refactor-migrate`.
- Source copy: every source file is copied unchanged into `org/src/`.
- Source files covered: `SKILL.md`, `references/controlled-brainstorming-playbook.md`, `references/current-board-packet-template.md`, `references/high-value-idea-sourcing.md`, `references/idea-generation-playbook.md`, `references/idea-thinking-flow.md`, `references/literature-survey-template.md`, `references/objective-contract-template.md`, `references/outline-seeding-example.md`, `references/pre-idea-draft-template.md`, `references/related-work-playbook.md`, `references/research-history-playbook.md`, and 2 more files.
- Source analysis: `org/analysis/analysis-of-idea.md`.
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

- `<IDEA_CONTEXT_BRIEF>`
- `<OBJECTIVE_CONTRACT>`
- `<CURRENT_BOARD_PACKET>`
- `<LITERATURE_SURVEY_REPORT>`
- `<CANDIDATE_IDEA_FRONTIER>`
- `<PRE_IDEA_DRAFT>`
- `<SELECTED_HYPOTHESIS>`
- `<IDEA_ROUTE_DECISION>`
- `<IDEA_BLOCKER_RECORD>`

## Unmatched Skill-Route Substitutions

idea maps to isomer-rsch-idea-v2. Source routes to experiment, optimize, scout, baseline, and paper outline map to v2 route decisions.

Where a source route names a DeepScientist skill that has no v2 target in this batch, the runtime page records the route through a semantic decision or blocker placeholder rather than pretending the missing Isomer skill exists.

## Environment Substitutions

- Source `venv`, `uv`, shell, package, Git, scheduler, and environment assumptions map to Pixi-aware Project or Topic Workspace context plus Execution Adapter Command Requests.
- Runtime pages should not require a fixed filesystem layout, virtual environment, or command path unless later storage and execution binding work adds one.
- Compatibility harness examples are allowed only as transitional `isomer-cli ext deepsci call ... --input-json <json-object>` instructions.

## Placeholder Registry

`migrate/placeholders.md` defines every placeholder used by rewritten runtime pages. Every rewritten page that mentions placeholders references that registry.

## Rewrite Targets

- `SKILL.md`: native v2 control surface.
- `references/objective-contract.md`: Objective Contract.
- `references/idea-sourcing.md`: Idea Sourcing.
- `references/selection-gate.md`: Selection Gate.
- `references/selected-hypothesis-template.md`: Selected Hypothesis Template.
- `references/literature-survey-template.md`: Literature Survey Template.

## Semantic Match Checks

The rewritten skill must preserve these source behaviors:

- Objective grounded.
- Current board recovered.
- Literature refreshed only where needed.
- Candidate frontier bounded.
- One falsifiable route selected or blocker recorded.
