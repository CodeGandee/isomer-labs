# Show Extensions

## Workflow

1. Run `isomer-cli --print-json system-skills extensions list` to read package-catalog extension metadata.
2. When the user names one extension, run `isomer-cli --print-json system-skills extensions show <extension-id>` to focus the response.
3. When Project context exists and declaration state matters, run `isomer-cli --print-json project system-extensions list`.
4. Report each extension's purpose, entry skill, public capability surface, and evidence state using **Extension State Labels**.
5. Route host usability, compatibility, installation, registration, refresh, or repair to `isomer-op-system-skill-mgr` without mutating state.
6. End with the appropriate visible research path, read-only manager invocation, or concrete-task route through `isomer-op-entrypoint`.

If the user's task does not map cleanly to these steps, use your native planning tool to build a read-only extension discovery plan from package-catalog metadata, selected Project declarations, the user's research goal, and the welcome guardrails, then execute only the inspection steps and report the next owner route.

## Extension State Labels

| Label | Evidence | Meaning |
| --- | --- | --- |
| `catalog-known` | `system-skills extensions list` or `show` | The installed Isomer package describes the optional capability, entry skill, commands, and member skills. This is not installation evidence. |
| Project-declared | `project system-extensions list` reports a user declaration | The Project Manifest records authoritative routing intent. This is not proof that the current host can load the family. |
| Host-usable | `isomer-op-system-skill-mgr` establishes a complete compatible managed receipt or complete live inventory | The selected host can use the complete family according to the manager's evidence contract. |
| Partial, incompatible, stale, or missing | Manager status or a confirmed route failure | The manager must diagnose installation, registration, compatibility, refresh, or repair. |

Do not collapse these labels into a single installed flag. Preserve a Project declaration even when the current host lacks the corresponding skill family.

## Current Package-Catalog Research Paradigms

The catalog currently defines DeepSci and Kaoju, but always derive the returned entry skill and public commands from `system-skills extensions` output so future packaged extensions remain discoverable.

| Extension | Research Fit | Entry Route |
| --- | --- | --- |
| `deepsci` | Hypothesis-driven production research, including experiments, analysis, decisions, writing, review, rebuttal, revision, and submission. | `start-deepsci-research`, then `$isomer-deepsci-pipeline` after readiness. |
| `kaoju` | Evidence-led literature, codebase, dataset, and model surveys, including source ingestion, bounded trials, comparisons, paper production, and wiki export. | `start-kaoju-survey`, then `$isomer-kaoju-pipeline` after readiness. |

## Management Routes

- Use `Use $isomer-op-system-skill-mgr detect-extensions` for read-only ordered resolution.
- Use `Use $isomer-op-system-skill-mgr status` for declaration, receipt, inventory, compatibility, and refresh evidence.
- Use `Use $isomer-op-system-skill-mgr install-extension` only when the user authorizes installation for a concrete agent host and scope.
- Use `Use $isomer-op-system-skill-mgr reconcile-extensions` only when additive Project bookkeeping is authorized.
- Use `Use $isomer-op-system-skill-mgr repair` for stale declarations, malformed receipts, invalid projections, incompatible versions, partial families, missing registration, or refresh delays.
- Use `Use $isomer-op-entrypoint` with a concrete DeepSci or Kaoju task when the user wants Isomer to resolve readiness and proceed rather than only inspect extension state.

This welcome subcommand must not install files, call `remember` or `forget`, inspect guessed host roots, classify an invented live inventory, or claim current-session availability after installation.

## Related Extension Terms

A system-skill extension is an optional agent-skill family. A Toolbox is project-local callback and Runtime Param customization owned by `isomer-op-toolbox-mgr`. The `isomer-cli ext` namespace exposes runtime and compatibility commands; it does not discover or install system-skill extensions.
