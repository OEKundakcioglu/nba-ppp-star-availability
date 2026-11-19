import numpy as np,pandas as pd,scipy.linalg as la
from scipy.sparse import csr_matrix
from scipy.stats import norm,chi2
from statsmodels.api import OLS
from statsmodels.stats.sandwich_covariance import cov_cluster_2groups
from pathlib import Path
from time import perf_counter
W=Path(__file__).resolve().parents[2]; O=W/'results/october_2026/recomputed'; O.mkdir(parents=True,exist_ok=True)
D=pd.read_csv(W/'data_intermediate/player_team_game_harmonized_cadence.csv.gz',low_memory=False)
L=pd.read_csv(W/'data_final/player_game_panel_analysis_ready.csv.gz',usecols=['player_team_game_id','star_prior_all_star_3yr','current_season_all_star_post_game'],low_memory=False)
L['star_allstar_only']=L.star_prior_all_star_3yr|L.current_season_all_star_post_game
D=D.merge(L[['player_team_game_id','star_allstar_only']],on='player_team_game_id',how='left',validate='one_to_one')
D=D.sort_values(['nba_player_id','season','game_date_et','team_game_number']).copy()
D['star_allstar_only']=D.groupby(['nba_player_id','season']).star_allstar_only.ffill().bfill().fillna(D.star_PPP_it).astype(float)
D['teamseason']=D.team+'|'+D.season
for c in ['star_PPP_it','postPPP','announced_tv_primary','is_home','back_to_back','three_games_in_four_days','four_games_in_six_days','opponent_bottom_quartile_pre','opponent_back_to_back','cup_game','absence_now_harm','absence_onset_harm','at_risk_for_new_onset_harm','report_outcome_observed']:
 D[c]=D[c].astype(float)
for out,col,scale in [('elo_100','signed_elo_advantage',100),('travel_1000','travel_km_since_previous_game',1000),('travel_disadv_1000','travel_disadvantage_km',1000),('minutes10_100','minutes_sum_prior_10_roster_games_harm',100),('games_before_10','games_played_before_game_harm',10),('dist65_10','dist_to_65_before_game_harm',10)]:D[out]=D[col]/scale
CTRL=['is_home','back_to_back','three_games_in_four_days','four_games_in_six_days','travel_1000','absolute_timezone_shift_hours','road_trip_game_number','elo_100','opponent_bottom_quartile_pre','opponent_back_to_back','rest_advantage_days','travel_disadv_1000','cup_game','minutes10_100','games_before_10','dist65_10']
print('full',len(D),'risk',int(D.at_risk_for_new_onset_harm.sum()),flush=True)
# Censor safe one-game spells from consecutive roster observations; exclude when next is missing.
D=D.sort_values(['season','team','nba_player_id','team_game_number','game_id']).copy()
G=D.groupby(['season','team','nba_player_id'],sort=False)
D['next_game']=G.team_game_number.shift(-1);D['next_absent']=G.absence_now_harm.shift(-1);D['next_obs']=G.report_outcome_observed.shift(-1)
D['prev_game']=G.team_game_number.shift(1);D['prev_absent']=G.absence_now_harm.shift(1);D['prev_obs']=G.report_outcome_observed.shift(1)
D['can_see_next']=(D.next_game==D.team_game_number+1)&(D.next_obs==1)
D['onegame']=((D.absence_onset_harm==1)&D.can_see_next&(D.next_absent==0)).astype(float)
D['longer']=((D.absence_onset_harm==1)&D.can_see_next&(D.next_absent==1)).astype(float)
D['repair_risk']=((D.prev_game==D.team_game_number-1)&(D.prev_absent==1)&(D.prev_obs==1)&(D.report_outcome_observed==1)).astype(float)
D['repair']=D.repair_risk*(1-D.absence_now_harm)
R=D[D.at_risk_for_new_onset_harm==1].copy()

