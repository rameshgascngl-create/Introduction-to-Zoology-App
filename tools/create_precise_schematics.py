"""Deterministic SVG master diagrams with legible English labels for bilingual native captions.
These are conceptual teaching charts, not organism morphology plates.
"""
import pathlib,cairosvg,json
root=pathlib.Path(__file__).resolve().parents[1];a=root/'app/src/main/assets';d=json.loads((a/'content.json').read_text('utf-8'))
HEADER='''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="660" viewBox="0 0 1200 660"><rect width="1200" height="660" rx="25" fill="#F6FAFB"/><defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="7" refY="3" orient="auto"><path d="M0 0 L7 3 L0 6" fill="none" stroke="#246753" stroke-width="1.5"/></marker></defs>'''
def box(x,y,w,h,title,sub,fill='#E3F2EA'):
 return f'''<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{fill}" stroke="#227A67" stroke-width="2"/><text x="{x+w/2}" y="{y+43}" font-family="DejaVu Sans" font-weight="bold" font-size="26" text-anchor="middle" fill="#153E49">{title}</text><text x="{x+w/2}" y="{y+77}" font-family="DejaVu Sans" font-size="18" text-anchor="middle" fill="#2B5161">{sub}</text>'''
def arrow(x1,y1,x2,y2):return f'<path d="M{x1},{y1} L{x2},{y2}" stroke="#246753" stroke-width="4" fill="none" marker-end="url(#arrow)"/>'
def title(t,sub):return f'<text x="600" y="56" text-anchor="middle" font-family="DejaVu Sans" font-weight="bold" font-size="36" fill="#133E50">{t}</text><text x="600" y="88" text-anchor="middle" font-family="DejaVu Sans" font-size="18" fill="#586B73">{sub}</text>'
# diagrams display large labels and no speculative anatomy
phys=HEADER+title('PHYSIOLOGICAL SYSTEMS WORK TOGETHER','Example: oxygen transport and activity')
phys+=box(70,140,280,110,'Respiratory','Oxygen enters blood')+box(460,140,280,110,'Circulatory','Transports oxygen')+box(850,140,280,110,'Muscular','Uses ATP for work')
phys+=arrow(355,195,450,195)+arrow(745,195,840,195)
phys+=box(70,350,280,110,'Nervous','Rapid coordination','#E5ECF7')+box(460,350,280,110,'Endocrine','Hormonal control','#E5ECF7')+box(850,350,280,110,'Excretory','Water and ion balance','#E5ECF7')
phys+=arrow(210,345,210,265)+arrow(600,345,600,265)+arrow(990,345,990,265)
phys+='<text x="600" y="550" text-anchor="middle" font-family="DejaVu Sans" font-size="24" font-weight="bold" fill="#246753">Homeostasis = coordinated regulation of the internal environment</text></svg>'
aqua=HEADER+title('AQUARIUM BIOLOGICAL FILTRATION','A simplified nitrogen transformation pathway')
aqua+=box(40,190,250,110,'Waste / Feed','Nitrogen enters water')+box(340,190,250,110,'Ammonia','NH3 / NH4+')+box(650,190,230,110,'Nitrite','NO2-')+box(930,190,230,110,'Nitrate','NO3-')
for x1,x2 in [(295,330),(595,640),(885,920)]:aqua+=arrow(x1,245,x2,245)
aqua+=box(140,400,400,110,'Microbial biofilter','Nitrifying microbial communities','#E5ECF7')+box(650,400,410,110,'Water changes / plants','Help manage nitrate accumulation','#E5ECF7')
aqua+=arrow(530,400,540,310)+arrow(890,305,855,390)
aqua+='<text x="600" y="588" text-anchor="middle" font-family="DejaVu Sans" font-size="18" fill="#536A74">Monitor pH, dissolved oxygen and temperature; never stock fish before biofiltration is established.</text></svg>'
lac=HEADER+title('LAC CULTIVATION: FIELD OPERATIONS','Kerria lacca — resin production on living host twigs')
items=[('Prepare host','Prune suitable twigs'),('Select broodlac','Healthy inoculum'),('Place broodlac','Attach to host shoots'),('Crawler settlement','Insects attach to twigs'),('Resin secretion','Protective lac encrustation'),('Harvest / process','Sticklac to seedlac')]
for i,(t,s) in enumerate(items):
 x=35+(i%3)*400;y=135+(i//3)*220
 lac+=box(x,y,340,120,t,s)
 if i%3<2: lac+=arrow(x+346,y+60,x+390,y+60)
lac+=arrow(1050,260,1050,335)+arrow(1050,335,205,335)+arrow(205,335,205,350)
lac+='<text x="600" y="618" font-family="DejaVu Sans" font-size="19" text-anchor="middle" fill="#4B6470">Based on ICAR–Indian Institute of Natural Resins and Gums production guidance.</text></svg>'
configs=[('native_physio','3.5','Integrated physiology — organ-system coordination','உறுப்பு மண்டலங்களின் ஒருங்கிணைப்பு',phys),('native_aquarium','5.1','Aquarium biofiltration and the nitrogen cycle','மீன்தொட்டி உயிரியல் வடிகட்டலும் நைட்ரஜன் சுழற்சியும்',aqua),('native_lac','5.4','Lac culture — production operations','அரக்குப் பூச்சி வளர்ப்பு — செயற்பாடுகள்',lac)]
for id,chapter,en,ta,svg in configs:
 (a/'svg'/f'{id}.svg').write_text(svg,encoding='utf-8')
 cairosvg.svg2png(bytestring=svg.encode('utf8'),write_to=str(a/'plates'/f'{id}.png'),output_width=1500,output_height=825)
 d['plates'].append({'id':id,'chapter':chapter,'enTitle':en,'taTitle':ta,'enCap':'Original concept schematic drawn for the native textbook; labels are explanatory, not a specimen anatomy plate.','taCap':'மாணவர்களின் கருத்துப் புரிதலுக்காக உருவாக்கப்பட்ட விளக்க வரைபடம்.','filename':id+'.png','sourceSvg':id+'.svg','kind':'original-2026'})
(a/'content.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),'utf8')
print('diagrams created:',len(configs),'total',len(d['plates']))
