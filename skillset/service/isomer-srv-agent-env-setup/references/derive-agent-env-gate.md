# Derive Agent Env Gate

Use this subcommand to generate or validate the operational per-agent readiness target spec from source agent intent, topic env predecessor evidence, authoritative agent plan, or an explicit manual target spec.

## Required Inputs

Recover these before asking the user:

| Input | Resolution |
| --- | --- |
| Agent env context | Require Project, Research Topic, Topic Workspace, Pixi binding, semantic topic labels, requester, and confirmation source from `resolve-agent-env-context`. |
| Topic env predecessor | Require `require-topic-env-ready` output and `topic.env.topic_setup_target_spec`. |
| Topic-main predecessor | Require `require-topic-main-ready` output when deriving or validating target specs that create worktrees or use projected external repos. |
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
   - Preserve every source-agent required cwd command as either a verification matrix entry or a named blocker; do not replace a requested build, inference, dataset, or benchmark path with an unrelated smoke test.
4. **Derive the per-agent verification matrix**:
   - For every authoritative Agent Name, record cwd as the resolved `agent.workspace`.
   - Record each command as `pixi run --manifest-path <manifest_path> --environment <pixi_environment> ...`.
   - Classify heavy commands and repeated full-matrix checks in `## Resource Check Plan`, and design bounded real-path variants that still exercise the requested command path.
   - For every heavy per-agent cwd command, consult `isomer-misc-bounded-run-tips` first for an applicable subcommand or recipe. If one matches, apply the selected guidance and record the skill/subcommand as the bounded-run guidance source. If none matches, write an explicit generic best-effort bounded plan that balances useful verification against host crash prevention while still exercising the source-agent cwd path.
5. **Preserve cwd assumptions** from the topic env gate:
   - If a topic env command is topic-root-only or repo-specific and cannot run from an Agent Workspace cwd, record `gate-cwd-incompatible` or an equivalent blocker instead of false readiness.
6. **Write or update the fixed Markdown template** from **Template**:
   - Write at the resolved `topic.env.agent_setup_target_spec` path when deriving from source intent.
   - When using an explicit manual target spec, record the explicit source and normalized target-spec copy or reference, then preserve every required section.
   - Use Markdown checkboxes in the generated gate file for every required predecessor item, worktree item, semantic path check, projection visibility check, resource check, verification matrix command, expected-result comparison, and blocker-resolution item that must be done or checked before readiness can be declared.
   - Keep optional diagnostics and supporting smoke checks outside `## Gate Checklist` unless they are required per-agent readiness work.
7. **Initialize or update the execution log**:
   - Include requester, confirmation source, optional Service Request refs, support Artifact refs, Provenance refs, changed files, commands run, blockers, and `Not run yet.` for verification commands that have not been executed.
8. **Report target spec metadata** and any blockers that prevent topic-main predecessor consumption, projection predecessor consumption, worktree creation, or verification.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step derivation plan from the source intent or explicit target spec, topic env predecessor, agent plan evidence, parent guardrails, and user request, then execute the plan.

## Template

```markdown
# Isomer Agent Environment Gate

## Source Agent Gate

## Gate Checklist

## Topic Env Gate

## Topic Pixi Binding

## Topic Main Development Repository Predecessor

## Agent Plan

## Semantic Paths

## Worktree Plan

## Verification Matrix

## Resource Check Plan

## Expected Results

## Blockers

## Execution Log
```

## Section Guidance

### Source Agent Gate

- Summarize `topic.intent.agent_env_requirements`.
- Cite the resolved source gate path.
- Name the explicit target spec source when the service was invoked manually.

### Gate Checklist

- Treat `## Gate Checklist` as the required per-agent readiness work contract, not a progress decoration. Every item in this section is required for the relevant per-agent readiness status, and full-matrix items are required for `overall_readiness_status: ready`.
- Use Markdown checkboxes for required actionable gate work: `- [ ]` before work runs and `- [x]` only after evidence exists.
- Include predecessor checks, worktree checks, semantic path checks, projection visibility checks, resource probes, bounded real-path verification commands, expected-result checks, and blocker-resolution items.
- For each required checklist item, state the pass condition, evidence source, bounded-run guidance source when heavy, affected Agent Name or matrix scope, and blocker condition either in the item text or in the matching `## Verification Matrix`, `## Expected Results`, `## Resource Check Plan`, `## Blockers`, or `## Execution Log` entry.
- Keep optional diagnostics and supporting smoke checks outside `## Gate Checklist`; if a smoke check is included in the checklist, its item text must make clear that only the smoke check is required.
- Keep unchecked items visible when they are blocked, unsafe, partial, or not yet run; explain the reason in `## Blockers` or `## Execution Log`.
- Do not mark all-agent readiness complete from selected-agent partial evidence.
- Do not mark a checkbox complete because a weaker smoke test passed unless the checkbox itself was only for that smoke test, or the user explicitly records a downgrade from the original critical-path item.

### Topic Env Gate

