# UC-02 Reading List Scope and Default Size

Status: accepted
Date: 2026-07-14
Related: ADR-0001

The initial UC-02 draft left three questions open: how the next direction is chosen, whether the reading list artifact is per-direction or global, and how many items a default list should contain. These decisions affect the artifact shape, the user interaction, and the handoff to the examine stage.

## Current Decision

- UC-02 does **not** decide how the next survey direction is selected. Direction selection and sequencing belong to UC-01 and to future scheduling logic. UC-02 assumes the direction is already selected when the reading list is built.
- The reading list artifact is **direction-owned**: one `kaoju:reading-list` artifact per direction. A direction identifier is part of the artifact metadata so downstream stages know which scope the list covers.
- A default reading list **targets** 3 priority items and 3 secondary items. The agent tries its best to reach that count on the first attempt, but falling short is a warning rather than a blocker; the human can approve a shorter list or ask the agent to expand coverage.
- Blocked or identity-unresolved candidates remain in discovery provenance but do not count toward the reachable 3+3 target. The agent performs bounded backfill before reporting a coverage deficit.
- Each reading-list item includes a `priority` field with values `priority` or `secondary`.

## Affected Artifacts

- `usecases/uc-02-collect-online-info-and-build-reading-list.md`: clarified that the artifact is per-direction, added `priority` to the item metadata table, updated the example response to show 3 priority + 3 secondary items, and resolved the three open questions.
- `README.md`: added ADR link to artifact map.

## Refinement History

### 2026-07-14 - Blocked-Item Backfill

- Resolved the remaining backfill question: blocked items do not satisfy the reachable target, bounded backfill is automatic, and an unresolved shortage remains a non-blocking warning.

### 2026-07-14 - Initial Decision

- Instruction: "this usecase does not concern how to pick the next direction to explore, and it is one artifact containing all in-depth reading list for one direction, so this is direction-owned reading list, default to have 3 items as priority and 3 items as secondary in a reading list"
- Applied changes:
  - Updated durable output description for `kaoju:reading-list` to state one artifact per direction.
  - Added `priority` field to the reading-list item metadata table.
  - Updated Event 001 example response to report 6 sources (3 priority, 3 secondary).
  - Updated Event 002 example response to group items under "Priority reads" and "Secondary reads".
  - Noted that the 3+3 size is a target, not a blocker; the agent tries its best and warns if the target is missed.
  - Replaced the three resolved initial questions with assumptions and deferred blocked-item backfill behavior to a later refinement.
