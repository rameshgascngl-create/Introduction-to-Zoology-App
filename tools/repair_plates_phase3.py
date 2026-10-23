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


# Refine four more flawed existing scientific plates without changing lesson IDs.
swap("original_orig5.svg",
     '<text x="392" y="210" font-size="9.5" fill="#7a3b8c" font-weight="bold">4. Post-anal tail</text><text x="392" y="221" font-size="8" fill="#5a4e42">(beyond anus, marked •)</text>',
     '<text x="363" y="205" font-size="8.5" fill="#7a3b8c" font-weight="bold">4. Post-anal tail</text><text x="363" y="215" font-size="7" fill="#5a4e42">(extends past anus)</text>')
swap("original_orig6.svg",
     '<text x="395" y="95" font-size="9.5" fill="#2e6b4f" font-weight="bold">Flagellum</text>',
     '<text x="386" y="145" font-size="8.5" fill="#2e6b4f" font-weight="bold">Flagellum</text>')
swap("original_orig15.svg",
     '<line x1="100" y1="188" x2="390" y2="188" stroke="#8f3f0b" stroke-width="1.6" stroke-dasharray="4,3"/>',
     '<line x1="100" y1="197" x2="390" y2="197" stroke="#8f3f0b" stroke-width="1.6" stroke-dasharray="4,3"/>')
swap("original_orig15.svg",
     '<text x="398" y="192" font-size="8" fill="#8f3f0b">Ozone concentration</text><text x="398" y="203" font-size="8" fill="#8f3f0b">(within stratosphere)</text>',
     '<text x="395" y="177" font-size="8" fill="#8f3f0b">Ozone-rich</text><text x="395" y="189" font-size="8" fill="#8f3f0b">stratosphere</text>')
swap("atlas_cell.svg",'<text x="386" y="82">Mitochondrion</text>',
     '<text x="350" y="74">Mitochondrion</text>')
swap("atlas_cell.svg",'<text x="401" y="315">Plasma membrane</text>',
     '<text x="310" y="335">Plasma membrane</text>')
swap("atlas_ecosystem.svg",'text-anchor="middle" font-size="16" font-weight="700"',
     'text-anchor="middle" font-size="12" font-weight="700"')
# Replace oversimplified lipid hierarchy with molecule-class distinctions; preserve filename.
lipid_svg=SVG/"notes_p40.svg"
if not lipid_svg.exists():
    lipid_svg.write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 600" role="img" aria-label="Major lipid classes with chemically distinct examples">
<rect width="1000" height="600" fill="#F6FBF9"/><text x="500" y="65" text-anchor="middle" font-size="43" font-family="sans-serif" font-weight="bold" fill="#153F4B">LIPID CLASSES AND FUNCTION</text>
<text x="500" y="100" text-anchor="middle" font-size="23" font-family="sans-serif" fill="#4C6171">Structural classes are not the same as their component molecules</text>
<g font-family="sans-serif" fill="#194A41"><rect x="40" y="155" width="440" height="145" rx="18" fill="#E5F3EA" stroke="#24715C" stroke-width="3"/><text x="260" y="202" text-anchor="middle" font-size="30" font-weight="bold">Triacylglycerols</text><text x="260" y="240" text-anchor="middle" font-size="23">Glycerol + 3 fatty acids</text><text x="260" y="271" text-anchor="middle" font-size="20">Long-term energy storage</text>
<rect x="520" y="155" width="440" height="145" rx="18" fill="#E7F0FA" stroke="#2E6287" stroke-width="3"/><text x="740" y="202" text-anchor="middle" font-size="30" font-weight="bold">Phospholipids</text><text x="740" y="240" text-anchor="middle" font-size="22">Polar head + hydrophobic tails</text><text x="740" y="271" text-anchor="middle" font-size="20">Membrane organisation</text>
<rect x="40" y="330" width="440" height="145" rx="18" fill="#FFF1DE" stroke="#A36B2A" stroke-width="3"/><text x="260" y="377" text-anchor="middle" font-size="30" font-weight="bold">Waxes</text><text x="260" y="415" text-anchor="middle" font-size="23">Long-chain fatty acid esters</text><text x="260" y="446" text-anchor="middle" font-size="20">Protective waterproof coatings</text>
<rect x="520" y="330" width="440" height="145" rx="18" fill="#F4E6F4" stroke="#885099" stroke-width="3"/><text x="740" y="377" text-anchor="middle" font-size="30" font-weight="bold">Sterols and steroids</text><text x="740" y="415" text-anchor="middle" font-size="23">Four fused carbon rings</text><text x="740" y="446" text-anchor="middle" font-size="20">Membranes and signalling</text></g>
<text x="500" y="541" text-anchor="middle" font-size="20" font-family="sans-serif" fill="#5A4E42">Fatty acids are constituents of many lipids, not a subgroup of triacylglycerols.</text>
</svg>''',encoding="utf-8")
# Replace the misleading figure with a straightforward vermicomposting operations flow.
vermi_svg=SVG/"original_orig22.svg"
data=vermi_svg.read_text(encoding="utf-8")
if '<!-- P3 corrected vermi chart -->' not in data:
    vermi_svg.write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 580" role="img" aria-label="Correct sequence of vermicomposting operations">
<rect x="8" y="8" width="984" height="564" rx="25" fill="#fffdf8" stroke="#c8d4cb" stroke-width="3"/>
<text x="500" y="62" text-anchor="middle" font-size="38" font-family="sans-serif" font-weight="bold" fill="#174A49">VERMICOMPOSTING OPERATIONS</text>
<text x="500" y="101" text-anchor="middle" font-size="23" font-family="sans-serif" fill="#526571">Feedstock management → worm processing → mature amendment</text>
<!-- P3 corrected vermi chart -->
<defs><marker id="a" markerWidth="10" markerHeight="10" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" stroke="#256B53" stroke-width="2" fill="none"/></marker></defs>
<g font-family="sans-serif" text-anchor="middle"><g fill="#e7f3e8" stroke="#2c755d" stroke-width="3"><rect x="45" y="170" rx="14" width="270" height="145"/><rect x="365" y="170" rx="14" width="270" height="145"/><rect x="685" y="170" rx="14" width="270" height="145"/><rect x="45" y="350" rx="14" width="270" height="135"/><rect x="365" y="350" rx="14" width="270" height="135"/><rect x="685" y="350" rx="14" width="270" height="135"/></g>
<g fill="#153f2e" font-size="25" font-weight="bold"><text x="180" y="218">1. Feedstock</text><text x="500" y="218">2. Prepare bed</text><text x="820" y="218">3. Add worms</text><text x="180" y="396">6. Soil use</text><text x="500" y="396">5. Cure and test</text><text x="820" y="396">4. Process</text></g>
<g fill="#39585b" font-size="20"><text x="180" y="263">Select safe organics</text><text x="500" y="263">Moisture + aeration</text><text x="820" y="263">Suitable epigeic species</text><text x="180" y="442">Apply mature compost</text><text x="500" y="442">Assess quality</text><text x="820" y="442">Feed + microbial action</text></g></g>
<g stroke="#256B53" stroke-width="4" fill="none" marker-end="url(#a)"><path d="M318 242 L358 242"/><path d="M638 242 L678 242"/><path d="M820 320 L820 343"/><path d="M680 417 L642 417"/><path d="M360 417 L320 417"/></g>
<text x="500" y="535" text-anchor="middle" font-size="20" font-family="sans-serif" fill="#8b254a">Maintain temperature, moisture, aeration and suitable feedstock; test the mature product.</text>
</svg>''',encoding="utf-8")


