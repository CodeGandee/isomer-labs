# Operator Guide

## Purpose

This generated support document explains how an operator should use the `deepsci-mini` execplan without confusing generated loop material with Isomer Workspace Runtime truth.

## Contents

## Creation and Specialization

Before launch, create a `{topic_agent_team_profile_id}` from `deepsci-mini`. The topic profile must choose concrete role bindings, expected UC-01 Artifacts, Coordination Policy, Gate Policy, Skill Binding projection refs, Capability Binding refs, and adapter posture.

## Default Team

- `deepsci-mini-lead`: internal root, handoff normalizer, Gate owner, and Decision Record steward.
- `deepsci-mini-scout`: source scouting and lightweight literature note specialist.
- `deepsci-mini-synth-reviewer`: evidence synthesis, inquiry comparison, and skeptical review specialist.

## Suggested UC-01 Manual Flow

1. Resolve Effective Topic Context for the selected Research Topic.
2. Create or reuse a `deepsci-mini` Topic Agent Team Profile.
3. Create an Agent Team Instance with one Agent Instance per role.
4. Start the lead.
5. Dispatch one scout handoff.
6. Normalize accepted scout output into Workspace Runtime.
7. Dispatch one synthesis-review handoff.
8. Normalize accepted synthesis-review output into Workspace Runtime.
9. Write View Manifest refs for literature matrix, claim graph, and inquiry comparison.
10. Open a follow-up Research Inquiry Gate.
11. Record the selected inquiry and rationale as a Decision Record.

## Platform Boundaries

Use maintained Houmao skills for platform mechanics: agent launch, mailbox operations, gateway posture, workspace preparation, memory, and inspection. Generated `deepsci-mini` skills own loop semantics only.
