## 1. Bounded Run Tips Skill

- [x] 1.1 Update `skillset/misc/isomer-misc-bounded-run-tips/SKILL.md` so it owns operation classification before bounded execution planning.
- [x] 1.2 Add classification output fields for classification source, result, reason, resource dimensions, bounded guidance requirement, and follow-up recipe or generic best-effort handling.
- [x] 1.3 Ensure examples in bounded-run tips are clearly user-tunable guidance rather than an exhaustive fixed heavy-operation list.

## 2. Topic and Agent Env Setup Services

- [x] 2.1 Update topic env setup entrypoint and reference pages so operation classification is delegated to bounded-run tips before resource-check planning.
- [x] 2.2 Update agent env setup entrypoint and reference pages so per-agent cwd operation classification is delegated to bounded-run tips before matrix resource-check planning.
- [x] 2.3 Update install and verify pages so they require classification evidence before enforcing bounded plans and block missing or inconsistent classification evidence.

## 3. Topic Team Specialization Operator

- [x] 3.1 Update topic team specialization guardrails and service-output expectations so the operator consumes classification evidence from delegated services.
- [x] 3.2 Remove or soften fixed normative heavy-operation lists in operator wording, keeping examples only when they are explicitly non-normative.

## 4. Specs and Validation

- [x] 4.1 Add the new mainline `isomer-bounded-run-tips-skill` spec and update mainline env setup, enclosure, and topic-team specs with delegated classification requirements.
- [x] 4.2 Update repository validation tests and fixtures to require delegated classification wording, classification evidence, concise structured skill writing, and absence of core-owned fixed heavy-operation definitions.
- [x] 4.3 Validate affected skills with quick validation where applicable and run relevant repository validation tests.
- [x] 4.4 Run `openspec validate delegate-heavy-operation-classification --strict` and fix any artifact or scenario-format issues.
