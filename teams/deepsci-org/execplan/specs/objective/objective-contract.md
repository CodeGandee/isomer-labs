# Objective Contract

## Purpose

This generated contract defines the reusable objective of `deepsci-org` at the Domain Agent Team Template layer. It is not a concrete Research Topic, Research Inquiry, Research Task, Run, Topic Workspace, Topic Agent Team Profile, or Agent Team Instance.

## Template Objective

`deepsci-org` preserves a DeepScientist-inspired research method as a reusable Isomer Domain Agent Team Template. The method groups Agent Roles by context locality, routes specialist handoffs through `deepsci-org-master`, records evidence and Decisions through Isomer concepts, and leaves all topic-specific choices configurable for `{topic_agent_team_profile_id}`.

## Required Topic Inputs

- `{research_topic_id}`: concrete Research Topic.
- `{research_topic_config_ref}`: Project Manifest-registered topic configuration.
- `{topic_workspace_ref}`: Project Manifest-declared Topic Workspace.
- `{workspace_runtime_ref}`: runtime record authority for Research Inquiries, Research Tasks, Runs, Artifacts, Evidence Items, Findings, Research Claims, Gates, Decision Records, View Manifests, and Provenance Records.
- `{topic_agent_team_profile_id}`: topic-level specialization of this template.
- `{agent_team_instance_id}`: runtime team created from the topic profile.
- `{coordination_policy_ref}`: handoff, review, Peer Read Access, retry, escalation, and Gate routing policy.
- `{gate_policy_ref}`: governed-action preflight policy.
- `{scheduler_policy_ref}`: automatic dispatch and monitoring policy when automatic mode is enabled.
- Role-scoped `{capability_binding_ref}` and `{skill_binding_projection_ref}` values.

## Configurable Topic Profile Choices

- Role set: keep all seven default Agent Roles or remove roles that the topic profile does not need.
- Stage order: tune the default Workflow Stage routing table.
- Scalable roles: decide whether `deepsci-org-experimenter` or `deepsci-org-analyzer` fan out across multiple Agent Instances for one Research Task.
- Publication surface: choose internal report, paper draft, figure bundle, slide deck, venue-specific package, or no publication surface.
- Review posture: choose broad Peer Read Access, promoted Artifact-only review, or handoff-bundle-only review.
- Baseline posture: route heavy reproduction through `deepsci-org-framer`, `deepsci-org-experimenter`, or a Service Request.
- Automation posture: stay in manual mode or enable automatic mode with explicit policies and governed-resource limits.

## Non-Goals

- Do not store credentials, provider payloads, launch commands, mailbox routes, gateway routes, command outputs, live process ids, or concrete Project paths in this Domain Agent Team Template.
- Do not infer Topic Workspaces from directory scans.
- Do not use Research Inquiry as a Parallel Execution Scope.
- Do not turn Workflow Stages into one Agent Role per stage.
