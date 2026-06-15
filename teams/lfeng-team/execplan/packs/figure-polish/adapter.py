"""figure-polish compiler adapter — render-inspect-revise QA on an existing SVG (stdlib only).

Deterministic post-processing of a figure produced upstream (e.g. by paper-plot): guarantee a white
background, add a thin frame, normalize the font family, and optionally stamp a title/caption. Returns
the QA tweaks applied. Entrypoint: render(...) (compiler kind). Style/QA only — does not invent data.
"""
from __future__ import annotations
import re
from pathlib import Path

_FONT = "Helvetica,Arial,sans-serif"


def render(*, command, input_path, out_path, params, quest_id):
    if not input_path:
        raise ValueError("figure-polish: --input <existing .svg> is required")
    src = Path(input_path)
    if not src.exists():
        raise FileNotFoundError(f"figure-polish: input not found: {input_path}")
    svg = src.read_text()
    if "<svg" not in svg:
        raise ValueError("figure-polish: input is not an SVG")
    params = params or {}
    notes = []

    m = re.search(r'<svg[^>]*\bwidth="([\d.]+)"[^>]*\bheight="([\d.]+)"', svg)
    if not m:
        m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    W, H = (float(m.group(1)), float(m.group(2))) if m else (720.0, 460.0)

    open_end = svg.index(">", svg.index("<svg")) + 1

    # 1) white background
    if "fill=\"white\"" not in svg[:open_end + 120]:
        svg = svg[:open_end] + f'\n<rect width="{W:.0f}" height="{H:.0f}" fill="white"/>' + svg[open_end:]
        notes.append("ensured white background")

    # 2) normalize font-family on the root <svg> if absent
    if "font-family" not in svg[:open_end]:
        svg = svg[:open_end - 1] + f' font-family="{_FONT}"' + svg[open_end - 1:]
        notes.append("normalized font-family")

    inserts = []
    # 3) thin frame
    inserts.append(f'<rect x="0.5" y="0.5" width="{W-1:.1f}" height="{H-1:.1f}" fill="none" stroke="#cccccc" stroke-width="1"/>')
    notes.append("added 1px frame")
    # 4) optional title / caption
    if params.get("title"):
        inserts.append(f'<text x="{W/2:.1f}" y="18" font-size="13" font-weight="bold" text-anchor="middle" fill="#222">{params["title"]}</text>')
        notes.append("stamped title")
    if params.get("caption"):
        inserts.append(f'<text x="{W/2:.1f}" y="{H-4:.1f}" font-size="10" text-anchor="middle" fill="#666">{params["caption"]}</text>')
        notes.append("stamped caption")

    svg = svg.replace("</svg>", "\n".join(inserts) + "\n</svg>")
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_text(svg)
    return {"ok": True, "out_path": out_path, "format": "svg",
            "summary": f"polished {src.name} ({len(notes)} QA tweaks)", "meta": {"qa_notes": notes}}
