# Placeholder Binding Index

## Workflow

1. Discover the selected v2 skill set from the user's requested route, prepared Topic Actor start packs, Topic Team Profile skill bindings, or operator-provided skill list.
2. For each selected skill, locate the skill-local `placeholder-bindings.md` file and verify that it has command guidance for `isomer-cli ext research records`.
3. Build a topic-level index that lists the skill name, binding file path or skill ref, placeholder groups, default semantic labels, profiles, and whether Topic Actor or formal agent metadata should be supplied when records are created.
4. Treat the topic-level index as navigation and readiness evidence only. When an index row conflicts with a skill-local binding page, the skill-local `placeholder-bindings.md` file wins.
5. Store or update the index through the workspace manager placeholder binding row when a durable record is needed, and include the index ref in Topic Actor start packs and formal agent bootstrap material.
6. Report blockers for missing binding pages, missing command guidance, or missing semantic labels. Do not write accepted artifacts to local scratch as a fallback.

If the user's task does not map cleanly to these steps, build a partial index for the selected skills and mark unchecked skills as blockers or deferrals.

## Minimum Index Columns

| Field | Meaning |
| --- | --- |
| skill | V2 skill that owns the binding page. |
| binding page | Skill-local `placeholder-bindings.md` path or installed skill ref. |
| placeholder groups | Placeholder tokens or grouped placeholder kinds covered by the page. |
| default labels | Semantic labels used by the binding rows. |
| profiles | Record profiles used by the binding rows. |
| actor metadata | Whether `--topic-actor`, `--actor-kind`, `--runtime-kind`, `--controller-kind`, or formal agent metadata should be supplied. |
| status | Available, missing, stale, partial, or blocked. |
| note | Caveat or repair route. |

## Authority Rule

Skill-local `placeholder-bindings.md` files are the authority for command shape, record kind, semantic label, profile, producer, and consumer. The topic-level index helps agents find the right page and proves bootstrap checked the selected skill set; it must not become a second source of truth.
