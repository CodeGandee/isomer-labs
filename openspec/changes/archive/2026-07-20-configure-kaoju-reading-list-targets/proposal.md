## Why

Kaoju currently fixes every direction-owned Reading List target at three priority works and three secondary works. Users need to control either category count or request one total count while preserving the existing bounded-search, shortage-warning, and human-approval behavior.

## What Changes

- Allow users to set the priority and secondary target counts independently, with an omitted category defaulting to three.
- Interpret a user-requested total of `N` works as `ceil(N / 2)` priority works and `floor(N / 2)` secondary works.
- Persist the effective target counts and their derivation in each Reading List so validation and later inspection use the accepted target rather than a hardcoded default.
- Calculate coverage warnings against the effective targets while continuing to exclude blocked, excluded, and duplicate candidates from reachable counts.
- Preserve legacy Reading Lists by treating absent target metadata as the existing three-priority and three-secondary default.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `kaoju-survey-intents`: Make direction-owned Reading List targets configurable and define default, explicit-category, total-count, validation, persistence, and shortage semantics.

## Impact

The change affects the Kaoju survey-intent specification, Reading List semantic validation, packaged Kaoju discover and pipeline skill guidance, survey-process tests, and the accepted Reading List design documentation. It adds no external dependency and does not change Reading List scope, approval, acquisition, or evidence semantics.
