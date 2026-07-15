## 1. Prepare and Audit

- [x] 1.1 Confirm the guardrails and troubleshooting-guide standards in `imsight-agent-skill-handling/references/create.md` are current.
- [x] 1.2 Run a grep across `extern/orphan/houmao-agents/skillset/imsight-skills/` to identify every sub-page `## Common Mistakes` section and every sub-page `## Guardrails` section that does not use strict `DO NOT ...` / `MUST ...` bullets.
- [x] 1.3 For each affected sub-page, classify existing `Common Mistakes` bullets as guardrail intent, troubleshooting intent, or obsolete.

## 2. Convert Common Mistakes in Agent Skill Handling

- [x] 2.1 Convert `## Common Mistakes` to `## Guardrails` in `imsight-agent-skill-handling/references/refactor-migrate.md`.

## 3. Convert Common Mistakes in LLM Wiki Commands

- [x] 3.1 Convert `## Common Mistakes` to `## Guardrails` in `imsight-llm-wiki/commands/audit.md`.
- [x] 3.2 Convert `## Common Mistakes` to `## Guardrails` in `imsight-llm-wiki/commands/collect.md`.
- [x] 3.3 Convert `## Common Mistakes` to `## Guardrails` in `imsight-llm-wiki/commands/compile.md`.
- [x] 3.4 Convert `## Common Mistakes` to `## Guardrails` in `imsight-llm-wiki/commands/deploy-viewer.md`.
- [x] 3.5 Convert `## Common Mistakes` to `## Guardrails` in `imsight-llm-wiki/commands/ingest.md`.
- [x] 3.6 Convert `## Common Mistakes` to `## Guardrails` in `imsight-llm-wiki/commands/inventory.md`.
- [x] 3.7 Convert `## Common Mistakes` to `## Guardrails` in `imsight-llm-wiki/commands/lint.md`.
- [x] 3.8 Convert `## Common Mistakes` to `## Guardrails` in `imsight-llm-wiki/commands/project.md`.
- [x] 3.9 Convert `## Common Mistakes` to `## Guardrails` in `imsight-llm-wiki/commands/query.md`.
- [x] 3.10 Convert `## Common Mistakes` to `## Guardrails` in `imsight-llm-wiki/commands/research.md`.
- [x] 3.11 Convert `## Common Mistakes` to `## Guardrails` in `imsight-llm-wiki/commands/scaffold.md`.
- [x] 3.12 Convert `## Common Mistakes` to `## Guardrails` in `imsight-llm-wiki/org/src/SKILL.md`.

## 4. Normalize Existing Guardrails in Autodev Master

- [x] 4.1 Normalize `## Guardrails` bullets to `DO NOT ...` / `MUST ...` in `imsight-autodev-master/commands/invocations/raw-openspec/apply-change.md`.
- [x] 4.2 Normalize `## Guardrails` bullets to `DO NOT ...` / `MUST ...` in `imsight-autodev-master/commands/invocations/raw-openspec/archive-change.md`.
- [x] 4.3 Normalize `## Guardrails` bullets to `DO NOT ...` / `MUST ...` in `imsight-autodev-master/commands/invocations/raw-openspec/explore.md`.
- [x] 4.4 Normalize `## Guardrails` bullets to `DO NOT ...` / `MUST ...` in `imsight-autodev-master/commands/invocations/raw-openspec/propose.md`.
- [x] 4.5 Normalize `## Guardrails` bullets to `DO NOT ...` / `MUST ...` in `imsight-autodev-master/commands/invocations/raw-openspec/sync-specs.md`.
- [x] 4.6 Normalize `## Guardrails` bullets to `DO NOT ...` / `MUST ...` in `imsight-autodev-master/commands/invocations/slave-skill/init-openspec.md`.
- [x] 4.7 Normalize `## Guardrails` bullets to `DO NOT ...` / `MUST ...` in `imsight-autodev-master/commands/invocations/slave-skill/openspec-one-pass.md`.
- [x] 4.8 Normalize `## Guardrails` bullets to `DO NOT ...` / `MUST ...` in `imsight-autodev-master/commands/workflows/bounded-openspec-phase.md`.
- [x] 4.9 Normalize `## Guardrails` bullets to `DO NOT ...` / `MUST ...` in `imsight-autodev-master/commands/workflows/continue-existing-change.md`.
- [x] 4.10 Normalize `## Guardrails` bullets to `DO NOT ...` / `MUST ...` in `imsight-autodev-master/commands/workflows/delegated-openspec-lifecycle.md`.
- [x] 4.11 Normalize `## Guardrails` bullets to `DO NOT ...` / `MUST ...` in `imsight-autodev-master/commands/workflows/prepare-slave-for-openspec.md`.
- [x] 4.12 Normalize `## Guardrails` bullets to `DO NOT ...` / `MUST ...` in `imsight-autodev-master/commands/workflows/recover-or-finalize-change.md`.
- [x] 4.13 Normalize `## Guardrails` bullets to `DO NOT ...` / `MUST ...` in `imsight-autodev-master/references/primitives/deliver-to-slave.md`.
- [x] 4.14 Normalize `## Guardrails` bullets to `DO NOT ...` / `MUST ...` in `imsight-autodev-master/references/primitives/inspect-slave.md`.

## 5. Normalize Existing Guardrails in Autodev Slave and Other Skills

- [x] 5.1 Normalize `## Guardrails` bullets to `DO NOT ...` / `MUST ...` in `imsight-autodev-slave/commands/init-openspec.md`.
- [x] 5.2 Normalize `## Guardrails` bullets to `DO NOT ...` / `MUST ...` in `imsight-autodev-slave/commands/openspec-one-pass.md`.
- [x] 5.3 Normalize `## Guardrails` bullets to `DO NOT ...` / `MUST ...` in `imsight-info-gathering/commands/find-libgen.md`.
- [x] 5.4 Normalize `## Guardrails` bullets to `DO NOT ...` / `MUST ...` in `imsight-project-automation/commands/openspec-one-pass.md`.
- [x] 5.5 Normalize `## Guardrails` bullets to `DO NOT ...` / `MUST ...` in `imsight-project-automation/commands/openspec-test-and-fix.md`.
- [x] 5.6 Normalize `## Guardrails` bullets to `DO NOT ...` / `MUST ...` in `imsight-project-mgr/commands/impl-in-worktree.md`.

## 6. Add or Update Troubleshooting Guides in Sub-Pages

- [x] 6.1 Add or update `## Troubleshooting Guide` in sub-pages where classified `Common Mistakes` bullets describe recoverable execution problems.
- [x] 6.2 Ensure each sub-page troubleshooting entry uses exactly two bullet levels: first-level problem, second-level "If <problem>, then <action>." solution.

## 7. Validate

- [x] 7.1 Grep all sub-pages to confirm zero `## Common Mistakes` headings remain.
- [x] 7.2 Review each updated sub-page `## Guardrails` section to confirm every bullet starts with "DO NOT" or "MUST", the list is sparse, and each rule protects the page's design intent.
- [x] 7.3 Review each sub-page `## Troubleshooting Guide` section to confirm it uses exactly two levels, contains only skill-specific execution problems, avoids universal common-sense advice, and does not restate guardrails or workflow steps.
