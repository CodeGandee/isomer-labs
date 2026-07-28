"""Typed contracts for history-aware Topic Git publication."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Mapping


class PublicationRefUpdateStrategy(StrEnum):
    NO_OP = "no-op"
    CREATE = "create"
    FAST_FORWARD = "fast-forward"
    FORCE_REPLACEMENT = "force-replacement"


class PublicationHistoryDisposition(StrEnum):
    RETAIN = "retain"
    PURGE = "purge"


@dataclass(frozen=True)
class PublicationHistoryCompatibility:
    compatible: bool
    evidence: tuple[str, ...]
    reason: str | None = None

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "compatible": self.compatible,
            "evidence": list(self.evidence),
        }
        if self.reason is not None:
            data["reason"] = self.reason
        return data

    @classmethod
    def from_json(cls, payload: Mapping[str, object]) -> PublicationHistoryCompatibility:
        raw_evidence = payload.get("evidence")
        return cls(
            compatible=bool(payload["compatible"]),
            evidence=(
                tuple(str(item) for item in raw_evidence)
                if isinstance(raw_evidence, list)
                else ()
            ),
            reason=str(payload["reason"]) if payload.get("reason") is not None else None,
        )


@dataclass(frozen=True)
class PublicationRefUpdate:
    ref: str
    strategy: PublicationRefUpdateStrategy
    planned_commit: str
    observed_commit: str | None = None
    base_commit: str | None = None
    compatibility: PublicationHistoryCompatibility = PublicationHistoryCompatibility(
        compatible=False,
        evidence=(),
    )
    fallback_reason: str | None = None

    def to_json(self) -> dict[str, object]:
        return {
            "ref": self.ref,
            "strategy": self.strategy.value,
            "observed_commit": self.observed_commit,
            "base_commit": self.base_commit,
            "planned_commit": self.planned_commit,
            "compatibility": self.compatibility.to_json(),
            "fallback_reason": self.fallback_reason,
        }

    @classmethod
    def from_json(cls, payload: Mapping[str, object]) -> PublicationRefUpdate:
        raw_compatibility = payload.get("compatibility")
        compatibility = (
            PublicationHistoryCompatibility.from_json(raw_compatibility)
            if isinstance(raw_compatibility, Mapping)
            else PublicationHistoryCompatibility(False, ())
        )
        return cls(
            ref=str(payload["ref"]),
            strategy=PublicationRefUpdateStrategy(str(payload["strategy"])),
            observed_commit=(
                str(payload["observed_commit"])
                if payload.get("observed_commit") is not None
                else None
            ),
            base_commit=(
                str(payload["base_commit"])
                if payload.get("base_commit") is not None
                else None
            ),
            planned_commit=str(payload["planned_commit"]),
            compatibility=compatibility,
            fallback_reason=(
                str(payload["fallback_reason"])
                if payload.get("fallback_reason") is not None
                else None
            ),
        )


@dataclass(frozen=True)
class HistoryAwarePublicationPlan:
    plan_id: str
    binding_id: str
    observed_refs: tuple[tuple[str, str], ...]
    expected_refs: tuple[tuple[str, str], ...]
    observed_tags: tuple[tuple[str, str], ...]
    expected_tags: tuple[tuple[str, str], ...]
    observed_remote_head: str | None
    history_disposition: PublicationHistoryDisposition
    ref_updates: tuple[PublicationRefUpdate, ...]
    push_order: tuple[str, ...]
    blockers: tuple[str, ...] = ()

    @property
    def ref_deletions(self) -> tuple[str, ...]:
        expected = {name for name, _ in self.expected_refs}
        return tuple(name for name, _ in self.observed_refs if name not in expected)

    @property
    def tag_deletions(self) -> tuple[str, ...]:
        expected = {name for name, _ in self.expected_tags}
        return tuple(name for name, _ in self.observed_tags if name not in expected)

    @property
    def provider_default_branch_action_required(self) -> bool:
        return self.observed_remote_head != "main"

    def to_json(self) -> dict[str, object]:
        return {
            "plan_id": self.plan_id,
            "binding_id": self.binding_id,
            "snapshot_mode": "exclusive_snapshot",
            "canonical_branch": "main",
            "history_disposition": self.history_disposition.value,
            "observed_remote_refs": dict(self.observed_refs),
            "expected_remote_refs": dict(self.expected_refs),
            "observed_remote_tags": dict(self.observed_tags),
            "expected_remote_tags": dict(self.expected_tags),
            "observed_remote_head": self.observed_remote_head,
            "expected_remote_head": "main",
            "ref_updates": [update.to_json() for update in self.ref_updates],
            "ref_deletions": list(self.ref_deletions),
            "tag_deletions": list(self.tag_deletions),
            "push_order": list(self.push_order),
            "blockers": list(self.blockers),
        }
