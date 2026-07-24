---
skill_invocation_notation: >
  Top-level skill entrypoints use SKILL.md. Parent-scoped subskill entrypoints use
  SKILL-MAIN.md and are loaded explicitly through their parent; nested SKILL.md is
  accepted only as legacy input when SKILL-MAIN.md is absent.
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Manage Paper Template

## Subcommands

`manage-paper-template()` is a terminal task selector when invoked without a child. It presents these actions and waits for or infers exactly one selection from the user's task. `--kind content|latex` is a role parameter for every applicable action; `content` and `latex` never become route components.

| Child Command | Use For | Detail |
| --- | --- | --- |
| `isomer-ext-kaoju-entrypoint->manage-paper-template()->list()` | List named stock in one role. | [commands/manage-paper-template/list.md](commands/manage-paper-template/list.md) |
| `isomer-ext-kaoju-entrypoint->manage-paper-template()->show()` | Inspect one named template. | [commands/manage-paper-template/show.md](commands/manage-paper-template/show.md) |
| `isomer-ext-kaoju-entrypoint->manage-paper-template()->create()` | Create named stock from an assessed directory. | [commands/manage-paper-template/create.md](commands/manage-paper-template/create.md) |
| `isomer-ext-kaoju-entrypoint->manage-paper-template()->copy()` | Copy named stock within one role. | [commands/manage-paper-template/copy.md](commands/manage-paper-template/copy.md) |
| `isomer-ext-kaoju-entrypoint->manage-paper-template()->update()` | Update named stock from an assessed directory. | [commands/manage-paper-template/update.md](commands/manage-paper-template/update.md) |
| `isomer-ext-kaoju-entrypoint->manage-paper-template()->replace()` | Replace named stock from another template in the same role. | [commands/manage-paper-template/replace.md](commands/manage-paper-template/replace.md) |
| `isomer-ext-kaoju-entrypoint->manage-paper-template()->merge()` | Build and apply an assessed merged candidate. | [commands/manage-paper-template/merge.md](commands/manage-paper-template/merge.md) |
| `isomer-ext-kaoju-entrypoint->manage-paper-template()->file()` | Select a bounded file mutation. | [commands/manage-paper-template/file.md](commands/manage-paper-template/file.md) |
| `isomer-ext-kaoju-entrypoint->manage-paper-template()->metadata()` | Select a bounded metadata mutation. | [commands/manage-paper-template/metadata.md](commands/manage-paper-template/metadata.md) |
| `isomer-ext-kaoju-entrypoint->manage-paper-template()->export()` | Export a non-canonical working tree. | [commands/manage-paper-template/export.md](commands/manage-paper-template/export.md) |
| `isomer-ext-kaoju-entrypoint->manage-paper-template()->observe()` | Observe an assessed exported tree without promotion. | [commands/manage-paper-template/observe.md](commands/manage-paper-template/observe.md) |
| `isomer-ext-kaoju-entrypoint->manage-paper-template()->archive()` | Archive unused named stock with its current token. | [commands/manage-paper-template/archive.md](commands/manage-paper-template/archive.md) |
| `isomer-ext-kaoju-entrypoint->manage-paper-template()->delete()` | Delete unused named stock with its current token. | [commands/manage-paper-template/delete.md](commands/manage-paper-template/delete.md) |
| `isomer-ext-kaoju-entrypoint->manage-paper-template()->migrate()` | Preview or apply an explicit role-aware migration. | [commands/manage-paper-template/migrate.md](commands/manage-paper-template/migrate.md) |

## Workflow

1. Consume the entrypoint's reconciled Research Topic and Topic Workspace, then retain `--topic TOPIC` on every applicable typed template call in this workflow. Resolve the requested action, actor, authorization boundary, and template role before source discovery. When no child command or unambiguous task is supplied, return the Subcommands table as the terminal result instead of guessing. Use role `content` for MyST structure, sections, drafting, or content-template language. Use role `latex` for LaTeX, TeX, a document class, style files, publisher or venue bundles, presentation, or PDF layout. Ask one role question only when the surrounding request cannot distinguish them. Each role has its own named namespace and its own `main`; never infer one role from the other role's files or records.
2. Map “export the LaTeX template for me to edit”, “get the LaTeX template”, and equivalent named-stock editing requests to `manage-paper-template()->export()` with role `latex`, name `main` unless explicitly named, and `isomer-cli --print-json ext kaoju paper template export --topic TOPIC --kind latex --name main` without `--target`. Use the CLI-resolved `<topic.paper.template_exchange_root>/latex/main/` path; do not construct a Topic Actor, Agent, Topic Main, cwd-relative, or other fallback path. A request to fill or repair the current paper TeX instead selects the paper-local `KAOJU:PAPER-DRAFT-TEX` and its `.isomer-kaoju-tex-fill.json` contract; it does not export or mutate named stock.
3. Resolve an explicit role-local name, stable ref, source directory, or export path directly. An omitted name means `main` only after the role is known. New calls always pass `--kind content` or `--kind latex`; omission is a compatibility default for content, not agent guidance.
4. Only when the user asks to update stocked state without a source locator, discover inside the selected role in this exact order:

   1. Run `isomer-cli --print-json ext kaoju paper template exports --kind KIND` and recompute registered export status. If exactly one eligible export is `edited`, select its path and recorded target name.
   2. If several selected-role exports are edited, identity-invalid, or make duplicate claims, present their concrete names, refs, paths, tokens, and digests and ask the user which source to use. Same-named exports of the other role are ineligible.
   3. If no edited export qualifies, resolve `topic.paper.template_exchange_root` and inspect `<root>/<kind>/main/`. If it exists, use it as source and target name `main`, even when the database has no selected-role `main`.
   4. During content migration only, report a recognized legacy `<root>/<name>/` export as a compatibility source. Never infer that a legacy root child is LaTeX from its path or file extensions alone.
   5. If no selected-role source exists, ask for a concrete directory or ref. Do not select by timestamp, paper line, path order, or the other role's database records.

