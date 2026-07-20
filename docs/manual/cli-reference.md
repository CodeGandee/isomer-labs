# isomer-cli Reference

This manual page documents `isomer-cli`, the command-line interface for Isomer Labs. It supports Project discovery, Project Manifest validation, Effective Topic Context resolution, Workspace Path Resolution previews, Workspace Runtime management, Domain Agent Team Template and Topic Agent Team Profile work, Agent Team Instance records, and Houmao-backed launch paths.

## Root and Project Options

The root command exposes:

- `--print-json` — emit deterministic JSON for the selected command.
- `--debug` — include traceback details for unexpected internal CLI errors.
- `-h, --help` — show help for the command.

The `project` command group exposes:

- `--root TEXT` — explicit Project root selector.
- `--manifest TEXT` — explicit Project Manifest selector.

When `project --root` is omitted, `isomer-cli` walks up from the current working directory until it finds a `.isomer-labs/` Project Config Directory.

Many topic-scoped commands also accept lifecycle selectors such as `--topic`, `--topic-workspace`, `--research-inquiry`, `--task`, `--run`, `--agent-team-instance`, `--agent-instance`, and `--topic-actor`. These selectors refine the Effective Topic Context or actor-scoped path context. They do not by themselves mutate state.

## Output Posture

JSON output uses the `isomer-cli-output.v1` wrapper and includes a `mutated` flag when the command mutates Project files, Workspace Runtime records, adapter manifests, or live Houmao state. Use root-level `--print-json` for every command that needs deterministic JSON, including failure output. Without `--print-json`, commands print structured human-readable text. Command-local `--json`, `--format json`, and `--format=json` are not public command shapes.

## Failure Output

`isomer-cli` normalizes invocation errors, domain validation failures, keyboard interruptions, and unexpected internal exceptions into Isomer diagnostics. A wrong-format invocation reports what was wrong, the expected command shape when Click can provide it, and one to three examples for the nearest public command path. For example, `isomer-cli project paths get` without a semantic label reports the missing `SEMANTIC_LABEL`, usage for `project paths get`, and valid `project paths get` examples.

With root-level `--print-json`, normalized failures still use the `isomer-cli-output.v1` wrapper and include `ok: false`, diagnostics, and mutation certainty. Invocation failures that happen before a command handler runs report `mutated: false`. Unexpected internal exceptions report `mutation_state: "unknown"` when Isomer cannot prove whether a mutating command had already changed files.

Normal failure output does not include Python tracebacks. Use root-level `--debug` or `ISOMER_CLI_DEBUG=1` only when a human needs traceback details for an unexpected internal error; JSON debug details are isolated under a `debug` field so agents can ignore them safely.

## Command Groups

### System Skill Installation Commands

The `system-skills` namespace discovers and installs packaged Isomer public skill packs from the released Python package into local coding-agent skill roots:

- `system-skills extensions list`
- `system-skills extensions show <extension-id>`
- `system-skills list`
- `system-skills status`
- `system-skills install`
- `system-skills upgrade`
- `system-skills uninstall`

The three atomic installation units are core, DeepSci, and Kaoju. Each projects a public welcome and execution entrypoint pair: `isomer-op-welcome` with `isomer-op-entrypoint`, `isomer-ext-deepsci-welcome` with `isomer-ext-deepsci-entrypoint`, and `isomer-ext-kaoju-welcome` with `isomer-ext-kaoju-entrypoint`. Core owns 19 protected members, DeepSci owns 21, and Kaoju owns 13. `system-skills list` and extension discovery distinguish ordered public roles, entrypoint commands, protected logical ids, scoped members, aliases, dependencies, and compatibility metadata. Protected members are parent-routed nested bundles rather than ordinary top-level install units.

Supported targets are `claude-code`, `codex`, `kimi-code`, `generic`, and `all`, and every target-resolving operation requires `--target`. When `--scope` is omitted, `system-skills install` defaults to Project scope at the exact current working directory and does not search ancestor Git or Isomer roots. Explicit `--scope project` is equivalent, while `--scope user` is the only route to user-wide installation. `system-skills status`, `upgrade`, and `uninstall` require an explicit `--scope user|project`. The `all` target expands to every concrete target and deduplicates identical physical roots. Every public and protected skill carries its PEP 440 Isomer release version in `agents/openai.yaml`. Receipt v5 stores one record per pack with ordered welcome and entrypoint projections plus its ordered protected inventory; status reports per-role projection integrity, receipt drift, missing or extra nested material, and compatibility against package-owned minimum floors.

| Target | Project Scope | User Scope |
| --- | --- | --- |
| `claude-code` | `<cwd>/.claude/skills` | `${CLAUDE_CONFIG_DIR:-~/.claude}/skills` |
| `codex` | `<cwd>/.agents/skills` | `${CODEX_HOME:-~/.codex}/skills` |
| `kimi-code` | `<cwd>/.kimi-code/skills` | `${KIMI_CODE_HOME:-~/.kimi-code}/skills` |
| `generic` | `<cwd>/.agents/skills` | `~/.agents/skills` |

**Side effects:** `install` copies selected complete packs by default, or symlinks both public siblings with `--mode symlink`, and tracks the target skill root in `isomer-labs-skill-manifest.json`. Public welcome and entrypoint names are reserved install slots. If either selected public path already exists, `install` preserves the pack unless `--force` is supplied. An extension selector includes core. Either public `--skill` selector resolves to its pack; a protected logical id or old pipeline alias is accepted only as a deprecated selector for its complete owner pack. `upgrade` stages and validates complete packs, writes receipt v5, then removes only exact stale top-level paths tracked by a legacy receipt. `uninstall` removes both receipt-owned public projections and refuses single-role or single-member removal. `extensions list`, `extensions show`, `list`, and `status` are read-only.

```bash
isomer-cli system-skills list
isomer-cli --print-json system-skills list
isomer-cli system-skills extensions list
isomer-cli system-skills extensions show kaoju
isomer-cli system-skills install --target codex
isomer-cli system-skills install --target codex --extension deepsci
isomer-cli system-skills install --target codex --extension kaoju
isomer-cli system-skills install --target all --skill isomer-op-entrypoint
isomer-cli system-skills install --target codex --skill isomer-op-entrypoint --force
isomer-cli system-skills install --target codex --scope user
isomer-cli system-skills upgrade --target codex --scope project
isomer-cli --print-json system-skills status --target generic --scope project
isomer-cli system-skills uninstall --target codex --scope project
```

Migration: an install without `--scope` selects Project scope, and explicit `--scope project` remains equivalent. Use `--scope user` for user-wide installation, and keep explicit scope on status, upgrade, and uninstall. Replace an old command such as `--target kimi-code --home .kimi-code/skills` with `--target kimi-code` or `--target kimi-code --scope project`; replace `--target kimi-code --home ~/.kimi-code/skills` with `--target kimi-code --scope user`. The public installer does not accept arbitrary roots. Use host-native installation for custom destinations and keep `internals inspect-system-skill-root --skill-root <root>` for provider-neutral read-only verification.

Receipt v1 through v4 readers retain old flat or single-entrypoint paths as legacy evidence without claiming public-pair integrity. Managed upgrade preserves the old receipt and projections if staging or validation fails. After receipt v5 is committed, cleanup removes only legacy paths tracked by the old receipt. It preserves untracked lookalike paths and reports exact `stale_retained` paths when cleanup is partial. Refresh the agent host or start a new session after installation or upgrade because current-session discovery may be cached.

### Internal System Skill Inspection Commands

The `internals` namespace exposes provider-neutral, read-only primitives for version-aligned Isomer system skills:

- `internals inspect-system-skill-root`
- `internals classify-system-skill-inventory`

`inspect-system-skill-root` requires one explicit `--skill-root` and accepts `--category core|extensions|all`, `--extension <id>`, and `--group <name>` filters. It inspects no parent, home, plugin, provider configuration, or conventional tool path. The result distinguishes absent roots, receipt v5 and v1-v4 legacy receipts, malformed or unsupported receipts, per-role copy and symlink public projections, welcome-only and entrypoint-only state, broken or invalid projections, unmanaged same-name directories, protected nested coverage, missing logical ids, receipt drift, and compatibility state. Ambient top-level siblings are reported without recursive classification.

`classify-system-skill-inventory` accepts repeated `--skill-name` values and optional versioned JSON through `--inventory-json <file>` or `--inventory-json -` for stdin. Structured input uses `isomer-system-skill-inventory.v1`. Recognized public names report `welcome_seen`, `entrypoint_seen`, or `public_pair_seen`; an old flat protected name or pipeline alias reports a legacy observation and candidate owner pack. Name-only inventory never proves receipt ownership or complete protected integrity. Unknown names remain unmatched ambient entries, and supplied paths are not inspected.

**Side effects:** none. Both commands return the standard output wrapper, `mutated: false`, and the `isomer-internal-system-skill-inspection.v2` payload contract.

```bash
isomer-cli --print-json internals inspect-system-skill-root --skill-root /explicit/agent/skill-root --extension kaoju
isomer-cli --print-json internals classify-system-skill-inventory --skill-name isomer-ext-kaoju-entrypoint --skill-name isomer-kaoju-trial
isomer-cli --print-json internals classify-system-skill-inventory --inventory-json inventory.json
```

### Extension Research Commands

The `ext research` namespace manages GUI-readable research records and idea lineage metadata:

The top-level `ext` namespace contains native runtime and compatibility commands. It is distinct from installable agent-skill extensions, which are discovered with `isomer-cli system-skills extensions`. Kaoju research decisions are orchestrated through `$isomer-ext-kaoju-entrypoint use <subcommand> to <task>`; deterministic MyST paper and wiki operations use `ext kaoju`.

- `ext research ideas generation upsert`
- `ext research ideas graph`
- `ext research ideas import-from-record`
- `ext research ideas lineage add`
- `ext research ideas query`
- `ext research ideas realize`
- `ext research ideas repair`
- `ext research ideas upsert`
- `ext research ideas validate`
- `ext research operation-sets inspect`
- `ext research operation-sets accept`
- `ext research operation-sets verify`
- `ext research records index cleanup`
- `ext research records index rebuild`
- `ext research records index validate`
- `ext research records lineage add`
- `ext research records lineage backfill`
- `ext research records lineage query`
- `ext research records lineage siblings`
- `ext research records lineage validate`
- `ext research records migrate-payload-files`
- `ext research records query export`
- `ext research records query facets`
- `ext research records query files`
- `ext research records query lineage`
- `ext research records query list`
- `ext research records query siblings`
- `ext research records render`
- `ext research records revise`
- `ext research records validate`

