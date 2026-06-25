## 1. Skill Bundle and Operator Registration

- [x] 1.1 Create `skillset/operator/isomer-admin-topic-workspace-mgr/` with minimal `SKILL.md` frontmatter and `agents/openai.yaml` metadata that consistently use `isomer-admin-topic-workspace-mgr`.
- [x] 1.2 Write the top-level skill router with grouped procedural, helper, and misc subcommand tables, default `topic-workspace` routing, required inputs, output contract, and guardrails.
- [x] 1.3 Add executable reference pages for `resolve-workspace`, `ensure-main-repo`, `plan-agents`, `create-worktrees`, `write-boundaries`, `create-agent-branch`, `validate-worktrees`, `summarize`, `help`, and `topic-workspace`.
- [x] 1.4 Ensure every reference page has a near-top `## Workflow`, numbered steps, and a freeform fallback.
- [x] 1.5 Update `skillset/operator/README.md` to list the new skill and describe its boundary relative to `isomer-admin-topic-team-specialize` and `isomer-srv-env-setup`.

## 2. Git-Backed Workspace Workflow Rules

- [x] 2.1 Define `resolve-workspace` instructions to resolve Project, Research Topic, and Topic Workspace through Project Manifest-backed Isomer context rather than directory scanning.
- [x] 2.2 Define `ensure-main-repo` instructions for `<topic-workspace-dir>/repos/topic-main`, including existing-repo validation, missing-repo creation policy, blocker reporting, and no silent repair.
- [x] 2.3 Define `plan-agents` instructions for agent-key normalization, collision rejection, role binding mapping, `agent_workspace_ref` planning, and `per-agent/<agent-key>/main` default branch naming.
- [x] 2.4 Define `create-worktrees` instructions for idempotent Git worktree creation under `<topic-workspace-dir>/agents/<agent-key>` and duplicate branch checkout rejection.
- [x] 2.5 Define `create-agent-branch` instructions that constrain future branches to `per-agent/<agent-key>/<branch-name>` and reject unsafe branch segments.
- [x] 2.6 Define `write-boundaries`, `validate-worktrees`, and `summarize` instructions for advisory Workspace Boundary docs, Peer Read Access notes, Git topology checks, profile or packet ref checks, blockers, and next actions.

## 3. Operator Skill Validation

- [x] 3.1 Extend `scripts/validate_skillsets.py` to require the new operator skill bundle, expected subcommand pages, workflow structure, local references, help table, and key guardrail/output terms.
- [x] 3.2 Add unit tests in `tests/unit/test_validate_skillsets.py` for accepted `isomer-admin-topic-workspace-mgr` structure and representative failures.
- [x] 3.3 Ensure generic operator skill validation still accepts existing operator skills and does not treat the new skill as one of the removed standalone helper skills.

## 4. Topic Team Specialization Integration

- [x] 4.1 Update `isomer-admin-topic-team-specialize` entrypoint, help, and relevant references to mention `isomer-admin-topic-workspace-mgr` for Git-backed Agent Workspace setup.
- [x] 4.2 Revise `references/setup-agent-workspace.md` so Git-backed `repos/topic-main` worktree setup is delegated to the topic workspace manager skill.
- [x] 4.3 Revise `references/validate-topic-team.md` and `references/finalize-topic-team.md` so delegated workspace outputs can be recorded as static setup evidence and missing delegated setup is reported as a blocker.
- [x] 4.4 Update operator skill validation expectations and tests if the Topic Team Specialization skill gains new required terms or references.

## 5. Profile, Packet, and Path Validation

- [x] 5.1 Extend Topic Agent Team Profile validation to accept `agent_workspace_ref` values under the selected Topic Workspace and reject refs outside the selected Topic Workspace, outside the Project root, or inside another Research Topic's Topic Workspace.
- [x] 5.2 Extend Topic Team Instantiation Packet validation with equivalent `agent_workspace_ref` topic-scope checks.
- [x] 5.3 Add or update tests for valid `<topic-workspace-dir>/agents/alice` refs, cross-topic refs, and refs that do not imply the future Agent Instance id equals `alice`.
- [x] 5.4 Update any serialization or fixture helpers needed to preserve role binding `agent_workspace_ref` values in packets and materialized profiles.

## 6. Workspace Runtime Path Planning

- [x] 6.1 Update Agent Team Instance creation so an active role binding with a validated `agent_workspace_ref` records the Agent Workspace path plan from that ref.
- [x] 6.2 Preserve the existing fallback to `<topic-workspace>/agents/<agent-instance-id>` when no approved `agent_workspace_ref` exists.
- [x] 6.3 Record path plan source/source detail so refs from profile or packet material are distinguishable from default generated paths.
- [x] 6.4 Ensure created Agent Instance ids remain globally unique and do not need to equal agent keys such as `alice`.
- [x] 6.5 Add runtime tests for path plan creation from `agent_workspace_ref`, fallback path creation, unsafe ref rejection, and Agent Workspace directory materialization.

## 7. Documentation and Validation

- [x] 7.1 Update docs or local references that describe Agent Workspace defaults so they mention approved `agent_workspace_ref` path plans as an explicit alternative to generated defaults.
- [x] 7.2 Run skill validation for the new skill, including the skill-creator quick validator and `pixi run validate-operator-skills`.
- [x] 7.3 Run `pixi run python -m unittest tests.unit.test_validate_skillsets` and any targeted runtime/profile validation tests added for this change.
- [x] 7.4 Run `openspec validate add-topic-workspace-manager-skill --strict`.
- [x] 7.5 Run the repository validation commands required before review: `pixi run lint`, `pixi run typecheck`, and `pixi run test`.
