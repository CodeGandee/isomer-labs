# Install Extension

Use this subcommand only after the user authorizes installing one package-catalog extension.

## Workflow

1. Resolve the extension id and selected Project. If the Project already declares the extension, preserve that declaration; an explicit install request still authorizes repairing or installing files.
2. Select a concrete host target supported by the installer. If the current host cannot identify one, report a blocker and preserve existing files and declarations instead of guessing a target or root.
3. Select project scope by default for a Project Operator request. Select user scope only after an explicit user request or confirmation, and explain that user-wide installation can affect the selected host across Projects.
4. Inspect any host-known root for the extension. If a complete compatible family already exists, skip installation and proceed to registration.
5. Run `isomer-cli --print-json system-skills install --target <host-known-target> --scope <selected-scope> --extension <extension-id>`. Add `--force` only when the user authorized replacing an invalid, stale, or incompatible Isomer-managed projection.
6. Read the resolved skill root from `skill_root` in the installation result. Verify with `isomer-cli internals inspect-system-skill-root --skill-root <resolved-root> --extension <extension-id>`.
7. Unless the user opted out, call Project `remember` after verification reports a complete usable family.
8. Check a refreshed live inventory when possible. Otherwise state that a host refresh is required and recommend a new turn, thread, or host-native reload.

If the user's task does not map cleanly to these steps, use your native planning tool to build an installation plan from the authorized extension, concrete host target, selected scope, verification evidence, and registration boundary, then execute the plan.

If installation succeeds but verification or registration fails, report a partial outcome. A later retry inspects first and completes registration without reinstalling verified files.

The scoped installer supports only target-defined project and user roots. For an arbitrary plugin, extra, or custom destination, explain that boundary and use host-native installation guidance instead of guessing a path.
