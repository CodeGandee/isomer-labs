# Install Extension

Use this subcommand only after the user authorizes installing one package-catalog extension.

1. Resolve the extension id and selected Project. If the Project already declares the extension, preserve that declaration; an explicit install request still authorizes repairing or installing files.
2. Select the skill root used by the current operator host. Obtain it from host context or the loaded core skill location. Do not let the CLI infer a root.
3. Inspect the root for the extension. If a complete compatible family already exists, skip installation and proceed to registration.
4. Run `isomer-cli system-skills install --target <host-known-target> --home <selected-root> --extension <extension-id>`. Add `--force` only when the user authorized replacing an invalid, stale, or incompatible Isomer-managed projection.
5. Verify with `isomer-cli internals inspect-system-skill-root --skill-root <selected-root> --extension <extension-id>`.
6. Unless the user opted out, call Project `remember` after verification reports a complete usable family.
7. Check a refreshed live inventory when possible. Otherwise state that a host refresh is required and recommend a new turn, thread, or host-native reload.

If installation succeeds but verification or registration fails, report a partial outcome. A later retry inspects first and completes registration without reinstalling verified files.
