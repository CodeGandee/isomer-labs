"""Ordered topic-stock and packaged-default selection for Kaoju templates."""

from __future__ import annotations

import builtins

from isomer_labs.kaoju.artifacts import KaojuServiceError
from isomer_labs.kaoju.template_defaults import load_packaged_template
from isomer_labs.kaoju.template_state import KaojuTemplateStateService
from isomer_labs.kaoju.template_support import (
    DEFAULT_TEMPLATE_NAME,
    TemplateSelection,
    validate_template_name,
)
from isomer_labs.runtime.records import RuntimeLifecycleRecord


class KaojuTemplateSelectionService(KaojuTemplateStateService):
    """Add strict explicit selection and non-mutating packaged fallback."""

    def resolve_selection(
        self,
        *,
        name: str | None = None,
        stable_ref: str | None = None,
    ) -> TemplateSelection:
        """Resolve an explicit topic selector or the role-local default with packaged fallback."""

        explicit = name is not None or stable_ref is not None
        selected_name = validate_template_name(name or DEFAULT_TEMPLATE_NAME)
        if explicit:
            state = self.resolve_state(name=name, stable_ref=stable_ref)
            if state.record.status != "ready":
                raise KaojuServiceError(
                    "template_not_active",
                    f"Explicit {self.template_kind.label} {state.name!r} is {state.record.status!r}, not ready.",
                )
            return TemplateSelection.from_state(self.template_kind, state)
        candidates = self._records_claiming_name(selected_name)
        if len(candidates) > 1:
            raise KaojuServiceError(
                "template_identity_conflict",
                f"Default {self.template_kind.label} name {selected_name!r} resolves to several records: "
                + ", ".join(record.id for record in candidates),
            )
        if candidates:
            state = self._state_from_record(candidates[0])
            if state.record.status != "ready":
                raise KaojuServiceError(
                    "template_not_active",
                    f"Default {self.template_kind.label} {selected_name!r} is {state.record.status!r}, not ready.",
                )
            return TemplateSelection.from_state(self.template_kind, state)
        packaged = load_packaged_template(self.template_kind)
        return TemplateSelection(
            template_kind=self.template_kind,
            name=packaged.name,
            selection_source="packaged-default",
            root=packaged.root,
            tree_digest=packaged.tree_digest,
            authored_metadata=packaged.authored_metadata,
            packaged_identity=packaged.identity,
            packaged_resource_version=packaged.resource_version,
        )

    def _records_claiming_name(self, name: str) -> builtins.list[RuntimeLifecycleRecord]:
        """Return records that claim a role-local name, including malformed state."""

        expected_ref = f"{self.template_kind.stable_ref_prefix}-{name}"
        store = self._store(read_only=True)
        try:
            records = [
                record
                for record in store.list_lifecycle_records()
                if record.topic_workspace_id == self.context.topic_workspace_id
                and record.transition_metadata.get("semantic_id") == self.template_kind.semantic_id
                and record.transition_metadata.get("template_kind", self.template_kind.kind) == self.template_kind.kind
                and (record.transition_metadata.get("template_name") == name or record.id == expected_ref)
            ]
        finally:
            store.close()
        return records
