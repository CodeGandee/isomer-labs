# Isomer Research Optimize Production DeepSci Refactor Migration Plan

## Scope

- Source skill: `extern/orphan/DeepScientist/src/skills/optimize`.
- Target skill: `skillset/research-paradigm/deepsci/isomer-rsch-optimize`.
- Migration mode: `refactor-migrate`.
- Source copy: every source file is copied unchanged into `org/src/`.
- Runtime support copy: every source file is copied and refactored under the target runtime tree with source-relative paths preserved, except the source entrypoint and `agents/openai.yaml`.
- Source files covered: `SKILL-SOURCE.md`, `references/brief-shaping-playbook.md`, `references/candidate-board-template.md`, `references/candidate-ranking-template.md`, `references/codegen-route-playbook.md`, `references/debug-response-template.md`, `references/frontier-review-template.md`, `references/fusion-playbook.md`, `references/method-brief-template.md`, `references/operational-guidance.md`, `references/optimization-memory-template.md`, `references/optimize-checklist-template.md`, `references/plateau-response-playbook.md`, `references/prompt-patterns.md`.
- Source analysis: `org/analysis/analysis-of-optimize.md`.
- Exclusions from deep inspection: package-card and static catalog files are treated as progressive-disclosure reference material when present; runtime behavior is summarized in the source analysis and native production DeepSci pages.

## Term Substitutions

| Source Term | Isomer Labs Term or Treatment |
| --- | --- |
| quest | Research Topic, Research Inquiry, Research Task, or Topic Workspace, depending on the source meaning. |
| quest files and durable quest state | Workspace Runtime records, Artifacts, Evidence Items, Findings, Gates, Decision Records, Provenance Records, and user-provided Research Topic context. |
| stage | production DeepSci research skill route or Workflow Stage context inside a Topic Agent Team Profile. |
| next stage or next anchor | `DEEPSCI:OPTIMIZE-ROUTE-DECISION` or `DEEPSCI:OPTIMIZE-BLOCKER-RECORD`, later bound to production DeepSci skill routing. |
| source templates and fixed paths | Semantic placeholders in `migrate/placeholders.md` until Isomer storage bindings are finalized. |
| `OPTIMIZE_CHECKLIST.md` | `DEEPSCI:OPTIMIZE-CHECKLIST` until storage binding is finalized. |
| `CANDIDATE_BOARD.md` | `DEEPSCI:CANDIDATE-BOARD` until storage binding is finalized. |

## Harness Substitutions

| Source Harness or Tool Rule | Isomer Labs Treatment |
| --- | --- |
| `memory.*` | Prefer Workspace Runtime-backed retrieval or recording. When compatibility is required, use `isomer-cli ext deepsci call memory.<tool> --input-json <json-object>` and status the result with the local placeholders. |
| `artifact.*` | Prefer Isomer Artifacts, Evidence Items, Findings, Decision Records, Gates, and Workspace Runtime records. When compatibility is required, use `isomer-cli ext deepsci call artifact.<tool> --input-json <json-object>` and status semantic meaning with placeholders. |
| `bash_exec(...)` | Use an Execution Adapter Command Request or the DeepScientist-compatible extension call for shell, CLI, Python, git, package, scheduler, or environment work. Do not describe native shell calls as the final skill contract. |
| Source candidate, line, report, frontier, and route records | Use candidate, line, attempt, frontier review, memory-card, route-decision, and blocker placeholders until storage bindings are finalized. |

## Storage and Artifact Substitutions

The migrated runtime pages do not bind source artifacts to concrete paths. They use the local placeholders defined in `migrate/placeholders.md`:

- `DEEPSCI:OPTIMIZATION-CONTEXT-BRIEF`
- `DEEPSCI:OPTIMIZATION-FRONTIER`
- `DEEPSCI:OPTIMIZE-CHECKLIST`
- `DEEPSCI:CANDIDATE-BOARD`
- `DEEPSCI:CANDIDATE-BRIEF`
- `DEEPSCI:METHOD-BRIEF`
- `DEEPSCI:CANDIDATE-RANKING`
- `DEEPSCI:CODEGEN-ROUTE-PLAN`
- `DEEPSCI:PROMOTED-OPTIMIZATION-LINE`
- `DEEPSCI:OPTIMIZATION-ATTEMPT-RECORD`
- `DEEPSCI:DEBUG-RESPONSE`
- `DEEPSCI:FUSION-PLAN`
- `DEEPSCI:PLATEAU-RESPONSE`
- `DEEPSCI:PROMPT-CONTRACT`
- `DEEPSCI:OPTIMIZATION-MEMORY-CARD`
- `DEEPSCI:FRONTIER-REVIEW`
- `DEEPSCI:OPTIMIZE-ROUTE-DECISION`
- `DEEPSCI:OPTIMIZE-BLOCKER-RECORD`

## Unmatched Skill-Route Substitutions

optimize maps to isomer-rsch-optimize. Source submodes and routes map to frontier decisions and production DeepSci experiment or decision handoffs.

Where a source route names a DeepScientist skill that has no production DeepSci target in this batch, the runtime page records the route through a semantic decision or blocker placeholder rather than pretending the missing Isomer skill exists.

## Environment Substitutions

