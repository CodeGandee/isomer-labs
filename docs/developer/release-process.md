# Release Process

Isomer Labs is published as the `isomer-labs` Python package. Releases should publish to PyPI through trusted publishing and publish the MkDocs site to GitHub Pages from the same release workflow.

Before a release, run:

```bash
pixi run lint
pixi run typecheck
pixi run test
pixi run docs-validate
```

The PyPI long description comes from `README.md`. Keep the README public-facing, installable with `uv tool install isomer-labs`, and free of source-checkout-only setup as the main path.

Use source-checkout commands only in developer sections. If trusted publishing is configured for the repository and workflow, no PyPI token should be committed or passed to CI.
