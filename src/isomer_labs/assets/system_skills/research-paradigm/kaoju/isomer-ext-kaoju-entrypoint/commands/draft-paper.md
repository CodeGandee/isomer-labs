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

# Draft Paper

## Workflow

1. Require accepted Audit Report, Field Summary, Related-Work Catalog, Claim Status Table, and the selected paper-line scope. Missing, contradicted, or stale prerequisites with known audit or synthesis producers yield `paused` prerequisite recovery before writing; report their routes and the draft resume point rather than invoking them inside this procedure.
2. Resolve an explicitly named content template through `template show --kind content`, or default to content `main`. Read its stable ref, current state token and tree digest, authored entrypoint, and use guidance, then interpret the arbitrary MyST-oriented tree for the requested paper. Do not inspect or select LaTeX stock during content-structure selection, and do not select another content name by timestamp, paper line, or record order.
3. Use `isomer-ext-kaoju-entrypoint->write` to select an adaptive structure profile from taxonomy, comparison, empirical survey, or general survey and explain the choice from the accepted direction. Resolve structure review before creating canonical `KAOJU:PAPER-STRUCTURE-MYST` and `KAOJU:PAPER-DRAFT-MYST` state tied to the selected content-template name, stable ref, state token, and observed digest. Human review is the default. Under explicit target-scoped prompt delegation, the agent may inspect, revise, reject, or accept the structure and draft within the accepted paper boundary without another user turn. Record review mode, prompt basis, reviewing actor, rationale, affected refs, and resume posture through existing supported provenance. Create or change the content template only through the role-explicit named-template workflow when the request authorizes that separate mutation.
4. Record `KAOJU:CITATION-MAP` and append-only `KAOJU:PAPER-REVISION-LOG`. Figures and tables remain separate file-backed Artifacts referenced through typed placeholders.
5. Validate MyST structure, required sections, directives, roles, citations, placeholders, displays, source refs, and evidence boundaries with file-location diagnostics.
6. Optionally derive `KAOJU:PAPER-DRAFT-MD`. It is a deterministic review view and never editable canonical state.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this command, its required inputs, and the user's request, then execute the plan.

## Owner, Inputs, and Outputs

Owner: `isomer-ext-kaoju-entrypoint->write`. Inputs: accepted audit and synthesis refs, paper line, and an explicit content template or content `main`. Outputs: selected content-template name, stable ref, state token and observed digest, canonical MyST structure and draft, citation map, revision log, and optional derived Markdown refs.

## Gates, Blockers, and Resume

Structure and draft review are required and default to human acceptance. Explicit target-scoped prompt delegation permits recorded agent review within the accepted paper boundary; silence, generic continuation, or run-to authorization alone does not. Resume at prerequisite resolution, structure selection, template, draft, validation, or acceptance.
