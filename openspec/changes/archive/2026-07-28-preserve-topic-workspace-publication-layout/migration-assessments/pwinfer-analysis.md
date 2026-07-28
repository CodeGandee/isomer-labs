# Pwinfer Analysis Publication Migration Assessment

## Scope and Posture

This is a read-only assessment of the registered `pwinfer-analysis` Source Topic Workspace, its Topic Git support files, the existing Project-local Topic Publication Copy, and the credential-safe GitHub publication remote. No source file, publication commit, remote ref, tag, or provider setting was changed.

The existing Publication Binding is legacy state. It identifies the correct Research Topic, Topic Workspace, copy, remote, and private visibility, but it does not grant `exclusive_snapshot` authority. A new binding acknowledgement is required before snapshot replacement.

## Retained-Path Accounting

The current plan contains 396 entries: 346 retained source-backed entries, 3 pseudo-source generated entries, and 47 excluded entries. The new projection maps every retained source-backed entry to the same relative output path. The normalized 346-entry identity map has SHA-256 `46ed8e838d5b51d704e8f5455adafe121fa9a145bd8eda618ba1c1a5a7945c8f`.

| Source Path or Family | Count | Legacy Output | New Planned Output | Result |
| --- | ---: | --- | --- | --- |
| `intent/**` | 13 | Same as source | Same as source | Already path-preserving |
| `records/**` | 328 | Same as source | Same as source | Already path-preserving |
| `pixi.toml` | 1 | `environment/pixi.toml` | `pixi.toml` | Remove synthetic `environment/` relocation |
| `pixi.lock` | 1 | `environment/pixi.lock` | `pixi.lock` | Remove synthetic `environment/` relocation |
| `topic-workspace.toml` | 1 | `environment/topic-workspace.toml` | `topic-workspace.toml` | Remove synthetic `environment/` relocation |
| `.gitattributes` | 1 | `environment/workspace.gitattributes` | `.gitattributes` | Restore root path |
| `.gitignore` | 1 | `environment/workspace.gitignore` | `.gitignore` | Preserve source root policy |
| **All retained source-backed entries** | **346** | 341 identity, 5 relocated | 346 identity | Complete accounting |

The next plan should separately privacy-scan and add the root readiness summary `isomer-topic-workspace-summary.md`, which exists but is absent from the legacy plan. It should keep empty directories absent unless they contain an approved tracked placeholder.

## Generated-Path Migration

| Legacy Entry | New Entry | Required Change |
| --- | --- | --- |
| pseudo-source `generated/README.md` to root `README.md` | generated-origin root `README.md` | Compose a versioned navigation block; no source path exists in this workspace |
| pseudo-source `generated/research-record-index.json` to root `research-record-index.json` | generated-origin `.isomer-publication/research-record-index.json` | Move portable lineage metadata into the reserved overlay |
| pseudo-source `generated/.gitignore` to root `.gitignore` | no generated `.gitignore` | Preserve source `.gitignore`; exclude copy-local `.isomer/` through `.git/info/exclude` |
| root `topic-workspace-projection.json` | `.isomer-publication/topic-workspace-projection.json` | Move publication metadata into the reserved overlay |
| root `topic-workspace-version.toml` | `.isomer-publication/topic-workspace-version.toml` | Move publication metadata into the reserved overlay |
| absent root `.gitmodules` | generated-origin root `.gitmodules` | Describe topic-owned component branches and registered upstream references |

The latest completed Q4-centered paper output is `records/artifacts/research-records/artifact/artifact-paper-pdf-461abfefd200/template.pdf`, SHA-256 `14af1af74128a8cadcbac84d0049c87f38db7faccc461ecd2ada37b1cd2e1319`, size 79,018 bytes. Its terminal report records successful compile, textual inspection, and visual inspection. The legacy plan excludes every PDF, and the typed validation record still says the publication gate is pending. The next plan must reconcile the user's publication approval with that record, rerun identity, license, and PDF checks, retain this exact Artifact path if eligible, and link it from README. It must not create `paper/latest.pdf`.

