## 1. Prepare and Audit

- [x] 1.1 Confirm the guardrails and troubleshooting-guide standards in `imsight-agent-skill-handling/references/create.md` are current.
- [x] 1.2 Run a grep across `extern/orphan/houmao-agents/skillset/imsight-skills/` to identify every `## Common Mistakes` section and every skill with both `## Guardrails` and `## Common Mistakes`.
- [x] 1.3 For each affected skill, classify existing `Common Mistakes` bullets as guardrail intent, troubleshooting intent, or obsolete.

## 2. Merge Dual-Section Skills

- [x] 2.1 Merge `## Guardrails` and `## Common Mistakes` in `imsight-autodev-master/SKILL.md` into a single `## Guardrails` section using "DO NOT ..." and "MUST ..." rules, moving recovery guidance to `## Troubleshooting Guide`.
- [x] 2.2 Merge `## Guardrails` and `## Common Mistakes` in `imsight-autodev-slave/SKILL.md` into a single `## Guardrails` section using "DO NOT ..." and "MUST ..." rules, moving recovery guidance to `## Troubleshooting Guide`.

## 3. Convert Common Mistakes to Guardrails

- [x] 3.1 Convert `## Common Mistakes` to `## Guardrails` in `imsight-dev-box-init/SKILL.md`.
- [x] 3.2 Convert `## Common Mistakes` to `## Guardrails` in `imsight-dev-box-network/SKILL.md`.
- [x] 3.3 Convert `## Common Mistakes` to `## Guardrails` in `imsight-doc-writing/SKILL.md`.
- [x] 3.4 Convert `## Common Mistakes` to `## Guardrails` in `imsight-info-gathering/SKILL.md`.
- [x] 3.5 Convert `## Common Mistakes` to `## Guardrails` in `imsight-llm-wiki/SKILL.md`.
- [x] 3.6 Convert `## Common Mistakes` to `## Guardrails` in `imsight-project-automation/SKILL.md`.
- [x] 3.7 Convert `## Common Mistakes` to `## Guardrails` in `imsight-project-design/SKILL.md`.
- [x] 3.8 Convert `## Common Mistakes` to `## Guardrails` in `imsight-project-explore/SKILL.md`.
- [x] 3.9 Convert `## Common Mistakes` to `## Guardrails` in `imsight-project-mgr/SKILL.md`.
- [x] 3.10 Convert `## Common Mistakes` to `## Guardrails` in `imsight-project-misc/SKILL.md`.

## 4. Add or Update Troubleshooting Guides

- [x] 4.1 Add or update `## Troubleshooting Guide` in skills where classified `Common Mistakes` bullets describe recoverable execution problems.
- [x] 4.2 Ensure each troubleshooting entry uses exactly two bullet levels: first-level problem, second-level "If <problem>, then <action>." solution.

## 5. Validate

- [x] 5.1 Grep the skillset to confirm zero `## Common Mistakes` headings remain.
- [x] 5.2 Review each updated `## Guardrails` section to confirm every bullet starts with "DO NOT" or "MUST", the list is sparse, and each rule protects the skill's design intent.
- [x] 5.3 Review each `## Troubleshooting Guide` section to confirm it uses exactly two levels, contains only skill-specific execution problems, avoids universal common-sense advice, and does not restate guardrails or workflow steps.
