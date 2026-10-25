"""Full static integrity validation for native v6.1.0 textbook and editorial provenance."""
import json,pathlib,re,collections,sys,hashlib,struct
project=pathlib.Path(__file__).resolve().parents[1]; a=project/'app/src/main/assets'
d=json.loads((a/'content.json').read_text('utf8'))
# A textbook edition and Android version must always agree at build time.
gradle=(project/'app/build.gradle.kts').read_text()
version=re.search(r'versionName\s*=\s*"([^"]+)"',gradle)
assert version, 'Missing Android versionName in Gradle'
assert d['edition']==version.group(1),(
    'Textbook edition does not match Android versionName',
    d['edition'],version.group(1))
assert len(d['units'])==5 and len(d['chapters'])==28
assert len(d['plates'])==58
assert len(d['questionBank'])==5
assert [x['id'] for x in d['chapters'] if x['unit']==3][-1]=='3.5'
assert len(set(x['id'] for x in d['chapters']))==28
assert len(set(x['id'] for x in d['plates']))==58
for u in d['units']:
    unit_ch=[c for c in d['chapters'] if c['unit']==u['id']]
    assert unit_ch
    assert [c['n'] for c in unit_ch]==list(range(1,len(unit_ch)+1)),u['id']
for ch in d['chapters']:
    for k in ('contentEn','contentTa','enTitle','taTitle','misEn','misTa','activityEn','activityTa','sourcePages'):
        assert ch[k],(ch['id'],k)
    assert len(re.sub(r'<[^>]+>','',ch['contentEn']))>=1450,ch['id']
    assert len(ch['contentTa'])>=900,ch['id']
    assert re.match(r'^\d+\.\d+$',ch['id'])
    assert '<script' not in ch['contentEn'].lower()
    assert all(isinstance(p,int) and 1<=p<=85 for p in ch['sourcePages'])
ids={x['id'] for x in d['chapters']}
for plate in d['plates']:
    assert plate['chapter'] in ids
    assert (a/'plates'/plate['filename']).stat().st_size>3000
    if plate['sourceSvg']:
        assert (a/'svg'/plate['sourceSvg']).stat().st_size>500
    else:
        assert plate['kind']=='reference-notes' and plate.get('sourcePages')
    assert plate['enTitle'] and plate['taTitle']
assert {p['chapter'] for p in d['plates']} >=ids

# Phase II syllabus-equivalence gate: Habitat is explicitly required by Unit IV.
by_id={c['id']:c for c in d['chapters']}
ecology=by_id['4.2']
assert 'habitat' in ecology['contentEn'].lower()
# Microhabitat has not been explicitly developed in recovered v6.3.0 lessons.
# Track as an editorial gap instead of claiming a syllabus equivalence pass.
# Standardise biology terminology without replacing Kotlin/Compose 'key' identifiers.
# The editorially preferred functional equivalent is 'இருபிரிவு இனங்காணல் முறை' for Dichotomous key.
taxonomy = by_id['1.1']['contentTa']
assert 'உயிரின இனங்காணல் வழிமுறை (Identification key)' in taxonomy
assert 'இருபிரிவு இனங்காணல் முறை (Dichotomous key)' in taxonomy
assert 'இருகிளைத் திறவுகோல்' not in taxonomy
assert 'ஒன்றுக்கொன்று மாறுபட்ட இரண்டு பண்புக் கூற்றுகளில்' in taxonomy
assert 'வாழிடம்' in ecology['contentTa']
assert 'niche' in ecology['contentEn'].lower()
assert any('habitat' in q['q'].lower() for q in d['questionBank']['4']['mcqEn'])
assert any('வாழிடம்' in q['q'] for q in d['questionBank']['4']['mcqTa'])
# Check actual figure bytes instead of trusting a filename and file size.
plate_hashes=[]
for plate in d['plates']:
    image=(a/'plates'/plate['filename'])
    with image.open('rb') as handle:
        header=handle.read(24)
    assert header[:8]==b'\x89PNG\r\n\x1a\n',(plate['id'],'not PNG')
    width,height=struct.unpack('>II',header[16:24])
    assert width>=300 and height>=100,(plate['id'],'unreadably small',width,height)
    plate_hashes.append(hashlib.sha256(image.read_bytes()).hexdigest())
assert len(set(plate_hashes))==58,'Some teaching plates contain identical pixels'
assert all(re.search(r'[\u0B80-\u0BFF]', c['contentTa']) for c in d['chapters']), 'Tamil body text missing'

for bank in d['questionBank'].values():
    assert len(bank['mcqEn'])==len(bank['mcqTa'])
    assert len(bank['bEn'])==len(bank['bTa'])
    assert len(bank['cEn'])==len(bank['cTa'])
    for q in bank['mcqEn']+bank['mcqTa']:
        assert len(q['o'])==4 and q['a'] in 'ABCD',q
        assert len(q.get('r','').strip())>=25,('Missing explanation',q['q'])
        assert len(set(x.lower().strip() for x in q['o']))==4,('Duplicate options',q['q'])
for unit,bank in d['questionBank'].items():
    # Position balancing is a valid static invariant; answer letter must move with its option.
    positions=collections.Counter(q['a'] for q in bank['mcqEn'])
    assert max(positions.values())-min(positions.get(x,0) for x in 'ABCD')<=1,(unit,positions)
    assert all(q['a']==t['a'] for q,t in zip(bank['mcqEn'],bank['mcqTa'])),unit
    assert all(not re.search(r'[\u0B80-\u0BFF]',option) for q in bank['mcqEn'] for option in q['o']),('Tamil distractor in English',unit)
    assert all(re.search(r'[\u0B80-\u0BFF]',q['r']) for q in bank['mcqTa']),('Missing Tamil rationale',unit)
