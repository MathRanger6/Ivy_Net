#!/usr/bin/env python3
"""Independent read-only reconstruction of saved three-season results.
Does not import the experiment driver or rerun assignment.
Writes a new verification record only.
"""
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd

HERE=Path(__file__).resolve()
WORK=HERE.parents[2]
REPO=WORK.parents[3]
OUT=WORK/"outputs/three_season_mechanism_v1"
DATA=WORK/"data/three_season_mechanism_v1/prepared"
STEM="ASSORT_20260927_three_season_mechanism_v1"
RECORD=WORK/"docs/run_records"/(STEM+"_run_record.json")
DEST=WORK/"docs/run_records"/(STEM+"_independent_review.json")

def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(2**20),b""): h.update(b)
    return h.hexdigest()

def main():
    if DEST.exists(): raise RuntimeError("Verification record exists")
    r=json.loads(RECORD.read_text())
    cfg=r["settings"]
    for path,h in r["input_method_hashes"].items(): assert sha(REPO/path)==h
    for path,h in r["output_hashes"].items(): assert sha(WORK/path)==h
    for name,h in r["prepared_input_hashes"].items(): assert sha(DATA/name)==h
    metrics=pd.read_csv(OUT/"repetition_metrics.csv")
    curves=pd.read_csv(OUT/"curve_bins.csv")
    seeds=json.loads((OUT/"repetition_seeds.json").read_text())
    assert len({x["seed"] for x in seeds})==300
    assert len(metrics)==600 and len(curves)==19200
    nchecks=0
    for year in cfg["seasons"]:
        p=pd.read_csv(DATA/f"{year}_players.csv.gz").sort_values("athlete_id").reset_index(drop=True)
        assert p.athlete_id.is_unique
        A=p.ability.to_numpy(); ids=p.athlete_id.to_numpy()
        caps=p.groupby("team_id").size().to_numpy()
        theta=np.quantile(A,.99)
        v=1/(1+np.exp(-10*(A-theta)))
        k=int(np.floor(.027*len(p)+.5))
        for rep in range(1,101):
            with np.load(OUT/str(year)/f"pair_{rep:03d}.npz") as z:
                assert int(z["K"])==k and abs(float(z["theta"])-theta)<1e-12
                for ri,rho in enumerate([0,1]):
                    frame=pd.DataFrame({"ability":A,"pool":z["pool"][ri],"v":v,"id":ids})
                    assert np.array_equal(frame.groupby("pool").size().to_numpy(),caps)
                    expected_c=frame.groupby("pool").v.transform("mean").to_numpy()
                    expected_peer=(frame.groupby("pool").ability.transform("sum")-A)/(frame.groupby("pool").ability.transform("size")-1)
                    np.testing.assert_allclose(expected_c,z["congestion"][ri],atol=1e-12)
                    np.testing.assert_allclose(expected_peer,z["peer"][ri],atol=1e-12)
                    bins=np.empty(len(p),dtype=int)
                    idx=frame.assign(peer=expected_peer).sort_values(["peer","id"]).index.to_numpy()
                    bins[idx]=np.arange(len(p))*16//len(p)
                    assert np.array_equal(bins,z["bins"][ri])
                    for li,lam in enumerate([0,1]):
                        scores=frame.assign(score=A-lam*expected_c).sort_values(["score","id"],ascending=[False,True])
                        selected=np.zeros(len(p),dtype=bool); selected[scores.index[:k]]=True
                        assert np.array_equal(selected,z["selected"][ri,li])
                        saved=curves.loc[(curves.season==year)&(curves.repetition==rep)&(curves.rho==rho)&(curves["lambda"]==lam)].sort_values("bin")
                        assert saved.n_players.sum()==len(p) and saved.n_selected.sum()==k
                        assert np.array_equal(np.bincount(bins,weights=selected,minlength=16),saved.n_selected)
                    total=np.sum((A-A.mean())**2)
                    between=sum(len(g)*(g.ability.mean()-A.mean())**2 for _,g in frame.groupby("pool"))
                    assert abs(between/total-z["h_sort"][ri])<1e-12
                    m=metrics.loc[(metrics.season==year)&(metrics.repetition==rep)&(metrics.rho==rho)].iloc[0]
                    assert int(m.displaced)==np.count_nonzero(z["selected"][ri,0]&~z["selected"][ri,1])
                    nchecks+=1
    original=pd.read_csv(WORK/"outputs/rotation_audit_2015/ASSORT_20260927_rotation_audit_v1_players.csv.gz").sort_values("athlete_id")
    current=pd.read_csv(DATA/"2015_players.csv.gz").sort_values("athlete_id")
    assert np.array_equal(original.athlete_id,current.athlete_id)
    np.testing.assert_allclose(original.points_per_minute,current.ppm,rtol=0,atol=0)
    np.testing.assert_allclose(original.ability_standardized,current.ability,rtol=0,atol=0)
    answer={"status":"passed","assignment_conditions_checked":nchecks,
            "selection_conditions_checked":2*nchecks,"checkpoint_pairs":300,
            "curve_rows_checked":len(curves),"unchanged_2015_values":True,
            "all_recorded_input_and_output_hashes_matched":True,
            "verification_script_sha256":sha(HERE),
            "checks":"Reconstructed congestion, peer means, bins, winners, displacement and variance-ratio sorting from saved rosters using separate pandas calculations. No assignment rerun.",
            "figure_review":"performed separately by VECTOR; not asserted by this script"}
    DEST.write_text(json.dumps(answer,indent=2)+"\n")
    print(json.dumps(answer))
if __name__=="__main__": main()

