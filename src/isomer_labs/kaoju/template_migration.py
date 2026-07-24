"""Contract migration helpers for mutable named Kaoju templates."""

from __future__ import annotations

import builtins
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
from typing import Any, Mapping, Sequence

from isomer_labs.kaoju.artifacts import KaojuServiceError
from isomer_labs.kaoju.content import DIRECTORY_MANIFEST_NAME
from isomer_labs.kaoju.template_support import (
    DEFAULT_TEMPLATE_NAME,
    EXPORT_METADATA_NAME,
    TEMPLATE_KINDS,
    _load_export_metadata,
    _atomic_write_json,
    _replace_directory,
    _required_actor,
    _utc_now,
    template_tree_digest,
    validate_template_name,
)
from isomer_labs.runtime.records import RuntimeLifecycleRecord, utc_timestamp


def migrate_template(
    service: Any,
    *,
    record_id: str | None = None,
    name: str | None = None,
    actor: str,
    authored_metadata: Mapping[str, object] | None = None,
    expected_state: str | None = None,
) -> dict[str, object]:
    if service.template_kind.kind == "latex":
        return _migrate_latex(
            service,
            record_id=record_id,
            name=name or DEFAULT_TEMPLATE_NAME,
            actor=actor,
            authored_metadata=authored_metadata or {},
            expected_state=expected_state,
        )
    inspection = service.inspect_migration()
    upgraded_refs = _upgrade_content_contract(service, actor=actor)
    candidates = inspection["active_candidates"]
    assert isinstance(candidates, list)
    content_records = inspection.get("content_records")
    if record_id is None and isinstance(content_records, list) and content_records:
        return {
            "ok": True,
            "mutated": bool(upgraded_refs),
            "operation": "paper.template.migrate",
            "template_kind": "content",
            "upgraded_content_refs": upgraded_refs,
            "preserved_active_legacy_record_ids": sorted(
                str(item["record_id"])
                for item in candidates
                if isinstance(item, dict) and isinstance(item.get("record_id"), str)
            ),
            "preserved_historical_record_ids": inspection["historical_record_ids"],
            "preserved_versioned_export_paths": inspection["versioned_export_paths"],
            "legacy_export_paths": inspection["legacy_export_paths"],
            "affected_refs": upgraded_refs,
            "diagnostics": [],
            "next_actions": (
                ["Pass an explicit legacy record ref and distinct template name to adopt preserved legacy content."]
                if candidates
                else []
            ),
        }
    selected: dict[str, object] | None = None
    if record_id is not None:
        selected = next((item for item in candidates if isinstance(item, dict) and item.get("record_id") == record_id), None)
        if selected is None:
            raise KaojuServiceError("template_migration_candidate_missing", f"Legacy template migration candidate not found: {record_id}")
    elif len(candidates) == 1:
        item = candidates[0]
        selected = item if isinstance(item, dict) else None
    elif len(candidates) > 1:
        raise KaojuServiceError("template_migration_ambiguous", "Several active legacy templates require explicit record ids and names.", tuple(str(item) for item in candidates))
    if selected is None:
        return {
            "ok": True,
            "mutated": bool(upgraded_refs),
            "operation": "paper.template.migrate",
            "template_kind": "content",
            "upgraded_content_refs": upgraded_refs,
            "preserved_historical_record_ids": inspection["historical_record_ids"],
            "preserved_versioned_export_paths": inspection["versioned_export_paths"],
            "legacy_export_paths": inspection["legacy_export_paths"],
            "affected_refs": upgraded_refs,
            "diagnostics": [],
            "next_actions": [],
        }
    selected_name = validate_template_name(name or (DEFAULT_TEMPLATE_NAME if len(candidates) == 1 else ""))
    if selected.get("entrypoint_ambiguous") is True:
        raise KaojuServiceError("template_migration_entrypoint_ambiguous", "Legacy template content has an ambiguous entrypoint; agent review and an explicit prepared tree are required.")
    legacy_record = service._read_record(str(selected["record_id"]))
    with service._temporary_directory("template-migration-") as temporary:
        candidate = temporary / "candidate"
        candidate.mkdir()
        content_path = Path(str(legacy_record.content_path)) if legacy_record.content_path else None
        if content_path is None or not content_path.exists():
            raise KaojuServiceError("template_migration_content_missing", f"Legacy template content is missing for {legacy_record.id}.")
        if content_path.name == DIRECTORY_MANIFEST_NAME:
            service._copy_canonical_tree(content_path.parent, candidate)
        elif content_path.is_file():
            shutil.copyfile(content_path, candidate / content_path.name)
        else:
            raise KaojuServiceError("template_migration_content_invalid", f"Legacy template content is unsupported: {content_path}")
        result = service.create(
            selected_name,
            source=candidate,
            actor=actor,
            source_refs=(legacy_record.id,),
            change_summary="Wrap one unambiguous active legacy template in the mutable named-template tree without semantic rewriting.",
        )
    result["operation"] = "paper.template.migrate"
    result["legacy_record_id"] = legacy_record.id
    result["upgraded_content_refs"] = upgraded_refs
    result["preserved_historical_record_ids"] = inspection["historical_record_ids"]
    result["preserved_versioned_export_paths"] = inspection["versioned_export_paths"]
    return result


