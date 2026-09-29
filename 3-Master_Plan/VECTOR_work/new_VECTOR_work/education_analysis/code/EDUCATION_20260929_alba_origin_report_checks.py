"""Compare all 168 source-coded Alba origin reports with county candidate records.
Bounded to 12 minutes and the observed source directory; no inferred URLs for
candidate reports. Placement companion stems are the source's verified pattern.
Names remain in memory. Each school result is flushed, and completed schools
are skipped on resume. No cross-school identity reconstruction.
"""
import argparse, collections, importlib.util, json, time
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("alba",Path(__file__).with_name("EDUCATION_20260929_alba_2001_structural_audit.py"))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
OUT=m.OUT;LOG=OUT/"origin_report_checks.jsonl"
def save(x):
    with LOG.open("a") as f:f.write(json.dumps(x,ensure_ascii=False)+"\n");f.flush()
    print(json.dumps({k:x[k] for k in ["source_code","status","candidate_rows","county_label_rows","candidate_extra_to_county","county_missing_from_school","placement_exact_matches"] if k in x},ensure_ascii=False),flush=True)
def main(policy_reviewed=False):
    if (OUT/"origin_report_check_summary.json").exists():
        print("Completed source-directory checkpoint exists; no rerun.");return
    prior=[json.loads(x) for x in LOG.read_text().splitlines()] if LOG.exists() else []
    latest={x["source_code"]:x for x in prior}
    done={code for code,x in latest.items() if x["status"]=="candidate_report_recovered"
          and not x.get("placement_report_unavailable",False)}
    directory=json.loads((OUT/"origin_school_directory.json").read_text())
    m.configure_retrieval(policy_reviewed)
    county=[]
    for idx in [1,501,1001,1501,2001,2501]:
        x=m.fetch(f"raport_candidati_total.asp-cj=AB&nj=ALBA&idx={idx}.htm","school_check_county_reference")
        if x is None:raise RuntimeError("County reference unavailable")
        county.extend(x[1])
    school_names=collections.Counter(x["name"] for x in directory)
    started=time.monotonic(); consecutive_failures=0
    for pos,d in enumerate(directory,1):
        if d["code"] in done:continue
        if time.monotonic()-started>720:
            print("12-minute source-check bound reached; preserved completed schools.",flush=True);break
        ref=[r for r in county if m.origin_parts(m.school_label(r))==(d["name"],"AB")]
        # Shared client paces every request, including companion reports and redirects.
        x=m.fetch(d["candidate_report"],"origin_candidates_"+d["code"])
        if x is None:
            save({"source_code":d["code"],"status":"candidate_report_unverified_retrieval_failure","county_label_rows":len(ref)})
            consecutive_failures+=1
            if consecutive_failures>=3:
                print("Stopped after three consecutive retrieval failures; no inference of source absence.",flush=True)
                break
            continue
        consecutive_failures=0
        rr=x[1]
        # The school roster's explicit source code supplies origin, not the person's destination.
        cn=collections.defaultdict(list);sn=collections.defaultdict(list)
        for r in ref:cn[r["Nume"]].append(r)
        for r in rr:sn[r["Nume"]].append(r)
        shared={n for n in cn.keys()&sn.keys() if len(cn[n])==len(sn[n])==1}
        fields=["admitere","capacitate","absolvire"]
        mismatch={f:sum(m.col(cn[n][0],f)!=m.col(sn[n][0],f) for n in shared) for f in fields}
        result={"source_code":d["code"],"school_name":d["name"],"status":"candidate_report_recovered",
          "candidate_rows":len(rr),"candidate_unique_names":len(sn),
          "county_label_rows":len(ref),"directory_same_name_codes":school_names[d["name"]],
          "exact_unique_names_shared":len(shared),"candidate_extra_to_county":len(sn.keys()-cn.keys()),
          "county_missing_from_school":len(cn.keys()-sn.keys()),"shared_component_disagreements":mismatch,
          "source_page":x[3],"applicant_county_column_counts":dict(collections.Counter(m.col(r,"Judeţ") for r in rr)),
          "full_graduating_cohort_denominator":"unavailable"}
        # Companion placement needed when roster adds people or a duplicate label needs resolution.
        # Also validate first coded school, preserving previous 78-row comparison independently.
        if result["candidate_extra_to_county"] or school_names[d["name"]]>1 or d["code"]=="101":
            target=d["candidate_report"].replace("raport_candidati_per_scoala","raport_total_per_scoala",1)
            y=m.fetch(target,"origin_placement_"+d["code"])
            if y is not None:
                pn=collections.defaultdict(list)
                for r in y[1]:pn[r["Nume"]].append(r)
                common={n for n in sn.keys()&pn.keys() if len(sn[n])==len(pn[n])==1}
                extras=(sn.keys()-cn.keys())&common
                result.update({"placement_rows":len(y[1]),"placement_exact_matches":len(common),
                  "placement_unmatched_candidate_names":len(sn.keys()-common),
                  "placement_composite_disagreements":sum(m.col(sn[n][0],"admitere")!=m.col(pn[n][0],"admitere") for n in common),
                  "extra_names_with_placement_rows":len(extras),
                  "extra_placement_descriptions":dict(collections.Counter(m.col(pn[n][0],"Liceu")+" | "+m.col(pn[n][0],"Specializare") for n in extras)),
                  "placement_page":y[3]})
            else:result["placement_report_unavailable"]=True
        save(result)
    write_summary()

def write_summary(stopped_reason=None):
    if not LOG.exists():return
    directory=json.loads((OUT/"origin_school_directory.json").read_text())
    latest={}
    for line in LOG.read_text().splitlines():
        x=json.loads(line); latest[x["source_code"]]=x
    results=list(latest.values())
    complete=(len(results)==len(directory) and all(x["status"]=="candidate_report_recovered"
              and not x.get("placement_report_unavailable",False) for x in results))
    summary={"directory_codes":len(directory),"attempted_codes":len(results),"directory_pass_finished":complete,
        "recovered_candidate_reports":sum(x["status"]=="candidate_report_recovered" for x in results),
        "unverified_candidate_reports":sum(x["status"]!="candidate_report_recovered" for x in results),
        "stopped_reason":stopped_reason,
        "candidate_rows_across_reports_not_deduplicated":sum(x.get("candidate_rows",0) for x in results),
        "codes_with_added_names_vs_county_label":sum(x.get("candidate_extra_to_county",0)>0 for x in results),
        "added_name_occurrences_not_unique_students":sum(x.get("candidate_extra_to_county",0) for x in results),
        "codes_with_component_disagreements":sum(any(x.get("shared_component_disagreements",{}).values()) for x in results),
        "codes_with_county_names_missing_from_school":sum(x.get("county_missing_from_school",0)>0 for x in results),
        "caution":"A school-name collision can make county-label reference contain multiple source codes. Counts across school reports are not assumed disjoint."}
    (OUT/("origin_report_check_summary.json" if complete else "origin_report_check_partial_summary.json")).write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(summary,ensure_ascii=False),flush=True)
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--run",action="store_true")
    p.add_argument("--policy-reviewed",action="store_true",
                   help="Use only after reviewing the archive's published crawling guidance.")
    args=p.parse_args()
    if args.run:
        try:main(args.policy_reviewed)
        except (m.RetrievalStopped,KeyboardInterrupt) as error:
            reason=str(error) or "Interrupted by user"
            m.emit({"kind":"stopped","reason":reason})
            write_summary(reason)
            raise SystemExit(2)
    else:p.print_help()
