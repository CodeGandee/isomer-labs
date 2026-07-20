# Isomer Research Finalize Production DeepSci Refactor Migration Plan

## Scope

- Source skill: `extern/orphan/DeepScientist/src/skills/finalize`.
- Target skill: `skillset/research-paradigm/deepsci/isomer-rsch-finalize`.
- Migration mode: `refactor-migrate`.
- Source copy: every source file is copied unchanged into `org/src/`.
- Source files covered: `SKILL.md`, `references/checkpoint-memory-template.md`, `references/finalization-checklist.md`, `references/resume-packet-template.md`.
- Source analysis: `org/analysis/analysis-of-finalize.md`.
- Exclusions from deep inspection: package-card and static catalog files are treated as progressive-disclosure reference material when present; runtime behavior is summarized in the source analysis and native production DeepSci pages.

## Term Substitutions

| Source Term | Isomer Labs Term or Treatment |
| --- | --- |
| quest | Research Topic, Research Inquiry, Research Task, or Topic Workspace, depending on the source meaning. |
| quest files and durable quest state | Workspace Runtime records, Artifacts, Evidence Items, Findings, Gates, Decision Records, Provenance Records, and user-provided Research Topic context. |
| stage | production DeepSci research skill route or Workflow Stage context inside a Topic Agent Team Profile. |
| next stage or next anchor | `<...ROUTE_DECISION>` placeholder in this migration, later bound to production DeepSci skill routing. |
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

- `DEEPSCI:FINALIZE-CONTEXT-BRIEF`
- `DEEPSCI:CLAIM-LEDGER`
- `DEEPSCI:FINAL-LIMITATIONS-REPORT`
- `DEEPSCI:FINAL-SUMMARY`
- `DEEPSCI:RESUME-PACKET`
- `DEEPSCI:CLOSURE-DECISION`
- `DEEPSCI:FINALIZE-BLOCKER-RECORD`
- `DEEPSCI:FINALIZE-CONTINUITY-UPDATE`

## Unmatched Skill-Route Substitutions

finalize maps to isomer-rsch-finalize. Source closure routes map to closure decisions and route-back placeholders when evidence gates fail.

Where a source route names a DeepScientist skill that has no production DeepSci target in this batch, the runtime page records the route through a semantic decision or blocker placeholder rather than pretending the missing Isomer skill exists.

## Environment Substitutions

- Source `venv`, `uv`, shell, package, Git, scheduler, and environment assumptions map to Pixi-aware Project or Topic Workspace context plus Execution Adapter Command Requests.
- Runtime pages should not require a fixed filesystem layout, virtual environment, or command path unless later storage and execution binding work adds one.
- Compatibility harness examples are allowed only as transitional `isomer-cli ext deepsci call ... --input-json <json-object>` instructions.

## Placeholder Registry

`migrate/placeholders.md` defines every placeholder used by rewritten runtime pages. Every rewritten page that mentions placeholders references that registry.

## Rewrite Targets

- `SKILL.md`: native production DeepSci control surface.
- `references/closure-gate.md`: Closure Gate.
- `references/claim-ledger-template.md`: Claim Ledger Template.
- `references/final-summary-template.md`: Final Summary Template.
- `references/resume-packet-template.md`: Resume Packet Template.
- `references/finalization-checklist.md`: source-preserved closure checklist and anti-pattern gate.
- `references/checkpoint-memory-template.md`: source-preserved pause-ready checkpoint memory template.

## Main Workflow Support Mapping

| Target Workflow Step | Source Sections and References | Runtime Support Pages |
| --- | --- | --- |
| Gather closure context | `SKILL.md` Preconditions and gate, Truth sources, Required durable outputs, Workflow step 1; `references/finalization-checklist.md`. | `references/closure-gate.md`, `references/finalization-checklist.md` |
| Check closure legitimacy | `SKILL.md` Preconditions and gate, Do not use when, Failure and blocked handling; `references/finalization-checklist.md`. | `references/closure-gate.md`, `references/finalization-checklist.md` |
| Build the claim ledger | `SKILL.md` Workflow step 2, Finalization-quality rules, Required durable outputs; `references/finalization-checklist.md` claim-ledger minimum. | `references/claim-ledger-template.md`, `references/finalization-checklist.md` |
| State limitations and failures | `SKILL.md` Workflow step 3, Stage purpose, Finalization-quality rules; `references/finalization-checklist.md`. | `references/final-summary-template.md`, `references/finalization-checklist.md` |
| Write final state | `SKILL.md` Workflow steps 4-6, Required durable outputs, Memory rules, Artifact rules; `references/resume-packet-template.md`. | `references/final-summary-template.md`, `references/resume-packet-template.md` |
| Choose closure route | `SKILL.md` Research-map role, Workflow step 7, Exit criteria, Interaction discipline; `references/checkpoint-memory-template.md`; `references/resume-packet-template.md`. | `references/resume-packet-template.md`, `references/checkpoint-memory-template.md` |

## Semantic Match Checks

The rewritten skill must preserve these source behaviors:

- Closure context gathered.
- Paper and evidence gates checked.
- Claims classified.
- Limitations explicit.
- Closure decision or blocker recorded.
- Resume path preserved when needed.
- Source closure checklist, checkpoint memory, paper/package gates, claim downgrade history, limitations, failure preservation, and reopen-condition rules remain discoverable from runtime support pages.
