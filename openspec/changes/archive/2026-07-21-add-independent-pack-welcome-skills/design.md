## Context

The applied `regroup-system-skills` baseline compacts 57 former top-level skills into three public entrypoint directories with 54 protected subskills. In that model, `SystemSkillPack` has one `source_path`, one `entry_skill`, one public-command list, and one top-level projection. Core welcome survives only as protected capability `isomer-op-entrypoint->welcome`; DeepSci and Kaoju have no dedicated welcome capability. Catalog lookup, materialization, installer selection, v4 receipts, explicit-root inspection, live-inventory classification, callback metadata, extension reporting, and validators all assume that one public entrypoint is synonymous with one complete pack.

This is efficient for informed users but weak for first contact. An entrypoint can route a concrete request only after the user knows enough vocabulary to describe the intended operation. The welcome role instead needs to teach the pack's intended work, show representative request language and exact public command forms, explain prerequisites and mutation boundaries, and hand the user to the entrypoint without executing the task.

The historical `isomer-op-welcome` bundle provides a useful core baseline. It already owns read-only path comparison, extension discovery, command mapping, and next-step guidance. This change restores that bundle as a public sibling rather than recreating the same procedure inside the entrypoint. DeepSci and Kaoju need equivalent pack-specific onboarding authored from their current command inventories, protected-member routing descriptions, and workflow contracts.

The design preserves canonical Isomer domain language. Welcome skills describe Projects, Research Topics, Topic Workspaces, Topic Actors, Agent Teams, Project Operator Sessions, and extension paradigms using the project language authority; they do not introduce another durable domain object.

## Goals / Non-Goals

**Goals:**

- Install and expose one independent welcome skill and one independent execution entrypoint for each core, DeepSci, and Kaoju pack.
- Make welcome useful before the user knows entrypoint command ids or internal capability names.
- Teach both deterministic command forms and representative natural-language routing cues without presenting cues as a hidden parser grammar.
- Keep welcome read-only and keep mutation, prerequisite recovery, and task completion with the execution entrypoint and protected owners.
- Preserve complete-pack installation, protected logical ids, callback targets, extension ids, and entrypoint invocation names.
- Make catalog, receipt, status, inspection, upgrade, and validation evidence cover all public projections in a pack.
- Safely migrate current pack-aware installations and older flat installations without overwriting untracked paths.

**Non-Goals:**

- This change does not make protected subskills independently public again.
- This change does not change the scientific methods, survey process, Project lifecycle, Topic lifecycle, callback semantics, or run-to prerequisite contracts owned by existing skills.
- This change does not make welcome a task executor, setup wizard, or mutation approval surface.
- This change does not require users to memorize literal natural-language keywords. Canonical command ids are deterministic; routing cues are teaching examples.
- This change does not add a new extension id, Project declaration, durable record type, or access-control boundary.

## Decisions

### 1. Every Pack Has Two Public Roles

Each current pack exposes exactly two public skills:

| Pack | Welcome | Execution Entrypoint |
| --- | --- | --- |
| core | `isomer-op-welcome` | `isomer-op-entrypoint` |
| deepsci | `isomer-ext-deepsci-welcome` | `isomer-ext-deepsci-entrypoint` |
| kaoju | `isomer-ext-kaoju-welcome` | `isomer-ext-kaoju-entrypoint` |

Welcome and entrypoint are sibling package resources and sibling top-level host projections. Protected subskills remain physically nested only under the execution entrypoint. The core `isomer-op-welcome` capability row and `welcome` protected-member row are removed, so `isomer-op-entrypoint->welcome` is no longer a canonical object designator.

The names use `isomer-op-*` for the core operator surface and `isomer-ext-<extension-id>-*` for public extension surfaces. Existing `isomer-<extension>-<purpose>` logical ids remain protected capability identities.

Alternative considered: keep welcome protected and improve entrypoint help. That retains the discoverability problem because users must first know the entrypoint and its help vocabulary. Alternative considered: make every protected owner public again. That reintroduces the inventory noise that compaction removed.

### 2. Welcome Teaches; Entrypoint Executes

Every welcome skill is read-only and has a common orientation shape:

1. Default or `help` gives a concise pack introduction and several high-value first tasks.
2. `show-options` groups typical use cases by user goal.
3. `choose-path` maps an ambiguous goal to one recommended entrypoint request.
4. `show-command-map` presents the complete public entrypoint command inventory.
5. `next-step` recommends the next invocation and may use only explicitly useful read-only context.

Core welcome additionally retains `show-extensions` and the established manual, Agent Team, DeepSci, and Kaoju start-path routines. Extension welcome skills use the common commands and pack-specific use-case references rather than duplicating execution pages.

