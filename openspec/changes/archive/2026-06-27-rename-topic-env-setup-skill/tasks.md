## 1. Rename Service Skill Bundle

- [x] 1.1 Move `skillset/service/isomer-srv-env-setup` to `skillset/service/isomer-srv-topic-env-setup`.
- [x] 1.2 Update the service skill frontmatter name, description, overview, examples, output fields, and `agents/openai.yaml` metadata to use `isomer-srv-topic-env-setup`.
- [x] 1.3 Update `skillset/service/README.md` and any service-skill discovery text to list `isomer-srv-topic-env-setup` instead of `isomer-srv-env-setup`.

## 2. Rename Service Subcommands

- [x] 2.1 Rename reference pages from `resolve-workspace`, `read-gate`, `ensure-repos`, `derive-gate`, `install-deps`, `verify-gate`, and `setup-for-topic-workspace` to `resolve-topic-workspace`, `read-env-gate`, `ensure-topic-repos`, `derive-env-gate`, `install-topic-deps`, `verify-env-gate`, and `setup-topic-env`.
- [x] 2.2 Update the service `SKILL.md` subcommand tables, default routing, invocation examples, and orchestration flow to use the new subcommand names.
- [x] 2.3 Update every service reference page so predecessor artifacts, fallback text, command examples, and cross-page links use the new subcommand names.

## 3. Enforce Topic Env Independence

- [x] 3.1 Add service guardrails stating that `team-profile/`, Topic Agent Team Profile material, Topic Team Instantiation Packets, Agent Team Instances, Agent Instances, Agent Workspace plans, roles, and agent count are not prerequisites for Topic Workspace env setup.
- [x] 3.2 Update `resolve-topic-workspace` so read-only validation or doctor diagnostics about team-profile or launch readiness are classified as non-blocking unless they also break Topic Workspace discovery, Pixi binding resolution, source gate reading, dependency setup, repo checks, or Pixi-scoped verification.
- [x] 3.3 Update gate-reading and verification text so live launch, profile materialization, runtime mutation, GUI work, and research decision authority remain out of scope while service-safe env checks still run.
- [x] 3.4 Ensure the service describes readiness through the single-agent runnable target model: one agent/operator can run the research commands inside the selected Topic Workspace.

## 4. Preserve Pixi Enclosure Behavior

- [x] 4.1 Keep the existing Pixi-first dependency ladder, including Pixi-managed installs, Pixi-mediated external runtime wiring, topic-local fallback under `.isomer-user-env/`, and blockers for sudo or machine-global mutation.
- [x] 4.2 Update enclosure references from `derive-gate`, `install-deps`, and `verify-gate` to `derive-env-gate`, `install-topic-deps`, and `verify-env-gate`.
- [x] 4.3 Verify all install and verification examples use `pixi add --manifest-path <manifest_path>`, `pixi install --manifest-path <manifest_path> --environment <pixi_environment>`, or `pixi run --manifest-path <manifest_path> --environment <pixi_environment>`.

## 5. Update Operator Delegation

- [x] 5.1 Update `skillset/operator/isomer-admin-topic-team-specialize` entrypoint text, output fields, guardrails, and `agents/openai.yaml` to delegate to `isomer-srv-topic-env-setup`.
- [x] 5.2 Update `references/setup-topic-env.md` to call `$isomer-srv-topic-env-setup setup-topic-env <research_topic_id> <auto|manual>` and to require registration, Pixi binding evidence, and a usable `env-gate.md` rather than specialization outputs.
- [x] 5.3 Update `fast-forward`, `step-by-step`, `help`, `ensure-topic-registration`, `validate-topic-team`, and `finalize-topic-team` references so Topic Workspace env setup is described as independent durable preparation and not as a team-profile prerequisite.
- [x] 5.4 Update related operator documentation, including `skillset/operator/README.md` and `isomer-admin-topic-workspace-mgr` references, so they name the new service and preserve the boundary between env setup and Git-backed Agent Workspace setup.

## 6. Update Validation and Tests

- [x] 6.1 Update `scripts/validate_skillsets.py` expectations for the renamed service bundle, reference filenames, public subcommands, and operator delegation text.
- [x] 6.2 Update unit tests that assert service skill names, command examples, subcommand sets, README entries, or validation strings.
- [x] 6.3 Add or update validation coverage that fails if `isomer-srv-topic-env-setup` requires `team-profile/` or Agent Team structure before env setup.

## 7. Verify the Change

- [x] 7.1 Run `openspec validate rename-topic-env-setup-skill --strict`.
- [x] 7.2 Run the skill-creator quick validation for `skillset/service/isomer-srv-topic-env-setup`.
- [x] 7.3 Run `pixi run validate-service-skills` or the repo-local equivalent service skill validation command.
- [x] 7.4 Run `pixi run python -m unittest tests.unit.test_validate_skillsets`.
- [x] 7.5 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test` when implementation edits are complete.
