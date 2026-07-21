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

# Start Research by Agent Team

## Workflow

1. Interpret this usage path as formal Topic Team Specialization from a Domain Agent Team Template.
2. Recommend parent-scoped route `isomer-op-entrypoint->topic-team`.
3. Use `$isomer-op-entrypoint use topic-team to fast-forward specialization` with the Research Topic and selected Domain Agent Team Template.
4. Explain that formal Agent Team research selects execution topology but does not select the DeepSci or Kaoju research paradigm; offer `start-deepsci-research`, `start-kaoju-survey`, or no optional paradigm as a separate choice when relevant.
5. Mention that the owner skill can create or consume prepared-topic evidence, specialize copied template material, route Topic Workspace setup through service skills, prepare Agent Workspace setup evidence, validate static topic-team material, and write the final topic-team summary.
6. State the mutation boundary: this welcome skill does not specialize the team, approve the profile, materialize the profile, create Agent Instances, run Execution Adapters, launch Houmao agents, mutate Workspace Runtime, or install or run an optional research extension.
7. Keep Houmao loop, runtime, launch profile, mailbox, gateway, and template-mapping explanation inside the `isomer-op-entrypoint->topic-team` workflow. The owner may delegate bounded adapter support through `isomer-op-entrypoint->houmao`.

If the user's task does not map cleanly to these steps, use your native planning tool to check whether the user supplied a Domain Agent Team Template; if not, ask for the template or recommend `start-research-manually`.

## Output Guidance

Recommend the agent-team research path in natural language and route it through `isomer-op-entrypoint->topic-team`. Give `$isomer-op-entrypoint use topic-team to fast-forward specialization` as the safe first invocation. Name any missing Research Topic, Domain Agent Team Template, Project context, research-paradigm choice, or mutation authority, then state whether to invoke the public entrypoint or provide the missing input.

Do not launch an Agent Team or Houmao runtime from the welcome surface.