Each typical-use-case row contains a one-sentence purpose, representative user phrases or routing cues, required context, canonical entrypoint command or task form, one exact invocation example, the action users should expect, mutation posture, and likely next step. A separate complete command map covers every current entrypoint public command once. Authors derive this language from entrypoint command contracts and protected-subskill routing metadata, but they must adapt and synthesize it for a newcomer rather than copy descriptions verbatim.

Welcome metadata permits implicit selection only for orientation, comparison, discovery, command-learning, and how-to requests. A concrete task routes to the entrypoint. Welcome never treats an example phrase as authorization to execute its example.

Alternative considered: generate welcome text directly from manifest descriptions. Generated inventory would remain accurate but would not supply the task framing, prerequisite explanation, or examples newcomers need. The chosen design keeps curated teaching content and validates its command coverage against the manifest.

### 3. Manifest v4 Separates Pack and Public-Skill Records

`manifest.toml` advances to `isomer-skillset-manifest.v4`. A pack retains `pack_id`, kind, extension id, availability, compatibility floor, ordered protected-member ids, and a designated `entry_skill`. It gains an ordered `public_skills` list.

Separate public-skill records contain:

- canonical `name`, owning `pack_id`, and role `welcome` or `entrypoint`;
- manifest-relative `source_path`;
- ordered public commands, aliases, callback insertion points, and optional compatibility floor.

The parser requires exactly one welcome and one entrypoint per current pack, requires `pack.entry_skill` to name the entrypoint-role record, and requires globally unique public names and paths. Extension entrypoints must remain `isomer-ext-<extension-id>-entrypoint`; extension welcomes must be `isomer-ext-<extension-id>-welcome`. Core names are fixed to `isomer-op-entrypoint` and `isomer-op-welcome`.

Protected capabilities continue to name their pack and stable logical id. Their source paths must remain below the designated entrypoint's `subskills/` directory, and their invocation designators continue to start with the designated entrypoint. Welcome skills own no protected members and expose no callback insertion points in this change.

Compatibility accessors may continue to expose `pack.entry_skill`, entrypoint commands, and entrypoint aliases to existing internal callers while new APIs enumerate `pack.public_skills` and resolve any public skill to its owning pack and role.

Alternative considered: add a single `welcome_skill` field beside existing pack fields. That is a smaller manifest edit but preserves the false model that only the entrypoint is a first-class public skill. First-class public-skill records make discovery, validation, future roles, and per-skill metadata explicit.

### 4. The Pack Remains the Selection and Mutation Unit

Group and extension selectors continue to select packs. Supplying either a welcome or entrypoint name through `--skill` resolves to the owning complete pack. Supplying a protected logical id continues to resolve to the owning pack with the existing compatibility diagnostic. Listing and JSON output distinguish the selected pack from its two public projections.

Install and upgrade stage both public directories plus the entrypoint's protected inventory before changing the live root. Any unsafe conflict at either public destination blocks the whole pack unless existing force and ownership rules authorize replacement. Commit and rollback operate across both sibling projections. Uninstall removes both receipt-owned public projections for the selected pack and never removes one public role in isolation.

This keeps welcome usable: installing a welcome alone would teach commands for a missing entrypoint, while installing an entrypoint alone would recreate the onboarding gap.

Alternative considered: make each public skill independently selectable and uninstallable. That permits incomplete packs and makes extension integrity ambiguous, so it is rejected.

### 5. Receipt v5 Records Packs with Multiple Public Projections

The target-root receipt advances to `isomer-labs-skill-manifest.v5`. Each pack record contains pack id, designated entrypoint, package version, the ordered public projection records, and the entrypoint's protected-member inventory. Each public projection record contains name, role, source path, projection mode, and skill version. Protected records retain logical id, relative nested path, invocation designator, and version.

Status classifies a pack as verified only when:

- both public destinations exist with correct identities, versions, projection modes, and receipt ownership;
- the entrypoint contains exactly the declared protected members with valid identities and compatible versions;
- welcome is a standalone valid bundle and does not contain or depend on the entrypoint's private subskill tree.

Explicit-root inspection reports per-public-skill observations and aggregate pack coverage. Live inventory can report `welcome_seen` and `entrypoint_seen` independently, but names alone never establish protected integrity or complete pack verification. Extension discovery returns both public skill records and continues to mark the entrypoint as the execution surface.

Alternative considered: store two independent v4 skill records with the same pack id. That can represent the files but cannot express atomic pack ownership, designated roles, or a complete-pack version boundary clearly, and older tools could mistake one record for a complete pack.

### 6. Current Invocation Forms Remain Usable During Migration

The canonical newcomer invocation becomes `$<pack-welcome>`; the canonical task invocation remains `$<pack-entrypoint> use <command> to <task>` or a concrete task-only entrypoint request.

For at least one minor release, entrypoint `help` and former welcome-style public commands delegate read-only behavior to the corresponding public welcome skill and emit the canonical welcome invocation. The entrypoint does not keep copied welcome resources. Empty entrypoint invocation delegates to welcome while preserving supplied context. Removing these compatibility routes requires a separate change after the compatibility period.