- Source `venv`, `uv`, shell, package, Git, scheduler, and environment assumptions map to Pixi-aware Project or Topic Workspace context plus Execution Adapter Command Requests.
- Runtime pages should not require a fixed filesystem layout, virtual environment, or command path unless later storage and execution binding work adds one.
- Compatibility harness examples are allowed only as transitional `isomer-cli ext deepsci call ... --input-json <json-object>` instructions.

## Placeholder Registry

`migrate/placeholders.md` defines every placeholder used by rewritten runtime pages. Every rewritten page that mentions placeholders references that registry.

## Rewrite Targets

- `SKILL-MAIN.md`: native production DeepSci control surface with workflow steps that reference the required support pages.
- `references/operational-guidance.md`: source-preserved operational page refactored into the full optimize protocol.
- `references/brief-shaping-playbook.md`: source-preserved brief-shaping playbook refactored into guidance, preferences, constraints, and quality gates.
- `references/method-brief-template.md`: source-preserved method brief template refactored into native support and template fields.
- `references/candidate-board-template.md`: source-preserved board template refactored into native ledger support.
- `references/candidate-ranking-template.md`: source-preserved ranking template refactored into shared-surface ranking support.
- `references/frontier-review-template.md`: source-preserved frontier review template refactored into route and submode support.
- `references/optimize-checklist-template.md`: source-preserved checklist template refactored into pass-level frontier support.
- `references/optimization-memory-template.md`: source-preserved memory template refactored into reusable-lesson support.
- `references/codegen-route-playbook.md`: source-preserved codegen playbook refactored into route selection support.
- `references/debug-response-template.md`: source-preserved debug template refactored into minimal-fix support.
- `references/fusion-playbook.md`: source-preserved fusion playbook refactored into complementary-line support.
- `references/plateau-response-playbook.md`: source-preserved plateau playbook refactored into route-review and non-repeat support.
- `references/prompt-patterns.md`: source-preserved prompt patterns refactored into prompt-contract support.
- `references/frontier-management.md`, `references/candidate-brief-template.md`, `references/candidate-ranking.md`, `references/run-recording.md`, `references/plateau-and-fusion.md`: compatibility pages from the first production DeepSci draft pointing to source-preserved pages.

## Main Workflow Support Mapping

| Target Workflow Step | Source Support Material | Target Runtime Support |
| --- | --- | --- |
| Recover the frontier | `SKILL-SOURCE.md` Control workflow step 1, Working surfaces, Core object model, Operational guidance; `references/operational-guidance.md` working surfaces and frontier recovery; `references/candidate-board-template.md`; `references/optimize-checklist-template.md`; `references/frontier-review-template.md`. | `references/operational-guidance.md`, `references/candidate-board-template.md`, `references/optimize-checklist-template.md`, `references/frontier-review-template.md` |
| Choose one submode | `SKILL-SOURCE.md` Control workflow step 2, Optimize submodes, Frontier route meanings, Non-negotiable rules; `references/operational-guidance.md` submode and frontier protocols; `references/plateau-response-playbook.md`. | `references/operational-guidance.md`, `references/frontier-review-template.md`, `references/plateau-response-playbook.md` |
| Shape or rank candidates | `SKILL-SOURCE.md` Control workflow steps 3-4, Core object model, Non-negotiable rules; `references/brief-shaping-playbook.md`; `references/method-brief-template.md`; `references/candidate-ranking-template.md`; `references/prompt-patterns.md`. | `references/brief-shaping-playbook.md`, `references/method-brief-template.md`, `references/candidate-ranking-template.md`, `references/prompt-patterns.md` |
| Promote or prepare one line | `SKILL-SOURCE.md` Control workflow steps 4-5, Core object model, Working surfaces; `references/operational-guidance.md` promotion, seed, loop, execution, and codegen protocols; `references/codegen-route-playbook.md`; `references/candidate-board-template.md`. | `references/operational-guidance.md`, `references/codegen-route-playbook.md`, `references/candidate-board-template.md` |
| Handle debug, fusion, or plateau evidence | `SKILL-SOURCE.md` Control workflow steps 5-6, Frontier route meanings, Non-negotiable rules; `references/debug-response-template.md`; `references/fusion-playbook.md`; `references/plateau-response-playbook.md`; `references/frontier-review-template.md`. | `references/debug-response-template.md`, `references/fusion-playbook.md`, `references/plateau-response-playbook.md`, `references/frontier-review-template.md` |
| Record the lesson and route | `SKILL-SOURCE.md` Validation, Operational guidance, Exit criteria; `references/optimization-memory-template.md`; `references/frontier-review-template.md`; `references/operational-guidance.md`. | `references/optimization-memory-template.md`, `references/frontier-review-template.md`, `references/operational-guidance.md` |

## Semantic Match Checks

The rewritten skill must preserve these source behaviors:

- Frontier is recovered before creating or promoting candidates.
- Exactly one primary submode is selected for each meaningful pass.
- Candidate briefs remain distinct from durable lines and implementation attempts.
- Brief shaping uses differentiated mechanisms and one shared comparison surface.
- Ranking applies family and change-layer diversity plus promotion caps.
- Seed and loop work keep active implementation pools small and validation-cost-aware.
- Debug is minimal-fix only and archive is allowed.
- Fusion requires complementary strengths and bounded validation.
- Plateau triggers route review, family shift, fusion, debug, stop, or explicit non-repeat rule.
- Reusable lessons are recorded only when decision-relevant.
- Exactly one next route, blocker, experiment handoff, or stop condition is recorded.
