import argparse, hashlib, json, math, sys
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
W=Path(__file__).resolve().parents[2];O=W/"outputs/selection50_v1"
L=[0,1,2,4,8,16]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--run",action="store_true")
 if not ap.parse_args().run:ap.error("--run required")
 if O.exists():raise RuntimeError("Refusing overwrite")
 O.mkdir(parents=True)
 rp=W/"docs/run_records/ASSORT_20260927_penalty_bars_v1_run_record.json"
 parent=json.loads(rp.read_text());inputs={str(rp.relative_to(W)):sha(rp)}
 inputs[str(Path(__file__).resolve().relative_to(W))]=sha(Path(__file__))
 for rel,h in parent["input_hashes"].items():
  assert sha(W/rel)==h;inputs[rel]=h
 rows=[]
 for year in [2014,2015,2016]:
  p=pd.read_csv(W/f"data/three_season_mechanism_v1/prepared/{year}_players.csv.gz").sort_values("athlete_id")
  A=p.ability.to_numpy();ids=p.athlete_id.to_numpy();n=len(A);k=math.floor(.5*n+.5)
  path=W/f"outputs/penalty_bars_v1/{year}_selections_and_bins.npz"
  assert sha(path)==parent["output_hashes"][str(path.relative_to(W))];inputs[str(path.relative_to(W))]=sha(path)
  with np.load(path) as z:
   assert np.array_equal(ids,z["athlete_id"])
   ew=z["ew_bins"].copy();qu=z["quantile_bins"].copy();old=z["selected"][3].copy()
  C=[]
  for rep in range(1,101):
   with np.load(W/f"outputs/three_season_mechanism_v1/{year}/pair_{rep:03d}.npz") as z:C.append(z["congestion"][1].copy())
  masks=[]
  for lam in L:
   selected=[]
   for r in range(100):
    score=A-lam*C[r];order=np.lexsort((ids,-score));mask=np.zeros(n,bool);mask[order[:k]]=True
    check=pd.DataFrame({"s":score,"id":ids}).sort_values(["s","id"],ascending=[False,True]).index[:k]
    assert set(check)==set(np.flatnonzero(mask))
    if lam==4:assert not (old[r]&~mask).any()
    selected.append(mask)
    for method,bins in [("EW",ew),("Quantile",qu)]:
     ns=np.bincount(bins[r],minlength=16);ks=np.bincount(bins[r,mask],minlength=16)
     assert ns.sum()==n and ks.sum()==k
     for bi in range(16):rows.append(dict(season=year,penalty=lam,method=method,repetition=r+1,bin=bi+1,players=int(ns[bi]),selected=int(ks[bi]),K=k,N=n))
   masks.append(selected)
   print(f"CHECKED {year}: 50%, lambda={lam}, K={k}; 100 saved assignments.",flush=True)
  np.savez_compressed(O/f"{year}_selections.npz",selected=np.array(masks),lambdas=L,athlete_id=ids)
  pd.DataFrame(rows).to_csv(O/"counts_by_repetition.csv",index=False)
 s=pd.DataFrame(rows).groupby(["season","penalty","method","bin"]).agg(players=("players","sum"),selected=("selected","sum"),mean_players=("players","mean"),occupied=("players",lambda x:int((x>0).sum()))).reset_index()
 s["rate"]=s.selected/s.players.replace(0,np.nan);s.to_csv(O/"bar_summary.csv",index=False)
 for year in [2014,2015,2016]:
  fig,axs=plt.subplots(6,2,figsize=(12,15),sharey=True)
  for row,lam in enumerate(L):
   for col,method in enumerate(["EW","Quantile"]):
    g=s.loc[(s.season==year)&(s.penalty==lam)&(s.method==method)]
    ax=axs[row,col];ax.bar(g.bin,100*g.rate,color="#3d7894");ax.set_ylim(0,100)
    ax.axhline(50,color="gray",ls=":");ax.set_title(f"{method} | lambda = {lam}");ax.set_xticks([1,4,8,12,16]);ax.set_ylabel("Selected (%)");ax.grid(axis="y",alpha=.15)
  fig.suptitle(f"{year}: 50% selection, rho = 1 | same teams across penalties",fontsize=15)
  fig.text(.5,.01,"100 saved assignments. EW edges and quantile memberships unchanged. Extreme EW bins remain sparse.\nExploratory visual comparison; no automatic downturn threshold or fitted parameter.",ha="center",fontsize=9)
  fig.tight_layout(rect=[0,.05,1,.96]);fig.savefig(O/f"{year}_sweep.png",dpi=130);plt.close(fig)
 assert all(sha(W/p)==h for p,h in inputs.items())
 record=dict(status="executed_checked",completed_utc=datetime.now(timezone.utc).isoformat(),python=sys.executable,rho=1,fraction=.5,lambdas=L,input_hashes=inputs,
 checks=["source hashes unchanged","independent ranking agrees","exact selected counts","10% lambda4 winners contained in 50% lambda4"],
 output_hashes={str(p.relative_to(W)):sha(p) for p in O.iterdir() if p.is_file()})
 (W/"docs/run_records/ASSORT_20260927_selection50_v1_run_record.json").write_text(json.dumps(record,indent=2)+"\n")
 print("COMPLETE",flush=True)
if __name__=="__main__":main()

