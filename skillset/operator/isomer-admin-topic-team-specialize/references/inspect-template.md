# Inspect Template

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the selected Domain Agent Team Template registration and source path.
2. Inspect manifest metadata, `topic_instantiation_required`, placeholder catalog, instantiation schema path, copyable material declarations, and source-boundary diagnostics.
3. Inspect role definitions, role binding slots, required skills, Agent Workspace placeholders, Workflow Stage ownership, and workspace contract constraints.
4. Report unresolved or invalid template-layer material without converting placeholders into concrete topic values.
5. Return a template inspection summary suitable for placeholder reconciliation and profile bundle drafting.

If the user's task does not map cleanly to these steps, use your native planning tool to inspect only the template artifacts required by the requested decision, then execute the plan.

## Reference Routing

Read first:

- `execplan/manifest.toml`, `execplan/harness/refs/instantiation-parameters.toml`, and `execplan/specs/participants/participants.toml`.
- `execplan/specs/workspace/workspace.toml` when Agent Workspace or Topic Workspace placement matters.

Read as needed:

- `execplan/harness/schemas/topic-profile-instantiation.schema.json` for packet-facing schema expectations.
- Generated agent profiles only to understand placeholders, not to create live agents directly.

## Exit Criteria

- Placeholder names, role slots, copyable material, schema paths, and Workflow Stage ownership are explicit.
- Template-boundary errors or missing files are reported.
- No concrete Topic Agent Team Profile Bundle is written by this subcommand.

## Guardrails

- Do not edit Domain Agent Team Template source while specializing a topic.
- Do not convert template placeholders into concrete values inside template material.
- Do not use execution adapter mechanics as a replacement for Topic Team Specialization.
