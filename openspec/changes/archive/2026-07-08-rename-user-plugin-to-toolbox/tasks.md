## 1. Domain Language and Specs

- [x] 1.1 Update `.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md` to define Toolbox as the canonical extension package term.
- [x] 1.2 Sync current OpenSpec specs so active requirements use Toolbox terminology, Toolbox table names, Toolbox schema names, and `skillset/toolboxes/` paths.
- [x] 1.3 Remove active current-spec requirements that preserve the old extension package concept name after the Toolbox replacement specs are in place.

## 2. Data Model and Manifest Schema

- [x] 2.1 Rename model dataclasses and fields from User Plugin names to Toolbox names in `src/isomer_labs/models/__init__.py`.
- [x] 2.2 Replace Project Manifest fields, TOML parsing, validation, rendering, and JSON output with `toolboxes`, `toolbox_runtime_param_imports`, and `toolbox_runtime_params`.
- [x] 2.3 Replace Topic Workspace Manifest fields, TOML parsing, validation, rendering, and JSON output with the same Toolbox table names.
- [x] 2.4 Replace durable identity and metadata fields with `toolbox_id`, toolbox-local callback keys, and Toolbox source metadata.
- [x] 2.5 Ensure old table names, field names, and schema versions fail with deterministic diagnostics rather than being accepted as aliases.

## 3. Toolbox Runtime and Callback Logic

- [x] 3.1 Rename `src/isomer_labs/project/user_plugins.py` to a Toolbox module and update registration, status, runtime param, import, resolution, mutation, and validation APIs.
- [x] 3.2 Rename `src/isomer_labs/project/user_plugin_callbacks.py` to a Toolbox callback manifest module and update manifest constants to `isomer-toolbox.v1` and `isomer-toolbox-runtime-params.v1`.
- [x] 3.3 Update skill callback install, resolve, list, show, validate, and gating code to use Toolbox metadata and `--toolbox-dir`.
- [x] 3.4 Update callback registry serialization so Toolbox-installed callbacks store `toolbox_id`, toolbox-local key, and Toolbox source metadata.
- [x] 3.5 Change missing Toolbox registration behavior for Toolbox-installed callbacks to deterministic gating diagnostics instead of compatibility enablement.

## 4. CLI Surface

- [x] 4.1 Replace `project user-plugins` with `project toolboxes` and update install, list, show, explain, enable, disable, update-source, uninstall, and validate commands.
- [x] 4.2 Replace `project user-plugin-params` with `project toolbox-params` and update define, set, get, list, explain, unset, validate, and import commands.
- [x] 4.3 Replace CLI option names, argument names, help text, diagnostics, and JSON command summaries so current output uses Toolbox wording only.
- [x] 4.4 Replace `project skill-callbacks install --plugin-dir` with `--toolbox-dir`.

## 5. Docs and Example Toolbox

- [x] 5.1 Update `docs/isomer-cli.md`, `docs/topic-workspace-definition.md`, and `docs/concepts.md` to document only Toolbox commands and schema names.
- [x] 5.2 Move `skillset/user-plugins/gpu-analytical-modeling` to `skillset/toolboxes/gpu-analytical-modeling`.
- [x] 5.3 Update the GPU analytical modeling Toolbox manifest, README, and review notes to use Toolbox terminology, `toolbox_id`, and Toolbox schema versions.
- [x] 5.4 Update living context docs that describe the GPU analytical modeling package so they no longer teach the old concept name.

## 6. Tests and Validation

- [x] 6.1 Rename and update runtime param tests to cover Toolbox manifest tables, fields, schema versions, resolution order, imports, and scope specialization.
- [x] 6.2 Rename and update skill callback tests to cover Toolbox manifest loading, installed callback keys, registry metadata, install semantics, and Toolbox status gating.
- [x] 6.3 Update CLI tests for `project toolboxes`, `project toolbox-params`, and `--toolbox-dir`.
- [x] 6.4 Update architecture/source-layout tests for renamed modules and moved package paths.
- [x] 6.5 Add negative tests showing old command names, table names, field names, and schema versions are rejected after the breaking rename.
- [x] 6.6 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test`.