### Project Extension and GUI Commands

These project commands register extension metadata, manage topic reset checkpoints, and run the local GUI:

- `project artifact-formats register`
- `project artifact-formats render`
- `project artifact-formats validate`
- `project skill-callbacks install`
- `project team-repositories inspect`
- `project team-repositories list`
- `project team-templates register`
- `project toolbox-params define`
- `project toolbox-params import list`
- `project toolbox-params import remove`
- `project toolbox-params import show`
- `project toolbox-params list`
- `project toolbox-params unset`
- `project toolbox-params validate`
- `project toolboxes explain`
- `project toolboxes list`
- `project toolboxes uninstall`
- `project toolboxes update-source`
- `project topic-main-guidance ensure`
- `project topic-main-guidance inspect`
- `project topic-main-guidance render`
- `project topic-reset apply`
- `project topic-reset checkpoint`
- `project topic-reset list`
- `project topic-reset plan`
- `project topic-reset show`
- `project topic-reset show-plan`
- `project topic-reset update-checkpoint`
- `project web serve`

### Project Houmao Integration Commands

The `project integrations houmao` namespace manages Isomer-owned Houmao integration policy and Project-local projected Houmao support skills. These commands keep Houmao as an internal provider for Isomer service routing; ordinary users should install and use Isomer system skills, then let Isomer-provided skill context route the agent to Houmao-owned procedures when needed.

- `project integrations houmao status`
- `project integrations houmao enable`
- `project integrations houmao disable`
- `project integrations houmao prepare-skills`
- `project integrations houmao skill-context`
- `project integrations houmao topic-service-master names`
- `project integrations houmao topic-service-master binding show`
- `project integrations houmao topic-service-master binding record`

**Side effects:** `status`, `skill-context`, `topic-service-master names`, and `topic-service-master binding show` are read-only. `enable` and `disable` record the Project Houmao integration policy in the Project Manifest. `prepare-skills` projects Isomer-managed Houmao support skills under the Project config directory. `topic-service-master binding record` writes the Topic Service Master binding to the selected Topic Workspace Manifest when Houmao integration is enabled; when integration is disabled it reports a skipped binding without mutating the workspace.

```bash
isomer-cli --print-json project integrations houmao status
isomer-cli --print-json project integrations houmao enable
isomer-cli --print-json project integrations houmao disable
isomer-cli --print-json project integrations houmao prepare-skills
isomer-cli --print-json project integrations houmao skill-context prepare-topic-service-master --topic my-topic
isomer-cli --print-json project integrations houmao topic-service-master names --topic-workspace my-topic
isomer-cli --print-json project integrations houmao topic-service-master binding show --topic my-topic
isomer-cli --print-json project integrations houmao topic-service-master binding record --topic my-topic --status prepared --specialist-name isomer-topic-my-topic-service-master --launch-profile-name isomer-topic-my-topic-service-master-default --managed-agent-name isomer-topic-my-topic-service-master --updated-by isomer-srv-topic-service-agent-support
```

`skill-context` requires a lifecycle route such as `prepare-topic-service-master`, `launch-topic-service-master`, `inspect-topic-service-master`, `stop-topic-service-master`, or `repair-topic-service-master`. When integration is enabled, the JSON output returns the Project-local `houmao_skill_path` and `houmao_project_path` that the Isomer skill should pass to the agent. When integration is disabled, callers should skip Houmao-backed work and report the recorded skip reason.

`topic-service-master names` accepts `--topic-workspace <topic-workspace-id>` and returns Isomer's suggested Houmao specialist, launch profile, and managed-agent names for that Topic Workspace. `topic-service-master binding show` resolves a selected topic through the normal Effective Topic Context selectors and reports suggested names plus the current binding. `topic-service-master binding record` accepts `--status prepared|launched|stopped|stale|archived|blocked|skipped`, `--specialist-name`, `--launch-profile-name`, `--managed-agent-name`, optional provider refs, and `--updated-by`.

### `project init`

Initialize the smallest valid Project configuration and Project-level Houmao overlay.

**Side effects:** runs the supported Houmao Project bootstrap boundary for the selected Project root and writes `.isomer-labs/manifest.toml`, the Isomer-managed Houmao overlay under `.isomer-labs/.houmao/`, and the selected content root's `README.md` and `.gitignore`. The fresh manifest contains path defaults but no Research Topic defaults, Research Topic registrations, or Topic Workspace registrations. The generated `.gitignore` ignores generated content by default while keeping `README.md` and `.gitignore` trackable. Does not create a Research Topic Config, Topic Workspace directory, `state.sqlite`, Workspace Runtime subdirectories, Agent Workspaces, adapter launch material, mailboxes, gateways, managed agents, sessions, or launch dossiers.

**Prerequisites:** the target directory must not already be an Isomer-managed Project unless you intend to reinitialize. Nested Project roots are allowed; cwd-based discovery resolves the nearest `.isomer-labs/manifest.toml`, like Git repository discovery. Houmao command resolution must succeed through `houmao-mgr`, `ISOMER_HOUMAO_COMMAND`, or a supported local checkout.

**Options:** pass `--content-dir <content-dir>` to select a project-local generated content root during fresh initialization.

```bash
isomer-cli project init
isomer-cli project init --content-dir custom-content
```

`--content-dir <content-dir>` must resolve inside the Project root and must not live inside `.isomer-labs/` or collide with root `.houmao/`. When omitted, init uses `isomer-content/`. Create Research Topics with `project topics create`, not `project init`. Direct initialization does not inspect agent skill roots, read a live agent inventory, or register optional extensions. When an active Project Operator Session uses `isomer-op-project-mgr init-project`, that higher-level skill delegates separate additive reconciliation to `isomer-op-system-skill-mgr` unless the user opts out.

### `project content-root move`

Plan or apply relocation of the Project generated content root.

**Side effects:** without `--yes`, none. `--dry-run` always builds the relocation plan without moving files or rewriting the Project Manifest, and omitting both `--dry-run` and `--yes` defaults to dry-run mode. With `--yes`, moves only Isomer-managed content-root policy files and registered Topic Workspace directories that are safe to move, updates Project Manifest path defaults and Topic Workspace paths, preserves unmanaged leftovers, and reports skipped or blocked entries. It does not rewrite runtime-internal paths inside moved Topic Workspaces.

**Options:** `--to <content-dir>` selects the new project-local generated content root. The destination must resolve inside the Project root, must not live inside `.isomer-labs/`, and must not collide with protected Project or Houmao paths.

```bash
isomer-cli project content-root move --to generated --dry-run
isomer-cli --print-json project content-root move --to generated --dry-run
isomer-cli --print-json project content-root move --to generated --yes
```

### `project cleanup`

Plan or apply cleanup of selected Isomer-managed Project material.

**Side effects:** without `--yes`, none. `--dry-run` always builds the same deterministic plan without deleting files, and omitting both `--dry-run` and `--yes` defaults to dry-run mode. With `--yes`, deletes only targets listed in the validated plan. `project cleanup` does not stop live Houmao agents, inspect gateways, infer unregistered Research Topics from directories, or remove the whole generated content root unless `--part content-root --purge-content-root --yes` is selected.

**Parts:** `project-config` removes `.isomer-labs/`; `houmao-overlay` removes the Isomer-managed `.isomer-labs/.houmao/` overlay; `content-policy` removes the selected content root's generated `README.md` and `.gitignore`; `topic-workspace` removes selected registered Topic Workspace directories; `runtime` removes `state.sqlite`, runtime-owned directories, and adapter runtime material under selected Topic Workspaces; `bootstrap` combines Project config, Houmao overlay, content policy files, and registered Topic Workspace directories; `content-root` removes the selected generated content root only with `--purge-content-root`.

```bash
isomer-cli project cleanup --part bootstrap --dry-run
isomer-cli project cleanup --part bootstrap --yes
isomer-cli --print-json project cleanup --part runtime --topic my-topic --dry-run
isomer-cli project cleanup --part content-root --purge-content-root --yes
```

When a valid Project Manifest exists, cleanup uses it as authority for path defaults, Research Topic registrations, and Topic Workspace registrations. If the manifest is missing or malformed, cleanup is limited to `.isomer-labs/`, `.isomer-labs/.houmao/`, root `.houmao/` as external state, and the built-in or explicitly selected content root policy files; it will not infer Research Topics from filesystem directories.

### `doctor`

Run read-only dependency, Project, and topic diagnostics.

**Side effects:** none. Checks host Pixi availability, Project-level Pixi configuration, optional `requires-pixi`, `pixi.lock` presence, Project-root topic Pixi bindings, and Topic Workspace Pixi binding targets. If no explicit `topic_standalone_pixi_bindings.manifest_path_or_dir` target exists, it checks the registered Topic Workspace directory as the implicit default target with Pixi environment `default`. Does not install Pixi environments, create lockfiles, create Topic Workspace runtime state, create Agent Workspaces, or edit Project config.

```bash
isomer-cli --print-json doctor
isomer-cli --print-json doctor --with-topic my-topic
```

### `project validate`

Validate the Project Manifest and registered configs.

**Side effects:** none.

```bash
isomer-cli --print-json project validate
isomer-cli --print-json project --root /path/to/project validate
```

### `project topics list`

List registered Research Topics.

**Side effects:** none.

```bash
isomer-cli project topics list
isomer-cli --print-json project topics list
```

### `project topics create`

Create and register a Research Topic and its Topic Workspace.

**Side effects:** writes `.isomer-labs/research-topics/<topic-id>.toml`, updates `.isomer-labs/manifest.toml` with `[[research_topics]]` and `[[topic_workspaces]]`, and creates the Topic Workspace directory. It does not create Workspace Runtime state or live Houmao state.

```bash
isomer-cli project topics create my-topic --statement "Investigate the concrete research question."
isomer-cli project topics create my-topic --statement "Investigate the concrete research question." --workspace-dir topic-workspaces/my-topic --set-default
```

### `project topics show`

Show one registered Research Topic, its config, associated Topic Workspace registration, effective workspace path, status, and diagnostics.

**Side effects:** none.

```bash
isomer-cli --print-json project topics show my-topic
```

### `project topics update`

Update bounded Research Topic metadata. Supported updates are `--statement`, `--status active|archived`, and `--set-default`; topic rename is not supported by this command.

**Side effects:** updates `.isomer-labs/manifest.toml` for status/default changes and the Research Topic Config for statement changes. It preserves existing workspace contents.

