# isomer-labs 0.5.0

This release compacts packaged system skills into three public packs with protected subskills, and adds operator context self-location, Kaoju Mindsets and explore planning, Operation Set acceptance, Topic Workspace Git management, and agent-fill TeX composition.

## Changes

### Added

- Added independent public newcomer welcomes for the core, DeepSci, and Kaoju packs. Each welcome teaches typical use cases, routing cues, prerequisites, mutation posture, and exact public commands before handing concrete work to its sibling entrypoint.
- Added the `isomer-skillset-manifest.v4` public-role catalog and `isomer-labs-skill-manifest.v5` receipts with ordered welcome and entrypoint projections per atomic pack.
- Added the `isomer-skillset-manifest.v3` public-pack and protected-capability catalog with stable logical ids, scoped invocation designators, dependency closure, callback stages, aliases, and compatibility floors.
- Added `isomer-labs-skill-manifest.v4` installation receipts with nested protected-member inventory, pack-integrity verification, staged legacy migration, safe stale cleanup, and rollback-preserving failure behavior.
- Added Operation Set acceptance: `ext research operation-sets inspect`, `accept`, and `verify` inventory every file in a worker operation set and require each to be bound to a durable record or explicitly discarded before closeout, persisting a resumable acceptance receipt. DeepSci pipeline stages and the new core `isomer-research-operation-set-recording` skill require accepted refs and a complete receipt before reporting success.
- Added read-only operator context self-location: `project self location` classifies the current working directory against registered Project, Topic Workspace, Topic Actor, and Agent boundaries, and `project self check --scope project|topic|topic-actor|agent` reconciles an intended target against ambient location and Effective Context. The operator entrypoint runs context preflight for context-sensitive routes and pins resolved selectors downstream, and Kaoju named-template, `init-tex`, `tex-status`, and `build-pdf` results include selected-context metadata.
- Added the protected Kaoju member `isomer-kaoju-explore` and its public `explore` entrypoint command for read-only interactive planning: it maintains an in-memory coverage map, asks up to five clarification questions, writes nothing by default, and routes to the selected Kaoju command only after explicit consent.
- Added Kaoju Mindsets: the public `create-topic` workflow derives user-editable Mindset Source files under `topic.intent.kaoju_mindsets` from packaged `paper.deep-dive`, `paper.skimming`, and `source-code.ingest` seeds, and applicable reading and ingestion Runs answer the questions into a Run-scoped `KAOJU:MINDSET-RECORD` Artifact.
- Added opt-in Topic Workspace Git management through the protected operator subskill `isomer-op-topic-workspace-git` with `status`, `local` (init, plan, status, commit, ignore), and `publish` (init, plan, status, sync) operations. Local tracking initializes a root repository only when ancestor repositories leave the workspace untracked and never touches remotes; publication builds a sanitized, ignored Topic Publication Copy under the Project temporary directory with privacy dispositions and pushes superproject and component branches to a user-provided remote.

### Changed

- Changed system-skill installation, status, upgrade, uninstall, discovery, and inspection to treat each welcome and entrypoint pair as one mutation unit, while reporting per-public-role evidence and migrating managed v4 installations to v5.
- Kept empty, help, and retained orientation commands compatible at each execution entrypoint by delegating read-only guidance to its public welcome sibling; refreshed agent hosts or new sessions are required to discover newly projected welcomes.
- Compacted packaged system skills into three user-facing packs. The 19 core, 21 DeepSci, and 13 Kaoju internal capabilities remain self-contained protected subskills beneath their execution entrypoint, while each pack exposes a public welcome and entrypoint pair.
- Standardized object-style invocation so skills and subskills use bare components, commands use `()`, and nested parent commands act as object generators for chains such as `manage-paper-template()->file()->put()`.
- Updated callback discovery, Skill Binding Projection, extension-query contracts, installer selection, inspection, operator recovery, and Isomer-Houmao private projection to resolve protected members by stable logical identity instead of flat package paths.
- Converted grouped Kaoju survey, dataset, and paper-template managers to explicit nested command routes while preserving role-specific content-template and LaTeX-template behavior.
- Changed Kaoju Reading List targets from a fixed three-priority plus three-secondary default to configurable counts. Priority and secondary targets can be set independently or requested as one total split, persist in the Reading List, and drive coverage warnings, while legacy lists keep the 3+3 default.
- Changed Kaoju MyST-to-TeX composition from mechanical regex conversion to an explicit agent-fill contract: `init-tex` scaffolds the template tree and a structured fill contract, and the agent fills frontmatter, abstract, bibliography, and tables by content judgment before build. LaTeX template adoption packs the full real template tree, rejects reference-only stub shims, and reports unfilled placeholders as diagnostics.

### Fixed

- Fixed record index row ids that silently truncated past 220 characters to append a SHA-256 digest suffix instead, and tightened edge extraction to skip array-container paths and drop the incorrect `provenance_refs` to `cites` relation.
- Fixed TeX composition to map MyST heading levels to the LaTeX section hierarchy (`#` to `\section`, `##` to `\subsection`, deeper to `\subsubsection`) instead of treating levels one and two as sections.
- Fixed the packaged system-skill manager's stale command examples, which placed an unsupported `--json` after `isomer-cli` subcommands; the corrected form uses the global `isomer-cli --print-json` option, and packaged-skill validation rejects command-local `--json` syntax.

### Breaking

- Stopped advertising or installing protected logical ids as independent top-level user skills. Invoke the owning public entrypoint instead; legacy DeepSci and Kaoju pipeline names remain deprecated selectors for complete-pack migration, and refreshed installations require an agent-host refresh or a new session.
- Renamed protected subskill entrypoints from `SKILL.md` to `SKILL-MAIN.md` so agent hosts that recursively scan for `SKILL.md` no longer register protected pack members as top-level skills; the six public welcome and execution entrypoints keep `SKILL.md`. Consumers opening a protected bundle's `SKILL.md` directly must switch to `SKILL-MAIN.md` or the role-aware resolver.
- Stopped lazily recreating absent Kaoju Mindset Sources. A Run now records a skipped posture and proceeds, while invalid existing Sources still pause for repair.

## Upgrade Notes

- Refresh the agent host or start a new session after upgrading so newly projected welcome skills are discovered.
- Invoke the owning public entrypoint for any capability previously called as a top-level protected skill; legacy DeepSci and Kaoju pipeline names remain deprecated selectors for complete-pack migration.

**Full Changelog**: https://github.com/CodeGandee/isomer-labs/compare/v0.4.0...v0.5.0
