# houmao-manifest-reconciliation Specification

## Purpose
Define the Houmao adapter JSON manifest and reconciliation contract that lets Isomer understand, adopt, validate, and report Houmao-backed Agent Team Instance runtime state without promoting Houmao-specific fields into generic Isomer schema.

## Requirements
### Requirement: Houmao Adapter JSON Manifest Contract
The system SHALL use JSON as the durable manifest format for Houmao adapter link, launch-material, and runtime state manifests.

#### Scenario: Quick launch writes manifest family
- **WHEN** Isomer quick launch prepares a Houmao-backed Agent Team Instance
- **THEN** the adapter writes or updates `adapter-link.json` and `launch-material-manifest.json` before launch and writes or updates `adapter-runtime-manifest.json` after observing the launch result

#### Scenario: Direct Houmao operation uses link manifest
- **WHEN** a user intends to operate a Houmao-backed Agent Team Instance directly through `houmao-mgr`
- **THEN** the system can export or validate an `adapter-link.json` file that carries Isomer refs, Houmao project refs, expected profile refs, expected agent refs, and Provenance refs

#### Scenario: JSON is durable and interchange format
- **WHEN** an Isomer CLI or API command emits machine-readable output for manifest export, reconciliation, adoption, or integrity inspection
- **THEN** the output is deterministic JSON and durable manifest files are JSON documents with separate manifest kind fields

### Requirement: Houmao Manifest Integrity
The system SHALL compute manifest integrity from parsed canonical JSON and referenced launch-material file digests.

#### Scenario: JSON formatting does not create drift
- **WHEN** JSON whitespace or object field ordering changes in a Houmao adapter JSON manifest
- **THEN** canonical manifest digest comparison does not report runtime drift solely because of that formatting change

#### Scenario: Referenced file bytes create drift
- **WHEN** a launch-material file referenced by `launch-material-manifest.json` changes bytes after its last recorded digest
- **THEN** reconciliation reports material drift for the affected file and links the drift to the relevant Agent Team Instance or Agent Instance refs when known

#### Scenario: Secret material is rejected
- **WHEN** reconciliation detects credentials, tokens, passwords, API keys, or other secret material in a Houmao adapter manifest payload intended for Workspace Runtime recording
- **THEN** the system rejects the recording operation and reports a redacted diagnostic without storing the secret-bearing payload

### Requirement: Houmao Reconciliation Classification
The system SHALL classify Houmao-backed Agent Team Instance reconciliation outcomes from JSON manifests, Workspace Runtime records, and live Houmao inspection.

#### Scenario: Linked but not launched
- **WHEN** `adapter-link.json` exists and no matching live Houmao runtime state is observed
- **THEN** reconciliation reports the Agent Team Instance as `linked` with no launch adoption

#### Scenario: Isomer launched state is confirmed
- **WHEN** Workspace Runtime records an Isomer quick launch and live Houmao runtime state still matches the adapter manifests
- **THEN** reconciliation reports `launched_by_isomer` and updates observation timestamps or diagnostics without changing generic identity records

#### Scenario: Direct Houmao launch is detected
- **WHEN** live Houmao runtime state matches an adapter link or user-supplied mapping but Workspace Runtime has no recorded launch for that state
- **THEN** reconciliation reports `external_detected` until an explicit adopt operation records the mapping

#### Scenario: Mapping conflict is detected
- **WHEN** one Isomer Agent Instance maps to multiple Houmao managed agents or one Houmao managed agent maps to multiple Isomer Agent Instance refs
- **THEN** reconciliation reports `conflicted` and refuses adoption until the conflict is resolved or a manual mapping decision is supplied

### Requirement: Direct Houmao Adoption
The system SHALL require an explicit adoption operation before externally launched Houmao state becomes recorded Isomer Agent Team Instance runtime state.

#### Scenario: Adoption records external launch
- **WHEN** a user approves adoption of an externally launched Houmao-backed Agent Team Instance
- **THEN** the system records adapter runtime refs, Agent Instance mappings, mapping confidence, manifest refs, reconciliation outcome, and Provenance Records in Workspace Runtime

#### Scenario: Adoption preserves user-authored material
- **WHEN** direct Houmao launch material differs from Isomer-generated material but passes path, secret, and mapping validation
- **THEN** adoption records the material as user-authored adapter launch material rather than overwriting it with regenerated Isomer material

#### Scenario: Adoption rejection is durable
- **WHEN** adoption is rejected because mapping, integrity, path, or secret checks fail
- **THEN** the system records or returns a rejected reconciliation result with diagnostics and does not mutate Agent Team Instance launch state
