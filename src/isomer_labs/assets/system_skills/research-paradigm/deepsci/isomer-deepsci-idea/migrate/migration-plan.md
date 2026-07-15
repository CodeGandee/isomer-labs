# Isomer Research Idea Production DeepSci Refactor Migration Plan

## Scope

- Source skill: `extern/orphan/DeepScientist/src/skills/idea`.
- Target skill: `skillset/research-paradigm/deepsci/isomer-rsch-idea`.
- Migration mode: `refactor-migrate`.
- Source copy: every source file is copied unchanged into `org/src/`.
- Runtime support copy: every source reference page is copied and refactored under `references/` with the source-relative path preserved. The source entrypoint is not copied over target `SKILL.md`, and target `agents/openai.yaml` is preserved.
- Source files covered: `SKILL.md`, `references/controlled-brainstorming-playbook.md`, `references/current-board-packet-template.md`, `references/high-value-idea-sourcing.md`, `references/idea-generation-playbook.md`, `references/idea-thinking-flow.md`, `references/literature-survey-template.md`, `references/objective-contract-template.md`, `references/outline-seeding-example.md`, `references/pre-idea-draft-template.md`, `references/related-work-playbook.md`, `references/research-history-playbook.md`, `references/research-outline-template.md`, and `references/selection-gate.md`.
- Source analysis: `org/analysis/analysis-of-idea.md`.
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

- `DEEPSCI:IDEA-CONTEXT-BRIEF`
- `DEEPSCI:OBJECTIVE-CONTRACT`
- `DEEPSCI:CURRENT-BOARD-PACKET`
- `DEEPSCI:LITERATURE-SURVEY-REPORT`
- `DEEPSCI:RELATED-WORK-MAP`
- `DEEPSCI:LIMITATIONS-MAP`
- `DEEPSCI:MECHANISM-FRAMING`
- `DEEPSCI:RAW-IDEA-SLATE`
- `DEEPSCI:CANDIDATE-IDEA-FRONTIER`
- `DEEPSCI:REJECTED-AND-DEFERRED-IDEAS`
- `DEEPSCI:PRE-IDEA-DRAFT`
- `DEEPSCI:SELECTED-HYPOTHESIS`
- `DEEPSCI:SELECTED-IDEA-DRAFT`
- `DEEPSCI:IDEA-ROUTE-DECISION`
- `DEEPSCI:IDEA-BLOCKER-RECORD`
- `DEEPSCI:IDEA-MEMORY-RECORD`
- `DEEPSCI:PAPER-OUTLINE-SEED`
- `DEEPSCI:RESEARCH-OUTLINE-NOTE`

## Unmatched Skill-Route Substitutions

idea maps to isomer-rsch-idea. Source routes to experiment, optimize, scout, baseline, and paper outline map to production DeepSci route decisions.

Where a source route names a DeepScientist skill that has no production DeepSci target in this batch, the runtime page records the route through a semantic decision or blocker placeholder rather than pretending the missing Isomer skill exists.

## Environment Substitutions

- Source `venv`, `uv`, shell, package, Git, scheduler, and environment assumptions map to Pixi-aware Project or Topic Workspace context plus Execution Adapter Command Requests.
- Runtime pages should not require a fixed filesystem layout, virtual environment, or command path unless later storage and execution binding work adds one.
- Compatibility harness examples are allowed only as transitional `isomer-cli ext deepsci call ... --input-json <json-object>` instructions.

## Placeholder Registry

`migrate/placeholders.md` defines every placeholder used by rewritten runtime pages. Every rewritten page that mentions placeholders references that registry.

## Rewrite Targets

- `SKILL.md`: native production DeepSci control surface.
- `references/objective-contract-template.md`: Objective Contract Template.
- `references/current-board-packet-template.md`: Current Board Packet Template.
- `references/high-value-idea-sourcing.md`: High-Value Idea Sourcing.
- `references/related-work-playbook.md`: Related-Work Playbook.
- `references/research-history-playbook.md`: Research History Playbook.
- `references/literature-survey-template.md`: Literature Survey Report Template.
- `references/idea-thinking-flow.md`: Idea Thinking Flow.
- `references/idea-generation-playbook.md`: Idea Generation Playbook.
- `references/controlled-brainstorming-playbook.md`: Controlled Brainstorming Playbook.
- `references/pre-idea-draft-template.md`: Pre-Idea Draft Template.
- `references/selection-gate.md`: Selection Gate And Handoff.
- `references/outline-seeding-example.md`: Outline Seeding Example.
- `references/research-outline-template.md`: Research Outline Template.
- `references/selected-hypothesis-template.md`: production DeepSci selected hypothesis handoff page distilled from source output contract and selection gate.
- `references/objective-contract.md` and `references/idea-sourcing.md`: compatibility pages that point to the preserved source-reference runtime pages.

