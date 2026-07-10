# Pipeline Artifact Bindings

Read `../isomer-kaoju-shared/references/artifact-semantics.md` for meaning. This page is the physical and API authority for the row below.

| Semantic id | Storage item | Record kind | Semantic label | Neutral profile | Producer | Consumers | Payload role | Lineage policy | Revision policy | Query metadata |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `kaoju:survey-terminal-report` | Managed JSON snapshot | `view_manifest` | `topic.records.views` | `isomer:research/record-format/profile/kaoju/control/survey-terminal-report/v1` | isomer-kaoju-pipeline | user and resumed procedures | Terminal state of one bounded invocation | `derived_from` stage outputs, decisions, blockers, and audit | Separate report per invocation | procedure, terminal status, accepted outputs |

## Normal Create

```text
isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --semantic-label topic.records.views --semantic-id kaoju:survey-terminal-report --format-profile isomer:research/record-format/profile/kaoju/control/survey-terminal-report/v1 --skill isomer-kaoju-pipeline --producer 'isomer-kaoju-pipeline' --consumer 'user and resumed procedures' --payload-file <payload-file> --metadata-json '{"actor_metadata":"<resolved>","procedure":"<procedure>","terminal_status":"<complete-paused-blocked>"}' --parents-json '<stage-output-refs>' --lineage-kind derived_from
```

## Lifecycle

Validate with the same selectors, then create one terminal report. List with exact family, semantic id, procedure, and optional latest filter; show with payload; use update only for lifecycle metadata. A resumed or repeated procedure creates a new follow-up descendant terminal report. Render on demand, export explicitly, and archive through generic record operations.