def inspect_latex_migration(service: Any, records: Sequence[RuntimeLifecycleRecord]) -> dict[str, object]:
    current = [
        service._summary(service._state_from_record(record))
        for record in records
        if service._is_named_template_record(record)
    ]
    candidates: list[dict[str, object]] = []
    historical: list[str] = []
    for record in records:
        semantic_id = record.transition_metadata.get("semantic_id")
        if semantic_id not in {"KAOJU:PAPER-TEMPLATE-TEX", "KAOJU:WRITING-TEMPLATE"}:
            continue
        item = _presentation_candidate(service, record)
        if record.status in {"archived", "superseded", "stale"}:
            historical.append(record.id)
        else:
            candidates.append(item)
    return {
        "ok": True,
        "mutated": False,
        "operation": "paper.template.migrate.inspect",
        "template_kind": "latex",
        "template_label": service.template_kind.label,
        "current_templates": current,
        "latex_candidates": candidates,
        "active_candidates": candidates,
        "historical_record_ids": sorted(historical),
        "proposed_mutations": [
            {
                "operation": "adopt-latex-stock",
                "source_ref": str(item["record_id"]),
                "target_name": DEFAULT_TEMPLATE_NAME,
                "requires_explicit_source": True,
                "requires_authored_metadata": True,
            }
            for item in candidates
        ],
        "required_authored_metadata": {
            "entrypoint": "safe relative .tex path",
            "extensions.latex": {
                "composition_mode": "preamble|marker|include",
                "build_profile": "tectonic|latexmk|pdflatex",
                "source_provenance": "non-empty string or object",
                "license_posture": "non-empty string",
            },
        },
        "conflicts": ["explicit_source_ref_required"] if len(candidates) > 1 else [],
        "diagnostics": [],
        "next_actions": [
            "Select an exact candidate ref and supply checked LaTeX authored metadata before applying adoption."
        ] if candidates else ["Prepare and create latex/main from an authorized LaTeX template directory."],
    }


def _presentation_candidate(service: Any, record: RuntimeLifecycleRecord) -> dict[str, object]:
    content_path = Path(record.content_path) if record.content_path else None
    root = content_path.parent if content_path is not None and content_path.name == DIRECTORY_MANIFEST_NAME else None
    entrypoints = (
        sorted(path.relative_to(root).as_posix() for path in root.rglob("*.tex") if path.is_file())
        if root is not None and root.is_dir()
        else ([content_path.name] if content_path is not None and content_path.suffix.lower() == ".tex" else [])
    )
    return {
        "record_id": record.id,
        "semantic_id": record.transition_metadata.get("semantic_id"),
        "status": record.status,
        "scope_key": record.transition_metadata.get("scope_key"),
        "content_path": record.content_path,
        "digest": service._legacy_content_digest(record),
        "entrypoints": entrypoints,
        "adoptable_directory": root is not None and root.is_dir(),
    }


