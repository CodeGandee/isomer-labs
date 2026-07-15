---
name: isomer-srv-topic-service-agent-support
description: Use when Topic Service Agents or optional Topic Service Masters need bounded service-team support for Topic Workspace management, environment setup, topic-team specialization, monitoring, diagnostics, or support Artifacts.
---

# Isomer Topic Service Agent Support

## Overview

This skill guides Topic Service Agents and optional Topic Service Masters through bounded support while preserving Project Operator ownership of decisions and canonical state.

## When to Use

Use this skill for an authorized Service Request that needs Topic Workspace support, environment setup assistance, topic-team specialization support, monitoring, diagnostics, or support Artifact writing.

## Workflow

When this skill is invoked, first select a subcommand when the request names one. If no subcommand is named, execute the default support workflow below.

1. Confirm the Service Request scope, selected Research Topic, Topic Workspace, requester, authorization, expected outputs, allowed file surfaces, and whether the work is being performed by a Topic Service Master or by the Project Operator Session or Operator Agent fallback.
2. Perform only Service Team work:
   - Allowed work includes Topic Workspace management from the resolved Topic Workspace cwd, topic environment readiness checks, Pixi environment configuration, Topic Main Development Repository or projection support, generated link or symlink introduction into Agent Workspaces, work-agent setup support, template inspection support, placeholder reconciliation support, copied material planning, topic edit drafting, monitoring, diagnostics, or support Artifact writing.
3. Record Service Request refs, Topic Service Agent refs, support Artifact refs, validation refs, and blockers for the Project Operator Session.
4. Return bounded output that can be validated by generic Isomer packet, profile bundle, runtime, or adapter validators.
5. Stop or request clarification when the Service Request would require research decision authority.

If the user's task does not map cleanly to these steps, use your native planning tool to restate the bounded Service Request and execute only the service-safe portion.

## Subcommands

Load only the subcommand pages needed for the support task.

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `prepare-topic-service-master` | Define or refresh the Project-scoped Houmao-backed Topic Service Master support material for a Topic Workspace without launching a live agent | [references/prepare-topic-service-master.md](references/prepare-topic-service-master.md) |
| `launch-topic-service-master` | Start the prepared Topic Service Master from the Topic Workspace cwd | [references/launch-topic-service-master.md](references/launch-topic-service-master.md) |
| `inspect-topic-service-master` | Inspect Topic Service Master readiness, runtime, mailbox, gateway, and blockers | [references/inspect-topic-service-master.md](references/inspect-topic-service-master.md) |
| `stop-topic-service-master` | Stop or pause a running Topic Service Master through the internal provider route | [references/stop-topic-service-master.md](references/stop-topic-service-master.md) |
| `repair-topic-service-master` | Repair missing projection, launch-profile, mailbox, gateway, or runtime support material | [references/repair-topic-service-master.md](references/repair-topic-service-master.md) |

## Reference Routing

Read first:

- Service Request payload and selected Effective Topic Context.
- Topic Workspace path and Workspace Runtime readiness.
- Topic Service Master status. If no Topic Service Master is started, treat the Project Operator Session or Operator Agent as the actor performing the same bounded workspace-management duty.
- Houmao integration policy from `isomer-cli --print-json project integrations houmao status` before any Houmao-backed Topic Service Master route.

Read as needed:

- Domain Agent Team Template inspection summary for Topic Team Specialization support.
- Copied material or topic edit draft requested by the Project Operator Session.
- Houmao skill context from `isomer-cli --print-json project integrations houmao skill-context <same-lifecycle-route> --topic <research-topic-id>` when a lifecycle subcommand needs internal provider procedure.

## Entry Signals

- A Topic Service Agent or Topic Service Master receives a bounded Service Request.
- A topic agent team member asks for support that requires Topic Workspace cwd or topic-owned surfaces, such as Pixi setup, projection repair, generated links, or Agent Workspace link introduction.
- No Topic Service Master is running, and the Project Operator Session or Operator Agent needs to perform bounded Topic Workspace manager work directly.
- Topic Creator or Topic Manager delegates Topic Service Master lifecycle work to `prepare-topic-service-master`, `launch-topic-service-master`, `inspect-topic-service-master`, `stop-topic-service-master`, or `repair-topic-service-master`.

## Exit Criteria

- Support outputs are recorded with refs and validation expectations.
- The requester can continue with packet reconciliation, profile materialization, launch orchestration, or blocker handling.
- Service boundaries and any refused research-authority requests are explicit.

## Operational Notes

- Use Isomer CLI skill-context and Project-local `.isomer-labs/houmao-skills/`.
- Use the returned `houmao_project_path` and tell agents to run Houmao commands with `--project-dir <houmao_project_path>`.

## Guardrails

- DO NOT own Research Claims, Gates, task routing, or research team membership.
- DO NOT store credentials or live process state in support Artifacts.
- DO NOT bypass Isomer validators or user approval.
- DO NOT ask the user to install Houmao system skills into their ordinary operator skill home as the primary route.
- DO NOT rely on implicit `.houmao/` discovery from Topic Workspace cwd.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
