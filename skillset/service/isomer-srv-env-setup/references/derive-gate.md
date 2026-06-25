# Derive Gate

Use this subcommand to generate the operational environment gate from the source gate and repo evidence.

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Require predecessor artifacts**: workspace context from `resolve-workspace`, source gate summary from `read-gate`, and repo context from `get-repos` when the source gate needs repos.
2. **Resolve the derived gate path** as `<topic-workspace-dir>/user-intent/derived/isomer-env-gate.md` and create its parent directory when needed.
3. **Translate user intent into operations**. Convert the source gate and repo evidence into concrete repo requirements, dependency plan, Pixi install commands, verification commands, expected results, and blockers.
4. **Apply dependency policy**. Include Python as the Topic Workspace glue language, prefer PyPI for Python packages unless Pixi/Conda is required for the gate, use Pixi/Conda for native tools and binary/runtime dependencies, and prefer the `nvidia` channel for NVIDIA tools.
5. **Write the fixed Markdown template** from **Template**. Include every section; write `None.` or a short reason when a section does not apply.
6. **Warning-label inferred repos** in `## Inferred Source Warnings` and carry the same warnings to the final skill output.
7. **Report `derived_gate_path`** and any blockers that prevent installation or verification.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the source gate, repo evidence, dependency policy, parent guardrails, and user request, then execute the plan.

## Template

```markdown
# Isomer Environment Gate

## Source Intent

## Runnable Target

## Repo Requirements

## Inferred Source Warnings

## Dependency Plan

## Pixi Install Commands

## Verification Commands

## Expected Results

## Blockers

## Execution Log
```

## Section Guidance

`## Source Intent` should summarize the user-authored source gate and cite `<topic-workspace-dir>/user-intent/src/env-gate.md`.

`## Runnable Target` should name the desired command or behavior that must work after setup.

`## Repo Requirements` should list repo names, paths under `repos/<repo-name>`, sources, and inspection notes.

`## Inferred Source Warnings` should list inferred repo sources and the reason each was chosen. Use `None.` only when no repo source was inferred.

`## Dependency Plan` should list Python glue baseline, PyPI dependencies, Pixi/Conda dependencies, native toolchains, NVIDIA channel decisions, editable installs, and why any Python package uses Pixi/Conda instead of PyPI.

`## Pixi Install Commands` should list the concrete commands the agent will run from the Topic Workspace root or with `--manifest-path <manifest_path>`.

`## Verification Commands` should list the exact Pixi commands that prove the runnable target works.

`## Expected Results` should state pass/fail criteria and expected outputs.

`## Blockers` should list missing repos, missing dependencies, ambiguous commands, unavailable packages, unsupported live-agent actions, or other reasons readiness cannot be claimed.

`## Execution Log` should be initialized as `Not run yet.` before `install-deps` or `verify-gate`, then updated by those subcommands when they run commands.
