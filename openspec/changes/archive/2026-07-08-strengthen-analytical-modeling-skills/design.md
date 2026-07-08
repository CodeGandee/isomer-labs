## Context

The project-local `gpu-analytical-modeling` user plugin already contains three callback skill groups: modeling method, evidence and experiment, and reporting and closure. It covers broad mistakes such as black-box fitting, evidence-class confusion, coarse bottleneck labels, and claim overreach.

Prior topic chatlog analysis shows a remaining analytical-modeling weakness. Agents need stronger guidance for the definition of the model itself: an analytical model should be an interpretable hardware model whose parameters have physical meaning, whose equations map workload inputs through internal hardware components and execution paths, and whose bottleneck predictions can be checked against observed bottleneck evidence. The existing `model-shape.md` mentions execution stages and equations but does not make these requirements concrete enough to prevent coarse bandwidth-style or fitted models from being accepted as sufficient.

## Goals / Non-Goals

**Goals:**

- Strengthen the existing project-local user-plugin skills so a GPU analytical model must be interpretable as hardware modeling, not merely prediction.
- Make physical-meaning parameters, hardware internal components, execution path, bottleneck formation, and observation-vs-prediction verification first-class guidance.
- Make hardware component graph, per-hop data movement, operation ordering, overlap/serialization, closed-form or bounded analytical terms, and probabilistic stochastic terms supporting guidance.
- Preserve existing plugin structure and source-type manifest semantics.
- Keep all implementation changes under `skillset/user-plugins/gpu-analytical-modeling/`.
- Keep instructions generic to GPU kernel analytical modeling rather than tying them to a specific kernel, GPU SKU, paper, topic workspace, host, or environment setup.

**Non-Goals:**

- Do not add packaged system skills or modify distribution assets.
- Do not modify User Skill Callback registry behavior, installer behavior, CLI commands, or runtime loading.
- Do not add cross-host, Pixi environment, proxy, or remote execution guidance.
- Do not implement an actual GPU model, profiler harness, paper pipeline, or simulator.
- Do not make AccelSim or any simulator an execution dependency.

## Decisions

1. **Strengthen `gpu-modeling-method` rather than adding another top-level skill.**

The gap is in the definition of an acceptable analytical model. Keeping the change inside `gpu-modeling-method` avoids expanding the plugin surface and matches the current grouping by purpose.

Alternative considered: add a fourth skill such as `gpu-execution-flow-model`. This would make the concept visible, but it would increase callback count and split model-shape guidance across two entrances.

2. **Add a dedicated hardware-model contract page or equivalent section.**

The model-shape command should gain concrete, executable guidance for physical parameters, hardware components, execution paths, data slicing, transfer edges, per-stage equations, overlap/serialization rules, stochastic terms, bottleneck selection rules, and verification expectations. This may be implemented as a new `commands/hardware-model-contract.md` or `commands/execution-flow-model.md` linked from `SKILL.md`, or as a substantial section in `model-shape.md` if that remains clearer.

Alternative considered: only edit existing bullet points in `model-shape.md`. That is too easy for future agents to skim past; the chatlog shows the need for stronger, named guidance about what counts as hardware-grounded analytical modeling.

3. **Make physical interpretability a model-quality gate.**

The strengthened guidance should reject anonymous factors and fitted parameters unless each one has a physical meaning, unit or dimension, source or calibration role, allowed range, and effect on a named hardware component or execution path.

Alternative considered: treat interpretability as a reporting concern. That is too late; parameter meaning determines whether the model is analytical at all.

4. **Keep closed-form preference as a model-quality gate, not an absolute ban.**

The strengthened guidance should prefer closed-form or bounded analytical expressions, but allow small recurrence, expectation, or piecewise terms when they are named, bounded, and justified. This captures mini-simulator-style reasoning without requiring a full event-driven simulator.

Alternative considered: require every model term to be closed form. That would reject useful probabilistic, queueing, and recurrence-based analytical terms that still satisfy the topic's spirit.

5. **Tie bottleneck claims to observation-vs-prediction checks.**

The strengthened guidance should say that a model claiming bottleneck insight needs predicted saturated component/path outputs plus a plan to compare those predictions with observed bottleneck evidence. Runtime accuracy alone does not verify the model's bottleneck explanation.

Alternative considered: leave this only to the evidence skill. The modeling skill still needs to require bottleneck outputs and selection rules up front so the evidence skill has something concrete to test.

6. **Treat simulator sources as modeling references.**

`source-map.md` already says simulator sources are architectural references, not direct truth. The strengthened analytical guidance should reinforce this at model-shape time: simulator concepts may inform component graphs and scheduling abstractions, but target-GPU parameters and claims still need source, measurement, or explicit assumption boundaries.

Alternative considered: remove simulator references entirely. That would discard useful modeling structure such as queues, schedulers, issue slots, memory partitions, and dependency paths.

## Risks / Trade-offs

- **Risk: Guidance becomes too verbose for callbacks.** → Mitigation: keep `SKILL.md` concise and move detailed execution-flow checks into a command page.
- **Risk: Agents treat mini-simulator language as permission to build a full simulator.** → Mitigation: state that the desired shape is analytical and bounded, not an event-driven simulator or executable simulator dependency.
- **Risk: The strengthened guidance drifts into experiment or paper-writing concerns.** → Mitigation: keep model-shape guidance focused on structure, equations, component/path outputs, and source boundaries; leave evidence and reporting details in the existing skill groups.
- **Risk: Topic-specific lessons leak into generic plugin text.** → Mitigation: use GPU-kernel language and examples such as tensor cores, shared memory, L2, HBM, scheduler partitions, and synchronization paths without requiring any specific kernel, GPU SKU, host, topic path, paper artifact, or environment setup.

## Migration Plan

Implementation should update the plugin files in place. No runtime migration is required because the plugin is project-local text consumed by callbacks.

Rollback is a normal file revert of the touched plugin files and change artifacts.

## Open Questions

No user decision is currently required. During implementation, choose between a new command page and an expanded `model-shape.md` based on which keeps the entrance skill concise and the command workflow actionable.
