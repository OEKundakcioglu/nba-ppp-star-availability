#!/usr/bin/env python3
"""Read-only stdlib audit of recovered NBA source metadata and independent coder labels."""
from pathlib import Path
from collections import Counter
import csv, gzip, hashlib, io, json, sys

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'provenance/historical_sources'
COD = ROOT / 'validation/independent_human_coding_2026_09'
MANIFEST = ROOT / 'manifests/SOURCE_AND_CODING_EXTENSION_SHA256.csv'
EXPECTED_COUNTS = {
 'audit_2020_21_upload.zip': 617,
 'audit_2021_22_upload.zip': 5567,
 'audit_2022_23_upload.zip': 5541,
 'audit_2023_24_upload.zip': 5441,
 'audit_2024_25_upload.zip': 5566,
 'audit_2025_26_upload.zip': 1497,
 'audit_2025_26_targeted_upload.zip': 3526,
}
LABELS = ('explicit_rest','illness','other_non_injury','specific','vague','unknown')

def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()

def csvrows(path):
 opener=gzip.open if str(path).endswith('.gz') else open
 with opener(path,'rt',encoding='utf-8-sig',newline='') as f:
  return list(csv.DictReader(f))

def verify():
 errors=[]
 def check(cond,desc):
  if not cond:errors.append(desc)
 # Source-archive checksums refer to the actual uncompressed CSV bytes.
 meta=json.loads((SRC/'ORIGINAL_SOURCE_MEMBER_SHA256.json').read_text())
 for name,dig in meta['members_uncompressed_sha256'].items():
  path=SRC/name
  if not path.exists():path=SRC/(name+'.gz')
  with (gzip.open(path,'rb') if str(path).endswith('.gz') else path.open('rb')) as f:
   h=hashlib.sha256()
   for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
  check(h.hexdigest()==dig,'Historical original-member digest mismatch: '+name)
 # All files added by this extension, including documentation and code.
 for entry in csvrows(MANIFEST):
  path=ROOT/entry['relative_path']
  check(path.is_file() and path.stat().st_size==int(entry['size_bytes']) and digest(path)==entry['sha256'],
        'Extension checksum mismatch: '+entry['relative_path'])
 injury=csvrows(SRC/'injury_report_inventory.csv.gz')
 kept=[r for r in injury if r['pdf_present'].lower()=='true']
 counts=Counter(r['archive'] for r in kept)
 check(len(injury)==37342,'Injury URL candidate count')
 check(len(kept)==27755,'Actual PDF count')
 check(dict(counts)==EXPECTED_COUNTS,'Per-archive PDF counts')
 check(all(r['hash_status']=='match' and r['computed_sha256'] and r['manifest_sha256']==r['computed_sha256'] for r in kept),'Archived manifest hashes disagree')
 archive_summary=csvrows(SRC/'injury_archive_summary.csv')
 check(len(archive_summary)==7 and all(int(r['stored_pdfs'])==counts[r['archive']] for r in archive_summary),'Archive summary counts')
 sample=csvrows(SRC/'primary_sample_report_map.csv.gz')
 check(len(sample)==7230 and len({r['game_id'] for r in sample})==7230,'Primary selected-game count/uniqueness')
 check(len({(r['archive'],r['archive_member']) for r in sample})==2054,'Distinct selected PDF count')
 known={(r['archive'],r['archive_member'],r['computed_sha256']) for r in kept}
 check(all((r['archive'],r['archive_member'],r['computed_sha256']) in known for r in sample),'Selected PDF is not indexed as saved/hash matched')
 box=csvrows(SRC/'boxscore_source_map.csv.gz')
 check(len(box)==7230 and len({r['nba_game_id'] for r in box})==7230,'Boxscore game ID count')
 check({r['game_id'] for r in sample}=={r['game_id'] for r in box},'Boxscore/selected-report game alignment')
 older=csvrows(SRC/'archived_game_report_links.csv.gz')
 check(len(older)==14460,'Historical game-report links count')
 exceptions=csvrows(SRC/'selected_report_timestamp_exceptions.csv')
 check(len(exceptions)==21 and len({(r['archive'],r['archive_member']) for r in exceptions})==8,'21-game/8-PDF exceptions')
 keys={(r['game_id'],r['archive'],r['archive_member']) for r in sample}
 check(all((r['game_id'],r['archive'],r['archive_member']) in keys for r in exceptions),'Exception selections not in primary map')
 check(all(abs(float(r['header_minus_manifest_minutes'])-15)<1e-9 and float(r['header_minutes_before_tip'])>0 for r in exceptions),'Exception timing / pre-tip checks')
 check(len(csvrows(SRC/'NBA_Source_Inventory.csv'))==30,'Source inventory record count')
 def coder(name):
  r=csvrows(COD/name)
  check(len(r)==300 and len({v['spell_id'] for v in r})==300,'Coder row uniqueness '+name)
  return {v['spell_id']:v for v in r}
 c1,c2,reference=coder('Encoded1.csv'),coder('Encoded2.txt'),coder('development_reference.csv')
 check(c1.keys()==c2.keys()==reference.keys(),'Coder sets do not match')
 pairs=[]
 for k in c1:
  a,b,o=c1[k],c2[k],reference[k]
  check(a['initial_designation_raw']==b['initial_designation_raw']==o['initial_designation_raw'],'Coder text mismatch: '+k)
  check(a['human_class_coder_1'] in LABELS and b['human_class_coder_2'] in LABELS,'Coder label invalid: '+k)
  check(not a['human_class_coder_2'] and not b['human_class_coder_1'],'Unexpected unblinded label: '+k)
  pairs.append((a['human_class_coder_1'],b['human_class_coder_2']))
 n=len(pairs);agree=sum(a==b for a,b in pairs)
 m1,m2=Counter(a for a,b in pairs),Counter(b for a,b in pairs)
 pe=sum(m1[t]*m2[t] for t in LABELS)/(n*n)
 kappa=(agree/n-pe)/(1-pe)
 check(n==300 and agree==260 and abs(kappa-0.8348813209494325)<1e-12,'Human coder inter-rater agreement')
 if errors:
  print('FAIL ('+str(len(errors))+' checks):\n'+'\n'.join(' - '+e for e in errors));return 1
 print('PASS: 37,342 URL checks; 27,755 manifest-hash-matched PDFs across 7 archive indexes; 7,230 primary game maps; 2,054 selected PDF objects.')
 print('PASS: 7,230 boxscore IDs; 14,460 historical report links; 21 selected timestamp exceptions across 8 pre-tipoff PDFs.')
 print(f'PASS: independent coder sheets 260/300 agreement; Cohen kappa={kappa:.9f}.')
 print('NOTE: This checks archived metadata and coder worksheets, not original NBA PDF bytes, raw boxscore JSON payloads, or the independence of the coding process.')
 return 0

if __name__=='__main__':sys.exit(verify())
