## Context

`isomer-srv-env-setup` currently owns gate-driven Pixi setup for a Topic Workspace. Its behavior is mostly correct: it resolves the selected Topic Workspace, reads `user-intent/src/env-gate.md`, derives `user-intent/derived/isomer-env-gate.md`, installs inferred dependencies through the Topic Workspace Pixi manifest, and verifies the requested runnable target through `pixi run`.

The name and operator routing now carry the wrong implication. Topic Workspace development environment setup is not part of Agent Team structure. It does not need roles, agent count, Agent Team Instances, or a materialized Topic Agent Team Profile Bundle. It only needs enough Topic Workspace context to answer whether one agent/operator can run the commands needed to conduct the research.

The implementation must preserve the existing Pixi-first enclosure behavior while making this boundary obvious in naming, command examples, predecessor checks, and validation.

## Goals / Non-Goals

**Goals:**

- Rename the service skill bundle to `isomer-srv-topic-env-setup`.
- Rename public service subcommands to topic-env names while preserving the existing setup chain.
- Make Topic Workspace env setup independent from `team-profile/`, Topic Agent Team Profile material, Agent Team Instance records, agent roles, and agent count.
- Update operator topic-team specialization references so they delegate to the renamed service and no longer require specialization material before env setup.
- Keep setup scoped to the selected Topic Workspace Pixi environment, source gate, derived gate, required repos, and service-safe environment files.

**Non-Goals:**

- Do not change Pixi binding semantics, including explicit `topic_standalone_pixi_bindings` and implicit Topic Workspace default binding behavior.
- Do not introduce per-agent environments or Agent Workspace-specific dependency installation.
- Do not create, validate, approve, materialize, or launch Topic Agent Team Profiles or Agent Team Instances.
- Do not weaken the no-sudo, no-global-mutation enclosure policy.
- Do not change research runtime or Houmao adapter behavior.

## Decisions

### Decision: Treat this as a breaking service rename

The service bundle should move from `skillset/service/isomer-srv-env-setup` to `skillset/service/isomer-srv-topic-env-setup`, and the frontmatter name, `agents/openai.yaml`, README entry, examples, and delegation text should use the new command name.

Alternative considered: keep the old bundle name and only update descriptions. That avoids churn, but it leaves the ambiguous service identity in place. The rename is worth the migration cost because the new name encodes the Topic Workspace boundary.

### Decision: Rename subcommands to topic-env terms

Use `resolve-topic-workspace`, `read-env-gate`, `ensure-topic-repos`, `derive-env-gate`, `install-topic-deps`, `verify-env-gate`, and `setup-topic-env`.

Alternative considered: keep current subcommands and only rename the parent skill. That keeps compatibility but preserves ambiguous terms like `resolve-workspace` and `setup-for-topic-workspace`. The new names are slightly longer, but they make direct invocation clearer.

### Decision: Team-profile state is out-of-scope diagnostic context

The service must not block when `team-profile/`, Topic Agent Team Profile, Topic Team Instantiation Packet, Agent Team Instance, Agent Workspace records, roles, or role counts are absent. If a read-only project diagnostic reports those as missing, the service may mention them as unrelated diagnostics, but readiness depends only on Topic Workspace env blockers.

Alternative considered: require topic-team specialization before environment setup. That matches the old operator flow, but it prevents early setup of the actual research environment and contradicts the single-agent runnable-target model.

### Decision: Keep Project Manifest and Pixi binding as prerequisites

The service still needs a Project Manifest-backed Research Topic, a Topic Workspace, and a resolvable Topic Workspace Pixi binding. This preserves the existing path safety and prevents ad hoc environment mutation in arbitrary directories.

Alternative considered: allow a raw directory with `env-gate.md` to be set up directly. That might be useful for experimentation, but it would bypass Isomer's Topic Workspace discovery and audit model.

### Decision: Update operator delegation, not operator ownership

`isomer-admin-topic-team-specialize setup-topic-env` should continue to prepare or reuse `env-gate.md` and record service output, but it must delegate heavy setup to `isomer-srv-topic-env-setup setup-topic-env`. It may run after registration before specialization when a gate exists, or after specialization when the gate is produced by topic-team material. It must not infer dependencies or mutate Pixi directly.

Alternative considered: move env setup fully out of the topic-team operator skill. That would make the boundary pure, but the operator skill still needs to coordinate setup evidence during the static topic-team workflow. Delegation keeps the boundary and preserves workflow ergonomics.

## Risks / Trade-offs

- Renaming breaks existing prompts and docs that call `$isomer-srv-env-setup` → Update all in-repo references and validation expectations in the same change.
- Existing validation may encode old reference filenames or subcommand names → Update tests and validation scripts together with the skill bundle move.
- `project doctor --topic` may report team-profile diagnostics as failures → Either avoid using it as a hard prerequisite in the service or classify team/profile diagnostics as non-blocking for env setup.
- Operators may still mentally treat env setup as a post-specialization step → Update topic-team help, fast-forward, step-by-step, and setup-topic-env reference pages to say env setup requires registration and an env gate, not team-profile material.
- Removing the old command entirely may surprise callers outside this repo → This change is marked breaking; a compatibility alias can be considered later, but the implementation should not preserve duplicate service surfaces unless validation requires it.

## Migration Plan

1. Move the service skill directory to `skillset/service/isomer-srv-topic-env-setup`.
2. Rename service reference files to the new subcommand names.
3. Update frontmatter, examples, output labels, predecessor messages, and internal references from old command/subcommand names to new names.
4. Add explicit guardrails that team-profile and Agent Team structure are not prerequisites for env setup.
5. Update `skillset/service/README.md`, topic-team operator references, topic workspace manager references, and agent metadata that mention the old service name.
6. Update validation scripts and tests for the new service name, path, reference filenames, and delegation text.
7. Run skill validation, repo skillset validation, OpenSpec validation, and targeted tests.

Rollback is a normal git revert of the rename and reference updates. No persisted data format changes are expected.

## Open Questions

- Should a temporary compatibility shim for `$isomer-srv-env-setup` exist outside the repo-local skillset, or should the breaking rename be strict?
- Should `isomer-admin-topic-team-specialize` present `setup-topic-env` before `specialize-team` in help text, or describe it as an independent step that can run after registration whenever `env-gate.md` is available?
