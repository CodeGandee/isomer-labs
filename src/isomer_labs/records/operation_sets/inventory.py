"""Worker-boundary resolution, inventory, and manifest reconciliation."""

from __future__ import annotations

from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence
import hashlib
import mimetypes
import os
import stat

from isomer_labs.core.diagnostics import Diagnostic, has_errors
from isomer_labs.core.path_utils import is_within
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.runtime.records import _slug
from isomer_labs.workspace.manifest import EffectiveAgentContext, EffectiveTopicActorContext, resolve_worker_output_policy
from isomer_labs.workspace.path_resolution import resolve_effective_agent_context, resolve_effective_topic_actor_context

from .models import (
    OPERATION_SET_CONTROL_DIR,
    OPERATION_SET_DEFAULT_MANIFEST,
    OperationSetAcceptanceManifest,
    OperationSetInventoryEntry,
    OperationSetOutput,
    ResolvedOperationSet,
    _context_failure_payload,
    _diagnostic,
    _has_item_errors,
    _item_diagnostic,
    _manifest_error,
    file_digest,
    load_operation_set_manifest,
    write_operation_set_manifest,
)

def resolve_operation_set(
    context: EffectiveTopicContext,
    operation_set_path: Path,
    *,
    env: Mapping[str, str],
    cwd: Path,
    agent_name: str | None = None,
    topic_actor_name: str | None = None,
) -> tuple[ResolvedOperationSet | None, list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    if agent_name is not None and topic_actor_name is not None:
        diagnostics.append(_diagnostic("operation_set_worker_ambiguous", "Select exactly one Agent or Topic Actor for operation-set acceptance."))
        return None, diagnostics
    agent_context: EffectiveAgentContext | None = None
    actor_context: EffectiveTopicActorContext | None = None
    if agent_name is not None:
        agent_context, context_diagnostics = resolve_effective_agent_context(
            context,
            env=env,
            cwd=cwd,
            explicit_agent_name=agent_name,
        )
        diagnostics.extend(context_diagnostics)
    elif topic_actor_name is not None:
        actor_context, context_diagnostics = resolve_effective_topic_actor_context(
            context,
            env=env,
            cwd=cwd,
            explicit_topic_actor_name=topic_actor_name,
        )
        diagnostics.extend(context_diagnostics)
    else:
        inferred_agent, agent_diagnostics = resolve_effective_agent_context(context, env=env, cwd=cwd, missing_is_error=False)
        inferred_actor, actor_diagnostics = resolve_effective_topic_actor_context(context, env=env, cwd=cwd, missing_is_error=False)
        if inferred_agent is not None and inferred_actor is not None:
            diagnostics.append(_diagnostic("operation_set_worker_ambiguous", "Both Agent and Topic Actor context resolve; select one explicitly."))
            return None, diagnostics
        if inferred_agent is not None:
            agent_context = inferred_agent
            diagnostics.extend(agent_diagnostics)
        elif inferred_actor is not None:
            actor_context = inferred_actor
            diagnostics.extend(actor_diagnostics)
        else:
            diagnostics.extend(agent_diagnostics)
            diagnostics.extend(actor_diagnostics)
            diagnostics.append(_diagnostic("operation_set_worker_missing", "Operation-set acceptance requires one Agent or Topic Actor context."))
            return None, diagnostics
    if has_errors(diagnostics):
        return None, diagnostics
    policy, policy_diagnostics = resolve_worker_output_policy(
        context,
        env=env,
        agent_context=agent_context,
        topic_actor_context=actor_context,
    )
    diagnostics.extend(policy_diagnostics)
    if policy is None or has_errors(diagnostics):
        return None, diagnostics
    candidate = operation_set_path if operation_set_path.is_absolute() else cwd / operation_set_path
    root = candidate.resolve(strict=False)
    output_root = policy.output_root.path.resolve(strict=False)
    if not candidate.exists() or not candidate.is_dir() or candidate.is_symlink():
        diagnostics.append(_diagnostic("operation_set_root_invalid", "Operation-set root must be an existing non-symlink directory.", path=candidate))
        return None, diagnostics
    if root == output_root or not is_within(root, output_root):
        diagnostics.append(_diagnostic("operation_set_root_escape", "Operation-set root must be a child of the selected worker output root.", path=root))
        return None, diagnostics
    relative = root.relative_to(output_root).as_posix()
    identity_digest = hashlib.sha256(f"{policy.worker_kind}:{policy.worker_name}:{relative}".encode()).hexdigest()[:12]
    operation_set_id = f"operation-set-{_slug(policy.worker_kind)}-{_slug(policy.worker_name)}-{_slug(relative)}-{identity_digest}"
    worker_scope_ref = agent_context.scope_ref if agent_context is not None else actor_context.scope_ref if actor_context is not None else ""
    return (
        ResolvedOperationSet(
            root=root,
            output_root=output_root,
            worker_kind=policy.worker_kind,
            worker_name=policy.worker_name,
            worker_scope_ref=worker_scope_ref,
            relative_path=relative,
            operation_set_id=operation_set_id,
        ),
        diagnostics,
    )


def inventory_operation_set(root: Path) -> tuple[list[OperationSetInventoryEntry], list[dict[str, object]]]:
    inventory: list[OperationSetInventoryEntry] = []
    diagnostics: list[dict[str, object]] = []

    def visit(directory: Path) -> None:
        try:
            entries = sorted(os.scandir(directory), key=lambda item: item.name)
        except OSError as exc:
            diagnostics.append(_item_diagnostic("operation_set_directory_unreadable", f"Cannot read operation-set directory: {exc}", path=directory))
            return
        for entry in entries:
            path = Path(entry.path)
            relative = path.relative_to(root).as_posix()
            if relative == OPERATION_SET_CONTROL_DIR or relative.startswith(f"{OPERATION_SET_CONTROL_DIR}/"):
                continue
            try:
                mode = entry.stat(follow_symlinks=False).st_mode
            except OSError as exc:
                diagnostics.append(_item_diagnostic("operation_set_entry_unreadable", f"Cannot inspect operation-set entry: {exc}", path=path))
                continue
            if stat.S_ISLNK(mode):
                target = path.resolve(strict=False)
                code = "operation_set_symlink_escape" if not is_within(target, root) else "operation_set_symlink_unsupported"
                diagnostics.append(_item_diagnostic(code, "Operation-set symlinks are not followed or accepted.", path=path, target=str(target)))
            elif stat.S_ISDIR(mode):
                visit(path)
            elif stat.S_ISREG(mode):
                try:
                    size = path.stat().st_size
                    digest = file_digest(path)
                except OSError as exc:
                    diagnostics.append(_item_diagnostic("operation_set_file_unreadable", f"Cannot read operation-set file: {exc}", path=path))
                    continue
                inventory.append(
                    OperationSetInventoryEntry(
                        path=relative,
                        digest=digest,
                        size_bytes=size,
                        media_type=mimetypes.guess_type(relative)[0],
                    )
                )
            else:
                diagnostics.append(_item_diagnostic("operation_set_special_file_unsupported", "Operation-set special files are not accepted.", path=path))

    visit(root)
    return sorted(inventory, key=lambda item: item.path), diagnostics


def scaffold_operation_set_manifest(
    context: EffectiveTopicContext,
    resolved: ResolvedOperationSet,
    inventory: Sequence[OperationSetInventoryEntry],
) -> OperationSetAcceptanceManifest:
    allocated: set[str] = set()
    outputs: list[OperationSetOutput] = []
    for index, item in enumerate(inventory):
        base = _slug(PurePosixPath(item.path).stem or f"output-{index + 1}")
        key = base
        suffix = 2
        while key in allocated:
            key = f"{base}-{suffix}"
            suffix += 1
        allocated.add(key)
        outputs.append(
            OperationSetOutput(
                key=key,
                path=item.path,
                digest=item.digest,
                size_bytes=item.size_bytes,
                media_type=item.media_type,
            )
        )
    return OperationSetAcceptanceManifest(
        operation_set_id=resolved.operation_set_id,
        revision=1,
        research_topic_id=context.research_topic.id,
        topic_workspace_id=context.topic_workspace_id,
        worker_kind=resolved.worker_kind,
        worker_name=resolved.worker_name,
        outputs=tuple(outputs),
        record_intents=(),
    )


def inspect_operation_set(
    context: EffectiveTopicContext,
    operation_set_path: Path,
    *,
    env: Mapping[str, str],
    cwd: Path,
    agent_name: str | None = None,
    topic_actor_name: str | None = None,
    manifest_path: Path | None = None,
    write_scaffold: bool = False,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    resolved, diagnostics = resolve_operation_set(
        context,
        operation_set_path,
        env=env,
        cwd=cwd,
        agent_name=agent_name,
        topic_actor_name=topic_actor_name,
    )
    if resolved is None:
        return _context_failure_payload("operation-sets.inspect", diagnostics), diagnostics
    inventory, inventory_diagnostics = inventory_operation_set(resolved.root)
    selected_manifest_path = manifest_path
    if selected_manifest_path is None:
        default_path = resolved.root / OPERATION_SET_CONTROL_DIR / OPERATION_SET_DEFAULT_MANIFEST
        if default_path.exists() or write_scaffold:
            selected_manifest_path = default_path
    manifest: OperationSetAcceptanceManifest | None = None
    manifest_diagnostics: list[dict[str, object]] = []
    if selected_manifest_path is not None and selected_manifest_path.exists():
        _require_manifest_control_path(selected_manifest_path, resolved.root)
        manifest = load_operation_set_manifest(selected_manifest_path)
        manifest_diagnostics.extend(_manifest_context_diagnostics(context, resolved, manifest))
        manifest_diagnostics.extend(_reconcile_manifest(inventory, manifest, require_dispositions=True))
    mutated = False
    if write_scaffold:
        if selected_manifest_path is None:
            raise _manifest_error("operation_set_manifest_path_missing", "A scaffold path could not be resolved.")
        if selected_manifest_path.exists():
            raise _manifest_error("operation_set_manifest_exists", f"Refusing to overwrite existing operation-set manifest: {selected_manifest_path}")
        manifest = scaffold_operation_set_manifest(context, resolved, inventory)
        write_operation_set_manifest(selected_manifest_path, manifest)
        mutated = True
        manifest_diagnostics.extend(_reconcile_manifest(inventory, manifest, require_dispositions=True))
    all_diagnostics = [*inventory_diagnostics, *manifest_diagnostics]
    return {
        "ok": not _has_item_errors(all_diagnostics),
        "mutated": mutated,
        "operation": "operation-sets.inspect",
        "resolved": resolved.to_json(),
        "inventory": [item.to_json() for item in inventory],
        "inventory_count": len(inventory),
        "manifest_path": str(selected_manifest_path.resolve(strict=False)) if selected_manifest_path is not None else None,
        "manifest": manifest.to_json() if manifest is not None else None,
        "manifest_digest": manifest.digest if manifest is not None else None,
        "reconciled": manifest is not None and not _has_item_errors(all_diagnostics),
        "diagnostics": all_diagnostics,
    }, diagnostics


def _manifest_context_diagnostics(
    context: EffectiveTopicContext,
    resolved: ResolvedOperationSet,
    manifest: OperationSetAcceptanceManifest,
) -> list[dict[str, object]]:
    diagnostics: list[dict[str, object]] = []
    expected = {
        "research_topic_id": context.research_topic.id,
        "topic_workspace_id": context.topic_workspace_id,
        "worker_kind": resolved.worker_kind,
        "worker_name": resolved.worker_name,
        "operation_set_id": resolved.operation_set_id,
    }
    observed = {
        "research_topic_id": manifest.research_topic_id,
        "topic_workspace_id": manifest.topic_workspace_id,
        "worker_kind": manifest.worker_kind,
        "worker_name": manifest.worker_name,
        "operation_set_id": manifest.operation_set_id,
    }
    for field_name, expected_value in expected.items():
        if observed[field_name] != expected_value:
            diagnostics.append(
                _item_diagnostic(
                    "operation_set_manifest_context_mismatch",
                    f"Manifest {field_name} does not match resolved operation-set context.",
                    field=field_name,
                    expected=expected_value,
                    observed=observed[field_name],
                )
            )
    return diagnostics


def _reconcile_manifest(
    inventory: Sequence[OperationSetInventoryEntry],
    manifest: OperationSetAcceptanceManifest,
    *,
    require_dispositions: bool,
) -> list[dict[str, object]]:
    diagnostics: list[dict[str, object]] = []
    inventory_by_path = {item.path: item for item in inventory}
    manifest_by_path = {item.path: item for item in manifest.outputs}
    for path in sorted(set(inventory_by_path) - set(manifest_by_path)):
        diagnostics.append(_item_diagnostic("operation_set_output_unclassified", "Material operation-set file is absent from the manifest.", path=path))
    for path in sorted(set(manifest_by_path) - set(inventory_by_path)):
        diagnostics.append(_item_diagnostic("operation_set_manifest_output_missing", "Manifest output does not exist in the operation set.", path=path))
    for path in sorted(set(inventory_by_path) & set(manifest_by_path)):
        observed = inventory_by_path[path]
        declared = manifest_by_path[path]
        if observed.digest != declared.digest or observed.size_bytes != declared.size_bytes:
            diagnostics.append(
                _item_diagnostic(
                    "operation_set_output_drift",
                    "Operation-set output size or digest differs from the manifest.",
                    path=path,
                    expected_digest=declared.digest,
                    observed_digest=observed.digest,
                    expected_size_bytes=declared.size_bytes,
                    observed_size_bytes=observed.size_bytes,
                )
            )
        if require_dispositions and declared.disposition is None:
            diagnostics.append(_item_diagnostic("operation_set_output_disposition_missing", "Manifest output lacks an acceptance disposition.", path=path))
        if declared.disposition == "disposable" and declared.reason is None:
            diagnostics.append(_item_diagnostic("operation_set_disposable_reason_missing", "Disposable output requires a concrete reason.", path=path))
        if declared.disposition in {"record_payload", "record_attachment"} and declared.record_key is None:
            diagnostics.append(_item_diagnostic("operation_set_output_record_key_missing", "Durable output disposition requires a record_key.", path=path))
    intent_keys = {item.key for item in manifest.record_intents}
    for output in manifest.outputs:
        if output.record_key is not None and output.record_key not in intent_keys:
            diagnostics.append(_item_diagnostic("operation_set_output_record_key_unknown", "Output refers to an unknown record intent.", path=output.path, record_key=output.record_key))
    return diagnostics


def _require_manifest_control_path(path: Path, root: Path) -> None:
    candidate = path.resolve(strict=False)
    control_root = (root / OPERATION_SET_CONTROL_DIR).resolve(strict=False)
    if not is_within(candidate, control_root):
        raise _manifest_error("operation_set_manifest_path_escape", "Operation-set manifest must stay inside the reserved control directory.")
