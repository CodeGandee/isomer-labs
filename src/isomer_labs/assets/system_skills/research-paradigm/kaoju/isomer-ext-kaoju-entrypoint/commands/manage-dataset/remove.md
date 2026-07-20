---
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Remove Dataset Registration

Route: `isomer-ext-kaoju-entrypoint->manage-dataset()->remove()`.

## Workflow

1. Resolve one registered dataset and confirm that removal of its managed link and registration is authorized.
2. Ask the Topic Workspace owner to remove only the managed link; never delete or alter the external target.
3. Revise the canonical manifest to mark the registration unavailable or removed while preserving prior evidence.
4. Report the retained external locator, revised ref, and downstream reuse blocker.

If the request does not map cleanly to these steps, use the native planning tool to build and execute a bounded plan from the parent manager contract without inventing another command.
