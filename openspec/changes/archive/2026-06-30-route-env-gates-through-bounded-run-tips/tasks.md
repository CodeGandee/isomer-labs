## 1. Topic Env Setup Skill

- [x] 1.1 Update `skillset/service/isomer-srv-topic-env-setup/references/derive-env-gate.md` so every heavy setup or verification item consults `isomer-misc-bounded-run-tips` before generic bounded-run judgment.
- [x] 1.2 Update topic gate section guidance so `## Resource Check Plan`, `## Gate Checklist`, `## Verification Commands`, and `## Expected Results` record the bounded-run guidance source, probes, limits, command, expected result, and blocker condition.
- [x] 1.3 Update `install-topic-deps.md` and `verify-env-gate.md` so they enforce the generated bounded-run plan and block missing, ambiguous, unsafe, or smoke-test-only heavy checks.

## 2. Agent Env Setup Skill

- [x] 2.1 Update `skillset/service/isomer-srv-agent-env-setup/references/derive-agent-env-gate.md` so every heavy per-agent cwd verification item consults `isomer-misc-bounded-run-tips` before generic bounded-run judgment.
- [x] 2.2 Update agent gate section guidance so selected-agent partial checks record the bounded-run guidance source, affected Agent Name scope, probes, limits, command, expected result, and blocker condition.
- [x] 2.3 Update `verify-agent-env-gate.md` so it enforces the generated bounded-run plan and never marks all agents ready from unrelated smoke tests or selected-agent partial evidence.

## 3. Shared Policy and Validation

- [x] 3.1 Update shared enclosure and service specs so bounded-run-first routing is captured in mainline OpenSpec requirements after implementation.
- [x] 3.2 Add or revise repository validation tests that inspect the topic env setup and agent env setup skill text for bounded-run-first routing, explicit generic fallback wording, and readiness enforcement.
- [x] 3.3 Validate affected skills with skill quick validation where applicable and run the relevant repo validation commands.
- [x] 3.4 Run `openspec validate route-env-gates-through-bounded-run-tips --strict` and fix any artifact or scenario-format issues.
