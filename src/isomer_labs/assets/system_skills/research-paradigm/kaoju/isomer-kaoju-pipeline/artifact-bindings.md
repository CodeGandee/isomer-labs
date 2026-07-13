# Pipeline Artifact Bindings

Read `../isomer-kaoju-shared/references/artifact-semantics.md` for meaning. This page is the physical and API authority for the row below.

| Semantic id | Storage item | Record kind | Semantic label | Neutral profile | Producer | Consumers | Payload role | Lineage policy | Revision policy | Query metadata |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `kaoju:survey-terminal-report` | Managed JSON snapshot | `view_manifest` | `topic.records.views` | `isomer:research/record-format/profile/kaoju/control/survey-terminal-report/v1` | isomer-kaoju-pipeline | user and resumed procedures | Terminal state of one bounded invocation | `derived_from` stage outputs, decisions, blockers, and audit | Separate report per invocation | procedure, terminal status, accepted outputs |
| `kaoju:writing-template` | Managed JSON snapshot | `artifact` | `topic.records.artifacts` | `isomer:research/record-format/profile/kaoju/control/writing-template/v1` | isomer-kaoju-pipeline | isomer-kaoju-pipeline, isomer-kaoju-write | Editable LaTeX template and preview | `derived_from` venue, paper type, and generation | Revise current template; refresh creates descendant | template_name, venue, paper_type, status |

## Normal Create

```text
isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --semantic-label topic.records.views --semantic-id kaoju:survey-terminal-report --format-profile isomer:research/record-format/profile/kaoju/control/survey-terminal-report/v1 --skill isomer-kaoju-pipeline --producer 'isomer-kaoju-pipeline' --consumer 'user and resumed procedures' --payload-file <payload-file> --metadata-json '{"actor_metadata":"<resolved>","procedure":"<procedure>","terminal_status":"<complete-paused-blocked>"}' --parents-json '<stage-output-refs>' --lineage-kind derived_from
```

```text
isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --semantic-id kaoju:writing-template --format-profile isomer:research/record-format/profile/kaoju/control/writing-template/v1 --skill isomer-kaoju-pipeline --producer 'isomer-kaoju-pipeline' --consumer 'isomer-kaoju-pipeline, isomer-kaoju-write' --payload-file <payload-file> --metadata-json '{"actor_metadata":"<resolved>","template_name":"<name>","venue":"<venue>","paper_type":"<type>"}' --parents-json '<from-record-if-any>' --lineage-kind derived_from
```

## Lifecycle

Validate with the same selectors, then create one terminal report. List with exact family, semantic id, procedure, and optional latest filter; show with payload; use update only for lifecycle metadata. A resumed or repeated procedure creates a new follow-up descendant terminal report. Render on demand, export explicitly, and archive through generic record operations.
