---
skill_invocation_notation: >
  Top-level skill entrypoints use SKILL.md. Parent-scoped subskill entrypoints use
  SKILL-MAIN.md and are loaded explicitly through their parent; nested SKILL.md is
  accepted only as legacy input when SKILL-MAIN.md is absent.
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Topic Workspace Publication

## Workflow

1. Infer one exact publication child from the user's task.
2. Load the selected child page plus the read-only context, direct Git, publication, privacy, and persistence references.
3. Execute only that child and keep the Source Topic Workspace root repository unchanged.

If the request does not map cleanly to one child, use the native planning tool to identify whether status, init, plan, or sync is the smallest safe publication operation, then execute it or return the missing decision.

## Subcommands

Select exactly one publication child operation:

| Child | Use For | Page |
| --- | --- | --- |
| `isomer-op-entrypoint->topic-git->publish()->status()` | Inspect binding, copy, projection, conflicts, and last outcomes. | [commands/publish/status.md](commands/publish/status.md) |
| `isomer-op-entrypoint->topic-git->publish()->init()` | Validate the remote and destination, create copy-local preparation, and avoid push. | [commands/publish/init.md](commands/publish/init.md) |
| `isomer-op-entrypoint->topic-git->publish()->plan()` | Inventory, classify, sanitize, compare, and bind approval to exact state. | [commands/publish/plan.md](commands/publish/plan.md) |
| `isomer-op-entrypoint->topic-git->publish()->sync()` | Reconstruct if needed, fetch, resolve safe changes, commit, and push components before the superproject. | [commands/publish/sync.md](commands/publish/sync.md) |

With no selected child or unambiguous task, return this table. Publication is available after Topic Workspace registration, does not require Workspace Runtime or local root tracking, and never stages or commits the Source Topic Workspace root repository.
