"""Record construction helpers for the UC-01 manual harness."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path

from isomer_labs.models import EffectiveTopicContext
from isomer_labs.runtime.records import _provenance_ref, _slug
from isomer_labs.runtime.records import RuntimeLifecycleRecord, utc_timestamp

from uc01_headless_vertical_slice.constants import UC01_RESEARCH_TASK_ID, UC01_SEED_INQUIRY_ID


def base_records(context: EffectiveTopicContext, actor_ref: str) -> list[RuntimeLifecycleRecord]:
    now = utc_timestamp()
    return [
        RuntimeLifecycleRecord(
            id=UC01_SEED_INQUIRY_ID,
            record_kind="research_inquiry",
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            status="active",
            created_at=now,
            updated_at=now,
            lifecycle_refs={"research_topic_id": context.research_topic.id},
            transition_metadata={"uc01": True, "scope": "Flash Attention 4 direction selection", "actor_ref": actor_ref},
            provenance_refs=[_provenance_ref("research-inquiry", UC01_SEED_INQUIRY_ID)],
        ),
        RuntimeLifecycleRecord(
            id=UC01_RESEARCH_TASK_ID,
            record_kind="research_task",
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            status="active",
            created_at=now,
            updated_at=now,
            lifecycle_refs={"research_inquiry_id": UC01_SEED_INQUIRY_ID},
            transition_metadata={"uc01": True, "task": "literature-feature-factor-mapping", "actor_ref": actor_ref},
            provenance_refs=[_provenance_ref("research-task", UC01_RESEARCH_TASK_ID)],
        ),
        RuntimeLifecycleRecord(
            id="run-uc01-closeout",
            record_kind="run",
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            status="complete",
            created_at=now,
            updated_at=now,
            lifecycle_refs={"research_task_id": UC01_RESEARCH_TASK_ID, "research_inquiry_id": UC01_SEED_INQUIRY_ID},
            transition_metadata={"uc01": True, "workflow_stage": "closeout", "actor_ref": actor_ref},
            provenance_refs=[_provenance_ref("run", "run-uc01-closeout")],
        ),
    ]


def artifact_specs(route_classification: str) -> list[dict[str, object]]:
    return [
        {"id": "artifact-uc01-seed-source-summary", "kind": "seed_source_summary", "title": "Seed-source summaries"},
        {"id": "artifact-uc01-flash-attention-implementation-notes", "kind": "flash_attention_implementation_note", "title": "Flash Attention implementation notes"},
        {"id": "artifact-uc01-gb10-feature-notes", "kind": "gb10_feature_note", "title": "GB10 and Blackwell feature notes"},
        {"id": "artifact-uc01-attention-kernel-bottleneck-notes", "kind": "attention_kernel_bottleneck_note", "title": "Attention-kernel bottleneck notes"},
        {"id": "artifact-uc01-shape-family-constraints", "kind": "shape_family_constraint", "title": "Shape-family constraints"},
        {"id": "artifact-uc01-correctness-constraints", "kind": "correctness_constraint", "title": "Correctness constraints"},
        {"id": "artifact-uc01-review-notes", "kind": "review_note", "title": "Synthesis-review notes"},
        {"id": "artifact-uc01-follow-up-inquiry-options", "kind": "inquiry_option", "title": "Follow-up Research Inquiry options", "route_classification": route_classification},
        {"id": "artifact-uc01-decision-record", "kind": "decision_record_artifact", "title": "Follow-up inquiry decision artifact", "route_classification": route_classification},
    ]


def evidence_specs() -> list[dict[str, object]]:
    return [
        {"id": "evidence-uc01-gb10-feature-map", "relation_intent": "supports_direction_mapping", "quality": "fixture"},
        {"id": "evidence-uc01-attention-kernel-bottlenecks", "relation_intent": "supports_factor_clustering", "quality": "fixture"},
        {"id": "evidence-uc01-correctness-constraints", "relation_intent": "bounds_future_measurement", "quality": "fixture"},
    ]


def finding_specs() -> list[dict[str, object]]:
    return [
        {"id": "finding-uc01-memory-hierarchy-factor", "claim_candidate": "Memory hierarchy and asynchronous copy choices are candidate optimization factors."},
        {"id": "finding-uc01-tensor-core-precision-factor", "claim_candidate": "Tensor Core precision mode is a candidate investigation path subject to correctness constraints."},
        {"id": "finding-uc01-cluster-cooperation-factor", "claim_candidate": "Cluster-level cooperation may warrant measured follow-up after baseline scoping."},
    ]


def view_specs(
    artifact_refs: list[str],
    evidence_refs: list[str],
    finding_refs: list[str],
    route_classification: str,
) -> list[dict[str, object]]:
    return [
        {"id": "view-manifest-uc01-literature-matrix", "view_kind": "literature_matrix", "artifact_refs": artifact_refs[:4], "evidence_item_refs": evidence_refs},
        {"id": "view-manifest-uc01-claim-graph", "view_kind": "claim_graph", "finding_refs": finding_refs, "evidence_item_refs": evidence_refs},
        {
            "id": "view-manifest-uc01-inquiry-comparison",
            "view_kind": "inquiry_comparison",
            "artifact_refs": artifact_refs,
            "gate_ref": "gate-uc01-follow-up-inquiry",
            "decision_record_ref": "decision-uc01-follow-up-inquiry",
            "route_classification": route_classification,
        },
    ]


def artifact_record(
    context: EffectiveTopicContext,
    spec: dict[str, object],
    actor_ref: str,
) -> tuple[RuntimeLifecycleRecord, RuntimeLifecycleRecord]:
    artifact_id = str(spec["id"])
    content_path = context.topic_workspace_path / "artifacts" / "uc01" / f"{artifact_id}.md"
    title = str(spec["title"])
    lines = [
        f"# {title}",
        "",
        f"Research Topic: `{context.research_topic.id}`",
        f"Research Inquiry: `{UC01_SEED_INQUIRY_ID}`",
        f"Research Task: `{UC01_RESEARCH_TASK_ID}`",
        f"Artifact kind: `{spec['kind']}`",
    ]
    if "route_classification" in spec:
        lines.append(f"Route classification: `{spec['route_classification']}`")
    lines.extend(["", "This deterministic fixture artifact is produced by the UC-01 manual harness."])
    _write_text(content_path, "\n".join(lines) + "\n")
    return simple_record(
        context,
        "artifact",
        artifact_id,
        "ready",
        {**spec, "uc01": True},
        actor_ref,
        content_path=str(content_path),
    )


def simple_record(
    context: EffectiveTopicContext,
    record_kind: str,
    record_id: str,
    status: str,
    metadata: dict[str, object],
    actor_ref: str,
    *,
    content_path: str | None = None,
) -> tuple[RuntimeLifecycleRecord, RuntimeLifecycleRecord]:
    now = utc_timestamp()
    provenance_id = f"provenance-{_slug(record_id)}"
    provenance = RuntimeLifecycleRecord(
        id=provenance_id,
        record_kind="provenance_record",
        research_topic_id=context.research_topic.id,
        topic_workspace_id=context.topic_workspace_id,
        status="complete",
        created_at=now,
        updated_at=now,
        lifecycle_refs={"output_ref": record_id, "actor_ref": actor_ref},
        transition_metadata={"uc01": True, "action": f"record-{record_kind}", "source": "uc01-manual-harness"},
        provenance_refs=[],
    )
    record = RuntimeLifecycleRecord(
        id=record_id,
        record_kind=record_kind,
        research_topic_id=context.research_topic.id,
        topic_workspace_id=context.topic_workspace_id,
        status=status,
        created_at=now,
        updated_at=now,
        lifecycle_refs=_string_refs(metadata),
        transition_metadata=metadata,
        content_path=content_path,
        provenance_refs=[provenance_id],
    )
    return record, provenance


def complete_record(context: EffectiveTopicContext, record_id: str, actor_ref: str) -> RuntimeLifecycleRecord:
    now = utc_timestamp()
    return RuntimeLifecycleRecord(
        id=record_id,
        record_kind="research_task",
        research_topic_id=context.research_topic.id,
        topic_workspace_id=context.topic_workspace_id,
        status="complete",
        created_at=now,
        updated_at=now,
        lifecycle_refs={"research_inquiry_id": UC01_SEED_INQUIRY_ID, "actor_ref": actor_ref},
        transition_metadata={"uc01": True, "completed_by": "uc01-manual-harness"},
        provenance_refs=[_provenance_ref("research-task", record_id)],
    )


def _string_refs(metadata: dict[str, object]) -> dict[str, str]:
    refs: dict[str, str] = {"research_inquiry_id": UC01_SEED_INQUIRY_ID}
    for key, value in metadata.items():
        if isinstance(value, str) and (key.endswith("_ref") or key.endswith("_id") or key == "route_classification"):
            refs[key] = value
    return refs


def _write_text(path: Path, content: str) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return sha256(content.encode("utf-8")).hexdigest()

