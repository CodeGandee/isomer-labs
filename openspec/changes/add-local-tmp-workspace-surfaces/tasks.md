## 1. Documentation and Domain Language

- [ ] 1.1 Update the canonical domain language to define `topic.tmp`, `topic.main_repo.tmp`, and `agent.tmp` as local disposable semantic labels and distinguish them from `agent.scratch`.
- [ ] 1.2 Update Topic Workspace documentation to show the tmp labels and their `isomer-default.v1` bindings in the standard layout and directory meanings.
- [ ] 1.3 Update system and runtime docs that describe worker visibility, sharing, evidence, or promotion boundaries so `tmp/` is never presented as shared or durable.
- [ ] 1.4 Extend documentation validation when useful so stale wording that treats `tmp/` as shared, durable, or evidence-ready is reported.

## 2. Path Resolution and Runtime Layout

- [ ] 2.1 Add Workspace Path Resolution support for `topic.tmp`, `topic.main_repo.tmp`, and `agent.tmp`.
- [ ] 2.2 Ensure Workspace Runtime initialization prepares or validates resolved `topic.tmp` and the owning Topic Workspace root ignore rule.
- [ ] 2.3 Ensure Topic Main Repository and Agent Workspace preparation creates or validates resolved `topic.main_repo.tmp` and `agent.tmp`, plus the owning Topic Main Repository ignore rule.
- [ ] 2.4 Keep `tmp/` out of durable runtime dependency semantics: path preview may report it, but runtime records, handoffs, evidence, and Provenance Records must not depend on it.

## 3. Validation Diagnostics

- [ ] 3.1 Add validation helpers that identify resolved tmp-label paths and detect durable references to temporary material.
- [ ] 3.2 Report missing or ineffective `tmp/` ignore policy for the Topic Workspace root and Topic Main Repository root.
- [ ] 3.3 Report tracked `tmp/` contents or boundary material that describes `tmp/` as Peer Read Access, generated-link target material, or handoff material.
- [ ] 3.4 Ensure validation never deletes, moves, archives, or promotes existing `tmp/` contents automatically.

## 4. Operator and Service Skills

- [ ] 4.1 Update `isomer-admin-topic-workspace-mgr` guidance to prepare and validate `topic.main_repo.tmp` and `agent.tmp` in `ensure-main-repo`, `create-worktrees`, `validate-worktrees`, `summarize`, and the full `topic-workspace` flow.
- [ ] 4.2 Update `isomer-admin-topic-team-specialize` guidance so delegated Agent Workspace setup evidence includes the `tmp/` ignore contract and never accepts `tmp/` as readiness evidence.
- [ ] 4.3 Update `isomer-srv-topic-env-setup` guidance to preserve `topic.tmp` as local disposable setup material in the baseline ignore policy.
- [ ] 4.4 Update skillset validation tests or rules so required public wording includes the `tmp/` local-only contract and rejects shared/durable `tmp/` wording.

## 5. Tests and Verification

- [ ] 5.1 Add or update unit tests for path resolution output covering `topic.tmp`, `topic.main_repo.tmp`, and `agent.tmp`.
- [ ] 5.2 Add or update runtime initialization and Agent Workspace creation tests for `tmp/` directory preparation and ignore policy behavior.
- [ ] 5.3 Add or update runtime validation tests for durable dependencies on `tmp/`, missing ignore policy, and tracked `tmp/` contents.
- [ ] 5.4 Run `openspec validate add-local-tmp-workspace-surfaces --strict`, `pixi run docs-validate`, `pixi run lint`, `pixi run typecheck`, and `pixi run test`.
