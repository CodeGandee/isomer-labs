---
name: isomer-rsch-topic-profile-draft
description: Draft reviewable Topic Agent Team Profile Bundle material from a validated Topic Team Instantiation Packet.
---

# Isomer Topic Profile Draft

## Workflow

When this skill is invoked, execute the following steps in order.

1. Read the validated Topic Team Instantiation Packet and selected Domain Agent Team Template inspection summary.
2. Draft the reviewable Topic Agent Team Profile Bundle contents: profile fields, role bindings, policy refs, expected Artifacts, copied material plan, proposed topic edits, launch blockers, and provenance refs.
3. Preview copied or rewritten template material that will live under `<topic-workspace>/team-profile/`.
4. Run or request save-time profile validation and capture diagnostics without treating preview material as authoritative.
5. Return the draft bundle summary and review checklist for approval.

If the user's task does not map cleanly to these steps, use your native planning tool to draft only the requested profile-bundle material and list missing packet inputs, then execute it.

## Reference Routing

Read first:

- Topic Team Instantiation Packet.
- Domain Agent Team Template copyable material declarations and placeholder catalog.

Read as needed:

- Selected Topic Workspace path and Workspace Runtime readiness when Agent Workspace refs are included.
- Topic Service Agent support Artifacts for copied material or topic edits.

## Entry Signals

- A packet has enough resolved placeholders to preview a profile bundle.
- A user needs to review role, policy, copied material, or launch blocker choices before approval.

## Exit Criteria

- The draft profile bundle summary is reviewable.
- Save-time validation diagnostics are reported.
- Approval requirements and launch blockers are explicit.

## Guardrails

- Do not write authoritative profile bundle material without approval provenance.
- Do not mark synthetic preview material as launchable.
- Do not include rich research outputs or credentials in profile bundle files.
