---
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Register Dataset

Route: `isomer-ext-kaoju-entrypoint->manage-dataset()->register()`.

## Workflow

1. Resolve the Topic Workspace, external dataset identity, access and license posture, and intended stable dataset id.
2. Ask the Topic Workspace owner to inspect the external target and create only the managed link; never copy, move, or mutate the target.
3. Revise `KAOJU:TOPIC-DATASET-MANIFEST` with immutable locators, observed metadata, fingerprint or staleness policy, actor, and provenance.
4. Validate the new canonical payload and report the resulting ref and reuse posture.

If the request does not map cleanly to these steps, use the native planning tool to build and execute a bounded plan from the parent manager contract without inventing another command.
