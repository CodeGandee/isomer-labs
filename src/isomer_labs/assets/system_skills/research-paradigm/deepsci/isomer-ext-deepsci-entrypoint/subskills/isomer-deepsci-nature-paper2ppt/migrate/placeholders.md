# Migration Placeholders

| Placeholder | Source Artifact or Route | Meaning | Producer or Caller | Consumer or Callee | Kind |
| --- | --- | --- | --- | --- | --- |
| DEEPSCI:PAPER-PRESENTATION-SOURCE-PACKET | paper metadata, claims, methods, results, figures, limitations | Extracted source packet for deck planning. | isomer-rsch-nature-paper2ppt | nature-paper2ppt | evidence |
| DEEPSCI:PAPER-TYPE-CLASSIFICATION | classified paper category | Paper type used to choose presentation logic. | isomer-rsch-nature-paper2ppt | nature-paper2ppt | decision |
| DEEPSCI:CHINESE-PRESENTATION-PLAN | Chinese slide sequence and story spine | Deck outline and logic in Chinese. | isomer-rsch-nature-paper2ppt | nature-paper2ppt, user | draft |
| DEEPSCI:PRESENTATION-FIGURE-SELECTION | selected evidence figures | Figure/panel selection based on argument value. | isomer-rsch-nature-paper2ppt | nature-paper2ppt | decision |
| DEEPSCI:PRESENTATION-ASSET-MANIFEST | output/assets/figures/ and asset_manifest.md | Prepared figure assets and provenance record. | isomer-rsch-nature-paper2ppt | nature-paper2ppt, user | figure |
| DEEPSCI:CHINESE-SLIDE-CONTENT | slide titles, bullets, captions, takeaways, speaker notes | Authored Chinese slide content. | isomer-rsch-nature-paper2ppt | nature-paper2ppt, user | draft |
| DEEPSCI:PPTX-DECK | output/final_presentation_cn.pptx | Editable Chinese PPTX deck. | isomer-rsch-nature-paper2ppt | user | report |
| DEEPSCI:PPTX-QA-REPORT | output/qa_report.md | Package, media, content, and optional render QA report. | isomer-rsch-nature-paper2ppt | user | report |
| DEEPSCI:PPTX-REVISION-LOG | render-inspect-revise defects and fixes | Defect and revision record for the deck. | isomer-rsch-nature-paper2ppt | user | report |
