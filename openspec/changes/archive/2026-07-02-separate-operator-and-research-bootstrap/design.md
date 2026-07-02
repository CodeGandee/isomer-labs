## Context

The operator skillset currently contains two deprecated compatibility skills: `isomer-admin-topic-prepare` and `isomer-admin-manual-research-session`. Their useful operator-side behavior has mostly been absorbed by `isomer-admin-topic-creator` and `isomer-admin-topic-workspace-mgr`, but the compatibility text also preserved v2 research bootstrap behavior, selected v2 skill guidance, placeholder-binding references, accepted-artifact command shapes, and per-actor start packs.

That coupling creates a fuzzy boundary. Operator skills should prepare Project, Topic Workspace, Topic Actor, cwd, and topology surfaces. Research-paradigm v2 skills should prepare v2-specific research storage, placeholder binding, selected research-skill readiness, and accepted research artifact guidance. The existing `skillset/research-paradigm/v2/isomer-rsch-workspace-mgr-v2` is the right home for v2-specific bootstrap.

## Goals / Non-Goals

**Goals:**

- Retire `isomer-admin-topic-prepare` and `isomer-admin-manual-research-session` as active operator skills.
- Remove active operator-skill dependency on `isomer-rsch-workspace-mgr-v2`, v2 placeholder bindings, selected v2 research skills, and research record command shapes.
- Make `isomer-admin-topic-creator` end at v2-independent Topic Workspace readiness and Topic Actor readiness.
- Move v2-independent start-pack content into `setup-actors` as actor onboarding material.
- Keep `isomer-admin-topic-workspace-mgr` focused on topology, Topic Actor CRUD, materialization, repair, and diagnostics.
- Make `isomer-rsch-workspace-mgr-v2` explicitly own v2 research bootstrap and any v2-specific actor access plan.

**Non-Goals:**

- Do not change Isomer CLI storage, runtime, or path-resolution behavior.
- Do not remove Topic Actor support.
- Do not move Topic Actor topology management into research-paradigm skills.
- Do not make `isomer-admin-topic-workspace-mgr` create research handoff records.
- Do not require a formal Topic Agent Team for manual or human-orchestrated research preparation.

## Decisions

1. **Retire compatibility skills instead of keeping deprecated shims.**

   The two deprecated skills are already no longer the normal user-facing route. Keeping them as delegated compatibility boundaries keeps stale route names and v2 leakage alive. Removing them simplifies the operator skill inventory and forces routing through the canonical owners.

   Alternative considered: keep the skills but strip v2 content. That preserves one more compatibility path and still leaves users with multiple ways to prepare a topic. The consolidation is clearer if the folders disappear and references point to the current owners.

2. **Replace start packs with actor onboarding material in `setup-actors`.**

   The useful v2-independent content of a start pack is actor identity, cwd, branch, support labels, integration surface, boundary notes, verification evidence, and blockers. That material belongs where actors are defined and materialized. The old authoritative research record, selected v2 skills, placeholder binding files, and accepted-artifact commands do not belong in operator skills.

   Alternative considered: add a `write-start-packs` subcommand to Topic Creator. That would keep the old mental model but would invite research-specific content back into operator setup. Actor onboarding material is enough for the operator boundary.

3. **Remove `bootstrap-research` from Topic Creator's active ladder.**

   Topic Creator should finalize readiness after Project, topic, runtime, topic environment, topic main, actor definitions, actor workspaces, actor env gates, and actor onboarding material are ready or blocked. v2 research bootstrap can run afterward through `isomer-rsch-workspace-mgr-v2`.

   Alternative considered: keep a neutral `bootstrap-research` subcommand that delegates without v2 detail. The name itself implies research-paradigm preparation, so removing it from the operator ladder is cleaner.

4. **Keep Topic Workspace Manager topology-only.**

   Workspace Manager can list, register, update, materialize, repair, archive, and diagnose Topic Actors and paths. It must not create research records, v2 bootstrap outputs, or handoff artifacts.

   Alternative considered: let Workspace Manager create actor onboarding cards. That would mix topology mutation with user-facing setup output. Topic Creator can orchestrate the actor setup and summary while Workspace Manager owns the lower-level topology operations.

5. **Let v2 research workspace manager consume operator readiness.**

   `isomer-rsch-workspace-mgr-v2` should treat Topic Workspace and Topic Actor readiness as inputs. It can validate v2 placeholder binding files, selected v2 skill readiness, actor recording metadata, and accepted-artifact command guidance without requiring operator skills to know those details.

## Risks / Trade-offs

- **Existing docs still route to retired skill names** -> Add a stale-reference cleanup task covering `skillset/operator/README.md`, project manager references, topic-team specialization references, and active skill manifests.
- **Loss of per-actor "start here" convenience** -> Preserve the convenience as v2-independent actor onboarding material under `setup-actors`, with actor-local pointer/card paths where appropriate.
- **Research users may expect accepted-artifact instructions from Topic Creator output** -> Move that instruction to `isomer-rsch-workspace-mgr-v2` and keep Topic Creator output explicit that research-paradigm bootstrap is a later stage.
- **Validation may not catch cross-skill boundary drift** -> Add or update validation checks to flag active operator references to `skillset/research-paradigm/v2`, `isomer-rsch-workspace-mgr-v2`, `placeholder-bindings.md`, `<RSCH_...>` placeholders, and `isomer-cli ext research records`.
- **Formal topic-team specialization may still describe prepared-topic evidence using retired names** -> Update that text to consume Topic Creator / Topic Workspace readiness evidence instead.

## Migration Plan

1. Update OpenSpec delta specs and tasks.
2. Remove retired operator skill folders.
3. Update Topic Creator docs:
   - Remove `bootstrap-research` as a helper subcommand and ladder stage.
   - Remove selected v2 skill, placeholder binding, storage recording command, and v2 bootstrap language.
   - Expand `setup-actors` to write/report actor onboarding material.
   - Update `finalize` and summary shape to report Topic Workspace and actor readiness only.
4. Update Project Manager and Operator README routing to use actual Topic Creator subcommands: `fast-forward`, `step-by-step`, `run-to`, `status`, and `repair`.
5. Update Topic Team Specialization text to refer to reusable Topic Creator / Topic Workspace readiness evidence rather than `isomer-admin-topic-prepare`.
6. Update Topic Workspace Manager text to remove complement references to retired skills and to keep research records out of scope.
7. Update `isomer-rsch-workspace-mgr-v2` to own v2 research bootstrap and consume Topic Actor readiness as input.
8. Run focused stale-reference searches, OpenSpec validation, and repository skill validation if available.