- Reference `topic.env.topic_setup_target_spec` as Topic Workspace predecessor evidence.
- State the predecessor readiness status and any relevant blockers.
- Keep topic-root success as prerequisite evidence only; it is not Agent Workspace cwd readiness.

### Topic Pixi Binding

- Record `manifest_path_or_dir`.
- Record `manifest_path`.
- Record `pixi_environment`.
- Record binding source and diagnostics when relevant.

### Topic Main Development Repository Predecessor

- Record required `topic.repos.main` predecessor evidence.
- Record required projection predecessor evidence from `topic.repos.main.projections.manifest`.
- Name the repair route to `isomer-srv-topic-env-setup` when evidence is missing, stale, or blocked.
- Do not ask agent env setup to create, initialize, configure, or repair topic-main.

### Agent Plan

- List authoritative Agent Names.
- List source role ids.
- List branch plan.
- List selected-agent partial scope when present.
- Include corroborating operator map evidence when available.

### Semantic Paths

- List `topic.repos.main`, `topic.repos.main.isomer_managed`, `topic.repos.main.projections.readonly`, `topic.repos.main.projections.writable`, `topic.repos.main.projections.manifest`, and `topic.agents_root`.
- List `agent.workspace` for every authoritative Agent Name.
- List required agent support labels.
- Include path sources and blockers.

### Worktree Plan

- List expected `per-agent/<agent-name>/main` branches.
- List resolved `agent.workspace` worktree paths.
- State whether each worktree will be created, reused, repaired by a blocker route, or left untouched.

### Verification Matrix

- List each Agent Name, source requirement, cwd, exact Pixi command, and expected result.
- Use `pixi run --manifest-path <manifest_path> --environment <pixi_environment> ...`.
- For heavy commands, selected-agent partial coverage or bounded inputs are allowed, but the command must still exercise the source-agent required path and align with the `## Resource Check Plan` guidance source.

### Resource Check Plan

- Classify each per-agent verification command as light or heavy.
- Treat compilation, deep model inference, full dataset download, large archive extraction, broad test suites, multi-process training, and large GPU jobs as heavy.
- For every heavy command, consult `isomer-misc-bounded-run-tips` before writing local generic guidance.
- When a bounded-run tips subcommand applies, record the matched skill/subcommand, selected lightweight probes, capacity signals, limits, bounded real-path command, affected Agent Name scope, expected result, and blocker condition.
- When no bounded-run tips subcommand applies, record the source as generic best-effort judgment, then name probes, capacity signals, limits, bounded real-path command, affected Agent Name scope, expected result, and blocker condition.
- Call out commands whose cost multiplies across every authoritative Agent Workspace.
- Prefer selected-agent partial coverage, fewer build jobs, selected build targets, tiny model or tensor shapes, sample data, reduced iterations, reduced batch size, selected tests, and short benchmark cases unless the user explicitly requires the full expensive matrix and resources are clearly idle.
- Do not accept a simple smoke test that misses the requested cwd command path as readiness evidence.

Example for per-agent CUDA cwd verification:

- Intent says: every planned Agent Workspace cwd must be able to build the baseline kernel and run a baseline benchmark.
- Good action: verify one selected authoritative Agent Name first when full-matrix cost is high; run from that agent's `agent.workspace`; use `nvidia-smi`; compile only the host architecture; cap build parallelism with `MAX_JOBS=1`; build a selected extension or kernel target; run a tiny benchmark case; label this as selected-agent partial evidence until every required Agent Name passes.
- Bad action: mark all agents ready after only checking that `torch.cuda.is_available()` works from one cwd.
- If the bounded selected-agent check cannot run safely: mark the selected agent blocked with resource evidence and the exact command to retry later.

### Expected Results

- State pass/fail criteria for each matrix command.
- State expected files, outputs, metrics, device visibility, projection visibility, or command output snippets.
- State when selected-agent partial evidence is insufficient for `overall_readiness_status: ready`.
- For heavy items, include the expected evidence that the bounded real-path command exercised the source-agent cwd command path, not merely a supporting smoke check.

### Blockers

- List missing predecessor evidence, missing source gate, agent-plan-conflict, unsafe path, out-of-scope source gate request, gate-cwd-incompatible command, or unresolved setup ambiguity.
- List insufficient resource capacity when a bounded real-path check cannot run safely.
- Keep selected-agent partial evidence separate from all-agent readiness.

### Execution Log

- Record direct Project Operator Session invocation, mutation confirmation, optional Service Request, support Artifact, or Provenance refs.
- Preserve resource check evidence, bounded real-path execution decisions, changed files, commands run, verification results, partial scope, and blockers.
- Do not claim verification has run before `verify-agent-env-gate`.

## Guardrails

- Do not create per-agent dependency plans, reinterpret Topic Workspace dependency policy, or ask this service to repair topic-main/projection predecessors.
- Do not use tmp paths as durable readiness evidence.
- Do not claim verification has run before `verify-agent-env-gate`.
- Do not create Workspace Runtime records or Agent Team Instance records.
