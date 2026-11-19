#!/usr/bin/env python3
"""Reproduce a bounded December 2025 exact-clock PDF content audit.

Requires: pandas and PyMuPDF, and the original archived `audit_2025_26_upload.zip`.
Does NOT modify any data, regressions, repository files, or archived PDFs.
"""
import argparse
import hashlib
import re
import sys
import unicodedata
import zipfile
from pathlib import Path

import fitz
import numpy as np
import pandas as pd

ABBR={
'Atlanta Hawks':'ATL','Boston Celtics':'BOS','Brooklyn Nets':'BKN','Charlotte Hornets':'CHA','Chicago Bulls':'CHI','Cleveland Cavaliers':'CLE','Dallas Mavericks':'DAL','Denver Nuggets':'DEN','Detroit Pistons':'DET','Golden State Warriors':'GSW','Houston Rockets':'HOU','Indiana Pacers':'IND','LA Clippers':'LAC','Los Angeles Lakers':'LAL','Memphis Grizzlies':'MEM','Miami Heat':'MIA','Milwaukee Bucks':'MIL','Minnesota Timberwolves':'MIN','New Orleans Pelicans':'NOP','New York Knicks':'NYK','Oklahoma City Thunder':'OKC','Orlando Magic':'ORL','Philadelphia 76ers':'PHI','Phoenix Suns':'PHX','Portland Trail Blazers':'POR','Sacramento Kings':'SAC','San Antonio Spurs':'SAS','Toronto Raptors':'TOR','Utah Jazz':'UTA','Washington Wizards':'WAS'}


def norm(s):
    s=unicodedata.normalize('NFKD',str(s).translate(str.maketrans({'Đ':'Dj','đ':'dj'})))
    s=s.encode('ascii','ignore').decode().lower()
    return re.sub('[^a-z0-9]','',s)


def line_rows(page):
    rows=[]
    for w in sorted(page.get_text('words'),key=lambda w:(round(w[1],1),w[0])):
        x,y,_,_,v,*_=w
        if not (75<=y<=530):continue
        if rows and abs(y-rows[-1][0])<1:rows[-1][1].append((x,v))
        else:rows.append([y,[(x,v)]])
    result=[]
    for y,words in rows:
        groups={k:[] for k in ('date','time','matchup','team','name','status','reason')}
        for x,v in words:
            g=('date' if x<100 else 'time' if x<194 else 'matchup' if x<265 else 'team' if x<425 else 'name' if x<575 else 'status' if x<665 else 'reason')
            groups[g].append(v)
        result.append((y,{k:' '.join(v) for k,v in groups.items()}))
    return result


