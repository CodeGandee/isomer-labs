---
name: isomer-rsch-template-inspect
description: Inspect Domain Agent Team Template manifests, placeholder catalogs, role bindings, workflow stages, workspace contracts, and diagnostics.
---

# Isomer Template Inspection

## Workflow

When this skill is invoked, execute the following steps in order.

1. Resolve the selected Domain Agent Team Template registration and source path.
2. Inspect manifest metadata, `topic_instantiation_required`, placeholder catalog, instantiation schema path, copyable material declarations, and source-boundary diagnostics.
3. Inspect role definitions, role binding slots, required skills, Agent Workspace placeholders, workflow stage ownership, and workspace contract constraints.
4. Report unresolved or invalid template-layer material without converting placeholders into concrete topic values.
5. Return a template inspection summary suitable for placeholder reconciliation and profile bundle drafting.

If the user's task does not map cleanly to these steps, use your native planning tool to inspect only the template artifacts required by the requested decision, then execute it.

## Reference Routing

Read first:

- `execplan/manifest.toml`, `execplan/harness/refs/instantiation-parameters.toml`, and `execplan/specs/participants/participants.toml`.
- `execplan/specs/workspace/workspace.toml` when Agent Workspace or Topic Workspace placement matters.

Read as needed:

- `execplan/harness/schemas/topic-profile-instantiation.schema.json` for packet-facing schema expectations.
- Generated agent profiles only to understand placeholders, not to launch agents directly.

## Entry Signals

- Topic Team Specialization needs the template's placeholder catalog and role binding slots.
- A Project Operator Session or Topic Service Agent must confirm whether a template is reusable and not directly launchable.

## Exit Criteria

- Placeholder names, role slots, copyable material, schema paths, and workflow stage ownership are explicit.
- Template-boundary errors or missing files are reported.
- No concrete Topic Agent Team Profile Bundle is written by this skill.

## Guardrails

- Do not edit Domain Agent Team Template source while specializing a topic.
- Do not convert template placeholders into concrete values inside template material.
- Do not use Houmao adapter mechanics as a replacement for Topic Team Specialization.
