## ADDED Requirements

### Requirement: Exact Idea Fragments Carry Display Fields
Exact object-valued source fragments for Primary Ideas SHALL carry the same `title` and `summary` display fields as canonical Research Ideas.

#### Scenario: Primary idea fragment resolves with display fields
- **WHEN** a latest Primary Idea realization resolves to an exact object-valued source fragment
- **THEN** the resolved object contains non-empty `title` and `summary`
- **AND** the idea detail read model can expose those values as the idea content display fields

#### Scenario: Fragment display fields differ from source aliases
- **WHEN** the resolved source fragment also contains a source-local label, candidate id, raw idea id, or other alias
- **THEN** those alias values remain alias or realization metadata
- **AND** they do not replace the fragment's `title`, `summary`, canonical `idea_id`, or display key

#### Scenario: Missing fragment summary is invalid
- **WHEN** a mutating CLI, API, or record-write convenience creates or updates a latest Primary Idea realization whose exact source fragment lacks `summary`
- **THEN** the write is rejected with a deterministic source-fragment display diagnostic
- **AND** validate reports the same condition for existing data without mutating payload files

### Requirement: Profile-aware Import Preserves Summary
Profile-aware idea import SHALL preserve authored `title` and `summary` from exact idea-bearing payload objects.

#### Scenario: Import uses idea object summary
- **WHEN** `import-from-record` imports a raw idea slate, candidate frontier, selected hypothesis, selected idea draft, rejected/deferred idea, route decision, or paper-facing idea seed profile
- **THEN** each imported Research Idea receives `title` and `summary` from the exact idea-bearing source object
- **AND** the import plan does not duplicate the same source text into both fields unless the source object itself contains that duplicate text

#### Scenario: Import reports non-interpretable idea object
- **WHEN** a profile-aware import finds an idea-bearing object without `title` or `summary`
- **THEN** the import plan reports a diagnostic naming the profile, source record, source JSON path, and missing field
- **AND** it does not guess from nearby context-only sections
