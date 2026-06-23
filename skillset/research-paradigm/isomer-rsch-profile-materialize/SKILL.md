---
name: isomer-rsch-profile-materialize
description: Call generic Isomer validators and materializers to write approved Topic Agent Team Profile Bundles under the selected Topic Workspace.
---

# Isomer Profile Materialize

## Workflow

When this skill is invoked, execute the following steps in order.

1. Confirm the selected Research Topic, Topic Workspace, Domain Agent Team Template, packet path, and approval provenance.
2. Run generic packet and profile-bundle validation before mutation.
3. Materialize the approved Topic Agent Team Profile Bundle under `<topic-workspace>/team-profile/`, including `profile.toml`, packet, approval, validation, copied template material, and provenance files.
4. Report the Project Manifest registration ref that should point at the bundle's `profile.toml`.
5. Validate the Project Manifest and profile bundle after materialization.

If the user's task does not map cleanly to these steps, use your native planning tool to identify the missing packet, approval, or workspace input, then execute only validated materialization steps.

## Reference Routing

Read first:

- Approved Topic Team Instantiation Packet.
- Topic Workspace path and Domain Agent Team Template source path.

Read as needed:

- Project Manifest registration guidance.
- Validation diagnostics from previous draft or approval passes.

## Entry Signals

- The packet is approved and ready to write an authoritative topic profile bundle.
- A Project Operator Session needs to convert reviewable material into durable bundle files.

## Exit Criteria

- The bundle exists at `<topic-workspace>/team-profile/`.
- Validation output and provenance files are present.
- The Project Manifest registration guidance is explicit.

## Guardrails

- Do not write outside the selected Topic Workspace.
- Do not create a second active profile bundle for the same Research Topic.
- Do not hand-edit runtime state; use Workspace Runtime APIs after profile materialization.
