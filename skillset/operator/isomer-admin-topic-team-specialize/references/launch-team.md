# Launch Team

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Confirm that the selected Topic Agent Team Profile comes from an approved profile bundle or an explicitly supported legacy path.
2. Validate Workspace Runtime initialization, Topic Environment Readiness, profile provenance, Agent Team Instance creation inputs, and launch blockers.
3. Create or select the Agent Team Instance through Workspace Runtime APIs, then inspect Agent Instance and Agent Workspace records.
4. Route launch materialization or quick launch through the Houmao Execution Adapter using approved profile bundle and runtime records.
5. Record adapter diagnostics, command refs, payload refs, launch refs, and operator provenance without storing adapter reasoning as topic-profile material.

If the user's task does not map cleanly to these steps, use your native planning tool to separate profile validation, runtime creation, and adapter launch into explicit steps, then execute the safe subset.

## Reference Routing

Read first:

- Materialized Topic Agent Team Profile Bundle.
- Workspace Runtime readiness and Agent Team Instance summary.

Read as needed:

- Houmao adapter docs and manifest refs when launch materialization is requested.
- Existing launch-preparation support outputs.

## Exit Criteria

- Runtime records or adapter launch records show the requested state.
- Project operator and support provenance refs are preserved.
- Any launch blockers are reported before Houmao mutation.

## Guardrails

- Do not launch from Domain Agent Team Template material alone.
- Do not launch preview-only Topic Agent Team Profile output.
- Do not add Project Operator Sessions or support actors as research team members unless the profile defines that role.
