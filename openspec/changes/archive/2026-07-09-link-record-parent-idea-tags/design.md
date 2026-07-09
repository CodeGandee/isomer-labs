## Context

Record detail tabs now use a Markdown-first surface that mirrors idea detail pages. They already display structured direct parent idea metadata when available, but that metadata is only text. The workbench already has a semantic `open-idea` command and an openable descriptor path for `idea:<topic>:<idea_id>`, so parent idea navigation can reuse the existing idea detail tab flow.

## Goals / Non-Goals

**Goals:**

- Let users open the idea detail tab directly from a record or artifact detail parent idea tag.
- Keep the metadata tag visually compact and consistent with existing detail status rows.
- Require a stable `direct_parent_idea.idea_id` before enabling navigation.
- Fail safely when parent idea metadata is stale or incomplete.

**Non-Goals:**

- Do not add a new backend endpoint or mutate query-index data.
- Do not infer idea links from display keys, titles, or prose.
- Do not change how parent idea metadata is derived.

## Decisions

1. Reuse the existing workbench command flow. The clickable tag should emit `workbenchCommands$.next({ type: "open-idea", topicId, ideaId })`, matching graph double-click behavior. Alternative considered: fetch the idea detail directly inside the record detail panel. That would duplicate tab routing and bypass URL/history behavior already handled by openable descriptors.

2. Gate clickability on `direct_parent_idea.idea_id`. Display keys such as `I-7` are presentation labels, not canonical ids, and titles can change. If `idea_id` is missing, the tag remains a normal status badge.

3. Preserve the tag visual language. The control should remain in the status row and look like a metadata chip, with accessible button semantics and hover/focus states. Alternative considered: add a separate `Open Parent Idea` toolbar button. That is clearer but costs more toolbar space for a contextual action.

4. Surface stale-link failure through toast notification. The openable descriptor flow can return `ok: false` when an idea was deleted or cannot be resolved. The GUI should not crash or silently swallow the click; it should show a short toast and leave the user in the current record detail tab.

## Risks / Trade-offs

- [Risk] Stale parent idea metadata may point at a deleted idea. → Mitigation: keep navigation read-only and show a toast when the openable descriptor cannot open a tab.
- [Risk] A clickable chip could be mistaken for a filter token. → Mitigation: use explicit label text (`parent idea: ...`) and button focus/hover styling.
- [Risk] Parent idea metadata might include only display labels. → Mitigation: keep display-only behavior unless `idea_id` exists.

## Migration Plan

No data migration is required. Implement the frontend interaction and tests, rebuild static assets, and validate the change. Rollback restores the parent idea tag to display-only text.

## Open Questions

None.
