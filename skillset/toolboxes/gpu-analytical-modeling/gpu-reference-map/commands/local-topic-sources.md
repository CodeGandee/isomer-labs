# Local Topic Sources

## Workflow

When local topic context may contain the needed source, execute the following steps in order.

1. **Read topic intent first**. Check the current Research Topic intent, evaluation contract, success criteria, and scope before broad search.
2. **Read durable records**. Prefer recorded decisions, previous analyses, accepted assumptions, experiment notes, and closure records over chat memory.
3. **Inspect local work products**. Review local model code, benchmark scripts, generated configurations, measured outputs, and prior plots or tables when they define current scope.
4. **Extract source boundaries**. State what the local source can justify, such as current target scope, metric definition, accepted split, known measurement, or recorded limitation.
5. **Name missing provenance**. If a local record lacks enough detail to justify a parameter, path, or evidence claim, mark the gap and route to the relevant source family.

If the user's task does not map cleanly to these steps, use your native planning tool to build a local-topic source plan from the topic intent, records, local artifacts, and missing claim, then execute the plan.

## Can Justify

- Current research scope, target claim, evaluation metric, accepted assumptions, and local decision history.
- Local implementation choices, scripts, run outputs, measured artifacts, and known limitations when the record includes enough provenance.

## Cannot Justify

- Vendor hardware facts, target-hardware behavior, or general GPU architecture claims unless the local record cites or preserves the source.
- Real-hardware accuracy claims when local output is synthetic, simulated, emulator-only, or derivation-only evidence.

## Preserve

- Topic id or local record id, artifact name, timestamp when available, input shapes, precision, kernel variant, hardware scope, command or script, and any caveat recorded with the source.
