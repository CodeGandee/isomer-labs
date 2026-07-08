## 1. Installer Core

- [x] 1.1 Add a package-owned system skill projection module with target resolution, selection resolution, copy or symlink projection, ownership markers, status discovery, and uninstall helpers.
- [x] 1.2 Add unit tests for target defaults, selector resolution, flat projection, ownership metadata, collision refusal, status, and uninstall preservation of unmanaged directories.

## 2. CLI Surface

- [x] 2.1 Add top-level `isomer-cli system-skills` commands for `list`, `status`, `install`, and `uninstall`.
- [x] 2.2 Add CLI tests for help output, JSON list output, install into a temporary skill root, status output, uninstall output, `--target all`, and rejected `--home` with `all`.

## 3. Documentation and Release Prep

- [x] 3.1 Update README and docs to recommend `isomer-cli system-skills install` for released system skill installation and document supported targets.
- [x] 3.2 Update CLI reference and docs validation expectations so the new commands are covered.
- [x] 3.3 Bump the package patch version for the next release because `v0.1.0` already exists.

## 4. Validation and Publishing

- [x] 4.1 Run focused unit tests, full unit tests, lint, docs validation, package build, and MkDocs strict build.
- [x] 4.2 Commit and push all changes to `main`.
- [ ] 4.3 Create a new GitHub release and verify the release workflow starts or completes the PyPI and GitHub Pages publishing jobs.
