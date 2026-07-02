## Context

The current `isomer-admin-topic-workspace-mgr` began as a Git-backed Topic Workspace topology helper, but it now also owns Topic Actor CRUD and materialization, actor diagnostics, Agent Workspace branch planning, boundary summaries, package installation, and operator-facing diagnostics. That makes the old name too narrow and makes package/environment routing awkward because users and other skills need a topic-level manager, not a workspace-only helper.

The existing implementation and specs use flat command-style subcommands with one reference page per subcommand. The repository validation script has hard-coded expectations for the old skill name and old subcommand/page names. Recent package-install routing also points research v2 skills and topic env setup guidance to `$isomer-admin-topic-workspace-mgr install-packages`.

`isomer-admin-topic-creator` remains the user-facing initialization front door. It should create or resume a topic until the Topic Workspace is initialized, then delegate ongoing actor, storage, environment, and topic-management work to the new topic manager. `isomer-rsch-workspace-mgr-v2` remains research-paradigm-specific bootstrap and must not be merged into the operator topic manager.

## Goals / Non-Goals

**Goals:**

- Rename the canonical initialized-topic management skill to `isomer-admin-topic-mgr`.
- Define the manager as the operator surface for an already initialized Research Topic.
- Reorganize public subcommands by scope while preserving one-level reference pages.
- Add explicit environment mutation commands for package install, update, and removal through the selected Topic Workspace Pixi environment.
- Add explicit environment verification commands that can run or delegate topic, actor, and agent readiness checks without blurring service boundaries.
- Update all skill, spec, manifest, validation, and routing references that name the old workspace-manager surface.
- Provide a migration route for old invocations so existing references do not fail during the transition.

**Non-Goals:**

- Do not make the topic manager create a Research Topic from blank state; that remains `isomer-admin-topic-creator`.
- Do not merge v2 research placeholder binding, storage bootstrap, or accepted research artifact guidance into the topic manager.
- Do not make the topic manager launch Houmao agents, create Agent Instances, mutate live team runtime state, or run Execution Adapters.
- Do not replace `isomer-srv-topic-env-setup` or `isomer-srv-agent-env-setup` for full gate-driven setup.
- Do not require schema-constrained package request files for environment mutation commands.

## Decisions

### Canonical Skill Name

Use `isomer-admin-topic-mgr` as the canonical skill name and folder. The new name matches the widened scope: initialized-topic storage, actors, team topology, environment mutation, environment verification, and diagnostics.

Alternative considered: keep `isomer-admin-topic-workspace-mgr` and only add grouped sections. That would avoid a large rename, but the name would keep teaching users and skills that the manager only handles workspace topology.

### Compatibility Wrapper

Keep a temporary `skillset/operator/isomer-admin-topic-workspace-mgr` compatibility wrapper unless implementation proves no active routes need it. The wrapper should be marked deprecated for direct use, name `isomer-admin-topic-mgr` as the replacement, and map old subcommands to new ones.

Alternative considered: direct folder rename with no wrapper. That is cleaner after migration but risky because many operator, service, research v2, and OpenSpec references still point to the old skill.

### Flat Scope-Prefixed Subcommands

Use one-level subcommands with scope prefixes rather than nested commands. This preserves the current skill validation model and keeps one reference page per executable command.

Proposed public command groups:

| Scope | Commands |
| --- | --- |
| Status | `status`, `doctor`, `help` |
| Storage | `storage-resolve`, `storage-inspect-main`, `storage-validate`, `storage-register-repo` |
| Actors | `actors-manage`, `actors-materialize`, `actors-diagnose` |
| Team | `team-plan`, `team-materialize-workspaces`, `team-write-boundaries`, `team-create-branch`, `team-validate-workspaces` |
| Environment mutation | `env-install-packages`, `env-update-packages`, `env-remove-packages` |
| Environment verification | `env-verify-topic`, `env-verify-actors`, `env-verify-agents` |

Alternative considered: nested command syntax such as `env install-packages` and `team validate-workspaces`. That reads well, but it would require validator and router changes beyond this skill rename.

