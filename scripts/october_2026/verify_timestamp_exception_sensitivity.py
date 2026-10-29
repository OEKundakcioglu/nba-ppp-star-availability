#!/usr/bin/env python3
"""Fast integrity and count check; does not refit regressions."""
from pathlib import Path
import csv,gzip,hashlib,sys
ROOT=Path(__file__).resolve().parents[2]
MANIFEST=ROOT/'manifests/TIMESTAMP_EXCEPTION_SENSITIVITY_SHA256.csv'
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()
def main():
 with MANIFEST.open(newline='',encoding='utf-8') as f: manifest=list(csv.DictReader(f))
 for entry in manifest:
  p=ROOT/entry['relative_path']
  if not p.is_file() or p.stat().st_size!=int(entry['size_bytes']) or digest(p)!=entry['sha256']:
   raise SystemExit('HASH MISMATCH: '+str(p))
 with (ROOT/'provenance/historical_sources/selected_report_timestamp_exceptions.csv').open(newline='',encoding='utf-8') as f:
  src=list(csv.DictReader(f))
 with (ROOT/'results/october_2026/timestamp_audit/selected_report_clock_audit.csv').open(newline='',encoding='utf-8') as f:
  rows=list(csv.DictReader(f))
 assert len(src)==len(rows)==21 and len({r['game_id'] for r in rows})==21
 assert len({r['pdf_sha256'] for r in rows})==8
 assert {r['game_id'] for r in src}=={r['game_id'] for r in rows}
 assert sum(int(float(r['header_lead_minutes'])<30) for r in rows)==2
 assert all(float(r['header_lead_minutes'])>0 and float(r['header_minus_manifest_minutes'])==15 for r in rows)
 with (ROOT/'results/october_2026/timestamp_audit/model_sensitivity.csv').open(newline='',encoding='utf-8') as f:
  estimates=list(csv.DictReader(f))
 assert len(estimates)==4
 for tv,original,excluded in [('announced_tv_primary',2.6304485901569383,2.6295050907599196),('tv_harmonized_linear',1.2389703651133357,1.253769704464706)]:
  for scenario,n,expected in [('full',180530,original),('exclude_21_games',180016,excluded)]:
   subset=[r for r in estimates if r['tv_definition']==tv and r['scenario']==scenario]
   assert len(subset)==1 and int(subset[0]['n'])==n and abs(float(subset[0]['estimate_pp'])-expected)<0.001
 print('PASS: %d audit files hashed, 21 report selections, 8 PDFs, 2 <30m lead, 4 archived model comparisons.'%len(manifest))
 print('Note: this is metadata and archived-result verification, not alternative report re-selection.')
if __name__=='__main__':main()
