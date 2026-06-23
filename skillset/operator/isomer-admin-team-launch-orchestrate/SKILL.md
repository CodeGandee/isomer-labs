---
name: isomer-admin-team-launch-orchestrate
description: Orchestrate Agent Team Instance creation and Houmao adapter launch from approved profile bundle and runtime material.
---

# Isomer Team Launch Orchestrate

## Workflow

When this skill is invoked, execute the following steps in order.

1. Confirm that the selected Topic Agent Team Profile comes from an approved profile bundle or an explicitly supported legacy path.
2. Validate Workspace Runtime initialization, Topic Environment Readiness, profile provenance, Agent Team Instance creation inputs, and launch blockers.
3. Create or select the Agent Team Instance through Workspace Runtime APIs, then inspect Agent Instance and Agent Workspace records.
4. Route launch materialization or quick launch through the Houmao adapter using approved profile bundle and runtime records.
5. Record adapter diagnostics, command refs, payload refs, launch refs, and operator provenance without storing adapter reasoning as topic-profile material.

If the user's task does not map cleanly to these steps, use your native planning tool to separate profile validation, runtime creation, and adapter launch into explicit steps, then execute the safe subset.

## Reference Routing

Read first:

- Materialized Topic Agent Team Profile Bundle.
- Workspace Runtime readiness and Agent Team Instance summary.

Read as needed:

- Houmao adapter docs and manifest refs when launch materialization is requested.
- Topic Service Agent support outputs when launch preparation used service help.

## Entry Signals

- The user asks to create, launch, inspect, stop, reconcile, or handoff through a topic team.
- The next step crosses from profile bundle material into Workspace Runtime or Houmao adapter material.

## Exit Criteria

- Runtime records or adapter launch records show the requested state.
- Project operator and Topic Service Agent provenance refs are preserved.
- Any launch blockers are reported before Houmao mutation.

## Guardrails

- Do not launch from Domain Agent Team Template material alone.
- Do not launch preview-only Topic Agent Team Profile output.
- Do not add Project Operator Sessions or Topic Service Agents as research team members unless the profile defines that role.
