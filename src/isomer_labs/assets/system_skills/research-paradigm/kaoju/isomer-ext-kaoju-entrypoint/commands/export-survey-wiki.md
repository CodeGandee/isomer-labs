---
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Export Survey Wiki

## Workflow

1. Resolve an explicit Artifact subset or accepted direction and paper scopes through state-DB queries. Reject ambiguity and stale content.
2. Use `isomer-ext-kaoju-entrypoint->export` and only `isomer-cli ext kaoju wiki export` to render Markdown pages plus canonical JSON metadata.
3. Stage an idempotent in-place update at the Topic Workspace default or actor override. Replace only paths owned by the prior valid manifest, preserve human files, and report created, changed, unchanged, stale, and removed managed paths.
4. Register checksummed `KAOJU:LLM-WIKI-EXPORT` and `KAOJU:LLM-WIKI-METADATA` revisions.
5. On request, deploy the independently implemented installed-package viewer and register `KAOJU:LLM-WIKI-VIEWER` plus its manifest. Clarify before touching a non-empty unrecognized target.
6. On request, start through `viewer_launch`, loopback by default. Handle port conflict, require a Gate for network exposure, and record Run and log refs.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this command, its required inputs, and the user's request, then execute the plan.

## Owner, Inputs, and Outputs

Owner: `isomer-ext-kaoju-entrypoint->export`. Outputs: export, metadata, viewer, viewer manifest, changelog, Run, log, and local URL.

## Gates, Blockers, and Resume

Network exposure requires a human Gate. Missing accepted inputs, stale content, target ambiguity, protected files, port conflict, or launch failure records a blocker. Never invoke `imsight-llm-wiki`.
