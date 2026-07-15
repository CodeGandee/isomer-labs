## 1. Establish the Migration Baseline

- [x] 1.1 Re-read the current `imsight-agent-skill-handling` creation, format, style-guide, and layout pages, and record `dbd425f` and `e3673cf` as the old-to-current template transition used for this migration.
- [x] 1.2 Enumerate all 55 active skill roots from every group in `src/isomer_labs/assets/system_skills/manifest.toml` and classify their Markdown pages as entrypoint, executable subpage, behavioral reference, or excluded provenance, migration, or passive-template material.
- [x] 1.3 Reproduce the baseline findings for old headings, duplicate behavioral sections, missing required entrypoint sections, loose Guardrails bullets, and missing executable-workflow fallbacks before editing assets.
- [x] 1.4 Inspect the current working-tree diff for every already modified target, especially `operator/isomer-op-system-skill-mgr`, and preserve those edits as the content baseline for narrow patches.

## 2. Add Current-Template Validation

- [x] 2.1 Add unit fixtures that prove template validation discovers all manifest-declared core and extension skills while excluding `org/`, `migrate/`, and `templates/` material.
- [x] 2.2 Add failing unit cases for entrypoint descriptions, required sections, duplicate or missing Guardrails, old `## Common Mistakes` headings, numbered workflows, and freeform fallbacks.
- [x] 2.3 Add failing unit cases for executable subpage workflows, strict `DO NOT` and `MUST` Guardrails bullets, optional two-level troubleshooting entries, and non-executable explanatory pages.
- [x] 2.4 Implement manifest-aware active-page enumeration in `scripts/validate_skillsets.py` without treating embedded source copies or passive assets as packaged runtime instructions.
- [x] 2.5 Implement file-specific entrypoint, workflow, Guardrails, Common Mistakes, and troubleshooting diagnostics and integrate them into the existing `--scope all` validation path.
- [x] 2.6 Confirm the new validator cases pass against conforming fixtures and fail only the intended malformed active pages.

## 3. Migrate Core Packaged Skills

- [x] 3.1 Review and migrate all four `misc` entrypoints, including the entrypoint with neither Guardrails nor Common Mistakes, while preserving exact invocation boundaries and package-specific guidance.
- [x] 3.2 Review and migrate all 10 `operator` entrypoints, merging the three dual-section skills, completing required entrypoint sections and descriptions, and preserving public subcommands, callback stages, and current uncommitted edits.
- [x] 3.3 Inspect every active operator command and reference page; normalize applicable Guardrails, add missing executable-workflow fallbacks, and leave explanatory pages free of artificial template sections.
- [x] 3.4 Review and migrate all five `service` entrypoints while preserving Service Request authority, Houmao adapter boundaries, environment gates, and manual-only or service-routed trigger constraints.
- [x] 3.5 Inspect every active misc and service subpage; convert old Common Mistakes, normalize existing Guardrails, classify recoverable problems into optional troubleshooting entries, and complete executable workflows.
- [x] 3.6 Run the manifest-aware validator for the core group findings and resolve every current-template diagnostic before continuing.

## 4. Migrate DeepSci Packaged Skills

- [x] 4.1 Review all 22 manifest-declared DeepSci entrypoints and classify every old Common Mistakes bullet as a prohibition, requirement, recoverable problem, or supporting explanation.
- [x] 4.2 Migrate the first half of the DeepSci entrypoints to the current description, Overview, When-to-Use, Workflow, and single-Guardrails contract without changing research-stage behavior or callback insertion points.
- [x] 4.3 Migrate the remaining DeepSci entrypoints to the same contract while preserving artifact, evidence, lineage, placeholder, and Workspace Runtime rules.
- [x] 4.4 Inspect every active DeepSci command, reference, binding, and scenario page for executable-workflow and behavioral-section conformance.
- [x] 4.5 Confirm no DeepSci file under `org/`, `migrate/`, or `templates/` was modified by the migration and that historical wording in those excluded roles does not fail validation.
- [x] 4.6 Run the manifest-aware validator for the DeepSci findings and resolve every current-template diagnostic before continuing.

## 5. Migrate Kaoju Packaged Skills

- [x] 5.1 Review and migrate all 14 manifest-declared Kaoju entrypoints to the current template while preserving survey contracts, artifact bindings, evidence requirements, and pipeline routing.
- [x] 5.2 Convert the nine Kaoju pipeline command pages that use `## Common Mistakes`, classifying behavioral rules separately from recoverable execution problems.
- [x] 5.3 Complete the freeform fallback on every remaining Kaoju executable command page that lacks it without changing the command's ordered workflow.
- [x] 5.4 Inspect every other active Kaoju command, reference, binding, and scenario page and normalize applicable Guardrails and troubleshooting content.
- [x] 5.5 Run the manifest-aware validator for the Kaoju findings and resolve every current-template diagnostic.

## 6. Verify Semantic and Repository Integrity

- [x] 6.1 Confirm all 55 active entrypoints start their description with `Use when`, contain Overview and When-to-Use sections, retain a numbered workflow with a freeform fallback, and contain exactly one strict Guardrails section.
- [x] 6.2 Confirm no active page contains `## Common Mistakes`, every active top-level Guardrails bullet starts with `DO NOT` or `MUST`, and every troubleshooting entry uses the specified two-level problem-and-solution form.
- [x] 6.3 Review the complete asset diff for lost constraints, trigger broadening, renamed subcommands, broken local links, callback drift, output-contract drift, and non-canonical Isomer domain language.
- [x] 6.4 Run `pixi run validate-skills` and the focused validator unit tests.
- [x] 6.5 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test` from the repository root.
- [x] 6.6 Re-run the manifest inventory and report the final active-page counts, excluded-role integrity, validations performed, and any unrelated pre-existing worktree changes left untouched.