5. Inspect arbitrary source and current target trees before mutation. For a content template, identify the MyST entrypoint, configuration, typed structure, placeholders, and use guidance. For a LaTeX template, preserve the multi-file tree and require a safe `.tex` entrypoint plus `extensions.latex` metadata with `composition_mode`, registered `build_profile`, `source_provenance`, and `license_posture`; require `marker` for marker mode, `body_path` for include mode, or an optional distinct `generated_entrypoint` for preamble mode. Prepare a clean candidate when source interpretation or merge is required.
6. Ask about any material structure, content, evidence, composition, entrypoint, build-profile, provenance, or licensing choice that the request does not authorize. Record the assessment, source refs, and change summary before mutation.
7. Run the applicable role-explicit operation. Every command below includes `--topic TOPIC` in addition to the shown role, name, source, and concurrency arguments:

   - `list` or `show`: run with `--kind KIND` and report role, name, stable ref, state token, tree digest, authored metadata, status, and default working path.
   - `create`: run `template create --kind KIND --name NAME --from PATH`; omitted names resolve selected-role `main`. A missing target never turns update into create silently.
   - `copy`: run `template create --kind KIND --name NEW --from-template EXISTING`. Source and target remain inside one role.
   - `update`: run `template update --kind KIND --name NAME --from PATH --expected-state TOKEN`. A recognized edited export may be supplied directly; the service strips only its reserved observation metadata and verifies role, ref, and token.
   - `replace`: run `template update --kind KIND --name TARGET --from-template SOURCE --expected-state TOKEN`. It performs no merge and leaves the source unchanged.
   - `merge`: inspect both inputs, construct a new selected-role candidate, and update from that directory. Never request a generic CLI merge.
   - `file put`, `file remove`, or `metadata patch`: use `--kind KIND` only for an explicitly bounded edit with the current token.
   - `export`: run `template export --kind KIND --name NAME`; the default path is `<exchange-root>/<kind>/<name>/` and remains non-canonical.
   - `observe`: after assessment, run `template export --kind KIND --name NAME --observe --target PATH`; observation does not promote the tree.
   - `migrate`: preview with `template migrate --kind KIND`. Apply content contract annotation with `--kind content --apply`. Adopt LaTeX only with `--kind latex --apply --record EXACT_REF --metadata-file FILE`; use `--expected-state` when replacing existing stock. Adoption copies the source and never mutates historical records.
   - `archive` or `delete`: pass `--kind KIND` and the current token; stop when durable paper state still references the selected stable ref.

8. Before replacing named state, report the role, target name, stable ref, current token and digest, selected source, and whether the user requested an ordinary named copy first. Ordinary updates create no additional name and retain no prior stock bytes as restorable state; used LaTeX states remain reproducible through paper-line TeX snapshots.
9. If target state changes after inspection, report the lost-update conflict, reread selected-role state, and reconcile again. Never retry with a stale token or switch roles to find a matching name.
10. Keep paper-specific TeX repair separate from LaTeX stock. A repaired `KAOJU:PAPER-DRAFT-TEX` stays paper-local. Promote repairs only when the user explicitly requests a LaTeX-template update and the assessed candidate passes the normal named-state workflow.
11. On a typed failure, compare returned selected-context metadata with the pinned Research Topic. Preserve the target and canonical exchange surface; stop, correct selectors, rerun context alignment, or route to the owning readiness workflow. Do not search sibling topics or replace failed export with `cp`, a raw filesystem copy, `--target` to another location, or an actor-local path unless the user separately requests an unmanaged copy.
12. Return affected stable and audit refs, role, name, resulting token and digest, selected-context metadata, export or migration refs, diagnostics, and the first incomplete stage.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this command, its required inputs, and the user's request, then execute the plan.

## Owner, Inputs, and Outputs

Owner: `isomer-ext-kaoju-entrypoint->write`; CLI: `isomer-cli ext kaoju paper template list|show|create|update|file|metadata|archive|delete|exports|export|promote-export|ensure-defaults|migrate|migrate-exchange-root`. Inputs: exact template role, role-local named state or one prepared assessed tree, current expected token for destructive operations, actor ref, authored metadata where required, and source assessment. Outputs: template role, selection source, stable or packaged identity, name, token when applicable, tree digest, authored metadata, mutation-audit ref, working-copy observation or migration result, diagnostics, and next action.

## Gates, Blockers, and Resume

An unresolved role, ambiguous selected-role source, material unresolved choice, missing target, stale token, unsafe path, reserved file, invalid composition contract, corrupt tree, edited-target overwrite, identity conflict, or durable dependent causes no canonical mutation. Resume at role selection, user source selection, agent assessment, candidate preparation, explicit create or adoption, state refresh, export reconciliation, or the requested low-level operation.