def fit(df,y,terms,label,groups=['nba_player_id','teamseason']):
 t0=perf_counter(); cols=list(dict.fromkeys([y,'nba_player_id','game_id']+groups+terms))
 d=df[cols].replace([np.inf,-np.inf],np.nan).dropna().copy()
 A=d[[y]+terms].to_numpy(float);ops=[]
 for g in groups:
  codes,vals=pd.factorize(d[g],sort=False); mat=csr_matrix((np.ones(len(codes)),(np.arange(len(codes)),codes)),shape=(len(codes),len(vals))); ct=np.asarray(mat.sum(axis=0)).ravel();ops.append((mat,ct))
 converged=False
 for it in range(240):
  if it%5==0: old=A.copy()
  for mat,ct in ops:A-=mat@((mat.T@A)/ct[:,None])
  if it%5==0 and np.max(np.abs(A-old))<1e-8:converged=True;break
 X=A[:,1:];good=(X*X).sum(0)>1e-12;X=X[:,good];names=[v for v,k in zip(terms,good) if k]
 Q,T,piv=la.qr(X,mode='economic',pivoting=True,check_finite=False); k=int(np.sum(np.abs(np.diag(T))>1e-9*abs(T[0,0])));take=np.sort(piv[:k]);X=X[:,take];names=[names[i] for i in take]
 model=OLS(A[:,0],X).fit();V,_,_=cov_cluster_2groups(model,pd.factorize(d.nba_player_id)[0],pd.factorize(d.game_id)[0],use_correction=True)
 b=model.params;se=np.sqrt(np.maximum(np.diag(V),0));rows=pd.DataFrame({'term':names,'coef':b,'se':se,'estimate_pp':100*b,'se_pp':100*se,'low_pp':100*(b-1.96*se),'high_pp':100*(b+1.96*se),'p':2*norm.sf(np.abs(b/se))});rows['n']=len(d);rows['iterations']=it+1;rows['converged']=converged;rows['model']=label
 rows.to_csv(O/(label+'.csv'),index=False)
 focus=rows[rows.term.isin(['triple','star_tv_2020-21','star_tv_2021-22'])]
 print(label,len(d),it+1,converged,round(perf_counter()-t0,1),focus[['term','estimate_pp','p']].to_dict('records'),flush=True)
 return rows,V

def triple(df,tv,star,label,home=False,out='absence_onset_harm'):
 d=df.copy();d['tv']=d[tv];d['star']=d[star]
 d['starpost']=d.star*d.postPPP;d['startv']=d.star*d.tv;d['posttv']=d.postPPP*d.tv;d['triple']=d.star*d.postPPP*d.tv
 ctr=CTRL if not home else [x for x in CTRL if x not in ['is_home','opponent_back_to_back','rest_advantage_days','travel_disadv_1000','elo_100','opponent_bottom_quartile_pre','cup_game']]
 gr=['nba_player_id','teamseason'] if not home else ['nba_player_id','teamseason','game_id']
 return fit(d,out,['star','tv','starpost','startv','posttv','triple']+ctr,label,gr)


