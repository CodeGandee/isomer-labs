## Why

Isomer Labs is now published on PyPI, but the README and public docs still present a repo-checkout, Pixi-first path that is confusing for users installing the tool. The docs need a clearer information architecture for public users, operators, and contributors, and the README should explain the published CLI plus system-skill installation path.

## What Changes

- Reclassify and rewrite the existing `docs/` pages into audience-oriented sections: `tutorial/`, `manual/`, and `developer/`, while keeping GUI contract pages under a stable UI contract location.
- Examine each current docs page before moving it, and rewrite it for the right tone: tutorial pages teach a sequence, manual pages support lookup, and developer pages explain implementation and maintenance.
- Rewrite `README.md` as a public tool entrypoint with installation through `uv tool install isomer-labs`, quick Project setup, Project Web launch, and links to the reorganized docs.
- Add public system-skill installation guidance that recommends `npx skills add` for agent surfaces and explains core versus DeepSci extension skills.
- Update `mkdocs.yml` navigation so GitHub Pages exposes the new documentation structure.
- Update documentation validation scripts and tests so required pages, README links, CLI coverage, stale JSON checks, semantic path checks, and required command examples follow the new locations.
- Preserve developer setup through Pixi in developer docs rather than making Pixi the public user install path.

## Capabilities

### New Capabilities
- `public-documentation-information-architecture`: Covers the published-user README, audience-oriented docs layout, MkDocs navigation, and docs validation expectations.

### Modified Capabilities
- `isomer-documentation-system-guide`: Updates documentation requirements from the current flat docs layout to the new tutorial/manual/developer layout and published-install posture.
- `packaged-system-skills`: Adds documentation requirements for public `npx skills add` installation guidance for packaged system skills.

## Impact

- Affected docs: `README.md`, `mkdocs.yml`, every existing `docs/*.md`, `docs/ui/contracts/*.md`, and new `docs/{tutorial,manual,developer}/` pages.
- Affected validation: `scripts/validate_docs.py`, `tests/unit/test_validate_docs.py`, and any hardcoded docs paths in tests or scripts.
- Affected release quality: future PyPI/GitHub Pages releases should present installable package metadata, public user docs, and agent skill install guidance consistently.