def parse_pdf(data,filename):
    doc=fitz.open(stream=data,filetype='pdf');rows=[];match=None;team=None
    title=doc[0].get_text().splitlines()[0]
    if not title.startswith('Injury Report:'):raise AssertionError(f'Invalid PDF heading {filename}: {title}')
    for pi,page in enumerate(doc):
        lines=line_rows(page)
        names=[y for y,p in lines if p['name'] and p['name'] not in ('Name','Player Name')]
        for y,p in lines:
            if p['matchup'] and re.fullmatch(r'[A-Z]{2,3}@[A-Z]{2,3}',p['matchup']):
                match=p['matchup'];team=None
            if p['team']:team=p['team']
            if not p['name'] and p['reason'] and y<90 and rows and rows[-1]['page']==pi-1 and (not names or names[0]-y>12):
                rows[-1]['reason']+=' '+p['reason']
            if p['name'] and p['name'] not in ('Name','Player Name') and not p['name'].startswith('Page'):
                reason=' '.join(q['reason'] for yy,q in lines if q['reason'] and abs(yy-y)<=10.5)
                rows.append({'file':filename,'page':pi,'matchup':match,'team':team,'name':p['name'],'status':p['status'],'reason':reason})
    return rows,title


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--pdf-zip',required=True,help='Path to the original audit_2025_26_upload.zip (not added to Git)')
    ap.add_argument('--repo',default=str(Path(__file__).resolve().parents[2]))
    args=ap.parse_args();repo=Path(args.repo)
    cand=pd.read_csv(repo/'results/october_2026/timestamp_audit/exact_clock/21_game_candidates.csv')
    assert len(cand)==cand.game_id.nunique()==21
    pairs=pd.concat([cand[['original_selected_filename','original_selected_sha256']].set_axis(['name','sha'],axis=1),cand[['candidate_earlier_filename','candidate_earlier_sha256']].set_axis(['name','sha'],axis=1)]).drop_duplicates()
    assert len(pairs)==16 and len(set(cand.original_selected_sha256))==len(set(cand.candidate_earlier_sha256))==8
    allrows=[];headings={}
    with zipfile.ZipFile(args.pdf_zip) as z:
        for name,sha in pairs.itertuples(index=False):
            path='audit_2025_26/pdf/'+name
            data=z.read(path)
            actual=hashlib.sha256(data).hexdigest()
            assert actual==sha,f'PDF HASH MISMATCH: {name}: {actual}'
            rows,title=parse_pdf(data,name)
            headings[name]=title;allrows+=rows
    df=pd.DataFrame(allrows)
    # Independently check the proposed earlier snapshot is the latest archived
    # header-issued report eligible at the recorded nominal cutoff, considering
    # both original and targeted 2025-26 PDF inventories.
    inv=pd.read_csv(repo/'provenance/historical_sources/injury_report_inventory.csv.gz',low_memory=False)
    inv=inv[(inv.season=='2025-26') & (inv.pdf_present==True) & inv.hash_status.eq('match')].copy()
    inv['header_dt']=pd.to_datetime(inv.pdf_header_timestamp_utc,utc=True,errors='raise')
    for r in cand.itertuples(index=False):
        cutoff=pd.Timestamp(r.cutoff_utc)
        elig=inv.loc[inv.header_dt<=cutoff]
        assert not elig.empty
        latest=elig.header_dt.max()
        assert latest==pd.Timestamp(r.candidate_earlier_header_utc),(r.game_id,latest)
        assert r.candidate_earlier_sha256 in elig.loc[elig.header_dt.eq(latest),'computed_sha256'].values
    # Exact PDF report title times are checked against the metadata inventories.
    for r in cand.itertuples(index=False):
        for name,timestamp in ((r.original_selected_filename,r.original_selected_header_utc),(r.candidate_earlier_filename,r.candidate_earlier_header_utc)):
            dt=pd.Timestamp(timestamp).tz_convert('America/New_York')
            expected=dt.strftime('Injury Report: %m/%d/%y %I:%M %p')
            assert headings[name]==expected,(name,headings[name],expected)
        cutoff=pd.Timestamp(r.cutoff_utc)
        assert pd.Timestamp(r.candidate_earlier_header_utc)<=cutoff<pd.Timestamp(r.original_selected_header_utc)
        assert (cutoff-pd.Timestamp(r.candidate_earlier_header_utc)).total_seconds()/60==45
        assert (pd.Timestamp(r.original_selected_header_utc)-cutoff).total_seconds()/60==15
    panel=pd.read_csv(repo/'data_intermediate/player_team_game_harmonized_cadence.csv.gz',usecols=['game_id','team','nba_player_name','designation_status','designation_reason','player_team_game_id','from_boxscore_roster','played_bool','absence_now_harm','at_risk_for_new_onset_harm','absence_onset_harm'],low_memory=False)
    orig=pd.read_csv(repo/'data_final/player_game_panel_analysis_ready.csv.gz',usecols=['player_team_game_id','not_playing_reason','boxscore_player_status'],low_memory=False)
    affected=panel[panel.game_id.isin(cand.game_id)].copy()
    assert len(affected)==733
    assert (int(affected.at_risk_for_new_onset_harm.sum()),int(affected.absence_onset_harm.sum()))==(514,35)
    corrected={};diffs=[];n_matched=0
    for r in cand.itertuples(index=False):
        away,home=r.game_id.split('|')[-1].split('@'); match=ABBR[away]+'@'+ABBR[home]
        old=df[(df.file==r.original_selected_filename)&df.matchup.eq(match)].copy().set_index(['team','name'])
        new=df[(df.file==r.candidate_earlier_filename)&df.matchup.eq(match)].copy().set_index(['team','name'])
        assert old.index.is_unique and new.index.is_unique
        assert set(old.index)==set(new.index),f'Listed names changed for {r.game_id}; full rebuild required'
        game=affected[affected.game_id.eq(r.game_id)].copy()
        for (team,pdfname),v in old.iterrows():
            full=pdfname.split(',',1)
            target=norm(full[1].strip()+' '+full[0].strip()) if len(full)==2 else norm(pdfname)
            matched=game[game.team.eq(team)&game.nba_player_name.map(norm).eq(target)]
            assert len(matched)==1,(r.game_id,team,pdfname,'panel match count',len(matched))
            p=matched.iloc[0];n_matched+=1
            assert v.status==p.designation_status,('Original status discrepancy',r.game_id,team,pdfname)
            assert ' '.join(str(v.reason).split())==' '.join(str(p.designation_reason).split()),('Original reason discrepancy',r.game_id,team,pdfname)
            q=new.loc[(team,pdfname)]
            corrected[p.player_team_game_id]=q.status
            if (q.status,q.reason)!=(v.status,v.reason):
                diffs.append({'game_id':r.game_id,'team':team,'player':p.nba_player_name,'earlier_status':q.status,'later_status':v.status,'earlier_reason':q.reason,'later_reason':v.reason,'status_changed':q.status!=v.status,'reason_changed':q.reason!=v.reason})
    assert n_matched==241 and len(diffs)==15 and sum(x['status_changed'] for x in diffs)==15 and sum(x['reason_changed'] for x in diffs)==1
    changed=affected.merge(orig,on='player_team_game_id',how='left',validate='one_to_one')
    assert len(changed)==733 and changed.boxscore_player_status.notna().all()
    played=changed.played_bool.astype(bool)
    coach=changed.not_playing_reason.fillna('').str.contains('COACH',case=False,na=False)
    coach_dnp=(~played)&(coach | (changed.boxscore_player_status.fillna('').eq('ACTIVE') & changed.not_playing_reason.fillna('').eq('')))
    absbox=changed.not_playing_reason.fillna('').str.contains('INJURY|REST|PERSONAL|GLEAGUE|HEALTH_AND_SAFETY|SUSPENSION|NOT_WITH_TEAM|TRADE|INELIGIBLE|RECONDITIONING|CONCUSSION|SELF_ISOLATING|ILLNESS',case=False,regex=True,na=False)
    def absence(status):
        return (~played)&(status.fillna('').str.casefold().eq('out') | absbox | (changed.boxscore_player_status.fillna('').eq('INACTIVE') & ~coach_dnp) | (~changed.from_boxscore_roster.astype(bool)&status.fillna('').str.casefold().eq('out')))
    original=absence(changed.designation_status)
    assert (original==changed.absence_now_harm).all(),'Original rule fails to reproduce archived panel'
    corrected_status=changed.designation_status.copy()
    corrected_status.loc[changed.player_team_game_id.isin(corrected)]=changed.loc[changed.player_team_game_id.isin(corrected),'player_team_game_id'].map(corrected)
    new=absence(corrected_status)
    assert (original==new).all(),'Corrected statuses change absence flags; full pipeline needed'
    print(f'PASS: 16 exact archived PDF bytes match SHA-256; PDF headers and cutoff times match.')
    print(f'PASS: 21 games, 241 listed players, 15 status changes (9 games), 1 reason change.')
    print('PASS: 733/733 original absence flags reproduced with archived exact rule; corrected status causes 0 absence changes.')
    print('PASS: 514 onset-risk observations, 35 new absence onsets, all unchanged under status substitutions.')
    print('LIMIT: This is bounded raw-PDF-status substitution, not a complete historical raw-to-panel rebuild.')
    return 0

if __name__=='__main__':
    try:sys.exit(main())
    except Exception as ex:
        print('FAIL:',type(ex).__name__,str(ex),file=sys.stderr)
        sys.exit(1)
