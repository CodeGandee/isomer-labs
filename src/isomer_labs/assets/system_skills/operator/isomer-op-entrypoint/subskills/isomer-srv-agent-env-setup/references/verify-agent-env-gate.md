# Verify Agent Env Gate

Use this subcommand to verify the Topic Workspace Pixi environment from each planned Agent Workspace cwd, or to rerun verification for one authoritative Agent Name as partial evidence.

## Required Inputs

Recover these before asking the user:

| Input | Resolution |
| --- | --- |
| Agent env context | Require Project, Research Topic, Topic Workspace, `manifest_path`, `pixi_environment`, semantic paths, requester, and confirmation source. |
| Topic env predecessor | Require ready or explicitly accepted Topic Workspace predecessor evidence from `require-topic-env-ready`. |
| Topic-main and projection predecessor | Require ready Topic Main Development Repository evidence, and projection predecessor evidence from `require-topic-main-ready` when the target spec depends on projected external repos. |
| Agent env target spec | Require resolved `topic.env.agent_setup_target_spec` from `derive-agent-env-gate`. |
| Gate checklist | Require `## Gate Checklist` from the agent env target spec; treat every item in that section as required readiness work unless the target spec explicitly moved the item to a non-readiness diagnostic section. |
| Worktree evidence | Require `create-agent-worktrees` output or read-only equivalent showing valid worktrees, support paths, and path evidence. |
| Verification matrix and resource check plan | Read `## Verification Matrix`, `## Resource Check Plan`, and `## Expected Results` from the target spec. Refuse to claim readiness when a resource-relevant matrix command lacks bounded-run tips classification evidence, or when a command classified as `heavy` or `unknown-risk` lacks a bounded-run guidance source, generic best-effort fallback evidence when used, affected Agent Name scope, bounded command, expected result, or blocker condition. |
| Package-specific runtime evidence | Require selected `isomer-misc-pkg-specifics` evidence or `no package-specific rule` when a verification matrix item depends on a named package's variant, accelerator, build, or runtime behavior. Route missing topic-level dependency planning back to `isomer-srv-topic-env-setup`. |
| Optional selected agent | Optional. It must be one authoritative Agent Name and reports selected-agent partial readiness evidence only. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Require predecessor artifacts**: resolved context, Topic Workspace predecessor evidence, Topic Main Development Repository predecessor evidence, projection predecessor evidence when required, agent env target spec, authoritative agent plan, and worktree evidence.
2. **Read the agent env target spec** and extract `## Gate Checklist`, `## Verification Matrix`, `## Resource Check Plan`, `## Expected Results`, `## Blockers`, `## Topic Pixi Binding`, and `## Execution Log`.
   - Confirm every targeted required checklist item has a pass condition, evidence source, affected Agent Name or matrix scope, and blocker condition.
   - Confirm every source-agent required cwd command has a matching verification matrix entry, bounded real-path command, or blocker. Do not accept a generic import, path, device-visibility, or projection-visibility smoke test as coverage for a requested build, inference, dataset, or benchmark path.
3. **Check Pixi files**:
   - Confirm the resolved `manifest_path`, selected `pixi_environment`, Topic Workspace `pixi.lock`, and `<topic-workspace-dir>/.pixi/` exist before reporting readiness.
4. **Choose target agents**:
   - Default to every authoritative planned Agent Name.
   - If a selected Agent Name is provided, verify only that authoritative name and label the result as selected-agent partial readiness evidence.
5. **Confirm commands are replayable**:
   - Each verification command must use `pixi run --manifest-path <manifest_path> --environment <pixi_environment> ...`.
   - Set cwd to the resolved `agent.workspace` for the target Agent Name.
   - When a matrix command depends on package-specific runtime behavior, use the selected verification expectation from `isomer-misc-pkg-specifics`, or require `no package-specific rule` before using generic verification.
   - If the agent target spec needs package dependency planning that is missing, stale, or ambiguous in `topic.env.topic_setup_target_spec`, report a blocker and route repair to `isomer-srv-topic-env-setup` instead of inventing per-agent install commands.
6. **Verify cwd-friendly semantic path query evidence**:
   - Include or record a check that an agent-scoped semantic label can be resolved from inside each target Agent Workspace without passing Agent Name.
7. **Verify projected external repo evidence when commands depend on it**:
   - Confirm the relevant projection entry from `topic.repos.main.projections.manifest` is present in predecessor evidence.
   - Confirm the projected path is visible from each target `agent.workspace` cwd without creating a substitute projection.
