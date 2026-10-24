#!/usr/bin/env bash
# One shell process is essential: android-emulator-runner executes each
# newline-separated script command independently rather than preserving
# compound bash loops or shell variables between lines.
set -uo pipefail
PACKAGE="com.gasczoology.introzoology"
mkdir -p qa-screenshots
test_status=0
gradle --no-daemon --stacktrace :app:connectedDebugAndroidTest || test_status=$?
echo "Instrumented test exit status: $test_status" | tee qa-screenshots/collection-log.txt
adb shell run-as "$PACKAGE" ls -la files/qa-screenshots >> qa-screenshots/collection-log.txt 2>&1 || true
missing=0
for shot in 01-home-en 02-diagram-fullscreen 03-chapter-tamil 04-bookmark-saved 05-quiz-portrait 06-quiz-landscape-before-scroll 06-quiz-landscape 07-all-units-tamil; do
    if adb exec-out run-as "$PACKAGE" cat "files/qa-screenshots/${shot}.png" > "qa-screenshots/${shot}.png" 2>/dev/null && [[ -s "qa-screenshots/${shot}.png" ]]; then
        printf 'Captured: %s\n' "$shot" | tee -a qa-screenshots/collection-log.txt
    else
        rm -f "qa-screenshots/${shot}.png"
        printf 'Missing screenshot: %s\n' "$shot" | tee -a qa-screenshots/collection-log.txt
        missing=$((missing + 1))
    fi
done
adb shell uiautomator dump /sdcard/window.xml || true
adb pull /sdcard/window.xml qa-screenshots/window.xml || true
adb logcat -d -t 2000 > emulator-last-logcat.txt || true
# Keep test and screenshot evidence failures separate for unambiguous triage.
if [[ "$test_status" -ne 0 ]]; then
    echo "FAIL: Android instrumentation tests returned $test_status" >&2
    exit "$test_status"
fi
if [[ "$missing" -gt 0 ]]; then
    echo "FAIL: $missing required QA screenshots could not be collected" >&2
    exit 1
fi
echo "PASS: 4 native UI tests and all 8 screenshot evidence files"
