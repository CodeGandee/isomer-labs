# Manage Paper Template

## Workflow

1. Resolve the current Topic Workspace, requested action, explicit template name or ref, explicit source path or export path, actor, and authorization boundary. Canonical templates form one flat namespace of mutable `KAOJU:PAPER-TEMPLATE-MYST` directory trees. `main` is the default for ordinary paper use and export.
2. When the request supplies a template name, canonical ref, template path, or export path, validate and use that explicit locator. Do not replace it through implicit discovery.
3. Only when the user asks to update the template in the current artifacts database without any locator, discover the source in this exact order:

   1. Run `isomer-cli --print-json ext kaoju paper template exports` and recompute registered export status. If exactly one eligible export is `edited`, select its path and recorded target name.
   2. If several exports are edited, identity-invalid, or make duplicate claims, present their concrete names, refs, paths, tokens, and digests and ask the user which source to use. Do not select by time or record order.
   3. If no edited export qualifies, resolve `topic.paper.template_exchange_root` through Workspace Path Resolution and inspect its `main/` child. If that directory exists, use it as source and target name `main`, even when the artifacts database has no template named `main`.
   4. If neither source exists, ask the user for a concrete template or path. Do not select an unrelated database record.

4. For an arbitrary directory, inspect the source tree and current canonical target tree, identify intended entrypoints and use guidance, interpret structural differences, resolve authorized changes, and prepare a clean candidate without `.isomer-template-export.json`. Isomer CLI checks integrity and concurrency but does not convert, interpret, or merge arbitrary trees.
5. Ask the user about any material structure, content, evidence, or entrypoint choice that the request does not authorize. Record the agent assessment, source refs, and change summary before mutation.
6. Run the applicable low-level operation:

   - `list` or `show`: query exact named state and report stable ref, state token, tree digest, authored metadata, status, and default working path.
   - `create`: use `template create --name NAME --from PATH` for a new prepared tree. A missing target never turns update into create silently.
   - `copy`: use `template create --name NEW --from-template EXISTING` when the user asks to save or preserve current state under another ordinary name. The copied name remains independently mutable and receives no special classification.
   - `update`: use `template update --name NAME --from PATH --expected-state TOKEN` only after agent preparation and assessment.
   - `replace`: use `template update --name TARGET --from-template SOURCE --expected-state TOKEN` for an explicit exact replacement. It performs no merge and leaves the source unchanged.
   - `merge`: inspect both inputs, construct a new candidate, and invoke update from that candidate. Never request a generic CLI merge.
   - `file put`, `file remove`, or `metadata patch`: use these only for an explicitly bounded low-level edit with the current token.
   - `export`: use `template export`, defaulting to canonical `main` and resolved `intent/derived/writing-template/main/`. The stable working directory is non-canonical.
   - `observe`: after agent reconciliation of a working tree, use `template export --observe --target PATH`; observation does not promote the tree.
   - `archive` or `delete`: supply the current token and stop when durable paper state still references the template.

7. Before replacing named state, report the target name, stable ref, current token and digest, selected source, and whether the user requested an ordinary named copy first. Ordinary updates create no additional name and retain no prior template bytes as restorable state.
8. If the target changes after inspection, report the lost-update conflict, reread state, and reconcile again. Do not retry with a stale token.
9. Record affected stable and audit refs, resulting token and digest, named-copy action if any, and checkpoint the Run at the first incomplete stage.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this command, its required inputs, and the user's request, then execute the plan.

## Owner, Inputs, and Outputs

Owner: `$isomer-kaoju-write`; CLI: `isomer-cli ext kaoju paper template list|show|create|update|file|metadata|archive|delete|exports|export|migrate`. Inputs: exact named state or one prepared agent-assessed tree, current expected token for destructive operations, actor ref, and source assessment. Outputs: stable template ref, name, token, tree digest, authored metadata, mutation-audit ref, working-copy observation, diagnostics, and next action.

## Gates, Blockers, and Resume

An ambiguous unnamed source, material unresolved choice, missing target, stale token, unsafe path, reserved file, corrupt tree, edited export target, identity conflict, or durable dependent causes no canonical mutation. Resume at user selection, agent assessment, candidate preparation, explicit create, state refresh, export reconciliation, or the requested low-level operation.
