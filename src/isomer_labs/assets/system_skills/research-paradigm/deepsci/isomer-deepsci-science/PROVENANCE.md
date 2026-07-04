# Science Skill Provenance

The `science` skill integrates package-routing ideas from FermiLink without
making FermiLink part of the Isomer runtime.

## Upstream Sources

- FermiLink repository: https://github.com/TaoELi/FermiLink
- Audited commit: `93f089a333a43089fb1a08a73c37d05fd6683214`
- Catalog source: `src/fermilink/data/curated_channels/skilled-scipkg.json`

## What Is Included

- Isomer-native generated package cards under `references/packages/`.
- Compact package index under `references/package-index.min.json`.
- A domain index for progressive disclosure.
- Package ids, descriptions, tags, knowledge URLs, source archive URLs, and
  upstream project URLs needed for routing.

## What Is Not Included

- FermiLink runner, CLI, FastAPI backend, Chainlit UI, HPC profile manager, or
  source implementation.
- Package source trees from `github.com/skilled-scipkg/*`.
- Scientific solver runtimes or compiled executables.
- A guarantee that any package can run in the user's environment.

## Isomer Runtime Boundary

Isomer uses the Isomer Execution Adapter for all execution and
a science evidence record for durable science evidence records. The package cards
are routing and knowledge pointers only.

If a Research Topic downloads a package knowledge base or scientific package source from
an upstream URL, that Research Topic should preserve the source URL and license context
in its own evidence files or artifact records.

## Regeneration

The generated catalog can be refreshed from a local FermiLink checkout with:

```bash
python scripts/generate_science_skill_catalog.py
```
