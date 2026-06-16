# Nature-style paper→PPTX procedure (ported from DeepScientist `nature-paper2ppt`)

Build a complete but efficient Nature-style **simplified-Chinese** deck from a paper/preprint/notes. The
deliverable is a real `.pptx` (the current Houmao adapter emits an HTML deck as a fallback — treat this
file as the authoring spec for slide content + figure logic regardless of the final renderer).

## Argument spine (answer before building)
1. What is the problem and why does it matter? 2. What was the gap? 3. What is the core claim/contribution?
4. What is the technical route? 5. What is the strongest evidence (×3)? 6. How was it validated?
7. What are the limitations and the take-home?

## Default 12–16 slide structure
标题页 → 研究背景 → 知识缺口 → 核心主张 → 技术路线 → 关键证据①②③ → 验证 → 机制模型 → 创新点 → 局限 → 总结.

## Per-slide schema
`{中文标题, purpose, layout, 3–4 bullets, figure_asset, caption, takeaway, speaker_note}`. Treat
equal-weight 1:1 layouts as the exception; pick a hero panel per slide. Conclusion-style titles (a claim,
not a topic). Select ONLY the figures the story needs; extract them with a figure asset-manifest. Run a
light verification pass; never fabricate results not in the source.
