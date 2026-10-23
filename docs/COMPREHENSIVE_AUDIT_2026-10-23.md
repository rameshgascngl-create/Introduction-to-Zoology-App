# Introduction to Zoology v6.1.1-QA — Comprehensive Product, Academic, Asset and Android Audit

**Audit date:** 2026-10-23. **Exact repository revision:** `5d4d4a1a01cf4b3c5de84e427ed42c0c59bdf882`, branch `phase2-native-source`. **Disposition: NOT APPROVED FOR PRODUCTION OR UNSUPERVISED STUDENT RELEASE.**

## 1. Scope, method, and evidence limitations
- Inspected the checked-in Gradle project, Kotlin `MainActivity.kt`, `AndroidManifest.xml`, content JSON schema and all chapter/assessment records, tests, validation code, CI workflows and their latest reported outcomes.
- Audited the five-unit 28-chapter inventory against the formal syllabus on page 3 of `Introduction to Zoology Unit I to V Notes.pdf` (85-page departmental reference). The PDF is the scope baseline; it is not a blanket scientific correctness or redistribution licence.
- Checked the 58 chapter-to-plate assignments and viewed all 58 image assets across original, supplement, atlas, revised and reference-note groups at tool-preview scale. This is a **visual sample-context review**, not proof of Android rendering on an actual phone, label-by-label anatomical certification, or legal rights clearance.
- Classified findings as **CONFIRMED SOURCE / IMAGE**, **CONFIRMED CI**, **DESIGN WEAKNESS**, or **UNVERIFIED RUNTIME**. No physical Android device was operated and no image was modified during this audit.
- `content.json` content was scanned programmatically by chapter for title/body/activity/misconception presence, topical heading structure, approximate space-delimited word count, image mapping and assessment-answer distributions. Space-delimited counts are *not* a fair standalone measure of Tamil translation quality.

## 2. Verified project inventory and academic depth
| Unit | Chapter count | Plate assignments | English approx. words | Tamil approx. space-separated words | MCQ / short / long (per language) |
|---|---:|---:|---:|---:|---:|
| I Animal biodiversity and systematics | 6 | 9 | 2,226 | 1,437 | 12 / 8 / 5 |
| II Cell biology and genetics | 5 | 15 | 1,959 | 1,394 | 12 / 8 / 5 |
| III Biochemistry and physiology | 5 | 10 | 1,714 | 1,101 | 14 / 9 / 6 |
| IV Ecology, development and evolution | 6 | 11 | 2,171 | 1,677 | 12 / 8 / 5 |
| V Entrepreneurial zoology | 6 | 13 | 2,430 | 1,644 | 12 / 8 / 5 |
| **Total** | **28** | **58** | **10,500** | **7,253** | **62 / 41 / 26** |

**What passes:** every chapter has English/Tamil lesson text, title, a misconception note, a classroom activity and source page references; every chapter is assigned at least one plate; all five syllabus units appear. **What does not follow:** every topic is developed sufficiently, the bilingual coverage is equivalent, or the figures are correct. The course is a two-credit introductory foundation course, but a marketed 'detailed textbook' needs more than basic topical presence.

