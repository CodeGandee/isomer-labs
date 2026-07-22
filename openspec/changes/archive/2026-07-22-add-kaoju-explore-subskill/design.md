## Context

Kaoju today routes a user prompt directly to one of ten survey intents, nine compatibility procedures, or three grouped managers. Each of those commands begins a bounded procedure that produces durable survey records. There is no lightweight, read-only phase for operators who want to think through how to perform a task before committing to a procedure.

The requested helper is an interactive planning discussion. It must keep state in memory, ask targeted questions, and only hand off to a concrete Kaoju command after the user agrees to a plan. The `imsight-project-explore` skill in the Houmao checkout provides a good questioning style (sequential and batch modes, proposed options, pros/cons, motivation/example/implication), but its file-writing contract must not be copied.

## Goals / Non-Goals

**Goals:**
- Provide a read-only planning discussion for Kaoju tasks.
- Keep the discussion in agent working memory; do not create files, artifacts, Runs, Gates, or Service Requests during exploration.
- Ask up to five clarification questions drawn from a Kaoju-specific coverage map.
- Return an agreed plan and recommended public invocation on consent.
- Support future expansion with context-specific subcommands for different Kaoju stages.

**Non-Goals:**
- Replace `isomer-ext-kaoju-welcome`, which teaches newcomers.
- Produce durable research records during exploration.
- Start another macro procedure from inside the bounded exploration discussion.
- Add new artifact bindings or semantic ids for exploration.

## Decisions

### 1. Implement `isomer-kaoju-explore` as a protected subskill with its own commands directory

The subskill pattern is already used by operator members such as `isomer-op-toolbox-mgr`. A protected subskill can own its own `commands/` directory, so `isomer-kaoju-explore` can later add stage-specific question modes (`directions`, `reading-list`, `comparison`, `trial`, `paper`, `wiki`, etc.) without expanding the entrypoint’s top-level command list.

### 2. Expose a single thin entrypoint command `explore`

`isomer-ext-kaoju-entrypoint` will gain one new public command, `explore`, backed by `commands/explore.md`. That command page resolves context, loads the subskill, receives the agreed plan, asks for final consent, and routes to the selected Kaoju command or procedure. The subskill itself does not execute the target.

### 3. Add a new `exploration_procedures` category to the Kaoju process contract

`explore` is neither a survey intent nor a compatibility procedure. Adding an `exploration_procedures` list to `survey-process.v2.json` keeps the taxonomy honest and avoids semantic confusion. `contracts.py` will expose the new list as a field on `KaojuContract`.

### 4. Route handoff through the entrypoint command page, not the subskill

The shared guardrail prohibits starting another macro procedure from inside a bounded procedure. The explore subskill is bounded and read-only; it returns a plan. The entrypoint command page, acting as the dispatcher, starts the target procedure after consent.

### 5. Adopt the questioning style from `imsight-project-explore` without its file contract

Each question presents:
- a concise motivation,
- a concrete example drawn from the current task,
- a proposed option with downstream implication,
- a short pros/cons table with 2–5 mutually exclusive options,
- an invitation to accept or override.

Sequential questioning is the default; batch mode is opt-in when the user asks for all questions at once.

### 6. No artifact-bindings.md for the explore subskill

Every other Kaoju subskill except `shared` owns artifact bindings because it produces durable artifacts. `isomer-kaoju-explore` does not, so it will not include an `artifact-bindings.md` file. This also keeps the existing test count for `artifact-bindings.md` files unchanged.

## Risks / Trade-offs

- **[Risk] The Kaoju contract hardcodes inventory counts.** Adding a protected member requires updating `contracts.py` and several unit tests. A mismatch between JSON and code breaks Kaoju loading.  
  **Mitigation**: Update `survey-process.v2.json` and `contracts.py` in the same commit, then run `pixi run test tests/unit/test_kaoju_contracts.py tests/unit/test_system_skill_assets.py tests/unit/test_kaoju_skill_assets.py`.

- **[Risk] Explore could be confused with welcome.** Both are read-only, but welcome teaches patterns while explore plans a specific task.  
  **Mitigation**: Document the distinction in both the entrypoint SKILL.md and the welcome command map. Keep `explore` out of the welcome typical-use-case list until it is stable.

- **[Risk] Inheriting the example skill’s file-writing behavior.** `imsight-project-explore` writes ADRs and design docs by default.  
  **Mitigation**: Make the no-artifact rule a top-level guardrail in `isomer-kaoju-explore/SKILL-MAIN.md` and repeat it in every subcommand page.

- **[Risk] Handoff logic duplicates routing knowledge.** The entrypoint command page must know how to map an explore plan to a public command.  
  **Mitigation**: Keep the mapping table small and explicit in `commands/explore.md`. Reuse the existing command pages rather than duplicating their workflows.

## Migration Plan

No runtime migration is needed. The change adds a new optional command and subskill. Existing Kaoju commands continue to work unchanged.

After implementation, run:
- `pixi run lint`
- `pixi run typecheck`
- `pixi run test tests/unit/test_kaoju_contracts.py tests/unit/test_kaoju_skill_assets.py tests/unit/test_system_skill_assets.py`

## Open Questions

- Should `explore` be added to `isomer-ext-kaoju-welcome` typical-use cases now, or after the subcommands mature?
- Should the subskill expose a `proceed()` subcommand for programmatic handoff, or is the entrypoint command page sufficient?
