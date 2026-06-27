## ADDED Requirements

### Requirement: Installed Entrypoint Failure Normalization
The system SHALL normalize failures from the installed `isomer-cli` entrypoint into Isomer diagnostics by default, including Click invocation errors, non-usage Click exceptions, keyboard interrupts, and unexpected Python exceptions.

#### Scenario: Click usage error is normalized
- **WHEN** a caller invokes `isomer-cli` with a missing argument, unknown command, invalid option, invalid choice, or extra argument
- **THEN** the process exits with a non-zero status and prints an Isomer diagnostic instead of Click's raw error-only output

#### Scenario: Unexpected Python exception is normalized
- **WHEN** a command raises an unexpected Python exception during installed `isomer-cli` execution
- **THEN** the process exits with a non-zero status and prints an internal-error Isomer diagnostic instead of an uncaught Python traceback

#### Scenario: Keyboard interrupt is normalized
- **WHEN** installed `isomer-cli` receives a keyboard interrupt during command execution
- **THEN** the process exits with interrupted status and prints a concise interruption diagnostic without a Python traceback

### Requirement: Invocation Errors Include Expected Command Shape
The system SHALL include actionable invocation guidance when a command is invoked in the wrong format.

#### Scenario: Missing argument reports usage and examples
- **WHEN** a caller runs `isomer-cli project paths get` without the required semantic label
- **THEN** the diagnostic identifies the missing argument, reports the expected command shape, and includes one to three valid `project paths get` examples

#### Scenario: Unknown subcommand reports nearby examples
- **WHEN** a caller runs an unknown subcommand under a known group such as `isomer-cli project paths gte`
- **THEN** the diagnostic identifies the unknown command and includes one to three examples for the nearest known command group or command path

#### Scenario: Invalid option reports corrected shape
- **WHEN** a caller passes an option that is not accepted by the selected command
- **THEN** the diagnostic names the invalid option, reports the expected command shape when available, and includes one to three valid examples for that command path

### Requirement: Structured Remediation Fields
The system SHALL expose remediation guidance as structured diagnostic fields instead of embedding all guidance in freeform messages.

#### Scenario: JSON diagnostic includes remediation fields
- **WHEN** a normalized failure is emitted in JSON mode and remediation guidance is available
- **THEN** each relevant diagnostic can include `hint`, `usage`, and `examples` fields in addition to `code`, `severity`, `concept`, `message`, `path`, `field`, and `line`

#### Scenario: Text diagnostic renders remediation fields
- **WHEN** a normalized failure is emitted in text mode and remediation guidance is available
- **THEN** the text output prints the primary diagnostic line followed by the hint, expected usage, and examples in a stable order

#### Scenario: Existing diagnostics remain compatible
- **WHEN** a command emits an existing diagnostic that has no remediation fields
- **THEN** JSON and text output preserve the existing diagnostic fields and do not require callers to handle new fields

### Requirement: JSON Failure Output Contract
The system SHALL preserve the `isomer-cli-output.v1` wrapper for normalized failures when root-level `--print-json` is requested.

#### Scenario: Pre-dispatch failure honors print-json
- **WHEN** a caller runs `isomer-cli --print-json project paths get` without a required argument
- **THEN** the output is valid JSON using the `isomer-cli-output.v1` wrapper and includes `ok: false`, the best-known command path, diagnostics, and mutation information

#### Scenario: Unknown command honors print-json
- **WHEN** a caller runs `isomer-cli --print-json project unknown-command`
- **THEN** the output is valid JSON using the `isomer-cli-output.v1` wrapper instead of Click's text error output

#### Scenario: Text mode remains text
- **WHEN** a caller runs a malformed command without root-level `--print-json`
- **THEN** the output is human-readable text and does not include the `isomer-cli-output.v1` JSON wrapper

### Requirement: Mutation Certainty Reporting
The system SHALL report mutation certainty for normalized failures so agents can decide whether follow-up inspection is needed.

#### Scenario: Invocation failure is non-mutating
- **WHEN** a command fails before command handler execution because of malformed invocation
- **THEN** the failure output reports `mutated: false`

#### Scenario: Internal exception after dispatch has unknown mutation state
- **WHEN** an unexpected exception is caught after command dispatch and the entrypoint cannot prove that no mutation occurred
- **THEN** the failure output reports `mutation_state: "unknown"` or an equivalent explicit unknown state instead of claiming `mutated: false`

#### Scenario: Domain handler failures keep known mutation fields
- **WHEN** a command handler returns a domain validation failure through the normal output path
- **THEN** the response preserves the handler's known `mutated` value and diagnostics

### Requirement: Traceback Debug Escape Hatch
The system SHALL suppress raw Python tracebacks by default and SHALL expose them only through explicit debug mode.

#### Scenario: Traceback suppressed by default
- **WHEN** a command raises an unexpected Python exception without debug mode enabled
- **THEN** the output contains a concise internal-error diagnostic and does not contain a Python traceback

#### Scenario: Debug mode includes traceback
- **WHEN** a command raises an unexpected Python exception with root-level debug mode or `ISOMER_CLI_DEBUG=1` enabled
- **THEN** the output includes the structured diagnostic and also includes traceback details in a debug-only section

#### Scenario: Debug details are isolated in JSON
- **WHEN** debug mode is enabled and the caller also requests `--print-json`
- **THEN** traceback details are placed under a dedicated debug field rather than inside the primary diagnostic message

### Requirement: Command Example Registry
The system SHALL provide a maintainable source for command examples used by invocation-error diagnostics.

#### Scenario: Nearest command examples are selected
- **WHEN** a wrong-format invocation can be associated with a known public command path
- **THEN** the diagnostic examples come from that command path's registered examples and include no more than three examples

#### Scenario: Group fallback examples are selected
- **WHEN** a wrong-format invocation can only be associated with a command group
- **THEN** the diagnostic examples come from that group or from representative child commands rather than from an unrelated top-level command

#### Scenario: Docs and registry stay aligned
- **WHEN** documented public command examples change
- **THEN** validation or tests detect stale high-value invocation examples used by normalized error diagnostics