## 3. Chapter-by-chapter findings and required academic review
| Chapter | Covered subject | Audit judgment and precise improvement requirement |
|---|---|---|
| 1.1 | Taxonomy and systematics | Topic and practical decision sequence present. Separate nomenclatural validity from phylogenetic placement; review dense repeated expansion prose and Tamil parity. The one attached supplementary plate has Tamil rendering failure. |
| 1.2 | Taxonomic hierarchy | Hierarchy present with three near-overlapping diagrams; consolidate the pedagogy into one full Domain-to-Species worked example and avoid repeated diagrams. Check species concepts beyond interbreeding. |
| 1.3 | Two/five kingdoms | Historical classification present. Label Whittaker's categories unequivocally historical; do not present the five kingdom split as a resolved phylogenetic tree. Compare three-domain / modern evidence explicitly. |
| 1.4 | Binomial nomenclature | Scientific naming present. Diagram `original_orig2.png` misaligns genus/specific-epithet boxes with the words; must replace or repair. Verify ICZN terminology and italicisation. |
| 1.5 | Animal phyla | Phylum features present; ensure an accurate diagnostic character matrix rather than a progress ladder. `original_orig4.png` right-hand clitellum label crowds the frame. |
| 1.6 | Invertebrates and chordates | Diagnostic features present, but `original_orig5.png` has clipped post-anal-tail annotation; update image and check notochord/dorsal nerve cord/pharyngeal features. |
| 2.1 | Cell theory | Historical theory and qualifications present. Supplementary cell-division graphic has missing Tamil glyphs. Expand contemporary examples distinguishing acellular viruses and special cell types. |
| 2.2 | Prokaryotic/eukaryotic ultrastructure | Major cell components present. Seven figures assigned to one chapter with duplicated general cell schematics; rationalise, add organelle-to-function and plant/animal comparison, examine `original_orig6.png` label collision. |
| 2.3 | Mendelism | Classical crosses and probability present; both a Punnett and a stepwise cross are assigned. Verify 9:3:3:1 dependence on independent assortment, parent/gamete labels and all genotype-phenotype keys. |
| 2.4 | DNA and RNA | Chemistry/structure present. Original/reference/atlas drawings duplicate aspects; clarify polarity, antiparallel strands, DNA vs RNA exceptions, base-pairing and source-image usage rights. |
| 2.5 | Central dogma | Replication/transcription/translation and exceptions present. `original_orig10.png` falsely restricts reverse transcription to retroviruses; cover retrotransposons, telomerase and relevant examples correctly. |
| 3.1 | Proteins | Amino acids, bonds, structural levels present. Contrast structural hierarchy with interactions and functional examples; compare the two assigned figures for clarity and consistency. |
| 3.2 | Carbohydrates | Major groups present. `notes_p38.png` classification is elementary; teach glycosidic linkage and reducing sugars explicitly and audit `notes_p39.png` chemical geometry/rights. |
| 3.3 | Lipids | Main types present. `notes_p40.png` presents fatty acids under triglycerides as though a taxonomic subgroup; replace that hierarchy with structural-class/constituent distinctions and check overlapping steroid/sterol grouping. |
| 3.4 | Water and vitamins | Solvent properties/vitamin categories present. `original_orig14.png` makes the unqualified claim that water-soluble vitamins are 'not stored'; explain exceptions such as B12. Consider deficiency matrix with species-relevant examples. |
| 3.5 | Vital organ systems | The topic was added and lists ten systems, but **approximately 350 English and 175 Tamil space-delimited words cover all systems together**: insufficient as a detailed treatment. Expand each system's core structures, sequence of function, regulation and cross-system examples; strengthen Tamil treatment. |
| 4.1 | Atmosphere strata | Layers are present; check altitude trends vs schematic boundaries. `original_orig15.png` overlays the stratosphere text with the ozone annotation. |
| 4.2 | Habitats and ecosystems | Habitat/microhabitat/niche gap was corrected. **Critical** `original_orig16.png` arrow shows solar energy into apex carnivores instead of primary producers. Correct energy-flow directions and distinguish matter cycles. |
| 4.3 | Gametogenesis | Both germ-cell processes present. **Critical** `original_orig17.png` places meiosis labels under inappropriate transitions. `notes_p57.png`/`notes_p58.png` arrows obscure ploidy/stage captions; map arrest points, meiosis I and II, ploidy and final products. |
| 4.4 | Fertilisation and development | Early stages appear. Explain cleavage, blastula, gastrulation and germ-layer contribution carefully; avoid implying the same geometrical morphology in every animal group. Atlas image must be checked with a light compositing background. |
| 4.5 | Origin of life and Darwinism | Distinction between chemical origin and biological evolution is explained. Supplement's Tamil glyphs are broken in the raster; include experimentally grounded examples and avoid teleological wording. |
| 4.6 | Modern synthesis | Mutation, gene flow, drift and selection present. `original_orig19.png` arrows can mislead by placing drift/gene flow solely as origins of heritable variation; distinguish forces altering allele frequencies from sources of new alleles. |
| 5.1 | Aquaculture and aquarium keeping | Both syllabus topics explicitly present. Refine species-specific husbandry and ammonia/nitrite/nitrate route; `native_aquarium.png` arrow toward water changes is ambiguous. |
| 5.2 | Apiculture | Colony castes and roles present with three alternative illustrations. Consolidate an accurate figure, clarify worker task polymorphism and locally relevant honey-bee species; verify reused caste image rights. |
| 5.3 | Sericulture | Metamorphosis/culture sequence present. Supplement Tamil labels are broken; clarify pupal biology, host plant suitability, disease management and harvesting ethics. |
| 5.4 | Lac culture and vermiculture | Both topics explicitly present. `native_lac.png` arrow sequence places harvest ahead of crawler settlement/resin deposition, scientifically wrong; correct production workflow. `original_orig22.png` overlaps header with a process node. |
| 5.5 | Poultry/dairy | Biosecurity, welfare, dairy hygiene present. Both supplementary diagrams render Tamil glyphs as squares; add measurable management parameters and applicable hygiene indicators with references. |
| 5.6 | Biotechnology/ecotourism | Both topics present but share one chapter and limited depth. PCR/evidence and ecotourism supplementary figures contain missing Tamil glyphs; add method controls, interpretation, environmental safeguards and examples. |

