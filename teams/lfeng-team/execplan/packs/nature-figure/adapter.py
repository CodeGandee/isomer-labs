"""nature-figure compiler adapter — Nature/high-impact-style figure from data (stdlib only).

Like paper-plot but with submission conventions: Wong colorblind-safe palette, despined axes (left+bottom
only, ticks outward), bold lowercase panel label, Arial, larger fonts, no gridlines. Reads CSV/JSON,
writes a self-contained SVG. Entrypoint: render(...) (compiler kind).
"""
from __future__ import annotations
import csv
import json
from pathlib import Path

# Wong (2011) colorblind-safe palette.
_PALETTE = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00", "#56B4E9", "#000000"]


def _parse(input_path):
    p = Path(input_path)
    if not p.exists():
        raise FileNotFoundError(f"nature-figure: input not found: {input_path}")
    if p.suffix.lower() == ".json":
        d = json.loads(p.read_text())
        if isinstance(d, list):
            return "x", [float(r["x"]) for r in d], {"y": [float(r["y"]) for r in d]}
        xs = [float(v) for v in d["x"]]
        series = ({k: [float(v) for v in vs] for k, vs in d["series"].items()}
                  if "series" in d else {"y": [float(v) for v in d["y"]]})
        return d.get("x_label", "x"), xs, series
    rows = list(csv.reader(p.open()))
    h, body = rows[0], rows[1:]
    return h[0], [float(r[0]) for r in body], {h[i]: [float(r[i]) for r in body] for i in range(1, len(h))}


def _ticks(lo, hi, n=5):
    if hi == lo:
        hi = lo + 1.0
    return [lo + (hi - lo) * i / (n - 1) for i in range(n)]


def render(*, command, input_path, out_path, params, quest_id):
    if not input_path:
        raise ValueError("nature-figure: --input is required (CSV/JSON data)")
    xlabel, xs, series = _parse(input_path)
    params = params or {}
    title = params.get("title", "")
    panel = params.get("panel", "a")
    ylabel = params.get("y_label", "value")
    W, H, ML, MR, MT, MB = 560, 380, 64, 130, 40, 54
    x0, x1, y0, y1 = ML, W - MR, H - MB, MT
    xmin, xmax = min(xs), max(xs)
    ally = [v for vs in series.values() for v in vs]
    ymin, ymax = min(ally), max(ally)
    if ymin == ymax:
        ymin, ymax = ymin - 1, ymax + 1

    def sx(v): return x0 + (0 if xmax == xmin else (v - xmin) / (xmax - xmin)) * (x1 - x0)
    def sy(v): return y0 - (v - ymin) / (ymax - ymin) * (y0 - y1)

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Arial,Helvetica,sans-serif">',
         f'<rect width="{W}" height="{H}" fill="white"/>',
         f'<text x="10" y="24" font-size="18" font-weight="bold" fill="#000">{panel}</text>']
    if title:
        o.append(f'<text x="{(x0+x1)/2:.1f}" y="22" font-size="13" text-anchor="middle" fill="#000">{title}</text>')
    # despined: only left + bottom axes
    o.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="#000" stroke-width="1.4"/>')
    o.append(f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" stroke="#000" stroke-width="1.4"/>')
    for t in _ticks(ymin, ymax):
        y = sy(t)
        o.append(f'<line x1="{x0-5}" y1="{y:.1f}" x2="{x0}" y2="{y:.1f}" stroke="#000"/>')
        o.append(f'<text x="{x0-9}" y="{y+4:.1f}" font-size="12" text-anchor="end">{t:.3g}</text>')
    for t in _ticks(xmin, xmax):
        x = sx(t)
        o.append(f'<line x1="{x:.1f}" y1="{y0}" x2="{x:.1f}" y2="{y0+5}" stroke="#000"/>')
        o.append(f'<text x="{x:.1f}" y="{y0+19:.1f}" font-size="12" text-anchor="middle">{t:.3g}</text>')
    o.append(f'<text x="{(x0+x1)/2:.1f}" y="{H-12}" font-size="13" text-anchor="middle">{xlabel}</text>')
    o.append(f'<text x="16" y="{(y0+y1)/2:.1f}" font-size="13" text-anchor="middle" transform="rotate(-90 16 {(y0+y1)/2:.1f})">{ylabel}</text>')
    for i, (name, ys) in enumerate(series.items()):
        c = _PALETTE[i % len(_PALETTE)]
        pts = " ".join(f"{sx(x):.1f},{sy(y):.1f}" for x, y in zip(xs, ys))
        o.append(f'<polyline points="{pts}" fill="none" stroke="{c}" stroke-width="2.2"/>')
        for x, y in zip(xs, ys):
            o.append(f'<circle cx="{sx(x):.1f}" cy="{sy(y):.1f}" r="3.2" fill="{c}"/>')
        ly = MT + 8 + i * 18
        o.append(f'<line x1="{x1+16}" y1="{ly}" x2="{x1+34}" y2="{ly}" stroke="{c}" stroke-width="2.2"/>')
        o.append(f'<text x="{x1+38}" y="{ly+4}" font-size="12">{name}</text>')
    o.append("</svg>")
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_text("\n".join(o))
    return {"ok": True, "out_path": out_path, "format": "svg",
            "summary": f"nature-style: {len(series)} series x {len(xs)} pts, panel {panel}",
            "meta": {"series": list(series), "points": len(xs), "palette": "wong"}}
