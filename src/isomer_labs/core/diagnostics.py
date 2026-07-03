"""Stable diagnostics for Isomer CLI validation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal


Severity = Literal["error", "warning"]


@dataclass(frozen=True)
class Diagnostic:
    """A deterministic validation diagnostic."""

    code: str
    severity: Severity
    concept: str
    message: str
    path: Path | None = None
    field: str | None = None
    line: int | None = None
    hint: str | None = None
    usage: str | None = None
    examples: tuple[str, ...] = ()

    @property
    def is_error(self) -> bool:
        return self.severity == "error"

    def render(self) -> str:
        parts = [self.severity.upper(), self.code, self.concept]
        if self.path is not None:
            parts.append(str(self.path))
        if self.field is not None:
            parts.append(self.field)
        location = " | ".join(parts)
        lines = [f"{location}: {self.message}"]
        if self.hint is not None:
            lines.append(f"  Hint: {self.hint}")
        if self.usage is not None:
            lines.append(f"  Usage: {self.usage}")
        if self.examples:
            lines.append("  Examples:")
            lines.extend(f"    {example}" for example in self.examples)
        return "\n".join(lines)

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "code": self.code,
            "severity": self.severity,
            "concept": self.concept,
            "message": self.message,
        }
        if self.path is not None:
            data["path"] = str(self.path)
        if self.field is not None:
            data["field"] = self.field
        if self.line is not None:
            data["line"] = self.line
        if self.hint is not None:
            data["hint"] = self.hint
        if self.usage is not None:
            data["usage"] = self.usage
        if self.examples:
            data["examples"] = list(self.examples)
        return data


def has_errors(diagnostics: list[Diagnostic]) -> bool:
    return any(diagnostic.is_error for diagnostic in diagnostics)