def _migrate_latex(
    service: Any,
    *,
    record_id: str | None,
    name: str,
    actor: str,
    authored_metadata: Mapping[str, object],
    expected_state: str | None,
) -> dict[str, object]:
    if not record_id:
        raise KaojuServiceError(
            "template_migration_source_required",
            "LaTeX template adoption requires an exact source record ref.",
        )
    selected_name = validate_template_name(name)
    source_record = service._read_record(record_id)
    semantic_id = source_record.transition_metadata.get("semantic_id")
    if semantic_id not in {"KAOJU:PAPER-TEMPLATE-TEX", "KAOJU:WRITING-TEMPLATE"}:
        raise KaojuServiceError(
            "template_migration_source_invalid",
            f"LaTeX adoption source {record_id} is {semantic_id!r}, not a TeX snapshot or legacy writing template.",
        )
    source_path = Path(source_record.content_path) if source_record.content_path else None
    if source_path is None or source_path.name != DIRECTORY_MANIFEST_NAME or not source_path.is_file():
        raise KaojuServiceError(
            "template_migration_content_invalid",
            "LaTeX adoption requires a managed directory source tree.",
        )
    metadata = json.loads(json.dumps(authored_metadata))
    extensions = metadata.setdefault("extensions", {})
    if not isinstance(extensions, dict):
        raise KaojuServiceError("template_extensions_invalid", "Template extension metadata must be a JSON object.")
    latex = extensions.setdefault("latex", {})
    if not isinstance(latex, dict):
        raise KaojuServiceError("latex_template_contract_required", "extensions.latex must be a JSON object.")
    latex["adopted_from_ref"] = source_record.id
    with service._temporary_directory("latex-template-adoption-") as temporary:
        candidate = temporary / "candidate"
        service._copy_canonical_tree(source_path.parent, candidate)
        try:
            current = service._read_state(selected_name)
        except KaojuServiceError as exc:
            if exc.code != "template_not_found":
                raise
            current = None
        if current is None:
            result = service.create(
                selected_name,
                source=candidate,
                authored_metadata=metadata,
                actor=actor,
                source_refs=(source_record.id,),
                change_summary=f"Adopt {source_record.id} as named LaTeX presentation stock.",
            )
        else:
            if not expected_state:
                raise KaojuServiceError(
                    "template_expected_state_required",
                    "Updating existing LaTeX stock during adoption requires its current state token.",
                )
            validated = service._validated_authored_metadata(metadata, root=candidate)
            result = service._replace_tree(
                current,
                candidate,
                expected_state=expected_state,
                authored_metadata=validated,
                actor=actor,
                operation="adopt",
                source_refs=(source_record.id,),
                change_summary=f"Adopt {source_record.id} as replacement named LaTeX presentation stock.",
            )
    result["operation"] = "paper.template.migrate"
    result["adopted_source_ref"] = source_record.id
    result["source_preserved"] = True
    return result


def _upgrade_content_contract(service: Any, *, actor: str) -> builtins.list[str]:
    _required_actor(actor)
    store = service._store(read_only=False)
    changed: list[str] = []
    try:
        store.connection.execute("BEGIN IMMEDIATE")
        for record in store.list_lifecycle_records():
            metadata = record.transition_metadata
            if (
                record.topic_workspace_id != service.context.topic_workspace_id
                or metadata.get("semantic_id") != service.template_kind.semantic_id
                or not isinstance(metadata.get("template_name"), str)
                or not isinstance(metadata.get("state_token"), str)
                or metadata.get("template_kind") == "content"
            ):
                continue
            next_metadata = {
                **metadata,
                "template_kind": "content",
                "contract_migration": {
                    "schema_version": "isomer-kaoju-template-contract-migration.v1",
                    "actor": actor,
                    "preserved_stable_ref": True,
                    "preserved_tree_bytes": True,
                },
            }
            store.upsert_lifecycle_record(
                RuntimeLifecycleRecord(
                    **{
                        **record.__dict__,
                        "updated_at": utc_timestamp(),
                        "transition_metadata": next_metadata,
                    }
                )
            )
            changed.append(record.id)
        store.connection.commit()
        service._refresh_index_after_commit(store, changed)
    except Exception:
        store.connection.rollback()
        raise
    finally:
        store.close()
    return changed


def legacy_content_export_paths(service: Any) -> builtins.list[str]:
    base = service._exchange_base_root(materialize=False)
    if not base.is_dir():
        return []
    reserved = {spec.exchange_subdirectory for spec in TEMPLATE_KINDS.values()}
    paths: list[str] = []
    for path in base.iterdir():
        if not path.is_dir() or path.name in reserved:
            continue
        metadata_path = path / EXPORT_METADATA_NAME
        if not metadata_path.is_file():
            continue
        try:
            metadata = _load_export_metadata(metadata_path, expected_kind="content")
        except KaojuServiceError:
            continue
        if metadata.get("compatibility_source") == "legacy-unqualified-content-export":
            paths.append(str(path))
    return sorted(paths)


