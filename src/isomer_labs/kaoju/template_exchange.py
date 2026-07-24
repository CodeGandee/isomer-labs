"""Working-copy exchange support for named Kaoju templates."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import tempfile
from typing import Mapping

from isomer_labs.kaoju.artifacts import KaojuServiceError
from isomer_labs.kaoju.template_selection import KaojuTemplateSelectionService
from isomer_labs.kaoju.template_support import (
    EXPORT_METADATA_NAME,
    EXPORT_METADATA_VERSION,
    TEMPLATE_EXCHANGE_LABEL,
    TemplateSelection,
    _atomic_write_json,
    _load_export_metadata,
    _replace_directory,
    _required_actor,
    _utc_now,
    template_tree_digest,
)


class KaojuTemplateExchangeService(KaojuTemplateSelectionService):
    """Add safe export creation and working-copy posture checks."""

    def _write_export(
        self,
        selection: TemplateSelection,
        target: Path,
        *,
        actor: str,
    ) -> None:
        if target.exists() and not target.is_dir():
            raise KaojuServiceError(
                "template_export_target_invalid",
                f"Template export target is not a directory: {target}",
            )
        if target.exists():
            entries = list(target.iterdir())
            metadata_path = target / EXPORT_METADATA_NAME
            if entries and not metadata_path.is_file():
                raise KaojuServiceError(
                    "template_export_target_unrecognized",
                    f"Template export target contains unrecognized or legacy content: {target}",
                    (
                        "Move or archive the existing directory outside Isomer, then export again.",
                    ),
                )
            if metadata_path.is_file():
                metadata = _load_export_metadata(
                    metadata_path,
                    expected_kind=self.template_kind.kind,
                )
                if not self._metadata_matches_selection(metadata, selection):
                    raise KaojuServiceError(
                        "template_export_identity_invalid",
                        f"Template export target claims a different source identity: {target}",
                    )
                observed = template_tree_digest(
                    target,
                    exclude_exchange_metadata=True,
                )
                if observed != metadata.get("exported_tree_digest"):
                    raise KaojuServiceError(
                        "template_export_edited",
                        f"Template export target contains edits and will not be overwritten: {target}",
                        (
                            "Use the Kaoju agent to reconcile the working tree, then update or observe it explicitly.",
                        ),
                    )
        metadata = self._export_metadata(
            selection,
            target,
            actor=actor,
            exported_tree_digest=selection.tree_digest,
        )
        target.parent.mkdir(parents=True, exist_ok=True)
        staged = Path(
            tempfile.mkdtemp(
                prefix=f".{target.name}.template-export-",
                dir=target.parent,
            )
        )
        try:
            self._copy_canonical_tree(selection.root, staged)
            _atomic_write_json(staged / EXPORT_METADATA_NAME, metadata)
            _replace_directory(staged, target)
        finally:
            if staged.exists():
                shutil.rmtree(staged)

    def _export_metadata(
        self,
        selection: TemplateSelection,
        target: Path,
        *,
        actor: str,
        exported_tree_digest: str,
    ) -> dict[str, object]:
        return {
            "schema_version": EXPORT_METADATA_VERSION,
            "template_kind": self.template_kind.kind,
            "template_name": selection.name,
            "selection_source": selection.selection_source,
            "canonical_ref": selection.stable_ref,
            "state_token": selection.state_token,
            "packaged_identity": selection.packaged_identity,
            "packaged_resource_version": selection.packaged_resource_version,
            "canonical_tree_digest": selection.tree_digest,
            "exported_tree_digest": exported_tree_digest,
            "observed_path": str(target.resolve(strict=False)),
            "observed_at": _utc_now(),
            "actor": _required_actor(actor),
            "exchange_root_label": TEMPLATE_EXCHANGE_LABEL,
            "canonical": False,
        }

    def _metadata_matches_selection(
        self,
        metadata: Mapping[str, object],
        selection: TemplateSelection,
    ) -> bool:
        if metadata.get("template_name") != selection.name:
            return False
        if selection.selection_source == "topic-stock":
            return (
                metadata.get("selection_source") == "topic-stock"
                and metadata.get("canonical_ref") == selection.stable_ref
            )
        return (
            metadata.get("selection_source") == "packaged-default"
            and metadata.get("packaged_identity")
            == selection.packaged_identity
            and metadata.get("packaged_resource_version")
            == selection.packaged_resource_version
        )

    def _export_status(
        self,
        record: Mapping[str, object],
    ) -> dict[str, object]:
        metadata_value = record.get("transition_metadata")
        metadata = metadata_value if isinstance(metadata_value, dict) else {}
        name = str(
            metadata.get("template_name")
            or metadata.get("scope_key")
            or ""
        )
        observed_path = str(
            metadata.get("observed_path")
            or record.get("content_path")
            or ""
        )
        path = Path(observed_path)
        posture = "missing"
        working_digest: str | None = None
        identity_valid = False
        canonical_changed = False
        if path.is_dir():
            metadata_path = path / EXPORT_METADATA_NAME
            if metadata_path.is_file():
                try:
                    disk_metadata = _load_export_metadata(
                        metadata_path,
                        expected_kind=self.template_kind.kind,
                    )
                    identity_valid = (
                        disk_metadata.get("template_name") == name
                        and disk_metadata.get("canonical_ref")
                        == metadata.get("canonical_ref")
                        and disk_metadata.get(
                            "selection_source",
                            "topic-stock",
                        )
                        == metadata.get("selection_source", "topic-stock")
                        and disk_metadata.get("packaged_identity")
                        == metadata.get("packaged_identity")
                        and disk_metadata.get("observed_path")
                        == str(path.resolve(strict=False))
                    )
                    working_digest = template_tree_digest(
                        path,
                        exclude_exchange_metadata=True,
                    )
                    if identity_valid:
                        posture = (
                            "edited"
                            if working_digest
                            != disk_metadata.get("exported_tree_digest")
                            else "unchanged"
                        )
                        if (
                            disk_metadata.get("selection_source")
                            == "packaged-default"
                        ):
                            from isomer_labs.kaoju.template_defaults import (
                                load_packaged_template,
                            )

                            packaged = load_packaged_template(
                                self.template_kind
                            )
                            canonical_changed = (
                                packaged.identity
                                != disk_metadata.get("packaged_identity")
                                or packaged.resource_version
                                != disk_metadata.get(
                                    "packaged_resource_version"
                                )
                                or packaged.tree_digest
                                != disk_metadata.get(
                                    "canonical_tree_digest"
                                )
                            )
                            if self._records_claiming_name(name):
                                canonical_changed = True
                        else:
                            try:
                                current = self._read_state(name)
                            except KaojuServiceError:
                                current = None
                            canonical_changed = (
                                current is None
                                or current.record.id
                                != disk_metadata.get("canonical_ref")
                                or current.state_token
                                != disk_metadata.get("state_token")
                                or current.tree_digest
                                != disk_metadata.get(
                                    "canonical_tree_digest"
                                )
                            )
                        if posture == "unchanged" and canonical_changed:
                            posture = "canonical-changed"
                    else:
                        posture = "identity-invalid"
                except (
                    KaojuServiceError,
                    OSError,
                    json.JSONDecodeError,
                ):
                    posture = "identity-invalid"
            else:
                posture = "identity-invalid"
        return {
            "template_kind": metadata.get("template_kind", "content"),
            "name": name,
            "path": observed_path,
            "export_ref": record.get("id"),
            "canonical_ref": metadata.get("canonical_ref"),
            "selection_source": metadata.get(
                "selection_source",
                "topic-stock",
            ),
            "packaged_identity": metadata.get("packaged_identity"),
            "packaged_resource_version": metadata.get(
                "packaged_resource_version"
            ),
            "recorded_state_token": metadata.get("state_token"),
            "recorded_canonical_tree_digest": metadata.get(
                "canonical_tree_digest"
            ),
            "recorded_exported_tree_digest": metadata.get(
                "exported_tree_digest"
            ),
            "working_tree_digest": working_digest,
            "posture": posture,
            "identity_valid": identity_valid,
            "canonical_changed": canonical_changed,
        }
