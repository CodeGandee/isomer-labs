# Derive Agent Env Gate

Use this subcommand to generate the operational per-agent readiness gate from the source agent gate, topic env predecessor evidence, and authoritative agent plan.

## Required Inputs

Recover these before asking the user:

| Input | Resolution |
| --- | --- |
| Agent env context | Require Project, Research Topic, Topic Workspace, Pixi binding, semantic topic labels, requester, and confirmation source from `resolve-agent-env-context`. |
| Topic env predecessor | Require `require-topic-env-ready` output and `user-intent/derived/isomer-env-gate.md`. |
| Source agent gate summary | Require `read-agent-env-gate` output from `user-intent/src/agent-env-gate.md`. |
| Agent plan | Require `plan-agent-workspaces` output with authoritative Agent Names, branch plan, and resolved semantic labels. |
| Derived gate path | Use `<topic-workspace-dir>/user-intent/derived/isomer-agent-env-gate.md`; create the parent directory when writing the gate. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Require predecessor artifacts**: resolved context, topic env predecessor evidence, source agent gate summary, and authoritative agent plan.
2. **Resolve the derived gate path** as `<topic-workspace-dir>/user-intent/derived/isomer-agent-env-gate.md` and create its parent directory when safe.
3. **Translate source gate requirements** into a per-agent operational gate. Use the Topic Workspace predecessor as evidence, but do not duplicate dependency planning from `isomer-env-gate.md`.
4. **Derive the per-agent verification matrix**. For every authoritative Agent Name, record cwd as the resolved `agent.workspace` and each command as `pixi run --manifest-path <manifest_path> --environment <pixi_environment> ...`.
5. **Preserve cwd assumptions** from the topic env gate. If a topic env command is topic-root-only or repo-specific and cannot run from an Agent Workspace cwd, record `gate-cwd-incompatible` or an equivalent blocker instead of false readiness.
6. **Write the fixed Markdown template** from **Template**. Include every section; write `None.` or a short reason when a section does not apply.
7. **Initialize or update the execution log** with requester, confirmation source, optional Service Request refs, support Artifact refs, Provenance refs, changed files, commands run, blockers, and `Not run yet.` for verification commands that have not been executed.
8. **Report `agent_env_gate_path`** and any blockers that prevent Topic Main Repository setup, worktree creation, or verification.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step derivation plan from the source gate, topic env predecessor, agent plan evidence, parent guardrails, and user request, then execute the plan.

## Template

```markdown
# Isomer Agent Environment Gate

## Source Agent Gate

## Topic Env Gate

## Topic Pixi Binding

## Topic Main Repository Configuration

## Agent Plan

## Semantic Paths

## Worktree Plan

## Verification Matrix

## Expected Results

## Blockers

## Execution Log
```

## Section Guidance

`## Source Agent Gate` should summarize `user-intent/src/agent-env-gate.md` and cite the source path.

`## Topic Env Gate` should reference `user-intent/derived/isomer-env-gate.md` as Topic Workspace predecessor evidence. A topic-root pass is prerequisite evidence only; it is not Agent Workspace cwd readiness.

`## Topic Pixi Binding` should record `manifest_path_or_dir`, `manifest_path`, `pixi_environment`, and binding source.

`## Topic Main Repository Configuration` should record non-destructive configuration requirements for the Topic Main Repository resolved by `topic.repos.main`.

`## Agent Plan` should list authoritative Agent Names, source role ids, branch plan, selected-agent partial scope when present, and any corroborating operator map evidence.

`## Semantic Paths` should list `topic.repos.main`, `topic.repos.main.isomer_managed`, `topic.agents_root`, `agent.workspace`, required agent support labels, path sources, and blockers.

`## Worktree Plan` should list expected `per-agent/<agent-name>/main` branches and resolved `agent.workspace` worktree paths.

`## Verification Matrix` should list each Agent Name, source requirement, cwd, exact Pixi command, and expected result.

`## Blockers` should list missing predecessor evidence, missing source gate, agent-plan-conflict, unsafe path, out-of-scope source gate request, gate-cwd-incompatible command, or unresolved setup ambiguity.

`## Execution Log` should record direct Project Operator Session invocation, mutation confirmation, optional Service Request, support Artifact, or Provenance refs, changed files, commands run, verification results, and blockers.

## Guardrails

- Do not create per-agent dependency plans or reinterpret Topic Workspace dependency policy.
- Do not use tmp paths as durable readiness evidence.
- Do not claim verification has run before `verify-agent-env-gate`.
- Do not create Workspace Runtime records or Agent Team Instance records.
