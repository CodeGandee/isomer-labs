# Objective Contract

## Purpose

This generated contract defines the reusable objective of `deepsci-mini` at the Domain Agent Team Template layer. It is not a concrete Research Topic, Research Inquiry, Research Task, Run, Topic Workspace, Topic Agent Team Profile, or Agent Team Instance.

## Template Objective

`deepsci-mini` preserves a compact DeepScientist-inspired research-direction exploration method as a reusable Isomer Domain Agent Team Template. The method keeps one lead role, one scouting role, and one synthesis-review role; routes specialist handoffs through `deepsci-mini-lead`; records evidence and decisions through Isomer concepts; and leaves all topic-specific choices configurable for `{topic_agent_team_profile_id}`.

## Required Topic Inputs

- `{research_topic_id}`: concrete Research Topic.
- `{research_topic_config_ref}`: Project Manifest-registered topic configuration.
- `{topic_workspace_ref}`: Project Manifest-declared Topic Workspace.
- `{workspace_runtime_ref}`: runtime record authority for Research Inquiries, Research Tasks, Runs, Artifacts, Evidence Items, Findings, Gates, Decision Records, View Manifests, and Provenance Records.
- `{topic_agent_team_profile_id}`: topic-level specialization of this template.
- `{agent_team_instance_id}`: runtime team created from the topic profile.
- `{coordination_policy_ref}`: handoff, review, Peer Read Access, retry, escalation, and Gate routing policy.
- `{gate_policy_ref}`: governed-action preflight policy.
- Role-scoped `{capability_binding_ref}` and `{skill_binding_projection_ref}` values.

## Configurable Topic Profile Choices

- Source scope: which seed sources, repositories, datasets, benchmarks, or literature provider bindings scouting may inspect.
- Evidence posture: whether candidate Evidence Items require human review before becoming accepted Evidence Items.
- Finding posture: whether factor clusters are recorded as first-class Finding records or lifecycle records with file-backed metadata.
- Gate posture: how many follow-up inquiry options must be presented and which choices require human selection.
- Live posture: use adapter-simulated mode for deterministic validation or live Houmao mode behind explicit readiness checks.

## Non-Goals

- Do not store credentials, provider payloads, launch commands, mailbox routes, gateway routes, command outputs, live process ids, or concrete Project paths in this Domain Agent Team Template.
- Do not run experiments, baseline reproduction, paper writing, publication preparation, or task-level fanout.
- Do not use Research Inquiry as a Parallel Execution Scope.
- Do not turn Workflow Stages into one Agent Role per stage.
