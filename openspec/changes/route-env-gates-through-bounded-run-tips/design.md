## Context

Topic env gates and agent env gates now require bounded real-path verification for heavy work. The service pages already say that compilation, model inference, large downloads, broad test suites, and large GPU jobs must use resource probes and bounded execution rather than risky full-scale runs. The repository also now has `isomer-misc-bounded-run-tips`, which is the right place for concrete recipes such as CUDA compile worker sizing and host GPU architecture selection.

The current boundary is uneven. Topic env derivation routes CUDA compile details to `isomer-misc-bounded-run-tips`, but agent env derivation does not. Non-CUDA heavy operations have no explicit first routing step, so a derived gate can invent a local resource plan without checking whether a more specific bounded-run recipe exists.

## Goals / Non-Goals

**Goals:**

- Make `isomer-misc-bounded-run-tips` the first routing surface for heavy-operation resource strategy during topic env gate and agent env gate generation.
- Preserve the current readiness invariant: a heavy source-intent path must run in bounded real-path form or be blocked with evidence.
- Make the generated gate auditable by recording whether a bounded decision came from a matching bounded-run tips subcommand or from generic best-effort judgment.
- Keep resource-safe execution choices separate from dependency source choice, CUDA runtime wiring, and Pixi enclosure policy.

**Non-Goals:**

- Do not add new bounded-run subcommands in this change.
- Do not change the topic workspace layout, path labels, or readiness status vocabulary.
- Do not make topic env setup responsible for per-agent cwd readiness.
- Do not allow smoke tests to replace source-intent build, inference, dataset, benchmark, or test paths.

## Decisions

1. Use a bounded-run-first lookup before writing `Resource Check Plan`.

   Gate derivation should first classify setup and verification commands as light or heavy. For every heavy command, it should check `isomer-misc-bounded-run-tips` for an applicable subcommand, such as `cuda-compile`. If a match exists, the generated gate should apply that recipe and record the source. If no match exists, the generated gate may use a generic best-effort bounded plan, but it must label the source as generic and explain the probes, limits, command, and blocker condition.

   Alternative considered: keep bounded-run guidance inline inside topic and agent env setup. That would duplicate resource policy and make later bounded-run recipes harder to adopt consistently.

2. Treat generated resource plans as execution contracts.

   `install-topic-deps`, `verify-env-gate`, and `verify-agent-env-gate` should enforce the derived gate's bounded-run plan. They may repair a missing or ambiguous plan by sending the caller back to derivation, but they should not silently replace the plan with a weaker smoke test or an unrecorded full-scale command.

   Alternative considered: let verification reinterpret the source intent each time. That would make readiness less reproducible and weaken the checklist contract.

3. Keep package/runtime routing separate from bounded-run routing.

   `isomer-misc-bounded-run-tips` decides how to run resource-heavy commands safely. Package-specific rules, package repository resolution, CUDA/C++ Pixi environment setup, and NVIDIA runtime wiring remain in their existing skills. For CUDA compile work, the derived gate may mention both surfaces: bounded-run tips for arch and parallelism, NVIDIA tools for environment wiring.

   Alternative considered: route all CUDA-related env gate work to bounded-run tips. That would overload a resource-safety skill with dependency and runtime setup decisions.

## Risks / Trade-offs

- [Risk] Agents may over-route small commands to bounded-run tips and add noise to simple gates. → Mitigation: only commands classified as heavy require the bounded-run-first lookup.
- [Risk] Generic best-effort plans may become vague. → Mitigation: require the gate to record probes, capacity signals, bounded command, expected result, and blocker condition whenever no specific subcommand exists.
- [Risk] Agent env verification can hide all-agent gaps behind selected-agent partial evidence. → Mitigation: selected-agent checks remain partial unless every authoritative Agent Name has passed the required matrix item.
- [Risk] Existing references may still contain local bounded-run prose. → Mitigation: implementation should keep concise local guidance but point resource-specific recipes to `isomer-misc-bounded-run-tips`.
