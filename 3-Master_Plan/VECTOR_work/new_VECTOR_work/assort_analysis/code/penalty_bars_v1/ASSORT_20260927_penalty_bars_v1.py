#!/usr/bin/env python3
"""Authorized chart-first penalty readout; no automatic downturn classification."""
import argparse, hashlib, json, math, sys, time
from pathlib import Path
from datetime import datetime, timezone
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve(); WORK=HERE.parents[2]
OUT=WORK/"outputs/penalty_bars_v1"
RECORD=WORK/"docs/run_records/ASSORT_20260927_penalty_bars_v1_run_record.json"
SPEC=WORK/"docs/decisions/ASSORT_20260927_penalty_bars_v1_specification.md"
DATA=WORK/"data/three_season_mechanism_v1/prepared"
SRC=WORK/"outputs/three_season_mechanism_v1"
LAMBDAS=[0,1,2,4]; YEARS=[2014,2015,2016]
def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for block in iter(lambda:f.read(2**20),b""):h.update(block)
    return h.hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2,allow_nan=False)+"\n")
def main():
    parser=argparse.ArgumentParser();parser.add_argument("--run",action="store_true")
    if not parser.parse_args().run:parser.error("--run required")
    if OUT.exists() or RECORD.exists():raise RuntimeError("Refusing overwrite")
    OUT.mkdir(parents=True);start=time.monotonic();inputs={}
    def track(p):inputs[str(p.relative_to(WORK))]=sha(p)
    for p in [HERE,SPEC]:track(p)
    parentpath=WORK/"docs/run_records/ASSORT_20260927_three_season_mechanism_v1_run_record.json"
    tenpath=WORK/"docs/run_records/ASSORT_20260927_selection_rate_comparison_v1_run_record.json"
    parent=json.loads(parentpath.read_text());tenrecord=json.loads(tenpath.read_text())
    track(parentpath);track(tenpath)
    rows=[];edges_record={};counts_record=[]
    for year in YEARS:
        pth=DATA/f"{year}_players.csv.gz"
        assert sha(pth)==parent["prepared_input_hashes"][pth.name];track(pth)
        p=pd.read_csv(pth).sort_values("athlete_id")
        A=p.ability.to_numpy();ids=p.athlete_id.to_numpy();n=len(A);k=math.floor(.1*n+.5)
        assert len(np.unique(ids))==n
        v=1/(1+np.exp(-10*(A-np.quantile(A,.99))))
        Cs=[];peers=[];quant=[]
        for rep in range(1,101):
            f=SRC/str(year)/f"pair_{rep:03d}.npz"
            assert sha(f)==parent["output_hashes"][str(f.relative_to(WORK))];track(f)
            with np.load(f) as z:
                pool=z["pool"][1];C=z["congestion"][1];sz=np.bincount(pool)
                np.testing.assert_allclose(C,(np.bincount(pool,weights=v)/sz)[pool],atol=1e-12)
                peer=(np.bincount(pool,weights=A)[pool]-A)/(sz[pool]-1)
                np.testing.assert_allclose(peer,z["peer"][1],atol=1e-12)
                Cs.append(C.copy());peers.append(peer);quant.append(z["bins"][1].copy())
        Cs=np.array(Cs);peers=np.array(peers);quant=np.array(quant)
        edges=np.linspace(peers.min(),peers.max(),17)
        ew=np.minimum(np.searchsorted(edges,peers,side="right")-1,15)
        assert ew.min()==0 and ew.max()==15
        edges_record[str(year)]=edges.tolist()
        tenfile=WORK/f"outputs/selection_rate_comparison_v1/{year}_selected_10pct.npz"
        assert sha(tenfile)==tenrecord["outputs"][str(tenfile.relative_to(WORK))];track(tenfile)
        with np.load(tenfile) as z:
            assert np.array_equal(ids,z["athlete_id"])
            prior=z["selected"][:,1,1].copy()
        print(f"VERIFIED {year}: {n} players; K={k}; all 100 saved assignments.",flush=True)
        allmasks=[]
        for lam in LAMBDAS:
            masks=[]
            for rep in range(100):
                score=A-lam*Cs[rep]
                order=np.lexsort((ids,-score));mask=np.zeros(n,dtype=bool);mask[order[:k]]=True
                check=pd.DataFrame({"score":score,"id":ids}).sort_values(["score","id"],ascending=[False,True]).index[:k]
                assert set(check)==set(np.flatnonzero(mask))
                assert mask.sum()==k
                if lam==1:assert np.array_equal(mask,prior[rep])
                masks.append(mask)
                for label,binarray in [("EW",ew),("Quantile",quant)]:
                    sizes=np.bincount(binarray[rep],minlength=16)
                    selected=np.bincount(binarray[rep,mask],minlength=16)
                    assert sizes.sum()==n and selected.sum()==k
                    for bi in range(16):
                        rows.append({"season":year,"lambda":lam,"method":label,"repetition":rep+1,
                          "bin":bi+1,"N":n,"K":k,"players":int(sizes[bi]),"selected":int(selected[bi]),
                          "rate":float(selected[bi]/sizes[bi]) if sizes[bi] else np.nan})
            allmasks.append(masks)
            print(f"CALCULATED {year}: lambda={lam}; 100 selections checked; EW and quantile counted.",flush=True)
        np.savez_compressed(OUT/f"{year}_selections_and_bins.npz",selected=np.array(allmasks),
          lambdas=np.array(LAMBDAS),athlete_id=ids,ew_bins=ew,quantile_bins=quant,ew_edges=edges)
        pd.DataFrame(rows).to_csv(OUT/"bin_counts_by_repetition.csv",index=False)
    df=pd.DataFrame(rows)
    summary=df.groupby(["season","lambda","method","bin"],sort=True).agg(
      total_players=("players","sum"),total_selected=("selected","sum"),
      mean_players=("players","mean"),occupied_repetitions=("players",lambda x:int((x>0).sum())),
      minimum_players=("players","min"),maximum_players=("players","max"),
      mean_nonempty_rate=("rate","mean"),p025_nonempty_rate=("rate",lambda x:x.quantile(.025)),
      p975_nonempty_rate=("rate",lambda x:x.quantile(.975))).reset_index()
    summary["pooled_rate"]=summary.total_selected/summary.total_players.replace(0,np.nan)
    summary.to_csv(OUT/"bar_summary.csv",index=False)
    dump(OUT/"ew_edges.json",edges_record)
    ymax=min(100,max(10,math.ceil(100*summary.pooled_rate.max()/10)*10))
    for year in YEARS:
        fig,axs=plt.subplots(5,2,figsize=(12,13),gridspec_kw={"height_ratios":[1,1,1,1,.85]})
        colors=["#63758c","#346a95","#ca872c","#a23e4a"]
        for col,method in enumerate(["EW","Quantile"]):
            for row,(lam,color) in enumerate(zip(LAMBDAS,colors)):
                g=summary.loc[(summary.season==year)&(summary["lambda"]==lam)&(summary.method==method)].sort_values("bin")
                ax=axs[row,col]
                ax.bar(g.bin,100*g.pooled_rate,color=color,width=.85)
                ax.axhline(10,color="black",ls=":",lw=.8)
                ax.set_ylim(0,ymax);ax.set_xlim(.3,16.7);ax.set_xticks([1,4,8,12,16])
                ax.set_ylabel("Selected (%)");ax.grid(axis="y",alpha=.2)
                ax.set_title(f"{method}: "+("fixed peer-quality intervals" if method=="EW" else "equal-count groups")+f" | lambda = {lam}")
            g=summary.loc[(summary.season==year)&(summary["lambda"]==0)&(summary.method==method)].sort_values("bin")
            ax=axs[4,col];ax.bar(g.bin,g.mean_players,color="#909a9e",width=.85)
            for x,y in zip(g.bin,g.mean_players):
                ax.text(x,y+max(g.mean_players)*.015,f"{y:.1f}" if y<10 else f"{y:.0f}",ha="center",va="bottom",fontsize=7,rotation=90)
            ax.set_ylim(0,max(g.mean_players)*1.3);ax.set_xlim(.3,16.7);ax.set_xticks([1,4,8,12,16])
            ax.set_title("Player counts — unchanged across penalties")
            ax.set_ylabel("Mean players / assignment");ax.set_xlabel("Peer-quality bin: low to high")
        fig.suptitle(f"{year}: increase penalty, keep 10% selection and rho = 1\nSame players and 100 saved assignments at every penalty",fontsize=15)
        fig.text(.5,.013,"Bars pool selected/player counts over assignments; repeated players are not independent empirical observations.\nEW edges fixed across all assignments within this season. Quantile groups preserve within-assignment ranks.\nDotted line: nominal 10% selection. Sparse EW tails require caution. No downturn threshold or lambda chosen.",ha="center",fontsize=9)
        fig.tight_layout(rect=[0,.07,1,.945]);fig.savefig(OUT/f"{year}_penalty_bars.png",dpi=150);plt.close(fig)
    assert all(sha(WORK/p)==h for p,h in inputs.items())
    dump(RECORD,{"status":"executed_checked_pending_visual_review","completed_utc":datetime.now(timezone.utc).isoformat(),
       "python_executable":sys.executable,"python":sys.version,"numpy":np.__version__,"pandas":pd.__version__,
       "rho":1,"selection_fraction":.1,"lambdas":LAMBDAS,"seasons":YEARS,"repetitions":100,
       "no_automatic_downturn_classification":True,"no_scarcity_comparison":True,
       "elapsed_seconds":time.monotonic()-start,"input_hashes":inputs,
       "checks":["input hashes matched existing records","congestion and peer quality reconstructed",
       "all 1200 selections checked with numpy and pandas ranking","saved lambda-one selections reproduced exactly",
       "both binning methods conserve all players and selected counts","source hashes unchanged"],
       "output_hashes":{str(p.relative_to(WORK)):sha(p) for p in sorted(OUT.iterdir()) if p.is_file()}})
    print(f"COMPLETE: charts saved; {time.monotonic()-start:.1f} seconds. No further stage executed.",flush=True)
if __name__=="__main__":main()

