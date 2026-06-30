# Isomer Research Science V2 Refactor Migration Plan

## Scope

- Source skill: `extern/orphan/DeepScientist/src/skills/science`.
- Target skill: `skillset/research-paradigm/v2/isomer-rsch-science-v2`.
- Migration mode: `refactor-migrate`.
- Source copy: every source file is copied unchanged into `org/src/`.
- Source files covered: `PROVENANCE.md`, `SKILL.md`, `references/artifact-science-tool.md`, `references/claim-type-discipline.md`, `references/domain-index.md`, `references/hpc-via-bash-exec.md`, `references/package-check-playbook.md`, `references/package-index.min.json`, `references/packages/abinit.md`, `references/packages/acts.md`, `references/packages/aiida-core.md`, `references/packages/alamode.md`, and 166 more files.
- Source analysis: `org/analysis/analysis-of-science.md`.
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

- `<SCIENCE_TASK_BRIEF>`
- `<SCIENCE_PACKAGE_CHECK>`
- `<SCIENCE_RUN_RECORD>`
- `<SCIENCE_VALIDATION_RESULT>`
- `<SCIENCE_CLAIM_RECORD>`
- `<SCIENCE_EVIDENCE_GRAPH_UPDATE>`
- `<SCIENCE_BLOCKER_RECORD>`
- `<SCIENCE_ROUTE_DECISION>`

## Unmatched Skill-Route Substitutions

science maps to isomer-rsch-science-v2. Source artifact.science routes map to local science evidence placeholders and compatibility harness calls.

Where a source route names a DeepScientist skill that has no v2 target in this batch, the runtime page records the route through a semantic decision or blocker placeholder rather than pretending the missing Isomer skill exists.

## Environment Substitutions

- Source `venv`, `uv`, shell, package, Git, scheduler, and environment assumptions map to Pixi-aware Project or Topic Workspace context plus Execution Adapter Command Requests.
- Runtime pages should not require a fixed filesystem layout, virtual environment, or command path unless later storage and execution binding work adds one.
- Compatibility harness examples are allowed only as transitional `isomer-cli ext deepsci call ... --input-json <json-object>` instructions.

## Placeholder Registry

`migrate/placeholders.md` defines every placeholder used by rewritten runtime pages. Every rewritten page that mentions placeholders references that registry.

## Rewrite Targets

- `SKILL.md`: native v2 control surface.
- `references/science-task-brief.md`: Science Task Brief.
- `references/evidence-recording.md`: Evidence Recording.
- `references/package-routing.md`: Package Routing.
- `references/hpc-execution-adapter.md`: HPC Execution Adapter.
- `references/claim-discipline.md`: Claim Discipline.

## Semantic Match Checks

The rewritten skill must preserve these source behaviors:

- Science task framed.
- Package cards are not availability proof.
- Execution uses Isomer command surfaces.
- Evidence nodes precede claims.
- Claim type calibrated.
- Blockers explicit.
