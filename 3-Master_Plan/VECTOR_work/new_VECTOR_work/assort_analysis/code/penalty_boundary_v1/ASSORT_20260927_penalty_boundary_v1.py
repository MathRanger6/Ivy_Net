#!/usr/bin/env python3
"""Bounded, authorized penalty construction followed by fixed-penalty scarcity."""
import argparse, hashlib, json, math, sys, time
from pathlib import Path
from datetime import datetime, timezone
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve()
WORK=HERE.parents[2]
SETTINGS=HERE.with_name("ASSORT_20260927_penalty_boundary_v1_settings.json")
SPEC=WORK/"docs/decisions/ASSORT_20260927_penalty_boundary_v1_specification.md"
OUT=WORK/"outputs/penalty_boundary_v1"
RECORD=WORK/"docs/run_records/ASSORT_20260927_penalty_boundary_v1_run_record.json"
DATA=WORK/"data/three_season_mechanism_v1/prepared"
SOURCE=WORK/"outputs/three_season_mechanism_v1"
def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for block in iter(lambda:f.read(2**20),b""): h.update(block)
    return h.hexdigest()
def dump(p,o): p.write_text(json.dumps(o,indent=2,allow_nan=False)+"\n")
def metric(counts,sizes,start):
    rates=lambda a,b:counts[:,a:b].sum(axis=1)/sizes[:,a:b].sum(axis=1)
    low=rates(0,4); peak=rates(start,start+4); high=rates(12,16)
    difference=peak-high
    return {"window_start":start+1,"window_end":start+4,
        "low":float(low.mean()),"peak":float(peak.mean()),"high":float(high.mean()),
        "rise":float((peak-low).mean()),"drop":float(difference.mean()),
        "relative_drop":float(difference.mean()/peak.mean()) if peak.mean()>0 else None,
        "positive_fraction":float(np.mean(difference>0)),
        "drop_p025":float(np.quantile(difference,.025)),
        "drop_p975":float(np.quantile(difference,.975))}
def best_window(counts,sizes):
    return int(np.argmax([(counts[:,s:s+4].sum(1)/sizes[:,s:s+4].sum(1)).mean() for s in range(9)]))
