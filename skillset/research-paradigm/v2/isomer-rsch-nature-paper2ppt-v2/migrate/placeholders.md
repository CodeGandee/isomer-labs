# Migration Placeholders

| Placeholder | Source Artifact or Route | Meaning | Producer or Caller | Consumer or Callee | Kind |
| --- | --- | --- | --- | --- | --- |
| <PAPER_PRESENTATION_SOURCE_PACKET> | paper metadata, claims, methods, results, figures, limitations | Extracted source packet for deck planning. | isomer-rsch-nature-paper2ppt-v2 | nature-paper2ppt | evidence |
| <PAPER_TYPE_CLASSIFICATION> | classified paper category | Paper type used to choose presentation logic. | isomer-rsch-nature-paper2ppt-v2 | nature-paper2ppt | decision |
| <CHINESE_PRESENTATION_PLAN> | Chinese slide sequence and story spine | Deck outline and logic in Chinese. | isomer-rsch-nature-paper2ppt-v2 | nature-paper2ppt, user | draft |
| <PRESENTATION_FIGURE_SELECTION> | selected evidence figures | Figure/panel selection based on argument value. | isomer-rsch-nature-paper2ppt-v2 | nature-paper2ppt | decision |
| <PRESENTATION_ASSET_MANIFEST> | output/assets/figures/ and asset_manifest.md | Prepared figure assets and provenance record. | isomer-rsch-nature-paper2ppt-v2 | nature-paper2ppt, user | figure |
| <CHINESE_SLIDE_CONTENT> | slide titles, bullets, captions, takeaways, speaker notes | Authored Chinese slide content. | isomer-rsch-nature-paper2ppt-v2 | nature-paper2ppt, user | draft |
| <PPTX_DECK> | output/final_presentation_cn.pptx | Editable Chinese PPTX deck. | isomer-rsch-nature-paper2ppt-v2 | user | report |
| <PPTX_QA_REPORT> | output/qa_report.md | Package, media, content, and optional render QA report. | isomer-rsch-nature-paper2ppt-v2 | user | report |
| <PPTX_REVISION_LOG> | render-inspect-revise defects and fixes | Defect and revision record for the deck. | isomer-rsch-nature-paper2ppt-v2 | user | report |
