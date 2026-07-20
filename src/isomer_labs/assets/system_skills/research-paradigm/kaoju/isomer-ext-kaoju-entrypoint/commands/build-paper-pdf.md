---
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Build Paper PDF

## Workflow

1. Resolve the accepted canonical MyST draft and its exact observed content-template identity, citation map, paper line, publication Gate policy, and an explicit named LaTeX template or LaTeX `main`. Content and LaTeX selectors are independent. If canonical MyST state is missing or stale, return `paused` prerequisite recovery with `draft-paper`; if LaTeX stock is missing, route to `manage-paper-template --kind latex` for create or explicit adoption.
2. Invoke `ext kaoju paper init-tex --content-template-ref REF` with either `--latex-template-name NAME`, `--latex-template-ref REF`, or the omitted-selector LaTeX `main` default. Snapshot the exact multi-file `KAOJU:PAPER-TEMPLATE-LATEX` state into `KAOJU:PAPER-TEMPLATE-TEX`, then compose a self-contained `KAOJU:PAPER-DRAFT-TEX` through the checked preamble, marker, or include contract. Record the content-template identity, LaTeX-template identity, state token, digests, source checksum, composition contract, build profile, entrypoint, citations, included files, and conversion diagnostics separately.
3. Run `paper tex-status` and require the write agent to inspect and repair derived TeX directly. Initialization never claims build readiness. Report stocked-template drift and paper-local repair drift without recomposition or stock mutation.
4. After build authorization, invoke `build-pdf` through the `document_build` extension point. The builder verifies the pinned snapshot, rejects a mismatched compatibility `--template-tex-ref`, uses the manifest entrypoint and registered build profile, and records a distinct Run, exact command, compile log, drift posture, and outputs.
5. Permit bounded presentation-only or TeX-syntax repair inside `KAOJU:PAPER-DRAFT-TEX` when it preserves canonical MyST and evidence meaning. Never promote a paper repair into named LaTeX stock unless the user explicitly requests that separate mutation. Any canonical content, dependency, build-profile, or interpretation change requires a revised plan and human Gate.
6. Validate PDF media type, digest, extracted text, hierarchy, citations, page sequence, displays, clipping, overflow, blank pages, density, and publication-quality profile before the publication Gate.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this command, its required inputs, and the user's request, then execute the plan.

## Owner, Inputs, and Outputs

Owner: `isomer-ext-kaoju-entrypoint->write`. Outputs: separate observed content-template and LaTeX-template identities, exact TeX snapshot and self-contained draft, drift posture, immutable build Run and compile log, PDF, PDF revision log, validation report, and publication bundle refs.

## Gates, Blockers, and Resume

Build and publication Gates are distinct. Resume at MyST validation, LaTeX stock resolution, TeX composition, agent repair, build authorization, build repair, PDF inspection, or publication acceptance.
