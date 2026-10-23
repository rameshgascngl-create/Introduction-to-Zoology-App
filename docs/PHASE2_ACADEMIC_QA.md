# Phase II academic, asset and Android QA audit

**Baseline:** 23 October 2026 · branch `phase2-native-source` · departmental *Introduction to Zoology Unit I to V Notes.pdf* (85 pages; prescribed syllabus on PDF page 3).

## Verified inventory (static)

| Unit | Prescribed scope | App chapters | Assigned plates | Current assessment |
|---|---|---:|---:|---|
| I | Biodiversity, taxonomy, two- and five-kingdom classifications, nomenclature, animal phyla, chordates | 6 | 9 | Structurally present |
| II | Cell theory, prokaryotic/eukaryotic cells, organelles, Mendelian inheritance, DNA/RNA, central dogma | 5 | 15 | Structurally present |
| III | Proteins, carbohydrates, lipids, water, vitamins and organ systems | 5 | 10 | Structurally present |
| IV | Atmosphere, habitat, ecosystem, gametogenesis, fertilisation, development, origin of life, Darwinism and modern synthesis | 6 | 11 | Habitat gap corrected in 4.2 |
| V | Aquaculture, aquarium keeping, apiculture, sericulture, lac culture, vermiculture, poultry, dairy, biotechnology and ecotourism | 6 | 13 | Structurally present |
| **Total** | | **28** | **58** | |

Assessment counts in original v6.1 package: 62 MCQs per language, 41 short-answer prompts per language and 26 long-answer prompts per language. Presence is verified; pedagogical validity of every question requires human review.

## Changes implemented in Phase II

1. Restored and committed the ordinary Android/Kotlin/Gradle project, 58 PNG plates and 47 SVG sources to a separate branch; the packaged-source workflow remains available for reconstruction.
2. Added definitions and a fieldwork activity for **habitat, microhabitat and ecological niche** in Chapter 4.2 in English and Tamil; clarified that habitat and niche are not interchangeable.
3. Extended the static QA gate to require this syllabus topic and Tamil body text, verify PNG file signatures and minimum dimensions, and reject exact duplicate PNGs.
4. Established a separate CI path to build subsequent checked-in source edits without overwriting them with the earlier packed payload.

## Acceptance criteria — open, not silently assumed complete

- [ ] Each of 58 plates: verify morphology, labels, arrow endpoints, and the correct chapter association against an authoritative reference; correct material scientific errors
- [ ] Each source image: document author, source, licence or written permission, adaptation status and required attribution before public distribution
- [ ] Review the 11 reference-note figures separately for redistribution rights
- [ ] Validate Tamil terminology for all 28 chapters with a Tamil-medium zoology reviewer
- [ ] On a physical Android device: inspect portrait/landscape, bottom navigation, Back behaviour, zooming and scroll state
- [ ] Inspect all long Tamil passages for font fallback, clipping and accessibility contrast; test increased font size
- [ ] Verify offline startup, persistence of bookmarks/completion, rotation and app resume
- [ ] Compare every MCQ answer key with the teaching text and syllabus; verify explanatory depth for each chapter
- [ ] Produce and verify a release-signed artifact with a known signing identity only after device QA

## Known limitations

The existing validation script proves structural integrity, not anatomical correctness. An exact-hash uniqueness check catches byte-identical images, not reused diagrams with resized/relabelled pixels. The 58 displayed image assignments do not establish that the images render legibly on a physical device. The supplied PDF contains some previously identified problematic figures; the v6.1 source replaces six but retains eleven from the notes. Treat **rights and specialist figure inspection as release blockers**, not as reasons to prevent a development APK.

**Release gate:** native build PASS → device screenshot QA → bilingual scientific/editorial review → source and asset rights audit → signed release.
