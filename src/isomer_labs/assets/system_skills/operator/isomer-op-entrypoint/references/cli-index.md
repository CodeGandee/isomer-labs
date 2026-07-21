# CLI Index

## Workflow

1. Decide whether the user asked for CLI execution, CLI discovery, or a task that should route to a skill before CLI use.
2. Classify the operation scope, extract prompt targets, and use `project self location` plus `project self check --scope <scope>` before context-sensitive mutation.
3. Pin every accepted Research Topic, Topic Actor, or Agent selector on applicable downstream commands; a later cwd change must not rediscover or replace the target.
4. Select the smallest CLI command family that owns the operation and inspect its `--help` output when flags or exact command shape are needed.
5. Preserve owner-skill boundaries: use CLI commands directly for CLI-owned operations, but route workflow-level setup, readiness, and research work through the owning skill.
6. Report commands run, read-only or mutation posture, selected target and source, alignment verdict, changed paths or records, blockers, and next action.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step CLI routing plan from current context, available command families, owner boundaries, and required approvals, then execute the plan or report the blocker.

## Safe Discovery Commands

Use these before ambiguous mutation:

- `isomer-cli project self queries`
- `isomer-cli project self show`
- `isomer-cli --print-json project self location`
- `isomer-cli --print-json project self check --scope <project|topic|topic-actor|agent>`
- `isomer-cli project self identity`
- `isomer-cli project self paths`
- `isomer-cli project validate`
- `isomer-cli doctor`
- `isomer-cli project topics list`
- `isomer-cli project context show`
- `isomer-cli project system-extensions list`
- `isomer-cli project system-extensions detect --skill-root <host-known-root>`
- `isomer-cli internals inspect-system-skill-root --skill-root <host-known-root>`
- `isomer-cli internals classify-system-skill-inventory --skill-name <host-visible-name>`
- `isomer-cli project paths get`
- `isomer-cli project paths explain`
- `isomer-cli project paths list`
- `isomer-cli project paths preview`

## Project and Topic Command Families

| Intent | CLI Family |
| --- | --- |
| Project initialization, validation, doctor, cleanup, or generated content root relocation. | `isomer-cli project init`, `validate`, `doctor`, `cleanup`, `content-root ...` |
| Research Topic CRUD. | `isomer-cli project topics ...` |
| Topic Workspace listing and inspection. | `isomer-cli project workspaces ...` |
| Effective Topic Context, ambient workspace location, task-target alignment, and progressive self context. | `isomer-cli project context ...`, `isomer-cli project self location`, `isomer-cli project self check ...`, `isomer-cli project self ...` |
| Workspace Path Resolution. | `isomer-cli project paths ...` |
| Topic repositories and topic-main guidance. | `isomer-cli project repos ...`, `isomer-cli project topic-main-guidance ...` |
| Topic Actors and Topic Actor Workspaces. | `isomer-cli project topic-actors ...` |
| Workspace Runtime readiness and inspection. | `isomer-cli project runtime ...` |
| Topic reset checkpoints and plans. | `isomer-cli project topic-reset ...` |
| Worker output policy. | `isomer-cli project outputs policy` |
| Toolbox registration, validation, install, enable, disable, update-source, uninstall, show, list, or explain. | `isomer-cli project toolboxes ...` |
| Toolbox callback insertion points, callback registry rows, callback resolution, validation, install, or refresh. | `isomer-cli project skill-callbacks ...` |
| Toolbox Runtime Param set, unset, import, get, explain, or validate. | `isomer-cli project toolbox-params ...` |
| Project extension declarations and explicit-root advisory detection. | `isomer-cli project system-extensions ...` |
| Provider-neutral explicit-root and live-inventory classification for version-aligned system skills. | `isomer-cli internals ...` |

## Research Records and Artifact Formats

| Intent | CLI Family |
| --- | --- |
| Create, list, show, update, delete, validate, or render structured research records. | `isomer-cli ext research records ...` |
| Maintain record indexes. | `isomer-cli ext research records index rebuild`, `validate`, or `cleanup` |
| Query record indexes, lineage, files, facets, or export views. | `isomer-cli ext research records query ...` |
| Inventory worker operation sets, preview or apply exhaustive acceptance, resume partial receipts, and verify closeout. | `isomer-cli ext research operation-sets inspect`, `accept`, or `verify` |
| Validate, render, or register Artifact Formats. | `isomer-cli project artifact-formats ...` |

Do not hand-edit research record indexes or acceptance receipts. Use `isomer-cli ext research records ...` and `isomer-cli ext research operation-sets ...` command families.

## Team and Handoff Command Families

| Intent | CLI Family |
| --- | --- |
| Domain Agent Team Template list, inspect, validate, or registration. | `isomer-cli project team-templates ...` |
| Topic Agent Team Profile specialization, materialization, and validation. | `isomer-cli project team-profiles ...` |
| Agent Team Instance create, list, show, adapter-link export, launch-material prepare, launch, inspect-live, stop, reconcile, or adopt. | `isomer-cli project team-instances ...` |
| Manual handoff dispatch, observation, or normalization. | `isomer-cli project handoffs ...` |
| Schema discovery. | `isomer-cli schemas list` |

Use global `isomer-cli` in operator guidance. Do not use repo-local Pixi wrapper command examples for Isomer CLI.
