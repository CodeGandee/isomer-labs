# deepsci-mini Team Specialization Guide

This guide explains how a Project Operator Session should understand and specialize the copied `deepsci-mini` execplan for one Research Topic. Read this file after the Domain Agent Team Template material has been copied into the Topic Agent Team Profile Bundle, before changing topic-facing instructions, placeholders, or contract refs.

## Source Boundary

`teams/deepsci-mini/execplan/` is Domain Agent Team Template material. Topic-specific edits belong in the copied template root, usually `<topic-workspace>/team-profile/execplan/`, not in the source template.

## Placeholders and Definitions

- `research_topic_id`: the selected Research Topic id from the Project Manifest or Research Topic Config.
- `research_inquiry_id`: the first inquiry, question, or run intent that the team should explore for this topic.
- `topic_workspace_ref`: the Topic Workspace path or ref that owns the topic-specific profile bundle.
- `workspace_runtime_ref`: the Workspace Runtime store that records runtime truth, handoffs, Artifacts, Decisions, and provenance.
- `topic_agent_team_profile_bundle_ref`: the Topic Agent Team Profile Bundle root, normally `<topic-workspace>/team-profile/`.
- `topic_agent_team_profile_id`: the stable profile id for this topic's one dedicated `deepsci-mini` team.
- `gate_policy_ref`: the Gate policy that tells the lead when to ask for user approval, repair, branch, park, or close decisions.
- `coordination_policy_ref`: the policy that defines manual or automatic coordination posture, wakeups, and handoff limits.
- `<role>.agent_profile_ref`: the concrete agent profile selected for `deepsci-mini-lead`, `deepsci-mini-scout`, or `deepsci-mini-synth-reviewer`.
- `<role>.capability_binding_ref`: the concrete capability binding for tools, model posture, credentials, hardware, or provider constraints for that role.
- `<role>.skill_projection_ref`: the concrete Skill Binding Projection for the role's installed research, operator, service, Houmao, or platform skills.
- `<role>.agent_workspace_ref`: the Agent Workspace path assigned to that role under the Topic Workspace.

The harness reference file `harness/refs/instantiation-parameters.toml` is the machine-readable placeholder source for this generated execplan package. Treat this guide as the operator-facing explanation of how to use those values during Topic Team Specialization.

## Assumptions

- One Research Topic is handled by one dedicated topic-level `deepsci-mini` team.
- The copied execplan is topic-owned material inside the Topic Agent Team Profile Bundle, and the Project Manifest keeps only a ref to that bundle.
- The source `deepsci-mini` template stays topic-neutral and must not contain GB10, UC-01, UC-07, credential, provider, or workspace values unless those values are examples clearly marked as examples.
- The default control mode is manual. Automatic control needs explicit topic policy, Scheduler Policy, Gate policy, and completion watcher refs.
- Topic Service Agents can help with environment setup, diagnostics, credential checks, or workspace support, but they are not members of the research team loop.
- Launch needs an approved Topic Team Instantiation Packet, a valid Topic Agent Team Profile Bundle, Workspace Runtime readiness, and adapter preflight. The copied execplan alone is not a launch authority.

## Team Workflow

`deepsci-mini` is a compact tree-loop with three roles. `deepsci-mini-lead` is the internal root role. The lead starts or resumes a bounded run, normalizes incoming specialist outputs into Workspace Runtime, opens Gates, records Decision Records, and decides whether the next bounded step should scout, synthesize, review, park, repair, or close.

`deepsci-mini-scout` performs source scouting and lightweight evidence capture. It should return bounded source notes, implementation notes, hardware or method facts, baseline observations when available, and evidence candidates to the lead through the handoff-result contract.

`deepsci-mini-synth-reviewer` compares the scout output, clusters candidate directions, checks weak claims, flags unsupported recommendations, and returns ranked options or review notes to the lead. It does not dispatch other participants.

## Contracts Used by the Team

- Manifest contract: `manifest.toml` declares template identity, topology, copyable material, mode posture, and generated package metadata.
- Participant contract: `specs/participants/participants.toml` declares the three roles, owned artifacts, and root role.
- Collaboration contract: `specs/collab/collab-overview.md` and `specs/collab/topology/topology.toml` define the tree-loop routing shape.
- Communication contracts: `specs/comms/schemas/*.schema.json` and `specs/comms/renderers/*.md.j2` define team-start, handoff-request, and handoff-result messages.
- State contract: `specs/state/state-model.md` explains what progress state the lead should read or update before scheduling the next bounded step.
- Harness contract: `harness/bin/deepsci-mini` and `harness/refs/instantiation-parameters.toml` expose validation, query, control, and placeholder views for the generated package.
- Isomer profile contracts: the Topic Team Instantiation Packet and Topic Agent Team Profile Bundle record topic values, copied material refs, approval provenance, and launch blockers.

## Cooperation Example

For a GB10 Flash Attention 4 Research Topic, the operator copies this execplan into `<topic-workspace>/team-profile/execplan/`, resolves the topic and role placeholders, and edits copied prompt material so the team asks GB10-specific scouting and review questions. The lead opens a bounded run and asks the scout to gather source notes about GB10 execution features, attention kernel shape families, precision modes, and baseline constraints. The scout returns a handoff result with evidence candidates. The lead normalizes that result, then asks the synthesis-reviewer to compare candidate optimization directions and flag claims that are generic or unsupported by GB10 evidence. The synthesis-reviewer returns ranked options and review notes. The lead opens a Gate for the user to accept a follow-up inquiry, request repair, branch, or park the topic with a resume packet.

## Specialization Steps

1. Create `team-specialization-plan.md` beside this guide in the copied template root.
2. List topic context, copied root path, placeholder resolutions, planned prompt edits, validation commands, and launch blockers in the plan before editing.
3. Rewrite copied files that mention generic UC-01, research-direction, placeholder, policy, artifact, or role-binding language so they match the selected Research Topic.
4. Keep topic edits narrow and explicit. Do not silently change source template semantics when a packet deferral or launch blocker would be more honest.
5. After editing, add a `Final Report` section to the plan with completed edits, deferred edits, generated-guide status, validation status, packet/profile outputs, and unresolved blockers.

## Guardrails

Do not edit this file in the source template for a specific topic. Edit the copied file under the topic's `team-profile/execplan/` root.

Do not create a topic-level `teams/` directory inside the Topic Workspace. Topic-specific team material belongs under `team-profile/`.

Do not skip packet/profile validation or adapter preflight because the team is manual-mode. Manual mode changes scheduling posture; it does not remove Isomer provenance or launch boundaries.
