## Context

Kaoju stores one current `KAOJU:READING-LIST` per accepted direction. The discover skill and pipeline command currently prescribe three reachable priority works and three reachable secondary works, while `_validate_reading_list` in `src/isomer_labs/kaoju/survey.py` applies the same fixed targets when it emits shortage warnings. Reading List payloads contain classified items but do not identify the target that bounded discovery.

The structured-record format permits additional section fields, so the change can add target metadata without changing the binding registry, semantic identifier, scope policy, or artifact profile. Existing Reading Lists must remain readable and retain their original 3+3 interpretation.

## Goals / Non-Goals

**Goals:**

- Derive deterministic priority and secondary targets from defaults, independent category requests, or one requested total.
- Persist the effective target and derivation with the direction-owned Reading List.
- Validate configurable targets and calculate shortage warnings against them.
- Preserve existing reachable-item, version-family, blocker, backfill, approval, and revision behavior.
- Keep Reading Lists that omit target metadata valid under the legacy 3+3 default.

**Non-Goals:**

- Changing how directions are selected or how source relevance is ranked.
- Imposing a new global maximum list size; the Survey Contract resource envelope and Gates continue to bound material requests.
- Changing which source classes qualify for a Reading List or treating discovery results as accepted evidence.
- Migrating or rewriting existing Reading List Artifacts.

## Decisions

### Store an Effective Target in the Reading List

New configurable Reading Lists will store `sections.target_counts` with integer `priority` and `secondary` fields plus a `basis` of `default`, `user-total`, or `user-categories`. `user-total` additionally stores `requested_total`. The payload will store `sections.achieved_counts` for the reachable priority and secondary item counts used by coverage reporting.

This keeps the search bound auditable and lets validation reproduce the user's request. Storing only the total was rejected because explicit category requests cannot always be reconstructed. Inferring the target from the final items was rejected because a shortage would erase the intended bound.

### Derive Counts Before Discovery

When the user supplies no count, the effective target is 3 priority and 3 secondary. When the user supplies category counts, each supplied count replaces that category's default and an omitted category remains 3. When the user supplies total `N`, the effective target is `(N + 1) // 2` priority and `N // 2` secondary, which gives the extra odd item to priority.

A total count and category counts are separate request modes. If a prompt supplies both modes, the agent asks for clarification instead of applying silent precedence. A total must be a positive integer. Category counts must be non-negative integers, and their combined effective target must be positive.

### Make Validation Backward-Compatible

The semantic validator will resolve missing `target_counts` as the legacy 3+3 default. When target metadata is present, it will validate the basis, integer ranges, required `requested_total`, total-count split, and optional-field posture. It will require `achieved_counts` and verify those counts against reachable `planned` and `human-added` items.

Shortage warnings will compare reachable counts with the resolved effective target. A category target of zero produces no warning for that category. Blocked, excluded, and duplicate candidates remain outside reachable counts, and duplicate reachable version families remain invalid.

### Keep Count Interpretation in Skill and Artifact Contracts

The pipeline command and discover skill will describe the three request modes, record the effective and achieved counts, and report shortages against the effective target. No new CLI count flags are needed because the public interface is the agent intent and the accepted structured Artifact.

## Risks / Trade-offs

- [Large user targets can increase search cost] → Keep resource bounds and Gate behavior in the Survey Contract, and preserve bounded search with an approvable shortage warning.
- [Legacy payloads do not record why 3+3 was used] → Interpret absent metadata as the documented legacy default without rewriting history.
- [Redundant achieved counts can drift from item state] → Validate them against the item collection whenever target metadata is present.
- [Natural-language requests can mix total and category counts] → Require clarification rather than choosing precedence implicitly.

## Migration Plan

Deploy the validator, skills, tests, and documentation together. Existing Artifacts without `target_counts` continue to validate as 3+3 lists. New or revised configurable lists include target and achieved metadata. Rollback leaves the extra structured fields harmless, although an older validator will again calculate warnings against 3+3.

## Open Questions

None.