def inspect_exchange_root_migration(service: Any) -> dict[str, object]:
    """Preview the exact legacy singular to plural exchange-root migration."""

    singular = (
        service.context.topic_workspace_path
        / "intent"
        / "derived"
        / "writing-template"
    ).resolve(strict=False)
    plural = (
        service.context.topic_workspace_path
        / "intent"
        / "derived"
        / "writing-templates"
    ).resolve(strict=False)
    effective = service._exchange_base_root(materialize=False)
    singular_inventory, singular_invalid = _exchange_inventory(singular)
    plural_inventory, plural_invalid = _exchange_inventory(plural)
    conflicts: list[dict[str, object]] = []
    for identity in sorted(set(singular_inventory) & set(plural_inventory)):
        legacy = singular_inventory[identity]
        current = plural_inventory[identity]
        if legacy["tree_digest"] != current["tree_digest"]:
            conflicts.append(
                {
                    "template_kind": identity[0],
                    "name": identity[1],
                    "singular_path": legacy["path"],
                    "singular_tree_digest": legacy["tree_digest"],
                    "plural_path": current["path"],
                    "plural_tree_digest": current["tree_digest"],
                }
            )
    invalid = [*singular_invalid, *plural_invalid]
    if effective != plural:
        posture = (
            "explicit-legacy-binding"
            if effective == singular
            else "nondefault-binding"
        )
    elif not singular_inventory and not singular.exists():
        posture = "singular-absent"
    elif invalid:
        posture = "invalid"
    elif conflicts:
        posture = "conflicting"
    elif singular_inventory and set(singular_inventory) <= set(plural_inventory):
        posture = "equivalent"
    elif singular_inventory:
        posture = "ready"
    else:
        posture = "empty"
    preview_body = {
        "effective_root": str(effective),
        "singular_snapshot": _directory_snapshot_digest(singular),
        "plural_snapshot": _directory_snapshot_digest(plural),
        "singular_inventory": _inventory_json(singular_inventory),
        "plural_inventory": _inventory_json(plural_inventory),
        "invalid": invalid,
        "conflicts": conflicts,
    }
    preview_token = "exchange-migration-preview-" + hashlib.sha256(
        json.dumps(preview_body, sort_keys=True).encode("utf-8")
    ).hexdigest()
    return {
        "ok": posture not in {
            "invalid",
            "conflicting",
            "explicit-legacy-binding",
            "nondefault-binding",
        },
        "mutated": False,
        "operation": "paper.template.migrate.exchange-root.inspect",
        "posture": posture,
        "effective_root": str(effective),
        "singular_root": str(singular),
        "plural_root": str(plural),
        "singular_inventory": preview_body["singular_inventory"],
        "plural_inventory": preview_body["plural_inventory"],
        "invalid": invalid,
        "conflicts": conflicts,
        "preview_token": preview_token,
        "diagnostics": [],
        "next_actions": _exchange_migration_actions(posture),
    }


