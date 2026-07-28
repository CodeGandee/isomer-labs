---
name: isomer-publish-topic-to-remote
description: Use when a user asks to prepare, publish, synchronize, overwrite, or verify a sanitized remote snapshot of a selected Isomer Topic Workspace in the current Project.
---

# Isomer Topic Publication

## Overview

Publish one Source Topic Workspace as a reproduction-oriented, identity-sanitized current-state snapshot. Preserve the Source Topic Workspace, build a disposable Topic Publication Copy, and synchronize only the exact approved remote references.

## When to Use

Use this skill for an explicit request to publish, synchronize, replace, or verify a selected Topic Workspace and its configured publication remote. It also applies when preparing a publication plan that the user will approve before mutation.

Do not use this skill for ordinary Project repository pushes, paper submission, provider repository creation, archival backup, or automatic Topic Workspace restoration. If the user asks only for status or inspection, keep the workflow read-only.

## Workflow

1. Resolve the current Project and the exact Research Topic. Require an explicit or unambiguous topic identifier, align it with `isomer-cli --print-json project self check --scope topic --topic <topic-id>`, and pin that identifier on every applicable query.
2. Read [publication-contract.md](references/publication-contract.md) and [sync-procedure.md](references/sync-procedure.md) before planning or mutating publication state. When the packaged Topic Workspace Git publication guidance exists under `src/isomer_labs/assets/system_skills/operator/isomer-op-entrypoint/subskills/isomer-op-topic-workspace-git/`, inspect it for newer requirements and treat the current project-owned contract as authoritative.
3. Query Project context through `isomer-cli`; do not infer the topic topology from directory names or scan sibling Topic Workspaces. Identify the Source Topic Workspace, Topic Main, Topic Actors, selected Agents, registered third-party repositories, runtime state location, Publication Binding, and credential-safe remote locator.
4. Inventory the Source Topic Workspace from the filesystem, including relevant untracked and uncommitted files. Classify every considered path exactly once as `track`, `template`, `exclude`, `component`, or `block`, and record the reason.
5. Select publication content from the default contract. Require an explicit current plan selection before including raw downloaded materials or raw experiment output artifacts. Block publication if credentials, unsupported identity-bearing binaries, unclear licenses, unknown remote visibility, or an unresolved path disposition remain.
6. Build or refresh the disposable Topic Publication Copy under the Project's ignored temporary space. Preserve each retained Source Topic Workspace-relative path, generate only the allowed publication metadata, sanitize personal identity, and publish nested topic-owned repositories as fresh same-remote submodules.
7. Produce a complete remote mutation plan from a fresh heads, tags, and symbolic-HEAD inventory. State the exact expected branches, tags, component commits, superproject commit, deletions, force updates, remote visibility, and any provider-side default-branch action.
8. Confirm that the current request and Publication Binding authorize the exact plan. Recheck source fingerprints and remote state immediately before mutation; stop and rebuild the plan if either is stale.
9. Publish component branches first and `main` last with direct `git -C <validated-path>` commands. Stage exact paths, verify the full index, push only named references, and record partial outcomes so a retry does not guess.
10. Reobserve the remote and verify a fresh recursive clone. Check the exact remote reference set, symbolic HEAD, root layout, gitlink modes and commits, clean worktree, README links, manifests, latest paper checksum, excluded paths, and sanitized identity.
11. Persist the plan and outcome through supported Topic Git state surfaces, then report the remote commit, references, symbolic HEAD, component mapping, latest paper path, verification result, and limitations.

If a required Isomer CLI query or supported persistence surface is unavailable, continue with read-only filesystem and Git inspection where safe, mark every inferred value, and stop before remote mutation unless the target, authority, content, and exact reference plan remain independently verifiable.

## Guardrails

- DO NOT modify the Source Topic Workspace or its nested Git histories to prepare a publication.
- DO NOT treat a Topic Publication Copy as a backup, canonical workspace, or automatically restorable workspace.
- DO NOT use the source Git index or `HEAD` as the publication content authority.
- DO NOT publish credentials, personal researcher identity, non-public hosts or IP addresses, or unsupported identity-bearing binary content.
- DO NOT include downloaded raw materials or raw experiment outputs by default.
- DO NOT create a provider repository or change provider settings without a separate explicit action.
- DO NOT use `git pull`, `merge`, `rebase`, `reset`, `clean`, broad staging, `--all`, or `--mirror`.
- DO NOT force-update or delete a remote reference outside the current exact approved plan.
- DO NOT push rewritten content to a third-party upstream repository.
- DO NOT edit `state.sqlite` or use direct SQL for publication state.
