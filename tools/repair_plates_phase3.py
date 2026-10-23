#!/usr/bin/env python3
"""Repair source SVG science errors, render approved masters with Tamil-capable librsvg, and validate output.
Run explicitly from repository root; never rewrite unlisted/reference-note raster assets.
"""
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
SVG=ROOT/"app/src/main/assets/svg"
PNG=ROOT/"app/src/main/assets/plates"

def swap(filename, old, new):
    path=SVG/filename
    s=path.read_text(encoding="utf-8")
    if old not in s:
        if new in s:
            return
        raise ValueError(f"{filename}: missing known source span: {old[:65]}")
    path.write_text(s.replace(old,new),encoding="utf-8")

# Direct sunlight toward primary producers at the bottom of the trophic pyramid, not the apex.
swap("original_orig16.svg",
     '<text x="250" y="50" text-anchor="middle" font-size="9.5" fill="#c98a3b" font-weight="bold">☀ Sun (energy input)</text><line x1="250" y1="58" x2="250" y2="89" stroke="#c98a3b" stroke-width="2.4" marker-end="url(#arr16a)"/>',
     '<text x="82" y="155" text-anchor="middle" font-size="9.5" fill="#a46a18" font-weight="bold">Sunlight</text><path d="M70,164 L105,220" fill="none" stroke="#c98a3b" stroke-width="2.5" marker-end="url(#arr16a)"/><text x="250" y="67" text-anchor="middle" font-size="8" fill="#5a4e42">Energy flows from producers up trophic levels and dissipates as heat</text>')
# Reverse transcription is not exclusive to retroviruses: retrotransposons and telomerase are examples.
swap("original_orig10.svg","(retroviruses only)","(e.g., retroviruses and retroelements)")
# Vitamin B12 is retained in the body for years in some cases, despite water solubility.
swap("original_orig14.svg","excreted readily, not stored","usually less stored; B12 exception")
# Meiosis I / II must label primary->secondary and secondary->spermatid transitions.
swap("original_orig17.svg",'<text x="60" y="112" font-size="7.5" fill="#8f3f0b">Meiosis I</text><text x="150" y="112" font-size="7.5" fill="#8f3f0b">Meiosis II</text>',
     '<text x="217" y="108" text-anchor="middle" font-size="7.2" fill="#8f3f0b">Meiosis I</text><text x="307" y="108" text-anchor="middle" font-size="7.2" fill="#8f3f0b">Meiosis II</text>')
swap("original_orig17.svg",'<text x="250" y="222"',
     '<text x="217" y="209" text-anchor="middle" font-size="7.2" fill="#8a1e3c">Meiosis I</text><text x="307" y="209" text-anchor="middle" font-size="7.2" fill="#8a1e3c">Meiosis II (sperm entry)</text><text x="250" y="222"')
swap("original_orig17.svg",'<text x="352" y="75"','<text x="352" y="75"')  # no-op explicit
# Distinguish spermatids from spermatozoa; terminal differentiating event is spermiogenesis.
swap("original_orig17.svg","Spermatids → Sperm","Spermatids → sperm")
# Simplify large marker geometry in meiotic diagrams so arrows cannot cover labels.
for name in ["notes_p57.svg","notes_p58.svg"]:
    swap(name,'<marker id="a" markerWidth="12" markerHeight="12" refX="8" refY="4" orient="auto">',
         '<marker id="a" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" refX="9" refY="4" orient="auto">')
    swap(name,'<path d="M0,0 L8,4 L0,8" fill="none" stroke="#246752" stroke-width="2"/>',
         '<path d="M0,0 L8,4 L0,8 Z" fill="#246752" stroke="none"/>')
# Explicit step numbers fix ambiguity caused by serpentine lac process direction.
for i,word in enumerate(["Prepare host","Select broodlac","Place broodlac","Crawler settlement","Resin secretion","Harvest / process"],start=1):
    swap("native_lac.svg",f'>{word}</text>',f'>{i}. {word}</text>')
# Replace misaligned superimposed nomenclature boxes with independent, legible labelled terms.
name=SVG/"original_orig2.svg"
s=name.read_text(encoding="utf-8")
if '<!-- P3 verified two-box layout -->' not in s:
    s='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 420" role="img" aria-label="Two parts of the scientific name Panthera leo">
 <rect x="8" y="8" width="744" height="404" rx="25" fill="#fffdf8" stroke="#d8d0c4" stroke-width="3"/>
 <text x="380" y="58" text-anchor="middle" font-family="sans-serif" font-size="33" font-weight="bold" fill="#153f2e">BINOMIAL NOMENCLATURE</text>
 <!-- P3 verified two-box layout -->
 <rect x="74" y="105" width="270" height="112" rx="14" fill="#e8f5ef" stroke="#276a52" stroke-width="3"/>
 <rect x="416" y="105" width="270" height="112" rx="14" fill="#eaf2fb" stroke="#245e89" stroke-width="3"/>
 <text x="209" y="152" text-anchor="middle" font-size="42" font-family="serif" font-style="italic" font-weight="bold" fill="#153f2e">Panthera</text>
 <text x="551" y="152" text-anchor="middle" font-size="42" font-family="serif" font-style="italic" font-weight="bold" fill="#245e89">leo</text>
 <text x="209" y="193" text-anchor="middle" font-size="22" fill="#153f2e">GENUS (capital initial)</text>
 <text x="551" y="193" text-anchor="middle" font-size="21" fill="#245e89">Specific epithet (lowercase)</text>
 <text x="380" y="260" text-anchor="middle" font-size="30" font-family="serif" font-style="italic" fill="#233b45">Panthera leo</text>
 <text x="380" y="303" text-anchor="middle" font-size="20" fill="#5a4e42">Printed scientific name: italicise both words</text>
 <text x="380" y="340" text-anchor="middle" font-size="20" fill="#5a4e42">Handwriting: underline each word separately</text>
 <text x="380" y="375" text-anchor="middle" font-size="18" fill="#8a1e3c">A specific epithet alone is not the full species name.</text>
 </svg>'''
    name.write_text(s,encoding="utf-8")

targets=[
"original_orig2","original_orig10","original_orig14","original_orig16","original_orig17","native_lac",
"notes_p57","notes_p58",
"supplement_systflow","supplement_celltheory","supplement_darwinselection","supplement_silkworm",
"supplement_poultrybio","supplement_dairyhygiene","supplement_molecular","supplement_ecotourism"
]
# Avoid distributing toxic Tamil squares: render via librsvg/Pango and require Tamil font availability.
fc=subprocess.run(["fc-match","-f","%{family}\n",":lang=ta"],capture_output=True,text=True,check=True)
if not ("Noto Sans Tamil" in fc.stdout or "Noto Serif Tamil" in fc.stdout):
    raise SystemExit("Tamil font absent; refusing to render bilingual plates. Got "+repr(fc.stdout))
for stem in targets:
    path=SVG/(stem+".svg")
    ET.parse(path)
    out=PNG/(stem+".png")
    subprocess.run(["rsvg-convert","--width","1500","-o",str(out),str(path)],check=True)
    with Image.open(out) as im:
        im.verify()
    with Image.open(out) as im:
        assert im.width>=300 and im.height>=100,(stem,im.size)
    print("Rendered",stem,out.stat().st_size)
# Guard against accidentally omitting any original plate.
assert len(list(PNG.glob("*.png"))) == 58, "Expected 58 pre-existing PNG filenames"
print("Phase III targeted image repair complete; inspect resulting PNGs visually before academic approval.")
