# Instantiation Guide

## Purpose

This generated guide explains how to turn the `deepsci-org` Domain Agent Team Template into a configurable Topic Agent Team Profile.

## Steps

1. Resolve `{project_manifest_ref}`, `{research_topic_id}`, `{research_topic_config_ref}`, `{topic_workspace_ref}`, and `{workspace_runtime_ref}` from Effective Topic Context.
2. Create `{topic_agent_team_profile_id}` from `{domain_agent_team_template_ref}`.
3. Choose whether all seven default Agent Roles remain active for the topic.
4. Replace role-scoped Agent Profile, Capability Binding, Skill Binding projection, and Agent Workspace placeholders.
5. Select Coordination Policy, Gate Policy, Scheduler Policy when automatic mode is allowed, literature provider bindings, baseline-waiver policy, and Artifact Format Profile refs.
6. Decide whether `deepsci-org-experimenter` or `deepsci-org-analyzer` can fan out for task-level parallel execution.
7. Decide whether `deepsci-org-reviewer` has broad Peer Read Access or only promoted Artifact and declared handoff access.
8. Validate the generated package and the topic profile before preparing agents.

## Configurable Defaults

Manual mode is the first-launch default. Automatic mode is a topic-level opt-in. Heavy baseline reproduction, Nature-family companions, review Peer Read Access, fanout thresholds, and publication surfaces are intentionally configurable.
