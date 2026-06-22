# DeepSci Mini Research Team Design

This document designs `deepsci-mini` as a compact Domain Agent Team Template for Isomer Labs UC-01 research-direction exploration. It follows DeepScientist practice, but it intentionally compresses the large `deepsci-org` team into three context-preserving Agent Roles so Milestone 6 can validate the end-to-end research recording path without the operational weight of seven participants.

## Source Basis

The design is grounded in these existing project materials:

- `.imsight-arts/project-explore/use-cases/uc-01-explore-new-research-direction.md` defines the desired UC-01 workflow: source collection, evidence extraction, inquiry comparison, skeptical check, Gate, and Decision Record.
- `context/design/project-goal.md` states that a research problem may need a narrow team and that users can override team composition.
- `context/explore/deepscientist-skill-analysis/` describes DeepScientist stage skills such as `scout`, `idea`, `analysis-campaign`, `review`, `decision`, and `finalize`.
- `teams/deepsci-org/` remains the full research organization template for larger milestones.

## Role Count

Use three core Agent Roles:

| Agent Role | Why It Exists | Context Kept Hot |
| --- | --- | --- |
| `deepsci-mini-lead` | Owns the team loop, handoff routing, Operator normalization, Gates, Decision Records, and closeout. | Research Topic state, Research Inquiries, handoffs, Gate state, Decision Records, closeout state. |
| `deepsci-mini-scout` | Combines source scouting and lightweight literature review because UC-01 needs bounded orientation before experimentation. | Seed sources, related papers, benchmark notes, source identity, candidate claims, Evidence Item candidates. |
| `deepsci-mini-synth-reviewer` | Combines synthesis and skeptical review because UC-01 needs defensible inquiry options, not full publication review. | Evidence Item candidates, factor clusters, weak claims, disagreement points, inquiry options, review notes. |

This is intentionally not a role-per-stage design. Workflow Stages remain visible in Coordination Policy and runtime records, but role boundaries follow context locality.

```text
Research Topic
  |
  v
deepsci-mini-lead
  |------ deepsci-mini-scout: source scouting + literature notes
  |------ deepsci-mini-synth-reviewer: evidence synthesis + skeptical review
  |
  v
Follow-up Research Inquiry Gate, Decision Record, View Manifests, durable Artifacts
```

## Skill Binding Projection

Install `isomer-rsch-shared` for every team role. It carries common evidence, handoff, terminology, provenance, and unsettled-surface rules.

| Agent Role | Required Skills | Optional Skills |
| --- | --- | --- |
| `deepsci-mini-lead` | `isomer-rsch-shared`, `isomer-rsch-intake`, `isomer-rsch-decision`, `isomer-rsch-finalize` | `isomer-rsch-review` when a final skeptical check is needed before a Gate. |
| `deepsci-mini-scout` | `isomer-rsch-shared`, `isomer-rsch-scout` | `isomer-rsch-baseline`, `isomer-rsch-science`, `isomer-rsch-paper-outline` when topic context requires them. |
| `deepsci-mini-synth-reviewer` | `isomer-rsch-shared`, `isomer-rsch-idea`, `isomer-rsch-analysis`, `isomer-rsch-review` | `isomer-rsch-science`, `isomer-rsch-paper-plot` for lightweight domain validation or diagnostic displays. |

## Manual Mode

`deepsci-mini` defaults to manual mode. The Operator Agent or Isomer CLI controls each handoff, observes candidate completion through the Houmao Execution Adapter or simulated adapter, and records accepted output through Workspace Runtime before any downstream dependency is built on it.

Manual mode is the right default for Milestone 6 because the main acceptance target is durable state and user-steered Gate resolution, not autonomous multi-stage continuation.

## UC-01 Acceptance Shape

The template is sufficient for UC-01 when one headless run can leave these durable records:

- Research Topic and initial Research Inquiry.
- Research Tasks for scouting and synthesis-review.
- Runs and handoff refs.
- Agent Team Instance and three Agent Instance refs.
- Source summary and literature note Artifacts.
- Claim candidates and Evidence Item refs or candidates.
- Synthesis and review note Artifacts.
- View Manifests for literature matrix, claim graph, and inquiry comparison.
- Follow-up Research Inquiry Gate.
- Selected Research Inquiry and Decision Record.
- Provenance Records linking handoffs to accepted outputs.

## Boundary

`deepsci-mini` is not a smaller `deepsci-org` Topic Agent Team Profile. It is its own Domain Agent Team Template. That distinction keeps the mini template honest: it has three default roles and simpler contracts, while `deepsci-org` remains available for later milestones that need baseline reproduction, implementation, analysis fanout, writing, and independent full review.