```bash
isomer-cli project topics update my-topic --statement "Investigate the revised concrete research question."
isomer-cli project topics update my-topic --status archived
isomer-cli project topics update my-topic --set-default
```

### `project topics delete`

Plan or apply Research Topic deletion.

**Side effects:** `--dry-run` mutates nothing. `--yes` removes the Research Topic registration, associated Topic Workspace registration, matching Project Manifest defaults, and Research Topic Config file when no blockers remain. It preserves the Topic Workspace directory and reports cleanup guidance for filesystem removal.

```bash
isomer-cli --print-json project topics delete my-topic --dry-run
isomer-cli --print-json project topics delete my-topic --yes
```

### `project workspaces list`

List registered Topic Workspaces.

**Side effects:** none.

```bash
isomer-cli project workspaces list
isomer-cli --print-json project workspaces list
```

### `project skill-callbacks`

Register, inspect, resolve, disable, and validate User Skill Callbacks. A User Skill Callback is supplemental instruction material attached to one packaged system skill and one stage, currently `begin` or `end`. Participating skills resolve `begin` callbacks after mandatory context checks and before workflow step 1, then resolve `end` callbacks after tentative outputs exist and before final response or handoff.

**Side effects:** `register` writes or updates a callback registry under `.isomer-labs/user-skill-callbacks/`, materializes inline prompts as managed Markdown files, and adds a Project Manifest or Research Topic Config registry ref. `install --toolbox-dir` is a lower-level callback refresh or repair primitive for Toolbox manifests; it writes callback records and ensures a matching Toolbox registration, but it does not install runtime-param default imports. `disable` marks the callback inactive while keeping the record. `resolve`, `insertion-points`, `list`, `show`, and `validate` are read-only.

Callbacks are instruction material, not executable provider payloads. They cannot override system or developer instructions, the owning system skill, the current user request, Isomer domain constraints, required Gates, evidence rules, validation, or recording obligations. Empty resolution results are normal and do not block the owning workflow.

```bash
isomer-cli --print-json project skill-callbacks register --topic my-topic --id scout-domain-prior --skill isomer-deepsci-scout --stage begin --prompt "Prefer the local benchmark contract before broad discovery."
isomer-cli --print-json project skill-callbacks register --scope project --id write-style-check --skill isomer-deepsci-write --stage end --prompt-file docs/callbacks/write-style-check.md
isomer-cli --print-json project skill-callbacks register --topic my-topic --id paper-dir-callback --skill isomer-deepsci-paper-outline --stage begin --skill-dir extern/orphan/my-paper-callback --allow-external-source
isomer-cli --print-json project skill-callbacks insertion-points
isomer-cli --print-json project skill-callbacks insertion-points --extension deepsci --skill isomer-deepsci-scout --stage begin
isomer-cli --print-json project skill-callbacks resolve --topic my-topic --skill isomer-deepsci-scout --stage begin
isomer-cli --print-json project skill-callbacks resolve --topic my-topic --skill isomer-deepsci-scout --stage begin --explain
isomer-cli --print-json project skill-callbacks list --topic my-topic
isomer-cli --print-json project skill-callbacks show scout-domain-prior --topic my-topic
isomer-cli --print-json project skill-callbacks disable scout-domain-prior --topic my-topic
isomer-cli --print-json project skill-callbacks validate --topic my-topic
```

Use `--prompt` for short inline guidance that Isomer should materialize into managed callback content. Use `--prompt-file` for a project-scoped file that already contains the guidance. Use `--skill-dir` when the callback guidance lives in an external skill directory with `SKILL.md`; Isomer reads it as supplemental instruction material and does not install it as a packaged system skill.

Ordinary `resolve` is the agent execution surface. Its ordered `callbacks` array contains only `id`, `source_type`, and an absolute `instruction_path`, plus `external: true` for an explicitly authorized source outside the Project root. `prompt` and `prompt_file` entries point to their readable prompt file. A `skill_dir` entry points directly to `<skill-dir>/SKILL.md`. An empty array is a successful result and needs no special handling.

Use `resolve --explain` when an operator or agent must diagnose precedence, registry provenance, source selection, Toolbox status, or gating. It returns the full callback records, registry refs, source metadata, effective Toolbox statuses, and gated callback ids that ordinary resolution intentionally omits. `list`, `show`, and `validate` remain the detailed inventory and management surfaces.

Resolution validates only state that can affect the requested instruction set: Project and selected-topic context, visible registries, the requested insertion point, callback sources, duplicate visible callback ids, and applicable Toolbox gating. Unrelated environment, template, profile, research-record, and other Project diagnostics remain available through `project validate`; registry-wide callback health remains available through `project skill-callbacks validate`.

Use `insertion-points` to query manifest-declared callback targets. By default it lists core insertion points and insertion points from Project-declared operator system extensions; `--extension <id>` and `--all-catalog-extensions` query catalog extension points without claiming that optional extension skill files were filesystem-verified.

Toolbox-installed callbacks include `toolbox_id` metadata. During `resolve`, Isomer checks the effective Toolbox status for the selected Project or topic context. A disabled Toolbox leaves callback records installed for audit, but its callbacks are omitted from ordinary resolution without exposing management state. `resolve --explain`, `list`, `show`, and `validate` report the relevant Toolbox status and `gated_callback_ids`. Callback records with Toolbox metadata but no matching Toolbox registration are omitted with a resolution-blocking diagnostic.

This compact default is a breaking JSON response change. Execution callers that previously parsed full callback records must consume the returned order and read each `instruction_path`. Management or diagnostic callers must add `--explain` or use `list` or `show`. The change requires no callback-registry, Toolbox-manifest, or Toolbox-registration migration.

System skill families use `isomer-<extension-name>-<purpose>` names for domain extensions such as `isomer-deepsci-*`. `isomer-misc-*` remains the public cross-domain helper namespace, not a generic extension bucket.

### `project system-extensions`

List and maintain user-declared Project operator system extensions, or inspect caller-supplied skill roots. Declarations live in the Project Manifest under `[operator.system_extensions]` and remain authoritative user-controlled policy, not proof that every current agent host can load an extension. Detection delegates each explicit root to the internal inspector and never turns an observation into a Project declaration.

**Side effects:** `remember` and `forget` mutate only the Project Manifest declaration list. `list` and `detect` are read-only. With no `--skill-root`, `detect` reports declarations and catalog state without scanning any filesystem root. Repeat `--skill-root` to inspect roots already known to the current caller.

```bash
isomer-cli --print-json project system-extensions list
isomer-cli --print-json project system-extensions detect
isomer-cli --print-json project system-extensions detect --skill-root /explicit/agent/skill-root
isomer-cli --print-json project system-extensions remember deepsci
isomer-cli --print-json project system-extensions forget deepsci
```

Detection keeps observations separated by supplied root and reports managed receipt evidence, projection state, complete and missing members, and version compatibility. Use `isomer-op-system-skill-mgr` for operator-aware declaration-first routing, live-inventory fallback, additive reconciliation, selected-root installation, stale declaration repair, and `host_refresh_required` guidance. Automated reconciliation never forgets declarations when different agents expose different extension inventories.

### `project toolboxes`

Install and manage Toolbox bundles. Registrations live in the Project Manifest for `scope = "project"` or in the selected Topic Workspace Manifest for `scope = "research_topic"`, `scope = "topic_actor"`, or `scope = "topic_agent"`. New topic-agent commands document `--topic-agent`; `--agent` remains accepted as an alias where this selector is supported.

**Side effects:** `install` validates the Toolbox manifest, writes or updates the selected Toolbox registration, installs declared callback records for Project or Research Topic scope, and registers manifest-declared runtime-param default bundle imports only when `--install-runtime-defaults` is present. Topic Actor and Topic Agent install scopes can manage Toolbox registration and runtime-param imports, but Toolboxes with callbacks are rejected at those narrower scopes until callback registries support them. `enable`, `disable`, `update-source`, and `uninstall` mutate only the selected manifest layer. `list`, `show`, `explain`, and `validate` are read-only.

```bash
isomer-cli --print-json project toolboxes install --toolbox-dir skillset/toolboxes/gpu-analytical-modeling
isomer-cli --print-json project toolboxes install --toolbox-dir skillset/toolboxes/gpu-analytical-modeling --topic my-topic --install-runtime-defaults
isomer-cli --print-json project toolboxes disable gpu-analytical-modeling --topic my-topic --scope research_topic
isomer-cli --print-json project toolboxes enable gpu-analytical-modeling --topic my-topic --scope topic_agent --topic-agent coder
isomer-cli --print-json project toolboxes show gpu-analytical-modeling --topic my-topic --topic-agent coder
isomer-cli --print-json project toolboxes validate --topic my-topic
```

### `project toolbox-params`

Manage Toolbox runtime params that callback skills can query through JSON. These commands are direct configuration primitives and can be used with or without high-level Toolbox installation. Effective param ids use `<toolbox_id>:<key>`. Values resolve in this order: Project Manifest imports, Project Manifest explicit params, Topic Workspace Manifest imports, Topic Workspace Manifest explicit params. Topic rows can specialize by Research Topic, exact Topic Actor name, or exact Topic Agent name.

**Side effects:** `define`, `set`, `unset`, `import add`, and `import remove` mutate only the selected manifest layer. `get`, `list`, `explain`, `validate`, `import list`, and `import show` are read-only.

```bash
isomer-cli --print-json project toolbox-params set gpu-analytical-modeling:evidence/mode --value strict --value-type enum --allowed-value strict --allowed-value relaxed
isomer-cli --print-json project toolbox-params import add gpu-analytical-modeling profiles/gpu-defaults.toml --topic my-topic --scope research_topic
isomer-cli --print-json project toolbox-params set gpu-analytical-modeling:evidence/mode --topic my-topic --scope topic_agent --topic-agent coder --value relaxed --value-type enum --allowed-value strict --allowed-value relaxed
isomer-cli --print-json project toolbox-params get gpu-analytical-modeling:evidence/mode --topic my-topic --topic-agent coder
isomer-cli --print-json project toolbox-params explain gpu-analytical-modeling:evidence/mode --topic my-topic --topic-agent coder
```

Imported TOML files contain param rows only. Import paths are relative to the manifest file that declares them, so Project Manifest imports resolve relative to `.isomer-labs/` and Topic Workspace Manifest imports resolve relative to the Topic Workspace root. Runtime params are not a credentials surface; secret-like keys or values are rejected.

### `project context show`

Show resolved Effective Topic Context.

**Side effects:** none. The resolved context is process-local and is not stored as Workspace Runtime state.

