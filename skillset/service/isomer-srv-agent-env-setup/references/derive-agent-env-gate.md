# Derive Agent Env Gate

Use this subcommand to generate or validate the operational per-agent readiness target spec from source agent intent, topic env predecessor evidence, authoritative agent plan, or an explicit manual target spec.

## Required Inputs

Recover these before asking the user:

| Input | Resolution |
| --- | --- |
| Agent env context | Require Project, Research Topic, Topic Workspace, Pixi binding, semantic topic labels, requester, and confirmation source from `resolve-agent-env-context`. |
| Topic env predecessor | Require `require-topic-env-ready` output and `topic.env.topic_setup_target_spec`. |
| Source agent intent summary | Require `read-agent-env-gate` output from `topic.intent.agent_env_requirements` when deriving from source intent. |
| Explicit target spec | Optional. A manual file, prompt, or context may supply the per-agent operational target spec directly. When supplied, validate it against this page's fixed sections and per-agent cwd verification policy instead of requiring source intent. |
| Agent plan | Require `plan-agent-workspaces` output with authoritative Agent Names, branch plan, and resolved semantic labels. |
| Agent env target spec | Resolve `topic.env.agent_setup_target_spec` through Workspace Path Resolution. Under `isomer-default.v1`, this defaults to `<topic-workspace-dir>/intent/derived/isomer-agent-env-gate.md`; create the parent directory when writing the target spec. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Require predecessor artifacts**:
   - Require resolved context, topic env predecessor evidence, source agent intent summary when deriving from source intent, explicit target spec input when manual mode is used, and authoritative agent plan.
2. **Resolve the target spec label** `topic.env.agent_setup_target_spec`:
   - Record semantic label, resolved path, storage profile, source, source detail, diagnostics, and blockers.
   - Create the parent directory when writing the target spec.
3. **Translate or validate source requirements** into a per-agent operational target spec:
   - Use the Topic Workspace predecessor as evidence.
   - Do not duplicate dependency planning from `topic.env.topic_setup_target_spec`.
4. **Derive the per-agent verification matrix**:
   - For every authoritative Agent Name, record cwd as the resolved `agent.workspace`.
   - Record each command as `pixi run --manifest-path <manifest_path> --environment <pixi_environment> ...`.
5. **Preserve cwd assumptions** from the topic env gate:
   - If a topic env command is topic-root-only or repo-specific and cannot run from an Agent Workspace cwd, record `gate-cwd-incompatible` or an equivalent blocker instead of false readiness.
6. **Write or update the fixed Markdown template** from **Template**:
   - Write at the resolved `topic.env.agent_setup_target_spec` path when deriving from source intent.
   - When using an explicit manual target spec, record the explicit source and normalized target-spec copy or reference, then preserve every required section.
7. **Initialize or update the execution log**:
   - Include requester, confirmation source, optional Service Request refs, support Artifact refs, Provenance refs, changed files, commands run, blockers, and `Not run yet.` for verification commands that have not been executed.
8. **Report target spec metadata** and any blockers that prevent Topic Main Repository setup, worktree creation, or verification.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step derivation plan from the source intent or explicit target spec, topic env predecessor, agent plan evidence, parent guardrails, and user request, then execute the plan.

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

`## Source Agent Gate` should summarize `topic.intent.agent_env_requirements` and cite its resolved path, or name the explicit target spec source when the service was invoked manually.

`## Topic Env Gate` should reference `topic.env.topic_setup_target_spec` as Topic Workspace predecessor evidence. A topic-root pass is prerequisite evidence only; it is not Agent Workspace cwd readiness.

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
