## 1. Fixture Project Material

- [x] 1.1 Create `tests/fixtures/projects/deepsci-profile-use-cases/` with a Project Manifest, two Research Topics, two Topic Workspaces, and registered UC-01, UC-02, UC-03, and UC-05 Topic Agent Team Profile files.
- [x] 1.2 Add UC-01 profile fixture values for exploring a new research direction, including scout/framer, analyzer, reviewer, follow-up inquiry Gate policy, expected Artifacts, and topic-scoped Agent Workspace refs.
- [x] 1.3 Add UC-02 profile fixture values for baseline reproduction and optimization, including Measurable Objective refs, baseline acceptance or waiver policy refs, experimenter/analyzer bindings, and expected metric Artifacts.
- [x] 1.4 Add UC-03 profile fixture values for paper revision planning, including feedback mapping, claim-risk, writer, reviewer, targeted-analysis, and final approval Gate refs.
- [x] 1.5 Add UC-05 profile fixture values for mixed manual and automatic Runs, including manual-mode defaults, automatic-mode opt-in refs, Completion Watcher Contract refs, Service Request policy refs, and handoff constraints as declarative refs.
- [x] 1.6 Ensure positive fixture files contain no Workspace Runtime state, Run status, Agent Team Instance ids, mailbox state, gateway state, live Houmao managed-agent ids, command outputs, rich research records, or secret-like fields.

## 2. Template Fixture Material

- [x] 2.1 Create a minimal project-local Domain Agent Team Template fixture package with manifest, participants, bindings, workspace contract, state contract, run contract, harness schema, generated skill path, role profile path, and notifier prompt path.
- [x] 2.2 Create a missing-artifact template fixture or temporary fixture builder that references a missing required template artifact.
- [x] 2.3 Create a template-boundary negative fixture or temporary fixture builder with concrete topic/runtime/launch truth where only placeholders are allowed.
- [x] 2.4 Document fixture intent in concise README files where the fixture layout would otherwise be opaque.

## 3. Template Validation Hardening

- [x] 3.1 Ensure custom project-local templates validate through generic structural rules without requiring `deepsci-org` role ids.
- [x] 3.2 Keep the seven-role `deepsci-org` expectation scoped to the built-in `deepsci-org` template id and source.
- [x] 3.3 Ensure missing manifest, participant contract, binding path, generated skill, harness schema, workspace contract, state contract, and run contract failures report deterministic Isomer diagnostics.
- [x] 3.4 Ensure concrete Research Topic, Topic Workspace, Topic Agent Team Profile, Agent Team Instance, mailbox, gateway, credential, launch, Run, and command-output truth in template material reports template-boundary diagnostics.
- [x] 3.5 Add CLI coverage for `team-templates list`, `team-templates inspect`, and `team-templates validate` against both built-in `deepsci-org` and the project-local fixture template.

## 4. Profile Validation and Write Semantics

- [x] 4.1 Add deterministic `registration_suggestion` structured guidance to `team-profiles specialize --write` JSON output without mutating Project Manifest or Research Topic Config files, and add concise text-mode registration guidance.
- [x] 4.2 Ensure `team-profiles specialize` without `--write` remains side-effect free and reports `written_path` as null.
- [x] 4.3 Ensure `team-profiles specialize --write` writes only the profile TOML file under the Project Config Directory.
- [x] 4.4 Validate duplicate Topic Agent Team Profile ids so duplicates fail regardless of registration status; leave topic lineage, archive, fork, and migration relationships to a future relationship/history surface.
- [x] 4.5 Validate missing required role bindings, inactive required roles, missing required skills, missing fanout policy for scalable roles, automatic mode without an automatic policy ref, and reviewer activation without reviewer read-access policy.
- [x] 4.6 Reject Houmao launch dossiers, mailbox state, gateway state, live managed-agent ids, Agent Team Instance ids, adapter launch facts, command outputs, rich research records, and secret-like fields from profile files.
- [x] 4.7 Validate cross-topic Topic Workspace refs, cross-topic Agent Workspace refs, cross-topic expected Artifact refs, and topic-local policy ref leakage where those refs encode another Research Topic.

## 5. Fixture-Based Tests

- [x] 5.1 Refactor positive profile tests to load the repo fixture Project rather than constructing every profile TOML string inline.
- [x] 5.2 Add tests that run `isomer-cli validate --json` against the positive fixture Project and assert deterministic success.
- [x] 5.3 Add tests that run `team-profiles validate` against each UC-01, UC-02, UC-03, and UC-05 fixture profile file.
- [x] 5.4 Add tests for `team-profiles specialize` preview and `team-profiles specialize --write` output shape, written path, and no implicit manifest mutation.
- [x] 5.5 Add tests for duplicate profile rejection across active and archived registrations.
- [x] 5.6 Add tests for template custom fixture success, missing-artifact fixture failure, and template-boundary fixture failure.
- [x] 5.7 Keep focused temporary-project tests for runtime truth, secret-like fields, and cross-topic leakage cases that are clearer as small inline fixtures.

## 6. Documentation and Roadmap

- [x] 6.1 Update README or developer notes to describe fixture Project expectations under `tests/fixtures/projects/`, `team-templates`, `team-profiles`, profile write semantics, and the no-launch boundary.
- [x] 6.2 Update CLAUDE.md or repository agent notes if command examples or contributor expectations change.
- [x] 6.3 Mark ROADMAP Milestone 2 checklist items complete only after template fixture, CLI, and validation tests pass.
- [x] 6.4 Mark ROADMAP Milestone 3 checklist items complete only after use-case fixture, profile specialization, negative validation, and CLI tests pass.
- [x] 6.5 Leave Milestone 4 and Houmao launch roadmap items incomplete.

## 7. Validation

- [x] 7.1 Run `openspec validate --all`.
- [x] 7.2 Run `pixi run lint`.
- [x] 7.3 Run `pixi run typecheck`.
- [x] 7.4 Run `pixi run test`.
- [x] 7.5 Run `pixi run validate-research-skills`.
- [x] 7.6 Confirm `openspec status --change "complete-milestone-2-3-template-profile-implementation" --json` reports all apply-required artifacts complete before implementation starts.
