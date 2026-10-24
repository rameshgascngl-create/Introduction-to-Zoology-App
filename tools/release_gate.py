#!/usr/bin/env python3
"""Fail closed: unknown copyright or unsatisfied QA must not ship as a signed academic Play release."""
import json, pathlib, os, re, sys
root=pathlib.Path(__file__).resolve().parents[1]
rights=json.loads((root/"docs/IMAGE_RIGHTS_LEDGER.json").read_text())
qa=json.loads((root/"docs/QA_SIGNOFF.json").read_text())
issues=[]
if len(rights["plates"])!=58: issues.append("Rights ledger does not account for all 58 figures")
for p in rights["plates"]:
    if p["rights_status"]!="CLEARED" or not p.get("license_id") or not p.get("permission_evidence"):
        issues.append("Uncleared redistribution rights: "+p["filename"])
    if p["academic_status"]!="APPROVED" or not p.get("reviewer"):
        issues.append("Figure not academically signed off: "+p["filename"])
for k,v in qa["automated"].items():
    if v is not True: issues.append("Automated QA missing: "+k)
for k in ("verified","portrait_nav","tamil_text","all_58_plates","zoom","rotation","offline","progress_persistence","quiz"):
    if qa["device"].get(k) is not True: issues.append("Physical device QA missing: "+k)
if not qa["device"].get("screenshots_path") or not qa["device"].get("reviewer"):
    issues.append("Physical device evidence/reviewer absent")
for k,v in qa["editorial"].items():
    if v is not True: issues.append("Editorial signoff missing: "+k)
for k in ("target_api_36","store_metadata","privacy_review"):
    if qa["release"].get(k) is not True: issues.append("Release gate missing: "+k)
gradle=(root/"app/build.gradle.kts").read_text()
if not re.search(r"targetSdk\s*=\s*36\b",gradle):issues.append("Play update targetSdk is not API 36")
if not os.environ.get("ANDROID_KEYSTORE_PATH"):issues.append("Production keystore path unavailable")
if issues:
    print("RELEASE BLOCKED ("+str(len(issues))+" requirements unmet):")
    for x in issues:print(" -",x)
    sys.exit(1)
print("All documented release gates passed (subject to authenticity of reviewer records).")