```bash
isomer-cli --print-json project context show --topic my-topic
```

### `project self`

Query small, read-only slices of the caller's process-local Isomer identity from an initialized Project or Topic Main Development Repository cwd.

**Side effects:** none. These commands do not create Topic Workspace directories, Workspace Runtime records, Path Plans, manifests, Pixi files, guidance files, launch material, adapter files, or live Houmao state.

Start with `project self show` for a tiny index, then ask for only the needed slice. Use `identity` for resolved topic, Topic Actor, and Agent refs; `pixi` for the selected manifest, environment, and `pixi run --manifest-path ... --environment ... python ...` hint; `env` for recognized Isomer environment input names without values by default; `paths <label>...` for requested semantic labels only; and `queries` for follow-up command examples. `project self env --values` may print allowlisted non-secret identity/path/config values, but secret-like names remain omitted.

```bash
isomer-cli --print-json project self show
isomer-cli --print-json project self identity
isomer-cli --print-json project self pixi
isomer-cli --print-json project self env
isomer-cli --print-json project self paths topic.repos.main agent.workspace --agent alice
isomer-cli --print-json project self queries
```

### `project paths preview`

Preview workspace paths, including semantic labels, compatibility surface ids, path sources, and the generated content root, without creating them.

**Side effects:** none.

```bash
isomer-cli project paths preview --topic my-topic
isomer-cli --print-json project paths preview --topic my-topic
```

### `project paths get`

Resolve one semantic workspace surface label for the selected Topic Workspace.

**Side effects:** none. This command does not create `topic-workspace.toml`, directories, Workspace Runtime records, Git repositories, branches, or worktrees.

Use dotted semantic labels such as `topic.repos.main`, `topic.records.artifacts`, `topic.runtime.db`, `topic.actors.workspace`, `topic.actors.private_artifacts`, `agent.workspace`, `agent.private_artifacts`, `agent.public_share`, and `agent.scratch`. Add `--configured` when you need the current manifest or environment answer instead of a historical Path Plan. Actor-scoped labels need a Topic Actor selector unless the current working directory is already inside the selected Topic Actor Workspace. Agent-scoped labels need an Agent Name or Agent Instance selector unless the current working directory is already inside the selected agent's Agent Workspace.

```bash
isomer-cli --print-json project paths get topic.records.artifacts --topic my-topic
isomer-cli --print-json project paths get topic.repos.main --topic my-topic --configured
isomer-cli --print-json project paths get topic.actors.output_root --topic my-topic --topic-actor operator
isomer-cli --print-json project paths get agent.output_root --topic my-topic --agent alice
```

### `project outputs policy`

Resolve the user-customizable worker output root and post-operation commit preference for one Topic Actor or Agent. The JSON result includes the absolute root, worker-relative root, worker identity, source metadata, operation-set pattern, and `commit_after_operation`. `.gitignore` and Git status control whether files under the root are tracked or committable.

**Side effects:** none. This command does not create directories, write manifests, write runtime records, launch agents, or commit files.

```bash
isomer-cli --print-json project outputs policy --topic my-topic --topic-actor operator
isomer-cli --print-json project outputs policy --topic my-topic --agent alice
```

### `project paths default`

Show the built-in default-layout path for one reserved semantic label without Path Plan, environment, or manifest override precedence. The command also plans the default candidate for a valid unregistered non-main grouped repository label such as `topic.repos.sources.method`.

**Side effects:** none. It does not write the Topic Workspace Manifest, create the candidate directory, bind the label, initialize Git, acquire content, or write a Path Plan. JSON output reports `mutated: false`; `path` contains the semantic label, absolute candidate path, `storage_profile`, and `source`. Text output prints the label and candidate path followed by the source.

```bash
isomer-cli --print-json project paths default topic.repos.main --topic my-topic
isomer-cli --print-json project paths default topic.repos.sources.method --topic my-topic
isomer-cli --print-json project paths default topic.actors.workspace --topic my-topic --topic-actor operator
isomer-cli --print-json project paths default agent.workspace --topic my-topic --agent alice
```

Invalid or main-repository sublabels fail with diagnostics. A valid grouped repository candidate remains available even when the Topic Workspace Manifest does not yet bind it.

### `project paths explain`

Explain candidate sources for one semantic label, including the selected source, source detail, diagnostics, and why the selected source wins.

**Side effects:** none.

```bash
isomer-cli --print-json project paths explain topic.repos.main --topic my-topic
isomer-cli --print-json project paths explain custom.datasets.raw --topic my-topic
```

### `project paths list`

List known semantic workspace labels with scope, required context, resolution status, path, source, and diagnostics when available.

**Side effects:** none.

```bash
isomer-cli project paths list --topic my-topic
isomer-cli --print-json project paths list --topic my-topic --topic-actor operator
isomer-cli --print-json project paths list --topic my-topic --agent alice
```

### `project paths register`

Register a semantic binding in the Topic Workspace Manifest. Active binding fields are intentionally compact: `label`, `path`, and `storage_profile`. Isomer does not infer `storage_profile` from the path because the same directory shape can have different ownership, durability, and safety semantics.

Use `custom.*` for user-defined labels. Use grouped reserved repository labels under `topic.repos.*`, such as `topic.repos.inner_group.some_repo_name`, when the binding describes another topic repository. Helper-created non-main repositories default under `repos/extern/...`; callers should still query the semantic label. Reserved roots such as `project`, `topic`, and `agent` are Isomer-owned except for accepted grouped families.

**Side effects:** writes `<topic-workspace>/topic-workspace.toml`; with `--create`, creates the validated target path. It does not create Workspace Runtime records or rewrite historical Path Plans.

```bash
isomer-cli --print-json project paths register custom.datasets.raw --topic my-topic --path data/raw --storage-profile topic_records_dir --create
isomer-cli --print-json project paths register topic.repos.inner_group.some_repo_name --topic my-topic --path repos/extern/inner_group/some_repo_name --storage-profile topic_repo --create
```

### `project paths update`

Update an existing manifest binding's `path`, `storage_profile`, or both after the same validation used by registration.

**Side effects:** writes `<topic-workspace>/topic-workspace.toml`; with `--create`, creates the new target path. It preserves previous filesystem targets and historical Path Plans.

```bash
isomer-cli --print-json project paths update custom.datasets.raw --topic my-topic --path data/raw-production DeepSci --create
```

### `project paths unregister`

Remove a dynamic `custom.*` or grouped reserved binding from the Topic Workspace Manifest.

**Side effects:** writes `<topic-workspace>/topic-workspace.toml`. It does not delete the target directory or historical Path Plans. Built-in labels cannot be unregistered; use `project paths reset` to remove a built-in override.

```bash
isomer-cli --print-json project paths unregister custom.datasets.raw --topic my-topic
```

### `project paths reset`

Remove a manifest override for a built-in reserved label and fall back to the default catalog behavior.

**Side effects:** writes `<topic-workspace>/topic-workspace.toml`. It does not delete the previous target directory or historical Path Plans.

```bash
isomer-cli --print-json project paths reset topic.repos.main --topic my-topic
```

### `project paths materialize-default`

Write or update the Topic Workspace Manifest and create selected default-layout paths from `isomer-default.v1`.

**Side effects:** writes `<topic-workspace>/topic-workspace.toml` and creates only the selected owned default directories. Without `--label`, the command materializes the standard topic-owned default readiness labels and does not create per-actor or per-agent directories. Actor-scoped labels such as `topic.actors.private_artifacts` require `--topic-actor` or another explicit Topic Actor selector. Agent-scoped labels such as `agent.private_artifacts` require `--agent` or another explicit agent selector.

```bash
isomer-cli --print-json project paths materialize-default --topic my-topic --label topic.records.artifacts
isomer-cli --print-json project paths materialize-default --topic my-topic --topic-actor operator --label topic.actors.private_artifacts
isomer-cli --print-json project paths materialize-default --topic my-topic --agent alice --label agent.private_artifacts
```

### `project paths materialize`

Create the currently configured target for an existing semantic label according to its `storage_profile`, ignoring stored Path Plans but honoring current environment and manifest configuration.

**Side effects:** creates the configured directory or file parent as required by the label's `storage_profile`. It does not alter the manifest and does not delete previous targets.

```bash
isomer-cli --print-json project paths materialize custom.datasets.raw --topic my-topic
isomer-cli --print-json project paths materialize topic.repos.main --topic my-topic
```

### `project repos create`

Register and create an empty non-main topic repository directory without writing the manifest by hand. A bare name such as `inner_group.some_repo_name` becomes `topic.repos.inner_group.some_repo_name`; the command uses `storage_profile = "topic_repo"` and defaults the path to `repos/extern/inner_group/some_repo_name`. Use this command only when an empty support directory is the intended result. Use semantic path commands to materialize or override `topic.repos.main`.

**Side effects:** writes `<topic-workspace>/topic-workspace.toml` and, unless `--no-create` is set, creates the repository target directory. It does not initialize Git, select a source, acquire content, verify identity, or record source provenance.

```bash
isomer-cli --print-json project repos create inner_group.some_repo_name --topic my-topic
isomer-cli --print-json project repos create tools.benchmarks --topic my-topic
isomer-cli --print-json project repos create topic.repos.tools.benchmarks --topic my-topic --path repos/extern/tools/benchmarks --replace
```

### `project repos register`

Register an existing externally acquired and verified directory as a non-main Canonical External Repository. A bare label such as `sources.method` becomes `topic.repos.sources.method`; the binding always uses `storage_profile = "topic_repo"`. The path must already be a safe project-local directory. Isomer does not inspect Git state, invoke a subprocess, create content, or infer source identity.

**Prerequisites:** acquire or copy the source with commands chosen by the user or agent, verify that it is the intended source, observe an immutable commit or digest, and remove or quarantine failed partial content outside Isomer. Keep credentials, signed URLs, headers, environment values, stdout, and stderr out of durable evidence.

**Side effects:** on a new valid binding, writes `<topic-workspace>/topic-workspace.toml` only. It does not create or alter the target directory, run Git, write a Workspace Runtime record, or clean external content. Repeating the same label and path is successful and reports `mutated: false`; registering a different path for an existing label fails and directs the caller to the explicit `project paths update` topology-change route.

Text output reports the normalized semantic label and absolute path. JSON output reports `ok`, `mutated`, `manifest`, `repository`, `created_paths: []`, and diagnostics. Failures include an invalid grouped label, `topic.repos.main` misuse, a missing path, a non-directory path, an unsafe or non-project-local path, and a binding conflict.

