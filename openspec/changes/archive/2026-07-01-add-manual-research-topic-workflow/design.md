## Context

The current operator skills can initialize Projects, create Research Topics, prepare Topic Workspace runtime state, set up the Topic Main Development Repository, and specialize Topic Agent Teams. The v2 research skills also have placeholder binding pages and transitional CRUD access through `isomer-cli ext research records`. The missing product path is human-orchestrated research: a user may start several manually controlled agents, such as Claude Code, Codex, Houmao-backed agents, or a mixed set, and coordinate them manually without first creating a formal Topic Agent Team Profile or Agent Team Instance.

The previous manual-topic-main framing is too narrow because it would push every manually controlled worker into `topic.repos.main`. That makes parallel work messy, blurs ownership, and prevents the same topic from mixing manually controlled agents with formal Agent Team Instance members. The better boundary is a Topic Actor layer: topic-local workers controlled by the Project Operator Session or Operator Agent, with stable names and Topic Actor Workspaces, independent from formal Agent Instance identity.

## Goals / Non-Goals

**Goals:**

- Provide a first-class operator workflow for human-orchestrated research with a default `operator` Topic Actor Workspace unless the user explicitly opts out, multiple manually controlled Topic Actors when requested through the Topic Workspace Manager, and no required formal Topic Agent Team.
- Let Topic Actors use separate Topic Actor Workspaces, defaulting to `<topic-workspace>/actors/<topic-actor-name>` and backed by worktrees in the default implementation, while keeping `topic.repos.main` as the Git anchor and integration surface.
- Allow Topic Actors to be non-Houmao sessions, Houmao-backed sessions, or a mixed set, without forcing all such workers into Agent Team Instance membership.
- Split reusable topic preparation from team-specific specialization so manual actors and formal teams share registration, runtime, topic intent, topic environment, topic-main, and research storage bootstrap logic.
- Let v2 research skills start from a Topic Actor Workspace, `topic.repos.main`, or a formal Agent Workspace by reading explicit bootstrap/readiness documents, a topic-level placeholder binding index, and skill-local `placeholder-bindings.md`.
- Keep accepted research state in Topic Workspace records via semantic labels and `isomer-cli ext research records`, while leaving Topic Actor Workspaces and Agent Workspaces as editable work surfaces.
- Preserve existing team specialization behavior as a composition over the common prep path, then team/profile/Agent Workspace steps.

**Non-Goals:**

- Do not require Topic Actor registration to create a formal Topic Agent Team Profile, Agent Team Instance, or Agent Instance.
- Do not use Topic Actors to replace formal Agent Instances when the user actually launches a managed team.
- Do not add a new storage backend or replace the transitional `ext research records` CRUD layer in this change.
- Do not make `topic.repos.main` the default shared cwd for every manually controlled worker.
- Do not make the Topic Workspace Manager the canonical creator of topic-main, topic env readiness, or research records.
- Do not support alternate source repositories for Topic Actor Workspace worktrees in the first implementation; `topic.repos.main` is the only accepted anchor.
- Do not implement formal adoption of Topic Actor-produced work into Agent Instance or Agent Team Instance identity in this change.

## Decisions

1. Introduce reusable topic preparation as an operator-level boundary.

   The implementation should add a top-level topic preparation workflow, likely as `isomer-admin-topic-prepare`, that resolves or creates the Research Topic, ensures Project Manifest registration, writes or validates `topic.intent.overview`, writes or validates `topic.intent.topic_env_requirements`, initializes or validates Workspace Runtime, delegates to `isomer-srv-topic-env-setup`, records topic-main readiness, and asks the Topic Workspace Manager to create or ensure the reserved `operator` Topic Actor Workspace unless the user explicitly opts out. Keeping this as a separate boundary avoids embedding manual actor setup into the team specialization skill. Alternative considered: keep extending `isomer-admin-topic-team-specialize`; that would preserve current flow shape but keep human-orchestrated work tied to team-only concepts.

