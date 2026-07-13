---
name: isomer-op-toolbox-mgr
description: Use when the user asks a Project Operator Session to create, convert, install, inspect, update, disable, uninstall, or explain project-local Isomer Toolboxes, Toolbox callback declarations, Toolbox Runtime Params, or Toolbox callback insertion points.
---

# Isomer Operator Toolbox Manager

## Overview

Use this operator skill to help users create and manage project-local Toolboxes. It authors Toolbox source material and composes existing `isomer-cli` Toolbox, User Skill Callback, Runtime Param, validation, and path-safety surfaces; it does not define new schemas or bypass CLI authority.

Toolbox skills default to routed or manual invocation. Author Toolbox skill metadata with `policy.allow_implicit_invocation: false`, and use callback prompt files to route agents to a named Toolbox skill and subcommand for a specific purpose.

## When to Use

Use this skill when the user wants to create a Toolbox, convert an existing skill into Toolbox callback material, insert a callback at a Callback Insertion Point, define or inspect Toolbox Runtime Params, install or manage a Toolbox, or list available insertion points.

Do not use this skill for marketplace publishing, dependency resolution, arbitrary external code execution, direct packaged system-skill mutation, or changes to Toolbox schemas, callback registry semantics, Runtime Param resolution, or CLI command behavior.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Default help mode**. If invoked without a concrete Toolbox task, select `help`, load [commands/help.md](commands/help.md), execute its workflow, and report its output.
2. **Resolve the Project and Toolbox context**. Identify Project root, Toolbox ID, source path, target skill, Callback Insertion Point, Toolbox-Local Key, Runtime Param keys, Toolbox Scope, topic selectors, and source skill paths when present. See **Concepts and Scope**.
3. **Select one subcommand** from the **Subcommands** tables. Prefer procedural subcommands for user-facing work; use helper subcommands only when the user explicitly asks for low-level authoring or a procedural command needs them.
4. **Load only the selected command page**. Execute that page's `## Workflow`, plus any local command page it explicitly names.
5. **Use existing authorities**. Author project-local Toolbox files directly when needed, but use `isomer-cli project toolboxes`, `isomer-cli project skill-callbacks`, and `isomer-cli project toolbox-params` for validation, install, callback refresh, Runtime Param mutation, and effective-state inspection.
6. **Report Toolbox output** using **Essential Output** by default and **Complete Output** when requested.

If the user's task does not map cleanly to these steps, use your native planning tool to build a bounded Toolbox plan from the subcommands, CLI boundaries, project context, scope constraints, diagnostics, and the user's intended Toolbox behavior, then execute the plan.

## Subcommands

Load only the selected command page before executing a subcommand.

### Procedural Subcommands

Procedural subcommands are user-facing Toolbox workflows. They may call helper subcommands internally, but they should present one coherent result to the user.

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `author-toolbox` | Create or update a complete Toolbox from freeform intent, an intent file, or a plain-language task | [commands/author-toolbox.md](commands/author-toolbox.md) |
| `convert-skill` | Convert an existing skill into Toolbox callback source material with manifest and Runtime Param guidance | [commands/convert-skill.md](commands/convert-skill.md) |
| `insert-callback` | Insert one Toolbox callback at a selected Callback Insertion Point | [commands/insert-callback.md](commands/insert-callback.md) |
| `define-runtime-params` | Design, import, set, unset, get, explain, or validate Toolbox Runtime Params | [commands/define-runtime-params.md](commands/define-runtime-params.md) |
| `manage-toolbox` | Validate, install, list, show, explain, enable, disable, update source, or uninstall Toolbox registration through `isomer-cli` | [commands/manage-toolbox.md](commands/manage-toolbox.md) |
| `identify-insertion-points` | List or explain callback insertion points available to Toolboxes | [commands/identify-insertion-points.md](commands/identify-insertion-points.md) |

### Helper Subcommands

Helper subcommands group CRUD-style work by target resource so the skill does not expose separate create, update, remove, list, and explain commands for the same material.

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `author-toolbox-source` | Create or update Toolbox directory skeletons, manifests, README notes, Toolbox skill directories, prompt router files, and default bundle files | [commands/author-toolbox-source.md](commands/author-toolbox-source.md) |
| `edit-callback-declarations` | Draft, add, update, or remove Toolbox manifest `[[callbacks]]` entries | [commands/edit-callback-declarations.md](commands/edit-callback-declarations.md) |
| `edit-runtime-params` | Declare Runtime Params, write bundles, register imports, set or unset explicit values, and explain effective values | [commands/edit-runtime-params.md](commands/edit-runtime-params.md) |
| `inspect-effective-state` | Inspect callback records, Runtime Params, Toolbox registration, gating, scope, and diagnostics without mutation | [commands/inspect-effective-state.md](commands/inspect-effective-state.md) |

