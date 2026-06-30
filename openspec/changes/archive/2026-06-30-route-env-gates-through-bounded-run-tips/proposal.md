## Why

Environment gate generation already requires bounded real-path checks for heavy work, but the routing rule is uneven: CUDA topic gates mention `isomer-misc-bounded-run-tips`, while agent gates and non-CUDA heavy work rely on local judgment. This lets derived gates invent ad hoc resource plans, miss available package-specific bounded-run guidance, or under-specify why a heavy path is safe enough to run.

## What Changes

- Require topic env gate derivation to consult `isomer-misc-bounded-run-tips` first for every heavy setup or verification item before writing the `Resource Check Plan`.
- Require agent env gate derivation to use the same bounded-run-first rule for every heavy per-agent cwd verification item, including selected-agent partial checks.
- Require generated gates to record whether a heavy-operation plan came from a matching bounded-run tips subcommand or from explicit generic best-effort judgment when no matching subcommand exists.
- Require install and verify steps to enforce the generated bounded-run plan instead of substituting unrelated smoke tests or silently reinterpreting heavy commands.
- Keep CUDA/NVIDIA package and runtime setup routing separate: bounded-run tips own resource-safe execution choices, while NVIDIA tools own CUDA/C++ Pixi environment and runtime wiring.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `isomer-service-env-setup-skill`: Topic env gate derivation, installation, and verification must use bounded-run tips as the first routing surface for heavy operations.
- `isomer-agent-env-setup-service-skill`: Agent env gate derivation and verification must use bounded-run tips as the first routing surface for heavy per-agent cwd operations.
- `isomer-service-env-setup-enclosure`: The shared enclosure policy must define bounded-run-first planning as part of heavy-operation safety, not only CUDA compile routing.

## Impact

- Affects `skillset/service/isomer-srv-topic-env-setup` reference pages for derived gate generation, dependency installation, and verification.
- Affects `skillset/service/isomer-srv-agent-env-setup` reference pages for derived gate generation and verification.
- Affects operator-facing validation expectations where topic team specialization consumes service output that includes resource check status and bounded real-path decisions.
- Affects OpenSpec requirements and tests that validate skill text around heavy-operation env gate generation.
