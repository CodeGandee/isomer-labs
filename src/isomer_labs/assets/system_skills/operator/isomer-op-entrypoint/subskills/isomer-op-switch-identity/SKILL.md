---
name: isomer-op-switch-identity
description: Use when a Project Operator needs to act under a selected Topic Actor or Agent identity posture, run commands from that worker's resolved workspace cwd, perform a one-time act-as prompt, persist the posture for the current session, report status, or reset back to normal operator identity.
---

# Isomer Operator Switch Identity

## Overview

Use this command-style operator skill to switch the Project Operator's working identity posture to a selected Topic Actor or Agent. The primary effect is cwd discipline and explicit invocation context: while switched, run task commands from the resolved `topic.actors.workspace` or `agent.workspace` and retain explicit topic and worker selectors unless a step explicitly needs another semantic path.

This skill is instruction-level posture, not OS-level impersonation, Agent Instance execution, Houmao launch, or Execution Adapter operation. Preserve provenance by saying the Project Operator acted as or on behalf of the selected identity.

## When to Use

Use this skill when the user asks the Project Operator to switch identity, act as a Topic Actor, act as an Agent, take over a worker's task, run one prompt as another worker, keep acting from that worker's workspace, report the current switched posture, or switch back.

Do not use this skill to create Topic Actor Workspaces, create Agent Workspaces, launch formal agents, mutate Workspace Runtime identity records, or repair worker topology. Route missing or unsafe worker workspace setup to `isomer-op-topic-mgr` or the relevant environment setup service.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Select command**: Choose `switch`, `act-as`, `status`, `reset`, or `help`; if the prompt names no command but asks to work as another identity, default to `switch` for the bounded task and do not persist unless the user explicitly asks.
2. **Resolve target identity**: For `switch` or `act-as`, identify exactly one target kind, Topic Actor or Agent, plus its name and selected Research Topic; if the target is ambiguous, ask for the missing kind, name, or topic before switching. A manifest default, including a sole active manifest actor, never activates a switch or supplies active posture on its own.
3. **Resolve target cwd**: Use semantic workspace path resolution, not directory scanning; for Topic Actors use `isomer-cli --print-json project paths get topic.actors.workspace --topic <topic> --topic-actor <topic-actor-name>`, and for Agents use `isomer-cli --print-json project paths get agent.workspace --topic <topic> --agent <agent-name>`.
4. **Check selected worker alignment**: From the resolved worker cwd, run `isomer-cli --print-json project self location`, then run `isomer-cli --print-json project self check --scope topic-actor --topic <topic> --topic-actor <topic-actor-name>` or `isomer-cli --print-json project self check --scope agent --topic <topic> --agent <agent-name>`. Stop before mutation if the selected worker does not resolve to the same cwd or the verdict is unresolved or conflict.
5. **Check readiness**: Confirm the resolved cwd exists, is the selected worker workspace, and is safe for the requested task; route Topic Actor readiness gaps to `isomer-op-topic-mgr actors-diagnose` or `project topic-actors diagnose`, and route Agent Workspace readiness gaps to `isomer-op-topic-mgr team-validate-workspaces` or available Agent Workspace setup evidence.
6. **Create a complete session-local posture envelope**: Remember target kind, Research Topic, worker name, resolved workspace cwd, persistence mode, and provenance source and wording. For one-task switches and `act-as`, run only the requested bounded work under the target identity and restore the previous Project Operator identity posture after the task summary; for persistent switches, retain this envelope only in the current operator session until `reset` or another switch.
7. **Run with cwd and selector discipline**: Default shell commands and file operations to the resolved `topic.actors.workspace` or `agent.workspace`. Every applicable topic- or worker-scoped command carries explicit `--topic` plus `--topic-actor` or `--agent` selectors from the envelope. Any command outside the worker cwd must state why, use a resolved semantic path, and retain the same selectors.
8. **Report provenance and status**: Say the Project Operator acted as or on behalf of the selected Topic Actor or Agent, include the complete posture envelope and selection evidence, and avoid claims that an independent Topic Actor process, launched Agent Instance, Houmao agent, or Execution Adapter produced the work.

