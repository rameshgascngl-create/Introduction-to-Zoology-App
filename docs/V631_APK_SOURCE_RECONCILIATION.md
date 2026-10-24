# v6.3.1-QA native source restoration

Source candidate: `Introduction_to_Zoology_v6.3.1_QA_DEBUG.apk`, SHA-256 `54b97042f390103b9c916c0bc7ef334a7c3852231c5d6315898263fc276e87c3`.

The uploaded APK's original `content.json` edition was `6.3.0-QA`, with 5 units, 28 bilingual chapters, 58 figure references, and 62 MCQs / 41 short / 26 long questions per language. The branch restores that expanded textbook data; only JSON edition/provenance metadata changes to `6.3.1-QA` to match the newly compiled package.

Extracted original JSON SHA-256: `00f437c7430b385d4370ef9796e7dc277a0bcfc02940a0b30cd911b474bfc92e`.

The uploaded APK's binary manifest claimed `6.2.0-QA` (620), even though its filename claimed v6.3.1. This branch sets Gradle to versionCode **631** and versionName **6.3.1-QA**; the Android top bar obtains its version from `BuildConfig.VERSION_NAME`.

**Known editorial gap:** Chapter 4.2 explains habitat and ecological niche but not microhabitat explicitly in both languages. This must be expanded in a later content/editorial review; do not substitute a validator claim for actual lesson text.

**Release gates remain unresolved:** Scientifically sign off 58 plates, clear original-image redistribution rights, inspect unobscured emulator/physical Android screens, and verify original signing certificate. The prior UI test screenshots were obstructed by Android System UI ANR dialogs. No production approval is claimed here.

**Verification:** `python3 tools/validate_content.py` and `gradle :app:assembleDebug :app:assembleDebugAndroidTest` must pass. Compare produced APK binary metadata and embedded content inventory with source. Use GitHub Action `native-v6.3.1-qa.yml` for clean compilation and QA artifact.
