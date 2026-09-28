import argparse,importlib,importlib.util,hashlib,json,math,sys,time
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve();W=HERE.parents[2];R=W.parents[3];O=W/"outputs/rho005_v1"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--run",action="store_true")
 if not ap.parse_args().run:ap.error("--run required")
 if O.exists():raise RuntimeError("Refusing overwrite")
 O.mkdir(parents=True);start=time.monotonic()
 helper=W/"code/three_season_mechanism_v1/ASSORT_20260927_three_season_mechanism_v1.py"
 spec=importlib.util.spec_from_file_location("prior_mechanism",helper);h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
 sys.path.insert(0,str(R/"sports"));gc=importlib.import_module("541_grandchild_homophily_assign")
 method=R/"sports/541_grandchild_homophily_assign.py"
 original=json.loads((W/"outputs/three_season_mechanism_v1/execution_inputs.json").read_text())
 assert sha(method)==original[str(method.relative_to(R))]
 parentpath=W/"docs/run_records/ASSORT_20260927_penalty_bars_v1_run_record.json"
 parent=json.loads(parentpath.read_text());inputs={str(HERE):sha(HERE),str(helper):sha(helper),str(method):sha(method),str(parentpath):sha(parentpath)}
 for rel,digest in parent["input_hashes"].items():
  assert sha(W/rel)==digest;inputs[str(W/rel)]=digest
 rows=[];metrics=[];edgeinfo={}
 for year in [2014,2015,2016]:
  p=pd.read_csv(W/f"data/three_season_mechanism_v1/prepared/{year}_players.csv.gz").sort_values("athlete_id")
  A=p.ability.to_numpy();ids=p.athlete_id.to_numpy();caps=p.groupby("team_id",sort=True).size().to_numpy();n=len(A);k=math.floor(.5*n+.5)
  v=np.exp(-np.logaddexp(0,-10*(A-np.quantile(A,.99))))
  oldpath=W/f"outputs/penalty_bars_v1/{year}_selections_and_bins.npz"
  assert sha(oldpath)==parent["output_hashes"][str(oldpath.relative_to(W))];inputs[str(oldpath)]=sha(oldpath)
  with np.load(oldpath) as z:oldedges=z["ew_edges"].copy()
  pools=[];peers=[];cons=[];quants=[];masks=[]
  for rep in range(100):
   seed=int(np.random.SeedSequence([20260925,year,rep]).generate_state(1,dtype=np.uint64)[0])
   rng=np.random.default_rng(seed);order=rng.permutation(n);uniforms=rng.random(n)
   oldf=W/f"outputs/three_season_mechanism_v1/{year}/pair_{rep+1:03d}.npz"
   with np.load(oldf) as z:
    assert int(z["seed"])==seed
    oldpool=z["pool"][1].copy();oldpeer=z["peer"][1].copy();oldC=z["congestion"][1].copy();oldq=z["bins"][1].copy()
   if rep==0:
    check,_=gc.grandchild_assign(h.PairedChoices(order,uniforms),A,roster_caps=caps,rho=1.)
    assert np.array_equal(check,oldpool)
   stream=h.PairedChoices(order,uniforms)
   pool,_=gc.grandchild_assign(stream,A,roster_caps=caps,rho=.05)
   assert stream.cursor==n and stream.permutations==1
   counts=np.bincount(pool,minlength=len(caps));assert np.array_equal(counts,caps)
   sums=np.bincount(pool,weights=A,minlength=len(caps))
   C=(np.bincount(pool,weights=v,minlength=len(caps))/counts)[pool]
   peer=(sums[pool]-A)/(counts[pool]-1)
   q=np.empty(n,dtype=np.int8);q[np.lexsort((ids,peer))]=np.arange(n)*16//n
   selected=[]
   for rho,pp,cc,pl in [(1.,oldpeer,oldC,oldpool),(.05,peer,C,pool)]:
    score=A-4*cc;order2=np.lexsort((ids,-score));m=np.zeros(n,bool);m[order2[:k]]=True
    check=pd.DataFrame({"s":score,"id":ids}).sort_values(["s","id"],ascending=[False,True]).index[:k]
    assert set(check)==set(np.flatnonzero(m));selected.append(m)
    sizes=np.bincount(pl);sm=np.bincount(pl,weights=A)
    hs=float(np.sum(sizes*(sm/sizes-A.mean())**2)/np.sum((A-A.mean())**2))
    metrics.append(dict(season=year,repetition=rep+1,rho=rho,h_sort=hs,K=k,N=n,seed=seed))
   pools.append([oldpool,pool]);peers.append([oldpeer,peer]);cons.append([oldC,C]);quants.append([oldq,q]);masks.append(selected)
   if (rep+1)%25==0:print(f"ASSIGNMENT {year}: {rep+1}/100 completed; {time.monotonic()-start:.1f}s",flush=True)
  peers=np.array(peers);quants=np.array(quants);masks=np.array(masks)
  # Keep the prior EW edges if they cover both conditions; otherwise expand jointly, never clip.
  expanded=bool(peers.min()<oldedges[0] or peers.max()>oldedges[-1])
  edges=np.linspace(min(oldedges[0],peers.min()),max(oldedges[-1],peers.max()),17) if expanded else oldedges
  ew=np.minimum(np.searchsorted(edges,peers,side="right")-1,15);assert ew.min()>=0 and ew.max()<=15
  edgeinfo[str(year)]={"expanded":expanded,"edges":edges.tolist()}
  np.savez_compressed(O/f"{year}_paired_assignments.npz",pool=np.array(pools),peer=peers,congestion=np.array(cons),quantile_bins=quants,ew_bins=ew,ew_edges=edges,selected=masks,athlete_id=ids,rhos=[1,.05])
  for rep in range(100):
   for ri,rho in enumerate([1.,.05]):
    for name,bins in [("EW",ew),("Quantile",quants)]:
     ns=np.bincount(bins[rep,ri],minlength=16);ks=np.bincount(bins[rep,ri,masks[rep,ri]],minlength=16)
     assert ns.sum()==n and ks.sum()==k
     for bi in range(16):rows.append(dict(season=year,repetition=rep+1,rho=rho,method=name,bin=bi+1,players=int(ns[bi]),selected=int(ks[bi])))
  pd.DataFrame(rows).to_csv(O/"counts_by_repetition.csv",index=False)
 s=pd.DataFrame(rows).groupby(["season","rho","method","bin"]).agg(players=("players","sum"),selected=("selected","sum"),mean_players=("players","mean"),occupied=("players",lambda x:int((x>0).sum()))).reset_index()
 s["rate"]=s.selected/s.players.replace(0,np.nan);s.to_csv(O/"bar_summary.csv",index=False)
 mt=pd.DataFrame(metrics);mt.to_csv(O/"assignment_metrics.csv",index=False)
 summary=mt.groupby(["season","rho"]).h_sort.agg(["mean","min","max"]);summary.to_csv(O/"sorting_summary.csv")
 (O/"ew_edges.json").write_text(json.dumps(edgeinfo,indent=2))
 for year in [2014,2015,2016]:
  fig,axs=plt.subplots(4,2,figsize=(12,10),gridspec_kw={"height_ratios":[1,1,.65,.65]})
  for col,methodname in enumerate(["EW","Quantile"]):
   for row,(rho,color) in enumerate([(1.,"#a23e4a"),(.05,"#277c83")]):
    g=s.loc[(s.season==year)&(s.rho==rho)&(s.method==methodname)].sort_values("bin")
    ax=axs[row,col];ax.bar(g.bin,100*g.rate,color=color)
    for x,tot in zip(g.bin,g.players):
     if tot==0:ax.text(x,2,"×",ha="center",color="gray")
    ax.set_ylim(0,100);ax.axhline(50,ls=":",color="gray");ax.set_ylabel("Selected (%)");ax.set_title(f"{methodname} | rho = {rho:g}");ax.set_xticks([1,4,8,12,16]);ax.grid(axis="y",alpha=.15)
    ax=axs[row+2,col];ax.bar(g.bin,g.mean_players,color=color,alpha=.6);ax.set_title(f"Mean players / assignment | rho = {rho:g}");ax.set_xticks([1,4,8,12,16])
   axs[3,col].set_xlabel("Peer-quality bin (low to high)")
  fig.suptitle(f"{year}: change assignment preference only | 50% selection, lambda = 4",fontsize=15)
  fig.text(.5,.012,"100 paired assignments. EW edges shared between rho settings; quantile bins compare relative ranks.\n× means no players, NOT zero selection. Sparse tails require caution. Player counts change with assignment.",ha="center",fontsize=9)
  fig.tight_layout(rect=[0,.06,1,.95]);fig.savefig(O/f"{year}_rho_comparison.png",dpi=140);plt.close(fig)
 assert all(sha(Path(p))==digest for p,digest in inputs.items())
 record=dict(status="executed_checked",completed_utc=datetime.now(timezone.utc).isoformat(),python=sys.executable,
 checks=["source hashes verified","rho1 first assignment exactly reconstructed per season","matched random order and uniforms","exact team capacities","independent selection rankings agree","all bins conserve counts","source hashes unchanged"],
 input_hashes=inputs,output_hashes={str(p.relative_to(W)):sha(p) for p in O.iterdir() if p.is_file()})
 (W/"docs/run_records/ASSORT_20260927_rho005_v1_run_record.json").write_text(json.dumps(record,indent=2))
 print("COMPLETE\n"+summary.to_string(),flush=True)
if __name__=="__main__":main()

