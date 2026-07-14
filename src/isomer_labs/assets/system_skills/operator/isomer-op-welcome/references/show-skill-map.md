# Show Skill Map

## Workflow

1. Print a compact direct-invocation table from user intent to active owner skill.
2. Include all active owner skills: `isomer-op-project-mgr`, `isomer-op-gui-mgr`, `isomer-op-switch-identity`, `isomer-op-toolbox-mgr`, `isomer-op-topic-creator`, `isomer-op-topic-mgr`, and `isomer-op-topic-team-specialize`.
3. Include the visible usage paths `start-research-manually` and `start-research-by-agent-team` as first-class entries.
4. Include direct invocation language with `$<skill-name>` for each owner skill.
5. Keep service skills and research-stage skills out of ordinary first-click paths, except as bounded support delegated by their owning operator workflow.

If the user's task does not map cleanly to these steps, use your native planning tool to build the shortest useful skill map from the active owner skills and state any missing decision.

## Direct Invocation Map

| Intent | Recommended Workflow | Owner Skill | Direct Invocation |
| --- | --- | --- | --- |
| Start manual or human-orchestrated research. | `start-research-manually` | `isomer-op-topic-creator` | `Use $isomer-op-topic-creator fast-forward` or `Use $isomer-op-topic-creator step-by-step`. |
| Start formal team-based research from a Domain Agent Team Template. | `start-research-by-agent-team` | `isomer-op-topic-team-specialize` | `Use $isomer-op-topic-team-specialize fast-forward`. |
| Initialize, validate, diagnose, or inspect the Project. | Project lifecycle workflow. | `isomer-op-project-mgr` | `Use $isomer-op-project-mgr check-project`, `list-topics`, `show-context`, or another Project subcommand. |
| Start, inspect, refresh, debug, troubleshoot, or look up backend APIs for the Project Web GUI. | Project Web GUI workflow. | `isomer-op-gui-mgr` | `Use $isomer-op-gui-mgr help`, `launch`, `status`, `api-reference`, `refresh-records`, or `troubleshoot`. |
| Act from a selected Topic Actor or Agent workspace cwd. | Operator identity posture switch. | `isomer-op-switch-identity` | `Use $isomer-op-switch-identity switch`, `act-as`, `status`, or `reset`. |
| Create, convert, install, inspect, update, disable, uninstall, or explain project-local Toolboxes, callback insertion points, callback declarations, or Toolbox Runtime Params. | Toolbox management workflow. | `isomer-op-toolbox-mgr` | `Use $isomer-op-toolbox-mgr help` or a specific Toolbox subcommand. |
| Manage an initialized Research Topic after Topic Creator handoff. | Initialized-topic management workflow. | `isomer-op-topic-mgr` | `Use $isomer-op-topic-mgr status` or a scoped initialized-topic subcommand. |
| Need Houmao adapter support during Project bootstrap or formal Agent Team work. | Owning operator workflow with service support. | `isomer-op-project-mgr`, or `isomer-op-topic-team-specialize` only when prompt or authoritative context establishes the formal Agent Team target | Use the owning operator workflow; it may delegate bounded support to `isomer-srv-houmao-interop`. Generic launch-facing work does not imply Topic Team Specialization. |

Retired operator compatibility skills are not active owner routes.

Service skills such as `isomer-srv-houmao-interop` are not first-click owner routes from this welcome surface.
