# Project Manifest Owns Topic Pixi Environment Bindings

Isomer Labs will record which Pixi environment or environments each Research Topic uses in the Project Manifest rather than inferring the relationship from Pixi environment names or storing the binding in Research Topic Config. The Project Manifest will use repeated `[[topic_pixi_environment_bindings]]` tables with `research_topic_id`, `pixi_environment`, optional `purpose`, and optional `status`, so one Research Topic can bind to multiple Project-root Pixi environments. Specialized names such as `<topic-slug>-<env-purpose>` are allowed as human convention but never treated as authoritative binding semantics.

## Status

accepted

## Considered Options

- Store Pixi environment intent in Research Topic Config.
- Infer topic Pixi environments from Research Topic ids or environment names.
- Store explicit Research Topic to Pixi environment bindings in repeated Project Manifest tables.

## Consequences

- `isomer-cli doctor` must validate explicit Project Manifest bindings against the Project-level Pixi manifest and must not infer topic-to-environment relationships from names.
- Research Topic Config remains a topic defaults and refs surface, not the owner of Project-level environment policy.
- Workspace Runtime records resolved environment readiness, selected environment use, and preparation provenance after a mutating preparation step.
- Validation should reject or warn on bindings that reference unknown Research Topic ids, missing Pixi environments, duplicate active topic/environment pairs, malformed purpose labels, or unsupported status values.
- Standalone Pixi isolation uses a separate `topic_standalone_pixi_bindings` table, as recorded by ADR 0026.