8. **Check resources before classified risky verification commands**:
   - Apply this when bounded-run tips classified a verification command as `heavy` or `unknown-risk`.
   - Treat the generated `## Resource Check Plan` and matching checklist item as the execution contract for each classified matrix command.
   - Confirm classification source, result, reason, resource dimensions, affected Agent Name scope, bounded-run guidance source, bounded command, expected result, and blocker condition.
   - If classification evidence or required bounded guidance is missing, report `blocked` and ask for `derive-agent-env-gate` to repair the target spec before verification.
   - Use lightweight read-only probes before commands classified as `heavy` or `unknown-risk`, including CPU load, available memory, available disk space, and GPU availability or active GPU processes when relevant.
   - Prefer the smallest real command that satisfies the gate, for example selected-agent partial run, reduced parallelism, selected build target, tiny model or tensor shape, sample data, reduced iterations, reduced batch size, selected tests, or short benchmark case.
   - If resources are insufficient, ambiguous, or already busy, do not run an unrelated smoke test in place of the required path. Explain naturally that the resource check is blocked, give the capacity reason and bounded real-path retry command, and keep selected-Agent partial evidence partial.
9. **Run verification commands** from the resolved `agent.workspace` cwd:
   - Do not rely on an activated shell, ambient Python environment, global package, unrecorded PATH entry, unrecorded library path, or unrecorded sourced script.
10. **Compare results to expected outputs** from the target spec and mark each agent command and its targeted checklist item as ready, failed, or blocked.
11. **Update the target spec execution log**:
   - Include Agent Name, cwd, resource check evidence, bounded real-path execution decisions, command, exit status, output summary, pass/fail result, partial scope when selected, blockers, any required unchecked checklist item, and next repair action.
12. **Report readiness**:
   - Use per-agent `ready` only when every targeted required `## Gate Checklist` item for that Agent Name is checked with cwd evidence from the resolved Agent Workspace.
   - Claim overall readiness only when every planned agent has a ready worktree, required support paths, complete path evidence, cwd-friendly query evidence, and every required checklist item for every planned Agent Name is covered by a passed verification command or bounded real-path command from that agent's cwd.
   - If any targeted required checklist item is unchecked, report `blocked`, `failed`, or `not checked` with the exact checklist item, Agent Name, reason, and next safe action.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from `topic.env.agent_setup_target_spec`, parent guardrails, and user request, then execute the plan.

## Readiness Rules

- `ready`: all targeted required `## Gate Checklist` items and source-agent required commands are covered by passed verification commands or bounded real-path commands from the resolved Agent Workspace cwd through recorded Pixi-scoped commands.
- `failed`: a targeted required checklist item was attempted through its matching command or check and did not satisfy expected results.
- `blocked`: predecessor artifacts, Topic Main Development Repository evidence, projection evidence, Pixi files, worktrees, support paths, path evidence, cwd query evidence, commands, expected results, or a targeted required checklist item are missing or cannot be completed. Name the exact checklist item and Agent Name.
- `not checked`: verification was explicitly not requested. Do not use `not checked` to bypass a source-agent required cwd command or targeted unchecked checklist item during setup; report `blocked` when a required bounded real-path check cannot be run safely.

Selected-agent direct verification updates that agent's evidence but does not make the overall result ready unless the complete matrix has already passed.

## Operational Contract

- Treat Topic Workspace readiness as prerequisite evidence only; every requested Agent Workspace cwd must be verified by this subcommand before reporting per-agent readiness.
- Report `gate-cwd-incompatible` or equivalent when a topic env command cannot run from Agent Workspace cwd.

## Operational Notes

- Missing, stale, blocked, or inconsistent projection evidence routes repair to `isomer-srv-topic-env-setup`.
- When selected-agent partial coverage or another bounded real-path command is enough and it exercises the critical path named by the checklist item, use it and label the evidence correctly.
- When the required command path cannot be exercised safely even in bounded form, block with resource evidence and leave the checklist item unchecked.
- A simple smoke test that misses the essential cwd command path is not enough to claim readiness.
- If the user explicitly accepts a weaker check, record the user downgrade, original checklist item, affected Agent Name or matrix scope, weaker evidence, and limitation instead of presenting it as proof that the original critical path passed.
- Readiness by agent and blockers must remain visible.

## Guardrails

- DO NOT claim readiness from topic-root-only success.
- DO NOT claim package-specific runtime readiness from solver success, package metadata, or generic import success when `isomer-misc-pkg-specifics` requires stronger evidence.
- DO NOT write or run independent PyPI, Pixi, Conda, or runtime-wiring package install commands for dependencies that belong to topic env setup.
- DO NOT create external repo projections or Agent Workspace-local substitute projections.
- DO NOT create Agent Instances, Workspace Runtime records, Houmao launch material, or Execution Adapter material.
- DO NOT suppress partial failures.
- DO NOT run verification classified as `heavy` or `unknown-risk` at full scale merely to make the all-agent matrix look stronger or because the generated bounded-run plan is incomplete.
- DO NOT mark a required checklist item complete with an unrelated weaker smoke test.
