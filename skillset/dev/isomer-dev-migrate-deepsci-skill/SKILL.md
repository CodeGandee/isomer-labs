---
name: isomer-dev-migrate-deepsci-skill
description: Use when the user explicitly invokes $isomer-dev-migrate-deepsci-skill to copy-migrate, refactor-migrate, or find-diff for an upstream DeepScientist source skill migrated into an Isomer Labs skill.
---

# Isomer DeepScientist Skill Migration

## Overview

Use this skill to migrate upstream DeepScientist skills into Isomer Labs skills and audit the logical difference after migration. It has two migration modes: `copy-migrate` keeps the migrated skill close to the original source structure while adapting terms and implementation details, and `refactor-migrate` rewrites the skill into a more native Isomer style while preserving essential logic. The `find-diff` subcommand compares source and migrated skill logic after migration.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Select the subcommand** from the **Subcommands** table. Use `copy-migrate` when the user asks to migrate and does not specify a mode.
2. **Resolve the source and/or target skill directories** using the selected subcommand's rules.
3. **Load the selected subcommand page** and follow its `## Workflow`.
4. **Validate and report** changed files, copied source files, migration mode or diff mode, placeholders, harness replacements, logical differences, and unresolved issues.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan using the subcommands and constraints in this skill, then execute the plan.

## Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `copy-migrate` | Migrate a DeepScientist skill while keeping the result as close to the original as practical, preserving document structure and making only targeted term, storage, CLI, and metadata adaptations. | [references/copy-migrate.md](references/copy-migrate.md) |
| `refactor-migrate` | Migrate a DeepScientist skill by first deep-inspecting the source process, planning term and harness substitutions, then rewriting the skill to look native to the current Isomer Labs project while preserving essential logic, constraints, assumptions, inputs, and outputs. | [references/refactor-migrate.md](references/refactor-migrate.md) |
| `find-diff` | After migration, deep-inspect the migrated skill in a clean subagent context and compare the migrated logic against the original source analysis under `org/analysis/`. | [references/find-diff.md](references/find-diff.md) |

## Invocation Notes

- Preferred explicit form: `$isomer-dev-migrate-deepsci-skill copy-migrate <source-skill> to <target-skill>`.
- Refactor explicit form: `$isomer-dev-migrate-deepsci-skill refactor-migrate <source-skill> to <target-skill>`.
- Diff explicit form: `$isomer-dev-migrate-deepsci-skill find-diff <target-skill>`.
- If the user asks to migrate a skill but does not name a mode, choose `copy-migrate`.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