# Final typography pass: prevent layout overflow and keep Tamil captions within cards.
swap("original_orig15.svg",
    '<text x="245" y="257" text-anchor="middle" font-size="8.5" fill="#5a4e42">',
    '<text x="245" y="251" text-anchor="middle" font-size="8.5" fill="#5a4e42">')
swap("original_orig15.svg",
    '<text x="245" y="268" text-anchor="middle" font-size="8" fill="#8a1e3c">',
    '<text x="245" y="263" text-anchor="middle" font-size="8" fill="#8a1e3c">')
swap("atlas_cell.svg",
    '<text x="350" y="74">Mitochondrion</text>',
    '<text x="310" y="74">Mitochondrion</text>')
swap("atlas_cell.svg",
    '<text x="310" y="335">Plasma membrane</text>',
    '<text x="270" y="333">Plasma membrane</text>')
def replace_once(name, old, new):
    p=SVG/name
    st=p.read_text(encoding="utf-8")
    if old in st:
        p.write_text(st.replace(old,new),encoding="utf-8")
    elif new not in st:
        raise ValueError(f"Cannot locate {name} text {old[:30]}")
replace_once("supplement_poultrybio.svg",
    'textLength="116" lengthAdjust="spacingAndGlyphs">ஆரோக்கியக் குஞ்சுகள்</text>',
    '>ஆரோக்கியக் குஞ்சுகள்</text>') if False else None
# Long bilingual card strings require two short lines, not ignored SVG textLength.
for file, changes in {
    "supplement_poultrybio.svg":[
        ("ஆரோக்கியக் குஞ்சுகள்","ஆரோக்கியக்"),
        ("காற்றோட்டம் + இடவசதி","காற்றோட்டம் + இடம்")],
    "supplement_dairyhygiene.svg":[
        ("ஆரோக்கியமான மடி","மடிநலம்"),
        ("சுத்தமான பால் கறத்தல்","சுத்தமான கறத்தல்"),
        ("விரைவு குளிரூட்டல்","விரைவுக் குளிரூட்டல்")]
}.items():
    p=SVG/file
    st=p.read_text(encoding="utf-8")
    for old,new in changes:
        st=st.replace(old,new)
    import re
    st=re.sub(r'font-size="12" font-weight="400" fill="#465662" text-anchor="middle"(?: textLength="116" lengthAdjust="spacingAndGlyphs")?>',
              'font-size="9" font-weight="400" fill="#465662" text-anchor="middle">',st)
    p.write_text(st,encoding="utf-8")

targets=[
"original_orig2","original_orig10","original_orig14","original_orig16","original_orig17","native_lac",
"notes_p57","notes_p58","notes_p40","original_orig5","original_orig6","original_orig15","original_orig22","atlas_cell","atlas_ecosystem",
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