The following Git commands are one replaceable external example. Use the user's exact command when supplied; otherwise choose Git, a provider CLI, a local copy, archive extraction, sparse checkout, submodules, LFS, or another suitable method outside Isomer.

```bash
target="$(isomer-cli --print-json project paths default topic.repos.sources.method --topic my-topic | jq -r '.path.path')"
git clone --branch "$SOURCE_REF" "$SOURCE_URL" "$target"
git -C "$target" remote get-url origin
git -C "$target" rev-parse --verify 'HEAD^{commit}'
isomer-cli --print-json project repos register sources.method --topic my-topic --path "$target"
isomer-cli --print-json project repos register sources.method --topic my-topic --path repos/extern/sources/method
```

After registration, a research workflow records the sanitized requested and resolved locators, semantic label, observed immutable identity, selected external method, verification basis, observation time, access and license posture, limitations, and blockers through its typed Artifact contract.

### `project artifacts describe/put/revise/latest/list/show/archive/migrate-scope`

Resolve and manage typed Kaoju Artifacts through Workspace Runtime. `describe` returns the checked declarative binding without an internal path template. `put` and `revise` infer record kind, profile, semantic label, content mode, revision behavior, accepted status, and scope policy. `latest`, `list`, and `show` query the state DB; they never scan directories for semantic state.

**Side effects:** `put` and `revise` validate content and relationships, allocate owner-preserved managed storage when applicable, write or register file-backed content, and create a durable record. `archive` changes lifecycle state without deleting external content. Other operations are read-only unless `migrate-scope --apply` performs an unambiguous legacy backfill.

```bash
isomer-cli --print-json project artifacts describe KAOJU:READING-LIST --topic my-topic
isomer-cli --print-json project artifacts put KAOJU:READING-LIST reading-list.json \
  --topic my-topic \
  --producer isomer-kaoju-discover \
  --scope-key direction:memory-offload \
  --relationships-json '[{"role":"direction_set","target_ref":"directions-1"},{"role":"discovery_ledger","target_ref":"discovery-1"}]'
isomer-cli --print-json project artifacts latest KAOJU:READING-LIST --topic my-topic --scope-key direction:memory-offload
isomer-cli --print-json project artifacts list --topic my-topic
isomer-cli --print-json project artifacts show <record-id> --topic my-topic
isomer-cli --print-json project artifacts revise <record-id> revised-reading-list.json --topic my-topic --producer isomer-kaoju-discover
isomer-cli --print-json project artifacts archive <record-id> --topic my-topic --reason superseded
isomer-cli --print-json project artifacts migrate-scope --topic my-topic
```

### `project runs begin/checkpoint/status/complete`

Record one Kaoju procedure attempt and its resumable stage state. A checkpoint carries completed Artifact refs, pending Gate, blockers, Service Requests, and an exact resume hint. Completion seals the Run; later checkpoints are rejected.

**Side effects:** `begin`, `checkpoint`, and `complete` write Research Task and Run lifecycle state through Workspace Runtime. `status` is read-only. Failed, stopped, and cancelled Runs remain durable and can point to a later new attempt.

```bash
isomer-cli --print-json project runs begin --topic my-topic --procedure-id build-reading-list --stage-id discover --id run-reading-1
isomer-cli --print-json project runs checkpoint run-reading-1 --topic my-topic --stage-id approve --completed-ref reading-list-1 --pending-gate-ref gate-reading-1
isomer-cli --print-json project runs status run-reading-1 --topic my-topic
isomer-cli --print-json project runs complete run-reading-1 --topic my-topic --terminal-status complete --completed-ref reading-list-1
```

### `project service-requests create/dispatch/status`

Record a bounded operational support request separately from its Research Task and Run, then dispatch it synchronously. A Service Request names scope, task, expected outputs, authorization, Service Dispatch Form, completion observations, actor refs, and an optional provider-neutral command request. The first release rejects `--no-wait`.

**Side effects:** `create` writes the Service Request. `dispatch` records running and terminal observations, executes an approved command through its Research Operation Extension Point when supplied, and writes a support Artifact. `status` is read-only. Smoke and code-trial requests must use `pixi run --environment <name>` and cannot execute in the ambient environment.

```bash
isomer-cli --print-json project service-requests create \
  --topic my-topic \
  --task-description "Run the task-critical smoke check" \
  --scope-kind run \
  --scope-ref run-env-1 \
  --expected-output-ref KAOJU:SMOKE-RUN-RESULT \
  --authorization "execute the approved named Pixi environment" \
  --dispatch-form tool_native_subagent \
  --completion-observation "task-critical check passes" \
  --command-request-json '{"extension_point":"smoke_run","argv":["pixi","run","--environment","default","--","sh","smoke.sh"]}' \
  --actor-ref project-operator-session:current

isomer-cli --print-json project service-requests dispatch <request-id> --topic my-topic
isomer-cli --print-json project service-requests status <request-id> --topic my-topic
```

### `project topic-actors list/show/register/update/archive/materialize/repair/diagnose`

Manage Topic Actor bindings and Topic Actor Workspaces for human-orchestrated workers. Topic Actor bindings live in the Topic Workspace Manifest, which remains the topology and path-resolution authority. When Workspace Runtime is available, mutating operations may also record audit or provenance rows, but runtime records do not replace manifest topology.

**Side effects:** `list`, `show`, and `diagnose` are read-only. `register`, `update`, and `archive` write `<topic-workspace>/topic-workspace.toml`. `materialize` and `repair` create or reuse the resolved Topic Actor Workspace and support paths, and may create a Git worktree from `topic.repos.main` using `per-topic-actor/<topic-actor-name>/main`. They do not create Agent Team Instance records, Agent Instance records, formal Agent Workspaces, Houmao launch material, or research records.

```bash
isomer-cli --print-json project topic-actors list --topic my-topic
isomer-cli --print-json project topic-actors show operator --topic my-topic
isomer-cli --print-json project topic-actors register operator --topic my-topic --actor-kind operator --runtime-kind human_cli --role-kind operator --controller-kind project_operator_session --materialize
isomer-cli --print-json project topic-actors register claude-scout --topic my-topic --actor-kind manual_worker --runtime-kind claude_code --role-kind scout --controller-kind human_user --materialize
isomer-cli --print-json project topic-actors update claude-scout --topic my-topic --status active
isomer-cli --print-json project topic-actors materialize claude-scout --topic my-topic
isomer-cli --print-json project topic-actors repair claude-scout --topic my-topic
isomer-cli --print-json project topic-actors diagnose --topic my-topic --topic-actor claude-scout
isomer-cli --print-json project topic-actors archive claude-scout --topic my-topic --reason "finished manual scouting"
```

`--source-repo` on materialization must resolve to `topic.repos.main` in this change. Alternate worktree source repositories are rejected instead of accepted as ad hoc topology.

### `schemas list`

List Isomer built-in schemas and contracts.

**Side effects:** none.

```bash
isomer-cli schemas list
isomer-cli --print-json schemas list
```

### `project runtime init`

Initialize or reopen the selected Workspace Runtime.

**Side effects:** creates or reopens the path resolved by `topic.runtime.db`, stores schema metadata, records owner Research Topic and Topic Workspace refs, persists semantic path plans for required runtime labels such as `topic.runtime`, `topic.records`, `topic.records.artifacts`, `topic.records.tasks`, `topic.records.runs`, `topic.records.views`, and `topic.records.logs`, and creates those resolved runtime-owned directories. Reopening a current-schema runtime is idempotent. Unsupported older or newer schemas produce diagnostics and do not create directories or rewrite owner refs.

```bash
isomer-cli --print-json project runtime init --topic my-topic
```

### `project runtime prepare`

Record selected topic environment readiness.

**Side effects:** writes or updates a `TopicEnvironmentReadinessRecord` in Workspace Runtime. Checks explicit Project Manifest `topic_pixi_environment_bindings`, explicit `topic_standalone_pixi_bindings.manifest_path_or_dir` targets, or the implicit registered Topic Workspace directory default when no explicit standalone target exists. Pixi must be installed and on `PATH`; online installation can use `curl -fsSL https://pixi.sh/install.sh | sh`, while offline hosts should receive a pre-downloaded `pixi` executable on `PATH`. Does not install Pixi environments or perform hidden repair.

```bash
isomer-cli --print-json project runtime prepare --topic my-topic
isomer-cli --print-json project runtime prepare --topic my-topic --actor operator
```

### `project runtime inspect`

Inspect Workspace Runtime metadata without mutation.

**Side effects:** none.

```bash
isomer-cli project runtime inspect --topic my-topic
isomer-cli --print-json project runtime inspect --topic my-topic
```

### `project runtime validate`

Validate Workspace Runtime records without mutation.

**Side effects:** none. Reports metadata, record counts, readiness summaries, path-plan mismatches, broken refs, missing Agent Workspace directories, stale handoffs, unresolved Gates, unsupported Research Claims, stale Provenance Records, schema mismatches, and cross-topic leakage.

```bash
isomer-cli project runtime validate --topic my-topic
isomer-cli --print-json project runtime validate --topic my-topic --require-ready-readiness
```

### `project team-instances create`

Create an Agent Team Instance record.

**Side effects:** writes Agent Team Instance record, Agent Instance records, Agent Workspace records, semantic path plans for `agent.workspace` and support labels such as `agent.isomer_managed`, `agent.private_artifacts`, `agent.runtime`, `agent.scratch`, `agent.public_share`, and `agent.links`, initial Workflow Stage Cursor records, and provenance refs, and materializes the resolved Agent Workspace directories. Each Agent Workspace is expected to be the agent's launch cwd and, for Git-backed topics, a worktree of `topic.repos.main` on an agent-owned branch. Does not launch Houmao agents, create mailboxes, write launch dossiers, or store adapter-specific launch refs.

**Prerequisites:** Workspace Runtime must be initialized, the Research Topic's single Topic Agent Team Profile Bundle must be materialized, and readiness should be `ready` for launch-facing work.

```bash
isomer-cli --print-json project team-instances create \
  --topic my-topic \
  --id ati-my-topic-deepsci
```

### `project team-instances list`

List Agent Team Instance records.

**Side effects:** none.

```bash
isomer-cli project team-instances list --topic my-topic
isomer-cli --print-json project team-instances list --topic my-topic
```

### `project team-instances show`

Show one Agent Team Instance record.

**Side effects:** none.

```bash
isomer-cli --print-json project team-instances show ati-my-topic-deepsci --topic my-topic
```

