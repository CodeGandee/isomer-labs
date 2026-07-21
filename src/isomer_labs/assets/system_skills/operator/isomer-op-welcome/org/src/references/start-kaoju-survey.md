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

# Start Kaoju Survey

## Workflow

1. Interpret this usage path as optional evidence-led survey work over literature, codebases, datasets, or models, not as a choice of manual or formal Agent Team execution topology.
2. Match the goal to a Kaoju pipeline intent using **Kaoju Capability Map**.
3. Treat package-catalog presence, Project declaration, and host usability as different evidence states; use `show-extensions` when state is unclear.
4. Recommend `$isomer-op-entrypoint` with the concrete Kaoju goal unless accepted extension and workspace readiness already makes `$isomer-ext-kaoju-entrypoint use <subcommand> to <task>` safe.
5. Route missing extension availability or compatibility through `isomer-op-entrypoint->system-skills`, and route missing Project, Topic Workspace, survey, repository, dataset, actor or agent workspace, or Kaoju readiness through the public entrypoint to the applicable scoped owner.
6. State the mutation boundary and next action without running research, installation, registration, bootstrap, acquisition, code execution, or workspace mutation from the welcome surface.

If the user's task does not map cleanly to these steps, use your native planning tool to compare the Kaoju pipeline capabilities, extension state, workspace readiness, execution topology, and active owner routes, then recommend one safe next invocation or ask for the missing survey goal.

## Kaoju Capability Map

| Goal | Public Entry Surface |
| --- | --- |
| Choose research directions or build a source reading list. | `$isomer-ext-kaoju-entrypoint use choose-directions to <task>` or `use build-reading-list to <task>`. |
| Ingest and examine a paper, report, repository, dataset, or model. | `$isomer-ext-kaoju-entrypoint use ingest-reading-item to <task>` or `use ingest-source-code to <task>`, followed by the selected evidence procedure. |
| Prepare an environment and run one separately approved bounded source-code trial. | `$isomer-ext-kaoju-entrypoint use prepare-code-run to <task>` or `use run-code-trial to <task>`. |
| Run a landscape, curated intake, direction expansion, theory comparison, method trial, comparative, or audit procedure. | The matching `$isomer-ext-kaoju-entrypoint use <named-pass> to <task>` invocation. |
| Draft and manage a MyST-first paper, build its PDF, or export accepted survey records to a self-contained wiki. | The matching `$isomer-ext-kaoju-entrypoint use <subcommand> to <task>` form. |

The pipeline may route to specialized Kaoju skills for framing, discovery, acquisition, examination, genuine reproduction, bounded trials, comparison, audit, synthesis, writing, or wiki export. Do not duplicate all fourteen skill descriptions in the welcome response unless the user asks for them.

## Readiness and Safe Invocation

If the extension and workspace are ready, recommend the matching direct pipeline invocation. If readiness is unknown, recommend:

`$isomer-op-entrypoint with the concrete Kaoju survey goal.`

The entrypoint preserves explicit extension intent, checks Project declaration and readiness, delegates missing extension state through `isomer-op-entrypoint->system-skills`, delegates missing Kaoju workspace readiness through `isomer-ext-kaoju-entrypoint->workspace`, and selects the matching intent or member.

Kaoju can operate with manual Topic Actors or an established formal Agent Team. Do not infer Topic Team Specialization from the survey paradigm, generic preparation, missing summaries, or missing Agent Workspaces.

## Mutation Boundary

This welcome path does not install or register Kaoju, prepare its workspace, create or mutate a Research Topic, specialize or launch an Agent Team, acquire sources, run code, execute a pipeline intent, or write research records. It only explains the capability and recommends the next owner route.