## Component and Reference Topology

| Source | Source Relationship | Published Path | New Branch | Migration Assessment |
| --- | --- | --- | --- | --- |
| Topic Main | Normal repository and worktree anchor | `repos/topic-main` | `components/topic-main` | Build a fresh sanitized snapshot; do not import source ancestry |
| Topic Actor `operator` | Worktree of Topic Main | `actors/operator` | `components/topic-actors/operator` | Build a fresh sanitized snapshot, record Topic Main anchor, exclude `.git` worktree control and unapproved worker output |
| Agents | No registered Agent Workspace is present | None | None | Publish no agent component |
| Registered non-main references | None registered | None | Upstream commit, no publication branch | Publish no third-party submodule until a reference is registered with locator, exact commit, visibility, and license posture |

The local `extern/orphan/powerinfer-survey` collection contains downloaded papers and notes, not registered Git reference repositories. Its paper bytes remain excluded because raw-material bytes are disabled. Durable record identities, digests, locators, evidence relationships, and limitations remain publishable. If a relevant GitHub source repository should appear as a third-party submodule, register it as a non-main `topic.repos.*` reference before generating the migration plan.

## Observed Remote Snapshot

The complete read-only remote observation found four branches, no tags, and remote HEAD selecting `topic-workspace/main`.

| Observed Branch | Observed Commit | Planned Result |
| --- | --- | --- |
| `main` | `84c2f8cde1a026df9b9bc30c5aba9089ce40b87a` | Force-replace with the new canonical superproject snapshot |
| `per-topic-actor/operator/main` | `693d86b65c237ef783cb5eb2c5e2bf73771e7037` | Delete after its replacement component branch is available |
| `topic-owner/main` | `84c2f8cde1a026df9b9bc30c5aba9089ce40b87a` | Delete after `components/topic-main` is available |
| `topic-workspace/main` | `a1ed3497c4406de9dd5d56d75f7ae3bd98749fae` | Delete only after remote HEAD moves to `main` |

The expected branch set is exactly `components/topic-main`, `components/topic-actors/operator`, and `main`. The expected tag set is empty. New commit ids remain unknown until the current source is re-inventoried, sanitized, rescanned, and committed in the Topic Publication Copy.

## Replacement Sequence

1. Record a matching `exclusive_snapshot` binding authority for the existing remote, Research Topic, Topic Workspace, and canonical `main`.
2. Rebuild or overwrite the dirty legacy Topic Publication Copy from current source state. Do not treat its `topic-workspace/main` checkout or staged legacy topology as authority.
3. Generate and verify all retained source-identical paths, the `.isomer-publication/` overlay, root README, root `.gitmodules`, and exact mode `160000` gitlinks.
4. Push `components/topic-main`, then `components/topic-actors/operator`, then force-replace canonical `main`.
5. Use a separately approved provider-supported action to change remote HEAD from `topic-workspace/main` to `main`.
6. Delete `per-topic-actor/operator/main`, `topic-owner/main`, and `topic-workspace/main` with exact planned refspecs. No tag deletion is needed.
7. Reobserve the complete remote. Success requires exactly the three expected branches, no tags, and remote HEAD selecting `main`.

The resulting repository is an inspectable current evidence and artifact snapshot. It is not a backup that restores Workspace Runtime, source Git ancestry, the Topic Main worktree family, local identity, or a working Topic Workspace. Any operational reconstruction remains manual.

## Migration Blockers

| Blocker | Resolution |
| --- | --- |
| Legacy binding lacks `exclusive_snapshot` authority | Obtain one-time acknowledgement bound to the unchanged remote, topic, and workspace identity |
| Current copy contains dirty staged and untracked legacy projection state | Rebuild or overwrite it from a fresh current plan |
| Remote HEAD selects a branch scheduled for deletion | Change the hosted default branch to `main` through a separate approved provider action |
| Latest PDF validation record says publication gate pending | Reconcile the user's approval and rerun current PDF eligibility checks |
| Root readiness summary is outside the legacy retained inventory | Privacy-scan it and include it at its source path if eligible |
