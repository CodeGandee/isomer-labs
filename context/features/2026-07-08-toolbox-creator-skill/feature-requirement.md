# Toolbox Creator Skill Feature Requirement

## Goal

Create an Isomer skill that teaches an agent how to create, install, inspect, update, and remove project-local Toolboxes using the canonical Toolbox language and CLI surface. The skill should help a Project Operator Session turn a reusable instruction package idea into a valid `skillset/toolboxes/<toolbox-id>/` tree, install its callbacks and registration through `isomer-cli`, and manage its runtime params across Project Manifest and Topic Workspace Manifest layers.

The first useful version should behave as a practical operating manual for Toolbox work. It should guide agents through choosing a stable `toolbox_id`, writing `manifest.toml`, creating callback skill directories or prompt files, defining runtime param defaults, validating the Toolbox, installing it at project or topic scope, and explaining effective state without falling back to obsolete extension-package terminology.

## Non-Goals

- Do not implement a new Toolbox marketplace, remote registry, package downloader, or dependency resolver.
- Do not change the Toolbox manifest schema, Project Manifest schema, Topic Workspace Manifest schema, or callback registry format as part of the skill itself.
- Do not make the skill install or execute arbitrary external code; Toolbox callback material remains supplemental instruction material.
- Do not let the skill bypass `isomer-cli` validation, OpenSpec requirements, User Skill Callback precedence rules, secret scanning, or path safety checks.
- Do not make a generated Toolbox project-global by default when the user asked for topic-scoped or topic-agent-specific behavior.
- Do not teach old command groups, table names, schema versions, or identity fields as migration aliases.

## Users And Workflows

- Project Operator Session: invokes the skill to create a new Toolbox, install an existing Toolbox, update Toolbox status or source path, define runtime params, inspect effective state, and troubleshoot validation diagnostics.
- Skill authoring agent: follows the skill to produce Toolbox source material with a valid manifest, README, callback skill directories, prompt files, and optional runtime param defaults.
- Research agent: benefits from installed Toolbox callbacks during begin or end callback resolution, but does not treat the Toolbox as a higher-priority system skill.
- Project reviewer: uses the skill's checklist to verify that a Toolbox is safe, scoped correctly, and free of credentials or topic-private material before installation.

Primary creation workflow:

1. The user asks the Project Operator Session to create a Toolbox for a reusable behavior, domain preference, or callback bundle.
2. The skill asks for or derives the Toolbox purpose, target system skills, begin or end stages, desired scope, optional runtime params, and whether any topic-specific specialization is needed.
3. The agent creates `skillset/toolboxes/<toolbox-id>/manifest.toml`, a README, callback skill directories with `SKILL.md`, optional prompt files, and optional runtime param bundle files.
4. The agent validates the Toolbox manifest and source paths before installing it.
5. The agent installs callbacks or a Toolbox registration through `isomer-cli`, then reports callback ids, registration scope, source path, runtime params, and validation diagnostics.

Primary management workflow:

1. The user asks to list, show, explain, enable, disable, update-source, uninstall, or validate a Toolbox.
2. The skill selects the correct CLI command group: `project toolboxes`, `project skill-callbacks`, or `project toolbox-params`.
3. The agent chooses Project, Research Topic, Topic Actor, or Topic Agent scope from explicit user context and refuses to guess a narrower scope when that would change behavior broadly.
4. The agent runs or proposes the appropriate command, then summarizes effective Toolbox status, gated callbacks, runtime param resolution, and any diagnostics.

## Functional Requirements

