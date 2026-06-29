## 1. Narrow Topic Env Setup Boundary

- [x] 1.1 Update `skillset/service/isomer-srv-topic-env-setup/SKILL.md` so the overview, output contract, guardrails, and help text define readiness as Topic Workspace predecessor evidence only.
- [x] 1.2 Update `skillset/service/isomer-srv-topic-env-setup/references/setup-topic-env.md` so the full workflow stops at Topic Workspace readiness and reports per-agent readiness as not checked rather than routed by the topic env setup skill.
- [x] 1.3 Update `skillset/service/isomer-srv-topic-env-setup/references/verify-env-gate.md` so direct verification cannot imply downstream Agent Workspace readiness and does not call or route to agent env setup.
- [x] 1.4 Update `skillset/service/isomer-srv-topic-env-setup/references/derive-env-gate.md` so later Agent Workspace cwd assumptions are preserved as source context only, not as topic env setup responsibility.

## 2. Strengthen Agent Env Setup Ownership

- [x] 2.1 Review `skillset/service/isomer-srv-agent-env-setup/SKILL.md` and references to ensure they clearly own `agent-env-gate.md`, `isomer-agent-env-gate.md`, per-Agent Workspace cwd verification, selected-agent partial evidence, and overall agent readiness.
- [x] 2.2 Update `require-topic-env-ready.md` wording so it consumes Topic Workspace predecessor evidence and routes missing or stale dependency repair back to `isomer-srv-topic-env-setup` without implying topic env setup owns downstream readiness.
- [x] 2.3 Update `derive-agent-env-gate.md` and `verify-agent-env-gate.md` wording where needed so topic-root readiness is prerequisite evidence only and every requested Agent Workspace cwd must be verified by agent env setup.

## 3. Route Supporting Policy to Existing Skills

- [x] 3.1 Update topic env setup dependency and enclosure text so package repository, mirror, registry, and channel reachability decisions reference `isomer-srv-resolve-pkg-repo` when source choice is not fixed by existing evidence.
- [x] 3.2 Update topic env setup CUDA/NVIDIA wording so architecture targets, CUDA/C++ build environment preferences, and build parallelism decisions reference `isomer-misc-nvidia-tools` instead of expanding topic env setup into a general NVIDIA guide.
- [x] 3.3 Keep necessary selected package source, NVIDIA channel, enclosure, and external runtime wiring evidence in `isomer-env-gate.md` output requirements.

## 4. Update Operator Orchestration Docs

- [x] 4.1 Update `skillset/operator/isomer-admin-topic-team-specialize/SKILL.md` and relevant reference pages so `setup-topic-env` delegates only Topic Workspace setup and `setup-agent-workspace` delegates per-agent readiness only after source agent gate, topic env predecessor, and Git topology evidence exist.
- [x] 4.2 Update `skillset/operator/isomer-admin-topic-workspace-mgr/` docs so Git topology remains separate from Agent Workspace environment readiness and any agent env setup call is caller-requested after validated topology.
- [x] 4.3 Update `skillset/service/README.md` and `skillset/operator/README.md` to describe the narrowed responsibilities and orchestration paths.

## 5. Update Call Graph and Acceptance Evidence

- [x] 5.1 Update `skillset/callgraph.md` so it removes the `isomer-srv-topic-env-setup` to `isomer-srv-agent-env-setup` call path and keeps the repair path from agent env setup back to topic env setup.
- [x] 5.2 Update the Calling Conditions table to distinguish Topic Workspace predecessor evidence from Agent Workspace cwd readiness evidence.
- [x] 5.3 Search the inspected skillset for stale language such as topic env setup "routes per-agent verification" and revise matches that imply ownership rather than next action reporting.

## 6. Validate

- [x] 6.1 Run `openspec validate refactor-topic-env-skill-boundary --strict` and fix any proposal, design, spec, or task validation errors.
- [x] 6.2 Run the relevant skill validation command for edited service and operator skills, or document why no validator is available.
- [x] 6.3 Run `pixi run test` or the narrowest relevant unit tests if validation changes touch tested skillset behavior.
- [x] 6.4 Review `skillset/callgraph.md` after edits to confirm the graph matches the new ownership model.
