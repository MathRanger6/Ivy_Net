#!/usr/bin/env python3
"""Only K changes; fixed lambda four, rho one, and existing EW/quantile bins."""
import argparse, hashlib, json, math, sys, time
from pathlib import Path
from datetime import datetime, timezone
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve();WORK=HERE.parents[2]
OUT=WORK/"outputs/scarcity_bars_v1"
RECORD=WORK/"docs/run_records/ASSORT_20260927_scarcity_bars_v1_run_record.json"
SPEC=WORK/"docs/decisions/ASSORT_20260927_scarcity_bars_v1_specification.md"
FRACTIONS=[.1,.05,.027,.01];YEARS=[2014,2015,2016]
def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for block in iter(lambda:f.read(2**20),b""):h.update(block)
    return h.hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2,allow_nan=False)+"\n")
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--run",action="store_true")
    if not ap.parse_args().run:ap.error("--run required")
    if OUT.exists() or RECORD.exists():raise RuntimeError("Refusing overwrite")
    OUT.mkdir(parents=True);start=time.monotonic();inputs={}
    def track(p):inputs[str(p.relative_to(WORK))]=sha(p)
    for p in [HERE,SPEC]:track(p)
    pp=WORK/"docs/run_records/ASSORT_20260927_penalty_bars_v1_run_record.json"
    parent=json.loads(pp.read_text());track(pp)
    for rel,h in parent["input_hashes"].items():
        assert sha(WORK/rel)==h;inputs[rel]=h
    previous=pd.read_csv(WORK/"outputs/penalty_bars_v1/bar_summary.csv")
    previouspath=WORK/"outputs/penalty_bars_v1/bar_summary.csv"
    assert sha(previouspath)==parent["output_hashes"][str(previouspath.relative_to(WORK))]
    track(previouspath)
    rows=[];slots=[]
    for year in YEARS:
        p=pd.read_csv(WORK/f"data/three_season_mechanism_v1/prepared/{year}_players.csv.gz").sort_values("athlete_id")
        A=p.ability.to_numpy();ids=p.athlete_id.to_numpy();n=len(A)
        savedpath=WORK/f"outputs/penalty_bars_v1/{year}_selections_and_bins.npz"
        assert sha(savedpath)==parent["output_hashes"][str(savedpath.relative_to(WORK))];track(savedpath)
        with np.load(savedpath) as z:
            assert np.array_equal(ids,z["athlete_id"])
            ew=z["ew_bins"].copy();quant=z["quantile_bins"].copy();edges=z["ew_edges"].copy()
            old=z["selected"][list(z["lambdas"]).index(4)].copy()
        orders=[]
        for rep in range(1,101):
            f=WORK/f"outputs/three_season_mechanism_v1/{year}/pair_{rep:03d}.npz"
            # Each source is already hash-checked against the preceding chart record.
            assert str(f.relative_to(WORK)) in inputs
            with np.load(f) as z:score=A-4*z["congestion"][1]
            order=np.lexsort((ids,-score))
            check=pd.DataFrame({"s":score,"id":ids}).sort_values(["s","id"],ascending=[False,True]).index.to_numpy()
            assert np.array_equal(order,check)
            orders.append(order)
        allmasks=[];larger=None
        for q in FRACTIONS:
            k=math.floor(q*n+.5);masks=[]
            slots.append({"season":year,"fraction":q,"N":n,"K":k,"achieved":k/n})
            for rep,order in enumerate(orders):
                mask=np.zeros(n,dtype=bool);mask[order[:k]]=True
                assert mask.sum()==k
                if q==.1:assert np.array_equal(mask,old[rep])
                masks.append(mask)
                for label,bins in [("EW",ew),("Quantile",quant)]:
                    counts=np.bincount(bins[rep],minlength=16)
                    winners=np.bincount(bins[rep,mask],minlength=16)
                    assert counts.sum()==n and winners.sum()==k
                    for bi in range(16):
                        rows.append({"season":year,"fraction":q,"achieved":k/n,"K":k,"method":label,
                          "repetition":rep+1,"bin":bi+1,"players":int(counts[bi]),"selected":int(winners[bi]),
                          "rate":float(winners[bi]/counts[bi]) if counts[bi] else np.nan})
            masks=np.array(masks)
            if larger is not None:assert not (masks&~larger).any()
            larger=masks;allmasks.append(masks)
            print(f"CHECKED {year}: {100*q:g}% target, {k}/{n} selected; 100 assignments; both binning methods.",flush=True)
        np.savez_compressed(OUT/f"{year}_selections_and_bins.npz",selected=np.array(allmasks),
          fractions=np.array(FRACTIONS),athlete_id=ids,ew_bins=ew,quantile_bins=quant,ew_edges=edges)
        pd.DataFrame(rows).to_csv(OUT/"bin_counts_by_repetition.csv",index=False)
    df=pd.DataFrame(rows)
    s=df.groupby(["season","fraction","achieved","method","bin"]).agg(
      total_players=("players","sum"),total_selected=("selected","sum"),mean_players=("players","mean"),
      occupied_repetitions=("players",lambda x:int((x>0).sum())),
      p025_nonempty_rate=("rate",lambda x:x.quantile(.025)),
      p975_nonempty_rate=("rate",lambda x:x.quantile(.975))).reset_index()
    s["pooled_rate"]=s.total_selected/s.total_players.replace(0,np.nan)
    s["relative_rate"]=s.pooled_rate/s.achieved
    for year in YEARS:
        for method in ["EW","Quantile"]:
            g=s.loc[(s.season==year)&(s.fraction==.1)&(s.method==method)].sort_values("bin")
            old=previous.loc[(previous.season==year)&(previous["lambda"]==4)&(previous.method==method)].sort_values("bin")
            np.testing.assert_allclose(g.pooled_rate,old.pooled_rate,atol=1e-12)
    s.to_csv(OUT/"bar_summary.csv",index=False);pd.DataFrame(slots).to_csv(OUT/"selection_counts.csv",index=False)
    ymax_abs=math.ceil(100*s.pooled_rate.max()/5)*5
    ymax_rel=math.ceil(s.relative_rate.max())
    for year in YEARS:
        for view in ["absolute","relative"]:
            fig,axs=plt.subplots(5,2,figsize=(12,13),gridspec_kw={"height_ratios":[1,1,1,1,.85]})
            for col,method in enumerate(["EW","Quantile"]):
                for row,(q,color) in enumerate(zip(FRACTIONS,["#a23e4a","#b27c24","#34748c","#61548a"])):
                    g=s.loc[(s.season==year)&(s.fraction==q)&(s.method==method)].sort_values("bin")
                    ax=axs[row,col]
                    vals=100*g.pooled_rate if view=="absolute" else g.relative_rate
                    ax.bar(g.bin,vals,color=color,width=.85)
                    ax.axhline(100*g.achieved.iloc[0] if view=="absolute" else 1,color="black",ls=":",lw=.8)
                    ax.set_ylim(0,ymax_abs if view=="absolute" else ymax_rel)
                    ax.set_xlim(.3,16.7);ax.set_xticks([1,4,8,12,16]);ax.grid(axis="y",alpha=.2)
                    ax.set_ylabel("Selected (%)" if view=="absolute" else "Bin rate / overall rate")
                    ax.set_title(f"{method} | {100*q:g}% selection")
                g=s.loc[(s.season==year)&(s.fraction==.1)&(s.method==method)].sort_values("bin")
                ax=axs[4,col];ax.bar(g.bin,g.mean_players,color="#909a9e",width=.85)
                for x,y in zip(g.bin,g.mean_players):
                    ax.text(x,y+max(g.mean_players)*.015,f"{y:.1f}" if y<10 else f"{y:.0f}",ha="center",va="bottom",fontsize=7,rotation=90)
                ax.set_ylim(0,max(g.mean_players)*1.3);ax.set_xlim(.3,16.7);ax.set_xticks([1,4,8,12,16])
                ax.set_title("Player counts — unchanged at every selection fraction")
                ax.set_ylabel("Mean players / assignment");ax.set_xlabel("Peer-quality bin: low to high")
            fig.suptitle(f"{year}: fewer places, same scores | lambda = 4, rho = 1\n"+("Actual selection rates" if view=="absolute" else "Relative rates: 2 means twice the overall selection rate"),fontsize=15)
            fig.text(.5,.013,"Same players, teams and bins at every fraction; 100 saved assignments. No additional assignment randomness.\nBars pool selected/player counts. Sparse EW tails require caution; repetitions are not independent empirical samples.\nVertical scales match all seasons and fractions within each view. No automatic downturn classification.",ha="center",fontsize=9)
            fig.tight_layout(rect=[0,.07,1,.945]);fig.savefig(OUT/f"{year}_scarcity_{view}.png",dpi=150);plt.close(fig)
    assert all(sha(WORK/p)==h for p,h in inputs.items())
    dump(RECORD,{"status":"executed_checked_pending_visual_review","completed_utc":datetime.now(timezone.utc).isoformat(),
      "python_executable":sys.executable,"python":sys.version,"numpy":np.__version__,"pandas":pd.__version__,
      "lambda":4,"rho":1,"fractions":FRACTIONS,"elapsed_seconds":time.monotonic()-start,
      "checks":["all prior source hashes verified","independent full-rank orders agree",
      "all 1200 selected sets have exact K","10% winners and bars exactly reproduced",
      "lower-fraction selections nested","both binnings conserve player and winner counts","source hashes unchanged"],
      "input_hashes":inputs,"output_hashes":{str(p.relative_to(WORK)):sha(p) for p in sorted(OUT.iterdir()) if p.is_file()}})
    print("COMPLETE: fixed-penalty scarcity comparison only.",flush=True)
if __name__=="__main__":main()

