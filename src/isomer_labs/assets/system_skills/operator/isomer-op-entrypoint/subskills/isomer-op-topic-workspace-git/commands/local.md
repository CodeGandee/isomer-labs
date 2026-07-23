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

# Local Topic Workspace Tracking

## Workflow

1. Infer one exact local child from the user's task.
2. Load the selected child page plus the read-only context, direct Git, local safety, and persistence references.
3. Execute only that child and report local state without reading publication as a prerequisite.

If the request does not map cleanly to one child, use the native planning tool to identify whether status, init, plan, ignore, or commit is the smallest safe local operation, then execute it or return the missing decision.

## Subcommands

Select exactly one local child operation:

| Child | Use For | Page |
| --- | --- | --- |
| `isomer-op-entrypoint->topic-git->local()->status()` | Inspect root repository, nested exclusions, and blockers. | [commands/local/status.md](commands/local/status.md) |
| `isomer-op-entrypoint->topic-git->local()->init()` | Initialize or safely reuse the root repository after ancestor proof and approval. | [commands/local/init.md](commands/local/init.md) |
| `isomer-op-entrypoint->topic-git->local()->plan()` | Classify root-owned whole files and create an exact commit plan. | [commands/local/plan.md](commands/local/plan.md) |
| `isomer-op-entrypoint->topic-git->local()->ignore()` | Update only the approved managed root ignore block. | [commands/local/ignore.md](commands/local/ignore.md) |
| `isomer-op-entrypoint->topic-git->local()->commit()` | Stage exact approved paths, verify the index, and create one local commit. | [commands/local/commit.md](commands/local/commit.md) |

With no selected child or unambiguous task, return this table. Local operations never load publication state as a prerequisite and never contact a remote.
