# Detect Extensions

Use this subcommand for read-only availability discovery.

## Workflow

1. Resolve the selected Project when one exists and run `isomer-cli --print-json project system-extensions list`.
2. Report declared extensions with `project_manifest` routing evidence. Do not rewrite their declarations. Continue when the request needs current-host usability evidence.
3. Collect project-scope skill roots from the current host context and pass each root explicitly to `internals inspect-system-skill-root`. Interpret current v5 receipt evidence before explicit-root integrity evidence.
4. If no complete usable managed pack is found, submit the host-visible skill names to `internals classify-system-skill-inventory` as the final limited evidence level.
5. Report managed complete, unmanaged complete, partial, missing, legacy migration candidate, incompatible, `welcome_seen`, `entrypoint_seen`, `public_pair_seen`, and unknown states. Provide registration, upgrade, repair, refresh, or installation advice but make no mutation.

If the user's task does not map cleanly to these steps, use your native planning tool to build a read-only discovery plan from the requested extension, selected Project, host-known roots, and live inventory, then execute the plan.

If the user supplies one extension id, stop after resolving that extension. Otherwise report each package-catalog extension in catalog order.
