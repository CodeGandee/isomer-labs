# Input Surfaces

## Workflow

1. Identify the strongest user-supplied input surface: explicit skill name, CLI command, file path, prompt body, Project root, Toolbox source or manifest, Research Topic, Topic Workspace, Topic Actor, Agent, Domain Agent Team Template, DeepSci stage, or Kaoju survey intent.
2. Resolve Project and Topic context through prompt evidence or read-only Isomer CLI context commands instead of scanning unregistered sibling directories.
3. For file inputs, determine whether the file is a topic brief, package request, research record payload, artifact-format payload, handoff, paper draft, experiment result, reviewer feedback, or generic prompt file.
4. For identity inputs, distinguish Topic Actor names from Agent Names and use `isomer-op-switch-identity` when the task must run from `topic.actors.workspace` or `agent.workspace`.
5. Return a normalized request containing `interpreted_goal`, `input_surface`, `selected_context`, missing fields, and the safest next route.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step input-resolution plan from the prompt, available Project context, and Isomer CLI read-only discovery commands, then execute the plan or stop on a missing-input blocker.

## Surface Map

| Input Surface | Typical Meaning | Route Hint |
| --- | --- | --- |
| Explicit `$isomer-op-*`, `$isomer-deepsci-*`, or `$isomer-kaoju-*` skill | User already chose a skill. | Load that skill and follow its workflow after checking obvious blockers. |
| `isomer-cli ...` language | User wants a CLI command family. | Use [cli-index.md](cli-index.md) and CLI help for that family. |
| Research Topic text or topic brief | Topic creation, preparation, or research-stage input. | New or partial topics route to `isomer-op-topic-creator`; prepared DeepSci or Kaoju work may route to extension skills. |
| Existing topic id or Topic Workspace | Initialized-topic or research-stage work. | Inspect context, then route to `isomer-op-topic-mgr`, the applicable research workspace manager, or a selected extension stage. |
| Topic Actor or Agent name | Work must run from a worker workspace. | Route to `isomer-op-switch-identity` for cwd discipline before doing the task. |
| Domain Agent Team Template | Formal Topic Team Specialization. | Route to `isomer-op-topic-team-specialize`. |
| Toolbox source path, Toolbox manifest, callback insertion point, Toolbox Runtime Param, or Toolbox registration language | Project-local Toolbox creation, conversion, installation, callback, parameter, or inspection work. | Route to `isomer-op-toolbox-mgr`, unless the user explicitly asks for a Toolbox CLI command family. |
| JSON payload or record file | Structured record or artifact format work. | Route to `isomer-cli ext research records ...` or `isomer-cli project artifact-formats ...`. |
| Paper draft, review, rebuttal, figure, or data statement | DeepSci paper companion work. | Route to the matching DeepSci extension skill after readiness checks. |
| Field-survey prompt, references, papers, repositories, datasets, models, or comparison request | Kaoju evidence-led survey work. | Route to `isomer-kaoju-pipeline` or the matching Kaoju stage after readiness checks. |

Prefer typed Isomer refs and semantic labels over inferred paths. Treat prompt memory, chat memory, rendered Markdown, and worker-local files as candidate context until the selected route accepts them.
