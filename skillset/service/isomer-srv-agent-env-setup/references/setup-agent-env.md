# Setup Agent Env

Use this subcommand to run the full all-agent Agent Workspace environment setup flow for one Research Topic.

## Required Inputs

Recover these before asking the user:

| Input | Resolution |
| --- | --- |
| `subcommand` | Use this page when the prompt names `setup-agent-env`, or when the prompt describes concrete Agent Workspace env setup without naming another subcommand. |
| Project root | Use the provided path or current working directory; it must resolve to an Isomer Project root containing `.isomer-labs/manifest.toml`. |
| Research Topic or Topic Workspace selector | Read a Research Topic id, Topic Workspace ref, or Topic Workspace path from the prompt or Project Manifest context. Ask only when several topics remain plausible. |
| Mutation confirmation | Require direct Project Operator Session mutation confirmation or Service Request authorization before creating or changing files. |
| `source_agent_env_gate_path` | Use `<topic-workspace-dir>/user-intent/src/agent-env-gate.md`; `read-agent-env-gate` must confirm it exists before readiness can be claimed. |
| `agent_env_gate_path` | Use `<topic-workspace-dir>/user-intent/derived/isomer-agent-env-gate.md`; `derive-agent-env-gate` must create or update it before worktree setup or verification. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Run the setup chain** in this fixed all-agent order: `resolve-agent-env-context`, `require-topic-env-ready`, `read-agent-env-gate`, `plan-agent-workspaces`, `derive-agent-env-gate`, `ensure-topic-main-repository`, `create-agent-worktrees`, and `verify-agent-env-gate`.
2. **Load each referenced subcommand page** and execute its `## Workflow`, carrying forward each result to the next step.
3. **Verify every authoritative planned Agent Name**. The full flow must not use selected-agent partial mode for overall readiness.
4. **Stop on blockers** when any step reports missing predecessor artifacts, missing source gate, missing topic env readiness, agent-plan-conflict, unsafe paths, unsafe Git state, nonmatching worktrees, failing cwd gate commands, out-of-scope requests, unconfirmed mutation, or failed preconditions.
5. **Report the combined result** using the parent **Output Contract**, including topic env predecessor status, semantic paths, requester, confirmation source, optional Service Request or Provenance refs, source and derived gate paths, Topic Main Repository state, agent workspace paths, branch plan, worktree status by agent, readiness by agent, overall readiness, changed files, commands run, blockers, and next action.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the linked subcommands, parent guardrails, and user request, then execute the plan.

## Step Order

| Order | Step | Reference | Carry Forward |
| --- | --- | --- | --- |
| 1 | Resolve agent env context | [resolve-agent-env-context.md](resolve-agent-env-context.md) | Project root, Research Topic, Topic Workspace, Pixi binding, semantic labels, requester, confirmation source, optional refs, and blockers. |
| 2 | Require topic env ready | [require-topic-env-ready.md](require-topic-env-ready.md) | Topic env predecessor status and repair route. |
| 3 | Read source agent gate | [read-agent-env-gate.md](read-agent-env-gate.md) | Source gate summary, required commands, Topic Main Repository configuration requirements, cwd assumptions, and blockers. |
| 4 | Plan Agent Workspaces | [plan-agent-workspaces.md](plan-agent-workspaces.md) | Authoritative Agent Names, branches, semantic paths, path sources, and blockers. |
| 5 | Derive agent env gate | [derive-agent-env-gate.md](derive-agent-env-gate.md) | `agent_env_gate_path`, verification matrix, expected results, and blockers. |
| 6 | Ensure Topic Main Repository | [ensure-topic-main-repository.md](ensure-topic-main-repository.md) | Git anchor state, owner branch, changed files, commands run, and blockers. |
| 7 | Create Agent Worktrees | [create-agent-worktrees.md](create-agent-worktrees.md) | Worktree status by agent, support path status, boundary material posture, and blockers. |
| 8 | Verify agent env gate | [verify-agent-env-gate.md](verify-agent-env-gate.md) | Readiness by agent, commands run, execution log, blockers, and overall readiness. |

## Expected Result

Successful setup leaves the selected Topic Workspace with:

```text
<topic-workspace-dir>/
  .pixi/
  pixi.lock
  repos/
    topic-main/                 # default binding for semantic label topic.main_repo
  agents/
    <agent-name>/               # default binding for semantic label agent.workspace
  user-intent/
    src/
      agent-env-gate.md
    derived/
      isomer-env-gate.md
      isomer-agent-env-gate.md
```

Readiness means every authoritative planned Agent Name has a valid Agent Workspace worktree, required support paths, semantic path evidence, and every required agent-env-gate command passes from that agent's resolved `agent.workspace` cwd through `pixi run --manifest-path <manifest_path> --environment <pixi_environment> ...`.

## Guardrails

- Run the subcommands in the order listed in **Step Order**.
- Do not skip directly to Git worktree creation or verification.
- Do not create per-agent Pixi environments or mutate dependencies.
- Do not claim runtime launch readiness.
- Preserve blockers and partial failures in the combined report.
