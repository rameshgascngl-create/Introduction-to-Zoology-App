#!/usr/bin/env python3
"""Deterministic, mobile-first teaching plate generator.
These corrected SVG masters and 1200px PNGs are produced at build time.
"""
from pathlib import Path
from math import cos, sin, pi
from html import escape
import cairosvg

ROOT=Path(__file__).resolve().parents[1]/"app/src/main/assets"
def T(x,y,s,size=37,color="#203B4B",bold=False,anchor="start"):
    return f'<text x="{x}" y="{y}" font-family="DejaVu Sans,Arial,sans-serif" font-size="{size}" fill="{color}" font-weight="{"bold" if bold else "normal"}" text-anchor="{anchor}">{escape(s)}</text>'
def R(x,y,w,h,fill="#F4F8FC",stroke="#D0DFE7",radius=20):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
def C(x,y,r,fill="#F8CADA",stroke="#AA5D7B",sw=4):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def P(d,fill,stroke="#526F80",sw=4):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'
def L(x,y,xx,yy,color="#647A87",sw=5):
    return f'<line x1="{x}" y1="{y}" x2="{xx}" y2="{yy}" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/>'
def page(h,title,subtitle,elements):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="'+str(h)+'" viewBox="0 0 1200 '+str(h)+'">'+
            R(0,0,1200,h,"white","white",0)+R(35,35,1130,h-70,"white","#CDDCE5",26)+
            T(85,115,title,48,"#145744",True)+T(85,165,subtitle,26,"#57717E")+"".join(elements)+"</svg>")
def save(name,svg):
    svgpath=ROOT/"svg"/name.replace(".png",".svg")
    pngpath=ROOT/"plates"/name
    svgpath.write_text(svg,encoding="utf8")
    cairosvg.svg2png(bytestring=svg.encode(),write_to=str(pngpath))
    assert pngpath.stat().st_size>3000,(name,pngpath.stat().st_size)
    print(f"RENDERED {name} {pngpath.stat().st_size} bytes")
# GENERALIZED ANIMAL EMBRYO: note mammalian blastocyst is a special blastula.
p=[]
ys=[275,555,835,1115,1395]
labels=[
 ("1   Zygote","Fertilised egg: one cell"),
 ("2   Cleavage","Repeated mitoses with little overall growth"),
 ("3   Morula","Compact, solid cluster of blastomeres"),
 ("4   Blastula","Fluid cavity (blastocoel) enclosed by cells"),
 ("5   Gastrula","Cell movements establish embryonic layers")
]
for n,(y,(title,detail)) in enumerate(zip(ys,labels)):
    p += [R(85,y-80,1030,228),T(405,y+15,title,43,"#194B62",True),T(405,y+69,detail,27)]
    if n<4:p += [L(270,y+156,270,ys[n+1]-100,"#287465",8),P(f"M 270 {ys[n+1]-78} l -16 -26 h 32 z","#287465","#287465",1)]
p += [C(255,286,78)]
p += [C(212,565,44),C(300,565,44)]
for i in range(12):
    a=2*pi*i/12;p.append(C(round(255+54*cos(a)),round(850+54*sin(a)),29))
p += [C(255,1128,78,"#D8EBF7","#497FA9",5),C(255,1128,51,"white","#5A93B0",3)]
for i in range(12):
    a=2*pi*i/12;p.append(C(round(255+68*cos(a)),round(1128+68*sin(a)),14,"#91C8E3","#497FA9",2))
p += [C(255,1407,79,"#FFE5BF","#A77A33"),P("M 194 1387 Q 255 1450 316 1387 Q 310 1460 255 1490 Q 200 1460 194 1387 Z","#F5A681","#B55C55")]
p += [T(90,1652,"Generalised diagram: cleavage and gastrulation vary among animal taxa.",24,"#56727F")]
save("atlas_embryo.png",page(1705,"Early developmental stages","Zygote  →  cleavage  →  morula  →  blastula  →  gastrula",p))
# ATMOSPHERE: preserve layer order, use approximate altitude bands, avoid falsely claiming scale.
p=[]
bands=[
 ("EXOSPHERE","~500–1,000 km and higher","Transitional outermost region","#DBD6EF"),
 ("THERMOSPHERE","~85–500+ km","Absorbs high-energy solar radiation","#C8D9F5"),
 ("MESOSPHERE","~50–85 km","Many meteors ablate here","#DAE8F3"),
 ("STRATOSPHERE","~12–50 km","Contains the ozone-rich region","#C7E9E1"),
 ("TROPOSPHERE","0–~8 to 18 km","Contains most weather and water vapour","#E2F0DE")
]
for i,(title,alt,note,fill) in enumerate(bands):
    y=240+215*i
    p += [R(86,y,1028,202,fill,fill),T(120,y+65,title,43,"#1B4857",True),T(1070,y+63,alt,29,"#254D61",anchor="end"),T(120,y+126,note,30,"#284C59")]
