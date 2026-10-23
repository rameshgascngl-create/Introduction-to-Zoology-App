"""Offline native content asset migration from an already-compiled Compose APK.
Changes packaged course data, native raster gallery, DEX display-version literal and
AXML manifest version metadata; no WebView code is introduced. Signs APK v2.
NOT equivalent to a clean Kotlin/Gradle build and NOT a production-signed release.
"""
import zipfile,pathlib,io,struct,sys,hashlib,zlib,json,os
from apk_v2_utility import sign,keypair,verify
ROOT=pathlib.Path(__file__).resolve().parents[1]
OLD=pathlib.Path('/mnt/data/Introduction_to_Zoology_v6.0.0_TRUE_NATIVE_DEBUG.apk')
NEW=pathlib.Path('/mnt/data/Introduction_to_Zoology_v6.1.0_NATIVE_CONTENT_DEVELOPMENT.apk')
A=ROOT/'app/src/main/assets'
original=zipfile.ZipFile(OLD)
orig=set(original.namelist())
updated={}
updated['assets/content.json']=(A/'content.json').read_bytes()
manifest=original.read('AndroidManifest.xml')
assert manifest.count('6.0.0'.encode('utf-16le'))==1
manifest=manifest.replace('6.0.0'.encode('utf-16le'),'6.1.0'.encode('utf-16le'))
assert manifest.count((600).to_bytes(4,'little'))==1
manifest=manifest.replace((600).to_bytes(4,'little'),(610).to_bytes(4,'little'))
updated['AndroidManifest.xml']=manifest
# Change native Compose top-bar version constant in classes3.dex. Correct Dex integrity header.
dex=bytearray(original.read('classes3.dex'))
assert dex.count(b'6.0.0')==1,dex.count(b'6.0.0')
dex=dex.replace(b'6.0.0',b'6.1.0')
dex[12:32]=hashlib.sha1(dex[32:]).digest()
dex[8:12]=struct.pack('<I',zlib.adler32(dex[12:])&0xffffffff)
updated['classes3.dex']=bytes(dex)
# New images sourced from the departmental PDF and SVG authored for the course.
for item in (A/'plates').glob('*.png'):
 rel='assets/plates/'+item.name
 if rel not in orig:updated[rel]=item.read_bytes()
# Remove older signature files because all signing data is reissued.
remove=lambda name:name.startswith('META-INF/') and (name.endswith(('.SF','.RSA','.DSA')) or name.endswith('MANIFEST.MF'))
paths={x for x in orig if not remove(x)} | set(updated)
# Put heavy payloads in the order of the original package (improves seeking), append new image data.
ordered=[x.filename for x in original.infolist() if x.filename in paths]+sorted(paths-orig)
unsigned=io.BytesIO()
with zipfile.ZipFile(unsigned,'w',allowZip64=False) as out:
 for name in ordered:
  old=original.getinfo(name) if name in orig else None
  data=updated.get(name) if name in updated else original.read(name)
  inf=zipfile.ZipInfo(name)
  inf.compress_type=(old.compress_type if old else zipfile.ZIP_DEFLATED)
  inf.date_time=old.date_time if old else (2026,10,23,11,30,0)
  inf.external_attr=old.external_attr if old else 0o644<<16
  inf.flag_bits=0
  # Android mmap requires uncompressed resources.arsc 4-byte aligned and uncompressed .so 4096 aligned.
  alignment=4096 if name.startswith('lib/') and name.endswith('.so') and inf.compress_type==zipfile.ZIP_STORED else (4 if name=='resources.arsc' and inf.compress_type==zipfile.ZIP_STORED else 0)
  if alignment:
   localstart=out.fp.tell()
   predicted=localstart+30+len(name.encode('utf8'))
   padding=(-predicted)%alignment
   if padding<4:padding+=alignment
   inf.extra=b'\x00\x00'+struct.pack('<H',padding-4)+bytes(padding-4)
  out.writestr(inf,data,compress_type=inf.compress_type,compresslevel=6)
unsigned_bytes=unsigned.getvalue()
# Before signing, independently verify the ZIP archive and its local data offsets.
z=zipfile.ZipFile(io.BytesIO(unsigned_bytes))
assert z.testzip() is None
assert json.loads(z.read('assets/content.json'))['edition']=='6.1.0'
for f in z.infolist():
 if f.filename=='resources.arsc' or f.filename.startswith('lib/') and f.filename.endswith('.so') and f.compress_type==0:
  data_pos=f.header_offset+30+len(f.filename.encode('utf8'))+len(f.extra)
  mod=4096 if f.filename.startswith('lib/') else 4
  assert data_pos%mod==0,(f.filename,data_pos,mod)
# Sign scheme v2 with a new temporary certificate (production signing not available).
key,cert=keypair()
final=sign(unsigned_bytes,key,cert)
verification=verify(final)
NEW.write_bytes(final)
verified=zipfile.ZipFile(NEW)
assert verified.testzip() is None
assert verified.read('assets/content.json')==updated['assets/content.json']
assert verified.read('AndroidManifest.xml')==updated['AndroidManifest.xml']
assert verified.read('classes3.dex')==updated['classes3.dex']
assert len(final)>21_000_000
print('APK',NEW,'size_bytes',len(final))
print('NATIVE DEX source matched, manifest bump and updated content validated, v2 signature cryptographically verified')
print(json.dumps(verification,indent=2))
(NEW.with_suffix('.sha256')).write_text(verification['signed_file_sha256']+'  '+NEW.name+'\n')
