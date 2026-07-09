## Context

The Click entrypoint already prints top-level help when `isomer-cli` is invoked without arguments, but its introductory text is a stale long command dump. Most nested Click groups keep the default missing-command behavior, so invocations such as `isomer-cli project topics` and `isomer-cli ext research` are normalized as `ISOCLI001` errors even though the message contains help text.

The CLI has many command groups spread across registration modules. A one-off fix in each module would be fragile and easy to miss as new groups are added.

## Goals / Non-Goals

**Goals:**
- Make no-argument invocation of every CLI group equivalent to that group's help output.
- Keep malformed invocations as normalized CLI errors.
- Replace the top-level long command dump with a short operator-oriented overview, canonical links, and top-level command descriptions in Click's generated `Commands:` section.
- Cover the behavior with focused unit tests.

**Non-Goals:**
- Redesign every command's help text.
- Add machine-readable command discovery output.
- Change command names, options, or command handler behavior.
- Change package installation or release metadata beyond using existing repository and docs URLs in help text.

## Decisions

Use a shared Click group class for no-argument help behavior. The class should set `invoke_without_command=True` and, when no subcommand was invoked, print the current context help and return normally. This makes all groups consistent and keeps existing `--help` formatting under Click's control.

Apply the shared group class through a small helper or decorator wrapper rather than patching every group callback manually. The top-level app and `project` group can use the same mechanism, while callbacks that need to initialize `ctx.obj` still run before help is printed.

Keep `--print-json <group>` as text help for no-argument group invocation. Help is an operator discovery surface rather than command result data, and this matches the behavior of explicit `--help` flags.

Source top-level links from stable constants in the CLI app. The repository URL is already declared in `mkdocs.yml`; the docs URL should match the GitHub Pages deployment at `https://codegandee.github.io/isomer-labs/`.

Avoid a separate custom top-level command list. The generated Click `Commands:` section should be the single command navigation surface, with richer help text on each top-level group.

## Risks / Trade-offs

- [Risk] A custom Click group can accidentally skip callback setup for groups with options. → Mitigation: implement the behavior after normal callback invocation and test `project --root <path>` style group help.
- [Risk] Existing tests may expect missing group subcommands to be errors. → Mitigation: update or add tests only for empty group invocations; keep malformed command tests unchanged.
- [Risk] New command groups might bypass the helper. → Mitigation: provide a local CLI helper and use it for every registered group touched by this command tree.
