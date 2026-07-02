## 1. Runtime Data Model

- [ ] 1.1 Add Workspace Runtime dataclasses and status constants for reset checkpoints, reset plans, reset plan actions, and reset outcomes.
- [ ] 1.2 Extend Workspace Runtime schema creation with topic-scoped tables and indexes for reset checkpoints, reset plans, reset actions, and reset outcomes.
- [ ] 1.3 Add row serialization/deserialization helpers for the new reset records.
- [ ] 1.4 Add WorkspaceRuntimeStore methods to create, update, fetch, list, and validate reset checkpoint, plan, action, and outcome records.
- [ ] 1.5 Extend runtime validation to report stale checkpoints, missing preserved targets, cross-topic checkpoint refs, invalid plan preconditions, and forbidden Git metadata.

## 2. Structured Reset Record Formats

- [ ] 2.1 Add DeepScientist artifact-format profiles for `control/topic-reset-checkpoint/v1`, `control/topic-reset-plan/v1`, and `report/topic-reset-outcome/v1`.
- [ ] 2.2 Add JSON Schema coverage for checkpoint, plan, and outcome payloads, including explicit rejection of Git operation fields and Git command strings.
- [ ] 2.3 Add Markdown templates for checkpoint, plan, and outcome generated review views.
- [ ] 2.4 Add unit tests that resolve, validate, reject forbidden Git metadata, and render the new reset format profiles.

## 3. Reset Checkpoint and Planning APIs

- [ ] 3.1 Implement checkpoint creation APIs that capture topic refs, operator-level readiness evidence, semantic path inventory, preserved record ids, runtime high-watermarks, generated view digests, actor/operator refs, status, and diagnostics without requiring research-paradigm skill knowledge.
- [ ] 3.2 Implement checkpoint update APIs that let later preparation workflows add preserved record ids, structured payload ids, generated view refs, semantic labels, digests, actor refs, source labels, and provenance refs.
- [ ] 3.3 Implement checkpoint list/show APIs with compact summaries and optional full structured payload/rendered-body includes.
- [ ] 3.4 Implement read-only reset planning APIs that compare the selected checkpoint to current runtime records, structured payloads, generated views, readiness records, artifact format registrations, and semantic-label-derived file paths.
- [ ] 3.5 Implement plan action classification for `preserve`, `delete_record`, `delete_file`, `delete_generated_view`, `regenerate`, `skip`, and `blocked`.
- [ ] 3.6 Implement managed actor/agent workspace inventory that preserves root directories and checkpoint-preserved baseline paths while marking other post-checkpoint contents under `topic.actors.workspace` and `agent.workspace` roots for deletion.
- [ ] 3.7 Implement safety preflight blockers for unresolved labels, unsupported runtime schema, unknown managed files, possible secret material, running teams, open handoffs, live adapter records, actor or agent material outside managed workspace roots, managed-root traversal hazards, and stale checkpoint evidence.
- [ ] 3.8 Add API tests for successful checkpoint creation, checkpoint extension, unrecorded preparation classification, missing initialized topic context, read-only planning, setup-record preservation, post-checkpoint research-record classification, managed actor/agent workspace deletion planning, and blocked unsafe surfaces.

## 4. Reset Apply APIs

- [ ] 4.1 Implement reset apply precondition checks that require selected topic context, checkpoint id, plan id, explicit confirmation, unchanged checkpoint digest, unchanged plan preconditions, and no blockers.
- [ ] 4.2 Implement destructive deletion of unpreserved reset-candidate runtime rows and structured payload rows named by the approved plan.
- [ ] 4.3 Implement semantic-label-derived generated view removal/regeneration and managed actor/agent workspace file or directory deletion for only paths named by the approved plan.
- [ ] 4.4 Implement reset outcome creation for success, partial success, and failure, including applied/skipped/failed actions, diagnostics, actor ref, checkpoint ref, plan ref, timestamps, and rendered view refs.
- [ ] 4.5 Add apply tests for confirmed apply, stale plan rejection, blocker rejection, destructive record deletion, managed-root file deletion, partial failure outcome recording, and no Git operation execution.

## 5. CLI Surface

- [ ] 5.1 Add `isomer-cli project topic-reset checkpoint` with `--render markdown`, actor metadata, deterministic JSON output, and compact human output.
- [ ] 5.2 Add `isomer-cli project topic-reset update-checkpoint` for explicit preservation updates from later preparation workflows.
- [ ] 5.3 Add `isomer-cli project topic-reset list` and `show` with summary output plus optional payload, diagnostics, and rendered-body includes.
- [ ] 5.4 Add `isomer-cli project topic-reset plan` and `show-plan` with read-only behavior, action summaries, blockers, and deterministic JSON output.
- [ ] 5.5 Add `isomer-cli project topic-reset apply` requiring checkpoint id, plan id, selected topic, and explicit `--yes` confirmation.
- [ ] 5.6 Add CLI tests for command registration, checkpoint update, JSON wrapper shape, human output summaries, read-only plan behavior, confirmation requirement, stale plan rejection, and forbidden Git metadata diagnostics.

## 6. Skillset Guidance

- [ ] 6.1 Update `isomer-admin-topic-creator finalize` guidance to create or refresh the first reset checkpoint from `topic.workspace.summary` and operator-level readiness evidence.
- [ ] 6.2 Update `isomer-admin-topic-mgr` guidance and reference pages to include operator-owned reset plan, inspect, and apply workflows using structured records and Workspace Runtime state only.
- [ ] 6.3 Add or update skillset validation checks that forbid Git reset/stash guidance in reset checkpoint workflows and forbid operator reset guidance from depending on `skillset/research-paradigm` skills.
- [ ] 6.4 Update research-preparation guidance that wants reset survival to call checkpoint update APIs; leave unrecorded preparation as redo-after-reset behavior.
- [ ] 6.5 Add skill contract tests covering Topic Creator checkpoint creation, Topic Manager reset ownership, operator guidance avoiding research-paradigm routing, and research-preparation checkpoint update guidance.

## 7. Verification

- [ ] 7.1 Run `pixi run lint`.
- [ ] 7.2 Run `pixi run typecheck`.
- [ ] 7.3 Run `pixi run test`.
- [ ] 7.4 Run the repository skillset validation command.