## 4. Confirmed figure defects and provenance
**Asset composition:** 22 `original`, 8 `supplement`, 8 `atlas`, 6 `original-2026-corrected`, 11 `reference-notes`, 3 `original-2026` = 58 assigned plates. The current validator asserts valid PNG signatures, ≥300 px width and ≥100 px height, unique SHA-256 bytes, target file existence and source SVG existence when declared. **None of these checks prove correctness of labels, layout or licensing.**

| Severity | Files | Confirmed visual/content defect |
|---|---|---|
| Critical | `original_orig16.png` | Solar energy arrow points to the apex of the trophic pyramid rather than producers. |
| Critical | `original_orig17.png` | Meiosis I/II labels do not align with the proper spermatogenesis transitions. |
| High | `native_lac.png` | Process arrows show harvest before crawler settlement/resin deposition. |
| High | `original_orig2.png` | Genus and specific-epithet highlight regions do not correctly delineate *Panthera leo*. |
| High | `supplement_systflow.png`, `supplement_celltheory.png`, `supplement_darwinselection.png`, `supplement_silkworm.png`, `supplement_poultrybio.png`, `supplement_dairyhygiene.png`, `supplement_molecular.png`, `supplement_ecotourism.png` | All eight supplementary PNGs render Tamil strings as placeholder rectangles; some Tamil strings cross box boundaries. Their SVG source includes actual Tamil characters: regenerate using proper Tamil font support and verify raster visually. |
| High | `notes_p57.png`, `notes_p58.png` | Meiosis stage arrows overlap explanatory text, rendering important ploidy-stage labels hard to read. |
| Medium | `original_orig10.png` | 'Retroviruses only' reverse-transcription restriction is false. |
| Medium | `original_orig14.png` | 'Water-soluble ... not stored' is unqualified and scientifically misleading. |
| Medium | `original_orig5.png`, `original_orig6.png`, `original_orig15.png`, `original_orig22.png` | Cropped label, collided legends, text crossing ozone line and header/node overlap respectively. |
| Medium | `notes_p40.png` | Lipid classification confuses fatty acid components with structural lipid categories. |
| Medium | `atlas_cell.png`, `atlas_ecosystem.png` | Edge labels clipped by composition/viewBox in the inspection rendering. |
| Review | 8 `atlas_*.png` images | Preview surfaces render transparent pixels black; labels that are black may be invisible *in the preview only*. Since the reader places them on a light backdrop, **do not call all atlas labels missing without on-device light-background screenshots**. Validate the actual compositing and edge clipping. |
| Review | 11 `reference-notes` files | Authorship, copyright, permission, source and adaptation details not provided in per-plate metadata. Redistribution clearance is NOT demonstrated. |