p += [T(87,1395,"Not drawn to altitude scale. Approximate boundaries vary with conditions.",26),
      T(87,1450,"The ionosphere overlaps several regions; it is not a separate thermal layer.",24,"#426777"),
      T(87,1500,"The exosphere is not defined by the temperature gradient.",24,"#426777")]
save("original_orig15.png",page(1565,"Regions of Earth's atmosphere","From space toward Earth's surface  |  Approximate boundaries",p))
# HUMAN GAMETOGENESIS: diploidy/haploidy and meiotic arrest are explicitly distinguished.
p=[R(80,235,1040,690,"#EFF7FD","#C4DDEB"),
   T(120,315,"SPERMATOGENESIS",45,"#185B80",True),
   T(120,380,"Spermatogonium (2n) → primary spermatocyte (2n)",29),
   T(120,448,"Meiosis I → two secondary spermatocytes (n)",29,"#236D7E",True),
   C(360,540,46,"#A8D8F7","#387EAE"),C(780,540,46,"#A8D8F7","#387EAE"),
   T(120,645,"Meiosis II → four spermatids (n)",30,"#236D7E",True)]
for x in [260,470,680,890]:
    p += [C(x,740,35,"#A8D8F7","#387EAE"),P(f"M {x} 778 q 65 15 60 50","none","#387EAE",4)]
p += [T(120,865,"Spermiogenesis → four mature spermatozoa",28)]
p += [R(80,955,1040,740,"#FFF5F8","#F0D1DD"),
      T(120,1030,"OOGENESIS IN HUMANS",45,"#983C64",True),
      T(120,1097,"Primary oocyte (2n): enters meiosis before birth",30),
      T(120,1155,"Arrest at prophase I; meiosis I resumes after puberty",27,"#7E566B"),
      T(120,1230,"Meiosis I → secondary oocyte (n) + first polar body (n)",27,"#983C64",True),
      C(300,1350,77,"#F6BED4","#AC5378"),C(750,1350,25,"#F6BED4","#AC5378"),
      T(120,1460,"Meiosis II begins; arrested at metaphase II",29),
      T(120,1520,"Completion normally follows fertilisation.",30),
      T(120,1590,"Outcome: one functional ovum and polar body/bodies.",27,"#73485E")]
save("atlas_gametes.png",page(1750,"Human gametogenesis","Meiosis, chromosome number and unequal cytokinesis",p))
# NATURAL SELECTION: variation, selective conditions, heritability, differential reproduction.
p=[T(92,245,"Illustrative heritable phenotype variation",33,"#225B66"),
   R(80,288,1040,440,"#EEF6FB","#BADBE9"),
   T(115,360,"BEFORE SELECTION",40,"#20546C",True)]
for i in range(8):
    x=190+(i%4)*220;y=468+(i//4)*126
    p.append(C(x,y,43,"#348CC3" if i<4 else "#CD8737","#35607B",3))
p += [T(115,690,"4 blue   :   4 ochre",29),
      T(90,808,"Suppose the environment favours the ochre phenotype.",29),
      T(90,865,"Differences in survival AND reproductive success alter frequencies.",26),
      R(80,940,1040,420,"#F1F8F2","#C8E2CD"),
      T(115,1010,"LATER GENERATION",40,"#236647",True)]
for i in range(8):
    x=190+(i%4)*220;y=1115+(i//4)*126
    p.append(C(x,y,43,"#348CC3" if i==0 else "#CD8737","#35607B",3))
p += [T(115,1326,"1 blue   :   7 ochre",29),
      T(90,1435,"Illustrative frequencies, not observed data.",26,"#54707A"),
      T(90,1490,"Natural selection has no predetermined direction or goal.",25,"#54707A")]
save("supplement_darwinselection.png",page(1550,"Natural selection across generations","Heritable variants can change in frequency",p))
print("PASS: four diagrams rebuilt as SVG and PNG")
