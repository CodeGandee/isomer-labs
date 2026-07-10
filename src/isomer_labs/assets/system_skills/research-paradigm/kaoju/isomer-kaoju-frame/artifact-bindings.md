# Frame Artifact Bindings

Read `../isomer-kaoju-shared/references/artifact-semantics.md` for meaning. This page is the physical and API authority for the rows below.

| Semantic id | Storage item | Record kind | Semantic label | Neutral profile | Producer | Consumers | Payload role | Lineage policy | Revision policy | Query metadata |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `kaoju:survey-contract` | Managed JSON snapshot | `artifact` | `topic.records.artifacts` | `isomer:research/record-format/profile/kaoju/contract/survey-contract/v1` | isomer-kaoju-frame | discover, acquire, examine, compare, audit, synthesize | Accepted survey boundary | `derived_from` user intent and prior contract when revised | Revise boundary changes | procedure, scope status, Gate refs |
| `kaoju:comparison-intent` | Managed JSON snapshot | `artifact` | `topic.records.artifacts` | `isomer:research/record-format/profile/kaoju/contract/comparison-intent/v1` | isomer-kaoju-frame | reproduce, compare, audit | User-reviewable comparison plan | `derived_from` candidates, survey contract, reusable Runs | Revise during clarification; preserve approved version | methods, metrics, procedure, unresolved decisions |
| `kaoju:proceed-decision` | Managed JSON snapshot | `decision_record` | `topic.records.artifacts` | `isomer:research/record-format/profile/kaoju/decision/proceed-decision/v1` | isomer-kaoju-frame | pipeline and empirical stages | Explicit route decision | `derived_from` exact intent version | Separate decision event | decision status, procedure, actor |

## Normal Create

```text
isomer-cli --print-json ext research records create --topic <topic> --record-kind <row-record-kind> --semantic-label <row-semantic-label> --semantic-id <row-semantic-id> --format-profile <row-neutral-profile> --skill isomer-kaoju-frame --producer 'isomer-kaoju-frame' --consumer '<row-consumers>' --payload-file <payload-file> --metadata-json '{"actor_metadata":"<resolved>","procedure":"<procedure>"}'
```

## Lifecycle

Validate with `records validate` using the row's complete create selectors, then create with **Normal Create**. List with `records query list --artifact-family kaoju --semantic-id <id> --latest-only`; show with `records show <record-id> --include-payload`; metadata-only changes use `records update <record-id> --record-kind <kind> --semantic-id <id>`. Revise contracts with `records revise <record-id> --semantic-id <id> --payload-file <payload-file>`; create Decisions and other follow-ups separately with `--parents-json` and `--lineage-kind derived_from`. Render with `records render <record-id>`; export with `records render <record-id> --output-file <export-path>`; archive with `records delete <record-id> --reason <reason>`.