**Asset placement finding:** every chapter has ≥1 registered plate; this proves catalogue assignment only. There are multiple overlapping instructional figures (e.g., 7 in Chapter 2.2, 4 in Chapter 4.3, 3 in Chapter 1.2). Review for redundant coverage. Scientific figures should be approved by *subject accuracy + legibility + attribution + placement*, not by asset count.

## 5. Assessment-bank audit
- Verified: 62 MCQs per language; English and Tamil answer letters agree; 41 short-answer and 26 long-answer prompts per language; each MCQ has four alternatives and a valid A–D key; no exact duplicate English question stems were detected in this data pass.
- **Confirmed key imbalance:** Across 62 English MCQs, answer positions are A=40, B=20, C=2, D=0. Unit IV is A=11/12; Unit V is A=12/12. This makes guessing and memorising answer positions viable. Randomise *option ordering together with answer-key updates*, not the stored key alone.
- **Confirmed language leakage:** English options contain Tamil text in Unit II Q12, Unit IV Q7, Unit V Q5 and Unit V Q10. Correct in English without corrupting the Tamil bank.
- **Confirmed missing remediation:** All 62 MCQs lack answer-specific explanations/rationales. UI only reveals answer letters and score; it does not explain why alternatives are wrong.
- **Content quality:** Several questions test direct recall rather than application, inference, diagram recognition, scientific evidence interpretation or numeracy; no difficulty tags, learning-outcome tags, randomized question order, distractor analytics or per-question feedback.
- **Design:** Quiz answers are saved for configuration changes via `rememberSaveable` while the screen remains in composition; durable score history, per-topic diagnosis and across-app-restart attempt tracking are not implemented.
- **Acceptance:** independent academic key audit, rebalanced position histogram, reasoned explanations for all 62, bilingual semantic equivalence check and at least one application/interpretation item per syllabus subtopic.

## 6. Native Android architecture and implementation audit
| Concern | Observed source evidence | Priority / consequence |
|---|---|---|
| Native implementation | Kotlin 2.0.21, Compose Material3, Gradle 8.10.2, AGP 8.7.3; no WebView or app INTERNET permission; `MainActivity` uses Compose and Android TextView. | PASS for native architecture and offline packaging. |
| Monolithic UI | `MainActivity.kt` has ~720 source lines and includes domain parsing, mutable state, navigation, reader, image zoom, quiz and persistence. | Medium: split into data repository, view-model, navigation, reader, image component and assessments for testability. |
| Eager load | `Syllabus.load(this)` parses entire bundled JSON in `onCreate` on main thread; no loading/error screen. | Medium: startup-jank and malformed-content crash *risks*, not measured defects. |
| Storage | `SharedPreferences` saves language, text size, bookmark/completion sets and last chapter; quiz is not persisted as history. | Medium: add structured durable attempt/progress model and upgrade migration tests. |
| Navigation | String states `home`, `unit`, `search`, `bookmarks`, `quiz`, `chapter`; handcrafted Back transitions. | Medium: return destination can change while paging within chapter; add navigation-state tests and clear error fallback. |
| Long lessons | Each chapter is HTML markup passed through `Html.fromHtml()` into native `TextView`; CSS classes and advanced HTML semantics are not preserved as browser CSS. | Medium: check heading hierarchy, ordered-list numbering, links and Tamil formatted display under native HTML parser. |
| Image loading | `BitmapFactory.decodeStream` inside composable `remember` decodes full PNG for each visible plate and again for full-screen dialog. | Medium: duplicate decode/memory-jank risk; use dimension-aware sampling, caching and failure telemetry. |
| Image zoom | Up to 5× scale, unbounded pan offset, no fit-to-screen clamp. | Medium: possible off-screen lost image or awkward recovery; physical touch validation required. |
| Orientation | Manifest `android:configChanges="orientation|screenSize|uiMode"`; Compose saveable state and custom handling. | Medium: verify insets, state and dark/light theme transitions on real devices. |
| Accessibility | Image inline content descriptions use raw filenames; many text labels are 11–13sp; mixed dark-mode/static custom colors. | High: add descriptive bilingual semantics, contrast/font-scaling audit, TalkBack and switch-access checks. |
| Assets | SVG masters and rendered PNG images are both packaged in assets although runtime reads PNGs. | Low/medium: separate source masters from runtime assets or otherwise document packaging strategy. |
| Resources/icon | Manifest contains no `android:icon`; source tree has no standard app `res` launcher assets. | Medium: app branding/launcher-icon acceptance gap. |
| Errors | Image load failures show literal English 'Diagram unavailable' and JSON load errors are not caught at startup. | Medium: implement bilingual recovery and explicit content error reporting. |
| Privacy/backup | No Internet permission and cleartext disabled; Android backup enabled for app data. | Low: review backup/data-handling expectations and store disclosure, no exfiltration mechanism observed. |
| Release | `versionCode=611`, `versionName=6.1.1-QA`, content edition=`6.1.0`; targetSdk=35; release has no configured signing identity. | High: reconcile versions, target API and signed AAB production workflow. |
| Build reproducibility | CI pins Gradle 8.10.2 but no `gradlew` wrapper is checked in. Several historical workflows coexist with the checked-in source workflow. | Medium: add wrapper and archive/disable dangerous payload-reconstruction workflows. |

