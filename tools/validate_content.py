"""Full static integrity validation for native v6.1.0 textbook and editorial provenance."""
import json,pathlib,re,collections,sys,hashlib,struct
project=pathlib.Path(__file__).resolve().parents[1]; a=project/'app/src/main/assets'
d=json.loads((a/'content.json').read_text('utf8'))
assert d['edition'] in ('6.2.0-QA','6.2.0')
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
assert 'habitat' in ecology['contentEn'].lower() and 'microhabitat' in ecology['contentEn'].lower()
assert 'வாழிடம்' in ecology['contentTa'] and 'நுண்வாழிடம்' in ecology['contentTa']
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
assert 'Functional physiology: processes' in by_id['3.5']['contentEn']
assert 'உறுப்பு மண்டலங்களின் செயல்முறைகளும்' in by_id['3.5']['contentTa']

assert not any('android.webkit.WebView' in p.read_text() for p in (project/'app/src/main/java').rglob('*.kt'))
sums=[sum(len(v[k]) for v in d['questionBank'].values()) for k in ('mcqEn','bEn','cEn')]
assert sums==[62,41,26],sums
counts=collections.Counter(x['kind'] for x in d['plates']);print('PASS: 5 units, 28 bilingual chapters, 58 diagrams',dict(counts),'62 MCQ, 41 short, 26 long; NO WebView')
