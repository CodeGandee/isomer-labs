# GPU Analytical Modeling Toolbox

This project-local toolbox provides User Skill Callback material for GPU kernel analytical modeling. It keeps GPU modeling preferences under `skillset/toolboxes/gpu-analytical-modeling/`; it is not part of the packaged Isomer distribution and does not install itself.

## Contents

- `manifest.toml`: Declarative install recipe for desired User Skill Callback registrations. It is not the installed callback registry.
- `gpu-reference-map/`: Callback skill for source families, source limits, and source-to-claim mapping.
- `gpu-modeling-method/`: Callback skill for analytical model shape, hardware contract, and baseline evidence classes.
- `gpu-evidence-and-experiment/`: Callback skill for evaluation contracts, profiler/counter evidence, component bottleneck proof, and model-refinement decisions.
- `gpu-reporting-and-closure/`: Callback skill for claim gates, math writing, and closure limits.
- `prompts/`: Short prompt-file callback material for narrow reminders.

## Manifest Role

The manifest describes the callbacks this Toolbox expects an operator to install. The top-level `toolbox_id` is the stable Toolbox identity, and each callback has a toolbox-local `key`. Installed callback ids use `<toolbox_id>:<key>`, such as `gpu-analytical-modeling:gpu-modeling-method/scout/begin`.

Install topic-scoped callbacks with:

```bash
pixi run isomer-cli --print-json project skill-callbacks install \
  --topic <topic-id> \
  --toolbox-dir skillset/toolboxes/gpu-analytical-modeling
```

The installed registry remains under `.isomer-labs/user-skill-callbacks/.../registry.toml` after registration.

Callback `key` values contain only letters, digits, `-`, `_`, and `/`. Use `/` for naming hierarchy only; it does not imply filesystem paths or ordering dependencies. If a callback omits `key`, Isomer derives `<target_skill>/<stage>`. A Toolbox cannot contain two unlabeled callbacks for the same target skill and stage because they would derive the same toolbox-local key.

Ordering is guaranteed only inside this Toolbox, by ascending Python string comparison of toolbox-local keys. Cross-Toolbox ordering is deterministic implementation detail and should not be used as a design contract.

## Recommended Targets

| Toolbox source | Recommended target stages | Use |
| --- | --- | --- |
| `gpu-reference-map` | `isomer-deepsci-scout:begin/end`, `isomer-deepsci-baseline:begin`, `isomer-deepsci-idea:begin`, `isomer-deepsci-analysis:begin`, `isomer-deepsci-experiment:begin`, `isomer-deepsci-review:begin` | Choose source families, source limits, and source-to-claim evidence boundaries before operational work hardens. |
| `gpu-modeling-method` | `isomer-deepsci-scout:begin/end`, `isomer-deepsci-baseline:begin`, `isomer-deepsci-idea:begin`, `isomer-deepsci-analysis:begin` | Shape equations, assumptions, hardware contracts, and baseline classes before model work hardens. |
| `gpu-evidence-and-experiment` | `isomer-deepsci-experiment:begin/end`, `isomer-deepsci-analysis:end`, `isomer-deepsci-review:begin`, `isomer-deepsci-decision:begin`, `isomer-deepsci-pipeline:begin` | Keep experiments falsifiable and route mismatches honestly. |
| `gpu-reporting-and-closure` | `isomer-deepsci-write:end`, `isomer-deepsci-review:end`, `isomer-deepsci-finalize:begin/end` | Keep user-facing claims, notation, and closure decisions aligned with evidence. |
| `prompts/ncu-command-posture.md` | `isomer-deepsci-experiment:begin` | Narrow reminder for Pixi and NCU command posture. |
| `prompts/no-emulator-overclaim.md` | `isomer-deepsci-write:end` | Narrow reminder to separate proxy evidence from real-hardware evidence. |

## Source Types

Manifest callback entries support the same source families as `project skill-callbacks register`: `skill_dir`, `prompt_file`, and `prompt`. Each entry should provide exactly one matching source field.

Use `skill_dir` for durable multi-step guidance, `prompt_file` for reusable short reminders, and inline `prompt` only for tiny static instructions.

## Scope Guidance

Prefer topic-scoped installation for a specific GPU kernel modeling topic:

```bash
pixi run isomer-cli --print-json project skill-callbacks install \
  --topic <topic-id> \
  --scope research_topic \
  --toolbox-dir skillset/toolboxes/gpu-analytical-modeling
```

Use project-scoped installation only when GPU analytical modeling is a project-wide default:

```bash
pixi run isomer-cli --print-json project skill-callbacks install \
  --scope project \
  --toolbox-dir skillset/toolboxes/gpu-analytical-modeling
```

Manual one-off callbacks can still use the lower-level registration surface with explicit installed ids:

```bash
pixi run isomer-cli --print-json project skill-callbacks register \
  --scope project \
  --id gpu-analytical-modeling:manual/no-emulator-overclaim/write/end \
  --skill isomer-deepsci-write \
  --stage end \
  --prompt-file skillset/toolboxes/gpu-analytical-modeling/prompts/no-emulator-overclaim.md
```

## Boundaries

These callback sources are supplemental instructions. They cannot override the owning DeepSci skill, `isomer-deepsci-shared`, system or developer instructions, the current user request, evidence gates, validation, recording obligations, or Isomer domain constraints.
