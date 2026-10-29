#!/usr/bin/env python3
"""Verify October release checksums, numerical headline tables and panel size."""
from pathlib import Path
import hashlib,csv,sys

ROOT=Path(__file__).resolve().parents[2]
MANIFEST=ROOT/'manifests/OCTOBER_2026_SHA256.csv'
EXPECTED={'data_intermediate/player_team_game_harmonized_cadence.csv.gz':('5483fc07465b84b20d29f54f0c49da53bef367cba712ad174111f3a7a794d8cd',18277761),
'packages/06_cadence_harmonized_identification.zip':('821b50373d0ab6f27237d05f2d1d2b32f669f2ebbcd25e7fe0cdd5cd8292b221',18614042),
'packages/01_analysis_ready_panel.zip':('a3d991bdaf41cbdba734abbd43853b495b27fbb96576743259413fcd50eb9155',28085705)}

def sha256(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

def verify():
    errors=[]
    with MANIFEST.open(newline='',encoding='utf-8') as f:
        rows=list(csv.DictReader(f))
    for item in rows:
        path=ROOT/item['relative_path']
        if not path.is_file() or path.stat().st_size!=int(item['size_bytes']) or sha256(path)!=item['sha256']:
            errors.append(f"October manifest mismatch: {item['relative_path']}")
    for relative,(hash_value,n) in EXPECTED.items():
        path=ROOT/relative
        if not path.is_file() or path.stat().st_size!=n or sha256(path)!=hash_value:
            errors.append(f"Original input missing/different: {relative}")
    import pandas as pd
    panel=ROOT/'data_intermediate/player_team_game_harmonized_cadence.csv.gz'
    if panel.exists():
        d=pd.read_csv(panel,usecols=['at_risk_for_new_onset_harm','absence_onset_harm'])
        if (len(d),int(d.at_risk_for_new_onset_harm.sum()),int(d.absence_onset_harm.sum()))!=(248778,180664,12731):
            errors.append('Unexpected panel sample counts')
    archived=ROOT/'results/october_2026/archive'
    head=ROOT/'results/october_2026/manuscript_estimates.csv'
    if head.exists():
        h=pd.read_csv(head)
        for name,row_name,expected in [('baseline_announced_tv_primary.csv','Main national-partner DDD',2.6304485901569383),('baseline_tv_harmonized_linear.csv','Linear-TV-only DDD',1.2389703651133357)]:
            x=pd.read_csv(archived/name)
            row=x.loc[x.term=='triple']
            if len(row)!=1 or abs(float(row.estimate_pp.iloc[0])-expected)>0.001:
                errors.append(f'Regression archive mismatch: {name}')
            y=h.loc[h.analysis==row_name]
            if len(y)!=1 or abs(float(y.estimate_pp.iloc[0])-expected)>0.001:
                errors.append(f'October summary mismatch: {row_name}')
    if errors:
        print('FAILED:\n'+'\n'.join(errors));return 1
    print(f'PASS: {len(rows)} October files hashed, 3 archived input hashes, panel sample counts and two headline coefficients.')
    print('Note: checksum and archived-coefficient checks are NOT a fresh full regression rerun.')
    return 0
if __name__=='__main__':sys.exit(verify())
