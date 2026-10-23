# Comprehensive independent audit: Introduction to Zoology v6.1.1-QA

**Date:** 23 October 2026. **Repository:** rameshgascngl-create/Introduction-to-Zoology-App. **Audited code:** branch phase2-native-source, commit 5d4d4a1a01cf4b3c5de84e427ed42c0c59bdf882. **Release verdict: BLOCKED.**

Evidence: all 28 chapter entries, 5 units, 58 PNG illustrations reviewed visually from source; Tamil/English assessment banks, native Android/Kotlin source, AndroidManifest, Gradle, static validator, three Android UI smoke tests, GitHub CI, course PDF and existing Phase II audit report. Device appearance, all prose scientific claims, Tamil editorial fidelity and asset redistribution rights have not been verified independently.

Native checked-in-source debug CI: https://github.com/rameshgascngl-create/Introduction-to-Zoology-App/actions/runs/39948257568 (PASS). Android emulator QA: https://github.com/rameshgascngl-create/Introduction-to-Zoology-App/actions/runs/39947866716 (FAIL; ADB device offline, not a demonstrated UI assertion failure).

## Executive gates

| Dimension | Status | Basis |
|---|---|---|
| 28 chapters in 5 units | STRUCTURE PASS | all have bilingual chapters, concept text, misconception, activity and pages |
| 58 plates | INVENTORY PASS, SCIENCE FAIL | all referenced; scientific arrows, Tamil glyph and clipping defects |
| 62 MCQs per language | PEDAGOGY FAIL | all 12 Unit V keys A; 40/62 keys A overall; no correct D |
| 41 short, 26 long prompts per language | INCOMPLETE | no rubrics, criteria or model answers |
| Native Android | BUILD PASS | successful checked-in source debug APK, Kotlin/Compose; no WebView |
| Emulator/device QA | UNVERIFIED | Android emulator ADB offline; no test assertions ran |
| Tamil diagram labels | FAIL | eight supplementary PNGs contain missing Tamil glyphs |
| IP/rights | BLOCKED | 11 figures reused from reference PDF, no asset-wise permission records |
| Play compliance | BLOCKED | Android targetSdk35, normal new/update Play submissions require 36 as of Aug 31 2026 |
| Release signing | BLOCKED | debug artifact only, no verified release/AAB signing pipeline |

## Every chapter — inventory, scope and findings

Approximate words count whitespace-separated text after HTML stripping; Tamil parity must be checked semantically, not merely by length.

| Chapter | Chapter title | EN word count | TA token count | Plates | Specific QA |
|---|---|---:|---:|---:|---|
| 1.1 | Introduction to Taxonomy & Systematics | 421 | 262 | 1 | Tamil text within systematic workflow figure illegible |
| 1.2 | Taxonomic Hierarchy | 403 | 248 | 3 | three redundant hierarchy charts; one omits Domain |
| 1.3 | Two Kingdom & Five Kingdom Classification | 320 | 245 | 1 | historical kingdom groupings correctly framed but not phylogenetic |
| 1.4 | Binomial Nomenclature | 364 | 229 | 2 | binomial typography must agree across text and illustrations |
| 1.5 | Different Phyla of Animal Kingdom | 369 | 230 | 1 | animal body-plan comparison has clipped leader |
| 1.6 | Salient Features of Invertebrates & Chordates | 349 | 223 | 1 | chordate tail label and note clipped |
| 2.1 | Cell Theory | 398 | 250 | 1 | Tamil rendered as boxes in supplementary cell theory plate |
| 2.2 | Ultrastructure of Prokaryotic & Eukaryotic Cells | 371 | 277 | 7 | seven plates, including three low-resolution reference scans; atlas label clipping |
| 2.3 | Mendelism & Inheritance | 440 | 338 | 3 | Mendel cross coverage present, source-scan dihybrid table requires independent key check |
| 2.4 | DNA and RNA | 381 | 277 | 3 | DNA and RNA notes graphic has obscured area, molecular hierarchy needs review |
| 2.5 | Central Dogma of Molecular Biology | 369 | 252 | 1 | retrovirus-only reverse transcription claim incorrect in graphic |
| 3.1 | Proteins | 334 | 240 | 2 | protein structural levels covered; check conformational depiction against diagrams |
| 3.2 | Carbohydrates | 303 | 212 | 3 | carbohydrate classification/structure present, verify chemical stereochemistry |
| 3.3 | Lipids | 327 | 231 | 2 | lipid chart present; taxonomy terminology needs contemporary scrutiny |
| 3.4 | Water & Vitamins | 400 | 243 | 2 | water-soluble-vitamin storage claim too absolute |
| 3.5 | Vital Physiological Organ Systems | 350 | 175 | 1 | one physiology plate; Tamil explanation shorter and needs parity review |
| 4.1 | Atmosphere & Its Strata | 337 | 208 | 1 | atmospheric graphic footer truncated |
| 4.2 | Habitats and Ecosystems | 482 | 371 | 2 | habitat/microhabitat/niche restored; solar arrow points into apex pyramid |
| 4.3 | Gametogenesis | 333 | 276 | 4 | meiosis labels wrong, stage-arrow overlaps, atlas requires app-background review |
| 4.4 | Fertilisation & Developmental Stages | 341 | 262 | 2 | developmental diagrams extremely schematic, validate stage representations |
| 4.5 | Origin of Life & Darwinism | 342 | 288 | 1 | natural selection content present, Tamil supplement plate unreadable |
| 4.6 | Modern Synthetic Theory (Neo-Darwinism) | 336 | 272 | 1 | genetic drift/gene flow causal graphics oversimplified |
| 5.1 | Aquaculture & Aquarium Keeping | 421 | 255 | 2 | biofilter arrow in aquarium nitrogen-cycle plate points wrong way |
| 5.2 | Apiculture (Bee Keeping) | 384 | 250 | 3 | bee caste PDF scan source rights; atlas label composite check |
| 5.3 | Sericulture | 373 | 244 | 2 | silkworm plate embedded Tamil unreadable; atlas captions check |
| 5.4 | Lac Culture & Vermiculture | 470 | 316 | 2 | lac flowchart incorrect order (harvest before secretion) |
| 5.5 | Poultry Keeping & Dairy Farming | 373 | 276 | 2 | poultry+dairy embedded Tamil broken and text overflowing |
| 5.6 | Biotechnology & Ecotourism | 409 | 303 | 2 | biotechnology+ecotourism embedded Tamil broken |

