## 1. Service Skill Bundle

- [x] 1.1 Create `skillset/service/isomer-srv-agent-env-setup/` with `SKILL.md`, `agents/openai.yaml`, and a `references/` directory.
- [x] 1.2 Write the entrypoint as a lean command-style router with grouped Procedural, Helper, and Misc subcommand tables.
- [x] 1.3 Add public subcommands `resolve-agent-env-context`, `require-topic-env-ready`, `read-agent-env-gate`, `plan-agent-workspaces`, `derive-agent-env-gate`, `ensure-topic-main-repository`, `create-agent-worktrees`, `verify-agent-env-gate`, `setup-agent-env`, and `help`.
- [x] 1.4 Define the parent output contract with topic env status, semantic paths, requester, confirmation source, optional Service Request or Provenance refs, source agent env gate path, derived agent env gate path, Topic Main Repository, agent workspace paths, branch plan, worktree status by agent, readiness by agent, overall readiness, changed files, commands run, blockers, and next action.
- [x] 1.5 Add guardrails forbidding per-agent Pixi environments, dependency mutation by default, Agent Instance creation, Workspace Runtime mutation, Houmao launch, Execution Adapter launch, destructive Git repair, directory-scan agent selection, and research decision authority.

## 2. Context and Topic Env Preconditions

- [x] 2.1 Implement `references/resolve-agent-env-context.md` to resolve Project, Research Topic, Topic Workspace, Topic Workspace Pixi binding, and topic semantic labels through Project Manifest-backed context.
- [x] 2.2 Ensure `resolve-agent-env-context` reports `topic.main_repo`, `topic.main_repo.isomer_managed`, `topic.agents_root`, `topic.records`, `topic.runtime`, path sources, diagnostics, and blockers.
- [x] 2.3 Implement `references/require-topic-env-ready.md` to require resolved Pixi manifest, selected Pixi environment, `pixi.lock`, `.pixi/`, and `user-intent/derived/isomer-env-gate.md`.
- [x] 2.4 Route missing or stale Topic Workspace dependency readiness back to `isomer-srv-topic-env-setup` instead of mutating dependencies in the agent env service.
- [x] 2.5 Record topic env predecessor evidence in service outputs without claiming per-agent cwd readiness from topic-root verification.
- [x] 2.6 Implement `references/read-agent-env-gate.md` to require `user-intent/src/agent-env-gate.md` and extract required commands, expected results, success criteria, Topic Main Repository configuration requirements, agent plan constraints, cwd assumptions, and blockers.
- [x] 2.7 Record direct Project Operator Session invocation, mutation confirmation, and optional Service Request, support Artifact, or Provenance refs without requiring Workspace Runtime records.

## 3. Agent Planning and Git Topology

- [x] 3.1 Implement `references/plan-agent-workspaces.md` to read authoritative Agent Names from active role bindings in the Topic Team Instantiation Packet or Topic Agent Team Profile material derived from that packet, treating explicit operator-provided maps only as corroborating evidence when they match.
- [x] 3.2 Validate Agent Names for path safety, reject normalized collisions, and refuse to select agents by scanning existing directories.
- [x] 3.3 Resolve `agent.workspace`, `agent.isomer_managed`, `agent.runtime`, `agent.private_artifacts`, `agent.scratch`, `agent.logs`, `agent.public_share`, `agent.inbox`, `agent.topic_readonly`, `agent.topic_writable`, and `agent.links` for each planned Agent Name.
- [x] 3.4 Implement `references/ensure-topic-main-repository.md` to create or reuse one normal non-bare Topic Main Repository resolved by `topic.main_repo` with owner branch `topic-owner/main`, including initialization and a minimal baseline commit for missing or empty safe targets, then apply non-destructive Topic Main Repository configuration required by `user-intent/derived/isomer-agent-env-gate.md`.
- [x] 3.5 Implement `references/create-agent-worktrees.md` to create or validate each `agent.workspace` as a worktree of `topic.main_repo` on `per-agent/<agent-name>/main`.
- [x] 3.6 Add blockers for existing nonmatching paths, bare or corrupt repos, ambiguous existing history state, missing base branches, duplicate branch checkout, unsafe branch names, and unsafe custom semantic bindings.
- [x] 3.7 Prepare or validate required agent support paths and boundary material, including cwd-friendly self-query guidance and peer-read sharing boundaries.

