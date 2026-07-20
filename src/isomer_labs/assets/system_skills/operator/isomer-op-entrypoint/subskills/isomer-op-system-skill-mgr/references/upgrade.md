# Upgrade

Use this subcommand only after the user authorizes managed installation migration or package-version upgrade for a concrete host target and scope.

## Workflow

1. Resolve the extension id, selected Project, concrete host target, and selected scope. Project scope is the default for a Project Operator request; user scope requires explicit user-wide intent.
2. Inspect the exact host-known root. If it has a current v4 receipt and complete compatible public packs, skip file mutation and finish any authorized Project registration.
3. Require a supported legacy receipt before managed flat-path migration. Treat untracked legacy-looking directories as conflicts or ambient evidence, not cleanup authority.
4. Run `isomer-cli --print-json system-skills upgrade --target <host-known-target> --scope <selected-scope> --extension <extension-id>`. The upgrade stages and validates the core pack plus the selected complete extension pack before replacing the receipt.
5. Read `skill_root` from the result and verify it with `isomer-cli internals inspect-system-skill-root --skill-root <resolved-root> --extension <extension-id>`. Require a current v4 receipt, complete nested protected coverage, managed receipt evidence, and usable compatibility.
6. Report `migration_status`, each removed stale path, and each `stale_retained` path. A retained path means cleanup is partial and needs bounded repair; it does not invalidate an otherwise verified new pack.
7. Unless the user opted out, call Project `remember` after v4 verification succeeds.
8. Report that the current agent session may cache old discovery. Require a host refresh or new session before claiming the new public entrypoint is live.

If the user's task does not map cleanly to these steps, use your native planning tool to build a bounded upgrade plan from the selected host target, receipt evidence, pack scope, compatibility status, and cleanup authority, then execute the plan or report the blocker.

If staging or validation fails, report that the old receipt and projections remain intact. Do not retry with deletion or a forced install unless the user separately authorizes replacement. Never delete an untracked skill directory because its name resembles an old protected skill.
