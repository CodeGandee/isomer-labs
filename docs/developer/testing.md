# Testing

Use Pixi from the repository root for local validation:

```bash
pixi run lint
pixi run typecheck
pixi run test
pixi run docs-validate
```

Unit tests live in `tests/unit/`, integration tests in `tests/integration/`, and manual checks in `tests/manual/`. Keep tests deterministic unless they explicitly validate a service or filesystem workflow.

Documentation validation checks required pages, CLI coverage, canonical language, stale JSON flags, semantic path documentation, and selected README links. Update `scripts/validate_docs.py` whenever docs move.