## 4. Agent Env Gate and Verification

- [x] 4.1 Implement `references/derive-agent-env-gate.md` to translate `user-intent/src/agent-env-gate.md` into `user-intent/derived/isomer-agent-env-gate.md` using topic env predecessor evidence and agent plan evidence.
- [x] 4.2 Include fixed sections `Source Agent Gate`, `Topic Env Gate`, `Topic Pixi Binding`, `Topic Main Repository Configuration`, `Agent Plan`, `Semantic Paths`, `Worktree Plan`, `Verification Matrix`, `Expected Results`, `Blockers`, and `Execution Log`.
- [x] 4.3 Derive per-agent verification commands from the source agent env gate that run through `pixi run --manifest-path <manifest_path> --environment <pixi_environment> ...` with cwd set to each resolved `agent.workspace`.
- [x] 4.4 Preserve topic env gate cwd assumptions so agent-cwd-incompatible commands become blockers rather than false readiness.
- [x] 4.5 Implement `references/verify-agent-env-gate.md` to run or report the per-agent verification matrix, allow selected-agent reruns only for authoritative Agent Names, label selected-agent results as partial evidence, and update the gate execution log.
- [x] 4.6 Verify cwd-friendly agent-scoped semantic path queries from inside each Agent Workspace without passing Agent Name.
- [x] 4.7 Report readiness by agent and overall readiness, using `ready` only when every planned agent has a valid worktree, support paths, path evidence, and every required agent-env-gate command passes from that agent's cwd.
- [x] 4.8 Treat `topic.main_repo.tmp` and `agent.tmp` as local ignored disposable surfaces when available and never as durable readiness evidence.

## 5. Full Flow and Operator Integration

- [x] 5.1 Implement `references/setup-agent-env.md` to orchestrate the full all-agent flow in order: resolve context, require topic env readiness, read source agent env gate, plan agents, derive agent env gate, ensure and configure the Topic Main Repository, create worktrees, then verify the derived agent env gate from every authoritative Agent Workspace cwd.
- [x] 5.2 Implement `references/help.md` with public subcommand usage, output fields, service boundaries, and examples.
- [x] 5.3 Update `skillset/service/README.md` to list `isomer-srv-agent-env-setup`.
- [x] 5.4 Update `isomer-admin-topic-workspace-mgr` entrypoint and references to route per-agent env readiness requests to `isomer-srv-agent-env-setup` while preserving Git-only topology flows.
- [x] 5.5 Update `isomer-admin-topic-team-specialize` `setup-agent-workspace`, `validate-topic-team`, and `finalize-topic-team` references to consume agent env service evidence.
- [x] 5.6 Update `isomer-srv-topic-env-setup` guidance to clarify that topic env setup remains topic-scoped and downstream agent-cwd verification belongs to `isomer-srv-agent-env-setup`.

## 6. Validation and Tests

- [x] 6.1 Extend repo skillset validation to require the new service bundle, UI metadata, subcommands, reference pages, semantic label terms, topic env predecessor terms, per-agent cwd verification terms, and runtime-boundary guardrails.
- [x] 6.2 Add or update unit tests in `tests/unit/test_validate_skillsets.py` for valid and invalid `isomer-srv-agent-env-setup` fixtures.
- [x] 6.3 Add validation coverage that fails when `user-intent/src/agent-env-gate.md`, `isomer-agent-env-gate.md`, `topic.main_repo`, `agent.workspace`, `pixi run --manifest-path`, per-agent cwd verification, or no-runtime-mutation boundaries are missing.
- [x] 6.4 Run `pixi run validate-skills` or the repo-local skill validation task and fix reported issues.
- [x] 6.5 Run `pixi run docs-validate` and fix documentation or skill reference issues.
- [x] 6.6 Run `pixi run test` and focused unit tests for skillset validation.
- [x] 6.7 Run `openspec validate add-agent-env-setup-service-skill --strict` and confirm the change remains valid.
