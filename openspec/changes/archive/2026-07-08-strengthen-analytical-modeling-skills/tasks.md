## 1. Modeling Method Guidance

- [x] 1.1 Update `gpu-modeling-method/SKILL.md` so the workflow explicitly applies execution-flow analytical model guidance when a model is proposed, accepted, or analyzed.
- [x] 1.2 Add a new `gpu-modeling-method/commands/hardware-model-contract.md` or `gpu-modeling-method/commands/execution-flow-model.md` command page, or equivalently expand `commands/model-shape.md`, to require physical-meaning parameters, hardware component graph, ordered execution stages, per-stage equations, data-movement sequencing, bottleneck selection rules, aggregation rules, assumptions, and validity limits.
- [x] 1.3 If a new command page is added, update the `gpu-modeling-method` subcommand table and workflow links so the command is reachable.
- [x] 1.4 Strengthen `commands/model-shape.md` so outputs include runtime, saturated hardware component, and blocking execution path when those claims are in scope.
- [x] 1.5 Add guidance that an analytical model is not accepted as hardware-grounded unless its parameters are interpretable as physical hardware behavior with units or dimensions, sources or calibration roles, bounds, and named effect on a component or path.

## 2. Analytical Model Shape Details

- [x] 2.1 Add guidance that data movement models must identify what data moves, how it is sliced or batched, which components it traverses, per-hop costs, and which hops overlap or serialize.
- [x] 2.2 Add guidance that aggregation must use explicit max, sum, overlap, queueing, recurrence, or piecewise regime rules rather than prose-only timing claims.
- [x] 2.3 Add guidance that closed-form or bounded analytical expressions are preferred, with recurrence or expectation terms allowed only when named, bounded, and justified.
- [x] 2.4 Add guidance for stochastic effects such as cache misses, contention, scheduling variability, or reuse to use explicit probability, expectation, bound, calibrated parameter, or uncertainty statements.
- [x] 2.5 Add guidance that mini-simulator-style modeling must remain an analytical abstraction and must not become an event-driven simulator or simulator-output dependency.
- [x] 2.6 Add guidance that runtime prediction alone does not prove bottleneck understanding; bottleneck-oriented models must compare predicted component/path against observed bottleneck evidence or record an evidence gap.

## 3. Source and Evidence Boundaries

- [x] 3.1 Strengthen `commands/source-map.md` or linked modeling guidance so simulator projects are architecture/modeling references, not target-hardware truth sources unless separately validated.
- [x] 3.2 Strengthen `commands/baseline-contract.md` if needed so coarse roofline, compute-vs-memory, simulator, and emulator outputs cannot satisfy exact saturated-component or blocking-path claims.
- [x] 3.3 Ensure the guidance remains generic to GPU kernel analytical modeling and does not hard-code any specific kernel, GPU SKU, topic workspace path, cross-host setup, environment handling, proxy/caching, host, paper artifact, or paper-output location.

## 4. Component and Path Selection

- [x] 4.1 Update modeling guidance to require explicit selection rules for saturated hardware component, such as `argmax`, slack, reservation time, active-cycle proxy, or queueing bottleneck.
- [x] 4.2 Update modeling guidance to require explicit selection rules for blocking execution path, such as dependency-chain cost, critical-path rule, or stage-level path comparison.
- [x] 4.3 Ensure coarse compute-bound or memory-bound labels are downgraded to coarse support unless exact component/path equations and evidence are present.
- [x] 4.4 Ensure the guidance asks agents to state what observation would support or refute each predicted bottleneck component or blocking path.

## 5. Validation

- [x] 5.1 Run the available skill validator against `gpu-modeling-method`.
- [x] 5.2 Run a structural check that every linked command page from `gpu-modeling-method/SKILL.md` exists and every command-like page has a numbered `## Workflow` with native-planning fallback.
- [x] 5.3 Inspect changed files for accidental operational guidance about cross-host execution, Pixi environment handling, proxies, caches, or topic-specific paths.
- [x] 5.4 Verify `git status --short` shows no changes under packaged system skill assets, callback registry behavior, CLI/runtime implementation, or distribution manifests caused by this change.
- [x] 5.5 Run `openspec validate "strengthen-analytical-modeling-skills" --type change --strict`.
