---
name: isomer-op-switch-identity
description: Use when a Project Operator needs to act under a selected Topic Actor or Agent identity posture, run commands from that worker's resolved workspace cwd, perform a one-time act-as prompt, persist the posture for the current session, report status, or reset back to normal operator identity.
---

# Isomer Operator Switch Identity

## Overview

Use this command-style operator skill to switch the Project Operator's working identity posture to a selected Topic Actor or Agent. The primary effect is cwd discipline: while switched, run task commands from the resolved `topic.actors.workspace` or `agent.workspace` unless a step explicitly needs another semantic path.

This skill is instruction-level posture, not OS-level impersonation, Agent Instance execution, Houmao launch, or Execution Adapter operation. Preserve provenance by saying the Project Operator acted as or on behalf of the selected identity.

## When to Use

Use this skill when the user asks the Project Operator to switch identity, act as a Topic Actor, act as an Agent, take over a worker's task, run one prompt as another worker, keep acting from that worker's workspace, report the current switched posture, or switch back.

Do not use this skill to create Topic Actor Workspaces, create Agent Workspaces, launch formal agents, mutate Workspace Runtime identity records, or repair worker topology. Route missing or unsafe worker workspace setup to `isomer-op-topic-mgr` or the relevant environment setup service.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Select command**: Choose `switch`, `act-as`, `status`, `reset`, or `help`; if the prompt names no command but asks to work as another identity, default to `switch` for the bounded task and do not persist unless the user explicitly asks.
2. **Resolve target identity**: For `switch` or `act-as`, identify exactly one target kind, Topic Actor or Agent, plus its name and selected Research Topic; if the target is ambiguous, ask for the missing kind, name, or topic before switching.
3. **Resolve target cwd**: Use semantic workspace path resolution, not directory scanning; for Topic Actors use `isomer-cli --print-json project paths get topic.actors.workspace --topic <topic> --topic-actor <topic-actor-name>`, and for Agents use `isomer-cli --print-json project paths get agent.workspace --topic <topic> --agent <agent-name>`.
4. **Check readiness**: Confirm the resolved cwd exists, is the selected worker workspace, and is safe for the requested task; route Topic Actor readiness gaps to `isomer-op-topic-mgr actors-diagnose` or `project topic-actors diagnose`, and route Agent Workspace readiness gaps to `isomer-op-topic-mgr team-validate-workspaces` or available Agent Workspace setup evidence.
5. **Apply posture**: For one-task switches and `act-as`, run only the requested bounded work under the target identity and restore the previous Project Operator identity posture after the task summary; for persistent switches, remember the selected identity posture for the current operator session until `reset` or another switch.
6. **Run with cwd discipline**: Default shell commands and file operations to the resolved `topic.actors.workspace` or `agent.workspace`; any command outside that cwd must state why and use a resolved semantic path.
7. **Report provenance and status**: Say the Project Operator acted as or on behalf of the selected Topic Actor or Agent, include the resolved cwd and persistence mode, and avoid claims that an independent Topic Actor process, launched Agent Instance, Houmao agent, or Execution Adapter produced the work.

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

## Output Contract

Default to **Essential Output** in chat. Use **Complete Output** when the user asks for complete, verbose, audit, debug, full handoff, or full output. Present either depth in natural-language Markdown. If the user explicitly requests JSON or another machine-readable format, serialize the applicable information in that format.

### Essential Output

State whether identity was switched, used for one action, made persistent, reset, blocked, or left unchanged. Name the target, topic, resolved Topic Actor or Agent Workspace, and persistence scope. Mention any command that had to run outside that workspace and why, then give blockers and the next safe action.

### Complete Output

Group the complete explanation by target-resolution evidence, workspace and worktree readiness, previous and active identity scope, restoration behavior, and provenance wording used to avoid unsupported runtime claims.

## Common Mistakes

- Do not infer a target by scanning workspace directories; ask or use Project Manifest-backed Isomer context.
- Do not use the Project root, Topic Workspace root, or `topic.repos.main` as the default switched cwd.
- Do not persist a switch unless the user explicitly asks for persistence.
- Do not leave `act-as` active after the following prompt completes.
- Do not claim OS-level impersonation, independent Topic Actor process execution, launched Agent Instance execution, Houmao launch, or Execution Adapter execution without verified runtime evidence.
- Do not overwrite another worker's uncommitted work without explicit user instruction.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
