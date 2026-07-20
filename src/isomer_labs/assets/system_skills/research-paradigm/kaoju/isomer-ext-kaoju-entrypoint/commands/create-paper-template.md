---
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Create Paper Template

## Workflow

1. Treat this retained procedure as content-template creation. Resolve the requested content-template name, defaulting it to content `main`, accepted audit and synthesis basis, target reader, and current content-template state. Route a LaTeX, TeX, document-class, style, venue-package, presentation, or PDF-layout request to `manage-paper-template` with role `latex` instead.
2. Use `isomer-ext-kaoju-entrypoint->write` to select and explain an adaptive typed structure profile.
3. Construct an arbitrary MyST-oriented directory tree with the intended entrypoint, configuration, includes, assets, guidance, section jobs, citation roles, typed display and source-ref placeholders, limitations, and reader constraints. Validate the prepared tree, then invoke `ext kaoju paper template create --kind content --name NAME --from PATH` when the name is absent or `template update --kind content --name NAME --from PATH --expected-state TOKEN` when the user authorized replacement. Never use generic Artifact revise for `KAOJU:PAPER-TEMPLATE-MYST`.
4. Validate MyST syntax, headings, roles, directives, placeholders, and evidence boundaries with `isomer-cli ext kaoju paper validate` before acceptance.
5. When the actor wants a manual-edit copy, compose `manage-paper-template` and run `ext kaoju paper template export --kind content`. Default unnamed export to content `main` and `<topic.paper.template_exchange_root>/content/main/`. The stable working directory is non-canonical.
6. Return the template name, stable ref, state token, observed tree digest, mutation-audit ref, diagnostics, optional export observation refs, and resume point.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this command, its required inputs, and the user's request, then execute the plan.

## Compatibility Mapping

`create-paper-template` is retained for callers that use the historical procedure name. It creates one mutable named content template backed by `KAOJU:PAPER-TEMPLATE-MYST`. LaTeX presentation stock uses `manage-paper-template --kind latex` and `KAOJU:PAPER-TEMPLATE-LATEX`. This procedure never writes a producer-selected internal path, uses `KAOJU:WRITING-TEMPLATE` for new state, or creates another name automatically.

## Gates, Blockers, and Resume

Missing accepted evidence, an unresolved name, an existing target without update authorization, invalid MyST, missing sources, unsafe tree content, or stale state blocks acceptance. Resume at structure selection, agent construction, explicit create or update choice, template validation, or optional export.