- The skill shall define Toolbox as a project-local extension package with a durable `toolbox_id`, source path, callback material, and optional runtime param defaults.
- The skill shall teach the canonical source layout under `skillset/toolboxes/<toolbox-id>/`, including `manifest.toml`, `README.md`, callback skill directories, prompt files, and optional default param bundle TOML files.
- The skill shall require Toolbox manifests to use `schema_version = "isomer-toolbox.v1"`, `kind = "toolbox-callback-bundle"`, and `toolbox_id`.
- The skill shall explain that callback ids installed from a Toolbox use `<toolbox_id>:<toolbox-local-key>`, while callback entries inside the manifest use toolbox-local `key` values.
- The skill shall teach the difference between `project skill-callbacks install --toolbox-dir <path>` and `project toolboxes install --toolbox-dir <path>`: callback install writes callback records and ensures registration, while Toolbox install manages parent registration.
- The skill shall document the management commands for `project toolboxes`: install, list, show, explain, enable, disable, update-source, uninstall, and validate.
- The skill shall document the runtime param commands for `project toolbox-params`: define, set, get, list, explain, unset, validate, import add, import list, import show, and import remove.
- The skill shall explain effective runtime param resolution order: Project Manifest imports, Project Manifest explicit rows, Topic Workspace Manifest imports, then Topic Workspace Manifest explicit rows.
- The skill shall teach that Project-scope Toolbox rows use Project Manifest scope, while topic-scope rows live in the Topic Workspace Manifest and may specialize by `research_topic`, `topic_actor`, or `topic_agent`.
- The skill shall use `--topic-agent` as the canonical topic-agent selector and treat `topic_agent_name` as topic-local Effective Agent Context Agent Name.
- The skill shall include validation guidance for duplicate callback keys, invalid source paths, missing `SKILL.md`, old schema fields, secret-like material, unsupported import-file content, and missing Toolbox registration.
- The skill shall teach agents to keep callback instructions supplemental to system instructions, developer instructions, owning system skill rules, current user requests, evidence Gates, validation, and recording obligations.
- The skill shall provide a creation checklist for new Toolboxes: purpose, audience, target skills, stage map, scope recommendation, source files, runtime params, default bundles, README, validation, install command, and rollback command.
- The skill shall provide management playbooks for common tasks: install for one topic, install project-wide, disable for one Topic Agent, update source path after moving a Toolbox, import default params, override one param for one Topic Agent, inspect gated callbacks, and uninstall a selected scope.
- The skill shall avoid teaching obsolete command groups, table names, schema names, or identity fields except when warning that validation rejects them.
- The skill shall include examples based on `gpu-analytical-modeling` only as an example Toolbox, not as the required shape for every Toolbox.

## System Boundaries

- In scope: one Isomer skill that instructs agents how to author Toolbox files, call existing `isomer-cli` Toolbox commands, reason about scope, and troubleshoot diagnostics.
- In scope: examples and checklists for valid Toolbox manifests, callback entries, runtime param rows, runtime param imports, and installed callback behavior.
- In scope: safe project-local filesystem edits under `skillset/toolboxes/` and manifest mutations through existing CLI commands when the user asks the agent to execute them.
- Out of scope: adding new CLI commands, changing validation rules, adding GUI Toolbox management, changing callback resolution order, or creating a remote Toolbox distribution system.
- Out of scope: direct editing of Project Manifest or Topic Workspace Manifest when an existing CLI command can perform the same mutation safely.
- Out of scope: treating a Toolbox as a packaged system skill, Agent Team Template, provider adapter, executable action bundle, or Workspace Runtime component.

## Operational Constraints

- The skill must follow the canonical domain language in `.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md`.
- The skill must prefer `isomer-cli` commands for installation and management so validation, path checks, and diagnostics remain authoritative.
- The skill must keep generated Toolbox ids stable, lowercase, path-safe, and suitable for callback ids and runtime param ids.
- The skill must warn before project-wide installation because project-scope Toolboxes affect all matching contexts unless narrowed later.
- The skill must warn before disabling or uninstalling a Toolbox because callback records may remain installed for audit while effective behavior changes through gating.
- The skill must keep credentials, API keys, benchmark-private data, and large copied source documents out of Toolbox manifests, callback bodies, README files, and default param bundles.
- The skill should run `pixi run lint`, `pixi run typecheck`, `pixi run test`, or narrower checks only when the surrounding repository change warrants code validation; pure Toolbox source edits may instead use CLI validation and targeted file inspection.
- The skill must make scope explicit in final reports: Project, Research Topic, Topic Actor, or Topic Agent.

## Assumptions

- Toolboxes are now the canonical Isomer term for project-local extension packages that can provide callback material and runtime param defaults.
- The existing `isomer-cli project toolboxes`, `project skill-callbacks install --toolbox-dir`, and `project toolbox-params` surfaces are sufficient for the first version of the skill.
- Most first users will create Toolboxes under the host Project's `skillset/toolboxes/` directory, even though the CLI can validate other project-local source paths.
- The skill can be packaged as a project-local or system skill later; this feature requirement defines behavior and content rather than the final packaging path.
- Agents using this skill have normal repository file-editing ability and can run local `pixi run isomer-cli ...` commands when the user asks them to act.

## Open Questions

- What should the skill be named and where should it live: `isomer-op-toolbox-mgr`, `isomer-dev-toolbox-creator`, or another package path?
- Should the first version be operator-facing only, or should it also support developers maintaining Isomer's own Toolbox schema and CLI implementation?
- Should the skill include a scaffold template for new Toolboxes, or should it only describe the expected files and let agents create them from scratch?
- Should the skill ask clarifying questions before creating a Toolbox, or should it infer defaults from target skills and user intent when possible?
- Which validation command should be the canonical final check for a newly created Toolbox: `project skill-callbacks install --toolbox-dir ... --dry-run` if added later, `project toolboxes validate`, direct manifest loading through tests, or another command?
- Should runtime param bundle authoring be a first-class workflow in this skill, or a short advanced section until more Toolboxes use it?
