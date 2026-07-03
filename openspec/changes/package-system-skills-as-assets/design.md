## Context

The repository already has `src/isomer_labs/assets/system_skills/`, but it is only a placeholder. The real production skills live under repository-root `skillset/`, while `src/isomer_labs` is being prepared for PyPI publishing and must not depend on repository-only directories at runtime. The distributable skillset is mostly static Markdown/YAML/JSON/Python/LaTeX material, about 6 MB excluding `skillset/dev/`, and `skillset/manifest.toml` already identifies the installable groups.

The current development workflow and validators expect a repo-root `skillset/` path. That path is useful as an authoring view, but it should no longer be the runtime source of truth for installed packages.

## Goals / Non-Goals

**Goals:**

- Make `src/isomer_labs/assets/system_skills/` the authoritative packaged copy for all non-development skills.
- Keep `skillset/dev/` outside the Python distribution and outside packaged system-skill discovery.
- Preserve a repo-root `skillset/` authoring view so current validators and documentation do not need an immediate large rewrite.
- Add package-resource APIs that can list manifest groups and materialize packaged skills without a source checkout.
- Add tests that prove manifest-listed skills resolve under package assets and `dev/` is excluded.

**Non-Goals:**

- Do not redesign skill content, naming, or group membership.
- Do not add a new agent-skill installation CLI surface in this change.
- Do not make development-only skills installable.
- Do not change Houmao system-skill discovery.

## Decisions

### Store distributable skills under `isomer_labs.assets.system_skills`

Use this layout:

```text
src/isomer_labs/assets/system_skills/
  README.md
  manifest.toml
  misc/
  operator/
  research-paradigm/
  service/
```

This keeps shipped skill material inside the package boundary and allows `importlib.resources.files("isomer_labs")` to locate it from editable installs and wheels. The alternative, keeping runtime code pointed at repository-root `skillset/`, conflicts with the PyPI boundary and fails outside source checkouts.

### Keep repo-root `skillset/` as an authoring view

After moving non-development content into package assets, keep `skillset/dev/` as a normal repo-local directory and represent the distributable entries from `skillset/` as links to `src/isomer_labs/assets/system_skills/`. This avoids duplicating 6 MB of skill material and preserves existing validator paths such as `skillset/operator/...`.

The authoring view is not a runtime API. Runtime code must use the package-resource helper instead of deriving a repository root.

### Add a narrow package-resource helper module

Add `isomer_labs.skills.system_assets` for package-owned system-skill resources. It should provide:

- a root accessor for `assets/system_skills`;
- manifest loading and group iteration;
- manifest-listed skill resolution with path traversal protection;
- optional materialization by copying a selected group or all manifest-listed groups to a filesystem target.

Use `importlib.resources` rather than `Path(__file__)` so the same API works in installed packages.

### Let `manifest.toml` define installability

Package assets may include provenance, licenses, `ds-analysis`, and `org/` source material, but installation/deployment code should follow `manifest.toml`. This keeps packaged support material available for audit while preventing accidental installation of directories not listed in groups.

### Keep architecture checks strict

The architecture tests should continue to reject source runtime references to repository-root `skillset/`. They should separately allow package-resource paths such as `assets/system_skills` because those are installed assets, not checkout-local directories.

## Risks / Trade-offs

- Symlink portability in developer checkouts → Use simple relative links at the top level only, keep the packaged source as ordinary files, and have tests validate both the authoring view and packaged root.
- Hatchling asset inclusion surprises → Add a wheel or installed-resource smoke test that reads representative files from `assets/system_skills`.
- Large wheel size growth → Accept the current size because these skills are part of the product; use the manifest to avoid installing non-listed support directories.
- Package-resource materialization could overwrite user files → Materialization should require an empty target or explicit replacement in any future CLI wrapper; the helper can default to non-destructive copying.

## Migration Plan

1. Move `skillset/README.md`, `skillset/manifest.toml`, and non-`dev` skill subtrees under `src/isomer_labs/assets/system_skills/`.
2. Recreate the repo-root `skillset/` authoring view with relative symlinks for distributable entries and the original `dev/` directory left in place.
3. Add `isomer_labs.skills.system_assets` and focused tests for manifest loading, path resolution, `dev/` exclusion, and materialization.
4. Update architecture tests so package assets are allowed but runtime repository-root `skillset/` dependencies remain forbidden.
5. Validate with lint, typecheck, unit tests, and OpenSpec status.

Rollback is direct: remove the helper module, move the packaged asset tree back to `skillset/`, restore `.gitkeep`, and remove the symlink authoring view.

## Open Questions

- Should a later change expose `isomer-cli system-skills list/materialize`, or should installation stay delegated to Houmao and external agent installers for now?
- Should provenance-only directories under `research-paradigm/` stay packaged indefinitely, or move into documentation assets after the first PyPI release?
