# Introduction to Zoology — native Android v6.1.0

This is a **native Android Kotlin / Jetpack Compose** reading application (no WebView) with locally bundled learning content, prepared from the 85-page *Introduction to Zoology Unit I to V Notes.pdf* supplied by the user.

## Inventory

- Five course units and 28 English–Tamil chapters, including the new Unit III chapter 3.5 (Vital Physiological Organ Systems).
- 58 teaching plates: 38 carried from v6.0.0, 11 directly reused from departmental notes, 6 redrawn to correct unsuitable PDF figures, and 3 new original course schematics.
- 62 bilingual MCQs, 41 bilingual short answers, and 26 long-answer prompts.
- Native home, unit browser, chapter reader, search, bookmarking, font adjustment, offline reading, zoomable diagrams, and tests.
- Each chapter includes reference page range from the uploaded departmental notes.

## Build the native app from source

Requires Android Studio, Android SDK 35, Java 17 and Gradle/dependencies available for first-time sync.

```bash
python3 tools/validate_content.py
gradle assembleDebug
```

The clean-build output is `app/build/outputs/apk/debug/app-debug.apk`. This **source project has not been compiled in the present container**, where Android SDK and AndroidX build dependencies are unavailable.

## Development APK provided separately

The distributed `Introduction_to_Zoology_v6.1.0_NATIVE_CONTENT_DEVELOPMENT.apk` was constructed by replacing **only JSON/textbook assets, PNG diagrams and version metadata** in the already compiled native 6.0.0 APK, then signing with a new development certificate (APK Signature Scheme v2). It is native, but it is not proof of a clean 6.1.0 Kotlin/Gradle build.

This development certificate **is different from prior builds**. Android will reject in-place upgrades across signing identities. Device installation and visual interaction checks are still required.

### Academic and image safety notes

The user-provided PDF is the primary source for learning content. Its p.17 echinoderm-symmetry table, p.28 monohybrid diagram and several other figures have identifiable errors and are not reproduced without correction. Six questionable/unsuitable PDF illustrations were replaced by new original SVG teaching plates, notably the original p.57 figure that shows a copyright notice. Eleven further figures were reused with page provenance; production redistribution rights need independent assessment. The earlier 38 figures were retained but are not globally certified as anatomically correct.

The attached PDF lists Lac Culture in its formal syllabus but has no detailed explanatory section on this topic. The new lac explanation is distinctly supplemented using ICAR-IINRG research and extension materials. Additional scientific correctness checks draw on ICZN and OpenStax, while preserving the syllabus sequence.

See `tools/validate_content.py`, `tools/upgrade_6_1.py`, `tools/create_precise_schematics.py`, `tools/replace_faulty_reference_figures.py` and the separate audit report. The upgrade scripts reference the uploaded source PDF on its original container path; the generated assets and content JSON are already present in this ZIP and do not require rerunning those scripts.