Unit illustration totals: 1=9, 2=15, 3=10, 4=11, 5=13. Unit II, Chapter 2.2 has seven illustrations while some chapters get one. Coverage of the official Foundation Course syllabus is structurally complete; no full academic sign-off of 28 chapter paragraphs has been established.

## All 58 illustration files — static visual audit

Transparent atlas PNGs may display black default SVG text as invisible in black-backed previews; verify composited over the app white background before labelling such text absent. Eight supplementary plates demonstrably display Tamil tofu glyphs in actual raster pixels.

| Chapter | PNG filename | Asset group | Evidence and disposition |
|---|---|---|---|
| 1.2 | original_orig1.png | original | Review: no severe fault established by static view, not a science sign-off. |
| 1.4 | original_orig2.png | original | P2: genus selection box intersects the scientific name. |
| 1.3 | original_orig3.png | original | Review: no severe fault established by static view, not a science sign-off. |
| 1.5 | original_orig4.png | original | P1: clitellum label clipped; oversimplified/ambiguous body-plan illustrations. |
| 1.6 | original_orig5.png | original | P1: post-anal-tail annotation and footnotes visibly clipped. |
| 2.2 | original_orig6.png | original | P1: several bacterial-cell label placements clash; anatomy/endpoints need checking. |
| 2.2 | original_orig7.png | original | Review: no severe fault established by static view, not a science sign-off. |
| 2.3 | original_orig8.png | original | Review: no severe fault established by static view, not a science sign-off. |
| 2.4 | original_orig9.png | original | Review: no severe fault established by static view, not a science sign-off. |
| 2.5 | original_orig10.png | original | P0: Reverse transcription restricted to retroviruses only (false; also telomerase/retrotransposons). |
| 3.1 | original_orig11.png | original | Review: no severe fault established by static view, not a science sign-off. |
| 3.2 | original_orig12.png | original | Review: no severe fault established by static view, not a science sign-off. |
| 3.3 | original_orig13.png | original | Review: no severe fault established by static view, not a science sign-off. |
| 3.4 | original_orig14.png | original | P2: water-soluble vitamins are presented as never stored (B12 exception). |
| 4.1 | original_orig15.png | original | P2: footer text cropped. |
| 4.2 | original_orig16.png | original | P0: solar-energy input arrow enters the top predator tier, rather than producers. |
| 4.3 | original_orig17.png | original | P0: meiosis I/II stage captions belong to wrong cell-stage transitions. |
| 4.4 | original_orig18.png | original | Review: no severe fault established by static view, not a science sign-off. |
| 4.6 | original_orig19.png | original | P2: causal flow conflates evolutionary variation with drift effects. |
| 5.1 | original_orig20.png | original | Review: no severe fault established by static view, not a science sign-off. |
| 5.2 | original_orig21.png | original | Review: no severe fault established by static view, not a science sign-off. |
| 5.4 | original_orig22.png | original | P2: node overlaps diagram title. |
| 1.1 | supplement_systflow.png | supplement | P0: all eight supplementary source PNGs rasterise Tamil labels as hollow square glyphs; some overflow boxes. |
| 2.1 | supplement_celltheory.png | supplement | P0: all eight supplementary source PNGs rasterise Tamil labels as hollow square glyphs; some overflow boxes. |
| 4.5 | supplement_darwinselection.png | supplement | P0: all eight supplementary source PNGs rasterise Tamil labels as hollow square glyphs; some overflow boxes. |
| 5.3 | supplement_silkworm.png | supplement | P0: all eight supplementary source PNGs rasterise Tamil labels as hollow square glyphs; some overflow boxes. |
| 5.5 | supplement_poultrybio.png | supplement | P0: all eight supplementary source PNGs rasterise Tamil labels as hollow square glyphs; some overflow boxes. |
| 5.5 | supplement_dairyhygiene.png | supplement | P0: all eight supplementary source PNGs rasterise Tamil labels as hollow square glyphs; some overflow boxes. |
| 5.6 | supplement_molecular.png | supplement | P0: all eight supplementary source PNGs rasterise Tamil labels as hollow square glyphs; some overflow boxes. |
| 5.6 | supplement_ecotourism.png | supplement | P0: all eight supplementary source PNGs rasterise Tamil labels as hollow square glyphs; some overflow boxes. |
| 1.2 | atlas_hierarchy.png | atlas | P2: omits Domain rank, whereas adjacent complete hierarchy includes it. |
| 2.2 | atlas_cell.png | atlas | P1: membrane and mitochondrion labels appear to extend outside graphic bounds. |
| 2.4 | atlas_dna.png | atlas | P2: extremely basic strand illustration with little molecular annotation. |
| 4.2 | atlas_ecosystem.png | atlas | P1: consumer labels cropped at edges. |
| 4.3 | atlas_gametes.png | atlas | Review: black on transparent preview can hide black SVG labels; inspect composited over white in app. |
| 4.4 | atlas_embryo.png | atlas | Review: verify stage labels and accuracy when rendered over app background. |
| 5.2 | atlas_bee.png | atlas | Review: simple illustration, must confirm caption labels on actual app background. |
| 5.3 | atlas_silk.png | atlas | Review: lifecycle graphic needs verified stage labels in app. |
| 1.2 | notes_p05.png | original-2026-corrected | Review: no severe fault established by static view, not a science sign-off. |
| 1.4 | notes_p13.png | original-2026-corrected | P2: scientific binomial appears nonitalicised despite nomenclature advice. |
| 2.2 | notes_p20.png | reference-notes | Review: no severe fault established by static view, not a science sign-off. |
| 2.2 | notes_p21.png | reference-notes | Review: no severe fault established by static view, not a science sign-off. |
| 2.2 | notes_p23.png | reference-notes | Review: no severe fault established by static view, not a science sign-off. |
| 2.2 | notes_p25.png | original-2026-corrected | Review: no severe fault established by static view, not a science sign-off. |
| 2.3 | notes_p28.png | original-2026-corrected | Review: no severe fault established by static view, not a science sign-off. |
| 2.3 | notes_p29.png | reference-notes | Review: no severe fault established by static view, not a science sign-off. |
| 2.4 | notes_p32.png | reference-notes | P1: scratched/obscured patch in reference graphic; provenance review. |
| 3.1 | notes_p36.png | reference-notes | Review: no severe fault established by static view, not a science sign-off. |
| 3.2 | notes_p38.png | reference-notes | Review: no severe fault established by static view, not a science sign-off. |
| 3.2 | notes_p39.png | reference-notes | Review: no severe fault established by static view, not a science sign-off. |
| 3.3 | notes_p40.png | reference-notes | Review: no severe fault established by static view, not a science sign-off. |
| 3.4 | notes_p42.png | reference-notes | Review: no severe fault established by static view, not a science sign-off. |
| 4.3 | notes_p57.png | original-2026-corrected | P1: green stage arrows obscure ploidy and meiotic-event text. |
| 4.3 | notes_p58.png | original-2026-corrected | P1: green stage arrows obscure oocyte arrest and meiotic text. |
| 5.2 | notes_p70.png | reference-notes | Review: no severe fault established by static view, not a science sign-off. |
| 3.5 | native_physio.png | original-2026 | Review: no severe fault established by static view, not a science sign-off. |
| 5.1 | native_aquarium.png | original-2026 | P1: biofilter arrow enters ammonia; show microbial nitrification at ammonia-to-nitrite-to-nitrate transformations. |
| 5.4 | native_lac.png | original-2026 | P0: harvest/process appears before crawler settlement and resin secretion in flow direction. |