If the user's task does not map cleanly to these steps, use your native planning tool to identify the requested identity action, collect the missing target evidence, preserve cwd discipline, and choose the safest command; ask only for target information that cannot be resolved from Project Manifest-backed context.

## Commands

Load only the selected command detail page before executing a command.

| Command | Use For | Detail |
| --- | --- | --- |
| `switch` | Resolve a Topic Actor or Agent target, then switch for one task or persist for the current session | [commands/switch.md](commands/switch.md) |
| `act-as` | Execute the following prompt once as a target identity, then restore the previous identity posture | [commands/act-as.md](commands/act-as.md) |
| `status` | Report the active switched identity posture, target kind, target name, cwd, persistence mode, and uncertainty | [commands/status.md](commands/status.md) |
| `reset` | Clear a persistent switched posture and return to normal Project Operator identity | [commands/reset.md](commands/reset.md) |
| `help` | Print usage, persistence modes, target resolution, cwd behavior, and provenance rules | [commands/help.md](commands/help.md) |

## Required Inputs

- Selected Project context or enough cwd evidence to resolve Project Manifest-backed context.
- Selected Research Topic for target workspace resolution.
- Target kind: Topic Actor or Agent.
- Target name: Topic Actor name for `topic.actors.workspace`, or Agent Name for `agent.workspace`.
- Persistence mode: one-task by default, persistent only when the user explicitly asks, or one-prompt restore for `act-as`.
- User prompt or task body for `act-as` and one-task `switch`.

## Session-Local Posture Envelope

The active envelope contains target kind, Research Topic, Topic Actor or Agent name, resolved worker workspace cwd, persistence mode, target-resolution source, and the provenance wording “Project Operator acted as or on behalf of”. It is planning context for the current operator session, not Project data, security identity, or runtime identity.

Do not write the envelope to the Project Manifest, local active context, Topic Workspace Manifest, Workspace Runtime, or another session-visible current-identity file. A persistent switch means persistent only within the current operator session.

## Output Contract

Default to **Essential Output** in chat. Use **Complete Output** when the user asks for complete, verbose, audit, debug, full handoff, or full output. Present either depth in natural-language Markdown. If the user explicitly requests JSON or another machine-readable format, serialize the applicable information in that format.

### Essential Output

State whether identity was switched, used for one action, made persistent, reset, blocked, or left unchanged. Name the target, topic, resolved Topic Actor or Agent Workspace, and persistence scope. Mention any command that had to run outside that workspace and why, then give blockers and the next safe action.

### Complete Output

Group the complete explanation by target-resolution evidence, workspace and worktree readiness, previous and active identity scope, restoration behavior, and provenance wording used to avoid unsupported runtime claims.

## Operational Notes

- Ask or use Project Manifest-backed Isomer context.

## Guardrails

- DO NOT infer a target by scanning workspace directories.
- DO NOT use the Project root, Topic Workspace root, or `topic.repos.main` as the default switched cwd.
- DO NOT persist a switch unless the user explicitly asks for persistence.
- DO NOT treat a manifest default or sole manifest actor as an active switched posture.
- DO NOT run a context-sensitive command without the envelope's explicit topic and worker selectors when that command supports them.
- DO NOT persist the posture in Project, local-context, Topic Workspace, Workspace Runtime, or cross-session files.
- DO NOT leave `act-as` active after the following prompt completes.
- DO NOT claim OS-level impersonation, independent Topic Actor process execution, launched Agent Instance execution, Houmao launch, or Execution Adapter execution without verified runtime evidence.
- DO NOT overwrite another worker's uncommitted work without explicit user instruction.
## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
