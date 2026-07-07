# Review of Skill Generality

## Summary

The GPU analytical modeling user-plugin is broadly aligned with its intended purpose: it captures general methodology for GPU kernel analytical modeling rather than flash-attention-specific implementation details. The strongest coverage is in hardware-grounded model shape, interpretable physical parameters, execution-path modeling, evidence-class separation, predicted-versus-measured latency gates, bottleneck observation evidence, and final evidence visibility. I found no direct leakage of the flash-attention topic name, B200 SKU, topic workspace paths, FlashAttention repository paths, or fixed paper layout from `isomer-content/topic-ws/flash-attention-4-whitebox-runtime-model` into the core skill instructions.

The main generality risks are operational rather than conceptual: the plugin includes Pixi-specific NCU command posture, host or remote-node recording, and an NCU-centered profiler protocol. Those details may be useful for the current Isomer environment, but they are less general than the GPU analytical modeling principles the plugin otherwise expresses.

## Project Owner Response

Pixi usage is acceptable in this plugin because Pixi is a required dependency of the Isomer Labs system. Pixi-specific command posture should be read as project-system context, not as topic-specific leakage from the flash-attention workspace.

## Coverage Assessment

The plugin covers the requested modeling principles well. `gpu-modeling-method/commands/hardware-model-contract.md` requires model claims, hardware component graphs, physical parameter inventories, execution paths, per-stage equations, data movement, bottleneck selection rules, validity limits, and observation checks. `gpu-modeling-method/commands/model-shape.md` reinforces inputs, outputs, units, bounded analytical expressions, aggregation logic, calibration bounds, and validity limits.

The evidence path is also strong. `gpu-evidence-and-experiment/commands/evaluation-contract.md` requires metrics, calibration and validation separation, fair comparison rules, predicted latency, measured latency, workload and hardware scope, metric definitions, and evidence classes. `gpu-evidence-and-experiment/commands/component-bottleneck-proof.md` requires stressors, observed component/path evidence, predicted and measured runtime, raw observations, evidence mapping rationale, and match or miss interpretation.

The reporting and closure path covers final evidence visibility. `gpu-reporting-and-closure/commands/claim-gate.md` asks for central claims, evidence classes, evidence sources, evidence packets, and overclaim downgrades. `gpu-reporting-and-closure/commands/closure-limits.md` requires final papers, reports, and closure summaries to show inputs, predictions, measured latency, observed bottleneck evidence, mapping rationale, and match or mismatch interpretation without prescribing a fixed section or layout.

Under-covered general principles are measurement uncertainty and model sensitivity. The plugin mentions run count, thresholds, bounds, and calibration splits, but it does not consistently require repeated timing distributions, warmup policy, variance/error bars, clock or thermal stability checks, parameter sensitivity analysis, or identifiability checks for calibrated physical terms.

## Generality Assessment

The core skills are appropriately general for GPU kernel analytical modeling. They avoid naming flash attention, a specific kernel implementation, a specific GPU SKU, workspace paths, exact artifact paths, or paper venue layout. The component examples are mostly generic GPU components, and the skills consistently frame simulator, emulator, profiler, microbenchmark, and real-hardware evidence as evidence classes rather than topic-specific tooling.

The plugin is less general at the operational boundary. `prompts/ncu-command-posture.md` and `gpu-evidence-and-experiment/commands/ncu-protocol.md` encode a Pixi/NCU command preference. `manifest.toml` and `README.md` register that prompt as part of the plugin. That turns an environment-specific execution lesson into reusable skill behavior. The NCU-specific guidance is acceptable if this plugin intentionally targets NVIDIA GPU modeling inside Isomer, but it should be labeled as one profiler backend rather than the general profiler protocol for all GPU analytical modeling.

Cross-checking against the flash-attention topic workspace showed that the topic contains likely contamination sources: `isomer-topic-workspace-summary.md` names `flash-attention-4-whitebox-runtime-model`, Pixi setup, B200 host capture, NCU 2025.4.1, and topic paths; `repos/topic-main/host-b200-spec.md` names NVIDIA B200 and a host-local NCU path. The plugin does not copy those names or paths. It only appears to inherit the broader operational pattern of Pixi plus NCU command wrapping.

## Findings

