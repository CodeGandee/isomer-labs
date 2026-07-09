# GPU Analytical Modeling Toolbox

This project-local Toolbox provides stage-specific User Skill Callback priors for GPU kernel analytical modeling. It keeps GPU modeling preferences under `skillset/toolboxes/gpu-analytical-modeling/`; it is not part of the packaged Isomer distribution and does not install itself.

## Contents

- `manifest.toml`: Declarative install recipe for stage-prior callback registrations.
- `callbacks/`: Short prompt-file callbacks that invoke an installed prior skill, subcommand, and purpose.
- `gpu-analytic-*-prior/`: Installed prior skills organized by DeepSci stage.

## Prompt Routing Contract

The Toolbox assumes that after installation the prior skills are discoverable by name in the agent skillset. Each callback prompt uses the same compact shape:

```md
Invoke `gpu-analytic-<stage>-prior` subcommand `<subcommand>`.

Purpose: <why this prior is injected at this insertion point>.

Treat this as supplemental prior guidance under the active DeepSci skill, project context, and user request.
```

This makes `manifest.toml` the readable map of what takes effect and when, while the stage-prior skill directory keeps the reusable guidance.

## Manifest Role

The manifest describes the callbacks this Toolbox expects an operator to install through the high-level Toolbox bundle path. The top-level `toolbox_id` is the stable Toolbox identity, and each callback has a toolbox-local `key`. Installed callback ids use `<toolbox_id>:<key>`, such as `gpu-analytical-modeling:experiment/begin/evaluation-and-profiler-contract`.

Install the Toolbox for one Research Topic with:

```bash
pixi run isomer-cli --print-json project toolboxes install \
  --topic <topic-id> \
  --toolbox-dir skillset/toolboxes/gpu-analytical-modeling
```

The installed registry remains under `.isomer-labs/user-skill-callbacks/.../registry.toml` after registration.

Callback `key` values contain only letters, digits, `-`, `_`, and `/`. Use `/` for naming hierarchy only; it does not imply filesystem paths or ordering dependencies. Ordering is guaranteed only inside this Toolbox, by ascending Python string comparison of toolbox-local keys. Cross-Toolbox ordering is deterministic implementation detail and should not be used as a design contract.

## Stage-Prior Map

| Callback target | Prompt invokes | Use |
| --- | --- | --- |
| `isomer-deepsci-scout:begin` | `gpu-analytic-scout-prior framing-prior` | Classify source families, early model-shape needs, simulator-structure boundaries, and evidence gaps. |
| `isomer-deepsci-scout:end` | `gpu-analytic-scout-prior output-check` | Check scout outputs for source families, model-shape expectations, evidence classes, and unresolved gaps. |
| `isomer-deepsci-idea:begin` | `gpu-analytic-idea-prior hypothesis-model-contract` | Ground GPU model hypotheses in source needs, hardware components, physical parameters, equations, assumptions, and evidence targets. |
| `isomer-deepsci-baseline:begin` | `gpu-analytic-baseline-prior evidence-baseline-contract` | Separate analytical, roofline, simulator, emulator, microbenchmark, profiler-counter, and real-hardware timing evidence classes. |
| `isomer-deepsci-analysis:begin` | `gpu-analytic-analysis-prior hardware-grounded-interpretation` | Ground interpretation in named components, execution paths, evidence classes, and source limits. |
| `isomer-deepsci-analysis:end` | `gpu-analytic-analysis-prior component-proof-check` | Check component/path bottleneck claims against matching observations, mismatch classes, and honest routes. |
| `isomer-deepsci-experiment:begin` | `gpu-analytic-experiment-prior evaluation-and-profiler-contract` | Shape evaluation metrics, data roles, profiler or NCU collection posture, component stressors, and claim-to-evidence mapping. |
| `isomer-deepsci-experiment:end` | `gpu-analytic-experiment-prior result-evidence-check` | Classify results by evidence class and prevent proxy evidence from becoming measured-hardware accuracy. |
| `isomer-deepsci-review:begin` | `gpu-analytic-review-prior source-and-evidence-review` | Map central claims to source families, evidence classes, source limits, and provenance gaps. |
| `isomer-deepsci-review:end` | `gpu-analytic-review-prior claim-strength-review` | Classify central claims by support level and make proof visibility or downgrade reasons explicit. |
| `isomer-deepsci-decision:begin` | `gpu-analytic-decision-prior mismatch-route` | Classify model/evidence mismatches and choose the next honest route. |
| `isomer-deepsci-pipeline:begin` | `gpu-analytic-pipeline-prior evidence-route` | Choose the next DeepSci route based on the weakest missing modeling evidence or source support. |
| `isomer-deepsci-write:end` | `gpu-analytic-write-prior claim-and-proxy-check` | Check claim strength, mathematical notation, and proxy-evidence wording. |
| `isomer-deepsci-finalize:begin` | `gpu-analytic-finalize-prior closure-readiness` | Decide whether central claims are publishable, limited, parked, deferred, routed back, or blocked. |
| `isomer-deepsci-finalize:end` | `gpu-analytic-finalize-prior final-evidence-class` | Classify every central runtime, counter-trend, saturated-component, and blocking-path claim by evidence class. |

## Source Types

The manifest uses `prompt_file` for every callback. Prompt files are intentionally short because they only route the active agent to a discoverable installed prior skill and subcommand. The durable guidance lives in `gpu-analytic-*-prior/`.

## Scope Guidance

Prefer Research Topic installation for a specific GPU kernel modeling topic:

```bash
pixi run isomer-cli --print-json project toolboxes install \
  --topic <topic-id> \
  --scope research_topic \
  --toolbox-dir skillset/toolboxes/gpu-analytical-modeling
```

Use project-scoped installation only when GPU analytical modeling is a project-wide default:

```bash
pixi run isomer-cli --print-json project toolboxes install \
  --scope project \
  --toolbox-dir skillset/toolboxes/gpu-analytical-modeling
```

Manual one-off callbacks can still use the lower-level registration surface with explicit installed ids. `project skill-callbacks install --toolbox-dir` remains available as a callback refresh or repair primitive for an existing Toolbox manifest, but it is not the normal Toolbox bundle install path.

## Boundaries

These callback sources are supplemental instructions. They cannot override the owning DeepSci skill, `isomer-deepsci-shared`, system or developer instructions, the current user request, evidence gates, validation, recording obligations, or Isomer domain constraints.
