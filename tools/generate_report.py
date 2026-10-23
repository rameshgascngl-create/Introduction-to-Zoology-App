from pathlib import Path
from collections import Counter,defaultdict
import json,re,hashlib,zipfile,sys
root=Path(__file__).resolve().parents[1]
a=root/'app/src/main/assets'
d=json.loads((a/'content.json').read_text('utf8'))
apk=Path('/mnt/data/Introduction_to_Zoology_v6.1.0_NATIVE_CONTENT_DEVELOPMENT.apk')
sourcezip=Path('/mnt/data/Introduction_to_Zoology_v6.1.0_TRUE_NATIVE_AndroidStudio_Source.zip')
report=Path('/mnt/data/Introduction_to_Zoology_v6.1.0_Syllabus_Image_Android_Audit.md')
chap_by=defaultdict(list)
for ch in d['chapters']:chap_by[ch['unit']].append(ch)
plate_by=Counter(p['chapter'] for p in d['plates'])
counts=Counter(p['kind'] for p in d['plates'])
sections=['# Introduction to Zoology v6.1.0 — Syllabus, Image and APK Audit','',
'**Build date:** 23 October 2026 · **Primary reference:** *Introduction to Zoology Unit I to V Notes.pdf* (85 pages), supplied by the user.','',
'## Outcome','',
'- Native framework: existing compiled Kotlin/Jetpack Compose app, not a WebView.','- Five syllabus units, **28 chapters**; one new Unit III chapter (3.5 Vital Physiological Organ Systems).',
'- **58 offline raster teaching plates** with Tamil/English captions; 11 retained directly from the supplied PDF; six unsuitable PDF illustrations replaced by original revised schematics; three further new original diagrams. The previously carried 38 plates were retained.',
'- **62 bilingual MCQs, 41 bilingual short-answer questions, 26 bilingual long-answer prompts.**',
'- Teaching extras added to each chapter: revised English explanations, revised Tamil explanations, chapter-linked departmental notes source-page reference, scientific misconception/correction notes and classroom activity.','',
'## Chapter-to-source crosswalk','',
'| Unit | Chapter | Topic | Primary reference pages | English words | Figures |','|---|---|---|---|---:|---:|']
for n,chapters in chap_by.items():
 for ch in chapters:
  w=len(re.findall(r'\b[\w-]+\b',re.sub('<[^>]*>',' ',ch['contentEn'])))
  pp=ch.get('sourcePages') or []
  sections.append(f"| {n} | {ch['id']} | {ch['enTitle']} | {pp[0]}–{pp[-1]} | {w} | {plate_by[ch['id']]} |")
