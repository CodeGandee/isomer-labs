# Resolve Context

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the selected Research Topic, Research Topic Config, Topic Workspace, registration assurance evidence, and Effective Topic Context.
2. Read durable project refs when needed for static packet/profile material:
   - Include policy refs, Capability Binding refs, Skill Binding Projection refs, provider refs, Gate policy refs, and default execution mode.
3. Inspect topic environment setup status only when durable setup evidence is in scope.
4. Return concrete manifest-backed refs that can fill a Topic Team Instantiation Packet or explicit blockers when refs are missing or still provisional.
5. Record whether refs came from Project Manifest, Research Topic Config, local context, service output, or user selection.

If the user's task does not map cleanly to these steps, use your native planning tool to resolve only the topic refs needed for the requested artifact, then execute the plan.

## Reference Routing

Read first:

- Project Manifest, selected Research Topic Config, `ensure-topic-registration` evidence, and local active context when present.
- Topic environment setup records and Agent Workspace setup records when durable setup evidence is in scope.

Read as needed:

- Domain Agent Team Template parameter catalog for required placeholder names.
- Policy or provider registration docs when a ref is ambiguous.

## Exit Criteria

- Concrete refs or named blockers exist for each requested placeholder.
- Topic environment and Agent Workspace setup refs are summarized as ready, missing, deferred, or blocked when requested.
- Source attribution is attached to each resolved ref.

## Guardrails

- DO NOT write runtime observations, live process state, or adapter state into Topic Agent Team Profile material.
- DO NOT invent policy refs when none are configured.
- DO NOT bypass user approval for profile bundle materialization.
