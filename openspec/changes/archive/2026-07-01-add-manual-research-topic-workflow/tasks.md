## 1. Operator Workflow Boundaries

- [x] 1.1 Update canonical domain language so Topic Actor Workspace is a third managed workspace type alongside Topic Workspace and Agent Workspace.
- [x] 1.2 Add a reusable topic preparation operator skill or reference set that resolves or creates the Research Topic, ensures Topic Workspace registration, validates Workspace Runtime, delegates topic environment setup, reports `topic.repos.main` readiness as the Git anchor, and delegates reserved `operator` Topic Actor Workspace creation to the Topic Workspace Manager by default unless the user explicitly opts out.
- [x] 1.3 Add a human-orchestrated research session operator skill or entrypoint that consumes prepared-topic evidence, delegates missing Topic Actor or Topic Actor Workspace work to the Topic Workspace Manager, runs research workspace bootstrap over the selected topology, and writes authoritative per-actor start-pack records plus actor-local copies or pointers.
- [x] 1.4 Update `isomer-admin-project-mgr` help and routing so manual or human-orchestrated research preparation hands off to common topic preparation, Topic Workspace Manager actor management, and human-orchestrated research session work while Topic Agent Team specialization remains explicit.
- [x] 1.5 Update `skillset/operator/README.md` to distinguish common topic preparation, human-orchestrated Topic Actor research, and Topic Agent Team specialization.

## 2. Topic Actor Manifest and Workspace Manager

- [x] 2.1 Add Topic Actor bindings to Topic Workspace Manifest parsing, validation, rendering, and JSON output, including core enum validation with `custom.*` escape hatches.
- [x] 2.2 Add default actor-scoped semantic labels such as `topic.actors_root`, `topic.actors.workspace`, `topic.actors.tmp`, `topic.actors.isomer_managed`, `topic.actors.private_artifacts`, `topic.actors.logs`, and `topic.actors.links`.
- [x] 2.3 Add path resolution support for Topic Actor context from explicit selector, environment, cwd, lifecycle refs, or manifest binding.
- [x] 2.4 Add `project topic-actors ...` CLI surfaces backed by `isomer-admin-topic-workspace-mgr` for listing, showing, registering, updating, archiving, materializing, repairing, and diagnosing Topic Actors and Topic Actor Workspaces.
- [x] 2.5 Add branch and worktree guidance for Topic Actor Workspaces using `per-topic-actor/<topic-actor-name>/main` from `topic.repos.main`, and reject or defer alternate source repositories in this change.
- [x] 2.6 Add `isomer-admin-topic-workspace-mgr` actor-management workflow guidance for Topic Actor CRUD, Topic Actor Workspace materialization/repair, actor-scoped path diagnostics, topology summaries, and canonical repair routing.
- [x] 2.7 Add Workspace Runtime mutation/provenance audit records for Topic Actor registration and materialization when runtime is available, without making runtime the topology authority.

## 3. Team Specialization Refactor

- [x] 3.1 Update `isomer-admin-topic-team-specialize` so its full flow delegates reusable topic preparation before team-specific steps when prepared-topic evidence is missing.
- [x] 3.2 Update team specialization subcommands, dependency manifests, and recovery guidance so prepared-topic evidence can satisfy common prerequisites without requiring or deleting Topic Actor bindings or Topic Actor Workspaces.
- [x] 3.3 Update `finalize-topic-team` output so `isomer-topic-summary.md` records reused common preparation refs, current Topic Actor roster, Topic Actor Workspace refs, team/profile/Agent Workspace readiness, and coexistence boundaries.

## 4. Research Workspace Bootstrap

- [x] 4.1 Update `isomer-rsch-workspace-mgr-v2` to describe and validate base topic readiness, Topic Actor readiness, and optional formal team readiness as composable topology layers.
- [x] 4.2 Update `isomer-rsch-shared-v2` and relevant v2 skill references so post-preparation questions route to the bootstrap layer matching the current cwd and selected actor or agent context.
- [x] 4.3 Ensure v2 skills keep placeholders in `SKILL.md` prose and use skill-local `placeholder-bindings.md` for Topic Actor and formal agent `isomer-cli ext research records` command guidance.
- [x] 4.4 Add or validate a topic-level placeholder binding index/readiness report that points to skill-local `placeholder-bindings.md` files without replacing them as the authority.
- [x] 4.5 Update research storage planning notes to describe Topic Actor readiness, actor start-pack contents, Topic Actor Workspace storage boundaries, and accepted-artifact storage boundaries.

## 5. Storage and Recording Contracts

- [x] 5.1 Update research record extension guidance or implementation so Topic Actor metadata is accepted without Agent Team Instance, Agent Instance, or Agent Workspace refs, and formal adoption of Topic Actor work is reported as out of scope.
- [x] 5.2 Update Topic Main Development Repository guidance so `topic.repos.main` is the only first-pass Git anchor and integration surface for Topic Actor Workspace worktrees rather than the universal manual coding-agent cwd.
- [x] 5.3 Add or update output templates for topic operation summaries and actor start packs, including actor cwd, runtime kind, v2 skills, placeholder bindings, semantic labels, blockers, next actions, authoritative record refs, and actor-local copy or pointer paths.

## 6. Validation

- [x] 6.1 Add or update tests and static validators showing human-orchestrated research preparation creates the default `operator` Topic Actor Workspace unless explicitly opted out.
- [x] 6.2 Add or update tests and static validators showing human-orchestrated research preparation succeeds with multiple Topic Actors and no team-profile, formal Agent Workspace, or Houmao launch artifacts.
- [x] 6.3 Add or update tests and static validators showing human-orchestrated Topic Actors can include Houmao-backed and non-Houmao workers without requiring Agent Team Instance membership.
- [x] 6.4 Add or update tests and static validators showing team specialization still succeeds by composing common topic preparation with team/profile/Agent Workspace steps while preserving Topic Actor bindings and Topic Actor Workspace refs.
- [x] 6.5 Validate the OpenSpec change with the repository OpenSpec validation command.
- [x] 6.6 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test` after implementation changes.
