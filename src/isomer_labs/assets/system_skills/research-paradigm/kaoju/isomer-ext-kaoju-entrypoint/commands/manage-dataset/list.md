---
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# List Datasets

Route: `isomer-ext-kaoju-entrypoint->manage-dataset()->list()`.

## Workflow

1. Resolve the Topic Workspace and latest unambiguous `KAOJU:TOPIC-DATASET-MANIFEST`.
2. List entries with id, name, summary, availability, fingerprint posture, access, and license state.
3. Report manifest ambiguity or absence without scanning the filesystem or mutating state.

If the request does not map cleanly to these steps, use the native planning tool to build and execute a bounded plan from the parent manager contract without inventing another command.
