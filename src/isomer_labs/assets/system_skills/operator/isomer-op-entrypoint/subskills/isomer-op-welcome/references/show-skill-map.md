---
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Show Skill Map

## Workflow

1. Print a compact direct-invocation table from user intent to active operator route.
2. Include the four visible research paths as first-class entries and explain the topology-versus-paradigm distinction.
3. Include `isomer-op-entrypoint->system-skills` for extension lifecycle and `$isomer-op-entrypoint` for concrete route-and-proceed tasks.
4. Show DeepSci and Kaoju entry skills in a separate optional extension table without claiming host usability.
5. Keep service skills and research-stage internals out of ordinary first-click paths except as bounded support delegated by their owner.

If the user's task does not map cleanly to these steps, use your native planning tool to build the shortest useful skill map from active operator routes, package-catalog extension entry skills, and the user's goal, then state any missing decision.

## Direct Invocation Map

| Intent | Recommended Workflow | Route | Public Invocation |
| --- | --- | --- | --- |
| Start manual or human-orchestrated research. | `start-research-manually` | `isomer-op-entrypoint->topic-create` | `$isomer-op-entrypoint use topic-create to fast-forward the requested setup` or guide it step by step. |
| Start formal team-based research from a Domain Agent Team Template. | `start-research-by-agent-team` | `isomer-op-entrypoint->topic-team` | `$isomer-op-entrypoint use topic-team to fast-forward specialization for the selected formal team`. |
| Start hypothesis-driven production research. | `start-deepsci-research` | `isomer-ext-deepsci-entrypoint` after readiness | `$isomer-ext-deepsci-entrypoint use <subcommand> to <task>` when ready, or `$isomer-op-entrypoint` with the concrete goal when readiness is unknown. |
| Start an evidence-led literature, code, dataset, or model survey. | `start-kaoju-survey` | `isomer-ext-kaoju-entrypoint` after readiness | `$isomer-ext-kaoju-entrypoint use <subcommand> to <task>` when ready, or `$isomer-op-entrypoint` with the concrete goal when readiness is unknown. |
| Give Isomer a concrete task and have it route and proceed. | Informed-user dispatch. | `isomer-op-entrypoint` | `$isomer-op-entrypoint` with the task. |
| Detect, reconcile, install, upgrade, inspect, or repair optional system-skill extensions. | System-skill extension lifecycle. | `isomer-op-entrypoint->system-skills` | `$isomer-op-entrypoint use system-skills to <task>`. |
| Initialize, validate, diagnose, or inspect the Project. | Project lifecycle workflow. | `isomer-op-entrypoint->project` | `$isomer-op-entrypoint use project to <task>`. |
| Start, inspect, refresh, debug, troubleshoot, or look up backend APIs for the Project Web GUI. | Project Web GUI workflow. | `isomer-op-entrypoint->gui` | `$isomer-op-entrypoint use gui to <task>`. |
| Act from a selected Topic Actor or Agent workspace cwd. | Operator identity posture switch. | `isomer-op-entrypoint->identity` | `$isomer-op-entrypoint use identity to <task>`. |
| Create, convert, install, inspect, update, disable, uninstall, or explain project-local Toolboxes, callback insertion points, callback declarations, or Toolbox Runtime Params. | Toolbox management workflow. | `isomer-op-entrypoint->toolbox` | `$isomer-op-entrypoint use toolbox to <task>`. |
| Manage an initialized Research Topic after Topic Creator handoff. | Initialized-topic management workflow. | `isomer-op-entrypoint->topic-manage` | `$isomer-op-entrypoint use topic-manage to <task>`. |
| Need Houmao adapter support during Project bootstrap or formal Agent Team work. | Owning operator workflow with service support. | `isomer-op-entrypoint->project`, or `isomer-op-entrypoint->topic-team` only with formal-team evidence | Use `$isomer-op-entrypoint` with the owning task; the route may delegate bounded protected service support. |

## Optional Extension Entry Skills

| Research Goal | Package-Catalog Entry Skill | Example Public Surface |
| --- | --- | --- |
| Hypothesis development, experiments, analysis, decisions, writing, review, rebuttal, revision, or submission. | `isomer-ext-deepsci-entrypoint` | `$isomer-ext-deepsci-entrypoint use <subcommand> to <task>`. |
| Evidence-led surveys, source ingestion, bounded trials, comparisons, paper production, or wiki export. | `isomer-ext-kaoju-entrypoint` | `$isomer-ext-kaoju-entrypoint use <subcommand> to <task>`. |

Package-catalog presence does not prove Project declaration, complete protected coverage, or current-session usability. Use `show-extensions` or `$isomer-op-entrypoint use system-skills to inspect readiness` before direct extension invocation when readiness is unknown.

Research paradigm and execution topology are independent. DeepSci or Kaoju does not imply a formal Agent Team, and manual or Agent Team setup does not select a paradigm.

Retired operator compatibility skills and protected service logical ids are not first-click routes from this welcome surface.
