## 1. Command Surface

- [x] 1.1 Add the top-level `doctor` command to the Click CLI command group and to the documented command surface.
- [x] 1.2 Wire existing global options, Project selectors, topic selectors, and output-format options into `doctor` without adding mutation-oriented flags such as `--fix`.
- [x] 1.3 Ensure `isomer-cli --help` lists `doctor` and `isomer-cli doctor --help` documents the read-only diagnostic behavior.

## 2. Diagnostic Model and Reporting

- [x] 2.1 Add internal doctor report and check models with stable check identifiers, `pass`, `warn`, `fail`, and `skip` statuses, human messages, and optional structured details.
- [x] 2.2 Add doctor JSON rendering under the existing versioned CLI output wrapper with `mode`, `ok`, `mutated: false`, `checks`, and optional `pixi`, `project`, `topic`, and diagnostic fields.
- [x] 2.3 Add grouped text rendering for host, Project, and topic diagnostics while avoiding secrets, full environment dumps, and unstable absolute paths unless they are already normal Project-relative paths.

## 3. Pixi Inspection

- [x] 3.1 Implement Pixi executable discovery with `shutil.which("pixi")`, deterministic missing-binary failure reporting, and `pixi --version` parsing.
- [x] 3.2 Implement Project-level Pixi manifest discovery for `pixi.toml` or `pyproject.toml` and parse Pixi environments from the manifest using a TOML parser.
- [x] 3.3 Report `pixi.lock` presence as a Project-level readiness check and emit a warning when the manifest exists but the lockfile is absent.
- [x] 3.4 Detect declared Pixi version requirements and verify them with `pixi workspace requires-pixi verify --manifest-path <manifest-or-root>` when available.
- [x] 3.5 Normalize subprocess failures, unsupported Pixi output, and malformed TOML into stable doctor checks instead of uncaught tracebacks.

## 4. Topic Environment Intent

- [x] 4.1 Extend Project Manifest parsing to accept repeated `[[topic_pixi_environment_bindings]]` tables with `research_topic_id`, `pixi_environment`, optional `purpose`, and optional `status`.
- [x] 4.2 Validate Project Manifest topic environment bindings by checking each named Pixi environment against the Project-level Pixi manifest.
- [x] 4.3 Report a missing Project Manifest topic environment binding for a selected Research Topic without inferring a Pixi environment from the Research Topic id or environment names.
- [x] 4.4 Support one Research Topic binding to multiple Project-root Pixi environments through multiple active `topic_pixi_environment_bindings` entries.
- [x] 4.5 Extend Project Manifest parsing to accept repeated `[[topic_standalone_pixi_bindings]]` tables with `research_topic_id`, Project-root-relative `manifest_path`, optional `pixi_environment`, optional `purpose`, and optional `status`.
- [x] 4.6 Validate standalone Pixi isolation bindings by requiring registered Research Topic ids, Project-contained manifest paths, existing standalone manifests during `doctor`, and no implicit discovery from Topic Workspace files.
- [x] 4.7 Reject or ignore runtime truth in Research Topic Config or Project Manifest, including Pixi install output, prepared environment paths, readiness records, secrets, and Agent Workspace state.

## 5. Doctor Execution Flow

- [x] 5.1 Implement dependency-only mode when no Isomer Project is discovered so `doctor` can still check host-level Pixi readiness.
- [x] 5.2 Implement Project mode when Project discovery succeeds, including Project Manifest, Pixi manifest, lockfile, and declared Pixi requirement checks.
- [x] 5.3 Implement topic mode when topic selectors resolve an Effective Topic Context, including Project Manifest topic environment binding checks and skipped topic checks when no topic is selected.
- [x] 5.4 Ensure doctor execution never creates Workspace Runtime state, `state.sqlite`, Topic Workspaces, Agent Workspaces, Runs, Pixi environments, lockfiles, or generated config.

## 6. Tests

- [x] 6.1 Add CLI help tests for `doctor`, common options, topic selectors, JSON output, and absence of mutation flags.
- [x] 6.2 Add host Pixi tests for found and missing Pixi binaries with subprocess behavior mocked.
- [x] 6.3 Add Project Pixi tests for manifest detection, missing manifest failures, lockfile warnings, and declared Pixi requirement verification.
- [x] 6.4 Add topic environment binding tests for explicit Project Manifest Pixi envs, multiple env bindings, missing bindings, missing named envs, standalone manifest checks, duplicate active bindings, and invalid binding config.
- [x] 6.5 Add JSON and text output tests that assert stable check shape, `mutated: false`, deterministic ordering, and secret redaction.
- [x] 6.6 Add side-effect tests that run `doctor` against temporary fixtures and assert no runtime database, workspace directory, Pixi environment, lockfile, or config file is created.

## 7. Documentation and Verification

- [x] 7.1 Document `isomer-cli doctor` usage, output modes, and read-only guarantees in the CLI documentation or README location used for existing commands.
- [x] 7.2 Update Project Manifest documentation with explicit topic Pixi environment bindings and the rule that Isomer never infers topic-to-environment relationships from names.
- [x] 7.3 Run `openspec validate --all`, `pixi run lint`, `pixi run typecheck`, and `pixi run test` after implementation.