Internal guidance replaces `isomer-op-entrypoint->welcome` with `$isomer-op-welcome`. References from core welcome to extension onboarding use `$isomer-ext-deepsci-welcome` and `$isomer-ext-kaoju-welcome`; references that start concrete work use the extension entrypoints.

Alternative considered: remove all former welcome commands immediately. Delegation costs little and avoids breaking established prompts while still restoring a single content owner.

### 7. Upgrade Is Staged and Conflict-Safe

Managed upgrade performs these steps per selected pack:

1. Read v1-v4 receipt evidence and classify current public or legacy flat paths.
2. Refuse an untracked conflicting target at any new public welcome path unless the user has separately resolved it.
3. Stage and recursively validate both new public projections.
4. Back up every receipt-owned destination that will change.
5. Commit both public projections and the v5 receipt.
6. Remove only obsolete paths tracked by the supported receipt, including an old independently tracked welcome path where applicable.
7. Roll back both projections and the receipt if commit fails before the new receipt is durable.

Replacing the current core entrypoint naturally removes its nested welcome copy only after the sibling welcome has staged successfully. Upgrading an older flat installation may reuse a receipt-tracked top-level `isomer-op-welcome` destination. Untracked welcome-like paths are preserved and reported as conflicts. A host refresh or new agent session remains required after projection changes.

### 8. Validation Treats Welcome Quality as a Contract

Manifest-aware validation enumerates both public records and recursively validates protected entrypoint members. Welcome validation checks identity, metadata, implicit-invocation scope, common commands, read-only posture, exact entrypoint handoff names, self-contained local references, command-map completeness, unique command coverage, representative use-case examples, mutation-boundary language, and prohibition of direct protected-skill invocation.

Pack-specific validation checks that core welcome covers common Project, Topic, topology, extension, GUI, identity, system-skill, and Toolbox paths; DeepSci welcome covers hypothesis, empirical, paper, revision, rebuttal, and polish patterns; and Kaoju welcome covers landscape discovery, reading-list work, evidence intake, comparison, trials, paper production, and wiki export. These are teaching categories, not new workflow owners.

Tests cover manifest v4 parsing, public-role identity collisions, pack selectors, v5 receipt round trips, atomic projection and rollback, migration from current v4 and older flat receipts, status and inspection evidence, discovery JSON, validator failures, and copy/symlink projection.

## Risks / Trade-offs

- [Public skill count increases from three to six] → Keep all workflow owners protected and document the welcome/entrypoint pair as two roles, not six unrelated products.
- [Curated use-case prose can drift from command metadata] → Validate full command-map coverage and exact command ids against manifest v4 while allowing curated examples to remain human-authored.
- [Natural-language cues may be mistaken for required magic keywords] → Label them as representative routing cues and always pair them with a deterministic command form.
- [Multiple public projections make install transactions more complex] → Stage and validate the complete pack, use bounded backups, write one v5 pack receipt, and roll back as a unit.
- [Older CLIs do not understand v5 receipts] → Treat v5 as a compatibility boundary, reject mutation from unsupported tools, document minimum compatible CLI behavior, and preserve v1-v4 read-only migration support in the new CLI.
- [Existing prompts use entrypoint welcome commands] → Retain one release of read-only delegation and emit the canonical independent welcome invocation.
- [Implicit welcome routing could intercept concrete tasks] → Restrict welcome trigger metadata and workflow gates to orientation and how-to intent; concrete tasks hand off without execution.

## Migration Plan

1. Add manifest v4 and catalog support while retaining read-only parsing of manifest v3 fixtures.
2. Move the existing core welcome bundle from the entrypoint subskill tree to `operator/isomer-op-welcome`, then remove its protected capability declaration.
3. Author and validate the DeepSci and Kaoju welcome sibling bundles.
4. Update entrypoints, route references, extension discovery, callback ownership metadata, and compatibility delegation.
5. Implement pack-atomic multi-public selection, projection, receipt v5, status, inspection, upgrade, uninstall, and rollback.
6. Add migration tests for current v4 pack receipts and earlier flat receipts, including tracked and untracked welcome conflicts.
7. Update documentation and changelog, align every packaged skill version with `project.version`, and run the full repository validation suite.
8. In release guidance, instruct users to run managed upgrade and refresh or restart the agent host.

Rollback before host release restores manifest v3, v4 receipt writing, and the protected core welcome layout. After a v5 installation exists, rollback requires a CLI that can read v5 and deliberately migrate back; an older CLI must refuse mutation rather than guess at ownership.

## Open Questions

None. Empty entrypoint invocation delegates to the independent welcome skill, and compatibility aliases remain for at least one minor release unless a later change explicitly removes them.
