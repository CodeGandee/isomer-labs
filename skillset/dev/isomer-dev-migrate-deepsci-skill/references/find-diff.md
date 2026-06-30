# Find Diff

## Overview

Use `find-diff` after a DeepScientist skill has been migrated into an Isomer Labs skill. This subcommand compares the source skill logic captured under `<target-skill-dir>/org/analysis/` with a fresh clean-context analysis of the migrated skill, then writes logical-difference reports under `<target-skill-dir>/migrate/compare/`.

## Workflow

When `find-diff` is invoked, execute the following steps in order.

1. **Resolve the migrated target skill**. See **Target and Inputs**.
2. **Verify source analysis exists** under `<target-skill-dir>/org/analysis/`. See **Required Inputs**.
3. **Spawn a clean-context subagent** and make it invoke `$imsight-agent-skill-handling deep-inspect` on the migrated skill. See **Migrated Skill Analysis**.
4. **Read the source and migrated analyses**. See **Analysis Inputs**.
5. **Compare logical behavior** and write `<target-skill-dir>/migrate/compare/compare-of-<source-skill-name>.md`. See **Comparison Report**.
6. **Summarize page-level differences** in `<target-skill-dir>/migrate/compare/summary.md`. See **Summary Report**.
7. **Validate and report** generated analysis files, comparison files, coverage gaps, and unresolved differences. See **Validation**.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan using the constraints in this page, then execute the plan.

## Target and Inputs

Use `<target-skill-dir>/...` for paths relative to the migrated target skill directory.

- Source copy: `<target-skill-dir>/org/src/`.
- Source analysis directory: `<target-skill-dir>/org/analysis/`.
- Migrated analysis directory: `<target-skill-dir>/migrate/analysis/`.
- Compare directory: `<target-skill-dir>/migrate/compare/`.
- Migrated analysis output: `<target-skill-dir>/migrate/analysis/analysis-of-<source-skill-name>.md`.
- Logical comparison output: `<target-skill-dir>/migrate/compare/compare-of-<source-skill-name>.md`.
- Page-level summary output: `<target-skill-dir>/migrate/compare/summary.md`.

Derive `<source-skill-name>` from the existing source analysis filename when possible. If multiple source analyses exist, compare each source analysis with the corresponding migrated analysis and write one `compare-of-<source-skill-name>.md` per pair.

## Required Inputs

Before spawning a subagent, confirm these inputs exist:

- `<target-skill-dir>/SKILL.md`.
- `<target-skill-dir>/org/src/`.
- At least one `<target-skill-dir>/org/analysis/analysis-of-<source-skill-name>.md`.
- `<target-skill-dir>/org/README.md`.
- `<target-skill-dir>/migrate/migration-plan.md`.
- `<target-skill-dir>/migrate/placeholders.md`.

If the source analysis is missing, stop and tell the user to run `copy-migrate` or `refactor-migrate` first, or explicitly run the missing source analysis pass.

## Migrated Skill Analysis

Spawn a subagent with clean context, meaning do not fork the current conversation context. If the available subagent tool has a `fork_context` option, set it to false or omit it when false is the default. Give the subagent only the target skill path, this subcommand's task, and the explicit instruction to use `$imsight-agent-skill-handling deep-inspect`.

The subagent must:

- Deep-inspect the migrated skill at `<target-skill-dir>/`.
- Exclude `<target-skill-dir>/org/` from the migrated skill logic analysis.
- Cover all migrated pages outside `org/` that represent skill behavior, including `SKILL.md`, subcommand pages, mode pages, workflow pages, primitive pages, and executable procedure pages.
- Treat `<target-skill-dir>/migrate/` as migration support material, not source skill behavior, unless a migrated skill page explicitly uses it at runtime.
- Write the output to `<target-skill-dir>/migrate/analysis/analysis-of-<source-skill-name>.md`.

The main agent must not reuse its own migration context as a substitute for this analysis. The clean-context analysis is meant to catch what the migrated skill says on its own.

## Analysis Inputs

Read the source analysis from `<target-skill-dir>/org/analysis/analysis-of-<source-skill-name>.md` and the migrated analysis from `<target-skill-dir>/migrate/analysis/analysis-of-<source-skill-name>.md`.

