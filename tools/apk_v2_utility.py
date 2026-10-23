"""Minimal APK Signature Scheme v2 sign/verify for reproducible offline native asset updates.
Designed for ZIP32 APKs and minSdk >= 24. No network, no apksigner binary required.
Uses standard APK chunked content digest and RSA PKCS1/SHA256 algorithm 0x0103.
"""
import io,os,sys,zipfile,struct,hashlib,shutil,pathlib,datetime
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa,padding
from cryptography import x509
from cryptography.x509.oid import NameOID
MAGIC=b'APK Sig Block 42'
V2=0x7109871a
ALG=0x0103
U32=lambda n:struct.pack('<I',n)
U64=lambda n:struct.pack('<Q',n)
LP=lambda b:U32(len(b))+b

def get_eocd(b):
 pos=b.rfind(b'PK\x05\x06')
 if pos<0 or pos+22>len(b):raise ValueError('no eocd')
 _,disk,disk2,entries,entries2,csize,coff,clen=struct.unpack_from('<IHHHHIIH',b,pos)
 if entries!=entries2 or disk or disk2 or coff==0xffffffff:raise ValueError('ZIP64 or multi-disk not supported')
 if pos+22+clen!=len(b):raise ValueError('invalid EOCD placement')
 return pos,coff,csize

def get_apk_signing_block(b):
 _,cd,_=get_eocd(b)
 if b[cd-16:cd]!=MAGIC:raise ValueError('no signing block magic')
 length=struct.unpack_from('<Q',b,cd-24)[0]
 start=cd-length-8
 if start<0 or struct.unpack_from('<Q',b,start)[0]!=length:raise ValueError('invalid signing block size')
 pairs={};pos=start+8
 while pos<cd-24:
  pairlen=struct.unpack_from('<Q',b,pos)[0];pos+=8
  sid=struct.unpack_from('<I',b,pos)[0];pos+=4
  pairs[sid]=b[pos:pos+pairlen-4];pos+=pairlen-4
 if pos!=cd-24:raise ValueError('invalid pairs')
 return start,cd,pairs

def readlp(s,p):
 if p+4>len(s):raise ValueError('LP truncated')
 n=struct.unpack_from('<I',s,p)[0];p+=4
 if p+n>len(s):raise ValueError('LP body truncated')
 return s[p:p+n],p+n

def digest(b,begin,cd):
 eocd,_,_=get_eocd(b)
 # chunk digest over the part before signing block, central directory, EOCD with modified CD offset
 sections=[memoryview(b)[:begin],memoryview(b)[cd:eocd],bytes(b[eocd:eocd+16])+U32(begin)+bytes(b[eocd+20:])]
 hlist=[]
 for section in sections:
  for start in range(0,len(section),1024*1024):
   part=section[start:start+1024*1024]
   hlist.append(hashlib.sha256(b'\xa5'+U32(len(part))+part).digest())
 return hashlib.sha256(b'\x5a'+U32(len(hlist))+b''.join(hlist)).digest()

def verify(b):
 from cryptography.hazmat.primitives.asymmetric import padding
 begin,cd,pairs=get_apk_signing_block(b)
 if V2 not in pairs:raise ValueError('no scheme v2 signer')
 signers,end=readlp(pairs[V2],0)
 if end!=len(pairs[V2]):raise ValueError('extra v2 bytes')
 signer,end=readlp(signers,0)
 if end!=len(signers):raise ValueError('multiple signer unsupported in utility')
 signed,p=readlp(signer,0);sigs,p=readlp(signer,p);pub,p=readlp(signer,p)
 if p!=len(signer):raise ValueError('trailing signer')
 dg,pos=readlp(signed,0);certs,pos=readlp(signed,pos);attrs,pos=readlp(signed,pos)
 if pos != len(signed):
  extra,pos=readlp(signed,pos)
  if extra or pos!=len(signed):raise ValueError('bad signed data')
 rec,pp=readlp(dg,0); algo=struct.unpack_from('<I',rec)[0]; digest_bytes,rd=readlp(rec,4)
 sr,sp=readlp(sigs,0);algorithm=struct.unpack_from('<I',sr)[0];signature,sp2=readlp(sr,4)
 crt,cp=readlp(certs,0)
 if algo!=ALG or algorithm!=ALG:raise ValueError(f'unsupported algorithm {algo:#x}, {algorithm:#x}')
 cert=x509.load_der_x509_certificate(crt)
 key=serialization.load_der_public_key(pub)
 if key.public_bytes(serialization.Encoding.DER,serialization.PublicFormat.SubjectPublicKeyInfo)!=cert.public_key().public_bytes(serialization.Encoding.DER,serialization.PublicFormat.SubjectPublicKeyInfo):raise ValueError('key differs from cert')
 key.verify(signature,signed,padding.PKCS1v15(),hashes.SHA256())
 actual=digest(b,begin,cd)
 if actual!=digest_bytes:raise ValueError(f'content digest mismatch {actual.hex()} != {digest_bytes.hex()}')
 return {'digest':actual.hex(),'cert_sha256':hashlib.sha256(crt).hexdigest(),'signed_file_sha256':hashlib.sha256(b).hexdigest()}

def signer_value(key,cert,content_digest):
 digest_rec=LP(U32(ALG)+LP(content_digest))
 sdata=LP(digest_rec)+LP(LP(cert.public_bytes(serialization.Encoding.DER)))+LP(b'')
 sig=key.sign(sdata,padding.PKCS1v15(),hashes.SHA256())
 sig_rec=LP(U32(ALG)+LP(sig))
 pub=key.public_key().public_bytes(serialization.Encoding.DER,serialization.PublicFormat.SubjectPublicKeyInfo)
 return LP(LP(sdata)+LP(sig_rec)+LP(pub))

def sign(b,key,cert):
 eocd,coff,_=get_eocd(b)
 # unsigned file contains no APK signing block
 if b[coff-16:coff]==MAGIC:raise ValueError('input already signed')
 dd=digest(b,coff,coff)
 val=LP(signer_value(key,cert,dd))
 pair=U64(len(val)+4)+U32(V2)+val
 sz=len(pair)+24
 sigblock=U64(sz)+pair+U64(sz)+MAGIC
 out=b[:coff]+sigblock+b[coff:eocd]+b[eocd:eocd+16]+U32(coff+len(sigblock))+b[eocd+20:]
 return out

def keypair():
 key=rsa.generate_private_key(public_exponent=65537,key_size=3072)
 sub=x509.Name([x509.NameAttribute(NameOID.COMMON_NAME,'Introduction to Zoology Native v6.1 Development'),x509.NameAttribute(NameOID.ORGANIZATION_NAME,'Offline Academic QA')])
 cert=x509.CertificateBuilder().subject_name(sub).issuer_name(sub).public_key(key.public_key()).serial_number(x509.random_serial_number()).not_valid_before(datetime.datetime(2026,1,1,tzinfo=datetime.timezone.utc)).not_valid_after(datetime.datetime(2040,1,1,tzinfo=datetime.timezone.utc)).sign(key,hashes.SHA256())
 return key,cert

if __name__=='__main__':
 b=pathlib.Path(sys.argv[1]).read_bytes();print(verify(b))
