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
| Topic Main Development Repository predecessor evidence | Require ready evidence from `require-topic-main-ready`, including topic-main Git state, Isomer-managed namespace posture, and projection metadata when the agent env target spec depends on projected external repos. |
| Agent env source intent | Resolve `topic.intent.agent_env_requirements` when deriving from user-authored source intent. Under `isomer-default.v1`, this defaults to `<topic-workspace-dir>/intent/src/agent-env-gate.md`; `read-agent-env-gate` must confirm it exists before source-intent-derived readiness can be claimed. |
| Agent env target spec | Resolve `topic.env.agent_setup_target_spec`, or accept an explicit manual target spec file, prompt, or context. Under `isomer-default.v1`, the label defaults to `<topic-workspace-dir>/intent/derived/isomer-agent-env-gate.md`; `derive-agent-env-gate` must create, update, normalize, or validate it before worktree setup or verification. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Run the setup chain** in this fixed all-agent order:
   - Run `resolve-agent-env-context`, `require-topic-env-ready`, `read-agent-env-gate` when deriving from source intent, `plan-agent-workspaces`, `derive-agent-env-gate`, `require-topic-main-ready`, `create-agent-worktrees`, and `verify-agent-env-gate`.
   - If an explicit target spec is supplied, `derive-agent-env-gate` validates that spec and records its source instead of requiring `read-agent-env-gate`.
   - Preserve every source-agent required cwd command through the chain. Heavy commands must become bounded real-path verification commands, not generic smoke tests that miss the requested build, inference, dataset, or benchmark path.
2. **Load each referenced subcommand page** and execute its `## Workflow`, carrying forward each result to the next step.
3. **Verify every authoritative planned Agent Name**. The full flow must not use selected-agent partial mode for overall readiness.
4. **Stop on blockers** when any step reports a blocking condition:
   - Include missing predecessor artifacts, missing source gate, missing Topic Workspace predecessor status, agent-plan-conflict, unsafe paths, unsafe Git state, nonmatching worktrees, failing cwd gate commands, out-of-scope requests, unconfirmed mutation, or failed preconditions.
5. **Report the combined result** using the parent **Output Contract**:
   - Include topic env predecessor status, topic-main predecessor evidence, projection predecessor evidence when required, semantic paths, requester, confirmation source, optional Service Request or Provenance refs, source intent or explicit target spec metadata, agent workspace paths, branch plan, worktree status by agent, resource check status, bounded real-path decisions, readiness by agent, overall readiness, changed files, commands run, blockers, and next action.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the linked subcommands, parent guardrails, and user request, then execute the plan.

## Step Order

| Order | Step | Reference | Carry Forward |
| --- | --- | --- | --- |
| 1 | Resolve agent env context | [resolve-agent-env-context.md](resolve-agent-env-context.md) | Project root, Research Topic, Topic Workspace, Pixi binding, semantic labels, requester, confirmation source, optional refs, and blockers. |
| 2 | Require topic env ready | [require-topic-env-ready.md](require-topic-env-ready.md) | Topic env predecessor status and repair route. |
| 3 | Read source agent intent | [read-agent-env-gate.md](read-agent-env-gate.md) | `topic.intent.agent_env_requirements` metadata, source intent summary, required commands, Topic Main Development Repository predecessor requirements, projection requirements, cwd assumptions, and blockers. Skip only when an explicit manual target spec is supplied. |
| 4 | Plan Agent Workspaces | [plan-agent-workspaces.md](plan-agent-workspaces.md) | Authoritative Agent Names, branches, semantic paths, path sources, and blockers. |
| 5 | Derive or validate agent env target spec | [derive-agent-env-gate.md](derive-agent-env-gate.md) | `topic.env.agent_setup_target_spec` metadata, target spec source, verification matrix, resource check plan, expected results, and blockers. |
| 6 | Require Topic Main Development Repository ready | [require-topic-main-ready.md](require-topic-main-ready.md) | Topic-main predecessor status, projection predecessor status when required, and repair route to `isomer-srv-topic-env-setup`. |
| 7 | Create Agent Worktrees | [create-agent-worktrees.md](create-agent-worktrees.md) | Worktree status by agent, support path status, boundary material posture, and blockers. |
| 8 | Verify agent env gate | [verify-agent-env-gate.md](verify-agent-env-gate.md) | Readiness by agent, resource check evidence, bounded real-path decisions, commands run, execution log, blockers, and overall readiness. |

## Expected Result

Successful setup leaves the selected Topic Workspace with:

```text
<topic-workspace-dir>/
  .pixi/
  pixi.lock
  repos/
    topic-main/                 # prepared predecessor for semantic label topic.repos.main
      isomer-managed/
        tracked/
          manifests/
            extern-projections.toml
        topic-owned/
          readonly/
            extern/
          writable/
            extern/
  agents/
    <agent-name>/               # default binding for semantic label agent.workspace
  intent/
    src/
      agent-env-gate.md           # default binding for topic.intent.agent_env_requirements
    derived/
      isomer-env-gate.md          # default binding for topic.env.topic_setup_target_spec
      isomer-agent-env-gate.md    # default binding for topic.env.agent_setup_target_spec
```

Readiness means topic env setup has prepared topic-main and required projections, every authoritative planned Agent Name has a valid Agent Workspace worktree, required support paths, semantic path evidence, and every required command from the resolved `topic.env.agent_setup_target_spec` passes from that agent's resolved `agent.workspace` cwd through `pixi run --manifest-path <manifest_path> --environment <pixi_environment> ...`. A generic smoke test can support diagnostics but cannot replace bounded real-path verification of each source-agent required cwd command.

## Guardrails

- Run the subcommands in the order listed in **Step Order**.
- Do not skip directly to Git worktree creation or verification.
- Do not create per-agent Pixi environments or mutate dependencies.
- Do not create, initialize, configure, repair, or project external repos into `topic.repos.main`; route missing or stale predecessor evidence to `isomer-srv-topic-env-setup`.
- Do not claim runtime launch readiness.
- Do not multiply resource-heavy verification across every Agent Workspace unless the resource check shows enough idle capacity and the target spec requires the full matrix. Use selected-agent partial evidence or another bounded real-path command when full verification would overload the host, but the selected command must still exercise the requested cwd path. If no bounded real-path command can run safely, report a blocker with resource evidence.
- Preserve blockers and partial failures in the combined report.
