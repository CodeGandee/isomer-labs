---
name: isomer-op-topic-workspace-git
description: Use when an operator asks to inspect, plan, initialize, ignore, or commit local Source Topic Workspace root history, or prepare, plan, reconstruct, or synchronize a sanitized Topic Publication Copy.
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

Own optional Topic Workspace root tracking and sanitized remote publication as two disabled-by-default layers. Source Topic Workspace means the canonical Topic Workspace in its source role. Topic Publication Copy means an ignored disposable projection outside that workspace, not a fourth workspace type or canonical source.

The local layer creates and commits only a root repository in the Source Topic Workspace. It preserves Topic Main, Topic Actor Workspace, Agent Workspace, and canonical external repository topology and never contacts a remote. The publication layer reads current filesystem content, creates fresh sanitized histories in the Topic Publication Copy, and can synchronize those histories without requiring local tracking or local commits.

## When to Use

Use this protected owner for explicit local root-history, root-ignore, exact local commit, sanitized publication-copy, privacy-plan, reconstruction, or remote synchronization requests. Use overall status for a vague tracking or versioning request. Ordinary Topic Workspace storage, actor, team, environment, reset, and diagnostic work remains with Topic Manager.

## Workflow

1. **Select one operation**. Use overall `status`, one `local` child operation, or one `publish` child operation. A vague request to track or version a Topic Workspace starts with overall status and explains both choices before mutation.
2. **Resolve selected context read-only**. Follow [references/context-queries.md](references/context-queries.md). Pin one Project, Research Topic, and Source Topic Workspace through explicit JSON queries. Load current Topic Actor, Agent, semantic-path, and Workspace Runtime evidence only when the selected operation needs it.
3. **Load only required contracts**. Every operation loads [references/direct-git-safety.md](references/direct-git-safety.md) plus its layer safety page. Publication planning or synchronization also loads privacy and persistence safety. Do not preload the other layer's mutation procedure.
4. **Plan before mutation**. Record exact paths, repository identities, fingerprints, blockers, and approvals. Local mutations require valid Workspace Runtime. Publication may begin after Topic Workspace registration and keeps pre-runtime state in the ignored copy-local support root.
5. **Revalidate and execute directly**. Recompute every applicable assumption. Run Git as the installed executable with `git -C <validated-resolved-path> ...`; never route Git through Isomer CLI or a non-Git helper.
6. **Verify boundaries and persist outcomes**. Inspect exact index, worktree, generated projection, component commits, fetched refs, and branch outcomes. Write only schema-validated Topic Git support files. Report the local and publication states separately.

If the task does not map cleanly to these operations, use the native planning tool to build a layer-scoped read-only plan. Stop before mutation when the intended layer, selected topic, privacy disposition, visibility, destination, remote mutation, conflict resolution, or branch replacement is ambiguous.

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
| [references/publication-safety.md](references/publication-safety.md) | Destination, remote, same-remote branch layout, fetch-first synchronization, reconstruction, and push order. |
| [references/privacy-projection.md](references/privacy-projection.md) | Inventory, dispositions, sanitization, rescanning, manifests, and conflicts. |
| [references/persistence.md](references/persistence.md) | Layer-specific schemas, copy-local state, runtime promotion, outcomes, and forbidden content. |

## Output Contract

Default to **Essential Output** in chat. Use **Complete Output** when the user asks for complete, verbose, audit, debug, full handoff, or full output. Present either depth in natural-language Markdown. If the user explicitly requests JSON or another machine-readable format, serialize the applicable information in that format.

### Essential Output

Lead with the selected Research Topic, operation, and outcome. For status, report local tracking as `disabled`, `enabled`, or `invalid` and publication as `disabled`, `prepared`, `synchronized`, `stale`, `copy-missing`, or `blocked`, with separate blockers and next actions. For plans, summarize exact scope, approvals, and blockers without sensitive excerpts. For mutation, summarize changed paths, commits or refs, branch outcomes, verification, and safe next action.

### Complete Output

Include resolved context and sources, all exact paths and repository identities, dispositions, fingerprints, direct commands, index verification, binding and visibility posture, component selection, conflicts, remote compatibility, destructive-plan evidence, per-branch outcomes, support files, and resume state.

## Guardrails

- DO NOT scan sibling Topic Workspaces, guess a path, replace an unresolved selected topic with a directory, or accept a context conflict.
- DO NOT add a Topic Git mutation family to Isomer CLI. Use Isomer CLI only for explicit read-only JSON information queries.
- DO NOT hide Git in a Python service, script, sanitization helper, projection helper, or command runner.
- DO NOT rely on ambient cwd. Every repository command uses the validated Source Topic Workspace, Topic Publication Copy, or sanitized component repository path.
- DO NOT broaden exact staging, pull, merge, rebase, reset, clean, rewrite source history, delete a remote branch, or repair unexpected state implicitly.
- DO NOT initialize Workspace Runtime, edit `state.sqlite`, or store credentials, secrets, sensitive excerpts, raw private diffs, source Git configuration, or credential-bearing URLs.
- DO NOT make local tracking and publication prerequisites, triggers, or authorities for each other.
- DO NOT call a Topic Publication Copy a workspace or use it as canonical research state.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome and use headings only when they improve clarity. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
