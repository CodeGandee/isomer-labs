## Why

The research-paradigm skill folders currently use the long
`isomer-labs-research-*` prefix, which is verbose in skill listings, manifests,
and role mappings. Renaming them to `isomer-rsch-*` keeps the Isomer identity
while making the research skill names shorter and easier to scan.

## What Changes

- **BREAKING** Rename every skill folder under `skillset/research-paradigm/`
  from `isomer-labs-research-<purpose>` to `isomer-rsch-<purpose>`.
- Update each renamed skill's `SKILL.md` frontmatter `name:` value to match its
  new folder name.
- Update same-skill local references, manifests, documentation, team mappings,
  and examples that mention the old names.
- Preserve skill purposes, descriptions, reference contents, manifests, and
  Isomer concept mappings; this is a naming change, not a methodology rewrite.
- Keep non-skill documentation traceable enough that archived OpenSpec history
  can still explain where the previous names came from.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `research-paradigm-skills`: change the required skill naming convention and
  folder list from `isomer-labs-research-*` to `isomer-rsch-*`.

## Impact

- Affects `skillset/research-paradigm/` folder names, `SKILL.md` frontmatter,
  local `agents/openai.yaml` manifests, and local skill references.
- Affects `skillset/README.md`, `skillset/research-paradigm/README.md`, and
  team docs that map generic research roles to installed skills.
- Does not change Python package code, Pixi configuration, runtime APIs, or the
  research methodology encoded in the skills.
