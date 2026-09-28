#!/usr/bin/env python3
"""Authorized bounded three-season assignment/congestion mechanism experiment.
--prepare freezes populations; --simulate runs 100 paired assignments per season.
Existing raw data, methods and outputs are read-only. New outputs refuse overwrite.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib
import json
import math
import os
from pathlib import Path
import sys
import time
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve()
WORK = HERE.parents[2]
REPO = WORK.parents[3]
STEM = "ASSORT_20260927_three_season_mechanism_v1"
SETTINGS = HERE.with_name(STEM + "_settings.json")
CFG = json.loads(SETTINGS.read_text())
SOURCE = REPO / "datasets/mbb/mbb_df_player_box.csv"
METHOD = REPO / "sports/541_grandchild_homophily_assign.py"
INPUT2015 = WORK / "outputs/rotation_audit_2015/ASSORT_20260927_rotation_audit_v1_players.csv.gz"
RECORD2015 = WORK / "docs/run_records/ASSORT_20260927_rotation_audit_v1_run_record.json"
PREFLIGHT = WORK / "docs/run_records" / (STEM + "_preflight.json")
DATA = WORK / "data/three_season_mechanism_v1/prepared"
OUT = WORK / "outputs/three_season_mechanism_v1"
RECORD = WORK / "docs/run_records" / (STEM + "_run_record.json")

def sha(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(2**20), b""):
            h.update(b)
    return h.hexdigest()

def write_json(p, d):
    p.write_text(json.dumps(d, indent=2, allow_nan=False) + "\n")

def assert_population(p):
    assert not p.athlete_id.duplicated().any()
    assert np.isfinite(p[["ppm","ability"]].to_numpy()).all()
    assert abs(p.ability.mean()) < 1e-10
    assert abs(p.ability.std(ddof=0)-1) < 1e-10
    assert p.groupby("team_id").size().min() >= 2
    assert (p.minutes >= CFG["minimum_player_minutes"]).all()

def prepare():
    if DATA.exists():
        raise RuntimeError("Prepared population already exists; refusing overwrite")
    DATA.mkdir(parents=True)
    source_before = sha(SOURCE)
    pre = json.loads(PREFLIGHT.read_text())
    assert source_before == pre["source_sha256_after"]
    parts = []
    offset = 0
    cols = ["season","game_id","athlete_id","team_id","athlete_display_name","minutes","points","did_not_play"]
    for ch in pd.read_csv(SOURCE, usecols=cols, chunksize=200000, low_memory=False):
        mask = pd.to_numeric(ch.season, errors="coerce").isin([2014,2016])
        x = ch.loc[mask].copy()
        x["source_data_row"] = np.flatnonzero(mask.to_numpy()) + offset + 1
        parts.append(x)
        offset += len(ch)
    raw = pd.concat(parts, ignore_index=True)
    audits = []
    for year in [2014,2016]:
        b = raw.loc[pd.to_numeric(raw.season).eq(year)].copy()
        for col in ["game_id","athlete_id","team_id","minutes","points"]:
            b[col] = pd.to_numeric(b[col], errors="coerce")
        blank = b.athlete_id.isna() & b.athlete_display_name.isna()
        b = b.loc[~blank & b.athlete_display_name.astype(str).str.strip().ne("-")].copy()
        assert b[["game_id","athlete_id","team_id"]].notna().all().all()
        for col in ["game_id","athlete_id","team_id"]:
            assert (b[col].mod(1) == 0).all()
            b[col] = b[col].astype(np.int64)
        games = b.groupby("team_id").game_id.nunique()
        b = b.loc[b.team_id.isin(games.index[games >= CFG["minimum_captured_games"]])].copy()
        partial = b.minutes.isna() ^ b.points.isna()
        zero_positive = b.minutes.eq(0) & b.points.gt(0)
        both = b.minutes.isna() & b.points.isna()
        assert not (both & ~b.did_not_play.astype(str).str.lower().eq("true")).any()
        assert not (b.minutes.lt(0) | b.points.lt(0)).any()
        assert not b.duplicated(["game_id","athlete_id","team_id"]).any()
        bad = partial | zero_positive
        expected = 111 if year == 2014 else 100
        assert int(bad.sum()) == expected
        b["omitted_stats"] = bad
        b["omitted_points"] = b.points.where(bad, 0).fillna(0)
        b.loc[bad].to_csv(DATA / f"{year}_omitted_source_rows.csv", index=False)
        b.loc[bad, ["minutes","points"]] = 0.0
        b[["minutes","points"]] = b[["minutes","points"]].fillna(0.0)
        b["played_game"] = b.game_id.where(b.minutes.gt(0))
        candidates = b.groupby(["athlete_id","team_id"], as_index=False).agg(
            played_games=("played_game","nunique"),minutes=("minutes","sum"),
            captured_games=("game_id","nunique"))
        candidates = candidates.loc[candidates.groupby("athlete_id").minutes.transform("max").gt(0)].copy()
        chosen = candidates.sort_values(["athlete_id","played_games","minutes"],
                    ascending=[True,False,False],kind="stable").drop_duplicates("athlete_id")
        tied = candidates.merge(chosen[["athlete_id","played_games","minutes"]],
                               on=["athlete_id","played_games","minutes"])
        if tied.athlete_id.duplicated().any():
            tied.to_csv(DATA / f"{year}_unresolved_team_ties.csv",index=False)
            raise RuntimeError("Ambiguous canonical team; stop")
        candidates = candidates.merge(chosen[["athlete_id","team_id"]].rename(columns={"team_id":"chosen_team"}),on="athlete_id")
        candidates.to_csv(DATA / f"{year}_canonical_team_candidates.csv",index=False)
        b = b.merge(chosen[["athlete_id","team_id"]],on=["athlete_id","team_id"],validate="many_to_one")
        assert not b.duplicated(["game_id","athlete_id"]).any()
        p = b.groupby(["athlete_id","team_id"],as_index=False).agg(
            name=("athlete_display_name","last"),minutes=("minutes","sum"),points=("points","sum"),
            played_games=("played_game","nunique"),omitted_rows=("omitted_stats","sum"),
            omitted_points=("omitted_points","sum"))
        before = len(p)
        p = p.loc[p.minutes >= CFG["minimum_player_minutes"]].sort_values("athlete_id").reset_index(drop=True)
        p["season"] = year
        p["ppm"] = p.points / p.minutes
        p["ability"] = (p.ppm-p.ppm.mean())/p.ppm.std(ddof=0)
        assert_population(p)
        p.to_csv(DATA / f"{year}_players.csv.gz",index=False)
        audit = {"season":year,"N":len(p),"teams":int(p.team_id.nunique()),
                 "fallback_rows_after_coverage":int(bad.sum()),
                 "fallback_rows_on_final_players":int(p.omitted_rows.sum()),
                 "final_players_affected":int(p.omitted_rows.gt(0).sum()),
                 "points_omitted_on_final_players":float(p.omitted_points.sum()),
                 "positive_playing_athletes_before_20_minute_floor":before,
                 "K":math.floor(CFG["selection_fraction"]*len(p)+0.5),
                 "minimum_roster":int(p.groupby("team_id").size().min()),
                 "ppm_mean":float(p.ppm.mean()),"ppm_population_sd":float(p.ppm.std(ddof=0))}
        audits.append(audit)
        print("PREPARED",json.dumps(audit),flush=True)
    old = json.loads(RECORD2015.read_text())
    expected = next(x["sha256"] for x in old["outputs"] if x["path"].endswith(INPUT2015.name))
    assert sha(INPUT2015) == expected
    p = pd.read_csv(INPUT2015).rename(columns={"ability_standardized":"ability", "points_per_minute":"ppm"})
    assert len(p) == 4267
    assert_population(p)
    p.sort_values("athlete_id").to_csv(DATA / "2015_players.csv.gz",index=False)
    audits.append({"season":2015,"N":len(p),"teams":int(p.team_id.nunique()),
                   "K":math.floor(CFG["selection_fraction"]*len(p)+0.5),
                   "input":"accepted rotation audit freeze, copied without recalculating values",
                   "input_sha256":expected,"minimum_roster":int(p.groupby("team_id").size().min())})
    for year in CFG["seasons"]:
        p = pd.read_csv(DATA / f"{year}_players.csv.gz")
        p.groupby("team_id").size().rename("capacity").to_csv(DATA / f"{year}_capacities.csv")
    after = sha(SOURCE)
    assert after == source_before
    write_json(DATA / "manifest.json",{"source_sha256":after,"settings_sha256":sha(SETTINGS),
        "driver_sha256_at_preparation":sha(HERE),"preflight_sha256":sha(PREFLIGHT),
        "population_2015_record_sha256":sha(RECORD2015),
        "populations":sorted(audits,key=lambda a:a["season"]),
        "files":{p.name:sha(p) for p in sorted(DATA.glob("*")) if p.is_file()}})
    print("PREPARATION COMPLETE; no assignment simulation yet.",flush=True)

class PairedChoices:
    def __init__(self, order, uniforms):
        self.order,self.uniforms,self.cursor=order,uniforms,0
        self.permutations=0
    def permutation(self,n):
        assert n == len(self.order) and self.permutations == 0
        self.permutations += 1
        return self.order.copy()
    def choice(self,n,p):
        assert len(p)==n and self.cursor < len(self.uniforms)
        assert np.isclose(np.sum(p),1) and np.all(p>=0)
        cdf=np.cumsum(p)
        # Pin only the roundoff endpoint; all interior probabilities unchanged.
        cdf[-1]=1.0
        j=int(np.searchsorted(cdf,self.uniforms[self.cursor],side="right"))
        self.cursor+=1
        assert 0 <= j < n
        return j

def winners(score,ids,k):
    mask=np.zeros(len(score),dtype=bool)
    mask[np.lexsort((ids,-score))[:k]]=True
    assert mask.sum()==k
    return mask

def simulate():
    manifest=json.loads((DATA/"manifest.json").read_text())
    assert sha(SETTINGS)==manifest["settings_sha256"]
    for name,h in manifest["files"].items():
        assert sha(DATA/name)==h
    if RECORD.exists():
        raise RuntimeError("Completed run exists; refusing overwrite")
    OUT.mkdir(parents=True,exist_ok=True)
    sources=[HERE,SETTINGS,METHOD,PREFLIGHT,DATA/"manifest.json",INPUT2015,RECORD2015]
    hashes={str(p.relative_to(REPO)):sha(p) for p in sources}
    config_record=OUT/"execution_inputs.json"
    if config_record.exists():
        assert json.loads(config_record.read_text())==hashes, "Resume inputs changed"
    else:
        write_json(config_record,hashes)
    sys.path.insert(0,str(METHOD.parent))
    gc=importlib.import_module("541_grandchild_homophily_assign")
    metrics=[]; curves=[]; seeds=[]
    start=time.monotonic()
    for year in CFG["seasons"]:
        p=pd.read_csv(DATA/f"{year}_players.csv.gz").sort_values("athlete_id")
        A=p.ability.to_numpy(float); ids=p.athlete_id.to_numpy(np.int64)
        caps=p.groupby("team_id",sort=True).size().to_numpy(np.int64)
        n=len(p); k=math.floor(n*CFG["selection_fraction"]+0.5)
        theta=float(np.quantile(A,CFG["theta_quantile"],method="linear"))
        t=CFG["gamma"]*(A-theta)
        viability=np.exp(-np.logaddexp(0,-t))
        baseline=winners(A,ids,k)
        yearout=OUT/str(year); yearout.mkdir(exist_ok=True)
        for rep in range(CFG["repetitions"]):
            seed=int(np.random.SeedSequence([CFG["master_seed"],year,rep]).generate_state(1,dtype=np.uint64)[0])
            seeds.append({"season":year,"repetition":rep+1,"seed":seed})
            checkpoint=yearout/f"pair_{rep+1:03d}.npz"
            if not checkpoint.exists():
                rng=np.random.default_rng(seed); order=rng.permutation(n); uniforms=rng.random(n)
                pools=[]; peers=[]; congestions=[]; labels=[]; selections=[]; sorting=[]
                for rho in CFG["rho"]:
                    stream=PairedChoices(order,uniforms)
                    pool,means=gc.grandchild_assign(stream,A,roster_caps=caps,rho=float(rho))
                    assert stream.cursor==n and stream.permutations==1
                    counts=np.bincount(pool,minlength=len(caps))
                    assert np.array_equal(counts,caps)
                    sums=np.bincount(pool,weights=A,minlength=len(caps))
                    C=np.bincount(pool,weights=viability,minlength=len(caps))/counts
                    peer=(sums[pool]-A)/(counts[pool]-1)
                    lab=np.empty(n,dtype=np.int8)
                    lab[np.lexsort((ids,peer))]=(np.arange(n)*CFG["bins"]//n).astype(np.int8)
                    selected=np.array([winners(A-lam*C[pool],ids,k) for lam in CFG["lambda"]])
                    assert np.array_equal(selected[0],baseline)
                    h=float(np.sum(counts*(sums/counts-A.mean())**2)/np.sum((A-A.mean())**2))
                    pools.append(pool); peers.append(peer); congestions.append(C[pool])
                    labels.append(lab); selections.append(selected); sorting.append(h)
                temp=checkpoint.with_suffix(".tmp")
                with temp.open("wb") as f:
                    np.savez_compressed(f,pool=np.array(pools,dtype=np.int16),peer=np.array(peers),
                        congestion=np.array(congestions),bins=np.array(labels),selected=np.array(selections),
                        h_sort=np.array(sorting),theta=theta,K=k,seed=np.uint64(seed))
                    f.flush(); os.fsync(f.fileno())
                temp.replace(checkpoint)
            with np.load(checkpoint) as z:
                assert int(z["seed"])==seed and int(z["K"])==k
                for ri,rho in enumerate(CFG["rho"]):
                    off,on=z["selected"][ri]
                    displaced=int(np.count_nonzero(off & ~on))
                    metrics.append({"season":year,"repetition":rep+1,"rho":rho,"N":n,"K":k,
                        "displaced":displaced,"displaced_fraction":displaced/k,
                        "h_sort":float(z["h_sort"][ri]),"theta":theta})
                    for li,lam in enumerate(CFG["lambda"]):
                        for b in range(CFG["bins"]):
                            ix=z["bins"][ri]==b
                            curves.append({"season":year,"repetition":rep+1,"rho":rho,"lambda":lam,
                                "bin":b+1,"n_players":int(ix.sum()),"n_selected":int(z["selected"][ri,li,ix].sum()),
                                "mean_peer":float(z["peer"][ri,ix].mean()),
                                "selection_rate":float(z["selected"][ri,li,ix].mean())})
            if (rep+1)%20==0 or rep==0:
                print(f"SIMULATION {year}: {rep+1}/100 pairs; elapsed {time.monotonic()-start:.1f}s",flush=True)
    m=pd.DataFrame(metrics); c=pd.DataFrame(curves)
    m.to_csv(OUT/"repetition_metrics.csv",index=False); c.to_csv(OUT/"curve_bins.csv",index=False)
    write_json(OUT/"repetition_seeds.json",seeds)
    summary=[]
    for (year,rho),g in m.groupby(["season","rho"]):
        summary.append({"season":int(year),"rho":int(rho),"N":int(g.N.iloc[0]),"K":int(g.K.iloc[0]),
            "displaced_mean":float(g.displaced.mean()),"displaced_median":float(g.displaced.median()),
            "displaced_min":int(g.displaced.min()),"displaced_max":int(g.displaced.max()),
            "displaced_p025":float(g.displaced.quantile(.025)),"displaced_p975":float(g.displaced.quantile(.975)),
            "any_displacement_fraction":float(g.displaced.gt(0).mean()),
            "h_sort_mean":float(g.h_sort.mean()),"h_sort_min":float(g.h_sort.min()),"h_sort_max":float(g.h_sort.max())})
    write_json(OUT/"summary.json",summary)
    means=c.groupby(["season","rho","lambda","bin"]).agg(
        mean_rate=("selection_rate","mean"),low=("selection_rate",lambda s:s.quantile(.025)),
        high=("selection_rate",lambda s:s.quantile(.975)),mean_peer=("mean_peer","mean")).reset_index()
    means.to_csv(OUT/"curve_summary.csv",index=False)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(3,2,figsize=(12,11),sharex=True,sharey=True)
    colors=["#52657b","#b74b12"]
    for row,year in enumerate(CFG["seasons"]):
        for col,rho in enumerate(CFG["rho"]):
            ax=axes[row,col]
            for li,lam in enumerate(CFG["lambda"]):
                g=means.loc[(means.season==year)&(means.rho==rho)&(means["lambda"]==lam)]
                x=g["bin"].to_numpy()
                ax.plot(x,100*g.mean_rate,color=colors[li],lw=2,label=["Congestion off","Congestion on"][li])
                ax.fill_between(x,100*g.low,100*g.high,color=colors[li],alpha=.10)
            n=int(m.loc[m.season.eq(year),"N"].iloc[0]); k=int(m.loc[m.season.eq(year),"K"].iloc[0])
            ax.axhline(100*k/n,color="gray",ls=":",lw=1)
            ax.set_title(f"{year} | "+("No similarity preference" if rho==0 else "Similarity preference")+" | "+f"N={n:,}, K={k}")
            ax.set_xticks([1,4,8,12,16]); ax.grid(alpha=.2)
            if col==0: ax.set_ylabel("Selected players (%)")
            if row==2: ax.set_xlabel("Peer-quality bin (low to high; equal player counts)")
    axes[0,0].legend(loc="upper left")
    fig.suptitle("Does congestion change the selection pattern?\nSame players within each season; 100 paired assignments; raw congestion",fontsize=15)
    fig.text(.5,.025,"Lines: mean across assignments. Shading: central 95% assignment range, not a confidence interval.\nBins rank leave-one-out teammate PPM within each assignment; they are not fixed numerical environments.\nDotted line: overall selected fraction. These are simulated selections, not observed draft outcomes.",ha="center",fontsize=10)
    fig.tight_layout(rect=[0,.085,1,.94])
    fig.savefig(OUT/"selection_curves.png",dpi=160); plt.close(fig)
    assert all(sha(REPO/p)==h for p,h in hashes.items())
    assert sha(SOURCE)==manifest["source_sha256"]
    write_json(RECORD,{"experiment_id":STEM,"status":"executed_pending_independent_review",
        "completed_utc":datetime.now(timezone.utc).isoformat(),"settings":CFG,
        "input_method_hashes":hashes,"raw_source_sha256_verified":manifest["source_sha256"],
        "numpy":np.__version__,"pandas":pd.__version__,"python":sys.version,
        "checks":["exact labeled capacities","one player per assignment","coupled order and uniforms",
                  "exact K","same ability-only winners","unchanged source/method hashes"],
        "output_hashes":{str(p.relative_to(WORK)):sha(p) for p in sorted(OUT.rglob("*")) if p.is_file()},
        "prepared_input_hashes":manifest["files"],"pairs":len(seeds),"assignment_runs":2*len(seeds)})
    print("SIMULATION COMPLETE",json.dumps(summary),flush=True)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--prepare",action="store_true")
    group.add_argument("--simulate",action="store_true")
    args=parser.parse_args()
    prepare() if args.prepare else simulate()