- **Medium: Pixi command posture leaks operational setup into reusable modeling guidance.** `prompts/ncu-command-posture.md:3`, `gpu-evidence-and-experiment/commands/ncu-protocol.md:7`, `README.md:35`, and `manifest.toml:139-145` prefer `pixi run ncu ...` and register that preference as a callback. This is a command-wrapper instruction, not a modeling principle, and it risks making the plugin less portable across non-Pixi projects or teams that run profiling through other launchers.
- **Medium: The profiler protocol is framed as NCU-specific instead of profiler-backend neutral.** `gpu-evidence-and-experiment/SKILL.md:23`, `gpu-evidence-and-experiment/commands/ncu-protocol.md:5-18`, and `gpu-modeling-method/commands/baseline-contract.md:23` center NCU as the profiler evidence path. NCU is a reasonable NVIDIA backend, but the general methodology is raw counters, counter-to-component mapping, failure capture, and claim linkage. The current naming may exclude other profiler stacks or non-NVIDIA GPU modeling work.
- **Low: Host and remote-node recording is useful evidence metadata but smells operational.** `gpu-evidence-and-experiment/commands/ncu-protocol.md:8` asks agents to record host or remote node when relevant. That can support reproducibility, but it sits close to the host/cross-host setup details present in the flash-attention topic workspace. It should remain metadata, not a required modeling concept.
- **Low: Measurement stability and uncertainty are under-specified.** `gpu-evidence-and-experiment/commands/evaluation-contract.md:8-11` defines metrics and predicted-versus-measured latency, and `gpu-evidence-and-experiment/commands/ncu-protocol.md:8` records run count, but the plugin does not require warmup policy, repeated-run distributions, variance, confidence intervals, clock/thermal state, or outlier handling before making latency-accuracy claims.
- **Low: Calibration sensitivity and identifiability are under-specified.** `gpu-modeling-method/commands/model-shape.md:12` requires few, named, bounded, physically interpretable constants, but the plugin does not ask whether calibrated parameters are identifiable, whether multiple parameter settings explain the same latency, or how sensitive bottleneck labels are to those parameters.
- **Low: Reporting language leans toward publication workflows.** `gpu-reporting-and-closure/SKILL.md:24`, `gpu-reporting-and-closure/commands/closure-limits.md:9`, and `gpu-reporting-and-closure/commands/closure-limits.md:19` mention paper, publish, and venue decision. The text avoids fixed layouts, so this is not a major leak, but reusable skill guidance for modeling reports could make publication language optional rather than primary.

## Recommendations

- Keep the core method, evidence, and closure structure; it already expresses the general principles well.
- Move Pixi command-wrapper guidance out of the general plugin path, or label it as an Isomer/Pixi local prompt that should not be registered by default for general GPU modeling.
- Rename or reframe `ncu-protocol` as a profiler-counter protocol with NCU as an example backend, while preserving the valuable raw-counter, mapping, failure, and claim-linkage requirements.
- Add a small measurement-quality gate covering warmup, repetitions, timing distribution, variance/error bars, clock or thermal stability, and outlier policy for measured latency claims.
- Add a calibration-quality gate covering parameter identifiability, sensitivity, and whether bottleneck selection changes under plausible parameter uncertainty.
- Keep publication and venue language subordinate to the more general concept of report, closure record, or user-facing evidence artifact.

## File Notes

- `README.md`: Clear plugin map and registration guidance, but includes Pixi install/register examples and documents the Pixi/NCU command-posture prompt as a recommended target.
- `manifest.toml`: Callback coverage is coherent across scout, baseline, idea, analysis, experiment, review, decision, pipeline, write, and finalize stages. The only generality concern is the registered `gpu-evidence.ncu-command.experiment.begin` prompt with local Pixi/NCU command posture.
- `prompts/ncu-command-posture.md`: The clearest operational leak. It is useful local guidance but not a general GPU analytical modeling principle.
- `prompts/no-emulator-overclaim.md`: Good general reminder; it cleanly separates emulator, simulator, synthetic, analytical-proxy, microbenchmark, profiler-counter, and real-hardware timing evidence.
- `gpu-modeling-method/SKILL.md`: Strong general overview and common mistakes. No topic-specific leakage found.
- `gpu-modeling-method/commands/source-map.md`: Good source-priority guidance. The explicit AccelSim/GPGPU-Sim examples are acceptable as simulator class examples, not topic leakage, though they are NVIDIA/GPGPU-culture specific.
- `gpu-modeling-method/commands/hardware-model-contract.md`: Strongest general methodology file. It captures the hardware-grounded analytical model contract directly.
- `gpu-modeling-method/commands/model-shape.md`: Strong general model-shape guidance. Add sensitivity/identifiability if the skill should cover calibration quality more fully.
- `gpu-modeling-method/commands/baseline-contract.md`: Strong evidence-class separation. NCU is named as one evidence class, which is fine if generalized to profiler-counter evidence.
- `gpu-evidence-and-experiment/SKILL.md`: Strong evidence workflow. It frames predicted-versus-measured latency and bottleneck observations clearly.
- `gpu-evidence-and-experiment/commands/evaluation-contract.md`: Strong latency and evidence gate. Measurement stability is the main missing general principle.
- `gpu-evidence-and-experiment/commands/ncu-protocol.md`: Good profiler-evidence mechanics, but too NCU/Pixi-specific for a fully general plugin.
- `gpu-evidence-and-experiment/commands/component-bottleneck-proof.md`: Strong bottleneck proof contract with useful proof table shape.
- `gpu-evidence-and-experiment/commands/failure-refinement.md`: Good mismatch routing. It could include measurement instability as a mismatch class.
- `gpu-reporting-and-closure/SKILL.md`: Good claim-gating and closure discipline. Publication wording is slightly stronger than necessary for general modeling reports.
- `gpu-reporting-and-closure/commands/claim-gate.md`: Strong evidence-packet requirement and overclaim control.
- `gpu-reporting-and-closure/commands/math-writing.md`: General and useful; no topic-specific leakage found.
- `gpu-reporting-and-closure/commands/closure-limits.md`: Strong final evidence visibility requirement. Publication and venue wording should remain optional language.
