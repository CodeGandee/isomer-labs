# Audit Artifact Bindings

Read `../isomer-kaoju-shared/references/artifact-semantics.md` for meaning. This page is the physical and API authority for the row below.

| Semantic id | Storage item | Record kind | Semantic label | Neutral profile | Producer | Consumers | Payload role | Lineage policy | Revision policy | Query metadata |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `kaoju:audit-report` | Managed JSON snapshot | `artifact` | `topic.records.artifacts` | `isomer:research/record-format/profile/kaoju/report/audit-report/v1` | isomer-kaoju-audit | pipeline, synthesize, user | Non-mutating evidence-readiness assessment | `derived_from` exact audited versions, evidence, decisions, and Runs | Separate report per audit boundary | claims, verdicts, readiness status, defects |

## Normal Create

```text
isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --semantic-id kaoju:audit-report --format-profile isomer:research/record-format/profile/kaoju/report/audit-report/v1 --skill isomer-kaoju-audit --producer 'isomer-kaoju-audit' --consumer 'pipeline, synthesize, user' --payload-file <payload-file> --metadata-json '{"actor_metadata":"<resolved>","procedure":"audit"}' --parents-json '<audited-record-refs>' --lineage-kind derived_from
```

## Lifecycle

Validate with the same selectors, then create. List by `--artifact-family kaoju --semantic-id kaoju:audit-report`; show with `--include-payload`; use update only for lifecycle metadata. A re-audit is a separate follow-up child, not a revision that hides the earlier verdict. Render on demand, export explicitly, and archive through generic record operations.
