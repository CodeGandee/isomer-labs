## Context

`skillset/toolboxes/gpu-analytical-modeling/manifest.toml` currently registers broad domain skills such as `gpu-reference-map`, `gpu-modeling-method`, `gpu-evidence-and-experiment`, and `gpu-reporting-and-closure` across many DeepSci callback stages. The callback runtime is stage-oriented, but the Toolbox directory is knowledge-area-oriented, so the installed behavior is hard to inspect: an operator can see that a source-map skill is injected, but not which stage prior and subcommand should affect the agent.

The user clarified that installed Toolbox skills are discoverable by name after installation. Callback prompt files can therefore tell the active DeepSci agent to invoke a named `gpu-analytic-{stage}-prior` skill and subcommand for a specific purpose.

## Goals / Non-Goals

**Goals:**

- Make the Toolbox layout reflect when priors take effect: scout, idea, baseline, analysis, experiment, review, decision, pipeline, write, and finalize.
- Make each callback prompt explicit about the prior skill, subcommand, and purpose to invoke.
- Preserve existing GPU analytical-modeling source, model, evidence, and reporting guidance in stage-prior subcommands.
- Keep the Toolbox project-local and generic to GPU kernel analytical modeling.

**Non-Goals:**

- Do not change callback resolver behavior, Toolbox manifest schema, CLI commands, or installed registry storage.
- Do not make the Toolbox topic-specific or bind it to a particular GPU SKU, kernel, host, artifact path, or paper workflow.
- Do not duplicate complete guidance inside callback prompts.

## Decisions

### Use stage-prior skill names

Create prior skills named `gpu-analytic-{stage}-prior`, such as `gpu-analytic-scout-prior`, `gpu-analytic-experiment-prior`, and `gpu-analytic-write-prior`. This makes installed skill names describe the stage they guide, while subcommands describe the exact prior being applied.

Alternative considered: keep broad domain skills and rename only callback keys. That would improve the manifest slightly, but agents would still receive broad skills and infer stage-specific behavior.

### Use prompt-file callbacks as routing prompts

Change callback entries to `source_type = "prompt_file"` and route each callback through a small prompt that says `Invoke <skill> subcommand <subcommand>. Purpose: <purpose>.` The prompt is the bridge from a DeepSci insertion point to a discoverable installed prior skill.

Alternative considered: register prior directories directly with `source_type = "skill_dir"`. That loads the right skill, but it does not pin the callback to a subcommand and purpose as clearly.

### Keep prior content concise and reusable

Move the existing command guidance into stage-prior subcommands, combining related source, model, evidence, and reporting content where the same stage uses them together. Each stage-prior `SKILL.md` should be short: overview, when to use, workflow, subcommands, and common mistakes only where useful.

Alternative considered: create one skill per callback entry. That would make each callback explicit, but it would multiply skill directories and repeat shared stage context.

### Preserve Toolbox identity

Keep `toolbox_id = "gpu-analytical-modeling"` and the canonical package path. The restructure changes authoring shape and callback source text, not the durable Toolbox identity.

## Risks / Trade-offs

- Prompt routing depends on installed skill discovery by name. Mitigation: every callback prompt names the exact prior skill and subcommand, and README documents the assumption.
- Splitting by stage can duplicate some source-boundary concepts across priors. Mitigation: keep duplicated text brief and stage-specific instead of recreating the full source taxonomy everywhere.
- Removing old broad skill directories may break manual references to their names. Mitigation: update README and manifest so the supported names are visible at the package root.

## Migration Plan

1. Create `gpu-analytic-{stage}-prior` skill directories with subcommands that preserve the existing guidance.
2. Create `callbacks/` prompt files that invoke a prior skill and subcommand for each manifest callback.
3. Replace `skill_dir` manifest entries with `prompt_file` entries using stage/purpose keys.
4. Update the README content and recommended target table.
5. Remove old broad domain skill directories and obsolete prompt files after equivalent stage-prior callbacks exist.
