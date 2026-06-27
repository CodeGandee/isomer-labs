## 1. Baseline and Documentation

- [x] 1.1 Record canonical domain-language support for **Local Tmp Surface**, including `topic.tmp`, `topic.main_repo.tmp`, and `agent.tmp`.
- [x] 1.2 Keep documentation validation that rejects bare or fixed-path-only `tmp/` wording unless it names semantic labels and local, ignored, disposable, not-durable semantics.
- [x] 1.3 Update user-facing docs from "planned" or "downstream" tmp wording to implemented first-class local tmp label wording after the code labels land.
- [x] 1.4 Update Topic Workspace documentation to list `topic.tmp`, `topic.main_repo.tmp`, and `agent.tmp` with `isomer-default.v1` bindings and distinguish tmp from `agent.scratch`, Peer Read Access, generated links, owner-preserved records, and Git-tracked material.

## 2. Semantic Surface Catalog and Path Resolution

- [x] 2.1 Add `topic.tmp`, `topic.main_repo.tmp`, and `agent.tmp` to the Topic Workspace Manifest semantic surface catalog with disposable, non-shared classification.
- [x] 2.2 Add default `isomer-default.v1` bindings for `<topic-workspace>/tmp/`, `<resolved topic.main_repo>/tmp/`, and `<resolved agent.workspace>/tmp/`.
- [x] 2.3 Add explicit compatibility ids such as `topic_tmp`, `topic_main_tmp`, and `agent_tmp` where compatibility surface mapping is needed.
- [x] 2.4 Ensure `project paths get`, `project paths list`, and path preview output can report tmp labels, resolved paths, path sources, and disposable/non-shared classification.
- [x] 2.5 Add or update unit tests for path resolution output covering `topic.tmp`, `topic.main_repo.tmp`, and `agent.tmp`, including custom manifest bindings and path safety diagnostics.

## 3. Setup, Materialization, and Ignore Policy

- [x] 3.1 Preserve the current `isomer-srv-topic-env-setup` behavior that writes literal `tmp/` into the Topic Workspace `.gitignore` during Topic Workspace environment setup.
- [x] 3.2 Update Topic Workspace materialization or setup paths that own `topic.tmp` to create or validate the resolved directory and Topic Workspace root ignore rule without writing `.gitkeep`.
- [x] 3.3 Update Topic Main Repository preparation to create or validate resolved `topic.main_repo.tmp` and the Topic Main Repository root ignore rule.
- [x] 3.4 Update Agent Workspace worktree preparation to create or validate resolved `agent.tmp`, relying on the Topic Main Repository ignore rule for Git worktrees.
- [x] 3.5 Ensure setup reports missing tmp directories as repairable local posture while treating missing or ineffective ignore policy as a readiness blocker for the owning setup flow.

## 4. Runtime and Validation Diagnostics

- [x] 4.1 Add validation helpers that identify resolved tmp-label paths from current semantic path evidence.
- [x] 4.2 Report durable references to tmp material from Workspace Runtime records, handoffs, Artifact locators, Provenance Records, Evidence Items, Decision Records, profile material, readiness evidence, or research claims.
- [x] 4.3 Report tracked files under resolved tmp paths and boundary material that describes tmp as Peer Read Access, generated-link target material, or handoff material.
- [x] 4.4 Ensure validation never deletes, moves, archives, promotes, or rewrites existing tmp contents automatically.
- [x] 4.5 Add or update runtime validation tests for durable dependencies on tmp, missing or ineffective ignore policy, and tracked tmp contents.

## 5. Operator and Service Skills

- [x] 5.1 Preserve current `isomer-srv-topic-env-setup` guidance that describes default `tmp/` as downstream `topic.tmp` posture and local disposable material.
- [x] 5.2 Preserve current `isomer-srv-agent-env-setup` guidance that treats `topic.main_repo.tmp` and `agent.tmp` as optional local ignored disposable posture when available.
- [x] 5.3 Update `isomer-admin-topic-workspace-mgr` guidance to prepare and validate `topic.main_repo.tmp` and `agent.tmp` in `ensure-main-repo`, `create-worktrees`, `validate-worktrees`, `summarize`, and the full `topic-workspace` flow.
- [x] 5.4 Update `isomer-admin-topic-team-specialize` guidance so delegated Agent Workspace setup evidence includes tmp ignore posture and never accepts tmp contents as readiness evidence.
- [x] 5.5 Update `isomer-srv-topic-env-setup` output guidance to report resolved `topic.tmp` when available while preserving the existing literal `tmp/` default ignore behavior.
- [x] 5.6 Update skillset validation tests or rules so required public wording includes the tmp local-only contract and rejects shared/durable tmp wording.

## 6. Verification

- [x] 6.1 Run `openspec validate add-local-tmp-workspace-surfaces --strict`.
- [x] 6.2 Run `pixi run docs-validate`.
- [x] 6.3 Run `pixi run lint`.
- [x] 6.4 Run `pixi run typecheck`.
- [x] 6.5 Run `pixi run test`.
