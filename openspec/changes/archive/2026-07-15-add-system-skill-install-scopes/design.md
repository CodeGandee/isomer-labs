## Context

The current resolver accepts a required target and an optional `--home` path. Despite its name, `--home` replaces the complete skill root, so callers must pass a terminal directory such as `.kimi-code/skills`; passing `.kimi-code` installs skills at the wrong level. Defaults also mix project-local Claude, Kimi, and generic roots with a user-global Codex root, so command intent is not explicit.

Agent hosts distinguish personal and project skills. Claude Code documents personal skills under its user configuration directory and project skills under `.claude/skills`; Kimi Code documents `$KIMI_CODE_HOME/skills` or `~/.kimi-code/skills` for user scope and `.kimi-code/skills` for project scope; Codex documents `.agents/skills` project discovery while the existing Isomer contract supports its established `$CODEX_HOME/skills` or `~/.codex/skills` personal installation. The generic target uses the shared `.agents/skills` convention. These conventions make scope a target-resolution input, not an arbitrary output path.

The canonical Isomer **Project** is an Isomer-managed directory tree, but this low-level installer can run before Project initialization. In this command family, `project` is an agent-host installation scope anchored to the current working directory; it does not assert that the directory is already an Isomer Project.

## Goals / Non-Goals

**Goals:**

- Make every target resolution state whether skills are for the current user or current working directory.
- Remove the ambiguous exact-root override from the public system-skill command family.
- Use host-supported user and project skill directories without requiring callers to append hidden tool directories or `/skills`.
- Keep install, status, upgrade, and uninstall symmetric across the same target-and-scope resolver.
- Preserve safe receipt ownership when multiple target labels resolve to one physical root.
- Keep existing receipt files readable and migrate them only during an authorized mutation.

**Non-Goals:**

- Discover an initialized Isomer Project, Git root, or nearest parent directory for `project` scope.
- Support arbitrary plugin, extra, environment-supplied, or manually selected skill roots through the public installer.
- Change explicit-root read-only inspection commands such as `internals inspect-system-skill-root`.
- Migrate Codex personal installations from the existing Isomer `$CODEX_HOME/skills` convention to the shared `~/.agents/skills` convention.
- Change packaged skill selection, copy and symlink projection behavior, compatibility policy, or Project extension declarations.

## Decisions

### Require Scope on Every Target-Resolving Command

`system-skills install`, `status`, `upgrade`, and `uninstall` will require `--scope user|project` alongside `--target`. The CLI will remove `--home` rather than retain an alias because the new interface deliberately removes arbitrary destination selection.

Examples:

```text
isomer-cli system-skills install --target kimi-code --scope project
isomer-cli system-skills install --target kimi-code --scope user
```

Requiring scope prevents a package update from silently changing an implicit installation from project-local to user-global or vice versa. A default such as `project` was considered and rejected because it would preserve ambiguity in automation and make user-wide effects depend on target-specific historical defaults.

### Resolve a Target-and-Scope Matrix

The resolver will compute exact skill roots from the following matrix:

| Target | `project` scope | `user` scope |
| --- | --- | --- |
| `claude-code` | `<cwd>/.claude/skills` | `${CLAUDE_CONFIG_DIR:-~/.claude}/skills` |
| `codex` | `<cwd>/.agents/skills` | `${CODEX_HOME:-~/.codex}/skills` |
| `kimi-code` | `<cwd>/.kimi-code/skills` | `${KIMI_CODE_HOME:-~/.kimi-code}/skills` |
| `generic` | `<cwd>/.agents/skills` | `~/.agents/skills` |

Environment-variable values are expanded as user paths and then resolved without requiring the destination to exist. `project` always uses the process current working directory supplied to the resolver; it does not search upward for Git or Isomer metadata. `user` always uses the current OS user's home context and never depends on the current working directory.

Using `--home` as a tool-home path and appending `/skills` was considered and rejected because its meaning would still vary between an OS home, a tool configuration root, and an exact skill root. Retaining `--skill-root` as a replacement escape hatch was also rejected because the requested model intentionally limits public installation to declared scopes; provider-neutral explicit-root inspection remains available separately.

### Deduplicate Physical Roots for `--target all`

