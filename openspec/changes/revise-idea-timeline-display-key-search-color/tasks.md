## 1. Runtime Display-Key Format

- [x] 1.1 Update Research Idea display-key validation to accept `I-<positive decimal>` and reject newly provided `I<index>` keys.
- [x] 1.2 Update automatic display-key allocation to emit `I-<index>` while preserving topic-scoped uniqueness and non-reuse behavior.
- [x] 1.3 Update display-key allocator/tombstone parsing so it reads both old `I<index>` and new `I-<index>` rows when computing the next index.
- [x] 1.4 Add explicit repair or migration planning for existing `I<index>` keys to matching `I-<index>` keys.
- [x] 1.5 Ensure display-key migration validates the complete plan and rejects collisions instead of silently remapping keys.
- [x] 1.6 Preserve read-only behavior so Project Web browsing, graph reads, timeline reads, exports, and validation do not migrate display keys.

## 2. Graph and Timeline Read Models

- [x] 2.1 Update graph node payloads and contract schemas to expose display keys in `I-<index>` format.
- [x] 2.2 Update Idea Graph visible label formatting so React Flow and Sigma labels lead with the display key when present.
- [x] 2.3 Update Idea Timeline row derivation to render `I-<index>` keys and parent display-key references.
- [x] 2.4 Keep canonical `idea_id` as row identity and display key as visible table identity only.
- [x] 2.5 Add diagnostics or recent-errors coverage for old or missing display keys without crashing graph or timeline views.

## 3. Timeline Search and Visibility

- [x] 3.1 Replace Idea Timeline status/relation/field-specific search controls with one fuzzy text search bar.
- [x] 3.2 Implement fuzzy matching over display key, title, aliases, one-liner, family, status, idea id, parent display-key labels, parent titles, relation kinds, and rendered table-entry fields.
- [x] 3.3 Ensure search evaluates supporting Research Idea rows but does not show them while Supporting Records is disabled.
- [x] 3.4 Ensure enabling Supporting Records after entering a query reveals matching supporting rows without clearing the search.
- [x] 3.5 Preserve existing sorting, entry-count, selection, and double-click/double-tap behavior after simplifying search controls.

## 4. Settings and Styling

- [x] 4.1 Change Idea Timeline row colorization default to off for browsers without a stored preference.
- [x] 4.2 Keep Project Settings controls for enabling/disabling row coloring and configuring primary/supporting row colors.
- [x] 4.3 Ensure row selection and row metadata remain visible through non-color cues when colorization is off.
- [x] 4.4 Update local-storage normalization and settings tests for the default-off behavior.

## 5. Documentation and Tests

- [x] 5.1 Update `docs/ui/contracts/` pages for `I-<index>` display keys, timeline fuzzy search state, and default-off row coloring.
- [x] 5.2 Update developer or context docs that mention the older `I<index>` display-key shape.
- [x] 5.3 Add backend tests for new key allocation, old-key migration, collision rejection, and no read-path migration.
- [x] 5.4 Add frontend tests for graph labels, timeline fuzzy search, supporting-row visibility, display-key rendering, and default-off colorization.
- [x] 5.5 Rebuild Project Web static assets.
- [x] 5.6 Run `npm --prefix web/ui test`.
- [x] 5.7 Run `npm --prefix web/ui run build`.
- [x] 5.8 Run `pixi run lint`.
- [x] 5.9 Run `pixi run typecheck`.
- [x] 5.10 Run `pixi run test`.
