## 1. Parent Idea Navigation

- [x] 1.1 Add a frontend helper that extracts a stable parent idea id and display label from `direct_parent_idea` metadata.
- [x] 1.2 Render the record detail parent idea tag as an accessible clickable badge when a stable idea id exists, and keep the existing inert badge when it does not.
- [x] 1.3 Route clicks through the existing `open-idea` workbench command and show a toast if the openable item cannot be resolved.

## 2. Validation

- [x] 2.1 Add frontend tests covering clickable parent idea navigation, inert parent idea labels without `idea_id`, and stale-link notification behavior.
- [x] 2.2 Rebuild static web assets so the packaged GUI includes the change.
- [x] 2.3 Run focused frontend tests and `openspec validate link-record-parent-idea-tags --strict`.
