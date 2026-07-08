## Context

The project-local `gpu-analytical-modeling` user plugin already contains `gpu-evidence-and-experiment` for evaluation contracts, NCU evidence, component bottleneck proof, and mismatch routing, plus `gpu-reporting-and-closure` for claim gating and proof placement. Recent chatlog analysis and follow-up discussion narrowed the experimentation gap to three generic requirements: bottleneck predictions need matching hard observations, analytical latency models need predicted-versus-measured latency checks, and final papers or reports need to show the hard evidence.

The change should not preserve topic-specific details from the source chatlog as general plugin law. Details such as one named kernel, one GPU SKU, one command wrapper, one host setup, one venue, or one artifact path belong in topic records, not reusable callback guidance.

## Goals / Non-Goals

**Goals:**

- Strengthen the existing experimentation skill so bottleneck-oriented claims require a targeted experiment that stresses one predicted component or path and collects hard evidence for the observation.
- Strengthen the evaluation contract so any analytical model that predicts latency compares predicted latency against measured latency before making latency-accuracy claims.
- Strengthen reporting and closure guidance so final papers and reports surface the evidence packet for central runtime, saturated-component, and blocking-path claims.
- Keep guidance generic to GPU kernel analytical modeling and project-local under `skillset/user-plugins/gpu-analytical-modeling/`.

**Non-Goals:**

- Do not add a new top-level skill group.
- Do not add packaged system skills or modify callback registry, installer, CLI, or runtime behavior.
- Do not add benchmark runners, profiler wrappers, command recipes, cross-host setup rules, or environment-specific troubleshooting as general guidance.
- Do not implement a GPU model, run experiments, collect profiler data, or rewrite a paper.
- Do not encode topic-specific names, hardware SKUs, venue templates, workspace paths, or artifact locations in generic plugin text.

## Decisions

1. **Strengthen existing skill groups rather than adding another entrance.**

The three gates belong to the current purpose split. `gpu-evidence-and-experiment` owns experiment design and interpretation, while `gpu-reporting-and-closure` owns final paper/report visibility. Adding a new top-level skill would make callback selection noisier without adding a distinct purpose.

Alternative considered: add a new `gpu-experiment-gates` skill. This would make the concept visible, but it would duplicate `evaluation-contract` and `component-bottleneck-proof`.

2. **Express the change as gates in existing command pages.**

Implementation should update `evaluation-contract.md`, `component-bottleneck-proof.md`, and reporting closure or claim-gate guidance. `evaluation-contract.md` should carry the predicted-versus-measured latency gate. `component-bottleneck-proof.md` should carry the one-component or one-path saturation experiment gate. Reporting guidance should carry the final hard-evidence visibility gate.

Alternative considered: create a new command page such as `experiment-gates.md`. This may be useful if implementation finds the existing pages too crowded, but the default should be fewer command pages because the concepts already map cleanly to current pages.

3. **Define hard evidence by role, not by one tool.**

Hard evidence should mean measured latency plus observations that can support or refute the component/path claim: raw counters, derived counter mappings, instruction mix, dependency-path evidence, microbenchmark behavior, measured timings, or an explicit evidence gap. The guidance can mention profiler counters generically, but it should not require one profiler, counter set, command wrapper, or target GPU.

Alternative considered: make NCU the required evidence source. That is too narrow for generic GPU kernel analytical modeling and would turn a topic-specific preference into universal law.

4. **Require visible evidence in final reports without prescribing paper layout.**

The final output must show the evidence packet for central claims, but the generic plugin should not require a specific section, appendix, table number, or venue format. The reusable requirement is visibility and auditability, not layout.

Alternative considered: prescribe a fixed appendix/main-section workflow. That was useful in the source topic but does not generalize.

## Risks / Trade-offs

- **Risk: Guidance becomes too weak if "hard evidence" stays vague.** → Mitigation: require named inputs, predicted latency, measured latency, predicted component/path, observed evidence, metric or observation values when available, mapping rationale, and match/mismatch interpretation.
- **Risk: Guidance becomes too strict for early-stage work.** → Mitigation: allow explicit evidence gaps, downgraded claims, or routing back to experiment rather than demanding that every draft already has final proof.
- **Risk: Topic-specific details creep back into generic plugin text.** → Mitigation: validate changed plugin files for specific kernel names, GPU SKUs, workspace paths, cross-host setup, command wrappers, paper venues, and artifact paths.

## Migration Plan

Implementation should update the plugin Markdown files in place. No runtime migration is required because the plugin is project-local text consumed by callbacks.

Rollback is a normal file revert of the touched plugin files and change artifacts.

## Open Questions

No user decision is currently required. During implementation, prefer updating existing command pages unless the text becomes clearer with one small command page linked from the existing skill.
