# Map Research Skills to Workflow Stages and Agent Role Capabilities

## Status

accepted

## Context

DeepScientist stores research behavior as source-controlled skills. Its registry and prompts distinguish stage skills from companion skills. Existing Isomer team language distinguishes Domain Agent Team Templates, Topic Agent Team Profiles, Agent Team Instances, Agent Roles, Agent Profiles, Agent Instances, Workflow Stages, Capability Bindings, Coordination Policy, and Execution Adapters.

The migration should not turn every DeepScientist skill into a new Isomer concept or a mandatory standalone agent.

## Decision

Map migrated skills as capabilities that can be attached to Agent Roles and Workflow Stages. Team topology remains outside the skill bodies.

| Migrated skill area | Typical Isomer use |
| --- | --- |
| shared | Common contract used by all research Agent Roles and Workflow Stages |
| intake | Workflow Stage for auditing existing Artifacts, Evidence Items, Findings, and Decision Records before choosing work |
| scout | Workflow Stage or capability for research-scout and research-lead roles |
| baseline | Workflow Stage or capability for baseline selection, reproduction, comparison, acceptance, or waiver |
| idea | Workflow Stage or capability for hypothesis and candidate-direction generation |
| optimize | Capability for algorithm-first search, frontier tracking, and branch promotion |
| experiment | Workflow Stage or capability for implementing one selected route and recording Run evidence |
| analysis | Workflow Stage or capability for ablation, robustness, error, or failure analysis |
| decision | Capability for recording evidence-backed choices, Gates, branch selection, stopping, or reset |
| finalize | Workflow Stage or capability for claim consolidation and Research Thread closure |
| write, paper-outline | Capabilities for report or manuscript planning and drafting from existing evidence |
| paper-plot, figure-polish | Capabilities for durable figures and result visualization |
| review, rebuttal | Capabilities for skeptical audit, revision planning, reviewer-response mapping, and evidence-gap routing |
| science | Capability for scientific computation discipline, validation, and evidence-backed claims |

The generic team documentation can map roles such as research-lead, research-scout, research-designer, research-executor, research-writer, and research-reviewer to these skills. A Topic Agent Team Profile can adapt that mapping for a concrete topic. An Agent Team Instance can then launch concrete Agent Instances from the profile.

## Considered Options

- Create one Isomer Agent Role for every migrated DeepScientist skill.
- Encode one fixed team topology inside the skillset.
- Treat skills as capabilities and keep topology in team/profile documentation.

## Consequences

- The research-paradigm skills remain reusable across different team shapes.
- Agent Role, Workflow Stage, and Capability Binding stay separate.
- Houmao specialist names, mailboxes, gateways, launch dossiers, and provider-specific details remain Execution Adapter concerns, not skill requirements.
- Skills should state their expected inputs, outputs, Gates, and handoff expectations, but not require a specific running team topology.
