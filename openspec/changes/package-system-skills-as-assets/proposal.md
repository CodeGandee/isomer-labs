## Why

Isomer's production agent skills are currently rooted at repository-level `skillset/`, but they are intended to ship with the Python distribution. Moving non-development skills into package assets lets installed PyPI builds expose the same built-in skill catalog without depending on a source checkout.

## What Changes

- Move the distributable skillset content, excluding `skillset/dev/`, under `src/isomer_labs/assets/system_skills/`.
- Keep a repo-root `skillset/` authoring view for existing validators, docs, and developer workflows, with `dev/` remaining repo-local.
- Add package-resource helpers for locating, reading, and materializing packaged system skills.
- Ensure packaging and tests include non-Python skill assets such as Markdown, YAML, JSON, Python helper scripts, and LaTeX paper templates.
- Preserve `skillset/manifest.toml` group semantics so install/deploy code uses explicit manifest entries rather than blindly installing every directory.

## Capabilities

### New Capabilities

- `packaged-system-skills`: Built-in Isomer system skills are distributed as package resources, queryable from installed packages, and materializable without a repository checkout.

### Modified Capabilities

- `isomer-python-module-architecture`: Permit package-owned `assets/system_skills` resources while continuing to reject runtime dependencies on repository-root `skillset/`.

## Impact

- Affected code: package assets, skillset authoring layout, package-resource helpers, packaging metadata, and architecture tests.
- Affected tests: source architecture tests, package asset smoke tests, and skillset validators that currently assume a physical repo-root `skillset/` tree.
- Runtime behavior: installed packages can locate and materialize official system skills without access to repository-local files.
- No new runtime dependencies are expected.
