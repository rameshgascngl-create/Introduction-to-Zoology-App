# Introduction to Zoology — Native Android (Phase II)

A fully **native Kotlin / Jetpack Compose** offline course reader for the *Introduction to Zoology* foundation course (Department of Zoology, Government Arts and Science College, Nagercoil). It does not use WebView or require Internet access in the app.

## Directly inspectable Android project

Unlike the earlier packed-source v6.1 branch, this branch contains the ordinary Android project: `app/src/main/java`, `app/src/main/assets/content.json`, `app/src/main/assets/plates`, Gradle files, and the static validator. A CI source-export archive is also retained under the Phase II GitHub Actions run.

**Course inventory:** five units; 28 chapters in English and Tamil; 58 teaching plates; 62 bilingual multiple-choice questions (as of the baseline v6.1 source); 41 short-answer and 26 long-answer prompts per language. Each chapter has source-page references. The unit-by-unit checklist is in `docs/PHASE2_ACADEMIC_QA.md`.

### Build and validate

Requires Java 17, Android SDK 35, Gradle 8.10.2 and Android Gradle Plugin dependencies.

```bash
python3 tools/validate_content.py
gradle --no-daemon assembleDebug
```

Debug APK: `app/build/outputs/apk/debug/app-debug.apk`.

**Two distinct workflows:**
- `phase2-extract-and-validate.yml` restores the former packaged source and publishes it to the development branch. It must **not** be used to rebuild later content edits, because extraction uses the original v6.1 payload.
- `phase2-native-build.yml` builds the **current ordinary checked-in project**; this is the authoritative CI path for subsequent Phase II changes.

The source-extraction workflow completed successfully on 23 October 2026 (run 39936309835), demonstrating Kotlin compilation, structural content validation, package metadata verification and creation of an installable **debug** APK. A debug APK is not a production-signed release.

### Chapter-level academic audit

The basis is the supplied 85-page *Introduction to Zoology Unit I to V Notes.pdf*, including the formal five-unit syllabus on PDF page 3. The original v6.1 lesson inventory structurally covers the listed units; the Phase II editorial correction explicitly adds the missing **habitat, microhabitat and ecological-niche** explanation in Unit IV, Chapter 4.2, in both languages.

Structural checks cannot prove that every diagram is anatomically correct or that every Tamil formulation is editorially polished. The 58 plates are present and have distinct file hashes, but **physical-device rendering, magnification, font clipping, copyright provenance and scientific figure review are not yet completed**. Eleven images reused from the departmental reference notes require rights verification before public redistribution. Earlier generated diagrams likewise require figure-by-figure inspection.

The GitHub Actions artifacts are development and QA outputs, not a production release. Signing key management, Play Store distribution and device testing are separate release gates.

See `tools/validate_content.py`, `native/PHASE2_SOURCE_MANIFEST.json` and `docs/PHASE2_ACADEMIC_QA.md` for the auditable inventory and acceptance criteria.
