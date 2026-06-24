## Context

`isomer-admin-topic-team-specialize` now covers topic initialization, topic/team clarification, team specialization, environment setup, Agent Workspace setup, validation, final summary, approval, materialization, and launch language. The skill's domain definition already says Topic Team Specialization is a design-time process that ends before Agent Team Instance creation, adapter launch materialization, or live agent launch. The current workflow still lists `launch-team`, Workspace Runtime readiness, Houmao Execution Adapter launch, and Agent Team Instance creation, so agents can interpret the skill as both a static material builder and a runtime operator.

The user clarified that environment setup is still static preparation. Installed packages, environment files, setup commands, created directories, and validation records are durable topic-team setup state even when they are not declarative Markdown or TOML material. The boundary is therefore not "files only"; it is durable preparation versus live runtime operation.

## Goals / Non-Goals

**Goals:**

- Keep `isomer-admin-topic-team-specialize` focused on static Topic Team material and durable setup preparation.
- Remove `launch-team` from the local subcommand set, help table, procedural flow, fast-forward path, step-by-step path, validator expectations, and tests.
- Keep `setup-topic-env` as a static preparation step that can install packages, update environment files, run setup commands, and record validation evidence without starting live team execution.
- Keep `setup-agent-workspace` as a static preparation step that can create directories and boundary notes for expected Agent Roles without creating Agent Instances or Workspace Runtime registrations.
- Keep `approve-profile` and `materialize-profile` as explicit static profile-material boundaries because they record approval provenance and write durable Topic Agent Team Profile Bundle material.
- Reword validation and finalization around static readiness: topic overview, copied specialization material, setup evidence, Agent Workspace layout, profile material, blockers, deferrals, and next operator action.
- Update validators and tests so the absence of `references/launch-team.md` is accepted and unexpected launch/runtime pages are rejected.

**Non-Goals:**

- Do not design a replacement runtime launch skill in this change.
- Do not remove Isomer domain-language definitions for runtime concepts from local support references when they are needed to state boundaries.
- Do not make `setup-topic-env` purely declarative or prohibit package installation.
- Do not make `setup-agent-workspace` create Agent Instances, start processes, register live runtime state, or launch adapters.
- Do not archive or rewrite the already-active topic-init change as part of artifact generation; implementation may update compatible active artifacts only where they would otherwise contradict the new boundary.

## Decisions

### Treat static material as durable preparation, not files-only material

Static Topic Team material includes human-readable topic/team documents, copied template material, draft or approved profile bundle material, setup records, installed packages, environment files, created Agent Workspace directories, validation records, and final summaries. The skill should describe this explicitly so agents do not incorrectly remove `setup-topic-env`.

Alternative considered: restrict the skill to declarative artifacts only. Rejected because the user explicitly said installed packages are static material for this workflow, even though they are not declarative material.

### Remove live launch from the module skill

`launch-team` should be removed from the subcommand list, help output, required reference pages, procedural subcommands, fast-forward/step-by-step optional tail, validator constants, and unit-test fixtures. The skill can still name launch as an out-of-scope later workflow when warning users that copied material is not live team execution.

Alternative considered: keep `launch-team` as an explicit later boundary in the same skill. Rejected because the skill should focus on producing static Topic Team material, not running the team.

### Keep approval and materialization as static boundaries

`approve-profile` and `materialize-profile` stay in the skill because they produce durable review/approval provenance and durable Topic Agent Team Profile Bundle files. They should not imply live launch readiness, Workspace Runtime registration, or adapter preflight. `materialize-profile` may report Project Manifest registration guidance but should not mutate runtime state.

Alternative considered: move approval and materialization to a separate governance skill now. Rejected because approval provenance and bundle materialization are still static material production and are already part of this module's profile-material boundary.

### Reframe validation and summary around static readiness

`validate-topic-team` should validate static material completeness and durable setup evidence, not runtime readiness. `finalize-topic-team` should write `isomer-topic-summary.md` with static setup state, static Agent Workspace layout, validation status, blockers, deferrals, and next actions. It should avoid "team can start" claims that depend on live agents or adapter state.

Alternative considered: leave runtime readiness checks as optional validation inputs. Rejected because optional runtime language tends to leak into normal skill behavior and help text.

### Keep local boundary references, but prune runtime requirements

The local `runtime-and-file-boundaries.md` reference can remain if it explains what this static skill must not do. Pages such as `resolve-project`, `resolve-context`, `draft-profile`, `materialize-profile`, and `isomer-domain-language.md` should remove launch-facing requirements and keep only static refs needed for topic/team material production.

Alternative considered: delete all local runtime boundary text. Rejected because agents still need boundary guidance to avoid writing command outputs, credentials, provider state, or runtime records into static material.

## Risks / Trade-offs

- Removing `launch-team` can leave users without an obvious next command for live execution → Mitigate by making help and final summary say live launch is outside this skill and should be handled by a later runtime/operator workflow.
- Keeping `setup-topic-env` can still mutate the filesystem or environment → Mitigate by documenting it as explicit durable setup, requiring visible commands/evidence/blockers, and prohibiting live team execution or credential capture.
- Keeping `setup-agent-workspace` can be confused with Agent Instance creation → Mitigate by requiring the page to state that workspace directories and boundary notes are static preparation and do not create Agent Instances or Workspace Runtime registrations.
- Existing active change artifacts still mention `launch-team` → Mitigate during implementation by updating the active change artifacts or replacing their contradictory requirements before validation.
- Validator constants can preserve old scope accidentally → Mitigate by removing `launch-team.md` from required subcommands and adding a check that `references/launch-team.md` is unexpected for this skill.

## Migration Plan

Update the skill entrypoint and subcommand pages first, then update `scripts/validate_skillsets.py` constants and logic, then update unit-test fixtures and assertions. Remove `references/launch-team.md` after validators no longer require it. Finally, update OpenSpec artifacts that still require `launch-team` so `openspec validate` and repository validation agree.
