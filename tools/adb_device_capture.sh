#!/usr/bin/env bash
# Evidence collector: requires user's own USB-connected Android test phone and ADB.
# Does NOT assert classroom QA or edit QA_SIGNOFF.json.
set -euo pipefail
APK="$(pwd)/app/build/outputs/apk/debug/app-debug.apk"
if [[ $# -gt 0 ]]; then APK="$1"; fi
if [[ ! -s "$APK" ]]; then echo "Missing APK: $APK"; exit 1; fi
adb start-server
num="$(adb devices | awk '$2=="device" {n++} END {print n+0}')"
if [[ "$num" -ne 1 ]]; then echo "Need exactly one authorised test device; found $num"; exit 1; fi
OUT="qa-device-evidence/$(date +%Y%m%d-%H%M%S)"
mkdir -p "$OUT"
adb devices -l | tee "$OUT/adb-device.txt"
adb shell getprop ro.build.version.release > "$OUT/android-version.txt"
adb shell getprop ro.product.model > "$OUT/device-model.txt"
adb shell wm size > "$OUT/screen-size.txt"
adb shell wm density > "$OUT/screen-density.txt"
adb install -r "$APK" | tee "$OUT/install.txt"
adb shell am force-stop com.gasczoology.introzoology || true
adb shell am start -n com.gasczoology.introzoology/.MainActivity | tee "$OUT/launch.txt"
sleep 3
adb shell pidof com.gasczoology.introzoology > "$OUT/process-id.txt" || { echo "App crashed during launch"; exit 1; }
adb shell screencap -p /sdcard/zoology-audit.png
adb pull /sdcard/zoology-audit.png "$OUT/home.png" >/dev/null
adb shell uiautomator dump /sdcard/zoology-hierarchy.xml >/dev/null || true
adb pull /sdcard/zoology-hierarchy.xml "$OUT/home-hierarchy.xml" >/dev/null || true
adb shell dumpsys meminfo com.gasczoology.introzoology > "$OUT/memory.txt"
adb logcat -d -t 1500 > "$OUT/logcat.txt"
echo "Evidence directory: $OUT"
echo "MANUAL ACCEPTANCE: 58 plates in normal and enlarged views; Tamil all 28 chapters;"
echo "3-button/gesture navigation, TalkBack, rotate/restart, bookmarks, offline, quiz and score."
