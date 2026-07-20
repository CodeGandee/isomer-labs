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
3. **If the default registry is not reachable**, inspect Bun configuration:
   - Check `bunfig.toml` in the project directory, then `~/.bunfig.toml`.
   - Read `[install]` `registry`, `[install]` `cache`, and scoped registry entries.
4. **Test each candidate registry** in declaration order and recommend the first reachable one.
5. **If no registry is reachable**, report that the default Bun registry is not usable and stop with a blocker.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the package context, project config, and reachability tests, then execute the plan.

## Output Contract

Default to **Essential Output** in chat. Use **Complete Output** when the user asks for complete, verbose, audit, debug, full handoff, or full output. Present either depth in natural-language Markdown. If the user explicitly requests JSON or another machine-readable format, serialize the applicable information in that format.

### Essential Output

Recommend the registry URL or configuration entry for Bun, and state whether it is reachable, blocked, or untested. Name missing package context or the absence of a reachable registry as a blocker.

### Complete Output

Group the complete explanation by default-registry reachability, locally configured and tested registries, the recommendation, and blockers.
