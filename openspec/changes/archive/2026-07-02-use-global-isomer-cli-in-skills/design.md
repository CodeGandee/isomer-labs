## Context

Skills under `skillset/operator`, `skillset/service`, `skillset/misc`, and `skillset/research-paradigm` are intended to be installed into agents that work in Projects, Topic Workspaces, Topic Actor Workspaces, or Agent Workspaces outside the `isomer-labs` repository. Those agents should not assume this repository exists as their cwd and should not call `isomer-cli` through `pixi run`.

`skillset/dev` is different. Dev skills operate on this repository and may continue to use Pixi for validation, migration, generation, and local code maintenance.

## Goals / Non-Goals

**Goals:**

- Make non-dev skill command examples call `isomer-cli` directly.
- Keep `skillset/dev/**` exempt from this rule.
- Update placeholder-binding command rows so Topic Actors and research agents can copy direct `isomer-cli ext research records ...` commands.
- Add validation so future non-dev skills do not reintroduce `pixi run isomer-cli`.

**Non-Goals:**

- Do not change Python CLI implementation or packaging.
- Do not rewrite repository developer docs that intentionally teach `pixi run ...` for this repo.
- Do not forbid all Pixi commands in non-dev skills; topic environment skills may still describe Topic Workspace Pixi environment commands when those commands are the user's research environment. The forbidden pattern is invoking Isomer's own CLI as `pixi run isomer-cli`.

## Decisions

1. Enforce by path scope.

   The rule applies to `skillset/**` except `skillset/dev/**`. This keeps the user-facing installed skills clean while preserving repo-local developer workflows. Alternative considered: ban `pixi run isomer-cli` globally. That would wrongly affect tests, scripts, docs, and dev skills that run inside this repository.

2. Preserve command semantics and remove only the Pixi prefix.

   `pixi run isomer-cli --print-json project validate` becomes `isomer-cli --print-json project validate`; `pixi run isomer-cli ext research records create ...` becomes `isomer-cli ext research records create ...`. This keeps CLI namespace, flags, and examples stable.

3. Validate the convention.

   Add a validation check that scans non-dev skill files and reports `pixi run isomer-cli` as an error. Existing validators should still validate canonical command namespaces such as `isomer-cli project ...` and `isomer-cli ext research records ...`.

## Risks / Trade-offs

- [Risk] Some examples may mention Pixi for Topic Workspace environment setup and get over-edited. → Mitigation: replace only Isomer CLI invocation prefixes, not legitimate Topic Workspace Pixi environment commands.
- [Risk] Generated v2 placeholder binding files have many repeated commands. → Mitigation: use a mechanical replacement for the exact prefix and validate afterward.
- [Risk] External agents may not have `isomer-cli` installed. → Mitigation: skills should report missing `isomer-cli` as an environment blocker; packaging as a global `uv` tool is assumed by this contract.

## Migration Plan

1. Replace `pixi run isomer-cli` with `isomer-cli` in all non-dev skill files.
2. Keep `skillset/dev/**` unchanged.
3. Add validator coverage for the forbidden non-dev command prefix.
4. Update tests that use expected command strings or fixtures.
5. Run skillset validation and targeted tests.