def apply_exchange_root_migration(
    service: Any,
    *,
    actor: str,
    expected_preview: str,
) -> dict[str, object]:
    """Apply one state-checked, conflict-free plural-root publication."""

    _required_actor(actor)
    inspection = inspect_exchange_root_migration(service)
    if inspection["preview_token"] != expected_preview:
        raise KaojuServiceError(
            "template_exchange_migration_stale",
            "Template exchange roots changed after preview; inspect migration again.",
        )
    posture = inspection["posture"]
    if posture in {
        "invalid",
        "conflicting",
        "explicit-legacy-binding",
        "nondefault-binding",
    }:
        raise KaojuServiceError(
            "template_exchange_migration_blocked",
            f"Template exchange-root migration is blocked with posture {posture}.",
        )
    if posture in {"singular-absent", "empty"}:
        return {
            **inspection,
            "mutated": False,
            "operation": "paper.template.migrate.exchange-root",
            "affected_refs": [],
        }
    singular = Path(str(inspection["singular_root"]))
    plural = Path(str(inspection["plural_root"]))
    singular_inventory, _ = _exchange_inventory(singular)
    plural_inventory, _ = _exchange_inventory(plural)
    plural.parent.mkdir(parents=True, exist_ok=True)
    staged = Path(
        tempfile.mkdtemp(
            prefix=f".{plural.name}.migration-",
            dir=plural.parent,
        )
    )
    observations: list[dict[str, object]] = []
    try:
        if plural.is_dir():
            _copy_exchange_tree(plural, staged)
        for identity, item in singular_inventory.items():
            if identity in plural_inventory:
                continue
            source = Path(str(item["path"]))
            target = staged / identity[0] / identity[1]
            _copy_exchange_tree(source, target)
            metadata_path = target / EXPORT_METADATA_NAME
            if metadata_path.is_file():
                metadata = _load_export_metadata(
                    metadata_path,
                    expected_kind=identity[0],
                )
                metadata.update(
                    {
                        "observed_path": str(
                            (plural / identity[0] / identity[1]).resolve(
                                strict=False
                            )
                        ),
                        "observed_at": _utc_now(),
                        "actor": actor,
                        "migration_source_path": str(source),
                    }
                )
                _atomic_write_json(metadata_path, metadata)
        staged_inventory, staged_invalid = _exchange_inventory(staged)
        if staged_invalid:
            raise KaojuServiceError(
                "template_exchange_migration_staging_invalid",
                "Staged plural exchange root failed inventory validation.",
                tuple(str(item) for item in staged_invalid),
            )
        expected_identities = set(plural_inventory) | set(singular_inventory)
        if set(staged_inventory) != expected_identities:
            raise KaojuServiceError(
                "template_exchange_migration_staging_invalid",
                "Staged plural exchange inventory is incomplete.",
            )
        for identity, item in staged_inventory.items():
            source_item = plural_inventory.get(identity) or singular_inventory[identity]
            if item["tree_digest"] != source_item["tree_digest"]:
                raise KaojuServiceError(
                    "template_exchange_migration_digest_mismatch",
                    f"Staged {identity[0]}/{identity[1]} digest changed during migration.",
                )
        _replace_directory(staged, plural)
        published_inventory, published_invalid = _exchange_inventory(plural)
        if published_invalid or {
            identity: item["tree_digest"]
            for identity, item in published_inventory.items()
        } != {
            identity: item["tree_digest"]
            for identity, item in staged_inventory.items()
        }:
            raise KaojuServiceError(
                "template_exchange_migration_verification_failed",
                "Published plural exchange root failed post-publication verification.",
            )
        for identity in sorted(set(singular_inventory) - set(plural_inventory)):
            target = plural / identity[0] / identity[1]
            metadata_path = target / EXPORT_METADATA_NAME
            if not metadata_path.is_file():
                continue
            metadata = _load_export_metadata(
                metadata_path,
                expected_kind=identity[0],
            )
            observations.append(
                _register_migrated_observation(
                    service,
                    metadata,
                    target,
                    actor=actor,
                )
            )
        shutil.rmtree(singular)
    finally:
        if staged.exists():
            shutil.rmtree(staged, ignore_errors=True)
    affected_refs: list[str] = []
    for observation in observations:
        raw_refs = observation.get("affected_refs")
        if isinstance(raw_refs, list):
            affected_refs.extend(str(ref) for ref in raw_refs)
    return {
        "ok": True,
        "mutated": True,
        "operation": "paper.template.migrate.exchange-root",
        "posture": "migrated",
        "singular_root": str(singular),
        "plural_root": str(plural),
        "preview_token": expected_preview,
        "observations": observations,
        "historical_observations_preserved": True,
        "canonical_records_rewritten": False,
        "affected_refs": affected_refs,
        "diagnostics": [],
        "next_actions": ["Use the plural role-aware exchange paths for future exports."],
    }


def _exchange_inventory(
    root: Path,
) -> tuple[dict[tuple[str, str], dict[str, object]], list[dict[str, object]]]:
    inventory: dict[tuple[str, str], dict[str, object]] = {}
    invalid: list[dict[str, object]] = []
    if not root.exists():
        return inventory, invalid
    if not root.is_dir() or root.is_symlink():
        return inventory, [
            {
                "code": "template_exchange_root_invalid",
                "path": str(root),
                "message": "Template exchange root is not a regular directory.",
            }
        ]
    for role in sorted(root.iterdir(), key=lambda item: item.name):
        if role.name not in TEMPLATE_KINDS or not role.is_dir() or role.is_symlink():
            invalid.append(
                {
                    "code": "template_exchange_role_invalid",
                    "path": str(role),
                    "message": "Exchange root may contain only content and latex role directories.",
                }
            )
            continue
        for child in sorted(role.iterdir(), key=lambda item: item.name):
            try:
                name = validate_template_name(child.name)
                digest = template_tree_digest(
                    child,
                    exclude_exchange_metadata=True,
                )
                metadata: dict[str, object] | None = None
                metadata_path = child / EXPORT_METADATA_NAME
                if metadata_path.is_file():
                    metadata = _load_export_metadata(
                        metadata_path,
                        expected_kind=role.name,
                    )
                    if metadata.get("template_name") != name:
                        raise KaojuServiceError(
                            "template_export_identity_invalid",
                            f"Export metadata does not name {role.name}/{name}.",
                        )
                inventory[(role.name, name)] = {
                    "template_kind": role.name,
                    "name": name,
                    "path": str(child.resolve(strict=False)),
                    "tree_digest": digest,
                    "export_metadata": metadata,
                }
            except KaojuServiceError as exc:
                invalid.append(
                    {
                        "code": exc.code,
                        "path": str(child),
                        "message": str(exc),
                    }
                )
    return inventory, invalid