**Key scientific repairs required:** gametogenesis-stage meiosis labelling, lac-harvest chronology, energy pyramid incoming sunlight to producers, reverse-transcription occurrence beyond retroviruses, and the misleading aquarium microbial arrow. Do not redraw a scientifically adequate image merely to homogenise style; repair proven errors in original editable masters, then re-rasterise and inspect.

**Legal source gate:** 11 reference-notes PNGs are copies derived from PDF notes; possession of notes is not automatically redistribution permission. Keep a provenance ledger for *each* PNG and master SVG including author, URL or origin, license and adaptation/attribution. No clear LICENSE or figure-rights ledger is checked into the audited tree.

## Full MCQ key audit

| Unit | Questions | Correct A | Correct B | Correct C | Correct D |
|---|---:|---:|---:|---:|---:|
| 1 | 12 | 4 | 6 | 2 | 0 |
| 2 | 12 | 3 | 9 | 0 | 0 |
| 3 | 14 | 10 | 4 | 0 | 0 |
| 4 | 12 | 11 | 1 | 0 | 0 |
| 5 | 12 | 12 | 0 | 0 | 0 |
| ALL | 62 | 40 | 20 | 2 | 0 |

- Unit V: all 12 keys are A; Unit IV 11/12 A; Unit II 9/12 B; never D in any unit. Students can predict correct choices. Balance key positions or randomise answer options while keeping the key aligned.
- Four English options contain Tamil: Unit 2 Q12, Unit 4 Q7, Unit 5 Q5 and Q10. Correct language separation.
- English and Tamil keys match positions in all checked MCQs; no duplicate options within a question and no exact duplicate English question text detected. This does not establish factual correctness of all distractors.
- No MCQ explanations, model short/long answers, grading rubrics or adaptive feedback are implemented. Current 62 items predominantly test factual recall. Add application, higher-order, practical and locally relevant cases and map questions to learning outcomes.
- Quiz uses transient Compose state, not permanent result history. Verify unit switches and process death restore with tests.

