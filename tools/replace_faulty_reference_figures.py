"""Replace six misleading/unlicensed illustrations with original precise label schematics.
The original PDF page figures remain in the source reference only; are not distributed in APK.
"""
from pathlib import Path
import json,cairosvg,html
root=Path(__file__).resolve().parents[1];a=root/'app/src/main/assets';d=json.loads((a/'content.json').read_text('utf8'))
head='''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="780" viewBox="0 0 1280 780"><rect width="1280" height="780" fill="#F6FBF9"/><defs><marker id="a" markerWidth="12" markerHeight="12" refX="8" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="none" stroke="#246752" stroke-width="2"/></marker></defs>'''
def t(x,y,s,size=27,weight='normal',color='#233B45',anchor='middle'):
 return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="DejaVu Sans" font-size="{size}" font-weight="{weight}" fill="{color}">{html.escape(s)}</text>'
def card(x,y,w,h,line1,line2='',fill='#E5F1EB'):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="19" fill="{fill}" stroke="#286F64" stroke-width="3"/>'+t(x+w/2,y+44,line1,24,'bold')+(t(x+w/2,y+83,line2,19) if line2 else '')
def arr(x,y,x2,y2):return f'<path d="M{x},{y} L{x2},{y2}" stroke="#286F64" stroke-width="4" fill="none" marker-end="url(#a)"/>'
def ttl(v,sub):return t(640,55,v,35,'bold','#174A49')+t(640,91,sub,19,color='#425F6D')
# Fix PDF hierarchy diagram omitting Kingdom (7 rungs required below Domain)
s=head+ttl('TAXONOMIC HIERARCHY','Example: human classification, broadest to most specific')
vals=[('Domain','Eukaryota'),('Kingdom','Animalia'),('Phylum','Chordata'),('Class','Mammalia'),('Order','Primates'),('Family','Hominidae'),('Genus','Homo'),('Species','Homo sapiens')]
for i,(k,v) in enumerate(vals):
 y=135+i*77;s+=card(185,y,380,63,k,'')+card(715,y,380,63,v,'', '#EBF0FA');s+=arr(575,y+31,705,y+31)
s+='</svg>'
# binomial typographic
b=head+ttl('BINOMINAL NOMENCLATURE','ICZN Article 5: names for species consist of genus + specific name')
b+=t(640,210,'Panthera leo',76,'bold','#174A49')
b+=arr(485,230,395,340)+arr(785,230,875,340)
b+=card(140,340,450,125,'GENUS','Capital initial: Panthera')+card(685,340,450,125,'SPECIFIC EPITHET','Lowercase: leo')
b+=t(640,545,'Print: italicise both words · Handwriting: underline each word',25)
b+=t(640,615,'Subspecies: Panthera tigris tigris (three words)',24)
b+='</svg>'
# corrected plant cell: cell wall / membrane, nucleus, vacuole, chloroplast, mito, ER, golgi
c=head+ttl('TYPICAL PLANT CELL','Schematic, not to scale — major structures are labelled')
c+='<rect x="355" y="140" width="555" height="545" rx="55" fill="#D9EDBE" stroke="#498448" stroke-width="22"/>'
c+='<rect x="382" y="167" width="501" height="491" rx="44" fill="#F8FAE9" stroke="#6FAA67" stroke-width="7"/>'
c+='<ellipse cx="635" cy="418" rx="145" ry="164" fill="#DCEFF9" stroke="#8CBCD5" stroke-width="7"/>'
c+='<circle cx="475" cy="256" r="66" fill="#D2C6E5" stroke="#75668E" stroke-width="6"/><circle cx="475" cy="255" r="25" fill="#896CAF"/>'
for x,y in [(785,240),(805,540),(483,552)]: c+=f'<ellipse cx="{x}" cy="{y}" rx="55" ry="25" fill="#90CB80" stroke="#467940" stroke-width="4"/><path d="M{x-34},{y} L{x+34},{y}" stroke="#487D36" stroke-width="5"/>'
c+='<ellipse cx="758" cy="331" rx="57" ry="34" fill="#FFC9AA" stroke="#A65C41" stroke-width="5"/>'
c+=t(230,234,'Nucleus',27,'bold')+arr(330,239,400,256)
c+=t(230,410,'Cell wall',27,'bold')+arr(315,415,355,415)
c+=t(235,492,'Cell membrane',25,'bold')+arr(340,490,385,490)
c+=t(1035,250,'Chloroplast',26,'bold')+arr(949,260,850,240)
c+=t(1045,335,'Mitochondrion',25,'bold')+arr(925,335,820,330)
c+=t(1035,440,'Central vacuole',25,'bold')+arr(919,448,775,434)
c+='</svg>'
# monohybrid correct T/t gametes
m=head+ttl('MENDELIAN MONOHYBRID CROSS','Parental generation: TT (tall) × tt (dwarf) → F1: Tt (tall)')
m+=card(140,160,400,120,'Parent 1: TT','Gamete T')+card(740,160,400,120,'Parent 2: tt','Gamete t')
m+=arr(540,275,610,372)+arr(740,275,670,372)+card(430,385,420,112,'F1 generation: Tt','Both inherited alleles')
m+=t(640,580,'F1 self-cross: Tt × Tt gives TT, Tt, Tt, tt',27,'bold')+t(640,652,'Genotypes 1:2:1  ·  Phenotypes 3 tall : 1 dwarf',26)
m+='</svg>'
# spermatogenesis: no unlicensed Britannica asset, correctly balanced meiosis
sp=head+ttl('SPERMATOGENESIS','Human example — chromosome numbers shown')
levels=[('Spermatogonium','2n, mitosis'),('Primary spermatocyte','2n, replicated DNA'),('Secondary spermatocytes','n, after meiosis I'),('Spermatids','n, after meiosis II'),('Spermatozoa','n, differentiation')]
for i,(lab,sub) in enumerate(levels):
 y=130+i*119;sp+=card(375,y,530,95,lab,sub,'#E4EDF5' if i%2 else '#E5F2E9')
 if i<4:sp+=arr(640,y+96,640,y+115)
