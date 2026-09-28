import json,hashlib,math,sys,argparse
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
W=Path(__file__).resolve().parents[2];O=W/"outputs/rho_scarcity_v1"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--run",action="store_true")
 if not ap.parse_args().run:ap.error("--run required")
 if O.exists():raise RuntimeError("Refusing overwrite")
 O.mkdir(parents=True);inputs={};rows=[];identity=[]
 pp=W/"docs/run_records/ASSORT_20260927_rho005_v1_run_record.json"
 parent=json.loads(pp.read_text());inputs[str(pp)]=sha(pp)
 for rel,digest in parent["output_hashes"].items():
  assert sha(W/rel)==digest;inputs[str(W/rel)]=digest
 priorpath=W/"outputs/scarcity_bars_v1/bar_summary.csv"
 prior=pd.read_csv(priorpath);inputs[str(priorpath)]=sha(priorpath)
 inputs[str(Path(__file__))]=sha(Path(__file__))
 for year in [2014,2015,2016]:
  pth=W/f"data/three_season_mechanism_v1/prepared/{year}_players.csv.gz"
  assert sha(pth)==parent["input_hashes"][str(pth)];inputs[str(pth)]=sha(pth)
  p=pd.read_csv(pth).sort_values("athlete_id");A=p.ability.to_numpy();ids=p.athlete_id.to_numpy();n=len(A)
  with np.load(W/f"outputs/rho005_v1/{year}_paired_assignments.npz") as z:
   assert np.array_equal(ids,z["athlete_id"])
   C=z["congestion"].copy();ew=z["ew_bins"].copy();qu=z["quantile_bins"].copy();old=z["selected"].copy()
  allrates=[]
  for q in [.5,.01]:
   k=math.floor(q*n+.5);masks=[]
   for rep in range(100):
    pair=[]
    for ri,rho in enumerate([1.,.05]):
     score=A-4*C[rep,ri];order=np.lexsort((ids,-score));mask=np.zeros(n,bool);mask[order[:k]]=True
     check=pd.DataFrame({"s":score,"id":ids}).sort_values(["s","id"],ascending=[False,True]).index[:k]
     assert set(check)==set(np.flatnonzero(mask));pair.append(mask)
     if q==.5:assert np.array_equal(mask,old[rep,ri])
     else:assert not (mask&~old[rep,ri]).any()
     for label,bins in [("EW",ew),("Quantile",qu)]:
      ns=np.bincount(bins[rep,ri],minlength=16);ks=np.bincount(bins[rep,ri,mask],minlength=16)
      assert ns.sum()==n and ks.sum()==k
      for bi in range(16):rows.append(dict(season=year,fraction=q,achieved=k/n,rho=rho,repetition=rep+1,method=label,bin=bi+1,players=int(ns[bi]),selected=int(ks[bi])))
    masks.append(pair)
    lost=int(np.sum(pair[0]&~pair[1]))
    identity.append(dict(season=year,fraction=q,repetition=rep+1,K=k,changed=lost,share_changed=lost/k))
   allrates.append(masks)
   print(f"CHECKED {year}: {100*q:g}% selection, K={k}, both rho settings, 100 paired repetitions.",flush=True)
  np.savez_compressed(O/f"{year}_selected.npz",selected=np.array(allrates),fractions=[.5,.01],rhos=[1,.05],athlete_id=ids)
  pd.DataFrame(rows).to_csv(O/"counts_by_repetition.csv",index=False)
 s=pd.DataFrame(rows).groupby(["season","fraction","achieved","rho","method","bin"]).agg(players=("players","sum"),selected=("selected","sum"),mean_players=("players","mean"),occupied=("players",lambda x:int((x>0).sum()))).reset_index()
 s["rate"]=s.selected/s.players.replace(0,np.nan);s["relative_rate"]=s.rate/s.achieved
 for year in [2014,2015,2016]:
  for method in ["EW","Quantile"]:
   a=s.loc[(s.season==year)&(s.fraction==.01)&(s.rho==1)&(s.method==method)].sort_values("bin")
   old=prior.loc[(prior.season==year)&(prior.fraction==.01)&(prior.method==method)].sort_values("bin")
   np.testing.assert_allclose(a.rate,old.pooled_rate,atol=1e-12)
 s.to_csv(O/"bar_summary.csv",index=False)
 it=pd.DataFrame(identity);it.to_csv(O/"identity_changes.csv",index=False)
 it.groupby(["season","fraction"]).agg(K=("K","first"),mean_changed=("changed","mean"),mean_share_changed=("share_changed","mean")).to_csv(O/"identity_summary.csv")
 for year in [2014,2015,2016]:
  for view in ["absolute","relative"]:
   fig,axs=plt.subplots(4,2,figsize=(12,11))
   for row,(q,rho) in enumerate([(.5,1),(.5,.05),(.01,1),(.01,.05)]):
    for col,method in enumerate(["EW","Quantile"]):
     g=s.loc[(s.season==year)&(s.fraction==q)&(s.rho==rho)&(s.method==method)].sort_values("bin")
     ax=axs[row,col];ax.bar(g.bin,100*g.rate if view=="absolute" else g.relative_rate,color="#a23e4a" if rho==1 else "#277c83")
     for bi,nobs in zip(g.bin,g.players):
      if nobs==0:ax.text(bi,.03 if view=="relative" else .5,"×",ha="center",color="gray")
     ax.axhline(100*g.achieved.iloc[0] if view=="absolute" else 1,color="gray",ls=":")
     ax.set_ylim(0,100 if view=="absolute" else 4)
     ax.set_title(f"{method} | {100*q:g}% selected | rho = {rho:g}")
     ax.set_ylabel("Selected (%)" if view=="absolute" else "Bin rate / overall rate")
     ax.set_xticks([1,4,8,12,16]);ax.grid(axis="y",alpha=.2)
     if row==3:ax.set_xlabel("Peer-quality bin (low to high)")
   fig.suptitle(f"{year}: does scarcity make rho matter less? | lambda = 4\n"+("Actual rates: same 0–100% scale" if view=="absolute" else "Relative rates: 1 equals the overall selection rate"),fontsize=15)
   fig.text(.5,.013,"Same 100 paired assignments reused at both selection fractions. EW edges shared; quantile bins are relative ranks.\n× = no players, not zero success. Extreme EW bins are sparse. Low rho narrows the range of environments.\nThe low-rho 2015 bin-2 absolute outlier at 50% represents one player-assignment observation.",ha="center",fontsize=9)
   fig.tight_layout(rect=[0,.075,1,.945]);fig.savefig(O/f"{year}_{view}.png",dpi=140);plt.close(fig)
 assert all(sha(Path(p))==h for p,h in inputs.items())
 record=dict(status="executed_checked",python=sys.executable,completed_utc=datetime.now(timezone.utc).isoformat(),input_hashes=inputs,
 checks=["source hashes unchanged","all 50% masks reproduced","rho1 1% bars reproduced","nested winner sets","independent ranking agrees","all counts conserved"],
 output_hashes={str(p.relative_to(W)):sha(p) for p in O.iterdir() if p.is_file()})
 (W/"docs/run_records/ASSORT_20260927_rho_scarcity_v1_run_record.json").write_text(json.dumps(record,indent=2))
 print("COMPLETE",flush=True)
if __name__=="__main__":main()

