## 1. Topic Manager Skill Bundle

- [x] 1.1 Create `skillset/operator/isomer-admin-topic-mgr/` with `SKILL.md`, `agents/openai.yaml`, and reference pages using `isomer-admin-topic-mgr` metadata.
- [x] 1.2 Rewrite the entrypoint around initialized-topic management and the grouped subcommand sections for status, storage, actors, team, environment mutation, and environment verification.
- [x] 1.3 Rename old reference pages into scoped pages: `topic-workspace` and `summarize` to `status`, `resolve-workspace` to `storage-resolve`, `ensure-main-repo` to `storage-inspect-main`, `manage-actors` to `actors-manage`, `plan-agents` to `team-plan`, `create-worktrees` to `team-materialize-workspaces`, `write-boundaries` to `team-write-boundaries`, `create-agent-branch` to `team-create-branch`, `validate-worktrees` to `team-validate-workspaces`, and `install-packages` to `env-install-packages`.
- [x] 1.4 Add new `doctor`, `storage-validate`, `storage-register-repo`, `actors-materialize`, `actors-diagnose`, `env-update-packages`, `env-remove-packages`, `env-verify-topic`, `env-verify-actors`, and `env-verify-agents` reference pages.
- [x] 1.5 Preserve current semantic path, Topic Actor, Git topology, package install, output-contract, and guardrail behavior while updating names and scope language.
- [x] 1.6 Add initialized-topic guardrails that route missing or uninitialized topic context to `isomer-admin-topic-creator`.

## 2. Compatibility Wrapper

- [x] 2.1 Convert `skillset/operator/isomer-admin-topic-workspace-mgr/` into a deprecated compatibility wrapper or remove it only if validation proves no active route depends on it.
- [x] 2.2 Add wrapper mappings from old commands to new `isomer-admin-topic-mgr` commands.
- [x] 2.3 Ensure wrapper output names the replacement command and defers canonical behavior, guardrails, and output contracts to the new topic manager.
- [x] 2.4 Update `skillset/manifest.toml` so `isomer-admin-topic-mgr` is active and the old wrapper is represented consistently with repository skillset conventions.

## 3. Routing and Documentation Updates

- [x] 3.1 Update `skillset/operator/README.md` to list `isomer-admin-topic-mgr` as the initialized-topic manager and describe the old workspace manager only as compatibility when retained.
- [x] 3.2 Update `isomer-admin-topic-creator` entrypoint, help, setup-actors, finalize, status, and repair guidance to delegate post-initialization actor, storage, environment, and validation work to `isomer-admin-topic-mgr`.
- [x] 3.3 Update `isomer-admin-project-mgr` guidance so initialized-topic storage, actor, team topology, package, and verification handoffs point to `isomer-admin-topic-mgr`.
- [x] 3.4 Update `isomer-admin-topic-team-specialize` guidance so optional topology inspection, branch helpers, boundary summaries, stale topology repair, and diagnostics route to `isomer-admin-topic-mgr` storage or team commands.
- [x] 3.5 Update `isomer-srv-topic-env-setup` guidance so ad hoc package install, update, remove, and package verification requests route to `isomer-admin-topic-mgr env-*` commands while full gate-driven setup remains service-owned.
- [x] 3.6 Update `isomer-srv-agent-env-setup` help and related references to name `isomer-admin-topic-mgr` for optional topology inspection and branch-helper support.
- [x] 3.7 Update `skillset/research-paradigm/v2/*` missing-package and setup-blocker guidance to route to `$isomer-admin-topic-mgr env-install-packages` or the relevant `env-*` command without direct package installation or local virtualenv setup.
- [x] 3.8 Replace stale in-repo references to `isomer-admin-topic-workspace-mgr` and old subcommand names, except where the compatibility wrapper intentionally documents them.

## 4. Validation and OpenSpec Alignment

- [x] 4.1 Update `scripts/validate_skillsets.py` constants, allowlists, required reference pages, required wording checks, and deprecated-wrapper checks for `isomer-admin-topic-mgr`.
- [x] 4.2 Add or update validation coverage for grouped topic-manager commands, environment mutation commands, environment verification commands, initialized-topic guardrails, and old-command compatibility mappings.
- [x] 4.3 Ensure the new `topic-manager-skill` spec and old `topic-workspace-manager-skill` wrapper delta remain consistent with implemented files.
- [x] 4.4 Search the repository for stale active references to old routes and either update them or mark them as intentional compatibility references.

## 5. Verification

- [x] 5.1 Run `openspec validate rename-topic-workspace-mgr-to-topic-mgr --strict`.
- [x] 5.2 Run `pixi run validate-operator-skills`.
- [x] 5.3 Run `pixi run lint`.
- [x] 5.4 Run `pixi run test`.
- [x] 5.5 Report changed paths, validation results, remaining compatibility references, and any blockers.
