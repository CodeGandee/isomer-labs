# Detect Extensions

Use this subcommand for read-only availability discovery.

1. Resolve the selected Project when one exists and run `isomer-cli project system-extensions list --json`.
2. Return declared extensions immediately with `project_manifest` evidence. Do not verify or rewrite their declarations.
3. For undeclared extensions, collect project-scope skill roots from the current host context and pass each root explicitly to `internals inspect-system-skill-root`.
4. If no complete usable managed family is found, submit the host-visible skill names to `internals classify-system-skill-inventory`.
5. Report complete, partial, missing, unmanaged, incompatible, and unknown state. Provide registration or installation advice but make no mutation.

If the user supplies one extension id, stop after resolving that extension. Otherwise report each package-catalog extension in catalog order.
