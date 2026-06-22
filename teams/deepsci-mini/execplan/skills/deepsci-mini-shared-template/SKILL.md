---
name: deepsci-mini-shared-template
description: Generated shared guardrails for deepsci-mini participants.
---

# deepsci-mini Shared Template

## Use When

Use this skill for any `deepsci-mini` participant work before handling team-start, handoff request, handoff result, tick, or operator-control tasks.

## Shared Rules

- Treat `deepsci-mini` as a Domain Agent Team Template until a Topic Agent Team Profile and Agent Team Instance provide concrete refs.
- Use Isomer domain terms in outputs: Research Topic, Research Inquiry, Research Task, Run, Artifact, Evidence Item, Finding, Gate, Decision Record, View Manifest, Provenance Record, Topic Workspace, Workspace Runtime, Agent Workspace.
- Keep Houmao-native refs in adapter payloads, manifests, or adapter tables.
- Do not treat raw mail, channel replies, file creation, or provider output as authoritative research state before `deepsci-mini-lead` normalization.
- Do not promote claim candidates to supported Research Claims without accepted Evidence Item refs.
- Stop at Gates, blockers, stale handoffs, unsupported claims, missing evidence, out-of-scope instructions, or destructive actions.
- Manual mode performs one bounded pass and stops; do not sleep, poll, tail logs, or wait in chat.

## UC-01 Durable Output Bias

Prefer small durable refs over broad prose. The useful UC-01 outputs are source summaries, literature notes, Evidence Item candidates, claim candidates, synthesis notes, review notes, inquiry options, View Manifest refs, a follow-up Research Inquiry Gate, a selected Research Inquiry, a Decision Record, and Provenance Records.
