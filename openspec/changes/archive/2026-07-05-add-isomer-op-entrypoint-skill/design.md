## Context

Isomer currently has several strong owner skills, but no single informed-user entrypoint that can receive a task, prompt, or file and choose the right system surface before acting. `isomer-op-welcome` intentionally stays read-only and menu-like, while `isomer-op-project-mgr`, `isomer-op-topic-creator`, `isomer-op-topic-mgr`, `isomer-op-switch-identity`, and `isomer-op-topic-team-specialize` own concrete operator workflows. Production DeepSci skills live under the extension namespace `research-paradigm/deepsci/` and also need to be reachable when the user asks for research-stage work.

The implementation should preserve the current owner boundaries. The entrypoint should be an index and dispatcher, not a new owner for project setup, topic setup, environment setup, research-stage method, or record storage.

## Goals / Non-Goals

**Goals:**

- Add `isomer-op-entrypoint` as an operator skill for users who already know Isomer and want the agent to route a concrete task to the right system skill or CLI surface.
- Include all system skill families in the entrypoint index: operator, service, misc, and extension skills, with DeepSci extension skills treated as first-class routes.
- Teach a simple workflow: parse task input, inspect safe context, classify route, load the selected reference or owner skill, proceed, and report route/output/blockers.
- Keep service skills as bounded support routes, not normal first-click user routes, unless a user explicitly invokes one.
- Keep `isomer-op-welcome` as the safe read-only orientation surface.
- Add validation so the new skill remains a working dispatcher rather than a stale prose catalog.

**Non-Goals:**

- Do not add new `isomer-cli` commands.
- Do not change DeepSci skill behavior or inventory.
- Do not make the entrypoint own lower-level mutation that belongs to Project Manager, Topic Creator, Topic Manager, Topic Team Specialization, service setup skills, or DeepSci research skills.
- Do not replace direct invocation of specialized skills when the user already names one.

## Decisions

### Add a compact operator skill with reference indexes

Create `src/isomer_labs/assets/system_skills/operator/isomer-op-entrypoint/` with a short `SKILL.md`, `agents/openai.yaml`, and focused reference pages. The main workflow should be the stable control surface; the longer skill and CLI catalogs should live under `references/`.

Alternative considered: extend `isomer-op-welcome`. Rejected because welcome is deliberately read-only, manual-invocation oriented, and optimized for first-time path selection rather than acting on an informed task.

### Route then proceed by default

The entrypoint should choose the best route and continue with that route unless the user asks only for a route explanation, status, or help. This distinguishes it from the welcome skill and makes it useful for prompts such as "use the right Isomer surface to process this file" or "take this topic task forward."

Alternative considered: make it a pure index. Rejected because the user specifically wants the agent to determine the next step and proceed.

### Treat DeepSci as an extension skill family

The entrypoint should include a dedicated `references/extension-skill-index.md` for `isomer-deepsci-*` skills. It should route prepared research-stage work to DeepSci skills, route named pass requests to `isomer-deepsci-pipeline`, route bootstrap readiness work to `isomer-deepsci-workspace-mgr`, and route missing topic/workspace readiness back to operator setup owners.

Alternative considered: keep DeepSci only in research-paradigm documentation. Rejected because the entrypoint is meant to index all system skills and extension skills are part of that system.

### Keep CLI routing shallow and discovery-oriented

The entrypoint should name CLI command families and safe preflight commands, not duplicate every option. It should point agents to `isomer-cli project self queries`, context/path/runtime/project/topic commands, research-record commands, artifact-format commands, handoff commands, and team/profile/instance commands where appropriate.

Alternative considered: maintain a complete CLI manual in the skill. Rejected because CLI help and existing owner skills are already the detailed source of truth, and a duplicated manual would become stale.

### Validate the entrypoint as a contract

Add a validator similar to the welcome and switch-identity module checks. The validator should require frontmatter, manifest metadata, near-top workflow, numbered steps, local references, output contract, "route then proceed" language, active owner-skill routes, extension skill routes, CLI route families, service-skill boundary language, retired-route exclusions, and global `isomer-cli` usage.

Alternative considered: rely on generic skill folder validation. Rejected because the hard part of this skill is routing behavior, not folder structure.

## Risks / Trade-offs

- Stale indexes → Keep `SKILL.md` short, keep route details in named references, and validate required skill/CLI terms.
- Service skills become first-click user routes → Require guardrail text that service skills are bounded support and normal user requests route through owner workflows.
- DeepSci tasks start before workspace readiness → Require extension routing to check topic/workspace readiness and use `isomer-deepsci-workspace-mgr` or operator setup routes first.
- Entrypoint duplicates welcome behavior → State the boundary: welcome is read-only orientation; entrypoint is informed-user routing plus execution.
- Entrypoint mutates too early → Require read-only preflight before ambiguous mutation and only proceed when the task implies action or a selected owner workflow owns the mutation.

## Migration Plan

1. Add the packaged `isomer-op-entrypoint` skill folder with `SKILL.md`, `agents/openai.yaml`, and references.
2. Register `operator/isomer-op-entrypoint` in the core packaged system-skill manifest.
3. Update operator documentation and packaged system-skill README material to list the new operator skill.
4. Extend validation and tests for the new entrypoint module and packaged asset materialization.
5. Run `pixi run lint`, `pixi run typecheck`, and `pixi run test`.

Rollback is simple: remove the skill folder, manifest entry, docs entry, and validator/test additions. No user data or stored records are migrated.

## Open Questions

- Should future work generate parts of the entrypoint index from `manifest.toml` and CLI help to reduce manual maintenance?
- Should direct user invocation of a service skill through the entrypoint be allowed only when the user explicitly names that service skill, or should it also be allowed for narrow support phrasing?
