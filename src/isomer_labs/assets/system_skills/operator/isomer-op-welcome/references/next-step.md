# Recommend the Next Core Step

## Workflow

1. Confirm that current Project or extension evidence would materially improve the recommendation.
2. Announce the selected read-only inspection commands before running them.
3. Run only commands from **Read-Only Commands** and report the evidence that affected routing.
4. Match the result to one curated pattern in [show-options.md](show-options.md).
5. Recommend one public welcome or execution invocation with the user's supplied context, expected action, mutation posture, blocker, and next step.

If the task does not map cleanly to these steps, use the native planning tool to decide whether read-only evidence can resolve it; otherwise recommend `show-options`, `show-extensions`, or `choose-path` without running a command.

## Read-Only Commands

- `isomer-cli project validate`
- `isomer-cli doctor`
- `isomer-cli project topics list`
- `isomer-cli project context show`
- `isomer-cli project self show`
- `isomer-cli project outputs policy`
- `isomer-cli system-skills extensions list`
- `isomer-cli project system-extensions list`

Do not infer verified pack integrity from package catalog, Project declaration, or observed public names. Recommend `$isomer-op-entrypoint use system-skills to inspect <extension-id> for <host> <scope>` when receipt, explicit-root, compatibility, installation, upgrade, or refresh evidence is needed.
