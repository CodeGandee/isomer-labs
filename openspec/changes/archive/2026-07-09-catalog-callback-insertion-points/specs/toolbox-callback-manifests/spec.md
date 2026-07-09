## ADDED Requirements

### Requirement: Toolbox Callback Targets Use Insertion Point Catalog
Toolbox callback manifest validation SHALL validate each callback target skill and stage pair against manifest-declared callback insertion points.

#### Scenario: Toolbox callback targets declared insertion point
- **WHEN** a Toolbox callback manifest entry targets a system skill and stage pair declared in the packaged callback insertion-point catalog
- **THEN** manifest validation accepts the target pair subject to existing Toolbox callback key, source, path, and duplicate-key rules

#### Scenario: Toolbox callback targets undeclared insertion point
- **WHEN** a Toolbox callback manifest entry targets a packaged system skill and stage pair that is not declared as a callback insertion point
- **THEN** manifest validation rejects the entry with a deterministic diagnostic that names the missing insertion point

#### Scenario: Optional extension target does not require filesystem verification
- **WHEN** a Toolbox callback manifest entry targets a known optional system extension insertion point
- **THEN** validation uses the packaged callback insertion-point catalog and does not inspect Project operator skill files