def main():
    raise RuntimeError("Superseded unexecuted draft: automatic thresholds and scarcity stage were not approved. Use penalty_bars_v1 instead.")
    ap=argparse.ArgumentParser();ap.add_argument("--run",action="store_true")
    if not ap.parse_args().run:ap.error("--run required")
    if OUT.exists() or RECORD.exists():raise RuntimeError("Refusing overwrite")
    cfg=json.loads(SETTINGS.read_text());OUT.mkdir(parents=True)
    started=time.monotonic()
    inputs={}
    def track(p):
        inputs[str(p.relative_to(WORK))]=sha(p)
    for p in [HERE,SETTINGS,SPEC]:track(p)
    parent_path=WORK/"docs/run_records/ASSORT_20260927_three_season_mechanism_v1_run_record.json"
    parent=json.loads(parent_path.read_text());track(parent_path)
    tenpath=WORK/"docs/run_records/ASSORT_20260927_selection_rate_comparison_v1_run_record.json"
    tenrecord=json.loads(tenpath.read_text());track(tenpath)
    frozen={}
    for year in cfg["seasons"]:
        pth=DATA/f"{year}_players.csv.gz"
        assert sha(pth)==parent["prepared_input_hashes"][pth.name];track(pth)
        p=pd.read_csv(pth).sort_values("athlete_id")
        ids=p.athlete_id.to_numpy();A=p.ability.to_numpy();n=len(A)
        assert len(np.unique(ids))==n
        v=1/(1+np.exp(-10*(A-np.quantile(A,.99))))
        C=[];bins=[]
        for rep in range(1,101):
            f=SOURCE/str(year)/f"pair_{rep:03d}.npz"
            assert sha(f)==parent["output_hashes"][str(f.relative_to(WORK))];track(f)
            with np.load(f) as z:
                pool=z["pool"][1];congestion=z["congestion"][1]
                calc=np.bincount(pool,weights=v)/np.bincount(pool)
                np.testing.assert_allclose(calc[pool],congestion,atol=1e-12,rtol=1e-12)
                C.append(congestion.copy());bins.append(z["bins"][1].copy())
        tenfile=WORK/f"outputs/selection_rate_comparison_v1/{year}_selected_10pct.npz"
        assert sha(tenfile)==tenrecord["outputs"][str(tenfile.relative_to(WORK))];track(tenfile)
        with np.load(tenfile) as z:
            assert np.array_equal(ids,z["athlete_id"])
            previous=z["selected"][:,1,1].copy()
        bins=np.array(bins)
        sizes=np.array([np.bincount(b,minlength=16) for b in bins])
        assert (sizes>0).all()
        frozen[year]={"A":A,"ids":ids,"C":np.array(C),"bins":bins,"sizes":sizes,"previous":previous}
        print(f"INPUT CHECK {year}: {n} players, 100 saved preferential assignments verified.",flush=True)
    def evaluate(year,lam,q):
        d=frozen[year];n=len(d["A"]);k=math.floor(q*n+.5)
        masks=[];counts=[]
        for r in range(100):
            score=d["A"]-lam*d["C"][r]
            order=np.lexsort((d["ids"],-score))
            mask=np.zeros(n,dtype=bool);mask[order[:k]]=True
            independent=pd.DataFrame({"s":score,"id":d["ids"]}).sort_values(["s","id"],ascending=[False,True]).index[:k]
            assert set(independent)==set(np.flatnonzero(mask))
            assert mask.sum()==k
            if lam==1 and q==.1:assert np.array_equal(mask,d["previous"][r])
            masks.append(mask);counts.append(np.bincount(d["bins"][r,mask],minlength=16))
        counts=np.array(counts)
        assert np.all(counts.sum(1)==k)
        return np.array(masks),counts,k
    search=[];search_curves=[];chosen=None;windows={}
    for lam in cfg["lambda_candidates"]:
        all_pass=True;current={}
        for year in cfg["seasons"]:
            masks,counts,k=evaluate(year,lam,.1)
            sizes=frozen[year]["sizes"]
            s=best_window(counts,sizes);m=metric(counts,sizes,s)
            passed=(m["rise"]>=cfg["rise"] and m["drop"]>=cfg["absolute_drop"]
                and m["relative_drop"] is not None and m["relative_drop"]>=cfg["relative_drop"]
                and m["positive_fraction"]>=cfg["positive_repetition_fraction"])
            m.update(season=year,penalty=lam,K=k,N=len(frozen[year]["A"]),passes=bool(passed))
            search.append(m);current[year]=s;all_pass &= passed
            np.savez_compressed(OUT/f"search_{year}_lambda_{lam}.npz",selected=masks,counts=counts,sizes=sizes,athlete_id=frozen[year]["ids"])
            for b in range(16):
                rates=counts[:,b]/sizes[:,b]
                search_curves.append({"season":year,"penalty":lam,"bin":b+1,"mean":rates.mean()})
            print(f"SEARCH lambda={lam}, {year}: rise {100*m['rise']:.2f} pp; fall {100*m['drop']:.2f} pp; relative fall {100*m['relative_drop']:.1f}%; passes={passed}",flush=True)
        pd.DataFrame(search).to_csv(OUT/"search_summary.csv",index=False)
        pd.DataFrame(search_curves).to_csv(OUT/"search_curves.csv",index=False)
        if all_pass:
            chosen=lam;windows=current;break
    dump(OUT/"search_decision.json",{"chosen_lambda":chosen,"windows_zero_based":windows,"bounded_candidates":cfg["lambda_candidates"]})
    boundary=[];curve_rows=[]
    if chosen is not None:
        print(f"FREEZE lambda={chosen}. Starting lower-selection-fraction comparison; no retuning.",flush=True)
        for year in cfg["seasons"]:
            d=frozen[year];n=len(d["A"]);sizes=d["sizes"]
            for lam in [0,chosen]:
                larger=None
                for q in cfg["fractions"]:
                    masks,counts,k=evaluate(year,lam,q)
                    if larger is not None:assert not (masks&~larger).any()
                    larger=masks
                    m=metric(counts,sizes,windows[year])
                    m.update(season=year,penalty=lam,fraction=q,K=k,N=n,achieved=k/n,
                        drop_over_overall_rate=m["drop"]/(k/n))
                    boundary.append(m)
                    adaptive=metric(counts,sizes,best_window(counts,sizes))
                    dump(OUT/f"adaptive_{year}_lambda_{lam}_q_{q}.json",adaptive)
                    np.savez_compressed(OUT/f"boundary_{year}_lambda_{lam}_q_{q}.npz",selected=masks,counts=counts,sizes=sizes,athlete_id=d["ids"])
                    for b in range(16):
                        rates=counts[:,b]/sizes[:,b]
                        curve_rows.append({"season":year,"penalty":lam,"fraction":q,"achieved":k/n,"bin":b+1,
                            "mean":rates.mean(),"p025":np.quantile(rates,.025),"p975":np.quantile(rates,.975)})
                print(f"BOUNDARY {year}, lambda={lam}: all five selection fractions checked.",flush=True)
            pd.DataFrame(boundary).to_csv(OUT/"boundary_summary.csv",index=False)
            pd.DataFrame(curve_rows).to_csv(OUT/"boundary_curves.csv",index=False)
    sc=pd.DataFrame(search_curves)
    fig,axs=plt.subplots(1,3,figsize=(12,3.9),sharey=True)
    for ax,year in zip(axs,cfg["seasons"]):
        for lam,g in sc.loc[sc.season==year].groupby("penalty",sort=True):
            ax.plot(g.bin,100*g["mean"],label=f"lambda {lam}",lw=1.7)
        ax.set_title(str(year));ax.set_xlabel("Peer-quality bin");ax.set_xticks([1,4,8,12,16]);ax.grid(alpha=.2)
    axs[0].set_ylabel("Selected (%)");axs[-1].legend(fontsize=8)
    fig.suptitle("Constructing a downturn at 10% selection | fixed assignment preference rho = 1")
    fig.tight_layout();fig.savefig(OUT/"penalty_search.png",dpi=160);plt.close(fig)
    if chosen is not None:
        c=pd.DataFrame(curve_rows)
        fig,axs=plt.subplots(3,2,figsize=(10,10),sharex=True)
        colors=["#193f74","#248d8c","#e49523","#a34973","#696969"]
        for row,year in enumerate(cfg["seasons"]):
            for q,color in zip(cfg["fractions"],colors):
                g=c.loc[(c.season==year)&(c.penalty==chosen)&(c.fraction==q)]
                axs[row,0].plot(g.bin,100*g["mean"],color=color,label=f"{100*q:g}% selected",lw=1.8)
                axs[row,1].plot(g.bin,g["mean"]/g.achieved,color=color,lw=1.8)
            for col in range(2):
                axs[row,col].set_title(f"{year} | "+("Actual selection rates" if col==0 else "Relative to overall selection rate"))
                axs[row,col].grid(alpha=.2);axs[row,col].set_xticks([1,4,8,12,16])
                if row==2:axs[row,col].set_xlabel("Peer-quality bin (low to high)")
            axs[row,0].set_ylabel("Selected (%)");axs[row,1].set_ylabel("Bin rate / overall rate")
        axs[0,0].legend(fontsize=8)
        fig.suptitle(f"Freeze lambda = {chosen}, then reduce available places | rho = 1 throughout")
        fig.text(.5,.01,"Means across 100 fixed assignments per season. Left shows absolute size; right separates shape from overall scarcity.\nThese are model selections, not observed draft rates. No rho comparison or new assignments.",ha="center",fontsize=9)
        fig.tight_layout(rect=[0,.055,1,.96]);fig.savefig(OUT/"scarcity_comparison.png",dpi=160);plt.close(fig)
    assert all(sha(WORK/p)==h for p,h in inputs.items())
    dump(RECORD,{"status":"executed_checked_pending_visual_review","completed_utc":datetime.now(timezone.utc).isoformat(),
        "python_executable":sys.executable,"python":sys.version,"numpy":np.__version__,"pandas":pd.__version__,
        "elapsed_seconds":time.monotonic()-started,"chosen_lambda":chosen,"rho":1,
        "checks":["source hashes matched parent records","congestion independently reconstructed",
            "previous lambda-one 10% selections reproduced","pandas and numpy rankings agree",
            "all selection counts exact","lower-fraction winner sets nested","source hashes unchanged"],
        "input_hashes":inputs,"output_hashes":{str(p.relative_to(WORK)):sha(p) for p in sorted(OUT.iterdir()) if p.is_file()}})
    print(f"COMPLETE: chosen lambda={chosen}; {time.monotonic()-started:.1f} seconds.",flush=True)
if __name__=="__main__":main()
