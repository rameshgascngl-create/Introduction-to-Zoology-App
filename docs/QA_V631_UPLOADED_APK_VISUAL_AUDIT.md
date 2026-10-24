# APK v6.3.1-labelled candidate — release-blocking audit

Date: 2026-10-24

Uploaded file: `Introduction_to_Zoology_v6.3.1_QA_DEBUG.apk`
SHA-256: `54b97042f390103b9c916c0bc7ef334a7c3852231c5d6315898263fc276e87c3`

## Conflicting version identifiers
- Filename: v6.3.1 QA DEBUG
- APK binary manifest: `6.2.0-QA`, version code `620`
- `assets/content.json` in uploaded APK: `6.3.0-QA`
- Older native app subtitle: `v6.1.1 QA`
- The current checked-in GitHub `content.json`: `6.2.0-QA` (shorter than uploaded payload).

**Do not rename the APK or treat it as a verified v6.3.1 release.** The expanded uploaded lesson data must be reconciled into the actual editable source before a clean native build.

## Emulator visual QA defect
Five instrumentation tests passed in successful run 40093719218, but all ten exported PNG screenshots visibly contain blocking Android 'System UI isn't responding' or 'Digital Wellbeing isn't responding' dialogs. The existing PNG checks verified file structure only, not unobscured visibility; visual QA is NOT PASSED.

## Mitigation
- Android UI instrumentation now checks the active window for ANR/crash dialogs after each screenshot, and fails rather than certifying obstructed evidence.
- Emulator cores/RAM increased to reduce resource starvation.
- Android title now uses `BuildConfig.VERSION_NAME` instead of an old hard-coded display version.
- Static validator enforces `content.json.edition == Gradle versionName`.

## Outstanding before release
- Import and verify the uploaded expanded 6.3.0-QA textbook payload into the editable source. Only then set coherent v6.3.1 identifiers and rebuild natively.
- Obtain unobscured screenshots plus real-device QA.
- Complete scientific and rights sign-off for all 58 figures and bilingual content.
- Sign with authorized production keystore, not debug key.

This audit does not infer that the Zoology application itself crashed from system-UI ANR dialogs.
