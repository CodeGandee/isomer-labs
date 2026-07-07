## 1. Preparation

- [ ] 1.1 Verify GitHub CLI (`gh`) is authenticated and has access to the `CodeGandee` organization.
- [ ] 1.2 Confirm the target repository name `isomer-example-fa4-analytical-model` is available in `CodeGandee`.
- [ ] 1.3 Inventory all host-specific identifiers in the topic workspace (username, hostname, absolute paths, email placeholders).
- [ ] 1.4 Decide final placeholder values (e.g., `<USER>`, `<GPU_HOST>`, `<PROJECT_ROOT>`, `<NCU_PATH>`).

## 2. Sanitization Script

- [ ] 2.1 Create `scripts/sanitize-workspace.py` that exports the topic workspace to a staging directory.
- [ ] 2.2 Implement text-file replacement for username, hostname, and absolute project paths.
- [ ] 2.3 Add exclusion list for redownloadable/private directories (`.pixi/`, `tmp/`, `chatlogs/raw/`, `.mypy_cache/`, `page_images/`, layout-check PNGs).
- [ ] 2.4 Add inclusion list for required files (`pixi.toml`, `pixi.lock`, `README.md`, source code, final figures, sanitized records/intent).
- [ ] 2.5 Add a dry-run mode that prints replacements and excluded paths without writing.

## 3. Submodule Mapping

- [ ] 3.1 Identify the exact upstream commits used for `repos/extern/flash-attention/` and `repos/extern/accel-sim-framework/`.
- [ ] 3.2 Create `.gitmodules` entries for upstream dependencies in the staging `main` branch.
- [ ] 3.3 Create `.gitmodules` entry for `actors/operator` pointing to the same public repo with `branch = actor-operator`.

## 4. Branch Export

- [ ] 4.1 Export sanitized `repos/topic-main/` content as the public `main` branch.
- [ ] 4.2 Export sanitized `actors/operator/` content as the public `actor-operator` branch.
- [ ] 4.3 Ensure both branches have no host-specific identifiers in their initial commit history.

## 5. Repository Creation and Push

- [ ] 5.1 Run `gh repo create CodeGandee/isomer-example-fa4-analytical-model --public`.
- [ ] 5.2 Initialize the staging repository with the sanitized `main` branch and push it.
- [ ] 5.3 Push the sanitized `actor-operator` branch to the public repository.
- [ ] 5.4 In the `main` branch, register and commit the `actors/operator` submodule pointer.

## 6. Documentation and Reproduction

- [ ] 6.1 Write `README.md` with clone, environment setup, submodule, and paper-build instructions.
- [ ] 6.2 Create `scripts/setup-extern.sh` to clone simulator dependencies with `--depth=1`.
- [ ] 6.3 Add a `chatlogs/README.md` summarizing the research narrative if chatlogs are excluded.
- [ ] 6.4 Add a `LICENSE` or reuse the source project license as appropriate.

## 7. Validation

- [ ] 7.1 Perform a fresh clone of the public repo with `--recurse-submodules`.
- [ ] 7.2 Run `pixi install` and verify the environment is created.
- [ ] 7.3 Run `scripts/setup-extern.sh` and verify extern submodules/simulators are present.
- [ ] 7.4 Run `pixi run test` and confirm tests pass.
- [ ] 7.5 Build the paper PDF and confirm the final document is produced.
- [ ] 7.6 Scan the public repo for any remaining host identifiers.