from scipy.stats import chi2
# Assign nearest TV anchor within +/-3 team games, dropping equal-distance ties.
team=D[['season','team','team_game_number','tv_harmonized_linear','announced_tv_primary']].drop_duplicates(['season','team','team_game_number']).copy()
RES=[]
for tv in ['announced_tv_primary']:
 tt=team.copy();tt['event_time']=np.nan
 for key,g in tt.groupby(['season','team'],sort=False):
  anchors=g.loc[g[tv]==1,'team_game_number'].to_numpy(dtype=int)
  if not len(anchors):continue
  idx=g.index.to_numpy();nums=g.team_game_number.to_numpy(dtype=int)
  distances=np.abs(nums[:,None]-anchors[None,:]); min_dist=distances.min(axis=1)
  tied=((distances==min_dist[:,None]).sum(axis=1)>1)
  best=anchors[distances.argmin(axis=1)];rel=nums-best
  tt.loc[idx,'event_time']=np.where((min_dist<=3)&(~tied),rel,np.nan)
 d=D.merge(tt[['season','team','team_game_number','event_time']],on=['season','team','team_game_number'],how='left',validate='many_to_one')
 d=d[d.event_time.notna()].copy();d['evt']=d.event_time.astype(int)
 # baseline at event zero, all other event time coefficients relative to it, with complete lower order interactions.
 def event_fit(input,outcome,label,age=False):
  t=input.copy();t['star']=t.star_PPP_it;t['starpost']=t.star*t.postPPP
  terms=['star','starpost']
  for k in [-3,-2,-1,1,2,3]:
   name=('m'+str(-k)) if k<0 else ('p'+str(k));z=(t.evt==k).astype(float)
   for col,arr in [('evt_'+name,z),('star_evt_'+name,t.star*z),('post_evt_'+name,t.postPPP*z),('triple_evt_'+name,t.star*t.postPPP*z)]:t[col]=arr;terms.append(col)
  ctr=CTRL
  if age:
   t['age2_3']=t.prev_age.between(2,3).astype(float)
   t['age4_6']=t.prev_age.between(4,6).astype(float)
   t['age7_10']=t.prev_age.between(7,10).astype(float)
   t['age11plus']=(t.prev_age>=11).astype(float)
   ctr=CTRL+['age2_3','age4_6','age7_10','age11plus']
  T,V=fit(t,outcome,terms+ctr,label)
  ids=[int(T.index[T.term==('triple_evt_'+( ('m'+str(-k)) if k<0 else ('p'+str(k))))][0]) for k in [-3,-2,-1,1,2,3]]
  beta=T.coef.to_numpy()[ids];vv=V[np.ix_(ids,ids)];stat=float(beta@np.linalg.pinv(vv)@beta);p=float(chi2.sf(stat,6))
  RES.append({'tv':tv,'outcome':outcome,'n':len(t),'wald_chi2_6':stat,'p':p})
  print('EVENT WINDOW TEST',tv,outcome,len(t),stat,p,flush=True)
 event_fit(d[d.at_risk_for_new_onset_harm==1],'absence_onset_harm','evt_onset_'+tv)
 event_fit(d[d.report_outcome_observed==1],'absence_now_harm','evt_prevalence_'+tv)
 # For repair, include only spells with observed onsets, excluding left-censored continuation.
 d=d.sort_values(['season','team','nba_player_id','team_game_number']).copy()
 full=D.sort_values(['season','team','nba_player_id','team_game_number']).copy()
 gr=full.groupby(['season','team','nba_player_id'],sort=False)
 full['run_new']=((full.absence_now_harm==0)|(full.prev_game!=full.team_game_number-1)|(full.prev_absent!=1)|(full.prev_obs!=1)).astype(int)
 full['run_index']=gr.run_new.cumsum()
 full['age']=full.groupby(['season','team','nba_player_id','run_index'],sort=False).cumcount()+1
 full['age']=np.where(full.absence_now_harm==1,full.age,np.nan)
 full['known']=full.groupby(['season','team','nba_player_id','run_index'],sort=False).absence_onset_harm.transform('max')
 gg=full.groupby(['season','team','nba_player_id'],sort=False)
 full['prev_age']=gg.age.shift(1);full['prev_known']=gg.known.shift(1)
 d=d.merge(full[['player_team_game_id','prev_age','prev_known']],on='player_team_game_id',how='left',validate='one_to_one')
 event_fit(d[(d.repair_risk==1)&(d.prev_known==1)&d.prev_age.notna()],'repair','evt_repair_'+tv,age=True)
pd.DataFrame(RES).to_csv(O/'event_window_joint_tests_national_partner.csv',index=False)
print('COMPLETE',flush=True)
