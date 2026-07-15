# Show Skill Map

## Workflow

1. Print a compact direct-invocation table from user intent to active operator route.
2. Include the four visible research paths as first-class entries and explain the topology-versus-paradigm distinction.
3. Include `isomer-op-system-skill-mgr` for extension lifecycle and `isomer-op-entrypoint` for concrete route-and-proceed tasks.
4. Show DeepSci and Kaoju entry skills in a separate optional extension table without claiming host usability.
5. Keep service skills and research-stage internals out of ordinary first-click paths except as bounded support delegated by their owner.

If the user's task does not map cleanly to these steps, use your native planning tool to build the shortest useful skill map from active operator routes, package-catalog extension entry skills, and the user's goal, then state any missing decision.

## Direct Invocation Map

| Intent | Recommended Workflow | Route | Direct Invocation |
| --- | --- | --- | --- |
| Start manual or human-orchestrated research. | `start-research-manually` | `isomer-op-topic-creator` | `Use $isomer-op-topic-creator fast-forward` or `Use $isomer-op-topic-creator step-by-step`. |
| Start formal team-based research from a Domain Agent Team Template. | `start-research-by-agent-team` | `isomer-op-topic-team-specialize` | `Use $isomer-op-topic-team-specialize fast-forward`. |
| Start hypothesis-driven production research. | `start-deepsci-research` | `isomer-deepsci-pipeline` after readiness | `Use $isomer-op-entrypoint` with the concrete DeepSci goal when readiness is not established. |
| Start an evidence-led literature, code, dataset, or model survey. | `start-kaoju-survey` | `isomer-kaoju-pipeline` after readiness | `Use $isomer-op-entrypoint` with the concrete Kaoju goal when readiness is not established. |
| Give Isomer a concrete task and have it route and proceed. | Informed-user dispatch. | `isomer-op-entrypoint` | `Use $isomer-op-entrypoint` with the task. |
| Detect, reconcile, install, inspect, or repair optional system-skill extensions. | System-skill extension lifecycle. | `isomer-op-system-skill-mgr` | `Use $isomer-op-system-skill-mgr detect-extensions`, `status`, `install-extension`, or `repair`. |
| Initialize, validate, diagnose, or inspect the Project. | Project lifecycle workflow. | `isomer-op-project-mgr` | `Use $isomer-op-project-mgr check-project`, `list-topics`, `show-context`, or another Project subcommand. |
| Start, inspect, refresh, debug, troubleshoot, or look up backend APIs for the Project Web GUI. | Project Web GUI workflow. | `isomer-op-gui-mgr` | `Use $isomer-op-gui-mgr help`, `launch`, `status`, `api-reference`, `refresh-records`, or `troubleshoot`. |
| Act from a selected Topic Actor or Agent workspace cwd. | Operator identity posture switch. | `isomer-op-switch-identity` | `Use $isomer-op-switch-identity switch`, `act-as`, `status`, or `reset`. |
| Create, convert, install, inspect, update, disable, uninstall, or explain project-local Toolboxes, callback insertion points, callback declarations, or Toolbox Runtime Params. | Toolbox management workflow. | `isomer-op-toolbox-mgr` | `Use $isomer-op-toolbox-mgr help` or a specific Toolbox subcommand. |
| Manage an initialized Research Topic after Topic Creator handoff. | Initialized-topic management workflow. | `isomer-op-topic-mgr` | `Use $isomer-op-topic-mgr status` or a scoped initialized-topic subcommand. |
| Need Houmao adapter support during Project bootstrap or formal Agent Team work. | Owning operator workflow with service support. | `isomer-op-project-mgr`, or `isomer-op-topic-team-specialize` only with formal-team evidence | Use the owning operator workflow; it may delegate bounded support to `isomer-srv-houmao-interop`. |

## Optional Extension Entry Skills

| Research Goal | Package-Catalog Entry Skill | Example Public Surface |
| --- | --- | --- |
| Hypothesis development, experiments, analysis, decisions, writing, review, rebuttal, revision, or submission. | `isomer-deepsci-pipeline` | `$isomer-deepsci-pipeline` with a matching named pass. |
| Evidence-led surveys, source ingestion, bounded trials, comparisons, paper production, or wiki export. | `isomer-kaoju-pipeline` | `$isomer-kaoju-pipeline` with a matching named intent. |

Package-catalog presence does not prove Project declaration or current-host usability. Use `show-extensions` or `isomer-op-system-skill-mgr` before direct extension invocation when readiness is unknown.

Research paradigm and execution topology are independent. DeepSci or Kaoju does not imply a formal Agent Team, and manual or Agent Team setup does not select a paradigm.

Retired operator compatibility skills are not active routes. Service skills such as `isomer-srv-houmao-interop` are not first-click owner routes from this welcome surface.
