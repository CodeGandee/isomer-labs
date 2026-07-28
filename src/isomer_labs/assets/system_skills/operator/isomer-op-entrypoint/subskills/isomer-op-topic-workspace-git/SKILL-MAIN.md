---
name: isomer-op-topic-workspace-git
description: Use when managing local Topic Workspace Git or publishing a reproducible, identity-sanitized Topic Publication Copy.
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

# Topic Workspace Git

## Overview

Own two independent, disabled-by-default Git layers:

| Layer | Input | Result | Remote Posture |
| --- | --- | --- | --- |
| Local tracking | Canonical Topic Workspace root | Local root repository and exact commits that preserve nested repository topology | Never contacts a remote |
| Remote publication | Current Topic Workspace filesystem and registered source identities | Inspectable sanitized evidence and artifacts with compatible sanitized publication ancestry and exact upstream references | Preserves compatible history through normal pushes and uses exact replacement only as an approved fallback |

Key terms:

- **Source Topic Workspace**: the canonical Topic Workspace acting as the source for tracking or publication.
- **Topic Publication Copy**: an ignored projection outside the Source Topic Workspace; it is neither canonical state nor another workspace type.

## When to Use

| Request | Route |
| --- | --- |
| Vague Topic Workspace tracking or versioning | Overall `status` |
| Local root history, ignore policy, planning, initialization, or exact commit | `local()` |
| Sanitized publication preparation, privacy planning, copy recovery, or remote synchronization | `publish()` |

Ordinary Topic Workspace storage, actor, team, environment, reset, and diagnostic work remains with Topic Manager.

## Workflow

1. **Select one operation** from the **Subcommands** table. Start a vague tracking or versioning request with overall `status()`.
2. **Resolve context read-only** with [context-queries.md](references/context-queries.md). Pin one Project, Research Topic, and Source Topic Workspace.
3. **Load the operation contracts** from **Shared References**:
   - Every operation loads direct Git safety and the selected layer's safety page.
   - Publication planning and synchronization also load privacy and persistence safety.
4. **Plan before mutation**. Record exact paths, identities, fingerprints, blockers, and approvals:
   - Local mutation requires valid Workspace Runtime.
   - Publication may begin after Topic Workspace registration and keeps pre-runtime support in the ignored copy.
   - Publication preserves retained Source Topic Workspace-relative paths while selecting intent, environment declarations, durable research lineage, topic-owned components, and registered GitHub references by default.
   - Publication never imports source Git ancestry. It may extend a compatible prior sanitized publication commit as the direct parent of a sanitized delta.
   - Downloaded material bytes and raw experiment-output bytes remain excluded until the current plan explicitly selects them.
5. **Revalidate and execute directly**. Recompute applicable assumptions and run path-scoped `git -C <validated-path> ...`.
6. **Verify and persist**. Check the exact repository or projection state, write only schema-valid support files, and report local and publication outcomes separately.

If the task does not map cleanly to these operations, use the native planning tool to build a layer-scoped read-only plan. Stop before mutation when any of these is ambiguous:

- intended layer or selected topic;
- privacy disposition, visibility, or destination;
- remote mutation, conflict resolution, or branch replacement.

## Subcommands

| Operation | Use For | Page |
| --- | --- | --- |
| `isomer-op-entrypoint->topic-git->status()` | Read both independent layer states, blockers, and next actions. | [commands/status.md](commands/status.md) |
| `isomer-op-entrypoint->topic-git->local()` | Select local status, init, plan, ignore, or commit. | [commands/local.md](commands/local.md) |
| `isomer-op-entrypoint->topic-git->publish()` | Select publication status, init, plan, or sync. | [commands/publish.md](commands/publish.md) |

## Shared References

| Reference | Use For |
| --- | --- |
| [references/context-queries.md](references/context-queries.md) | Read-only Isomer context and topology queries, pinning, and rejection rules. |
| [references/direct-git-safety.md](references/direct-git-safety.md) | Direct path-scoped Git, exact staging, ref safety, and forbidden operations. |
| [references/local-safety.md](references/local-safety.md) | Local runtime prerequisite, ancestor evidence, root repository, nested exclusions, and local support state. |
| [references/publication-safety.md](references/publication-safety.md) | Destination, topic-owned and upstream-reference submodules, history-aware synchronization, exclusive-snapshot fallback, copy recovery, and push order. |
| [references/privacy-projection.md](references/privacy-projection.md) | Semantic defaults, raw-byte selection, individual-identity sanitization, navigation, manifests, rescanning, and conflicts. |
| [references/persistence.md](references/persistence.md) | Layer-specific schemas, copy-local state, runtime promotion, outcomes, and forbidden content. |

## Output Contract

Default to **Essential Output** in chat. Use **Complete Output** when the user asks for complete, verbose, audit, debug, full handoff, or full output. Present either depth in natural-language Markdown. If the user explicitly requests JSON or another machine-readable format, serialize the applicable information in that format.

| Depth | Use When |
| --- | --- |
| **Essential Output** | Default |
| **Complete Output** | User requests complete, verbose, audit, debug, or full handoff output |

### Essential Output

Lead with the selected Research Topic, operation, and outcome.

| Operation | Report |
| --- | --- |
| Status | Local state (`disabled`, `enabled`, or `invalid`), publication state (`disabled`, `prepared`, `synchronized`, `stale`, `copy-missing`, or `blocked`), blockers, and next actions |
| Plan | Exact semantic scope, source-to-output path identity, raw-byte settings, repository identities, reproduction limitations, complete remote refs and tags, history posture, per-ref strategies and evidence, approvals, conflicts, and blockers without sensitive excerpts |
| Mutation | Changed paths, README and research-index state, commits or refs, preserved sanitized ancestry or fallback replacement, ref and remote-HEAD outcomes, verification, and safe next action |

### Complete Output

Include:

- resolved context, sources, paths, and repository identities;
- dispositions, fingerprints, direct commands, and index verification;
- binding, visibility, exclusive-snapshot fallback authority, component and reference selection, raw-byte settings, identity substitutions, reproduction limitations, conflicts, and complete remote inventory;
- history-compatibility and fallback evidence, per-ref strategies, ref and tag outcomes, remote-HEAD diagnostics, support files, and resume state.

## Guardrails

- DO NOT scan sibling Topic Workspaces, guess a path, replace an unresolved selected topic with a directory, or accept a context conflict.
- DO NOT add a Topic Git mutation family to Isomer CLI. Use Isomer CLI only for explicit read-only JSON information queries.
- DO NOT hide Git in a Python service, script, sanitization helper, projection helper, or command runner.
- DO NOT preload the unselected layer's mutation procedure.
- DO NOT rely on ambient cwd. Every repository command uses the validated Source Topic Workspace, Topic Publication Copy, or sanitized component repository path.
- DO NOT broaden exact staging, pull, merge, rebase, reset, clean, rewrite source history, delete an unplanned remote ref or tag, or repair unexpected state implicitly.
- DO NOT initialize Workspace Runtime, edit `state.sqlite`, or store credentials, secrets, sensitive excerpts, raw private diffs, source Git configuration, or credential-bearing URLs.
- DO NOT remove a credential-free GitHub owner or repository name as personal information; preserve it as organization or source provenance.
- DO NOT publish downloaded material bytes or raw experiment-output bytes without an explicit current-plan selection.
- DO NOT make local tracking and publication prerequisites, triggers, or authorities for each other.
- DO NOT call a Topic Publication Copy a workspace or use it as canonical research state.
- DO NOT describe a Topic Publication Copy as an operational backup or promise automatic Topic Workspace restoration; working reconstruction is manual.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
