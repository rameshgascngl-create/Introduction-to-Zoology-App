"""Full static integrity validation for native v6.1.0 textbook and editorial provenance."""
import json,pathlib,re,collections,sys
project=pathlib.Path(__file__).resolve().parents[1]; a=project/'app/src/main/assets'
d=json.loads((a/'content.json').read_text('utf8'))
assert d['edition']=='6.1.0'
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
for bank in d['questionBank'].values():
    assert len(bank['mcqEn'])==len(bank['mcqTa'])
    assert len(bank['bEn'])==len(bank['bTa'])
    assert len(bank['cEn'])==len(bank['cTa'])
    for q in bank['mcqEn']+bank['mcqTa']:
        assert len(q['o'])==4 and q['a'] in 'ABCD',q
assert not any('android.webkit.WebView' in p.read_text() for p in (project/'app/src/main/java').rglob('*.kt'))
sums=[sum(len(v[k]) for v in d['questionBank'].values()) for k in ('mcqEn','bEn','cEn')]
assert sums==[62,41,26],sums
counts=collections.Counter(x['kind'] for x in d['plates']);print('PASS: 5 units, 28 bilingual chapters, 58 diagrams',dict(counts),'62 MCQ, 41 short, 26 long; NO WebView')
