"""Directory entry point for the UC-01 manual acceptance harness."""

from __future__ import annotations

import sys
from pathlib import Path

HARNESS_PARENT = Path(__file__).resolve().parent.parent
REPO_ROOT = Path(__file__).resolve().parents[3]
for path in (REPO_ROOT / "src", HARNESS_PARENT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

def _main() -> int:
    from uc01_headless_vertical_slice.runner import main

    return main()


if __name__ == "__main__":
    raise SystemExit(_main())
