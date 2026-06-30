## ADDED Requirements

### Requirement: Project Manager Uses Essential and Complete Output
The Project Manager operator skill SHALL split its output contract into Essential Output and Complete Output.

#### Scenario: Essential project output reports lifecycle status
- **WHEN** `isomer-admin-project-mgr` reports a result without a complete-output request
- **THEN** it reports Project root, Project manifest status, selected Research Topic or Topic Workspace when relevant, operation result, important changed paths, blockers or diagnostics, and next action

#### Scenario: Complete project output preserves lifecycle bookkeeping
- **WHEN** complete output is requested from `isomer-admin-project-mgr`
- **THEN** it reports Project Manifest path, Houmao project and overlay paths, Research Topic refs, Topic Workspace refs, effective topic context, runtime status, cleanup plan, relocation plan, commands run, diagnostics, and next action when those fields apply

#### Scenario: Cleanup and relocation stay understandable by default
- **WHEN** cleanup or content-root relocation runs without a complete-output request
- **THEN** Essential Output reports the selected mode, planned or applied changes, skipped or blocked targets, and next action
- **AND** Complete Output carries the full target list, warnings, unmanaged leftovers, and command evidence