def _inventory_json(
    inventory: Mapping[tuple[str, str], Mapping[str, object]],
) -> list[dict[str, object]]:
    return [
        dict(inventory[identity])
        for identity in sorted(inventory)
    ]


def _directory_snapshot_digest(root: Path) -> str | None:
    if not root.exists():
        return None
    digest = hashlib.sha256()
    for path in sorted(
        root.rglob("*"),
        key=lambda item: item.relative_to(root).as_posix(),
    ):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            return f"unsafe-symlink:{relative}"
        if not path.is_file():
            continue
        digest.update(relative.encode("utf-8"))
        digest.update(path.read_bytes())
    return f"sha256:{digest.hexdigest()}"


def _copy_exchange_tree(source: Path, target: Path) -> None:
    if source.is_symlink():
        raise KaojuServiceError(
            "template_symlink_forbidden",
            f"Template exchange tree cannot contain a symbolic link: {source}",
        )
    target.mkdir(parents=True, exist_ok=True)
    for path in sorted(
        source.rglob("*"),
        key=lambda item: item.relative_to(source).as_posix(),
    ):
        relative = path.relative_to(source)
        if path.is_symlink():
            raise KaojuServiceError(
                "template_symlink_forbidden",
                f"Template exchange tree cannot contain a symbolic link: {relative}",
            )
        destination = target / relative
        if path.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
        elif path.is_file():
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, destination)


def _register_migrated_observation(
    service: Any,
    metadata: Mapping[str, object],
    target: Path,
    *,
    actor: str,
) -> dict[str, object]:
    from isomer_labs.kaoju.template_defaults import load_packaged_template
    from isomer_labs.kaoju.template_support import TemplateSelection

    role_service = service.__class__(
        service.context,
        env=service.env,
        cwd=service.cwd,
        kind=str(metadata["template_kind"]),
    )
    if metadata.get("selection_source") == "packaged-default":
        packaged = load_packaged_template(str(metadata["template_kind"]))
        if (
            metadata.get("packaged_identity") != packaged.identity
            or metadata.get("canonical_tree_digest") != packaged.tree_digest
        ):
            return {
                "ok": False,
                "mutated": False,
                "posture": "source-changed",
                "path": str(target),
                "affected_refs": [],
            }
        selection = TemplateSelection(
            template_kind=packaged.template_kind,
            name=packaged.name,
            selection_source="packaged-default",
            root=packaged.root,
            tree_digest=packaged.tree_digest,
            authored_metadata=packaged.authored_metadata,
            packaged_identity=packaged.identity,
            packaged_resource_version=packaged.resource_version,
        )
    else:
        try:
            state = role_service.resolve_state(
                name=str(metadata["template_name"]),
                stable_ref=str(metadata["canonical_ref"]),
            )
        except KaojuServiceError:
            return {
                "ok": False,
                "mutated": False,
                "posture": "source-changed",
                "path": str(target),
                "affected_refs": [],
            }
        if (
            state.state_token != metadata.get("state_token")
            or state.tree_digest != metadata.get("canonical_tree_digest")
        ):
            return {
                "ok": False,
                "mutated": False,
                "posture": "source-changed",
                "path": str(target),
                "affected_refs": [],
            }
        selection = TemplateSelection.from_state(
            role_service.template_kind,
            state,
        )
    return role_service._register_export_observation(
        selection,
        target,
        actor=actor,
        operation="migrate",
    )


def _exchange_migration_actions(posture: object) -> list[str]:
    if posture == "explicit-legacy-binding":
        return [
            "Keep the explicit singular binding or change it deliberately before applying root migration."
        ]
    if posture == "nondefault-binding":
        return [
            "Keep the explicit custom binding or change it deliberately before applying built-in root migration."
        ]
    if posture in {"invalid", "conflicting"}:
        return [
            "Reconcile the reported paths without overwrite, then preview migration again."
        ]
    if posture in {"ready", "equivalent"}:
        return ["Apply migration with the exact preview token."]
    return []