Codex and `generic` project scope both resolve to `<cwd>/.agents/skills`, and custom environment values can make other destinations overlap. The resolver will expand `all`, group target-scope bindings by normalized absolute skill root, and execute each physical root once. Results will expose every binding associated with that root rather than pretending that duplicate writes are separate installations.

For example:

```text
--target all --scope project
  <cwd>/.claude/skills      bindings: claude-code/project
  <cwd>/.agents/skills      bindings: codex/project, generic/project
  <cwd>/.kimi-code/skills   bindings: kimi-code/project
```

Executing all concrete targets independently was considered and rejected because the second operation on a shared root would either preserve files without recording the second target or rewrite a receipt with contradictory ownership metadata.

### Add Scope-Aware Receipt Bindings

New mutations will write `isomer-labs-skill-manifest.v3`. Instead of one exclusive `target` string, the receipt will contain a sorted set of bindings, each with `target` and `scope`, plus the existing normalized `skill_root`, package metadata, timestamp, and per-skill records. One physical root can therefore serve more than one compatible host label without duplicate projection.

The result model and JSON output will report `scope`, resolved `skill_root`, and root bindings. A concrete target command normally has one binding; an `all` command can have several bindings for one result. Human output will state both target and scope so user-global and project-local operations cannot look identical.

Receipt v1 and v2 remain readable as legacy evidence. Read-only status will not invent a missing legacy scope. The next successful install, upgrade, or uninstall mutation at the explicitly resolved root will write v3 with the current target-scope binding while preserving valid tracked skill records. If an existing v3 receipt is mutated through another target-scope binding that resolves to the same root, the writer will merge that binding rather than replace prior bindings.

### Keep Operator Installation Scoped but Inspection Provider-Neutral

`isomer-op-system-skill-mgr` will choose `project` for Project Operator installations unless the user explicitly requests a user-wide installation. It will call the low-level installer with `--target <host-known-target> --scope <scope>`, then verify the resolved root reported by the command with explicit-root inspection. Detection and live-inventory logic remain provider-neutral and do not scan the new conventional roots automatically.

This preserves the manager's separation between deterministic authorized installation and evidence-based detection. It also makes user-wide installation an explicit user decision because it affects every project loaded by that host.

## Risks / Trade-offs

- [Removing arbitrary roots blocks plugin and custom host layouts] → Keep provider-neutral explicit-root inspection, direct users with nonstandard installation needs to host-native installation mechanisms, and state this boundary in help and docs.
- [Required scope breaks existing scripts] → Fail with normal Click unknown or missing-option diagnostics and publish direct command migrations from omitted scope and `--home` forms.
- [The term `project` can be mistaken for an initialized Isomer Project] → Define it consistently as current-working-directory agent-host scope in CLI help, JSON, and documentation.
- [User-scope host conventions may change] → Isolate the matrix in one resolver, cover environment overrides with tests, and document the supported paths as an Isomer compatibility contract.
- [Shared roots can produce duplicate writes or contradictory receipts] → Group resolved absolute roots before filesystem operations and use multi-binding v3 receipts.
- [Legacy receipts lack scope] → Report them as legacy without inference and add scope metadata only during a user-authorized mutation at an explicitly resolved root.

## Migration Plan

1. Add scope and binding types, implement the target-scope matrix, and group resolved targets by absolute skill root.
2. Add v3 receipt read/write support while retaining v1 and v2 parsing.
3. Replace `--home` with required `--scope` on install, status, upgrade, and uninstall; update JSON and human output.
4. Update `isomer-op-system-skill-mgr`, documentation, examples, and validators to use target plus scope.
5. Add unit tests for every matrix entry, environment override, missing scope, rejected `--home`, shared-root deduplication, v2 reads, and v3 binding migration.
6. Release the change as a breaking CLI update. Rollback consists of reinstalling the previous Isomer CLI; v3 receipts must remain non-destructive to older binaries, which will report an unsupported schema instead of mutating an unrecognized receipt.

## Open Questions

None. The design intentionally keeps Codex user-scope resolution compatible with the existing Isomer `$CODEX_HOME/skills` contract; adopting Codex's shared `~/.agents/skills` user convention can be proposed separately with an explicit migration for existing personal installations.
