# Topic Config Owns Environment Intent

Isomer Labs previously planned to store each Research Topic's intended Pixi environment strategy and Pixi environment ref in its Research Topic Config. ADR 0025 supersedes this decision: the Project Manifest now owns explicit Research Topic to Pixi environment bindings.

## Status

superseded by ADR-0025

## Considered Options

- Store topic environment mapping in each Research Topic Config.
- Store topic environment mapping directly in the Project Manifest.
- Store topic environment mapping only in Workspace Runtime.
- Add a separate `.isomer-labs/environments.toml` mapping file.

## Consequences

- Do not add Pixi environment intent fields to Research Topic Config under this decision.
- Preserve this ADR only as historical context for why environment intent briefly appeared in the Milestone 4 design.
