# Topic Context Resolution

## Workflow

When this subskill is selected, execute the following steps in order.

1. Resolve the selected Research Topic, Research Topic Config, Topic Workspace, and Effective Topic Context.
2. Read policy refs, Capability Binding refs, Skill Binding Projection refs, provider refs, Gate policy refs, and default execution mode from durable project material.
3. Inspect Workspace Runtime presence and Topic Environment Readiness status without treating runtime truth as profile configuration.
4. Return concrete refs that can fill a Topic Team Instantiation Packet or explicit blockers when refs are missing.
5. Record whether refs came from Project Manifest, Research Topic Config, local context, service output, or user selection.

If the user's task does not map cleanly to these steps, use your native planning tool to resolve only the topic refs needed for the requested artifact, then execute the plan.

## Reference Routing

Read first:

- Project Manifest, selected Research Topic Config, and local active context when present.
- Workspace Runtime inspection output when launch or Agent Workspace setup is in scope.

Read as needed:

- Domain Agent Team Template parameter catalog for required placeholder names.
- Policy or provider registration docs when a ref is ambiguous.

## Exit Criteria

- Concrete refs or named blockers exist for each requested placeholder.
- Runtime readiness is summarized as ready, missing, failed, stale, or blocked.
- Source attribution is attached to each resolved ref.

## Guardrails

- Do not write runtime observations into Topic Agent Team Profile material.
- Do not invent policy refs when none are configured.
- Do not bypass user approval for launch-facing profile bundle materialization.