## Android architecture and engineering

**Code organisation: P1.** A single 720-line MainActivity.kt contains model parsing, data structures, navigation, all screens, image decoding, quizzes and SharedPreferences. Split typed content repository, screen-specific view models, navigation, reusable UI components and assessments. Current string routes and ad hoc returnView make back-stack correctness fragile. Data is loaded synchronously at Activity creation without a graceful malformed-content recovery state.

**Image memory and UX: P1.** The full-size PNG is decoded from assets for each NativePlate and PlateDialog using BitmapFactory.decodeStream and remember. There is no decode-to-target-resolution, bounded pan, prefetch policy or explicit bitmap cache budget. 58 plates and repeated full-screen navigation can stress low-memory devices; no actual OOM crash has been established. Profiles and device tests are necessary. Dialog pinch zoom works in code, but screen reader/button-only zoom controls and rich text alternatives are missing.

**Rich text / pedagogical hierarchy: P1.** Chapters contain HTML sections, h2/h3/h4, div class concept-note and ordered lists but are rendered through Android TextView Html.fromHtml. CSS class formatting is not applied by this renderer. Verify heading hierarchy, ordered-list indentation, formulas, selection, external links, Tamil fonts, line wraps and display-font magnification in actual screenshots. Search scans raw HTML instead of parsed plain text, returns matched chapters without location highlighting, and uses a linear scan.

**Navigation and saved state: P1.** Home, unit, search, bookmarks and quiz screens use Compose; completion/bookmark/language/font/last chapter stored via SharedPreferences. Screen string and current chapter saved via rememberSaveable but per-chapter scroll position not explicitly tracked. 'chapter' hides bottom tabs. Validate all history paths, Home/Back, rotation, lifecycle resume, double-tap zoom, three-button and gesture navigation. Android 15 edge-to-edge requires careful insets; source uses Scaffold but no actual runtime evidence demonstrates nav safety.

