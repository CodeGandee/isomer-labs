## ADDED Requirements

### Requirement: Research Template Domain Failures Honor Output Mode
The system SHALL render failures from `isomer-cli ext research templates` according to the root-selected CLI output mode while preserving the domain error code, diagnostics, non-zero exit status, and known mutation state.

#### Scenario: Context failure is text by default
- **WHEN** a caller runs `isomer-cli ext research templates list` without root-level `--print-json` and no Effective Topic Context can be selected
- **THEN** the command exits non-zero and emits human-readable Isomer diagnostics and topic-selection guidance
- **AND** it does not emit a raw JSON document

#### Scenario: Context failure uses versioned JSON when requested
- **WHEN** a caller runs `isomer-cli --print-json ext research templates list` and no Effective Topic Context can be selected
- **THEN** the command exits non-zero and emits valid JSON using the `isomer-cli-output.v1` wrapper
- **AND** the response includes command path, `ok: false`, `mutated: false`, `error.code: context_resolution_failed`, and the context diagnostics

#### Scenario: Template operation failure honors output mode
- **WHEN** a research-template subcommand reaches a domain failure such as `template_not_found`, `template_dir_missing`, or `template_already_exists`
- **THEN** text mode emits a concise human-readable failure and JSON mode preserves the stable domain error under the versioned CLI wrapper
- **AND** both modes exit non-zero without claiming a mutation that did not occur

#### Scenario: Successful template payload compatibility is preserved
- **WHEN** a research-template subcommand succeeds
- **THEN** this change does not remove or rename the existing command-specific success payload fields
