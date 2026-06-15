"""nature-data template adapter — Data Availability statement + FAIR checklist (stdlib only).

Drafts a Markdown Data Availability statement, dataset citations, and a FAIR checklist STRICTLY from the
provided inventory. Missing identifiers are written as explicit `[to be assigned]` placeholders — it
never invents DOIs/accessions/repositories. Entrypoint: generate(...) (template kind).

Input JSON: {"datasets": [{"name","repository","accession","doi","url","access","license","notes"}],
             "code": {"repository","url","license"}}  # access: open|restricted|on-request
"""
from __future__ import annotations
import json
from pathlib import Path

_PH = "[to be assigned]"


def generate(*, command, input_path, out_path, params, quest_id):
    if not input_path:
        raise ValueError("nature-data: --input is required (data inventory JSON)")
    p = Path(input_path)
    if not p.exists():
        raise FileNotFoundError(f"nature-data: input not found: {input_path}")
    inv = json.loads(p.read_text())
    datasets = inv.get("datasets", [])
    code = inv.get("code")
    missing = []

    L = ["# Data Availability", ""]
    if not datasets:
        L.append("No datasets were declared in the inventory; complete the inventory before drafting.")
    else:
        parts = []
        for d in datasets:
            name = d.get("name", _PH)
            repo = d.get("repository", _PH)
            ident = d.get("doi") or d.get("accession") or d.get("url")
            if not ident:
                ident = _PH; missing.append(name)
            acc = d.get("access", "open")
            if acc == "open":
                parts.append(f"**{name}** is available in the {repo} repository ({ident}).")
            elif acc == "on-request":
                parts.append(f"**{name}** is available from the authors on reasonable request ({repo}, {ident}).")
            else:
                parts.append(f"**{name}** is subject to access restrictions; see {repo} ({ident})"
                             + (f"; license: {d['license']}." if d.get("license") else "."))
        L += [" ".join(parts), ""]
    if code:
        L += ["## Code Availability", "",
              f"Code is available at {code.get('repository', _PH)} ({code.get('url', _PH)})"
              + (f", license {code['license']}." if code.get("license") else "."), ""]

    L += ["## Dataset citations", ""]
    for i, d in enumerate(datasets, 1):
        L.append(f"{i}. {d.get('name', _PH)}. {d.get('repository', _PH)}. "
                 f"{d.get('doi') or d.get('accession') or d.get('url') or _PH}.")
    L += ["", "## FAIR checklist", ""]
    for d in datasets:
        nm = d.get("name", _PH)
        f_ = "yes" if (d.get("doi") or d.get("accession")) else "NO (persistent id missing)"
        a_ = "yes" if d.get("repository") else "NO (repository missing)"
        i_ = "yes" if d.get("format") else "review (declare format/standard)"
        r_ = "yes" if d.get("license") else "NO (license missing)"
        L.append(f"- **{nm}** — Findable: {f_}; Accessible: {a_}; Interoperable: {i_}; Reusable: {r_}")

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_text("\n".join(L) + "\n")
    return {"ok": True, "out_path": out_path, "format": "md",
            "summary": f"data-availability for {len(datasets)} dataset(s); {len(missing)} missing persistent ids",
            "meta": {"datasets": len(datasets), "missing_identifiers": missing}}
