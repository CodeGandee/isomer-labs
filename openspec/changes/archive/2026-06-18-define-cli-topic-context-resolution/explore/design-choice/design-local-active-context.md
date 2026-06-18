# Local Active Context

The accepted first-version design standardizes `.isomer-labs/local.toml` as the Project-local active context file for `isomer-cli`.

## Accepted Choice

Option A: `isomer-cli` may read untracked `.isomer-labs/local.toml` as a low-precedence convenience source for active topic-context identity refs. Explicit CLI selectors, current directory inside a registered Topic Workspace, and supported topic-context environment variables take precedence. The Project Manifest default Research Topic remains the final fallback.

## Rationale

The CLI is system-level, but topic selection is Project-scoped. A project-local active context gives interactive use a stable current Research Topic without putting user-local preference in the shared Project Manifest or in a global machine-level file.

## Consequences

- `.isomer-labs/local.toml` is untracked by default and is not shared project truth.
- The file can carry only candidate active Research Topic, Topic Workspace, Research Inquiry, Research Task, and Run identity refs plus schema version.
- The file must not contain Workspace Runtime state, command outputs, live process ids, research records, or secrets.
- Every value from the file must validate against the Project Manifest, Research Topic Config, and Workspace Runtime before use.

## Rejected Alternatives

- No local active context in v1. This keeps the CLI simpler but makes interactive topic-scoped commands depend on repeated flags or cwd.
- Store active topic in the Project Manifest. This makes user-local preference look like shared project truth.
