"""nature-polishing template adapter — deterministic English polishing + editor notes (stdlib only).

Style ONLY: mechanical fixes (whitespace/punctuation/capitalization) + a conservative formal phrasebank.
It never adds, removes, or strengthens claims. Subjective issues (weasel words, long sentences, passive
hints) are surfaced as *suggestions* in an editor-notes section, not auto-applied. Entrypoint: generate(...).

Input: a text/Markdown file. Output: polished Markdown + a `## Editor notes` section.
"""
from __future__ import annotations
import re
from pathlib import Path

# Conservative formal substitutions (lexical, claim-neutral). Each entry: (regex, replacement, human-label)
# — the human-label is what the editor notes show (never the raw regex). These NEVER strengthen a claim;
# verb-strengthening rewrites (e.g. show->demonstrate) are deliberately excluded — that is the opposite of
# the Nature overclaim guidance, which softens claim verbs.
_PHRASEBANK = [
    (r"\ba lot of\b", "many", "a lot of"), (r"\blots of\b", "many", "lots of"),
    (r"\bin order to\b", "to", "in order to"),
    (r"\bdue to the fact that\b", "because", "due to the fact that"),
    (r"\bin spite of the fact that\b", "although", "in spite of the fact that"),
    (r"\butilize\b", "use", "utilize"), (r"\bbig\b", "large", "big"),
]
_WEASEL = ["very", "really", "quite", "somewhat", "clearly", "obviously", "significantly improved", "state-of-the-art"]
# Overclaim verbs/adjectives (Nature style-guardrails): flag as SUGGESTIONS to soften — never auto-rewrite.
_OVERCLAIM = ["prove", "proves", "proven", "conclusively", "unprecedented", "superior", "the best",
              "for the first time", "breakthrough"]


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
    for pat, repl, label in _PHRASEBANK:
        new = re.sub(pat, repl, polished, flags=re.IGNORECASE)
        if new != polished:
            applied.append(f"'{label}' -> '{repl}'")  # human-readable, not the raw regex
        polished = new

    # suggestions (NOT applied)
    suggestions = []
    for w in _WEASEL:
        n = len(re.findall(r"\b" + re.escape(w) + r"\b", text, flags=re.IGNORECASE))
        if n:
            suggestions.append(f"consider removing/qualifying '{w}' ({n}x)")
    for w in _OVERCLAIM:
        n = len(re.findall(re.escape(w), text, flags=re.IGNORECASE))
        if n:
            suggestions.append(f"soften overclaiming term '{w}' ({n}x) — Nature style prefers show/suggest/"
                               "to our knowledge/among the strongest")
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
