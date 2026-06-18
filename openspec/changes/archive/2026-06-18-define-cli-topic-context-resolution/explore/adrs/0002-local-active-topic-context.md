# Local Active Topic Context

`isomer-cli` will support untracked `.isomer-labs/local.toml` as a Project-local convenience file for active topic-context identity refs. The file is lower precedence than explicit CLI selectors, current directory selection, and supported topic-context environment variables, and it is higher precedence than the Project Manifest default Research Topic.

## Status

accepted

## Considered Options

- Standardize `.isomer-labs/local.toml` as untracked local active context.
- Omit local active context from the first version.
- Store active topic selection in the Project Manifest.

## Consequences

Interactive topic-scoped commands can have a Project-local current topic without making the preference shared project truth. Values from `.isomer-labs/local.toml` are candidate identity refs only; they must validate before use and cannot carry Workspace Runtime state, research records, command outputs, process ids, or secrets.