sections+=['','## Image audit and provenance','',
'Image types: '+', '.join(f'{name}: {count}' for name,count in sorted(counts.items()))+'.','',
'- PDF p.5: taxonomy diagram omitted Kingdom; **replaced with complete eight-rank original hierarchy**.',
'- PDF p.13: a miniature lettering poster is difficult to read and insufficiently precise; **replaced with ICZN-compliant binomial naming chart**.',
'- PDF p.25: plant-cell illustration uses an oversimplified organelle arrangement; **replaced with original labelled plant-cell schematic**.',
'- PDF p.28: **scientific error**: gamete from homozygous recessive `tt` parent labelled `T`; **replaced** with correct `T`/`t` monohybrid cross.',
'- PDF p.57: labelled spermatogenesis illustration carries third-party Encyclopaedia Britannica copyright notice; **not redistributed**; replaced with an original step schematic.',
'- PDF p.58: oogenesis diagram does not clearly distinguish human meiotic arrests and fertilisation-triggered completion; **replaced with a corrected stage diagram**.',
'- PDF p.6 and p.9 pictorial comparison graphics excluded because they oversimplify taxonomy and mix unrelated categories; p.26 comparison graphic omitted as oversimplified.',
'- Eleven directly reused PDF images are accompanied by source-page captions. **Commercial/public redistribution rights have not been independently established** for all embedded figures; permissions must be resolved before a store release.','',
'## Scientific corrections','',
'- **Echinoderm symmetry:** Bilateral larvae / usually pentaradial adults; the PDF p.17 summary table reverses them. Correction is explicitly in chapter 1.5; misleading table is not used as a plate.',
'- **Chordata:** A backbone is not universal to all chordates. Notochord, dorsal hollow nerve cord and other developmental traits are the diagnostic framework (chapters 1.5–1.6).',
'- **Five-kingdom scheme:** Presented as a historical framework; Monera and Protista are not modern natural clades (chapter 1.3).',
'- **Species concept:** Biological species concept is not universally applicable to asexual taxa and fossils (chapter 1.2).',
'- **Cell theory:** Binary fission and eukaryotic division distinguished; cells do not all arise by mitosis or meiosis (chapter 2.1).',
'- **Cell structure:** Bacterial vs archaeal cell-wall composition and existence of prokaryotic cytoskeletal systems clarified (chapter 2.2).',
'- **Mendelian ratios:** 3:1 and 9:3:3:1 are conditional on assumptions, not universal (chapter 2.3).',
'- **DNA/RNA and central dogma:** RNA viral replication and reverse transcription qualified (chapters 2.4–2.5).',
'- **Lac culture:** Listed in PDF syllabus p.3 but not presented as a substantive standalone section. Added biology and cultivation guidance from ICAR-IINRG, marked as an external supplement in chapter 5.4.',
'- **Aquarium keeping:** Given explicit biofiltration, water chemistry and invasive-release prevention content within 5.1 (PDF pp.67–69).',
'- **Physiological systems:** New detailed 3.5 chapter from PDF pp.47–49 to correct missing syllabus content.',
'','## Authoritative supplementary references','',
'- [ICZN Article 5: Principle of Binominal Nomenclature](https://code.iczn.org/chapter-2-the-number-of-words-in-the-scientific-names-of-animals/article-5-principle-of-binominal-nomenclature/)',
'- [ICAR Institutes Profile, Indian Institute of Natural Resins and Gums](https://www.icar.gov.in/sites/default/files/2022-12/ICAR-INSTITUTE-PROFILE_.pdf)',
'- [OpenStax Biology, Echinoderm morphology](https://openstax.org/books/biology/pages/28-5-superphylum-deuterostomia)',
'','## Android package validation','',
'- APK produced by **replacing assets and version metadata in the previously compiled native 6.0.0 APK**, not by fresh Gradle compilation. Existing Compose classes remain compiled from v6.0.0 and are compatible with the expanded JSON lesson/plate inventory.',
'- Android version name `6.1.0` / versionCode `610` in binary AndroidManifest.xml; displayed version literal updated in classes3.dex, with DEX SHA-1 and Adler-32 header checksums recomputed.',
'- APK signature scheme **v2** cryptographically signed and verified; independent algorithm calibrated against the intact, original 6.0.0 debug APK signature and digest.',
'- Package ZIP CRC integrity and presence of all 58 referenced PNGs verified; uncompressed native library entries remain page-aligned in new ZIP.',
'- Original application ID, Android minSdk and native code architecture retained. No WebView introduced.',
'- **New signing certificate:** cannot be installed as an update over previous differently signed APKs. Do not uninstall a version containing important stored reading progress without backup.',
'- **NOT YET VERIFIED:** clean Gradle 6.1.0 compilation, Android PackageManager installation, screen rendering, Tamil line breaking, image label legibility on real phones, image pan/zoom gestures, bookmarks/quiz persistence or accessibility.',
'- Any previously persisted settings use the pre-existing preference namespace; in-place data migration requires the original release signing key.',
'','## Release policy','',
'1. Use the supplied complete Android Studio source ZIP to perform a clean build in an Android SDK/Gradle environment.',
'2. Verify source compilation, package signer, package metadata and startup on actual Android 13+ phone and 7–10 inch tablet.',
'3. Audit all inherited 38 schematic plates, verify remaining 11 PDF-source figures for rights/clarity, and run Tamil editorial review.',
'4. Rebuild a production APK/AAB using the original release key only after device acceptance.','']
sections += [f'**Development APK SHA-256:** `{hashlib.sha256(apk.read_bytes()).hexdigest()}`',
 f'**APK file size:** `{apk.stat().st_size:,}` bytes.',
 f'**Android Studio source archive:** `{sourcezip.name}`.' if sourcezip.exists() else '']
report.write_text('\n'.join(sections),'utf8')
print(report,report.stat().st_size)
