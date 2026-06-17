## Context

The archived `research-paradigm-skills` spec currently defines skill folders
with the `isomer-labs-research-<purpose>` naming convention. The implemented
skillset also has documentation, role mappings, `SKILL.md` frontmatter, and at
least one `agents/openai.yaml` manifest that use those names.

The requested target naming convention is `isomer-rsch-<purpose>`, for example
`isomer-rsch-analysis`. This is a repo-local documentation and skill-packaging
rename. It should not change the research methodology, evidence rules,
provenance model, or TBD-surface mappings.

## Goals / Non-Goals

**Goals:**

- Rename every research-paradigm skill folder from
  `isomer-labs-research-<purpose>` to `isomer-rsch-<purpose>`.
- Update each renamed skill's `SKILL.md` frontmatter `name:` to match the
  folder name.
- Update local manifests, relative links, skill listings, team mappings, and
  docs that refer to the old names.
- Preserve methodology content, reference files, provenance notices, and local
  self-contained packaging work already done for `analysis`.
- Validate that old skill names no longer appear in active skill docs except
  where archived history or explicit migration notes require them.

**Non-Goals:**

- Do not change skill descriptions or research-stage responsibilities unless a
  wording update is needed to remove the old name.
- Do not create compatibility alias folders unless a follow-up change explicitly
  decides to support aliases.
- Do not change Python package code, Pixi configuration, OpenSpec archive
  history, or source DeepScientist material.
- Do not rework the analysis skill's richer references beyond preserving their
  internal links after the folder rename.

## Decisions

### Rename folders and frontmatter together

Each folder rename must be paired with the corresponding `SKILL.md` `name:`
change. Skill discovery depends on names and folders staying coherent, and
having mismatched names would make validation ambiguous.

Alternative considered: rename folders only. That would preserve old trigger
names and defeat the purpose of shortening the skill names.

### Use direct rename with no alias folders

The implementation should remove the old active folders rather than keep alias
copies. Alias folders would double the visible skill list and risk stale copies
of methodology references.

Alternative considered: add alias stubs from old names to new names. That might
help transition, but skills are file bundles, not importable modules with a
clear alias mechanism. It is safer to make the rename explicit and update all
repo references.

### Preserve relative links inside each moved skill

Links that point within a skill directory should continue to point within that
directory after the rename. Links from stage skills to the shared skill should
be updated from `../isomer-labs-research-shared/SKILL.md` to
`../isomer-rsch-shared/SKILL.md`.

Alternative considered: make every skill self-contained during the rename.
That is larger than the naming change. The existing self-contained analysis
work should be preserved, but other skills can keep using the shared skill
unless a future change broadens the packaging rule.

### Treat archived OpenSpec files as history

The active skillset, main spec, and current docs should use `isomer-rsch-*`.
Archived OpenSpec change files may retain old names because they record the
original extraction decision.

Alternative considered: rewrite archived history. That would obscure what was
originally proposed and implemented.

## Risks / Trade-offs

- Stale references to old names remain in active docs -> Run targeted `rg`
  searches for `isomer-labs-research-` outside `openspec/changes/archive/`.
- Manifests drift from `SKILL.md` frontmatter -> Validate every renamed skill's
  folder name, frontmatter `name:`, and manifest prompt where present.
- Shell renames lose files under Git history -> Use `mv` or equivalent tracked
  renames and inspect `git status`.
- Archived specs still mention old names -> Accept as historical context, but
  make sure the active main spec is updated through the delta spec.

## Migration Plan

1. Build a rename map for all current `isomer-labs-research-*` folders.
2. Rename the folders under `skillset/research-paradigm/`.
3. Update each `SKILL.md` `name:` value and any local references to old folder
   names.
4. Update `agents/openai.yaml` manifests and default prompts when present.
5. Update active docs and team mappings to use `isomer-rsch-*`.
6. Update the main OpenSpec requirement through this change's delta spec.
7. Validate with structure, frontmatter, manifest, and stale-name scans.

Rollback is mechanical: restore the prior folder names, frontmatter names,
docs, and spec wording from Git.