### Google Play requirement (time-sensitive)
Google Play has required new standard Android phone/tablet apps and updates submitted from **31 August 2026** to target **API 36**, subject to an approved extension. Current `targetSdk = 35` is therefore **not compliant for an ordinary new/update submission on 23 October 2026 without applicable extension**; existing-app discoverability has a separate API 35 rule. Official: https://support.google.com/googleplay/android-developer/answer/11926878 and https://developer.android.com/google/play/requirements/target-sdk . Direct sideloading/debug QA is a different channel and is not blocked by this Play submission criterion.

## 7. QA, release safety and reliability evidence
- Last successful source build: GitHub Actions **39948257568** at commit `5d4d4a1`, including content integrity, Kotlin compilation, package and debug-signature checks. Produces **debug APK**, not signed release or AAB.
- UI/emulator workflow **39947866716** did **not pass**. The app and androidTest APK compiled, but device repeatedly reported `adb: device offline`; the test failure is emulator infrastructure, not proof of a failing in-app assertion. Do **not** claim that portrait navigation, Tamil rendering, bookmarks, rotation, TalkBack or zoom passed.
- Existing instrumented smoke suite has **three tests**, targeting chapter 1.1 diagram + Tamil, bookmark recreation, and quiz rotation. It does not cover each unit/chapter, multi-font sizes, accessibility, repeated open-close image decoding, lower-memory phones or release mode.
- The existing structural validator does not evaluate scientific causal-arrow order, Tamil glyph rasterisation, clipping, licence terms, publisher attribution, biased answer positions or release-target policy.
- Remaining tests: Android 13/14/15/16, small phone/tablet, 3-button/gesture navigation, 100–200% text-scale, offline cold start, app resume/kill/restore, process memory and zoom gestures, rotation with open dialog, 28-chapter navigation screenshots, every diagram on light/dark reader background, bilingual test submissions and real device accessibility service.

## 8. Prioritised defect register and resolution gates
**P0 — block classroom/production acceptance until corrected**
1. P0-01 Science: `original_orig16.png` sun-to-apex-carnivore arrow → fix energy flow at producer base; add subject-review check.
2. P0-02 Science: `original_orig17.png` misplaced meiosis labels → redraw properly with stage-specific ploidy transitions.
3. P0-03 Visual bilingual: all 8 supplement PNGs render Tamil tofu boxes → restore Tamil-capable rasterisation and visually inspect rendered PNG bytes.
4. P0-04 Science: `native_lac.png` wrong process order → correct crawler establishment, feeding/resin secretion, harvest, and processing.
5. P0-05 Release: image reuse provenance and permissions for all 11 reference-note rasters unknown → obtain rights/attribution or replace with licensed alternatives before public distribution.