### `project team-instances adapter-link export`

Write or print a Houmao adapter link JSON manifest.

**Side effects:** writes `adapter-link.json` under the Topic Workspace adapter directory unless `--print` is used. Does not launch agents.

```bash
isomer-cli --print-json project team-instances adapter-link export ati-my-topic-deepsci --topic my-topic
isomer-cli --print-json project team-instances adapter-link export ati-my-topic-deepsci --topic my-topic --print
```

### `project team-instances launch-material prepare`

Prepare Houmao launch material without launching agents.

**Side effects:** writes shared launch material, creates or updates `adapter-link.json` and `launch-material-manifest.json`, and records materialization state in Workspace Runtime. Does not launch, stop, message, or inspect Houmao managed agents.

```bash
isomer-cli --print-json project team-instances launch-material prepare ati-my-topic-deepsci \
  --topic my-topic --adapter houmao
```

### `project team-instances launch`

Quick-launch a Houmao-backed Agent Team Instance.

**Side effects:** runs preflight, writes shared launch material, creates or updates `adapter-link.json` and `launch-material-manifest.json`, launches one Houmao managed agent per Isomer Agent Instance, writes `adapter-runtime-manifest.json`, and records command runs, payload refs, a launch attempt, and reconciliation state in Workspace Runtime. This is a live mutation of external Houmao state.

```bash
isomer-cli --print-json project team-instances launch ati-my-topic-deepsci \
  --topic my-topic --adapter houmao
```

### `project team-instances inspect-live`

Inspect Houmao adapter manifest integrity without mutation.

**Side effects:** none. Runs read-only Houmao CLI inspection and records a bounded adapter inspection snapshot in Workspace Runtime. The snapshot is a durable record of the observation; the underlying Houmao state is not modified.

```bash
isomer-cli --print-json project team-instances inspect-live ati-my-topic-deepsci \
  --topic my-topic --adapter houmao --integrity
```

### `project team-instances stop`

Stop a Houmao-backed Agent Team Instance.

**Side effects:** an explicit live mutation. Targets known mapped Houmao agent names from manifests or launch attempts and records a stopped, partial, failed, or stale outcome in Workspace Runtime.

```bash
isomer-cli --print-json project team-instances stop ati-my-topic-deepsci \
  --topic my-topic --adapter houmao
```

### `project team-instances reconcile`

Record Houmao adapter manifest reconciliation state.

**Side effects:** writes or updates `adapter-runtime-manifest.json` and records an `AdapterReconciliationRecord` in Workspace Runtime. Does not start, stop, or message Houmao-managed agents.

```bash
isomer-cli --print-json project team-instances reconcile ati-my-topic-deepsci \
  --topic my-topic
```

### `project team-instances adopt`

Adopt externally launched Houmao runtime state.

**Side effects:** records an explicit decision to associate externally launched Houmao runtime state with the selected Agent Team Instance. Requires `--yes` to confirm.

```bash
isomer-cli --print-json project team-instances adopt ati-my-topic-deepsci \
  --topic my-topic --yes
```

### `project handoffs dispatch`

Dispatch a manual handoff through the selected Execution Adapter.

**Side effects:** writes or reuses a Run lifecycle record, writes a Handoff record, links the handoff and Run to the Agent Team Instance, writes durable handoff payload files, invokes Houmao mail dispatch for the Houmao adapter, and records adapter command and payload refs. Requires ready Workspace Runtime and a launched, adopted, or linked adapter context.

```bash
isomer-cli --print-json project handoffs dispatch \
  --topic my-topic \
  --agent-team-instance ati-my-topic-deepsci \
  --source-agent-instance ati-my-topic-deepsci-deepsci-org-master \
  --target-agent-instance ati-my-topic-deepsci-deepsci-org-experimenter \
  --run run-default-first-handoff \
  --message "Draft the first experiment execution plan." \
  --expected-output artifact:default:first-handoff
```

### `project handoffs observe`

Record a non-authoritative Signal Observation for a handoff.

**Side effects:** writes a Signal Observation record, durable observation payload files, and any adapter command/payload refs needed to read mail or gateway output. Observation alone does not complete a Run, accept a handoff, promote returned claims into Evidence Items, or accept an Artifact.

```bash
isomer-cli --print-json project handoffs observe <handoff-id> --topic my-topic --source mail
isomer-cli --print-json project handoffs observe <handoff-id> --topic my-topic --source gateway
isomer-cli --print-json project handoffs observe <handoff-id> --topic my-topic --source file --payload-json handoff-observation.json
isomer-cli --print-json project handoffs observe <handoff-id> --topic my-topic --source inspection
```

### `project handoffs normalize`

Record the Operator Agent decision for a handoff result.

**Side effects:** writes a handoff normalization record and payload ref, updates the Handoff record, records output Artifact lifecycle refs when supplied, and completes the linked Run only for `accepted`. Supported statuses are `accepted`, `rejected`, `blocked`, `superseded`, `repair_routed`, and `follow_up`.

```bash
isomer-cli --print-json project handoffs normalize <handoff-id> \
  --topic my-topic \
  --status accepted \
  --signal-observation <signal-observation-id> \
  --output-artifact artifact:default:first-handoff \
  --rationale "Accepted after Operator review."
```

### `ext kaoju paper template` and Paper Derivation Commands

`ext kaoju paper template` owns two independent mutable named namespaces. `--kind content` selects `KAOJU:PAPER-TEMPLATE-MYST`, which defines canonical MyST authoring structure. `--kind latex` selects `KAOJU:PAPER-TEMPLATE-LATEX`, which stores multi-file presentation bundles. Each namespace has its own `main`. Every path-safe role-local name maps to one stable record, managed directory tree, opaque state token, tree digest, bounded authored metadata, and kind-qualified mutation audit. Omitting `--kind` selects content only for compatibility; new automation should pass the role explicitly.

`template list` and `show` are read-only. `create` accepts `--from PATH` or a same-role `--from-template NAME`; omitted names use role-local `main`. `update`, `file put`, `file remove`, `metadata patch`, `archive`, and `delete` require the current `--expected-state` token. A registered edited export can be passed directly to `update`; the service verifies its kind, stable ref, and source token before stripping reserved export metadata. LaTeX metadata requires a safe `.tex` entrypoint and `extensions.latex` with `composition_mode`, registered `build_profile`, `source_provenance`, and `license_posture`. Preamble mode may declare `generated_entrypoint`; marker mode requires `marker`; include mode requires `body_path`.

`template export --kind content` defaults to `<exchange-root>/content/main/`; `--kind latex` defaults to `<exchange-root>/latex/main/`. Reserved `.isomer-template-export.json` records the kind, name, stable ref, token, digests, path, actor, and time. Clean recognized targets refresh in place; edited or unrecognized targets are preserved. `template exports --kind KIND` reports only that role's `unchanged`, `edited`, `missing`, `identity-invalid`, or `canonical-changed` working copies. `--observe --target PATH` records an assessed tree without promoting it.

The Kaoju agent resolves content versus LaTeX role before discovery. With no source locator, it uses exactly one edited export of that role, asks when several role-local candidates qualify, otherwise checks `<exchange-root>/<kind>/main/`, then asks for a source. It never selects the other role's same-named record or export.

`template migrate --kind content` previews existing records and legacy export paths; `--apply` annotates old named content records without changing stable refs, state tokens, or tree bytes. `template migrate --kind latex` reports historical TeX candidates. Adoption requires `--apply --record EXACT_REF --metadata-file FILE`, copies the selected tree into LaTeX stock, and leaves the source record unchanged. Replacing existing stock also requires `--expected-state`. The retired `paper export-template`, `paper apply-template`, and legacy `ext research templates` mutation surfaces remain non-mutating.

`paper validate` checks canonical MyST. `derive-markdown` creates a non-canonical review view. `init-tex` takes an exact content-template ref and an explicit LaTeX selector or default LaTeX `main`, snapshots the complete presentation tree, and composes a self-contained TeX draft through preamble, marker, or include mode. `tex-status` reports stocked-template and paper-local repair drift. `build-pdf` verifies the pinned snapshot, uses the declared entrypoint and build profile, executes `document_build`, and records the Run, compile log, drift, PDF inspection, and publication Gate.

```bash
isomer-cli --print-json ext kaoju paper template list --topic my-topic --kind content
isomer-cli --print-json ext kaoju paper template create --topic my-topic --kind content --from prepared-content-template --actor agent:writer
isomer-cli --print-json ext kaoju paper template create --topic my-topic --kind latex --from publisher-template --metadata-file latex-template.json --actor agent:writer
isomer-cli --print-json ext kaoju paper template show --topic my-topic --kind latex
isomer-cli --print-json ext kaoju paper template export --topic my-topic --kind latex --actor agent:writer
isomer-cli --print-json ext kaoju paper template exports --topic my-topic --kind latex
isomer-cli --print-json ext kaoju paper template update --topic my-topic --kind latex --from topic-workspace/intent/derived/writing-template/latex/main --expected-state template-state-... --actor agent:writer
isomer-cli --print-json ext kaoju paper template file put --topic my-topic --kind latex --path sections/method.tex --from updated-method.tex --expected-state template-state-... --actor agent:writer
isomer-cli --print-json ext kaoju paper template file remove --topic my-topic --kind latex --path sections/obsolete.tex --expected-state template-state-... --actor agent:writer
isomer-cli --print-json ext kaoju paper template create --topic my-topic --kind content --name main-before-change --from-template main --actor agent:writer
isomer-cli --print-json ext kaoju paper template metadata patch --topic my-topic --kind latex --patch-file latex-template.json --expected-state template-state-... --actor agent:writer
isomer-cli --print-json ext kaoju paper template archive --topic my-topic --kind latex --name old-publisher --expected-state template-state-... --actor agent:writer --reason superseded
isomer-cli --print-json ext kaoju paper template delete --topic my-topic --kind latex --name old-publisher --expected-state template-state-... --actor agent:writer
isomer-cli --print-json ext kaoju paper template migrate --topic my-topic --kind content
isomer-cli --print-json ext kaoju paper template migrate --topic my-topic --kind latex --apply --record paper-tex-template-2 --metadata-file latex-template.json --actor agent:writer

isomer-cli --print-json ext kaoju paper validate --topic my-topic prepared-template/paper/index.md
isomer-cli --print-json ext kaoju paper derive-markdown --topic my-topic --source-ref paper-draft-3 --paper-line paper:main
isomer-cli --print-json ext kaoju paper init-tex --topic my-topic --draft-ref paper-draft-3 --content-template-ref artifact-paper-template-myst-main --latex-template-name main --paper-line paper:main
isomer-cli --print-json ext kaoju paper tex-status --topic my-topic --draft-tex-ref paper-tex-draft-3
isomer-cli --print-json ext kaoju paper build-pdf --topic my-topic --draft-tex-ref paper-tex-draft-3 --template-tex-ref paper-tex-template-2 --paper-line paper:main --audit-ref paper-audit-4 --inspected --pdf-inspected

# Retired commands return paper_template_command_retired without mutation.
isomer-cli --print-json ext kaoju paper export-template --topic my-topic --source-ref paper-structure-1 --paper-line paper:main --draft-ref paper-draft-3 --citation-map-ref citation-map-1
isomer-cli --print-json ext kaoju paper apply-template --topic my-topic old-template-export
```

