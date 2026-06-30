## 1. Domain Language and Documentation

- [x] 1.1 Update canonical domain language to define Topic Main Development Repository, canonical external repositories, external repository projections, projection access intent, and the breaking recreate policy for generated `isomer-content/` internals.
- [x] 1.2 Update `docs/topic-workspace-definition.md` to show `isomer-managed/topic-owned/readonly/extern/`, `isomer-managed/topic-owned/writable/extern/`, and `isomer-managed/tracked/manifests/extern-projections.toml`.
- [x] 1.3 Update `docs/concepts.md`, `docs/runtime-and-files.md`, and `docs/getting-started.md` so topic env setup owns topic-main readiness and agent env setup consumes it.
- [x] 1.4 Update `context/design/skill-process/team-specialization.md` and `skillset/callgraph.md` with the revised process order and top-level skill calls.
- [x] 1.5 Remove migration language that promises old generated Topic Workspace internals continue to work; state that generated `isomer-content/` can be recreated under the revised layout.

## 2. Semantic Surfaces and Path Resolution

- [x] 2.1 Add storage profiles for topic-main projection roots and tracked projection manifest files.
- [x] 2.2 Add built-in semantic labels for `topic.repos.main.projections.readonly`, `topic.repos.main.projections.writable`, and `topic.repos.main.projections.manifest`.
- [x] 2.3 Update Topic Workspace Manifest validation so fixed projection labels are not treated as dynamic grouped `topic.repos.*` repositories.
- [x] 2.4 Update Workspace Path Resolution previews, `paths get`, `paths explain`, and path-plan serialization to report projection labels, storage profiles, path sources, and blockers.
- [x] 2.5 Remove tests or compatibility expectations that synthesize deprecated projection paths or old generated internals.

## 3. Topic Environment Setup Service

- [x] 3.1 Revise `isomer-srv-topic-env-setup` entrypoint and subcommand references to include Topic Main Development Repository setup and external projection materialization.
- [x] 3.2 Add or update service reference pages for `ensure-topic-main-repository` and `project-extern-repos`.
- [x] 3.3 Revise `setup-topic-env` order so it resolves or validates the derived target spec before materializing topic-main, external repos, projections, Pixi dependencies, and verification.
- [x] 3.4 Ensure topic env output reports topic-main Git state, Isomer-managed namespace posture, projection metadata, commands run, changed files, blockers, and `per_agent_readiness_status: not_checked`.
- [x] 3.5 Ensure existing canonical external repos are read-only by default during `ensure-topic-repos` unless the target spec explicitly authorizes mutation.

## 4. Agent Environment Setup Service

- [x] 4.1 Revise `isomer-srv-agent-env-setup` entrypoint and subcommand list to replace mutating topic-main setup with `require-topic-main-ready`.
- [x] 4.2 Remove normal-flow topic-main creation, initialization, and configuration from agent env setup docs and reference pages.
- [x] 4.3 Update `setup-agent-env` order to require topic env readiness, topic-main readiness, authoritative Agent Names, and derived agent target spec before worktree creation.
- [x] 4.4 Update agent env verification to consume projection predecessor evidence when agent cwd commands depend on projected external repos.
- [x] 4.5 Update output contracts and validators so missing topic-main or projection evidence routes repair to `isomer-srv-topic-env-setup`.

## 5. Operator Skills

- [x] 5.1 Revise `isomer-admin-topic-team-specialize` so normal operator flow creates derived topic and agent target specs before invoking services.
- [x] 5.2 Revise `setup-topic-env`, `setup-agent-workspace`, `validate-topic-team`, `finalize-topic-team`, `fast-forward`, and `step-by-step` references for the new order.
- [x] 5.3 Re-scope `isomer-admin-topic-workspace-mgr` as optional topology inspection, branch helper, boundary summary, and legacy compatibility support rather than canonical topic-main creation.
- [x] 5.4 Update operator and service README files, skill validators, and call graph expectations for the revised ownership boundaries.

## 6. Code, Fixtures, and Tests

- [x] 6.1 Update semantic surface unit tests for projection labels, storage profiles, custom `topic.repos.main` binding behavior, and unknown `topic.repos.main.*` rejection.
- [x] 6.2 Update CLI tests for path preview/get/explain output and repository creation behavior under the revised projection contract.
- [x] 6.3 Replace generated `isomer-content/` fixtures that encode old internal paths instead of migrating them.
- [x] 6.4 Update documentation and skillset validation tests to require new terms and reject old ownership language.
- [x] 6.5 Update any runtime visibility or layout diagnostics that still assume old top-level topic-main collaboration or projection paths.

## 7. Validation

- [x] 7.1 Run `openspec validate revise-topic-main-development-repo --strict` and repair artifact issues.
- [x] 7.2 Run `openspec validate --all`.
- [x] 7.3 Run `pixi run test`.
- [x] 7.4 Run `pixi run typecheck`.
- [x] 7.5 Run `pixi run lint`.
