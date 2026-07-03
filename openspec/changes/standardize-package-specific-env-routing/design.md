## Context

Isomer now has three environment-related surfaces that can touch named packages:

- `isomer-srv-topic-env-setup` derives and materializes the topic-level operational env gate, including dependency plans, Pixi install commands, runtime wiring, and verification commands.
- `isomer-admin-topic-mgr env-*` handles ad hoc package install, update, remove, and package verification requests for initialized Topic Workspaces.
- `isomer-srv-agent-env-setup` derives and verifies per-Agent Workspace cwd readiness from topic-level predecessor evidence, while avoiding duplicate topic dependency planning.

The package-specific caveat registry, `isomer-misc-pkg-specifics`, already exists and currently contains PyTorch guidance. The current service guidance mentions it in topic env derivation, but the rule is not consistently expressed across ad hoc package mutation, update/removal, or agent cwd verification. This leaves a gap where a generic PyPI-first or Conda/Pixi-first choice can outrun package-specific requirements such as CPU/GPU variants, CUDA compatibility, Flash Attention build caveats, or runtime metadata checks.

## Goals / Non-Goals

**Goals:**

- Make `isomer-misc-pkg-specifics` the first lookup for named package decisions that affect operational env gates, package mutation, or package-specific runtime readiness.
- Keep operational topic env derivation centralized in `isomer-srv-topic-env-setup`.
- Keep operational agent cwd env derivation centralized in `isomer-srv-agent-env-setup`.
- Ensure `isomer-admin-topic-mgr env-*` uses the same package-specific-first rule for ad hoc package mutation.
- Record `no package-specific rule` as explicit evidence when a named package is not in the registry, then continue with generic package routing.

**Non-Goals:**

- Do not make operator skills derive operational env target specs.
- Do not make every research or operator skill load package-specific pages before writing high-level env intent.
- Do not make `isomer-srv-agent-env-setup` duplicate topic-level dependency planning.
- Do not route package setup through `isomer-misc-tool-packs`; that skill remains manual-only.
- Do not create a package database beyond the current skill-reference structure.

## Decisions

1. Package-specific lookup is mandatory at operational decision points.

   Any skill deriving an operational env gate, mutating named packages, or verifying package-specific runtime readiness should check `isomer-misc-pkg-specifics` before generic source and verification rules. If the registry has no matching page, the caller records `no package-specific rule` and proceeds with its generic policy.

   Alternative considered: have high-level source-intent writers consult package specifics first. That would leak package-source decisions into operator intent surfaces and make Topic Creator or Topic Team Specialize responsible for details that belong in service setup.

2. Topic env setup remains the owner for topic-level operational dependency planning.

   `isomer-srv-topic-env-setup derive-env-gate` should turn `topic.intent.topic_env_requirements` into `topic.env.topic_setup_target_spec`. During that derivation, it should consult package-specific guidance for every named package before writing install commands, source choices, variant expectations, verification commands, or blockers.

   Alternative considered: make every caller route to `isomer-misc-pkg-specifics` directly before invoking topic env setup. That would duplicate routing logic and make the service less authoritative.

3. Topic Manager env mutation uses the same package-specific-first rule.

   Ad hoc install/update/remove requests do not go through full gate derivation. They still choose package sources and verification checks, so they need the same registry preflight. Update and removal should consider package-specific caveats because changing or removing a package can break variants or runtime expectations.

   Alternative considered: route ad hoc package mutation back through full topic env setup. That would be too heavy for simple "install matplotlib" requests and would blur the existing Topic Manager package-mutation surface.

4. Agent env setup consumes topic dependency planning but can use package-specific runtime caveats.

   `isomer-srv-agent-env-setup` should not invent dependency plans when `topic.env.topic_setup_target_spec` is missing or stale. It should route repair back to `isomer-srv-topic-env-setup`. When a per-agent cwd verification matrix depends on a named package's runtime behavior, it should use package-specific verification expectations as supporting evidence.

   Alternative considered: let agent env setup derive missing package install steps. That creates two dependency planners and risks divergence from the topic env gate.

5. Validation should check the rule at the guidance level.

   The implementation should add validation terms and tests that reject generic package-source ladders that omit the package-specific-first lookup at operational decision points.

## Risks / Trade-offs

- [Risk] The package-specific skill is small and may not list most packages. → Mitigation: missing entries return `no package-specific rule` and generic routing continues with explicit evidence.
- [Risk] Callers may overuse package-specific lookup for ordinary packages with no caveats. → Mitigation: only require lookup for named package decisions at operational decision points, not for broad conceptual source intent.
- [Risk] Ad hoc package mutation and full gate setup can diverge. → Mitigation: both surfaces must use the same package-specific-first rule and record selected evidence.
- [Risk] Agent env setup could start duplicating dependency planning. → Mitigation: require it to route missing or stale topic dependency planning back to `isomer-srv-topic-env-setup`.
- [Risk] Validation may become brittle if it checks exact prose. → Mitigation: validate durable terms and route relationships rather than sentence-level wording.
