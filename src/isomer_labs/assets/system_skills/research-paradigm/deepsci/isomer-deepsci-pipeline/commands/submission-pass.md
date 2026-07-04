# submission-pass

Finalize a reviewed paper bundle for submission or archive.

## Recipe

| Order | Stage | Skill | Consumes | Produces | Continue if | Pause if | Expensive |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | audit | `isomer-deepsci-review` | `paper-bundle` | `review-report` | `route_decision == finalize` | `route_decision != finalize` | no |
| 2 | data_statement | `isomer-deepsci-nature-data` | `paper-bundle` | `data-availability-statement` | `ready == true` | blocker exists | no |
| 3 | close | `isomer-deepsci-finalize` | `paper-bundle`, `review-report`, `data-availability-statement` | `final-summary` | `closure_decision` in `[stop, park, publish]` | blocker exists | no |

## Workflow

When this subcommand is invoked, execute the following steps in order.

1. **Check entry context**. Ensure `paper-bundle` is available from the caller context.
2. **Execute stages sequentially**. Invoke each stage skill with automatic artifact handoffs. Use the **Recipe** table above for stage order, inputs, outputs, and transition conditions.
3. **Apply transition rules**. After each stage, use `references/transition-rules.md` to decide continue, pause, or block.
4. **Produce the terminal report**. Write ``pipeline-terminal-report`` using `references/terminal-report-template.md`.

If the user's task does not map cleanly to this pass, route back to `isomer-deepsci-pipeline` main workflow or use your native planning tool.

## Notes

- Use this pass when the paper bundle is ready for final review and submission packaging.
- If the target venue is not Nature-family, replace or skip `isomer-deepsci-nature-data` under external control.
- The close stage produces the `closure-decision` for the external controller.
