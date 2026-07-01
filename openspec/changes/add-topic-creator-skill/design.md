## Context

The current operator skillset has the right internal ownership boundaries, but it exposes too many of those boundaries to a user starting from a blank state. A user who wants “make this topic ready for manual research” must discover `isomer-admin-project-mgr`, `isomer-admin-topic-prepare`, `isomer-admin-topic-workspace-mgr`, `isomer-admin-manual-research-session`, service setup skills, and `isomer-rsch-workspace-mgr-v2` in the right order.

The new `isomer-admin-topic-creator` skill should become the canonical user-facing ladder for topic initialization. Existing skills remain available so old prompts and lower-level delegated workflows keep working while the operator surface migrates.

## Goals / Non-Goals

**Goals:**

- Provide one operator skill that can plan, run, resume, and repair topic creation from empty or partial Project state to manual-research-ready Topic Workspace.
- Keep lower-level ownership intact: project lifecycle, topic environment setup, Topic Actor topology, v2 research bootstrap, start packs, and formal team specialization still have bounded owners.
- Mark `isomer-admin-topic-prepare` and `isomer-admin-manual-research-session` as deprecated for direct user invocation while retaining them as compatibility and delegation surfaces.
- Update docs, manifest, validation, and tests so users see the new skill as the happy path and advanced operators still have escape hatches.

**Non-Goals:**

- Do not remove compatibility skills in this change.
- Do not merge `isomer-admin-topic-workspace-mgr` into the creator; actor CRUD and worktree topology remain separate.
- Do not make formal Topic Team Specialization part of manual topic creation. The creator may hand off to `isomer-admin-topic-team-specialize`, but it does not adapt templates or materialize formal teams.
- Do not introduce new CLI storage APIs unless implementation discovers that existing `isomer-cli` surfaces cannot support the required orchestration.

## Decisions

1. `isomer-admin-topic-creator` is an orchestration skill, not a new authority layer.

   It owns the user-facing flow and final handoff, but delegates mutation to existing owner skills and CLI surfaces. This prevents a second implementation of Project Manifest edits, topic env setup, Topic Actor CRUD, or start-pack recording. Alternative considered: fold all topic-preparation and manual-session content into the creator immediately; that would simplify the visible skillset but would make compatibility riskier.

2. The creator uses a command-style ladder with idempotent stages.

   The public subcommands are `help`, `plan`, `create`, `ensure-project`, `define-topic`, `register-topic`, `init-runtime`, `setup-topic-env`, `setup-actors`, `bootstrap-research`, `start-manual-research`, `status`, and `repair`. `create` runs the normal happy path, `plan` is dry-run, `status` explains the current ladder position, and `repair` resumes from blockers. Alternative considered: expose only `create` and `help`; that would be easier to document but weaker for partial workspaces and debugging.

3. Compatibility skills are deprecated only for direct user invocation.

   `isomer-admin-topic-prepare` and `isomer-admin-manual-research-session` should keep their workflows and can still be called by `isomer-admin-topic-creator`, but their frontmatter should include `deprecated: true` and a `deprecation` object with `replaced_by: isomer-admin-topic-creator`. Alternative considered: delete them now; the previous inspection showed active docs, validators, and tests still reference them.

4. “Manual-research-ready” is an explicit readiness contract.

   A topic is manual-research-ready when the Project exists, the Research Topic and Topic Workspace are registered, Workspace Runtime is initialized or validated, topic intent exists, topic environment and `topic.repos.main` are ready, requested Topic Actors have `topic.actors.workspace` cwd surfaces, v2 placeholder/storage bootstrap has run or reported blockers, and per-actor start packs exist as Topic Workspace research records with actor-local pointers.

5. Project Manager becomes a router, not the topic creation guide.

   `isomer-admin-project-mgr` should continue to own Project lifecycle operations. When a user asks for blank-state topic creation or manual research setup, Project Manager should route to `isomer-admin-topic-creator` rather than expecting the user to chain `prepare-topic` and `manual-research`.

## Risks / Trade-offs

- [Risk] The new creator duplicates text from compatibility skills and the copies drift. → Mitigation: migrate guidance into creator reference pages and update compatibility skill frontmatter plus help to redirect users while preserving only delegated/internal details there.
- [Risk] A user may still invoke deprecated skills directly. → Mitigation: deprecation warnings should be visible in YAML frontmatter, descriptions, help pages, README, and validation expectations, but the skills should still return useful compatibility output.
- [Risk] `create` could become too broad and hide important mutations. → Mitigation: require `plan`-style reporting inside `create`, preserve explicit operator intent before mutation, and report each delegated owner and command boundary.
- [Risk] Topic Team Specialization and manual research setup could blur. → Mitigation: creator prepares manual research readiness and may report a next action to specialize a team, but formal template adaptation remains in `isomer-admin-topic-team-specialize`.

## Migration Plan

1. Add the `isomer-admin-topic-creator` skill bundle with command-style workflow, help page, stage reference pages, output contract, and guardrails.
2. Migrate user-facing topic initialization guidance from Project Manager, Topic Prepare, and Manual Research Session into creator references.
3. Add deprecation metadata and direct-invocation warnings to `isomer-admin-topic-prepare` and `isomer-admin-manual-research-session`.
4. Update `isomer-admin-project-mgr` routing and help so topic creation and manual-research setup point to the creator.
5. Update `skillset/operator/README.md`, `skillset/manifest.toml`, `.kimi-code/skills/` symlink installation, validation scripts, and unit tests.
6. Validate operator skills and OpenSpec artifacts. Keep compatibility skills installed until a later removal change.

## Open Questions

- Should `isomer-admin-topic-creator create` always create the default `operator` Topic Actor, or should it ask when the user explicitly requested only Project/topic registration?
- Should the creator write a new canonical topic initialization summary record, or reuse the existing operation summary/start-pack records emitted by lower-level skills?
