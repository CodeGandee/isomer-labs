## 1. Validator Contract

- [x] 1.1 Change packaged-skill Guardrails validation to accept only concise top-level `DO NOT ...` bullets and update the diagnostic text.
- [x] 1.2 Update validator fixtures and unit assertions to cover accepted negative-only Guardrails, rejected `MUST ...` bullets, executable subpages, and excluded historical material.

## 2. Core Operator and Misc Skill Migration

- [x] 2.1 Migrate positive Guardrails in the entrypoint, GUI manager, Project manager, switch-identity commands, system-skill manager, Toolbox manager, and NVIDIA tools by converting prohibitions, removing duplicates, or relocating operational guidance.
- [x] 2.2 Migrate positive Guardrails in Topic Creator and Topic Manager entrypoints and subpages while preserving semantic-path, topology, branch, identity, package, reset, and readiness contracts.
- [x] 2.3 Migrate positive Guardrails in Topic Team Specialization and Welcome entrypoints and subpages while preserving routing, formal-team, evidence, read-only, and output contracts.

## 3. Service Skill Migration

- [x] 3.1 Migrate positive Guardrails in Agent Environment Setup and Topic Environment Setup entrypoints and subpages while preserving operation ordering, semantic labels, Pixi command shapes, bounded-run evidence, and readiness boundaries.
- [x] 3.2 Migrate positive Guardrails in Package Repository Resolution and Topic Service Agent Support while preserving source-selection, audit, lifecycle, and mutation boundaries.

## 4. Active-Scope Semantic Audit

- [x] 4.1 Audit every manifest-declared active Guardrails section, including DeepSci and Kaoju extensions, and relocate positive operation clauses appended to `DO NOT ...` bullets when they act as workflow, routing, evidence, or output instructions.
- [x] 4.2 Confirm active Guardrails contain zero `MUST ...` bullets, every top-level bullet begins with `DO NOT`, and excluded provenance, migration, passive-template, and archived history remain unchanged.

## 5. Validation

- [x] 5.1 Run focused packaged-skill validator tests and `pixi run validate-skills`, then fix all negative-only Guardrails failures.
- [x] 5.2 Run `pixi run lint`, `pixi run typecheck`, `pixi run test`, and strict OpenSpec validation for this change; report any unrelated pre-existing failures without weakening the migration.