2. Add Topic Actor bindings inside the Topic Workspace Manifest.

   A Topic Actor is a topic-local, path-safe worker identity for human-orchestrated work. Its manifest binding should include `topic_actor_name`, `actor_kind`, `runtime_kind`, `role_kind`, `controller_kind` or controller ref, `default_cwd_label`, optional `workspace_label`, optional `workspace_path`, optional `branch`, optional `adapter_ref`, and `status`. Core fields use small enumerations with `custom.*` escape hatches: `actor_kind` includes `operator`, `manual_worker`, `houmao_backed`, and `service_assisted`; `runtime_kind` includes `human_cli`, `claude_code`, `codex`, `houmao`, and `shell`; `role_kind` includes `operator`, `scout`, `coder`, `experimenter`, `analyst`, `writer`, and `reviewer`; `controller_kind` includes `project_operator_session`, `operator_agent`, `human_user`, and `houmao`; `status` includes `planned`, `ready`, `active`, `blocked`, `stale`, and `archived`. The preferred preserved name for the Project Operator control actor is `operator`, and ordinary manually controlled workers use names such as `claude-scout`, `codex-exp-a`, or `houmao-writer-a`. The Topic Workspace Manifest remains the topology and path-resolution authority; when Workspace Runtime is available, Topic Workspace Manager registration and materialization also write mutation/provenance audit records. Alternative considered: store these names only in Workspace Runtime; that would make path resolution fragile before runtime exists and would hide durable topology from the topic-owned manifest.

3. Add Topic Actor Workspace labels separate from `agent.*`.

   Topic Actor Workspaces are a third managed workspace type alongside Topic Workspace and Agent Workspace. They should use labels such as `topic.actors_root`, `topic.actors.workspace`, `topic.actors.tmp`, `topic.actors.isomer_managed`, `topic.actors.private_artifacts`, `topic.actors.logs`, and `topic.actors.links`. Under `isomer-default.v1`, `topic.actors.workspace` should resolve to `<topic-workspace>/actors/<topic-actor-name>`, and the default Git branch should be `per-topic-actor/<topic-actor-name>/main`. Formal Agent Instances keep using `agent.workspace` under `<topic-workspace>/agents/<agent-name>` and `per-agent/<agent-name>/main`. Alternative considered: reuse `agent.workspace` for manual actors; that would imply Agent Instance identity where none exists.

4. Keep `topic.repos.main` as the anchor and integration surface.

   Topic Workspace environment setup still creates and verifies `topic.repos.main` as the normal non-bare repository. Topic Actor Workspace worktrees and formal Agent Workspace worktrees attach to it, but manually controlled workers should not all share it as their cwd. The first pass rejects or defers alternate worktree source repositories instead of accepting ad hoc source policies. The operator may still use `topic.repos.main` for integration, review, and direct single-worker work. Alternative considered: create a second manual-main repository; that would split the Git anchor and duplicate source truth.

5. Put Topic Actor CRUD and workspace materialization under the Topic Workspace Manager.

   `isomer-admin-topic-workspace-mgr` should own Topic Actor CRUD and Topic Actor Workspace materialization because those operations mutate Topic Workspace topology. Its actor subcommands and guidance should back the `project topic-actors ...` CLI surface for listing, showing, registering, updating, archiving, materializing, repairing, and diagnosing Topic Actors. It should validate Topic Actor bindings, actor-scoped semantic labels, worktree branches, and runtime audit records when available. It must still route missing topic-main readiness, topic env readiness, and research record labels to their canonical workflows instead of creating substitutes. Alternative considered: keep actor CRUD inside the manual research session workflow; that would make actor management unavailable outside manual sessions and blur topology management with research orchestration.

6. Add a human-orchestrated research session workflow over prepared topics.

   Add an operator-facing workflow, likely `isomer-admin-manual-research-session`, that consumes common topic preparation, determines the requested actor topology, delegates missing Topic Actor creation or repair to `isomer-admin-topic-workspace-mgr`, runs the research workspace bootstrap over the prepared actor topology, and writes per-actor start packs. Each start pack should name the actor cwd, runtime kind, role, relevant v2 skills, placeholder binding documents, `isomer-cli ext research records` command shapes, and storage boundaries. The authoritative start pack is a Topic Workspace research record; actor-local material is a small copy or pointer for startup convenience. Alternative considered: ask users to create workspaces and record actor metadata manually; that would work for experts but would leave no stable Isomer query surface.

7. Generalize the v2 research workspace manager by topology layers rather than exclusive modes.

   Keep `isomer-rsch-workspace-mgr-v2` as the compatibility entrypoint, but make its prose and references describe a Research Workspace Bootstrap with composable layers: base topic readiness, Topic Actor readiness, and optional formal Agent Team readiness. Base readiness requires registered Topic Workspace, initialized Workspace Runtime, topic overview, topic env readiness, topic-main readiness, materialized record labels, skill-local placeholder bindings, and a topic-level binding index or readiness report that points to those skill-local files. Actor readiness adds Topic Actor bindings, Topic Actor Workspace readiness, actor cwd instructions, and actor recording metadata. Formal team readiness keeps the existing post-specialization checks for profile, summary, Agent Workspace access, and agent-visible paths.