### `ext kaoju process show` and `ext kaoju bindings list/describe`

Inspect the installed Kaoju process and shared artifact contracts without resolving a Project or Topic Workspace. `process show` returns versioned process data and logical binding-query metadata. `bindings list` returns canonical-identifier-sorted summaries, and `bindings describe` joins storage-neutral meaning with the checked storage binding.

**Side effects:** none. These commands return `mutated: false` and accept only exact uppercase `KAOJU:WHAT` identifiers. They do not read skill-family paths or apply aliases.

```bash
isomer-cli --print-json ext kaoju process show
isomer-cli --print-json ext kaoju bindings list
isomer-cli --print-json ext kaoju bindings describe KAOJU:SURVEY-CONTRACT
```

### `ext kaoju wiki export/deploy/start`

Export accepted state-DB Artifacts to an idempotent Markdown and canonical JSON wiki, deploy the independently implemented package-owned viewer, or launch a recognized deployment. Selection can use explicit Artifact refs or accepted direction and paper scopes. Default targets resolve inside the Topic Workspace; actor paths remain authorized external targets.

**Side effects:** `export` and `deploy` stage recognized managed-file updates, preserve unrecognized human files, write changelogs and checksummed directory manifests, and register wiki or viewer Artifacts. `start` uses the `viewer_launch` extension point, records a Run and log, binds to loopback by default, and requires a network-exposure Gate for non-loopback hosts. These commands use installed package resources and never invoke an external `imsight-llm-wiki` skill.

```bash
isomer-cli --print-json ext kaoju wiki export --topic my-topic --direction-scope direction:memory-offload
isomer-cli --print-json ext kaoju wiki deploy --topic my-topic topic-workspaces/my-topic/exports/kaoju-wiki
isomer-cli --print-json ext kaoju wiki start --topic my-topic topic-workspaces/my-topic/exports/kaoju-viewer
```

### `ext deepsci tools`

List the DeepScientist compatibility tools exposed through Isomer extension shims.

**Side effects:** none.

```bash
isomer-cli ext deepsci tools
isomer-cli ext deepsci tools artifact
```

### `ext deepsci call`

Call one DeepScientist compatibility tool against the selected Topic Workspace.

**Side effects:** depends on the tool. Compatibility calls may write extension-owned records inside the Workspace Runtime database and may return durable references that later production DeepSci skills summarize through canonical `DEEPSCI:WHAT` bindings. Use this surface only for source-shaped compatibility behavior while the native research record APIs are still incomplete.

```bash
isomer-cli ext deepsci call artifact.record \
  --topic my-topic \
  --input-json '{"title":"Draft note","body":"Compatibility note."}'
```

### `ext research records create/show/list/update/revise/delete`

Create, inspect, query, revise, or archive topic-scoped research records with canonical extension artifact identifiers.

**Side effects:** `create` and `update` write or update a Workspace Runtime lifecycle record and, when `--body` or `--body-file` is supplied, write a durable body under the resolved semantic label, defaulting to `topic.records.artifacts` except for runs, tasks, and views. `delete` archives the lifecycle record by setting its status to `archived`; it does not remove stored body files. `show` and `list` are read-only.

**Use:** Kaoju work uses `project artifacts`, which resolves the packaged registry and infers physical fields. DeepSci record operations pass exact uppercase `DEEPSCI:WHAT` values through `--semantic-id`. Structured creation uses an explicit format profile and payload file and rejects direct `--body` or `--body-file` authoring.

When a Topic Actor creates or updates an accepted research record, include `--topic-actor <topic-actor-name>` and known actor metadata such as `--actor-kind`, `--runtime-kind`, `--controller-kind`, and `--adapter-ref`. Include formal Agent Team Instance, Agent Instance, or Agent Workspace refs only when the record was actually produced inside that formal context; do not fabricate those refs for Topic Actor work.

```bash
isomer-cli --print-json ext research records create \
  --topic my-topic \
  --record-kind artifact \
  --semantic-id DEEPSCI:LITERATURE-SCOUTING-REPORT \
  --format-profile isomer:deepsci/record-format/profile/report/literature-scouting-report/v2 \
  --skill isomer-deepsci-scout \
  --producer isomer-deepsci-scout \
  --consumer isomer-deepsci-idea \
  --topic-actor claude-scout \
  --actor-kind manual_worker \
  --runtime-kind claude_code \
  --controller-kind human_user \
  --payload-file scouting-report.json

isomer-cli --print-json ext research records list \
  --topic my-topic \
  --semantic-id DEEPSCI:LITERATURE-SCOUTING-REPORT

isomer-cli --print-json ext research records show <record-id> \
  --topic my-topic --include-body

isomer-cli --print-json ext research records update <record-id> \
  --topic my-topic \
  --record-kind artifact \
  --status complete \
  --semantic-id DEEPSCI:LITERATURE-SCOUTING-REPORT \
  --format-profile isomer:deepsci/record-format/profile/report/literature-scouting-report/v2 \
  --payload-file scouting-report.json

isomer-cli --print-json ext research records delete <record-id> \
  --topic my-topic \
  --reason superseded
```

Neutral list and query filters compose:

```bash
isomer-cli --print-json ext research records list \
  --topic my-topic --semantic-id KAOJU:SURVEY-CONTRACT

isomer-cli --print-json ext research records query list \
  --topic my-topic \
  --artifact-family kaoju \
  --semantic-id KAOJU:RELATED-WORK-CATALOG \
  --procedure landscape-pass \
  --latest-only
```

`--latest-only` follows explicit revision and supersession links and reports competing current candidates. `show --include-payload` reads canonical JSON, `render` produces an on-demand readable view, and `render --output-file` creates an explicit export without changing latest state.

### `ext research operation-sets inspect/accept/verify`

Inventory one Topic Actor or Agent operation set, preview and apply an exhaustive durable-record plan, and verify its receipt. See [Operation Set Acceptance](operation-set-acceptance.md) for the manifest and recovery contract.

**Side effects:** `inspect` is read-only unless `--write-scaffold` is present. `accept` is read-only by default; `accept --apply` creates or revises records through the existing record service, copies managed attachments, applies authored Research Idea effects atomically with their record, and writes acceptance receipt progress. `verify` is read-only and never repairs state.

```bash
isomer-cli --print-json ext research operation-sets inspect <operation-set-path> \
  --topic my-topic --topic-actor researcher

isomer-cli --print-json ext research operation-sets accept <manifest-path> \
  --topic my-topic --topic-actor researcher

isomer-cli --print-json ext research operation-sets accept <manifest-path> \
  --topic my-topic --topic-actor researcher --apply

isomer-cli --print-json ext research operation-sets verify <receipt-or-operation-set-id> \
  --topic my-topic
```

Use exactly one of `--topic-actor` and `--agent` when inference is ambiguous. `inspect --write-scaffold` never overwrites an existing manifest. A successful preview is not completion; require apply to return a complete receipt and verify to succeed.

### `ext research templates create/list/show/refresh/compile/remove`

Inspect legacy non-canonical LaTeX writing-template records that predate mutable named MyST trees. `list` and `show` remain read-only. `create`, `refresh`, `compile`, and `remove` return `legacy_template_mutation_disabled` plus named Kaoju CRUD, migration, or agentic reconciliation guidance and do not write `intent/derived/writing-template`.

**Side effects:** none for `list`, `show`, or disabled mutation commands. Use generic record reads for historical payload and lineage access.

```bash
isomer-cli --print-json ext research templates create --name main
isomer-cli --print-json ext research templates list
isomer-cli --print-json ext research templates show --name main
isomer-cli --print-json ext research templates refresh --name main
isomer-cli --print-json ext research templates compile --name main
isomer-cli --print-json ext research templates remove --name main
```

### Structured Error Examples

These intentionally incomplete or invalid invocations exercise the CLI's command-specific structured error guidance:

```bash
isomer-cli --print-json ext research ideas list --topic my-topic
isomer-cli --print-json ext research ideas graph --topic my-topic
isomer-cli --print-json ext research ideas validate --topic my-topic
isomer-cli --print-json ext kaoju paper template show --topic my-topic --kind latex --name main
isomer-cli --print-json ext kaoju paper template export --topic my-topic --kind latex --name main --actor agent:writer
isomer-cli --print-json ext research records list --topic my-topic
isomer-cli --print-json ext research records show <record-id> --topic my-topic
isomer-cli --print-json ext research records create --topic my-topic --record-kind artifact
```

### UC-01 Manual Harness

UC-01 is intentionally not a product CLI command. From a source checkout, run the pinned acceptance path from the manual harness so case-specific ids, fixture output specs, simulated handoff payloads, summaries, and closeout assertions stay outside `src/isomer_labs`.

```bash
pixi run python tests/manual/uc01_headless_vertical_slice
ISOMER_MANUAL_LIVE_HOUMAO=1 pixi run python tests/manual/uc01_headless_vertical_slice --live-houmao
```

### `project team-templates list`

List registered Domain Agent Team Templates.

**Side effects:** none.

```bash
isomer-cli project team-templates list
isomer-cli --print-json project team-templates list
```

### `project team-templates inspect`

Inspect a registered Domain Agent Team Template.

**Side effects:** none. The output includes template roles, Workflow Stage ownership, placeholder catalog entries, instantiation schema paths, and copyable material declarations such as `execplan/` for templates that support Topic Team Specialization.

```bash
isomer-cli --print-json project team-templates inspect deepsci-org
```

### `project team-templates validate`

Validate a registered Domain Agent Team Template.

**Side effects:** none.

```bash
isomer-cli project team-templates validate deepsci-org
isomer-cli project --root /path/to/project team-templates validate fixture-method-team
```

### `project team-profiles specialize`