### Misc Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `help` | Explain this skill, public subcommands, required inputs, output shape, and guardrails | [commands/help.md](commands/help.md) |

## Concepts and Scope

- **Toolbox**: a project-local bundle under `skillset/toolboxes/<toolbox-id>/` that can declare callback material and Runtime Param defaults.
- **Toolbox ID**: the stable Toolbox identity from the manifest `toolbox_id`.
- **Callback Insertion Point**: a declared target skill and stage pair, such as a packaged system skill's `begin` or `end` stage.
- **Toolbox Skill**: a project-local skill shipped inside a Toolbox. It should be routed by a callback prompt or invoked manually, and its `agents/openai.yaml` should set `allow_implicit_invocation: false` by default.
- **Toolbox-Local Key**: the callback or Runtime Param key authored inside one Toolbox. Installed callback ids use `<toolbox_id>:<toolbox-local-key>`.
- **Runtime Param**: a Toolbox-specific value whose effective id is `<toolbox_id>:<param-key>` while stored rows keep `toolbox_id` and `key` separate.
- **Toolbox Scope**: the Project, Research Topic, Topic Actor, or Topic Agent layer selected for registration, Runtime Param values, or effective-state inspection.

Default new Toolbox source to `skillset/toolboxes/<toolbox-id>/`. Block writes outside the Project root unless the user explicitly supplies an allowed external source path and the relevant CLI operation supports it.

## Output Contract

Default to **Essential Output** in chat. Use **Complete Output** when the user asks for complete, verbose, audit, debug, full handoff, or full output. Present either depth in natural-language Markdown. If the user explicitly requests JSON or another machine-readable format, serialize the applicable information in that format.

### Essential Output

Lead with the Toolbox operation outcome. Name the Toolbox, source path, and selected scope when relevant, then summarize changed files or identifiers, installed callbacks, Toolbox skill invocation posture, effective Runtime Params, validation, diagnostics, blockers, rollback guidance, and the next action.

### Complete Output

Include grouped details for commands run, project and scope selectors, authored paths, manifest entries, callback source refs, Runtime Param declarations and bundle rows, import rows, effective-state inspection, mutation summary, validation diagnostics, skipped work, rollback hints, and blockers.

## Guardrails

Do not edit packaged system skill files or the packaged system-skill manifest as part of Toolbox operations.

Do not mutate callback registries, Project Manifests, or Topic Workspace Manifests directly when an `isomer-cli` command owns that behavior.

Do not write credentials, tokens, passwords, private data, or secret-like values into Toolbox manifests, callback material, README notes, prompt files, or Runtime Param bundles. Report a blocker or redacted diagnostic instead.

Do not describe a Toolbox skill as automatically or implicitly invoked by default. Direct `skill_dir` callback sources are supplemental instruction material; use them only when that is the explicit requested shape.

Warn when Project scope could affect every compatible topic context. Warn again before disable, uninstall, or source replacement when the operation can broadly change callback behavior.

Use `--topic-agent` for Topic Agent selection. Keep Topic Actor and Topic Agent Runtime Param scope explicit.

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Splitting each CRUD operation into a separate helper command | Group operations by target resource, such as callback declarations or Runtime Params. |
| Treating callback ids and local keys as the same thing | Author local `key` values and report installed callback ids as `<toolbox_id>:<toolbox-local-key>`. |
| Letting Toolbox skills look implicitly auto-invoked | Add `agents/openai.yaml` with `allow_implicit_invocation: false`, and route through prompt-file callbacks or manual invocation. |
| Setting Runtime Params by editing TOML from memory | Use `isomer-cli project toolbox-params` for mutation and explanation unless a command is only drafting source bundles. |
| Installing before validating scope and insertion point | Validate manifest, target skill, stage, source paths, and scope before install or refresh. |
| Hiding broad effects in a short success message | Report selected scope, effective status, blockers, diagnostics, and rollback hints in Essential Output. |

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