### Old-to-New Command Mapping

Map old commands to new commands in the compatibility wrapper and in documentation:

| Old Command | New Command |
| --- | --- |
| `topic-workspace` | `status` |
| `summarize` | `status` |
| `resolve-workspace` | `storage-resolve` |
| `ensure-main-repo` | `storage-inspect-main` |
| `manage-actors` | `actors-manage` |
| `plan-agents` | `team-plan` |
| `create-worktrees` | `team-materialize-workspaces` |
| `write-boundaries` | `team-write-boundaries` |
| `create-agent-branch` | `team-create-branch` |
| `validate-worktrees` | `team-validate-workspaces` |
| `install-packages` | `env-install-packages` |

### Environment Mutation

`env-install-packages` should keep the flexible intake behavior introduced for `install-packages`: package requests can come from plain prompts, Markdown files, structured files, requirements-style lists, or copied blocker text. The manager infers the package intent, chooses a Pixi route, mutates only the selected Topic Workspace environment, and verifies the result.

`env-update-packages` and `env-remove-packages` should share the same intake and verification pattern. Update requests should avoid broad environment upgrades unless the user explicitly asks. Removal requests should report dependency and gate risks before mutation and verify that relevant checks still pass after removal.

### Environment Verification

Use explicit verification commands so package setup, actor setup, and topology setup do not imply readiness they have not proved. `env-verify-topic` verifies the Topic Workspace gate or delegates to `isomer-srv-topic-env-setup` when full setup evidence is required. `env-verify-actors` verifies selected Topic Actor cwd gates and actor support labels. `env-verify-agents` delegates formal Agent Workspace cwd proof to `isomer-srv-agent-env-setup` and reports returned evidence.

### Boundary With Topic Creator

The creator owns initialization. The topic manager owns initialized-topic management. If the topic manager cannot resolve an initialized Research Topic and Topic Workspace through Project Manifest-backed context, it reports a blocker and routes to `isomer-admin-topic-creator`.

### Boundary With Research v2

Research v2 skills should not install packages directly, create local virtualenvs, or route through workspace-manager wording. They should route missing package or runtime setup requests to `$isomer-admin-topic-mgr env-install-packages` and keep v2 placeholder binding or storage bootstrap in `isomer-rsch-workspace-mgr-v2`.

## Risks / Trade-offs

- [Risk] Many existing references name `isomer-admin-topic-workspace-mgr` and old subcommands. → Mitigation: implement a compatibility wrapper, update references in one pass, and validate with `rg`, `pixi run validate-operator-skills`, and strict OpenSpec validation.
- [Risk] The new topic manager could become too broad and absorb creator, service, or research responsibilities. → Mitigation: state hard guardrails in the entrypoint, help page, specs, and validation terms.
- [Risk] Environment mutation commands can damage a working Pixi environment. → Mitigation: require selected topic context, plan before mutation, avoid ambient installs, use Pixi-bound commands, and verify after mutation.
- [Risk] Flat scope-prefixed commands are slightly less elegant than nested commands. → Mitigation: keep them now for validator compatibility and leave nested command parsing for a future CLI/router change.

## Migration Plan

1. Create `skillset/operator/isomer-admin-topic-mgr/` with updated frontmatter, agent metadata, grouped command router, output contract, guardrails, and renamed reference pages.
2. Convert old reference pages into new scoped pages, preserving current behavior while updating command names and scope language.
3. Add new environment update, remove, and verification pages.
4. Replace direct references in operator skills, service skills, research v2 skills, README material, manifest entries, and validation constants.
5. Keep `skillset/operator/isomer-admin-topic-workspace-mgr/` as a deprecated compatibility wrapper that maps old commands to new commands.
6. Update OpenSpec specs and validation expectations.
7. Run repository skillset validation and strict OpenSpec validation.

## Open Questions

- Should the compatibility wrapper remain for one release-like archive cycle, or should implementation remove it once all in-repo references migrate?
- Should `doctor` be a public command in the first implementation, or should `status` cover diagnostics until a later split?
