# Install to uv

## Overview

Install the current Isomer Labs checkout into uv's user tool directory in editable mode. Give the installed distribution a PEP 440 local version tied to the current Git commit while restoring the checkout's release or release-candidate version immediately after the build.

## Workflow

1. **Resolve and inspect the checkout**.
   - Use the explicit checkout path, or find the repository root from the current directory.
   - Confirm `pyproject.toml` declares project name `isomer-labs` and the `isomer-cli` script.
   - Require `uv`, a readable Git `HEAD`, and a single unambiguous static project version.
   - Capture `git status --porcelain=v1`, the exact original version value, `uv --version`, `uv tool list`, and the current `isomer-cli` executable when present.
   - Do not require a clean checkout, but stop when the version field has merge conflicts or cannot be restored with a targeted inverse edit.
2. **Derive the local build version**.
   - Parse the original value as PEP 440 and preserve its public release form, including any release-candidate, development, or post-release segment.
   - Read the lowercase short commit with `git rev-parse --short=7 HEAD`.
   - Form `<public-version>+local.<short-commit>` for a clean preflight checkout or `<public-version>+local.<short-commit>.dirty` when unrelated changes already exist.
   - Validate the result as PEP 440 before editing any file.
3. **Temporarily stamp project metadata**.
   - Replace only the `[project]` version value with the derived local version using the available targeted file-editing mechanism.
   - Confirm the edit did not alter other `pyproject.toml` content or overwrite pre-existing changes.
   - Never commit the temporary local version.
4. **Install the editable user tool**.
   - From the checkout root, run `uv tool install --editable . --force`.
   - Use uv's default user tool and executable directories. Do not add `sudo`, a system environment, or a second package installer.
   - Capture the complete command result and installed distribution version.
5. **Restore source metadata in all outcomes**.
   - Immediately restore the exact original project version, whether installation succeeded, failed, or was interrupted after the temporary edit.
   - Use the targeted inverse edit. Never use `git reset`, `git checkout`, or another whole-file restoration that could discard user work.
   - Confirm `pyproject.toml` contains the original version before running installation verification.
6. **Verify the installation**.
   - Run `uv tool list`, `command -v isomer-cli`, `isomer-cli --version`, and an `isomer-cli --help` smoke check.
   - Resolve the uv tool directory with `uv tool dir`. Inspect the `isomer-labs/uv-receipt.toml` requirement and require `editable = "<absolute-checkout-path>"`.
   - Inspect the installed distribution's `direct_url.json` and require the same checkout URL with `"editable": true`; confirm its editable `.pth` points at `<checkout>/src`.
   - Require `isomer-cli --version` to report the derived local build version.
7. **Verify worktree preservation and report**.
   - Compare final `git status --porcelain=v1` with the captured preflight state. The temporary version edit must leave no residual source change.
   - Do not remove, rewrite, stage, or commit unrelated files to make the comparison pass.
   - Report the installation outcome, local version, editable source, executable and uv tool paths, receipt and direct-URL editability evidence, smoke check, and worktree preservation in natural language.

If the checkout or uv layout differs from these expectations, use the native planning tool for a bounded diagnostic pass, preserve the restoration guarantee, and report the unsupported condition instead of guessing a destructive repair.

## Failure Handling

- Restore the original version before reporting any build, resolution, installation, or verification failure.
- If uv cannot resolve dependencies, report its command output and leave any pre-existing tool installation untouched when uv does so atomically; do not claim rollback without verifying it.
- If the installed version is correct but editable evidence is missing, report verification failure and include the receipt and `direct_url.json` paths examined.
- If final worktree state differs, identify only the paths changed by this procedure and repair those targeted changes. Preserve all preflight differences.

## Output Contract

Return a concise natural-language result. State whether installation succeeded, give the actual commit-stamped local version, editable source path, and executable path, then summarize the uv receipt, `direct_url.json`, smoke-check, and worktree-preservation evidence. Use the actual release or release-candidate version, commit, paths, and status from the run.

## Common Mistakes

- Deriving from `Version.base_version`, which drops release-candidate, development, and post-release segments. Preserve the public version instead.
- Adding `.dirty` after the temporary metadata edit rather than from the preflight state. Determine dirty posture before stamping.
- Treating a directory source in the uv receipt as proof of editability. Require the explicit editable receipt field and `direct_url.json` flag.
- Restoring the entire file from Git. Restore only the temporary version substitution.
