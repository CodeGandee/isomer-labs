# Bun Resolve

Use this subcommand to choose reachable registries for Bun.

## Required Inputs

| Input | Resolution |
| --- | --- |
| Package context | The package name(s) or scope the user wants to install. |
| Project config | Optional `bunfig.toml` in the project directory or `~/.bunfig.toml`. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Test the default Bun registry** with `curl -I --max-time 10 https://registry.npmjs.org/` or `bun pm ls <package>` when Bun is available.
2. **If the default registry is reachable**, recommend it.
3. **If the default registry is not reachable**, inspect Bun configuration. Check `bunfig.toml` in the project directory, then `~/.bunfig.toml`. Read `[install]` `registry`, `[install]` `cache`, and scoped registry entries.
4. **Test each candidate registry** in declaration order and recommend the first reachable one.
5. **If no registry is reachable**, report that the default Bun registry is not usable and stop with a blocker.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the package context, project config, and reachability tests, then execute the plan.

## Output Contract

Report:

- `subcommand`: `bun-resolve`.
- `default_registry_reachable`: `true`, `false`, or `not tested`.
- `local_registries`: registries discovered from `bunfig.toml` files, including scoped entries.
- `recommended_registry`: the URL or config entry to pass to Bun.
- `tested_registries`: each candidate and its reachability result.
- `blockers`: missing package context or no reachable registry.
