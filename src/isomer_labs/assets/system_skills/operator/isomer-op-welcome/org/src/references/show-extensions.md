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

# Show Extensions

## Workflow

1. Run `isomer-cli --print-json system-skills extensions list` to read package-catalog extension metadata.
2. When the user names one extension, run `isomer-cli --print-json system-skills extensions show <extension-id>` to focus the response.
3. When Project context exists and declaration state matters, run `isomer-cli --print-json project system-extensions list`.
4. Report each extension's purpose, entry skill, public capability surface, and evidence state using **Extension State Labels**.
5. Route host integrity, compatibility, installation, upgrade, registration, refresh, or repair through `isomer-op-entrypoint->system-skills` without mutating state.
6. End with the appropriate visible research path, public manager invocation, or concrete-task route through `$isomer-op-entrypoint`.

If the user's task does not map cleanly to these steps, use your native planning tool to build a read-only extension discovery plan from package-catalog metadata, selected Project declarations, the user's research goal, and the welcome guardrails, then execute only the inspection steps and report the next owner route.

## Extension State Labels

| Label | Evidence | Meaning |
| --- | --- | --- |
| `catalog-known` | `system-skills extensions list` or `show` | The installed Isomer package describes the optional public pack, entry skill, commands, and protected members. This is not installation evidence. |
| Project-declared | `project system-extensions list` reports a user declaration | The Project Manifest records authoritative routing intent. This is not pack-integrity proof. |
| `entrypoint_seen` | Limited live inventory contains the public entrypoint name | The name is visible, but protected integrity and current-session usability remain unverified. |
| Pack-integrity-verified | Current v4 receipt or explicit-root verification reports complete protected coverage and usable compatibility | The complete pack material is verified. A new install or upgrade may still require a host refresh. |
| Partial, legacy, incompatible, stale, or missing | Manager status or a confirmed route failure | The manager must diagnose migration, installation, registration, compatibility, refresh, or repair. |

Do not collapse these labels into a single installed flag. Preserve a Project declaration even when the current host lacks the corresponding skill family.

## Current Package-Catalog Research Paradigms

The catalog currently defines DeepSci and Kaoju, but always derive the returned entry skill and public commands from `system-skills extensions` output so future packaged extensions remain discoverable.

| Extension | Research Fit | Entry Route |
| --- | --- | --- |
| `deepsci` | Hypothesis-driven production research, including experiments, analysis, decisions, writing, review, rebuttal, revision, and submission. | `start-deepsci-research`, then `$isomer-ext-deepsci-entrypoint` after readiness. |
| `kaoju` | Evidence-led literature, codebase, dataset, and model surveys, including source ingestion, bounded trials, comparisons, paper production, and wiki export. | `start-kaoju-survey`, then `$isomer-ext-kaoju-entrypoint` after readiness. |

## Management Routes

- Use `$isomer-op-entrypoint use system-skills to detect extensions` for read-only ordered resolution.
- Use `$isomer-op-entrypoint use system-skills to report extension status` for declaration, receipt, explicit-root, limited inventory, compatibility, and refresh evidence.
- Use `$isomer-op-entrypoint use system-skills to install <extension-id>` only when the user authorizes installation for a concrete agent host and scope.
- Use `$isomer-op-entrypoint use system-skills to upgrade <extension-id>` for an authorized managed legacy migration or package refresh.
- Use `$isomer-op-entrypoint use system-skills to reconcile extensions` only when additive Project bookkeeping is authorized.
- Use `$isomer-op-entrypoint use system-skills to repair <extension-id>` for stale declarations, malformed receipts, invalid packs, incompatible versions, partial coverage, missing registration, legacy evidence, or refresh delays.
- Use `$isomer-op-entrypoint` with a concrete DeepSci or Kaoju task when the user wants Isomer to resolve readiness and proceed rather than only inspect extension state.

This welcome subcommand must not install files, call `remember` or `forget`, inspect guessed host roots, classify an invented live inventory, or claim current-session availability after installation.

## Related Extension Terms

A system-skill extension is an optional public skill pack. A Toolbox is project-local callback and Runtime Param customization owned through `isomer-op-entrypoint->toolbox`. The `isomer-cli ext` namespace exposes runtime and compatibility commands; it does not discover or install system-skill extensions.
