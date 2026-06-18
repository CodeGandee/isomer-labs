# Operator Guide

## Purpose

This file explains how an operator should use the generated execplan.

## Use

Treat this package as generated material for a Domain Agent Team Template. Edit `teams/deepsci-org/intention/` when the reusable template intent changes; regenerate `execplan/` afterward. Do not edit generated contracts as the long-term source of truth.

## Topic Instantiation

Before launch, create `{topic_agent_team_profile_id}` from `{domain_agent_team_template_ref}`. The topic profile must choose role set, stage tuning, expected Artifacts, Coordination Policy, Capability Binding refs, Skill Binding projection refs, Gate policy refs, Scheduler policy refs when automatic mode is allowed, literature provider refs, baseline-waiver policy refs, and allowed Research Operation Extension Point refs.

## Execution Stages

1. Prepare agents with the maintained Houmao agent-definition surfaces after the topic profile resolves concrete profile and skill facts.
2. Prepare workspaces with `houmao-utils-workspace-mgr` or equivalent manual readiness evidence from the workspace contract.
3. Validate loop readiness after agent and workspace facts exist.
4. Launch agents through maintained Houmao lifecycle surfaces.
5. Start the loop by sending the first `deepsci-org.email.team-start` trigger after agents are live.

## Control

First launch defaults to manual mode. Automatic mode requires topic-level Scheduler Policy, Gate Policy, Capability Binding, Skill Binding projection, and Completion Watcher Contract coverage. Stop, pause, resume, recovery, mode switching, manual stepping, gateway posture, notifier posture, mail delivery, mailbox operations, and lifecycle operations remain platform operations owned by maintained Houmao skills.