## Main Workflow Support Mapping

| Target Workflow Step | Source Sections and References | Runtime Support Pages |
| --- | --- | --- |
| Check readiness and recover context | `SKILL.md` Match signals, Use when, Do not use when, Preconditions and gate, Failure and blocked handling, Exit criteria; `references/selection-gate.md` promotion gate. | `references/objective-contract-template.md`, `references/current-board-packet-template.md`, `references/selection-gate.md` |
| Lock the objective and board | `SKILL.md` Control workflow steps 1-2, Constraints, Validation, Three-layer todo contract, Current-node plan and checklist; `references/objective-contract-template.md`; `references/current-board-packet-template.md`. | `references/objective-contract-template.md`, `references/current-board-packet-template.md` |
| Plan and refresh evidence | `SKILL.md` Control workflow step 4, Truth sources, Related-work and novelty mandate, Memory rules; `references/literature-survey-template.md`; `references/related-work-playbook.md`; `references/research-history-playbook.md`. | `references/literature-survey-template.md`, `references/related-work-playbook.md`, `references/research-history-playbook.md` |
| Extract the limitation and mechanism frame | `SKILL.md` Control workflow steps 3 and 5, Direction-shaping protocol, Thinking protocol, Stage purpose; `references/high-value-idea-sourcing.md`; `references/idea-thinking-flow.md`; `references/research-outline-template.md`. | `references/high-value-idea-sourcing.md`, `references/idea-thinking-flow.md`, `references/research-outline-template.md` |
| Generate a bounded frontier | `SKILL.md` Control workflow steps 6-7, Creative-divergence protocol, Integrated ideation workflow, Common ideation failure modes; `references/controlled-brainstorming-playbook.md`; `references/idea-generation-playbook.md`. | `references/controlled-brainstorming-playbook.md`, `references/idea-generation-playbook.md` |
| Challenge serious candidates | `SKILL.md` Control workflow step 8, Draft-before-submit SOP, Non-negotiable rules; `references/pre-idea-draft-template.md`. | `references/pre-idea-draft-template.md` |
| Select, branch, reject, or block | `SKILL.md` Control workflow steps 9-10, Idea output contract, Idea quality rules, Novelty and research-value rules, Artifact rules, Failure and blocked handling; `references/selection-gate.md`. | `references/selection-gate.md`, `references/selected-hypothesis-template.md` |
| Record durable outcomes and route next | `SKILL.md` Required durable outputs, Memory rules, Artifact rules, Research-map role, Exit criteria; `references/literature-survey-template.md`; `references/outline-seeding-example.md`; `references/research-outline-template.md`. | `references/literature-survey-template.md`, `references/outline-seeding-example.md`, `references/research-outline-template.md` |

## Semantic Match Checks

The rewritten skill must preserve these source behaviors:

- Objective grounded before ideation, with false-progress and hard constraints explicit.
- Current board recovered before widening, with incumbent, blocker, stale routes, and validation budget class explicit.
- Durable memory and local evidence checked before external search.
- Literature refreshed or deliberately reused, with related-work map, history view, closest-prior-work table, novelty or value verdict, and citation-ready support.
- Limitation, contradiction, mechanism framing, and lever bucket extracted before candidate generation.
- Bounded divergence run with route-family diversity unless strong durable evidence justifies abbreviation.
- Candidate frontier narrowed to serious decision packages rather than slogans.
- Pre-idea draft or equivalent challenge memo written for serious surviving candidates before promotion.
- Selection gate applied with value, feasibility, novelty, falsifiability, evidence quality, constraint fit, anti-win, minimal validation, and abandonment checks.
- One falsifiable route selected, an algorithm-first frontier routed to optimize, a branch or reject decision recorded, or a blocker recorded.
- Durable outcome records and reusable memory or outline seeds preserved when the source rules call for them.
