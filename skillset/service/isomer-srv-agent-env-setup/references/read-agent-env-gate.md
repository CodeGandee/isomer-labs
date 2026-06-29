# Read Agent Env Gate

Use this subcommand to read the user-authored Agent Workspace source intent and extract the static setup and cwd verification contract.

## Required Inputs

Recover these before asking the user:

| Input | Resolution |
| --- | --- |
| Agent env context | Require resolved Project, Research Topic, Topic Workspace, Pixi binding, and topic semantic path evidence from `resolve-agent-env-context`. |
| Agent env source intent | Resolve `topic.intent.agent_env_requirements` through Workspace Path Resolution. Under `isomer-default.v1`, this defaults to `<topic-workspace-dir>/intent/src/agent-env-gate.md`. |
| Topic env predecessor | Prefer `require-topic-env-ready` output so the source gate can be interpreted against the selected Topic Workspace Pixi environment. |
| Optional modifiers | None for this step. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Require resolved context** from `resolve-agent-env-context`; refuse to run when Project, Research Topic, Topic Workspace, or Pixi binding evidence is missing.
2. **Resolve the source intent label** `topic.intent.agent_env_requirements`; record semantic label, resolved path, storage profile, source, source detail, diagnostics, and blockers.
3. **Read the source intent** and extract source intent, required command set, expected results, success criteria, Topic Main Repository configuration requirements, agent plan constraints, cwd assumptions, and blockers.
4. **Check service-safe scope**. If the source intent asks for Agent Instance creation, Workspace Runtime mutation, Houmao launch, Execution Adapter launch, live research execution, privileged host mutation, dependency mutation, or research decisions, report an out-of-scope blocker instead of deriving executable setup steps.
5. **Require enough specificity** to derive required Agent Workspace cwd commands. If commands, expected results, or cwd assumptions are missing or ambiguous, report a blocker.
6. **Report the source gate summary** and carry it to `derive-agent-env-gate`, `ensure-topic-main-repository`, and `verify-agent-env-gate`.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step source-gate inspection from the resolved context, source file, topic env predecessor, and parent guardrails, then execute the plan.

## Output Notes

Carry forward:

- `agent_env_source_label`;
- `agent_env_source_path`;
- source storage profile, source, source detail, diagnostics, and blockers;
- source intent;
- required command set;
- expected results;
- success criteria;
- Topic Main Repository configuration requirements;
- agent plan constraints;
- cwd assumptions;
- out-of-scope requests;
- blockers.

## Guardrails

- Preserve uncertainty instead of pretending a vague source intent is precise.
- Do not choose Agent Names here.
- Do not create or mutate files from this subcommand.
- Passing means every required command must be runnable from each planned `agent.workspace` cwd through the resolved Topic Workspace Pixi environment.