sp+='</svg>'
# oogenesis accurately with follicle maturation and metaphase-II hold
o=head+ttl('HUMAN OOGENESIS','Arrest points and unequal cytoplasmic division')
levels=[('Oogonium','2n — fetal mitotic proliferation'),('Primary oocyte','2n — arrest in prophase I'),('Secondary oocyte','n — meiosis I completed; 1st polar body'),('Ovulated secondary oocyte','Arrest in metaphase II'),('Ovum / mature female pronucleus','Meiosis II completes after sperm entry')]
for i,(lab,sub) in enumerate(levels):
 y=120+i*121;o+=card(330,y,620,103,lab,sub,'#F8E5EF' if i%2 else '#F0E5F8')
 if i<4:o+=arr(640,y+104,640,y+116)
o+='</svg>'
fix={5:(s,'Taxonomic hierarchy with all eight ranks','முழு எட்டு நிலை வகைப்பாட்டு படிநிலை'),13:(b,'Scientific names — corrected nomenclature','சரியான அறிவியல் பெயரிடல்'),25:(c,'Labelled plant cell organelles (original diagram)','தாவரச் செல் உறுப்புகள் — திருத்தப்பட்ட படம்'),28:(m,'Monohybrid cross: corrected T and t gametes','சரியான T மற்றும் t பாலணுக்களுடன் ஒரு பண்புக் கலப்பு'),57:(sp,'Spermatogenesis — original stepwise schematic','விந்தணு உருவாக்கம் — தனிப்பட்ட படிவரைபடம்'),58:(o,'Oogenesis and meiotic arrest — corrected schematic','முட்டை உருவாக்கம் மற்றும் மியாசிஸ் தடைநிலை')}
for page,(svg,english,tam) in fix.items():
 name=f'notes_p{page:02d}'
 (a/'svg'/f'{name}.svg').write_text(svg,'utf8')
 cairosvg.svg2png(bytestring=svg.encode(),write_to=str(a/'plates'/f'{name}.png'),output_width=1600,output_height=975)
 p=next(v for v in d['plates'] if v['id']==f'notes{page}')
 p['enTitle']=english;p['taTitle']=tam
 p['enCap']=f'Corrected original course schematic; replaces the unsuitable illustration on departmental notes page {page}. Not a reproduction of that image.'
 p['taCap']=f'பாடக்குறிப்பு பக்கம் {page} இல் இருந்த குறைபாடுடைய படத்திற்குப் பதிலாக உருவாக்கப்பட்ட திருத்தப்பட்ட விளக்கப்படம்.'
 p['sourceSvg']=name+'.svg';p['kind']='original-2026-corrected'
 d['editorialRevision'].setdefault('replacedPDFPlates',[]).append(page)
(a/'content.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),'utf8')
print('Corrected six images',list(fix),'resulting teaching plates',len(d['plates']))
