# GPU Analytical Modeling User Plugin

This project-local user-plugin provides User Skill Callback material for GPU kernel analytical modeling. It keeps GPU modeling preferences under `skillset/user-plugins/gpu-analytical-modeling/`; it is not part of the packaged Isomer distribution and does not install itself.

## Contents

- `manifest.toml`: Declarative install recipe for desired User Skill Callback registrations. It is not the installed callback registry.
- `gpu-modeling-method/`: Callback skill for source priority, analytical model shape, and baseline evidence classes.
- `gpu-evidence-and-experiment/`: Callback skill for evaluation contracts, NCU evidence, component bottleneck proof, and model-refinement decisions.
- `gpu-reporting-and-closure/`: Callback skill for claim gates, math writing, and closure limits.
- `prompts/`: Short prompt-file callback material for narrow reminders.

## Manifest Role

The manifest describes the callbacks this plugin expects an operator or future installer to register. Current activation is still explicit:

```bash
pixi run isomer-cli --print-json project skill-callbacks register \
  --topic <topic-id> \
  --id gpu-modeling-method.scout.begin \
  --skill isomer-deepsci-scout \
  --stage begin \
  --skill-dir skillset/user-plugins/gpu-analytical-modeling/gpu-modeling-method
```

The installed registry remains under `.isomer-labs/user-skill-callbacks/.../registry.toml` after registration.

## Recommended Targets

| Plugin source | Recommended target stages | Use |
| --- | --- | --- |
| `gpu-modeling-method` | `isomer-deepsci-scout:begin/end`, `isomer-deepsci-baseline:begin`, `isomer-deepsci-idea:begin`, `isomer-deepsci-analysis:begin` | Shape sources, equations, assumptions, and baseline classes before model work hardens. |
| `gpu-evidence-and-experiment` | `isomer-deepsci-experiment:begin/end`, `isomer-deepsci-analysis:end`, `isomer-deepsci-review:begin`, `isomer-deepsci-decision:begin`, `isomer-deepsci-pipeline:begin` | Keep experiments falsifiable and route mismatches honestly. |
| `gpu-reporting-and-closure` | `isomer-deepsci-write:end`, `isomer-deepsci-review:end`, `isomer-deepsci-finalize:begin/end` | Keep user-facing claims, notation, and closure decisions aligned with evidence. |
| `prompts/ncu-command-posture.md` | `isomer-deepsci-experiment:begin` | Narrow reminder for Pixi and NCU command posture. |
| `prompts/no-emulator-overclaim.md` | `isomer-deepsci-write:end` | Narrow reminder to separate proxy evidence from real-hardware evidence. |

## Source Types

Manifest callback entries support the same source families as `project skill-callbacks register`: `skill_dir`, `prompt_file`, and `prompt`. Each entry should provide exactly one matching source field.

Use `skill_dir` for durable multi-step guidance, `prompt_file` for reusable short reminders, and inline `prompt` only for tiny static instructions.

## Scope Guidance

Prefer topic-scoped registration for a specific GPU kernel modeling topic:

```bash
pixi run isomer-cli --print-json project skill-callbacks register \
  --topic <topic-id> \
  --id gpu-evidence.experiment.begin \
  --skill isomer-deepsci-experiment \
  --stage begin \
  --scope research_topic \
  --skill-dir skillset/user-plugins/gpu-analytical-modeling/gpu-evidence-and-experiment
```

Use project-scoped registration only when GPU analytical modeling is a project-wide default:

```bash
pixi run isomer-cli --print-json project skill-callbacks register \
  --scope project \
  --id gpu-reporting.finalize.begin \
  --skill isomer-deepsci-finalize \
  --stage begin \
  --skill-dir skillset/user-plugins/gpu-analytical-modeling/gpu-reporting-and-closure
```

Prompt-file callbacks use the same registration surface with `--prompt-file`:

```bash
pixi run isomer-cli --print-json project skill-callbacks register \
  --scope project \
  --id gpu-reporting.no-emulator-overclaim.write.end \
  --skill isomer-deepsci-write \
  --stage end \
  --prompt-file skillset/user-plugins/gpu-analytical-modeling/prompts/no-emulator-overclaim.md
```

## Boundaries

These callback sources are supplemental instructions. They cannot override the owning DeepSci skill, `isomer-deepsci-shared`, system or developer instructions, the current user request, evidence gates, validation, recording obligations, or Isomer domain constraints.
