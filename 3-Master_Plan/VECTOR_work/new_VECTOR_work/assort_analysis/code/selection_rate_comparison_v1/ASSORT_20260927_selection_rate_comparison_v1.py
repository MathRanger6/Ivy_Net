#!/usr/bin/env python3
"""Authorized 2.7% vs 10% comparison on identical saved teams/scores.
No assignment, parameter fitting, data rebuilding or new randomness.
"""
import argparse, hashlib, json, math, time
from pathlib import Path
from datetime import datetime, timezone
import numpy as np
import pandas as pd
HERE=Path(__file__).resolve(); WORK=HERE.parents[2]
SOURCE=WORK/"outputs/three_season_mechanism_v1"
DATA=WORK/"data/three_season_mechanism_v1/prepared"
OUT=WORK/"outputs/selection_rate_comparison_v1"
RECORD=WORK/"docs/run_records/ASSORT_20260927_selection_rate_comparison_v1_run_record.json"
PARENT=WORK/"docs/run_records/ASSORT_20260927_three_season_mechanism_v1_run_record.json"
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(2**20),b""):h.update(b)
 return h.hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,allow_nan=False)+"\n")
def main():
 a=argparse.ArgumentParser();a.add_argument("--run",action="store_true")
 if not a.parse_args().run:a.error("--run required")
 if OUT.exists() or RECORD.exists():raise RuntimeError("Refusing overwrite")
 OUT.mkdir(parents=True)
 parent=json.loads(PARENT.read_text())
 inputs={str(PARENT.relative_to(WORK)):sha(PARENT),str(HERE.relative_to(WORK)):sha(HERE)}
 for path,h in parent["output_hashes"].items():
  assert sha(WORK/path)==h;inputs[path]=h
 for name,h in parent["prepared_input_hashes"].items():
  assert sha(DATA/name)==h;inputs[str((DATA/name).relative_to(WORK))]=h
 old=pd.read_csv(SOURCE/"repetition_metrics.csv")
 metrics=[];curves=[];start=time.monotonic()
 for year in [2014,2015,2016]:
  p=pd.read_csv(DATA/f"{year}_players.csv.gz").sort_values("athlete_id")
  A=p.ability.to_numpy();ids=p.athlete_id.to_numpy();n=len(A)
  saved10=[]
  for rep in range(1,101):
   with np.load(SOURCE/str(year)/f"pair_{rep:03d}.npz") as z:
    pairs=[]
    for ri,rho in enumerate([0,1]):
     selected_by_rate={}
     for q in [.027,.10]:
      k=math.floor(q*n+.5);selected=[]
      for lam in [0,1]:
       score=A-lam*z["congestion"][ri]
       order=np.lexsort((ids,-score))
       mask=np.zeros(n,dtype=bool);mask[order[:k]]=True
       # Separate pandas sort verifies tie rule and selected identities.
       check=pd.DataFrame({"score":score,"id":ids}).sort_values(["score","id"],ascending=[False,True]).index[:k]
       assert set(check)==set(np.flatnonzero(mask))
       assert mask.sum()==k
       if q==.027:assert np.array_equal(mask,z["selected"][ri,lam])
       selected.append(mask)
       for b in range(16):
        ix=z["bins"][ri]==b
        curves.append({"season":year,"repetition":rep,"rho":rho,"lambda":lam,"fraction":q,
          "K":k,"bin":b+1,"n_players":int(ix.sum()),"n_selected":int(mask[ix].sum()),
          "mean_peer":float(z["peer"][ri,ix].mean()),"rate":float(mask[ix].mean())})
      selected_by_rate[q]=np.array(selected)
      d=int(np.count_nonzero(selected[0]&~selected[1]))
      if q==.027:
       prev=old.loc[(old.season==year)&(old.repetition==rep)&(old.rho==rho)].iloc[0]
       assert d==prev.displaced and k==prev.K
      metrics.append({"season":year,"repetition":rep,"rho":rho,"fraction":q,"N":n,"K":k,
         "people_losing_selected_spot":d,"fraction_selected_changed":d/k})
     assert not (selected_by_rate[.027]&~selected_by_rate[.10]).any()
     pairs.append(selected_by_rate[.10])
    saved10.append(pairs)
   if rep%20==0:print(f"READOUT {year}: {rep}/100 saved pairs; elapsed {time.monotonic()-start:.1f}s",flush=True)
  np.savez_compressed(OUT/f"{year}_selected_10pct.npz",selected=np.array(saved10),athlete_id=ids)
 m=pd.DataFrame(metrics);c=pd.DataFrame(curves)
 m.to_csv(OUT/"selection_changes_by_repetition.csv",index=False);c.to_csv(OUT/"curve_bins.csv",index=False)
 summary=m.groupby(["season","rho","fraction"]).agg(N=("N","first"),K=("K","first"),
  mean_people_changed=("people_losing_selected_spot","mean"),
  mean_percent_selected_changed=("fraction_selected_changed",lambda x:100*x.mean()),
  min_people=("people_losing_selected_spot","min"),max_people=("people_losing_selected_spot","max"),
  p025_people=("people_losing_selected_spot",lambda x:x.quantile(.025)),
  p975_people=("people_losing_selected_spot",lambda x:x.quantile(.975))).reset_index()
 summary.to_csv(OUT/"selection_changes_summary.csv",index=False)
 agg=c.groupby(["season","rho","lambda","fraction","bin"]).agg(mean_rate=("rate","mean"),
   low=("rate",lambda x:x.quantile(.025)),high=("rate",lambda x:x.quantile(.975)),
   mean_peer=("mean_peer","mean")).reset_index()
 agg.to_csv(OUT/"curve_summary.csv",index=False)
 import matplotlib
 matplotlib.use("Agg")
 import matplotlib.pyplot as plt
 fig,axs=plt.subplots(3,2,figsize=(12,11),sharex=True,sharey=True)
 for row,year in enumerate([2014,2015,2016]):
  for col,rho in enumerate([0,1]):
   ax=axs[row,col]
   for lam,color,label in [(0,"#52657b","Congestion off"),(1,"#b74b12","Congestion on")]:
    g=agg.loc[(agg.season==year)&(agg.rho==rho)&(agg["lambda"]==lam)&(agg.fraction==.10)]
    ax.plot(g.bin,100*g.mean_rate,color=color,lw=2,label=label)
    ax.fill_between(g.bin.to_numpy(),100*g.low,100*g.high,color=color,alpha=.10)
   s=summary.loc[(summary.season==year)&(summary.rho==rho)&(summary.fraction==.10)].iloc[0]
   ax.axhline(100*s.K/s.N,ls=":",color="gray",lw=1)
   ax.set_title(f"{year} | "+("No similarity preference" if rho==0 else "Similarity preference")+f" | K={int(s.K)}")
   ax.set_xticks([1,4,8,12,16]);ax.grid(alpha=.2)
   if col==0:ax.set_ylabel("Selected players (%)")
   if row==2:ax.set_xlabel("Peer-quality bin (low to high; equal player counts)")
 axs[0,0].legend()
 fig.suptitle("10% selection: more opportunities, identical teams and scores\n100 paired assignments per season; raw congestion unchanged",fontsize=15)
 fig.text(.5,.025,"Lines: assignment means. Shading: central 95% assignment range, not confidence intervals.\nBins and peer values are identical to the 2.7% comparison. No team formation was rerun.\nDotted line: overall selected fraction. These are simulated selections, not draft predictions.",ha="center",fontsize=10)
 fig.tight_layout(rect=[0,.085,1,.94]);fig.savefig(OUT/"selection_curves_10pct.png",dpi=160);plt.close(fig)
 assert all(sha(WORK/path)==h for path,h in inputs.items())
 write(RECORD,{"status":"executed_checked_pending_visual_review","completed_utc":datetime.now(timezone.utc).isoformat(),
 "scope":"Only selection fraction changed, 0.027 to 0.10; no assignment rerun",
 "input_hashes":inputs,"numpy":np.__version__,"pandas":pd.__version__,
 "checks":["all original 2.7% winners and counts exactly reproduced","10% sets contain corresponding 2.7% sets",
 "independent pandas and numpy score/tie rankings agree in every case","unchanged parent files"],
 "outputs":{str(p.relative_to(WORK)):sha(p) for p in sorted(OUT.iterdir()) if p.is_file()}})
 print("READOUT COMPLETE\n"+summary.to_string(index=False),flush=True)
if __name__=="__main__":main()