assert 'homeostasis' in by_id['3.5']['contentEn'].lower()
assert 'digestive system' in by_id['3.5']['contentEn'].lower()
assert 'சமநிலை பேணுதல்' in by_id['3.5']['contentTa']
# Editorial QA: enforce both-language parity for microhabitat and germ layers.
ecology = by_id['4.2']
embryology = by_id['4.4']
assert 'Microhabitat:' in ecology['contentEn'] and 'நுண்வாழிடம் (Microhabitat)' in ecology['contentTa']
assert 'a <em>place</em>' in ecology['contentEn'] and 'நுண்வாழிடம் என்பது' in ecology['contentTa']
assert 'சூழலியல் பங்குயும்' not in ecology['contentTa']
assert 'ஓம்புயிரிக்குத் தீங்கு' in ecology['contentTa'] and 'விருந்தோம்பிக்குத் தீங்கு' not in ecology['contentTa']
assert 'does not always follow one fixed path' in ecology['contentEn']
assert 'நிரந்தர முடிவை அடைவதில்லை' in ecology['contentTa']
assert 'Sponges (Porifera) lack true tissues and true germ layers' in embryology['contentEn']
assert 'கடற்பஞ்சுகளுக்கு (Porifera) உண்மையான திசுக்களோ கருப்படைகளோ இல்லை' in embryology['contentTa']
assert 'Sponges and cnidarians have only two layers' not in embryology['contentEn']
assert 'கடற்பஞ்சுகள், நிடேரியர்களுக்கு இரு படைகள்' not in embryology['contentTa']
assert 'மூவடுக்குக் கருக்கோளமாக்கம் (Gastrulation)' in embryology['contentTa']
assert 'பிளவிப்பெருகல் (Cleavage)' in embryology['contentTa']
assert 'இருபால் உயிரிகள் (hermaphrodites)' in by_id['1.5']['contentTa']
assert 'ஈருடலிகள்' not in by_id['1.5']['contentTa']
assert 'ஓம்புயிரி செல்களில்' in by_id['5.6']['contentTa']
# Contextual Tamil zoological terminology regression checks.
# 'திறவுகோல்' occurs in school textbooks, but this edition uses a descriptive
# reader-friendly equivalent; do not blindly replace Kotlin Compose key().
tamil_payload=json.dumps({
    'chapters':[{'title':c['taTitle'],'lesson':c['contentTa'],'mis':c['misTa'],'activity':c['activityTa']} for c in d['chapters']],
    'plates':[{'title':p['taTitle'],'caption':p['taCap']} for p in d['plates']],
    'banks':{k:{name:val for name,val in q.items() if name.endswith('Ta')} for k,q in d['questionBank'].items()}
},ensure_ascii=False)
for wrong in ('திறவுகோல்','முறையியல்','மாதிரி மாதிரியம்','ஆலிலை வடிவம்',
              'மும்மொழிப் பெயர்','சிற்றினப் பெயரடை','வாழ்க்கை நிலை'):
    assert wrong not in tamil_payload,('Disallowed ambiguous Tamil translation',wrong)
assert 'இருபிரிவு இனங்காணல் முறை (Dichotomous key)' in by_id['1.1']['contentTa']
assert 'இனத்தொடர்பு தொகுப்பமைவு (Systematics)' in by_id['1.1']['contentTa']
assert 'அமைப்பொத்த உறுப்புகள்' in by_id['1.1']['contentTa']
assert 'செயலொத்த உறுப்புகள்' in by_id['1.1']['contentTa']
assert 'முச்சொல் பெயர் – trinomen' in by_id['1.4']['contentTa']
assert 'வகைப்பாட்டு மாதிரி நிர்ணயம் (Typification)' in by_id['1.4']['contentTa']
assert 'குளோவர் இலை வடிவம்' in by_id['2.4']['contentTa']
assert 'சூழலியல் பங்கு (Ecological niche)' in by_id['4.2']['contentTa']
assert 'முதுகுப்புறக் குழல்வடிவ நரம்புநாண்' in by_id['1.6']['contentTa']
assert 'சமச்சீர் (Symmetry)' in by_id['1.5']['contentTa']
assert 'நவீன உருவாக்கக் கோட்பாடு' in by_id['4.6']['contentTa']
assert 'மரபியல் நகர்வு (Genetic drift)' in by_id['4.6']['contentTa']
assert 'ஒப்பாரின்–ஹால்டேன்' in by_id['4.5']['contentTa']
for inaccurate in ('செயற்கைக் கொள்கை','இனத்தொடர்பு தொகுப்பமைவியல்','சீரமைவு',
                   'முதுகுப்புற உள்ளீடற்ற','மரபணு நகர்வு','வாழிடம் முகவரி; நிச் தொழில்'):
    assert inaccurate not in tamil_payload,('Contextual mistranslation',inaccurate)


assert not any('android.webkit.WebView' in p.read_text() for p in (project/'app/src/main/java').rglob('*.kt'))
sums=[sum(len(v[k]) for v in d['questionBank'].values()) for k in ('mcqEn','bEn','cEn')]
assert sums==[62,41,26],sums
counts=collections.Counter(x['kind'] for x in d['plates']);print('PASS: 5 units, 28 bilingual chapters, 58 diagrams',dict(counts),'62 MCQ, 41 short, 26 long; NO WebView')
