---
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Input Surfaces

## Workflow

1. Identify the strongest user-supplied input surface: explicit skill name, CLI command, file path, prompt body, Project root, Toolbox source or manifest, Research Topic, Topic Workspace, Topic Actor, Agent, Domain Agent Team Template, Topic Agent Team Profile or Bundle, Topic Team Instantiation Packet, Agent Team Instance, DeepSci stage, or Kaoju survey intent.
2. Classify the requested operation scope as `project`, `topic`, `topic-actor`, or `agent`, and extract every prompt-named Research Topic, Topic Actor, and Agent as an explicit selector candidate before consulting defaults.
3. Run `isomer-cli --print-json project self location` for ambient workspace facts, then run `isomer-cli --print-json project self check --scope <scope>` with the extracted `--topic`, `--topic-actor`, or `--agent` selectors for context-sensitive work. Resolve Project and Topic context through this evidence instead of scanning unregistered sibling directories.
4. For file inputs, determine whether the file is a topic brief, package request, research record payload, artifact-format payload, handoff, paper draft, experiment result, reviewer feedback, or generic prompt file.
5. For identity inputs, distinguish Topic Actor names from Agent Names and use `isomer-op-entrypoint->identity` when the task must run from `topic.actors.workspace` or `agent.workspace`. Do not treat a sole manifest actor fallback as an active switch posture.
6. Explain the normalized goal, strongest input surface, operation scope, ambient location, pinned target and source, alignment verdict, missing information, and safest next route in natural language.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step input-resolution plan from the prompt, available Project context, and Isomer CLI read-only discovery commands, then execute the plan or stop on a missing-input blocker.

## Surface Map

| Input Surface | Typical Meaning | Route Hint |
| --- | --- | --- |
| Explicit `$isomer-op-entrypoint`, `$isomer-ext-deepsci-entrypoint`, or `$isomer-ext-kaoju-entrypoint` skill | User already chose a public pack. | Load that entrypoint and follow its public routing workflow after checking obvious blockers. |
| `isomer-cli ...` language | User wants a CLI command family. | Use [cli-index.md](cli-index.md) and CLI help for that family. |
| Research Topic text or topic brief | Topic creation, preparation, or research-stage input. | New or partial topics route to `isomer-op-entrypoint->topic-create`; prepared DeepSci or Kaoju work may route to a public extension. A topic alone does not imply a formal Agent Team. |
| Existing topic id or Topic Workspace | Initialized-topic or research-stage work. | Inspect context, then route to `isomer-op-entrypoint->topic-manage`, the applicable public extension's `workspace` member, or a selected extension route. Existing topic context alone does not imply a formal Agent Team. |
| Topic Actor or Agent name | Work must run from a worker workspace. | Route to `isomer-op-entrypoint->identity` for cwd discipline before doing the task. |
| Explicit specialization invocation or formal Agent Team target | Formal Topic Team Specialization. | Route to `isomer-op-entrypoint->topic-team` only when the user explicitly invokes it or the prompt or authoritative context identifies a Domain Agent Team Template, Topic Agent Team Profile or Bundle, Topic Team Instantiation Packet, Agent Team Instance, selected formal-team material, or equivalent Agent Team target. |
| Toolbox source path, Toolbox manifest, callback insertion point, Toolbox Runtime Param, or Toolbox registration language | Project-local Toolbox creation, conversion, installation, callback, parameter, or inspection work. | Route to `isomer-op-entrypoint->toolbox`, unless the user explicitly asks for a Toolbox CLI command family. |
| JSON payload or record file | Structured record or artifact format work. | Route to `isomer-cli ext research records ...` or `isomer-cli project artifact-formats ...`. |
| Worker operation-set directory, acceptance manifest, partial receipt, or unrecorded operation outputs | Exhaustive staging closeout or explicit historical repair. | Route to `isomer-op-entrypoint->operation-sets` or `isomer-cli ext research operation-sets ...`; do not route it to generic Project lifecycle management. |
| Paper draft, review, rebuttal, figure, or data statement | DeepSci paper companion work. | Route to the matching DeepSci extension skill after readiness checks. |
| Field-survey prompt, references, papers, repositories, datasets, models, or comparison request | Kaoju evidence-led survey work. | Route to `isomer-ext-kaoju-entrypoint` or the matching Kaoju stage after readiness checks. |

Prefer typed Isomer refs and semantic labels over inferred paths. Treat prompt memory, chat memory, rendered Markdown, and worker-local files as candidate context until the selected route accepts them.

Project Manifest defaults are visible fallback inputs, not ambient location or acting posture. Once preflight accepts a topic or worker target, retain its explicit selectors on every applicable downstream command and rerun preflight before an intentional scope change.

Do not use generic `prepare`, launch-facing work, a missing summary, a missing Agent Workspace, or a readiness gap as a substitute for formal Agent Team intent. When formal-team evidence is contextual rather than explicit in the prompt, name that evidence in the routing rationale.
