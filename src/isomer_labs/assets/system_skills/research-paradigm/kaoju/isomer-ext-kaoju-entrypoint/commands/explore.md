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

# Explore

## Workflow

1. **Resolve context**. Run `isomer-cli --print-json project self location` and, when a topic is named or implied, `isomer-cli --print-json project self check --scope topic --topic <topic>`. Stop on unresolved or conflicting context.
2. **Load the explore subskill**. Read `subskills/isomer-kaoju-explore/SKILL-MAIN.md` and let it select the appropriate context-specific subcommand (`auto`, `directions`, `reading-list`, `intake`, `comparison`, `trial`, `paper`, `wiki`, or `help`).
3. **Run the interactive planning discussion**. Follow the selected subcommand page. The subskill maintains an in-memory coverage map and asks up to five clarification questions. It writes no files, artifacts, Runs, Gates, or Service Requests.
4. **Receive the agreed plan**. When the discussion reaches consensus, the subskill returns a plan summary containing the selected command or procedure, scope, evidence strategy, output form, risks, and the exact public invocation.
5. **Ask for explicit consent**. Present the plan and recommended invocation. If the user does not confirm, stop and return the plan as a paused recommendation.
6. **Route to the selected command**. On confirmation, load the selected command page and execute it with the pinned topic and any resolved context. Do not merge this planning exchange into the target procedure's Run.

If the user's task does not map cleanly to these steps, use the native planning tool to build a bounded exploration plan from the available subcommands, context, and user goal, then execute it.

## Owner, Inputs, and Outputs

Owner: `isomer-ext-kaoju-entrypoint->explore`. Inputs: Research Topic, Topic Workspace, prior survey state, active Runs, and the user's task prompt. Output: a confirmed public invocation for the next Kaoju command or procedure.

## Gates, Blockers, and Resume

The consent step is mandatory. Context conflicts, missing workspace readiness, or an unresolved planning question pause at the explore subcommand. Resume by re-invoking `explore` with the same context; no durable Run is created for the planning phase.
