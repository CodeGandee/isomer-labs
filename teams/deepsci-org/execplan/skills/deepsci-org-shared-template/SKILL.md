---
name: deepsci-org-shared-template
description: Generated shared guardrails for all deepsci-org Domain Agent Team Template participants; use with generated deepsci-org event and tick skills.
---

# deepsci-org Shared Template

## Scope

Use this generated skill as shared posture for any participant working under the `deepsci-org` execplan. This package is a Domain Agent Team Template, not a concrete Topic Agent Team Profile, Agent Team Instance, Topic Workspace, Run, or live team.

## Read First

- `../../manifest.toml`
- `../../specs/collab/collab-overview.md`
- `../../specs/participants/participants.toml`
- `../../specs/collab/topology/topology.toml`
- `../../specs/workspace/workspace.toml`
- `../../specs/run/run-contract.md`

## Rules

- Keep Isomer domain terms intact: Domain Agent Team Template, Topic Agent Team Profile, Agent Team Instance, Agent Role, Agent Profile, Capability Binding, Skill Binding projection, Topic Workspace, Workspace Runtime, Research Topic, Research Inquiry, Research Task, Run, Artifact, Evidence Item, Finding, Research Claim, Gate, Decision Record, and Provenance Record.
- Leave topic values as placeholders until `{topic_agent_team_profile_id}` specializes them.
- Treat `deepsci-org-master` as the internal team root and only default dispatcher.
- Return normal specialist results to `deepsci-org-master`.
- Do not create, launch, inspect, stop, or message managed agents from this shared skill. Use maintained Houmao skills for platform mechanics.
- Do not store credentials, provider payloads, command outputs, rich Artifact contents, or live process ids in this execplan.
- Promote durable dependencies into Isomer records before another role relies on them.

## Evidence Posture

Treat negative, failed, blocked, infeasible, null, and contradictory results as evidence. Publication and review work must not make unsupported claims sound stronger; route evidence gaps back to framing, experimentation, analysis, or master decision.