**Accessibility/localisation: P1.** Most buttons have semantics, but icons often null contentDescription, image text alternatives are generic, Tamil caption image labels largely embedded as English or rasterised tofu. Need TalkBack traversal, contrast, 200% text-size test, small-phone clipping test, RTL-independent flow, and Tamil spell/semantic review. English and Tamil chapter text are not proven equivalent; Chapter 3.5 Tamil materially shorter in simple word tokens, prompting review.

**Offline/privacy/security: low-to-medium risk.** Positive: no android.permission.INTERNET and no WebView, usesCleartextTraffic=false. Only launcher activity exported (normal). Manifest allows Backup and fullBackupContent; student preferences can be restored by OS, check privacy statement and data extraction rules. No apparent remote analytics or data transmission in audited source. No authentication is needed for a local textbook.

**Build reproducibility/release: P0.** minSdk24 compileSdk35 targetSdk35 versionCode611 versionName6.1.1-QA; content.json internal edition still 6.1.0 (can be valid content-baseline, label clearly). Kotlin 2.0.21, AGP8.7.3, Java17, Gradle8.10.2. For standard Android phone Google Play new or updated applications since 31 August 2026, targetSdk36 is required unless an approved exemption/extension (Nov 1 2026); private sideload QA does not face same Play gate. Release config has no signing key/pipeline; isMinifyEnabled=false. Commit Gradle wrapper, pin dependencies/action SHAs, record artifact SHA and SBOM, implement signed AAB + controlled keystore, and verify API36 edge-to-edge after migration. Disable risky source-export workflow dispatch after normal checked-in source branch is authoritative.

**QA methodology: P0.** tools/validate_content.py checks presence, lengths, counts, tags, 4-option MCQs, file signatures, PNG dimensions and exact hashes, but has no semantic/anatomical/translation/rights checks. Python assert statements can be disabled with python -O. Add structured schema, explicit errors, bilingual cross checks, option randomness and figure QA metadata, Android unit tests and screenshot-driven instrumentation.

**Existing instrumentation: 3 smoke tests only.** NativeReaderSmokeTest checks Chapter 1 Tamil+diagram dialog, bookmark recreation, quiz choice rotation. Emulator CI test APK compiled but runner ADB was offline repeatedly; do not count a UI test pass. Add tests on API24/29/33/35/36 emulators and at least one physical low-RAM device. Capture full page/touch screenshot evidence before approval.

## Formal remediation and acceptance checklist

| Ticket | Severity | Correction | Acceptance proof |
|---|---|---|---|
| ZOO-001 | P0 | Tamil missing glyphs in eight supplement illustrations | all re-rasterised plates with correct Tamil visually verified on phone |
| ZOO-002 | P0 | Fix meiosis sequence, lac production arrows, apex sunlight, reverse transcription | signed biology/editorial diagram review |
| ZOO-003 | P0 | Fix MCQ key pattern, mixed-language options and add explanations | independent key-check across 62 EN/TA MCQs |
| ZOO-004 | P0 | Figure permission/credits | source/licence/derivative ledger for 58 PNGs |
| ZOO-005 | P0 | Google Play target API and release signing | signed release AAB/APK; target36 or documented exception |
| ZOO-006 | P1 | Fix ADB emulator job then pass instrumented tests | screenshots, XML/test logs, rotated+Tamil+offline screens |
| ZOO-007 | P1 | Correct clipped labels/overlapping arrows in specific figures | clear 100% and 200% zoom, no arrow-to-label ambiguity |
| ZOO-008 | P1 | Correct bitmap memory/recreation and back-stack | stress test low RAM, 58 plates, repeated rotations |
| ZOO-009 | P1 | Review all Tamil conceptual parity and morphology captions | chapter-by-chapter sign-off by Tamil zoology editor |
| ZOO-010 | P2 | Modularise UI/content/test architecture | passing parser, quiz, navigation, state migration tests |

**Release gate:** P0 educational and licensing issues resolved -> all 28 bilingual lessons audited -> full 58-plate screenshot QA -> 62 MCQ keys/rationales -> emulator and physical-device PASS -> production-signed release and Play requirement satisfied. **No final release approval at this checkpoint.**

Sources: https://github.com/rameshgascngl-create/Introduction-to-Zoology-App/tree/phase2-native-source ; https://support.google.com/googleplay/android-developer/answer/11926878 ; https://developer.android.com/about/versions/15/behavior-changes-15
