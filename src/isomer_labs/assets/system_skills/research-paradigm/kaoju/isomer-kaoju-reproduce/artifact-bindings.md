# Reproduce Artifact Bindings

Read `../isomer-kaoju-shared/references/artifact-semantics.md` for meaning. This page is the physical and API authority for the rows below. Large inputs and raw outputs remain referenced files or external material.

| Semantic id | Storage item | Record kind | Semantic label | Neutral profile | Producer | Consumers | Payload role | Lineage policy | Revision policy | Query metadata |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `kaoju:generated-dataset` | Managed JSON snapshot plus file refs | `artifact` | `topic.records.artifacts` | `isomer:research/record-format/profile/kaoju/material/generated-dataset/v1` | isomer-kaoju-reproduce | reproduce, compare, audit | Generator contract and output identity | `derived_from` generator inputs and Proceed Decision | Separate per generated identity | source, checks, output file refs |
| `kaoju:method-trial` | Managed JSON snapshot | `artifact` | `topic.records.artifacts` | `isomer:research/record-format/profile/kaoju/run/method-trial/v1` | isomer-kaoju-reproduce | audit, synthesize | Trial contract and interpreted attempts | `derived_from` source digests, dataset, decision, and Runs | Separate trial; follow-up descendants | metrics, evidence verdict, procedure |
| `kaoju:method-trial-run` | Managed JSON snapshot plus raw-output refs | `run` | `topic.records.runs` | `isomer:research/record-format/profile/kaoju/run/method-trial-run/v1` | isomer-kaoju-reproduce | method trial, compare, audit | One first-hand attempt | `derived_from` exact code, input, evaluator, environment, and decision | Never revise fidelity; separate faithful, adapted, repaired, failed, blocked, and probe Runs | metrics, purpose, terminal status, output files |

## Normal Create

```text
isomer-cli --print-json ext research records create --topic <topic> --record-kind <row-record-kind> --semantic-label <row-semantic-label> --semantic-id <row-semantic-id> --format-profile <row-neutral-profile> --skill isomer-kaoju-reproduce --producer 'isomer-kaoju-reproduce' --consumer '<row-consumers>' --payload-file <payload-file> --metadata-json '{"actor_metadata":"<resolved>","procedure":"method-trial"}' --files-json '<raw-output-and-material-refs>'
```

## Lifecycle

Validate payload-first, create with **Normal Create**, list by exact family and semantic id with optional `--latest-only`, and show with payload. Use metadata-only `records update` for lifecycle status; content-changing corrections create follow-up children. Every faithful, adapted, repaired, failed, blocked, or generated-input attempt is a separate Run with immediate parents and `derived_from` lineage. Render on demand, export explicitly with `--output-file`, and archive without deleting referenced inputs or outputs.
