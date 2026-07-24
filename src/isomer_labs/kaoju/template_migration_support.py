"""Small presentation helpers for Kaoju template migrations."""

from __future__ import annotations

import builtins
from typing import Sequence


def migration_next_actions(
    candidates: Sequence[object],
) -> builtins.list[str]:
    """Describe the safe next migration step for active candidates."""

    if len(candidates) == 1:
        return [
            "Review the selected content and run template migrate to create mutable named template main.",
        ]
    if len(candidates) > 1:
        return [
            "Assign an explicit name to each distinct active legacy template before migration.",
        ]
    return []
