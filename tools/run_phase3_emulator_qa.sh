#!/usr/bin/env bash
# Capture emulator evidence through MediaStore, which survives the test APK
# teardown. Fail closed if a screenshot is a text error rather than PNG data.
set -uo pipefail
mkdir -p qa-screenshots
adb shell mkdir -p /sdcard/Pictures/IntroductionZoologyQA || true
adb shell rm -f '/sdcard/Pictures/IntroductionZoologyQA/*.png' || true
test_status=0
gradle --no-daemon --stacktrace :app:connectedDebugAndroidTest || test_status=$?
printf 'Instrumentation exit code: %s\n' "$test_status" | tee qa-screenshots/collection-log.txt
adb shell ls -la /sdcard/Pictures/IntroductionZoologyQA >> qa-screenshots/collection-log.txt 2>&1 || true
adb pull /sdcard/Pictures/IntroductionZoologyQA/. qa-screenshots/ >> qa-screenshots/collection-log.txt 2>&1 || true
python3 - <<'PY'
import pathlib,struct,zlib,sys
out=pathlib.Path("qa-screenshots")
names=["01-home-en","02-diagram-fullscreen","03-chapter-tamil",
"04-bookmark-saved","05-quiz-portrait","06-quiz-landscape-before-scroll",
"06-quiz-landscape","07-all-units-tamil"]
errors=[]
for name in names:
    p=out/(name+".png")
    if not p.is_file():
        errors.append(name+": missing file")
        continue
    buf=p.read_bytes()
    if len(buf)<5000 or not buf.startswith(b"\x89PNG\r\n\x1a\n"):
        errors.append(name+": not a credible PNG (size="+str(len(buf))+")")
        continue
    idx=8; width=height=0; saw_idat=False; saw_iend=False
    try:
        while idx<len(buf):
            ln=struct.unpack(">I",buf[idx:idx+4])[0]
            kind=buf[idx+4:idx+8]
            payload=buf[idx+8:idx+8+ln]
            crc=struct.unpack(">I",buf[idx+8+ln:idx+12+ln])[0]
            if zlib.crc32(kind+payload)&0xffffffff!=crc:
                raise ValueError("PNG CRC mismatch")
            idx+=12+ln
            if kind==b"IHDR":
                width,height=struct.unpack(">II",payload[:8])
            if kind==b"IDAT": saw_idat=True
            if kind==b"IEND": saw_iend=True; break
        if not(saw_idat and saw_iend and width>=320 and height>=320):
            raise ValueError("missing image data or implausible dimensions")
        print("PNG_OK",name,width,height,len(buf))
    except Exception as exc:
        errors.append(name+": "+str(exc))
if errors:
    print("SCREENSHOT_QA_FAIL:")
    print("\n".join(errors))
    sys.exit(2)
print("SCREENSHOT_QA_PASS: 8 genuine PNG files")
PY
image_status=$?
adb shell uiautomator dump /sdcard/window.xml || true
adb pull /sdcard/window.xml qa-screenshots/window.xml || true
adb logcat -d -t 2000 > emulator-last-logcat.txt || true
if [[ "$test_status" -ne 0 ]]; then
    echo "FAIL: instrumented tests" >&2
    exit "$test_status"
fi
if [[ "$image_status" -ne 0 ]]; then
    echo "FAIL: invalid/missing screenshot evidence" >&2
    exit "$image_status"
fi
echo "PASS: four UI tests and eight CRC-validated PNG screenshots"
