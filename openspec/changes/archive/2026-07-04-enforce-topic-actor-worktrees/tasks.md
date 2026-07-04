## 1. Worktree Inspection

- [x] 1.1 Add a reusable actor worktree inspection helper that reads `git worktree list --porcelain` from resolved `topic.repos.main`, normalizes paths, and reports matching path, branch, duplicate branch checkout, and non-Git topic-main states.
- [x] 1.2 Add structured actor worktree readiness payload fields for source repo, workspace path, expected branch, observed branch, status, blockers, and next action.

## 2. Actor Materialization and Diagnostics

- [x] 2.1 Update `src/isomer_labs/workspace/actors.py` so missing actor workspace paths are created as worktrees of resolved `topic.repos.main` on `actor.effective_branch`.
- [x] 2.2 Update existing actor workspace handling so matching worktrees are reused and nonmatching existing paths block without overwriting, moving, cleaning, resetting, or reinitializing content.
- [x] 2.3 Reject duplicate actor branch checkouts in another topic-main worktree before attempting `git worktree add`.
- [x] 2.4 Treat missing or non-Git `topic.repos.main` as a blocker for actor worktree readiness instead of creating a placeholder actor directory.
- [x] 2.5 Update `diagnose_topic_actor` output to include the same actor worktree readiness evidence and blockers used by materialization.
- [x] 2.6 Ensure actor support paths are created only after the actor workspace is validated or created as the expected topic-main worktree.

## 3. Skills and Operator Guidance

- [x] 3.1 Update Topic Manager actor materialization, diagnostics, and verification references to say actor readiness requires the expected topic-main worktree and branch evidence.
- [x] 3.2 Update Topic Creator `setup-actors` guidance to stop before actor env gate verification when delegated worktree readiness evidence is missing or blocked.
- [x] 3.3 Update manual research onboarding guidance so manually controlled Topic Actors use topic-main worktree workspaces, while controller provenance remains the actor/agent distinction.

## 4. Tests and Validation

- [x] 4.1 Add unit tests for missing actor workspace creation, existing matching worktree reuse, existing nonmatching path blocker, duplicate branch checkout blocker, and non-Git topic-main blocker.
- [x] 4.2 Add or update CLI-level diagnostics tests so `actors-diagnose` reports worktree readiness and blockers for selected Topic Actors.
- [x] 4.3 Run `pixi run test` for the affected unit tests.
- [x] 4.4 Run `openspec validate enforce-topic-actor-worktrees --strict`.