The main agent owns the comparison reports. Do not delegate `<target-skill-dir>/migrate/compare/compare-of-<source-skill-name>.md` or `<target-skill-dir>/migrate/compare/summary.md` to the clean-context subagent.

Compare the logic described in the analyses, not surface wording. Focus on:

- entrypoints and activation rules,
- public subcommands, modes, and workflow pages,
- required inputs and assumptions,
- produced outputs and handoffs,
- decision gates and stop conditions,
- evidence requirements,
- artifact placeholder semantics,
- harness and CLI behavior,
- environment assumptions,
- storage behavior,
- validation behavior,
- ownership boundaries and side effects.

## Comparison Report

Write `<target-skill-dir>/migrate/compare/compare-of-<source-skill-name>.md`.

Use this structure:

```markdown
# Logical Difference: <source-skill-name>

## Compared Inputs

- Source analysis: `<target-skill-dir>/org/analysis/analysis-of-<source-skill-name>.md`
- Migrated analysis: `<target-skill-dir>/migrate/analysis/analysis-of-<source-skill-name>.md`

## Executive Summary

<Short statement of whether the migrated skill preserves, narrows, broadens, or changes the source logic.>

## Difference Table

| Area | Source Logic | Migrated Logic | Difference Type | Impact | Recommendation |
| --- | --- | --- | --- | --- | --- |
| <entrypoint, subcommand, gate, artifact, output, etc.> | <source behavior> | <migrated behavior> | <preserved, renamed, narrowed, broadened, removed, added, unresolved> | <logical impact> | <keep, fix, document, or investigate> |

## Missing or Added Behavior

<List behavior present in one analysis but absent in the other.>

## Placeholder and Artifact Differences

<Compare source artifacts with migrated placeholders and note semantic drift.>

## Open Questions

<Questions that require user or maintainer judgment.>
```

## Summary Report

Write `<target-skill-dir>/migrate/compare/summary.md` after all comparison reports are written.

Summarize differences for:

- `SKILL.md` entrypoint behavior.
- Each migrated subcommand page.
- Each migrated mode, workflow, primitive, or executable procedure page.
- Cross-page handoffs and placeholder usage.

Use this structure:

```markdown
# Migration Difference Summary

## Compared Analyses

| Source Analysis | Migrated Analysis | Compare Report |
| --- | --- | --- |
| `<target-skill-dir>/org/analysis/analysis-of-<source-skill-name>.md` | `<target-skill-dir>/migrate/analysis/analysis-of-<source-skill-name>.md` | `<target-skill-dir>/migrate/compare/compare-of-<source-skill-name>.md` |

## Entrypoint Differences

<Logical differences in `SKILL.md`.>

## Subskill and Page Differences

| Page | Difference Summary | Action |
| --- | --- | --- |
| `<page path>` | <Difference in logic, inputs, outputs, gates, or handoffs.> | <keep, fix, document, or investigate> |

## Overall Recommendation

<Whether the migration is logically faithful enough to keep, needs repair, or needs a new migration pass.>
```

## Validation

Before finishing, confirm:

1. `<target-skill-dir>/migrate/analysis/analysis-of-<source-skill-name>.md` exists and was produced by a clean-context subagent.
2. The migrated analysis excludes `<target-skill-dir>/org/`.
3. `<target-skill-dir>/migrate/compare/compare-of-<source-skill-name>.md` exists for each compared analysis pair.
4. `<target-skill-dir>/migrate/compare/summary.md` exists.
5. The comparison report distinguishes preserved, renamed, narrowed, broadened, removed, added, and unresolved behavior.
6. The final response lists the generated files and the highest-impact logical differences.

## Common Mistakes

- Comparing raw Markdown files instead of comparing the logic captured in the two analysis reports.
- Letting the subagent inherit the migration conversation context.
- Including `<target-skill-dir>/org/` as migrated runtime behavior.
- Treating renamed terms as logical changes without checking the migration plan.
- Missing subcommand or workflow pages that are not directly linked from `SKILL.md`.
- Writing only a summary and skipping the detailed `compare-of-<source-skill-name>.md` report.
