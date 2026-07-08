## 1. Experiment Evidence Gates

- [x] 1.1 Update `gpu-evidence-and-experiment/SKILL.md` so the workflow frames experimentation around evidence gates for predicted-versus-measured latency and bottleneck observation.
- [x] 1.2 Strengthen `gpu-evidence-and-experiment/commands/evaluation-contract.md` so analytical latency or runtime models must report predicted latency, measured latency, workload and hardware scope, metric definition, and evidence class before making latency-accuracy claims.
- [x] 1.3 Strengthen `gpu-evidence-and-experiment/commands/evaluation-contract.md` so emulator, simulator, synthetic, analytical-proxy, or derivation-only evidence cannot substitute for measured latency when claiming measured hardware accuracy.
- [x] 1.4 Strengthen `gpu-evidence-and-experiment/commands/component-bottleneck-proof.md` so bottleneck experiments intentionally stress one predicted component or blocking path at a time when feasible.
- [x] 1.5 Strengthen `gpu-evidence-and-experiment/commands/component-bottleneck-proof.md` so proof records include predicted component/path, intended stressor, observed hard evidence, evidence mapping rationale, match/mismatch interpretation, and explicit gaps.
- [x] 1.6 Update mismatch or evidence routing guidance if needed so missing bottleneck observations or missing measured latency route to more evidence, downgraded claims, explicit limitations, or blockers.

## 2. Final Evidence Visibility

- [x] 2.1 Update `gpu-reporting-and-closure/SKILL.md` so final paper/report/closure guidance requires visible hard evidence for central runtime, saturated-component, and blocking-path claims.
- [x] 2.2 Strengthen `gpu-reporting-and-closure/commands/claim-gate.md` so supported central claims cite or show the evidence packet rather than only naming a conclusion.
- [x] 2.3 Strengthen `gpu-reporting-and-closure/commands/closure-limits.md` so publishable closure is blocked, routed back, or limited when final output omits hard evidence for central claims.
- [x] 2.4 Ensure final-evidence guidance does not prescribe a specific paper section, appendix layout, venue template, artifact path, or topic-specific output location.

## 3. Generic Scope and Plugin Boundaries

- [x] 3.1 Inspect changed plugin guidance to ensure examples stay generic to GPU kernel analytical modeling and do not hard-code a specific kernel, GPU SKU, topic workspace, host setup, command wrapper, profiler command, paper venue, paper artifact, or artifact path.
- [x] 3.2 Verify implementation changes remain under `skillset/user-plugins/gpu-analytical-modeling/` and this change directory, with no packaged system skill, callback registry, CLI/runtime, or distribution manifest changes.
- [x] 3.3 Avoid adding a new top-level skill group unless implementation shows the existing command pages cannot express the gates clearly.

## 4. Validation

- [x] 4.1 Run the available skill validator against `gpu-evidence-and-experiment`.
- [x] 4.2 Run the available skill validator against `gpu-reporting-and-closure`.
- [x] 4.3 Run a structural check that linked command pages in touched skill `SKILL.md` files exist and command-like pages still have numbered `## Workflow` sections with native-planning fallbacks.
- [x] 4.4 Run `openspec validate "strengthen-gpu-experiment-evidence-gates" --type change --strict`.
