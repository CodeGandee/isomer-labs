# Show Skill Map

## Workflow

1. Print a compact direct-invocation table from user intent to active owner skill.
2. Include all active owner skills: `isomer-admin-project-mgr`, `isomer-admin-topic-creator`, `isomer-admin-topic-mgr`, `isomer-admin-topic-team-specialize`, and `isomer-admin-houmao-interop`.
3. Include the visible usage paths `start-research-manually` and `start-research-by-agent-team` as first-class entries.
4. Include direct invocation language with `$<skill-name>` for each owner skill.
5. Keep service skills and research-stage skills out of ordinary first-click paths, except as delegated owners named by their operator workflow.

If the user's task does not map cleanly to these steps, use your native planning tool to build the shortest useful skill map from the active owner skills and state any missing decision.

## Direct Invocation Map

| Intent | Recommended Workflow | Owner Skill | Direct Invocation |
| --- | --- | --- | --- |
| Start manual or human-orchestrated research. | `start-research-manually` | `isomer-admin-topic-creator` | `Use $isomer-admin-topic-creator fast-forward` or `Use $isomer-admin-topic-creator step-by-step`. |
| Start formal team-based research from a Domain Agent Team Template. | `start-research-by-agent-team` | `isomer-admin-topic-team-specialize` | `Use $isomer-admin-topic-team-specialize fast-forward`. |
| Initialize, validate, diagnose, or inspect the Project. | Project lifecycle workflow. | `isomer-admin-project-mgr` | `Use $isomer-admin-project-mgr check-project`, `list-topics`, `show-context`, or another Project subcommand. |
| Manage an initialized Research Topic after Topic Creator handoff. | Initialized-topic management workflow. | `isomer-admin-topic-mgr` | `Use $isomer-admin-topic-mgr status` or a scoped initialized-topic subcommand. |
| Explain or customize Houmao interop. | Houmao interop workflow. | `isomer-admin-houmao-interop` | `Use $isomer-admin-houmao-interop help` or a specific interop subcommand. |

Retired operator compatibility skills are not active owner routes.