**P1 — high priority before declaring student-quality QA pass**
6. P1-01 `original_orig2.png` genus/epithet regions misaligned.
7. P1-02 `notes_p57.png`, `notes_p58.png` arrows obscure key descriptions; `original_orig5.png`, `original_orig6.png` label clipping/collision.
8. P1-03 Correct `original_orig10.png` reverse-transcription restriction and `original_orig14.png` vitamin storage oversimplification.
9. P1-04 MCQ key placement skew A40/B20/C2/D0; fix all four English/Tamil mixed-distractor errors and write 62 feedback rationales.
10. P1-05 Improve Unit III Chapter 3.5 explanatory depth and all short Tamil coverage areas; do chapter-by-chapter bilingual scientific review.
11. P1-06 Repair emulator/ADB runner and obtain actual screenshots, XML/test result evidence; no app-level runtime PASS yet.
12. P1-07 Upgrade and test `targetSdk` / `compileSdk` to 36 and configure reproducible production-signed AAB only after release gates.
13. P1-08 Resolve atlas/image clipping and visually inspect all 58 assets in the actual Compose reader at normal and enlarged size.

**P2 — important engineering/pedagogy improvements**
14. P2-01 Split `MainActivity`, separate repository/domain/UI/test code and introduce robust loading/failure screen.
15. P2-02 Add image sampling/cache, bounded pan/zoom, scroll-state recovery and font/accessibility QA.
16. P2-03 Add native resources/app icon, bilingual image error strings, learning objectives and in-app source/credits ledger.
17. P2-04 Standardise publication version identity, Gradle wrapper, modern release workflow and disable stale packed-source workflow for ongoing work.
18. P2-05 Improve assessment pedagogical taxonomy, per-topic tags, rubrics/model answers, progress analytics and study-mode explanations.
19. P2-06 Reduce overlapping diagrams and rationalise figure ordering in Chapters 1.2, 2.2, 4.3 and 5.2.

## 9. Acceptance matrix
| Gate | Passing evidence required | Current audit |
|---|---|---|
| Source integrity | Checked-in Kotlin project + clean CI compile | **PASS** |
| Syllabus inventory | 5 units, 28 chapters and every prescribed main subtopic mapped | **PRESENT; depth needs review** |
| Scientific text | 28 chapter sign-offs with citations, corrected conceptual errors | **NOT APPROVED** |
| Figures | 58/58 placement, label anatomy, legibility and arrow audits recorded and cleared | **FAIL — visible defects** |
| Tamil | Sentence-level translation review + rasterised glyph inspection + on-device testing | **FAIL — supplementary plates** |
| Assessments | unbiased answer placements + semantic parity + all 62 rationale checks + subject QA | **FAIL — bias and mixed-language options** |
| Native UI | Emulator and physical-device screenshot/XML/gesture/accessibility pass | **NO PASS EVIDENCE** |
| Distribution rights | per-asset author, source, licence, adaptation and permission ledger | **NOT CLEARED** |
| Production packaging | API 36 (unless approved extension), release-signed AAB, version identity and Play Console validation | **NOT READY** |

**Decision:** retain v6.1.1-QA as a debug development build; do not label it final, error-free, scientifically verified or store-ready. Correct P0 items and rerun the expanded gates in severity order. This audit does not itself modify student lessons or plates.

## 10. Evidence pointers
- GitHub project tree at audit SHA: https://github.com/rameshgascngl-create/Introduction-to-Zoology-App/tree/5d4d4a1a01cf4b3c5de84e427ed42c0c59bdf882
- Source reader: `app/src/main/java/com/gasczoology/introzoology/MainActivity.kt`; content: `app/src/main/assets/content.json`; images: `app/src/main/assets/plates/` and `svg/`.
- Static tests: `tools/validate_content.py`; UI smoke: `app/src/androidTest/java/com/gasczoology/introzoology/NativeReaderSmokeTest.kt`.
- Last source build PASS: https://github.com/rameshgascngl-create/Introduction-to-Zoology-App/actions/runs/39948257568
- Emulator QA non-PASS: https://github.com/rameshgascngl-create/Introduction-to-Zoology-App/actions/runs/39947866716
- Formal syllabus: user-provided `Introduction to Zoology Unit I to V Notes.pdf`, page 3 (85 pages total).