8. Broaden `isomer-topic-summary.md` into a topic operation summary.

   `isomer-topic-summary.md` should report the active research topology. It can list registered Topic Actors, their Topic Actor Workspaces, any formal Topic Agent Team Profile or Agent Team Instance refs, storage surfaces, v2 skill bindings, blockers, and next actions. The summary should not claim that no team exists merely because a manual actor workflow ran; it should report the current state.

9. Record Topic Actor provenance without fabricating Agent Instance refs.

   A manually controlled Codex, Claude, Houmao-backed, or mixed-provider session should record provenance through `topic_actor_name`, `actor_kind`, `runtime_kind`, `producer`, controller metadata, and optional adapter refs. It must not fabricate Agent Instance, Agent Workspace, or Agent Team Instance refs. Formal adoption of Topic Actor-produced work into Agent Instance or Agent Team Instance identity is deferred to a later change; this change preserves original Topic Actor metadata and reports adoption as unsupported when requested.

10. Keep storage binding through `placeholder-bindings.md`.

   V2 skills should keep abstract placeholders in workflow prose and read per-skill `placeholder-bindings.md` for concrete record kind, profile, semantic label, and `isomer-cli ext research records` command shapes. The topic-level binding index is readiness evidence and a navigation aid, not the authority that replaces skill-local binding files. Topic Actor Workspaces should have enough workspace state and start-pack guidance so these commands work without hard-coded paths in skill bodies.

## Risks / Trade-offs

- The new Topic Actor Workspace layer adds a third managed workspace type. Mitigation: update canonical domain language directly and define Topic Actor Workspace narrowly as the managed work area for a topic-local human-orchestrated worker, not as Agent Instance identity.
- Topic Actor Workspace worktrees and Agent Workspace worktrees may look similar on disk. Mitigation: use separate roots, `actors/` and `agents/`, separate branch prefixes, `per-topic-actor/` and `per-agent/`, and separate CLI selectors.
- Existing users may expect `isomer-admin-topic-team-specialize fast-forward` to perform all setup. Mitigation: keep the full team path as a composition that calls common prep before team-specific work and preserves existing Topic Actors.
- Manual workers can produce files in Topic Actor Workspaces that look durable but have not been recorded. Mitigation: actor start packs and v2 bindings must state that accepted research artifacts are created or updated through `isomer-cli ext research records`.
- `ext research records` is transitional and generic. Mitigation: bind placeholders to stable semantic labels, profiles, and actor metadata now so future native `project records ...` commands can replace the command shape without changing skill semantics.
- Topic-level placeholder binding indexes can become stale. Mitigation: treat skill-local `placeholder-bindings.md` as authoritative and regenerate or validate the index during bootstrap.

## Migration Plan

1. Update canonical domain language, then add the common topic preparation contract with default `operator` Topic Actor Workspace creation delegated to the Topic Workspace Manager.
2. Add Topic Actor manifest schema support, actor-scoped semantic labels, path resolution, `project topic-actors ...`, and runtime audit guidance under `isomer-admin-topic-workspace-mgr`.
3. Add the human-orchestrated research session contract so it consumes prepared Topic Actors and delegates missing actor topology work to the Topic Workspace Manager.
4. Update `isomer-admin-topic-team-specialize` to call or reference common topic preparation for the reusable setup portion while retaining its team/profile/Agent Workspace steps and preserving existing Topic Actors.
5. Update `isomer-rsch-workspace-mgr-v2`, `isomer-rsch-shared-v2`, and v2 placeholder-binding guidance for Topic Actor topology and the topic-level binding index.
6. Update storage support notes, start-pack templates, and tests/validators so human-orchestrated readiness does not require team-only files, but can coexist with team files.
7. Validate a topic with the default `operator` Topic Actor Workspace, validate a topic with multiple additional Topic Actors and no formal team, then validate a topic where Topic Actors coexist with a specialized team.

## Resolved Questions

- Topic Actor Workspace is a new canonical workspace type and must be added to canonical domain language.
- Topic Actor registration lives under `project topic-actors ...` and is owned by `isomer-admin-topic-workspace-mgr`.
- Start packs are authoritative Topic Workspace research records, with actor-local copies or pointers.
- Common topic preparation creates the `operator` Topic Actor Workspace by default unless the user explicitly opts out.
- Topic Actor binding fields use small core enums with `custom.*` escape hatches.
- The Topic Workspace Manifest is the topology authority; Workspace Runtime records mutation/provenance audit events when available.
- Skill-local `placeholder-bindings.md` files are authoritative; the topic-level binding index is readiness evidence.
- Topic Actor Workspace worktrees use `topic.repos.main` as the only supported anchor in the first pass.
- Formal adoption of Topic Actor-produced work into Agent Instance or Agent Team Instance identity is deferred.
