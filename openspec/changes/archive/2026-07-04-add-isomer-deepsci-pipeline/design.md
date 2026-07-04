## Context

The Isomer Labs production DeepSci research skillset (`isomer-deepsci-*`) is intentionally factored into single-step skills: `scout`, `baseline`, `idea`, `experiment`, `analysis`, `decision`, `write`, `review`, `rebuttal`, `finalize`, and companions such as `paper-outline`, `paper-plot`, `figure-polish`, and `nature-*`. Each skill owns one research stage, reads shared semantic artifacts from the prior stage, and writes its own artifacts through the `isomer-deepsci-shared` contract.

This factoring is correct, but it pushes stage-sequencing responsibility to the user or to an external orchestrator. The proposed `isomer-deepsci-pipeline` skill fills the gap by providing named, reusable, single-pass recipes that execute a linear sequence of production DeepSci skills with automatic artifact handoffs. Looping, retrying, and macro strategy remain outside the skill; the pipeline terminates with a report that an external controller consumes to decide what to do next.

## Goals / Non-Goals

**Goals:**
- Add a new `isomer-deepsci-pipeline` production DeepSci skill that executes one named linear recipe.
- Represent each recipe as a self-contained subcommand page so pass-specific behavior can grow beyond a simple stage list.
- Preserve each wrapped skill's existing workflow, quality gates, callbacks, and blocker semantics.
- Produce a terminal report that states which stages ran, what artifacts were produced, and what the last stage recommends as the next macro action.
- Provide an initial catalog of common single-pass recipes (`empirical-pass`, `hypothesis-pass`, `paper-pass`, `revision-pass`, `rebuttal-pass`, `polish-pass`, `submission-pass`).
- Update the `research-paradigm-skills` spec to include the new skill folder in the canonical list.

**Non-Goals:**
- The pipeline skill does not implement loops, retries, or macro strategy. Those belong to the external controller.
- It does not replace or subsume any existing production DeepSci skill.
- It does not introduce new semantic-placeholder types or new storage-binding semantics beyond the control-surface objects the pipeline itself produces.
- It does not auto-install packages, manage topic workspaces, or perform operator-level topology work.

## Decisions

**1. Single-pass recipes, not loop constructs**
- *Decision*: Recipes contain no `loop_to`, `max_iterations`, or backward edges.
- *Rationale*: The user explicitly stated that looping is external control. Keeping the skill single-pass makes it deterministic, testable, and composable. An external controller can invoke `empirical-pass` followed by `paper-pass`, or invoke `empirical-pass` again if the terminal report recommends another experiment cycle.
- *Alternative considered*: Built-in iterative recipes with `loop_to`. Rejected because it would teach the agent to loop, violating the stated boundary.

**2. Self-contained subcommand pages under `commands/`**
- *Decision*: Each pass has a dedicated Markdown page under `commands/` that embeds the recipe table and any pass-specific notes.
- *Rationale*: The user noted that later passes may need customization beyond their stage lists. A dedicated page lets a pass override transition rules, entry context, cost gating, or routing without complicating the main skill entrypoint.
- *Alternative considered*: Declarative YAML files under `pipelines/`. Rejected because YAML is too rigid once a pass needs prose-level customization or conditional notes.

**3. The skill invokes existing skills, not internal logic**
- *Decision*: Each stage names a production DeepSci skill; the pipeline skill delegates to it using the same invocation surface the skill already uses.
- *Rationale*: This preserves the wrapped skill's callbacks, gates, and reference-routing discipline. The pipeline skill is pure orchestration.
- *Alternative considered*: Inline the sub-skills' steps into the pipeline. Rejected because it would duplicate logic and weaken gate discipline.

**4. Terminal report as the only output to the external controller**
- *Decision*: The pipeline ends with a `pipeline-terminal-report` that captures status, stages, artifacts, and the last stage's recommended next action.
- *Rationale*: A single, stable output shape lets an external controller decide macro flow without parsing intermediate skill-specific artifacts.
- *Alternative considered*: Emitting per-stage events. Rejected because the individual skills already produce durable artifacts; the controller only needs the aggregate terminal verdict.

**5. Pause on blocker or deviation, do not silently continue**
- *Decision*: If a stage emits a blocker or a `route_decision` that the recipe cannot satisfy, the pipeline stops and records a paused/blocked terminal report.
- *Rationale*: This preserves the safety properties of the wrapped skills. A paused pipeline can be resumed by an external controller or human after the blocker is resolved.
- *Alternative considered*: Skipping optional stages automatically. Rejected because "optional" is a controller decision, not a pipeline default.

## Risks / Trade-offs

- **[Risk] Recipe drift when wrapped skills change their artifacts.**  
  → *Mitigation*: Recipes declare consumed and produced artifact IDs that are validated against the `isomer-deepsci-shared` semantic-placeholder registry. The `commands/` pages can be reviewed when wrapped skills evolve.
- **[Risk] A pipeline hides the cumulative cost of a multi-stage run.**  
  → *Mitigation*: Each recipe marks expensive stages in its table; the skill may surface a checkpoint before such stages. The terminal report records every stage that ran so the cost is auditable.
- **[Risk] Users treat a pipeline as a black-box "make paper" button.**  
  → *Mitigation*: The skill pauses on every blocker and produces a terminal report that names the next responsible route. It never silently completes when evidence is missing.
- **[Trade-off] More files to maintain.** Adding a pass page increases the skill surface. The trade-off is accepted because each page is self-contained and easier to customize than a shared recipe engine.

## Migration Plan

1. Create `skillset/research-paradigm/deepsci/isomer-deepsci-pipeline/` with the standard skill layout (`SKILL.md`, `agents/openai.yaml`, `commands/`, `references/`, `placeholder-bindings.md`).
2. Author the initial pass subcommand pages in `commands/`.
3. Update `openspec/specs/research-paradigm-skills/spec.md` to include `isomer-deepsci-pipeline` in the list of production DeepSci skill folders.
4. Validate the new skill with `pixi run lint` and `pixi run test` if Python helpers are added.
5. No rollback needed beyond reverting the new folder and spec change; existing skills are untouched.

## Open Questions

- Should recipes support parameter substitution (e.g., `--venue=nature` expands to different stage lists), or should each variant be a separate recipe?
- Should the skill accept an explicit starting stage so a controller can resume a previously paused pipeline mid-recipe?
- Should the pipeline skill register its own durable record kind, or is the `pipeline-terminal-report` sufficient as a plain worker output?
