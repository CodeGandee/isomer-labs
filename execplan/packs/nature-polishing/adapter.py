"""nature-polishing template adapter — deterministic English polishing + editor notes (stdlib only).

Style ONLY: mechanical fixes (whitespace/punctuation/capitalization) + a conservative formal phrasebank.
It never adds, removes, or strengthens claims. Subjective issues (weasel words, long sentences, passive
hints) are surfaced as *suggestions* in an editor-notes section, not auto-applied. Entrypoint: generate(...).

Input: a text/Markdown file. Output: polished Markdown + a `## Editor notes` section.
"""
from __future__ import annotations
import re
from pathlib import Path

# Conservative formal substitutions (lexical, claim-neutral).
_PHRASEBANK = [
    (r"\ba lot of\b", "many"), (r"\blots of\b", "many"), (r"\bin order to\b", "to"),
    (r"\bdue to the fact that\b", "because"), (r"\bin spite of the fact that\b", "although"),
    (r"\butilize\b", "use"), (r"\bbig\b", "large"), (r"\bgot\b", "obtained"),
    (r"\bshow that\b", "demonstrate that"),
]
_WEASEL = ["very", "really", "quite", "somewhat", "clearly", "obviously", "significantly improved", "state-of-the-art"]


def _mechanical(text):
    notes = []
    t = text
    t2 = re.sub(r"[ \t]{2,}", " ", t)
    if t2 != t:
        notes.append("collapsed repeated spaces")
    t = t2
    t2 = re.sub(r"\s+([,.;:!?])", r"\1", t)
    if t2 != t:
        notes.append("removed space before punctuation")
    t = t2
    t2 = re.sub(r"([,.;:!?])([A-Za-z])", r"\1 \2", t)
    if t2 != t:
        notes.append("added space after punctuation")
    t = t2
    # sentence-start capitalization (simple)
    def cap(m): return m.group(1) + m.group(2).upper()
    t = re.sub(r"(^|[.!?]\s+)([a-z])", cap, t)
    return t, notes


def generate(*, command, input_path, out_path, params, quest_id):
    if not input_path:
        raise ValueError("nature-polishing: --input is required (text/markdown)")
    p = Path(input_path)
    if not p.exists():
        raise FileNotFoundError(f"nature-polishing: input not found: {input_path}")
    text = p.read_text()
    polished, notes = _mechanical(text)
    applied = []
    for pat, repl in _PHRASEBANK:
        new = re.sub(pat, repl, polished, flags=re.IGNORECASE)
        if new != polished:
            applied.append(f"{pat} -> {repl}")
        polished = new

    # suggestions (NOT applied)
    suggestions = []
    for w in _WEASEL:
        n = len(re.findall(r"\b" + re.escape(w) + r"\b", text, flags=re.IGNORECASE))
        if n:
            suggestions.append(f"consider removing/qualifying '{w}' ({n}x)")
    longs = [s for s in re.split(r"(?<=[.!?])\s+", text) if len(s.split()) > 40]
    if longs:
        suggestions.append(f"{len(longs)} sentence(s) exceed 40 words — consider splitting")
    if re.search(r"\b(was|were|been|is|are)\s+\w+ed\b", text):
        suggestions.append("passive-voice constructions detected — prefer active voice where natural")

    out = [polished.rstrip(), "", "## Editor notes (suggestions only; claims unchanged)", ""]
    out += [f"- mechanical: {', '.join(notes) or 'none'}"]
    out += [f"- phrasebank applied: {', '.join(applied) or 'none'}"]
    out += [f"- {s}" for s in suggestions] or ["- no stylistic suggestions"]
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_text("\n".join(out) + "\n")
    return {"ok": True, "out_path": out_path, "format": "md",
            "summary": f"polished prose ({len(notes)} mechanical, {len(applied)} phrasebank, {len(suggestions)} suggestions)",
            "meta": {"mechanical": notes, "phrasebank": applied, "suggestions": suggestions}}
