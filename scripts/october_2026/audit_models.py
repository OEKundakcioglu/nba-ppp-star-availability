"""Identification diagnostics using the archived harmonized panel, no causal claims."""
import os
os.environ['OPENBLAS_NUM_THREADS']='2';os.environ['OMP_NUM_THREADS']='2';os.environ['MKL_NUM_THREADS']='2'
from time import perf_counter
from pathlib import Path
import numpy as np, pandas as pd
from scipy.sparse import csr_matrix
import scipy.linalg as la
from scipy.stats import norm
from statsmodels.api import OLS
from statsmodels.stats.sandwich_covariance import cov_cluster_2groups
DIR=Path(__file__).resolve().parents[2]/'results/october_2026/recomputed/audit';DIR.mkdir(parents=True,exist_ok=True)
P=Path(os.environ.get('NBA_AUDIT_PANEL', str(Path(__file__).resolve().parents[2]/'data_intermediate'/'player_team_game_harmonized_cadence.csv.gz')))
D=pd.read_csv(P,low_memory=False)
D['teamseason']=D.team+'|'+D.season
for out,col,scale in [('elo_100','signed_elo_advantage',100),('travel_1000','travel_km_since_previous_game',1000),('travel_disadv_1000','travel_disadvantage_km',1000),('minutes10_100','minutes_sum_prior_10_roster_games_harm',100),('games_before_10','games_played_before_game_harm',10),('dist65_10','dist_to_65_before_game_harm',10)]: D[out]=D[col]/scale
CTRL=['is_home','back_to_back','three_games_in_four_days','four_games_in_six_days','travel_1000','absolute_timezone_shift_hours','road_trip_game_number','elo_100','opponent_bottom_quartile_pre','opponent_back_to_back','rest_advantage_days','travel_disadv_1000','cup_game','minutes10_100','games_before_10','dist65_10']
MED=['minutes10_100','games_before_10','dist65_10']
PRE=['is_home','back_to_back','three_games_in_four_days','four_games_in_six_days','travel_1000','absolute_timezone_shift_hours','road_trip_game_number','opponent_bottom_quartile_pre','opponent_back_to_back','rest_advantage_days','travel_disadv_1000','cup_game']
# Lower-order terms: star, tv, star-post, star-tv, post-tv; post is absorbed by team-season.
def fit(d,y,ctrl,tv='announced_tv_primary',lbl='main',subset=None):
 t=perf_counter();d=d.copy();d['star']=d.star_PPP_it.astype(float);d['tv']=d[tv].astype(float);d['post']=d.postPPP.astype(float)
 d['starpost']=d.star*d.post;d['startv']=d.star*d.tv;d['posttv']=d.post*d.tv;d['triple']=d.starpost*d.tv
 terms=['star','tv','starpost','startv','posttv','triple']+ctrl
 d=d[list(dict.fromkeys([y,'nba_player_id','game_id','teamseason']+terms))].replace([np.inf,-np.inf],np.nan).dropna()
 A=d[[y]+terms].to_numpy(float)
 ops=[]
 for g in ['nba_player_id','teamseason']:
  codes,uni=pd.factorize(d[g],sort=False)
  mat=csr_matrix((np.ones(len(codes)),(np.arange(len(codes)),codes)),shape=(len(codes),len(uni)))
  ct=np.asarray(mat.sum(axis=0)).ravel();ops.append((mat,ct))
 converged=False
 for it in range(240):
  if it%5==0: old=A.copy()
  for mat,ct in ops: A-=mat@((mat.T@A)/ct[:,None])
  if it%5==0 and np.max(np.abs(A-old))<1e-8:converged=True;break
 X=A[:,1:];good=(X*X).sum(0)>1e-12;X=X[:,good];names=[v for v,k in zip(terms,good) if k]
 Q,T,piv=la.qr(X,mode='economic',pivoting=True,check_finite=False)
 k=int(np.sum(np.abs(np.diag(T))>1e-9*abs(T[0,0])))
 take=np.sort(piv[:k]);X=X[:,take];names=[names[i] for i in take]
 model=OLS(A[:,0],X).fit()
 V,_,_=cov_cluster_2groups(model,pd.factorize(d.nba_player_id)[0],pd.factorize(d.game_id)[0],use_correction=True)
 b=model.params;se=np.sqrt(np.maximum(np.diag(V),0))
 j=names.index('triple')
 result={'name':lbl,'N':len(d),'coef_pp':100*b[j],'se_pp':100*se[j],'CI_low_pp':100*(b[j]-1.96*se[j]),'CI_high_pp':100*(b[j]+1.96*se[j]),'p':2*norm.sf(abs(b[j]/se[j])),'iterations':it+1,'converged':converged,'seconds':round(perf_counter()-t,1),'dropped_terms':';'.join(set(terms)-set(names))}
 print(result,flush=True)
 return result

R=D[D.at_risk_for_new_onset_harm].copy()
results=[]
results.append(fit(R,'absence_onset_harm',CTRL,lbl='reported_model_partner'))
results.append(fit(R,'absence_onset_harm',[x for x in CTRL if x not in MED],lbl='remove_outcome_affected_workload'))
results.append(fit(R,'absence_onset_harm',PRE,lbl='schedule_and_pregame_only_no_elo'))
results.append(fit(R,'absence_onset_harm',[],lbl='fixed_effects_only'))
results.append(fit(R,'absence_onset_harm',[x for x in CTRL if x not in MED],tv='tv_harmonized_linear',lbl='remove_workload_linear_tv'))
# Treat all observed games, outcome prevalence: different estimand and risk composition
P=D[D.report_outcome_observed].copy()
results.append(fit(P,'absence_now_harm',[x for x in CTRL if x not in MED],lbl='absent_prevalence_partner'))
pd.DataFrame(results).to_csv(DIR/'coefficient_sensitivity.csv',index=False)