Preview Topic Team Specialization for the selected Research Topic by deriving a candidate Topic Agent Team Profile.

**Side effects:** by default, prints preview or candidate material without writing files. `--profile-id` is preview-only and is not accepted by the packet-backed authoritative materialization path. Legacy preview-write behavior may write a single profile file, but authoritative Topic Team Specialization writes the Research Topic's one Topic Agent Team Profile Bundle under `team-profile/` in the owning Topic Workspace and keeps only the Project Manifest ref in Project Config. Does not launch Houmao agents, create an Agent Team Instance, or write Workspace Runtime state.

```bash
isomer-cli --print-json project team-profiles specialize \
  --topic my-topic --use-case UC-01
isomer-cli --print-json project team-profiles specialize \
  --topic my-topic --use-case UC-01 --write
```

### `project team-profiles materialize`

Materialize an approved packet-backed Topic Agent Team Profile Bundle for the selected Research Topic.

**Side effects:** without `--write`, previews validation and planned bundle paths. With `--write`, writes `<topic-workspace>/team-profile/profile.toml`, `instantiation-packet.toml`, `approval.toml`, validation output, provenance files, and copied topic-edited template material. It does not mutate Workspace Runtime, launch Houmao agents, or create an Agent Team Instance.

```bash
isomer-cli --print-json project team-profiles materialize \
  --topic flash-attention-gb10-peak-performance-optimization \
  --packet fixtures/uc01/topic-team-instantiation-packet.toml
isomer-cli --print-json project team-profiles materialize \
  --topic flash-attention-gb10-peak-performance-optimization \
  --packet fixtures/uc01/topic-team-instantiation-packet.toml --write
```

### `project team-profiles validate`

Validate a Topic Agent Team Profile file or a `profile.toml` file inside a Topic Agent Team Profile Bundle.

**Side effects:** none.

```bash
isomer-cli project team-profiles validate isomer-content/topic-ws/my-topic/team-profile/profile.toml
isomer-cli project --root /path/to/project team-profiles validate topic-workspaces/my-topic/team-profile/profile.toml
```

## Research Idea Portfolio Commands

`ext research ideas upsert` records stable canonical identity and initial exploration, decision, evidence, archive, and visibility facets. `transition` performs an expected-state mutation with actor, rationale, operation correlation, and applicable Decision Record, Gate, Evidence Item, Artifact, Finding, Research Task, Run, or Provenance Record refs. Closing requires a canonical reason code.

`decision-options upsert` records explicit Decision Record membership and outcome. `generation upsert` records one production pass; generation membership never substitutes for decision membership. `lineage add` records a canonical Idea Lineage Edge independently of research-record lineage.

`query`, `graph`, `decision-context`, `traverse`, and `validate` are read-only. `query` supports repeatable facet filters plus generation, Decision Record, archive, and visibility selection. `traverse` requires roots and `ancestors` or `descendants`, and accepts relation, depth, node, and edge bounds. Results label incomplete traversal.

`migrate-status` and `migrate-kaoju-direction-set <record-id>` preview by default and mutate only with `--apply`. Preview preserves current data. Kaoju migration preserves direction ids as aliases and never invents disposition reasons or lineage.

`steer` is the explicit composite mutation for `--action explore` or `--action explore-instead`. It requires target identity, actor, and idempotency key. Explore-instead also requires repeatable `--replace-idea-id` and rationale. Expected revision, expected facets, replacement dispositions, closure reasons, reopening confirmation, Gate policy, adapter routing, prompt, and `--no-dispatch` are available for deterministic operator workflows. See [Research Idea Portfolio](research-idea-portfolio.md) for examples and semantics.

```bash
isomer-cli --print-json ext research ideas decision-context --topic my-topic --idea-id idea-1
isomer-cli --print-json ext research ideas decision-options upsert --topic my-topic --decision-record-id decision-1 --idea-id idea-1 --outcome selected --actor agent:reviewer
isomer-cli --print-json ext research ideas migrate-kaoju-direction-set --topic my-topic direction-set-1
isomer-cli --print-json ext research ideas transition --topic my-topic idea-1 --facet exploration_state --expected-from proposed --to exploring --actor agent:researcher --rationale "Begin the accepted direction."
isomer-cli --print-json ext research ideas traverse --topic my-topic --root-idea-id idea-1 --direction descendants
```

## Side-effect Summary

| Command | Mutates Project files | Mutates Workspace Runtime | Mutates adapter files | Mutates live Houmao state |
|---|---|---|---|---|
| `project init` | yes (`.isomer-labs/`, `.isomer-labs/.houmao/`, content root policy files) | no | no | no |
| `doctor` | no | no | no | no |
| `project validate` | no | no | no | no |
| `project topics list` | no | no | no | no |
| `project topics create` | yes (topic config, manifest, workspace dir) | no | no | no |
| `project topics show` | no | no | no | no |
| `project topics update` | yes (manifest or topic config) | no | no | no |
| `project topics delete` | yes with `--yes`; `--dry-run` is read-only | no | no | no |
| `project workspaces list` | no | no | no | no |
| `project context show` | no | no | no | no |
| `project self show/identity/pixi/env/paths/queries` | no | no | no | no |
| `project outputs policy` | no | no | no | no |
| `project paths preview` | no | no | no | no |
| `project paths default` | no | no | no | no |
| `project paths explain` | no | no | no | no |
| `project paths get` | no | no | no | no |
| `project paths list` | no | no | no | no |
| `project paths materialize-default` | yes (`topic-workspace.toml`, selected default dirs) | no | no | no |
| `project paths materialize` | yes (configured target dirs or file parents) | no | no | no |
| `project paths register` | yes (`topic-workspace.toml`, optional target dirs) | no | no | no |
| `project paths update` | yes (`topic-workspace.toml`, optional target dirs) | no | no | no |
| `project paths unregister` | yes (`topic-workspace.toml` only) | no | no | no |
| `project paths reset` | yes (`topic-workspace.toml` only) | no | no | no |
| `project repos create` | yes (`topic-workspace.toml`, optional repository target dir) | no | no | no |
| `project repos register` | yes for a new binding (`topic-workspace.toml` only) | no | no | no |
| `project topic-actors list/show/diagnose` | no | no | no | no |
| `project topic-actors register/update/archive` | yes (`topic-workspace.toml`) | yes when runtime audit is available | no | no |
| `project topic-actors materialize/repair` | yes (Topic Actor Workspace dirs or worktree) | yes when runtime audit is available | no | no |
| `schemas list` | no | no | no | no |
| `project runtime init` | yes (dirs, sqlite) | yes | no | no |
| `project runtime prepare` | no | yes | no | no |
| `project runtime inspect` | no | no | no | no |
| `project runtime validate` | no | no | no | no |
| `project team-instances create` | yes (dirs) | yes | no | no |
| `project team-instances list` | no | no | no | no |
| `project team-instances show` | no | no | no | no |
| `project team-instances adapter-link export` | yes (manifest) | yes (ref) | yes | no |
| `project team-instances launch-material prepare` | yes (material) | yes | yes | no |
| `project team-instances launch` | yes (material, manifests) | yes | yes | yes |
| `project team-instances inspect-live` | no | yes (snapshot) | no | no |
| `project team-instances stop` | no | yes (outcome) | no | yes |
| `project team-instances reconcile` | no | yes | yes (runtime manifest) | no |
| `project team-instances adopt` | no | yes | no | no |
| `project handoffs dispatch` | no | yes | yes (handoff payloads) | yes |
| `project handoffs observe` | no | yes | yes (observation payloads) | mail/gateway only |
| `project handoffs normalize` | no | yes | yes (normalization payloads) | no |
| `ext deepsci call` | no | tool-dependent | no | no |
| `ext deepsci tools` | no | no | no | no |
| `ext research records create` | yes with body files | yes | no | no |
| `ext research records show` | no | no | no | no |
| `ext research records list` | no | no | no | no |
| `ext research records update` | yes with body files | yes | no | no |
| `ext research records delete` | no | yes (archives record) | no | no |
| `ext research operation-sets inspect` | only with `--write-scaffold` | no | no | no |
| `ext research operation-sets accept` | no | no | no | no |
| `ext research operation-sets accept --apply` | yes (managed record files) | yes | no | no |
| `ext research operation-sets verify` | no | no | no | no |
| `ext research ideas query/graph/decision-context/traverse/validate` | no | no | no | no |
| `ext research ideas upsert/realize/generation/lineage/transition/decision-options` | no | yes | no | no |
| `ext research ideas migrate-status/migrate-kaoju-direction-set` | no in preview; no Project files on apply | only with `--apply` | no | no |
| `ext research ideas steer --no-dispatch` | no | yes | no | no |
| `ext research ideas steer` | no | yes | yes when a route is available | yes when a route is available |
| `project team-templates list` | no | no | no | no |
| `project team-templates inspect` | no | no | no | no |
| `project team-templates validate` | no | no | no | no |
| `project team-profiles specialize` | only with `--write` | no | no | no |
| `project team-profiles materialize` | yes with `--write` | no | no | no |
| `project team-profiles validate` | no | no | no | no |

## Environment Variables

- `ISOMER_HOUMAO_COMMAND` — override the `houmao-mgr` executable path used by the Houmao adapter.
- `ISOMER_HOUMAO_CHECKOUT` — override the local Houmao checkout path used when `houmao-mgr` is not on `PATH`.
- `ISOMER_AGENT_NAME`, `ISOMER_AGENT_INSTANCE_ID`, and `ISOMER_AGENT_WORKSPACE_DIR` — optional agent-context inputs for agent-scoped semantic path queries. Explicit CLI selectors win over environment context.
- `ISOMER_PATH__TOPIC__REPOS__MAIN`, `ISOMER_PATH__CUSTOM__DATASETS__RAW`, and other generated `ISOMER_PATH__...` variables — semantic path overrides derived from dotted labels. A generated variable for `custom.*` applies only after that custom label exists in the effective catalog.
- `ISOMER_TOPIC_WORKSPACE_RUNTIME_DB`, `ISOMER_TOPIC_WORKSPACE_RECORDS_DIR`, `ISOMER_TOPIC_WORKSPACE_ARTIFACTS_DIR`, and related `ISOMER_TOPIC_WORKSPACE_*` path variables — compatibility path overrides used by Workspace Path Resolution before manifest/default bindings. Prefer semantic labels in new docs and scripts.

If `houmao-mgr` is not on `PATH`, the adapter falls back to `extern/orphan/houmao`, then `ISOMER_HOUMAO_CHECKOUT`, then `~/workspace/code/houmao`.
