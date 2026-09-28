#!/usr/bin/env python3
"""Measure lambda=1 penalties in existing runs. No new assignment or lambda search.
All spreads weight players equally. Cutoff diagnostics cover both existing rates.
Illustrations use repetition 1 and smallest athlete ID among losses/gains.
"""
import argparse,hashlib,json,math,sys,time
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
import pandas as pd
HERE=Path(__file__).resolve();WORK=HERE.parents[2]
SRC=WORK/"outputs/three_season_mechanism_v1"
DATA=WORK/"data/three_season_mechanism_v1/prepared"
RATE=WORK/"outputs/selection_rate_comparison_v1"
OUT=WORK/"outputs/penalty_magnitude_v1"
RECORD=WORK/"docs/run_records/ASSORT_20260927_penalty_magnitude_v1_run_record.json"
PARENT=WORK/"docs/run_records/ASSORT_20260927_three_season_mechanism_v1_run_record.json"
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(2**20),b""):h.update(b)
 return h.hexdigest()
def main():
 a=argparse.ArgumentParser();a.add_argument("--run",action="store_true")
 if not a.parse_args().run:a.error("--run required")
 if OUT.exists() or RECORD.exists():raise RuntimeError("Refusing overwrite")
 OUT.mkdir(parents=True)
 parent=json.loads(PARENT.read_text())
 inputs={str(PARENT.relative_to(WORK)):sha(PARENT),str(HERE.relative_to(WORK)):sha(HERE)}
 for rel,h in parent["output_hashes"].items():
  assert sha(WORK/rel)==h;inputs[rel]=h
 for name,h in parent["prepared_input_hashes"].items():
  assert sha(DATA/name)==h;inputs[str((DATA/name).relative_to(WORK))]=h
 tenrecord=WORK/"docs/run_records/ASSORT_20260927_selection_rate_comparison_v1_run_record.json"
 tr=json.loads(tenrecord.read_text())
 inputs[str(tenrecord.relative_to(WORK))]=sha(tenrecord)
 for rel,h in tr["outputs"].items():
  assert sha(WORK/rel)==h;inputs[rel]=h
 scale=[];cutoff=[];examples=[];fixed=[];start=time.monotonic()
 for year in [2014,2015,2016]:
  p=pd.read_csv(DATA/f"{year}_players.csv.gz").sort_values("athlete_id").reset_index(drop=True)
  A=p.ability.to_numpy();ids=p.athlete_id.to_numpy();order=np.lexsort((ids,-A))
  n=len(A);theta=float(np.quantile(A,.99));v=1/(1+np.exp(-10*(A-theta)))
  with np.load(RATE/f"{year}_selected_10pct.npz") as saved:ten=saved["selected"].copy()
  fixed.append({"season":year,"N":n,"ability_sd":float(A.std()),"theta":theta,
     "ability_p90":float(np.quantile(A,.9)),"ability_p95":float(np.quantile(A,.95)),
     "ability_p99":theta,"mean_individual_viability":float(v.mean())})
  for rep in range(1,101):
   with np.load(SRC/str(year)/f"pair_{rep:03d}.npz") as z:
    for ri,rho in enumerate([0,1]):
     C=z["congestion"][ri];S=A-C;pool=z["pool"][ri]
     size=np.bincount(pool)
     independently=np.bincount(pool,weights=v)/size
     np.testing.assert_allclose(C,independently[pool],atol=1e-12)
     assert np.all((C>=0)&(C<=1)) and abs(C.mean()-v.mean())<1e-12
     gapA=A[z["bins"][ri]==15].mean()-A[z["bins"][ri]==14].mean()
     gapC=C[z["bins"][ri]==15].mean()-C[z["bins"][ri]==14].mean()
     scale.append({"season":year,"repetition":rep,"rho":rho,
        "penalty_mean":C.mean(),"penalty_sd":C.std(),"penalty_min":C.min(),"penalty_max":C.max(),
        "penalty_p50":np.quantile(C,.5),"penalty_p90":np.quantile(C,.9),"penalty_p99":np.quantile(C,.99),
        "penalty_range":np.ptp(C),"sd_penalty_over_sd_ability":C.std()/A.std(),
        "top_bin_minus_next_ability":gapA,"top_bin_minus_next_penalty":gapC,
        "top_bin_minus_next_score":gapA-gapC})
     for q in [.027,.10]:
      k=math.floor(q*n+.5)
      off=np.zeros(n,dtype=bool);off[order[:k]]=True
      on=z["selected"][ri,1] if q==.027 else ten[rep-1,ri,1]
      ranked=np.lexsort((ids,-S));expected=np.zeros(n,dtype=bool);expected[ranked[:k]]=True
      assert np.array_equal(on,expected)
      lost=off&~on;gained=~off&on;count=int(lost.sum());assert count==gained.sum()
      boundary=float(A[order[k-1]])
      cutoff.append({"season":year,"repetition":rep,"rho":rho,"fraction":q,"K":k,
        "ability_cutoff":boundary,"adjacent_ability_gap":boundary-A[order[k]],
        "lost_count":count,"lost_fraction":count/k,
        "mean_penalty_ability_only_winners":float(C[off].mean()),
        "mean_penalty_other_players":float(C[~off].mean()),
        "max_lost_ability_above_cutoff":float(np.max(A[lost]-boundary)) if count else np.nan,
        "max_gained_ability_below_cutoff":float(np.max(boundary-A[gained])) if count else np.nan,
        "mean_lost_minus_gained_ability":float(A[lost].mean()-A[gained].mean()) if count else np.nan,
        "mean_lost_minus_gained_penalty":float(C[lost].mean()-C[gained].mean()) if count else np.nan})
      if rep==1 and count:
       lo=np.flatnonzero(lost)[0];ga=np.flatnonzero(gained)[0]
       namecol="name" if "name" in p else "athlete_display_name"
       ex={"season":year,"rho":rho,"fraction":q,"K":k,"repetition":rep,
         "losing_id":int(ids[lo]),"gaining_id":int(ids[ga]),
         "losing_name":str(p.iloc[lo][namecol]),"gaining_name":str(p.iloc[ga][namecol]),
         "losing_ability":float(A[lo]),"gaining_ability":float(A[ga]),
         "losing_penalty":float(C[lo]),"gaining_penalty":float(C[ga]),
         "losing_score":float(S[lo]),"gaining_score":float(S[ga])}
       assert ex["losing_ability"]>=ex["gaining_ability"] and ex["losing_score"]<=ex["gaining_score"]
       examples.append(ex)
   if rep%25==0:print(f"DIAGNOSTIC {year}: {rep}/100 saved pairs; elapsed {time.monotonic()-start:.1f}s",flush=True)
 s=pd.DataFrame(scale);c=pd.DataFrame(cutoff)
 s.to_csv(OUT/"penalty_scale_by_repetition.csv",index=False)
 c.to_csv(OUT/"cutoff_by_repetition.csv",index=False)
 pd.DataFrame(examples).to_csv(OUT/"first_repetition_examples.csv",index=False)
 pd.DataFrame(fixed).to_csv(OUT/"fixed_season_quantities.csv",index=False)
 # Each season/preference mean below averages 100 repetitions, not new empirical samples.
 ss=s.groupby(["season","rho"]).mean(numeric_only=True).drop(columns="repetition").reset_index()
 cs=c.groupby(["season","rho","fraction"]).mean(numeric_only=True).drop(columns="repetition").reset_index()
 ss.to_csv(OUT/"penalty_scale_summary.csv",index=False)
 cs.to_csv(OUT/"cutoff_summary.csv",index=False)
 assert len(s)==600 and len(c)==1200
 assert all(sha(WORK/rel)==h for rel,h in inputs.items())
 rec={"status":"executed_checked","completed_utc":datetime.now(timezone.utc).isoformat(),
      "python_executable":sys.executable,"python":sys.version,"numpy":np.__version__,"pandas":pd.__version__,
      "purpose":"describe existing lambda=1 penalty scale and actual cutoff changes; no parameter sweep",
      "scope":"600 saved assignment conditions, 1200 selection-rate conditions",
      "checks":["congestion independently recomputed from saved rosters","mean congestion equals mean viability",
                "every saved winner set checked against unchanged scores","lost/gained counts balance",
                "deterministic example selection; no search for dramatic example","all input hashes unchanged"],
      "input_hashes":inputs,"outputs":{str(p.relative_to(WORK)):sha(p) for p in OUT.iterdir() if p.is_file()}}
 RECORD.write_text(json.dumps(rec,indent=2,allow_nan=False)+"\n")
 print("DIAGNOSTIC COMPLETE\n"+ss.to_string(index=False)+"\n"+cs.to_string(index=False),flush=True)
if __name__=="__main__":main()

