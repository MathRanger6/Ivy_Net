"""Bounded Alba 2001 source audit. No sorting or outcome estimates.
Student names are used in memory for exact correspondence only, never persisted.
A full rerun refetches pages because identifiable HTML is not cached.
Successful final output is a resume gate; incremental events preserve progress.
"""
import argparse, collections, datetime, hashlib, itertools, json, re
from pathlib import Path
from bs4 import BeautifulSoup
from romania_archive_retrieval import ArchiveClient, RetrievalStopped

BASE=Path(__file__).resolve().parents[1]
OUT=BASE/"outputs/romania_alba_2001_structural_audit_20260929"
SOURCE="http://www.edu.ro/adm2001/"
STAMP="20020816151117"
CLIENT=None

def configure_retrieval(policy_reviewed=False):
    global CLIENT
    OUT.mkdir(parents=True,exist_ok=True)
    CLIENT=ArchiveClient(OUT,emit,policy_reviewed=policy_reviewed)

def emit(x):
    x={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),**x}
    with (OUT/"events.jsonl").open("a") as f:
        f.write(json.dumps(x,ensure_ascii=False)+"\n"); f.flush()
    if x.get("kind")!="page": print(json.dumps(x,ensure_ascii=False),flush=True)

def fetch(path,kind):
    requested=f"https://web.archive.org/web/{STAMP}id_/{SOURCE}{path}"
    if CLIENT is None:
        raise RetrievalStopped("Retrieval must be explicitly configured after policy review.")
    result=CLIENT.get(requested)
    if result is None:
        emit({"kind":"fetch_error","requested":requested,"error":"Page unverified; see HTTP attempt log."})
        return None
    raw,url=result
    body=raw.decode("cp1250",errors="replace")
    soup=BeautifulSoup(body,"html.parser")
    table=next((t for t in soup.find_all("table") if any(
        c.get_text(" ",strip=True) in ["CNP","Cod şcoală"] for c in t.find_all("th"))),None)
    if table is None:
        emit({"kind":"parse_error","requested":requested,"effective_url":url.strip()});return None
    h=[c.get_text(" ",strip=True) for c in table.find_all("th")]
    rows=[];cells=[]
    for tr in table.find_all("tr"):
        cc=tr.find_all("td",recursive=False)
        if len(cc)==len(h) and re.fullmatch(r"\d+",cc[0].get_text(strip=True)):
            rows.append(dict(zip(h,[c.get_text(" ",strip=True) for c in cc])));cells.append(cc)
    meta={"kind":"page","report":kind,"requested":requested,"effective_url":url.strip(),
          "sha256_decoded_body":hashlib.sha256(body.encode()).hexdigest(),"headers":h,"rows":len(rows)}
    emit(meta)
    return h,rows,cells,meta

def col(row,term):
    return next((v for k,v in row.items() if term.lower() in k.lower()),"")
def school_label(row):
    return col(row,"coal")
def origin_parts(label):
    # Only split the explicitly printed county suffix; no fuzzy name normalization.
    m=re.fullmatch(r"(.*?)\s*/\s*([A-Z]{1,2})",label)
    return (m.group(1),m.group(2)) if m else (label,None)
def key(row):
    # General candidate pages append / COUNTY; local placement labels omit it.
    # Compare the exact remaining school label, not an approximate school name.
    return (row.get("Nume",""),origin_parts(school_label(row))[0])
def grouped(rows):
    d=collections.defaultdict(list)
    for r in rows:d[key(r)].append(r)
    return d
def numeric(row,term):
    try:return float(col(row,term).replace(",","."))
    except ValueError:return None

def main(policy_reviewed=False):
    OUT.mkdir(parents=True,exist_ok=True)
    final=OUT/"summary_v2.json"
    if final.exists():
        print("Completed checkpoint exists; no network rerun. "+str(final));return
    configure_retrieval(policy_reviewed)
    emit({"kind":"start","scope":"Alba 2001 structure only","schema_version":2,
          "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
    directory=fetch("raport_scoli_din_judet.asp-cj=AB&nj=ALBA&idx=0.htm","origin_directory")
    if directory is None:raise RuntimeError("Origin directory unavailable")
    dh,dr,dc,dm=directory
    reg={}
    for r,cc in zip(dr,dc):
        name=r["Nume şcoală"];link=next((a["href"] for c in cc for a in c.find_all("a",href=True) if "candidati_per_scoala" in a["href"]),None)
        reg[r["Cod şcoală"]]={"code":r["Cod şcoală"],"name":name,"address":r["Adresă"],
                "medium":r["Mediu"],"candidate_report":link}
    (OUT/"origin_school_directory.json").write_text(json.dumps(list(reg.values()),ensure_ascii=False,indent=2)+"\n")
    groups={}
    plans=[
      ("candidate","raport_candidati_total",[1,501,1001,1501,2001,2501]),
      ("admitted","raport_admisi_per_judet",[0,500,1000,1500,2000,2500]),
      ("unassigned","raport_respinsi_per_judet",[0]),
      ("incoming_candidate","raport_candidati_altejud_per_judet",[0]),
      ("incoming_admitted","raport_admisi_altejud_per_judet",[0]),
      ("incoming_unassigned","raport_respinsi_altejud_per_judet",[0])]
    for kind,stem,indices in plans:
        rr=[];ok=True
        for idx in indices:
            x=fetch(f"{stem}.asp-cj=AB&nj=ALBA&idx={idx}.htm",kind)
            if x is None:ok=False;continue
            rr.extend(x[1])
        groups[kind]=rr
        emit({"kind":"report_family","report":kind,"rows":len(rr),"all_requested_pages_returned":ok})
        if not ok and kind in ["candidate","admitted","unassigned"]:raise RuntimeError("Required county pages incomplete")
    cg=grouped(groups["candidate"]);ag=grouped(groups["admitted"]);ug=grouped(groups["unassigned"])
    matches={};ambiguities=0
    for k,rr in cg.items():
        options=ag.get(k,[])+ug.get(k,[])
        if len(rr)==1 and len(options)==1:matches[k]=options[0]
        elif len(rr)>1 or len(options)>1:ambiguities+=len(rr)
    county_conflicts=[k for k,v in matches.items() if origin_parts(school_label(cg[k][0]))[1]
                     and origin_parts(school_label(v))[1]
                     and origin_parts(school_label(cg[k][0]))[1]!=origin_parts(school_label(v))[1]]
    for k in county_conflicts:del matches[k]
    score_disagree=sum(col(cg[k][0],"admitere")!=col(v,"admitere") for k,v in matches.items())
    name_reg=collections.defaultdict(list)
    for code,d in reg.items():name_reg[d["name"]].append(code)
    per_origin=collections.defaultdict(list)
    for r in groups["candidate"]:per_origin[school_label(r)].append(r)
    school_summaries=[]
    towns=["ALBA IULIA","BAIA DE ARIES","OCNA MURES","AIUD","BLAJ","CUGIR","SEBES","CIMPENI","ABRUD","ZLATNA","TEIUS"]
    for label,rr in sorted(per_origin.items()):
        name,county=origin_parts(label)
        codes=name_reg.get(name,[]) if county=="AB" else []
        d=reg[codes[0]] if len(codes)==1 else {}
        address=d.get("address","")
        address_without_county=address[5:] if address.startswith("ALBA ") else address
        town=next((t for t in towns if address_without_county==t or address_without_county.startswith(t+" ")),None) if d.get("medium")=="U" else None
        exams=[numeric(r,"capacitate") for r in rr]; exams=[v for v in exams if v is not None]
        linked=[r for r in rr if key(r) in matches]
        destinations={(col(matches[key(r)],"Liceu"),col(matches[key(r)],"Specializare")) for r in linked if key(r) in ag}
        school_summaries.append({"origin_label":label,"origin_county":county,"source_code":codes[0] if len(codes)==1 else None,
          "directory_exact_name_matches":len(codes),"address":address,"medium":d.get("medium"),"explicit_urban_address_town":town,
          "applicant_records":len(rr),"exact_status_matches":len(linked),"ambiguous_records":sum(len(cg[key(r)])>1 or len(ag.get(key(r),[])+ug.get(key(r),[]))>1 for r in rr),
          "unmatched_records":sum(key(r) not in matches for r in rr),
          "distinct_observed_destination_school_tracks":len(destinations),
          "exam_observed_count":len(exams),"exam_min":min(exams) if len(exams)>=5 else None,"exam_max":max(exams) if len(exams)>=5 else None,
          "full_graduating_cohort_completeness":"unknown"})
    (OUT/"origin_group_audit.json").write_text(json.dumps(school_summaries,ensure_ascii=False,indent=2)+"\n")
    townstats=[]
    for town in towns:
        schools=[s for s in school_summaries if s["explicit_urban_address_town"]==town]
        ranges=[s for s in schools if s["exam_min"] is not None]
        pairs=list(itertools.combinations(ranges,2))
        townstats.append({"town":town,"exactly_mapped_origin_groups":len(schools),"applicant_records":sum(s["applicant_records"] for s in schools),
          "schools_with_at_least_5_records_and_exam_ranges":len(ranges),"range_pairs":len(pairs),
          "intersecting_exam_range_pairs":sum(max(a["exam_min"],b["exam_min"])<=min(a["exam_max"],b["exam_max"]) for a,b in pairs)})
    summary={
      "scope":"Alba 2001 report structure, exact correspondence, and observed score support; no substantive analysis",
      "directory_entries":len(reg),"report_rows":{k:len(v) for k,v in groups.items()},
      "distinct_origin_labels":len(per_origin),"origin_county_counts":dict(collections.Counter(origin_parts(school_label(r))[1] for r in groups["candidate"])),
      "exact_unique_name_origin_status_matches":len(matches),"ambiguous_candidate_records":ambiguities,
      "unmatched_candidate_records":sum(len(v) for k,v in cg.items() if k not in matches),
      "duplicate_candidate_key_records":sum(len(v) for v in cg.values() if len(v)>1),
      "status_keys_absent_from_candidate":len((ag.keys()|ug.keys())-cg.keys()),
      "composite_disagreements_on_exact_matches":score_disagree,
      "explicit_origin_county_conflicts_rejected":len(county_conflicts),
      "exact_directory_mapped_groups":sum(s["source_code"] is not None for s in school_summaries),
      "exact_directory_mapped_records":sum(s["applicant_records"] for s in school_summaries if s["source_code"] is not None),
      "incoming_candidate_exact_overlap_with_general":len(grouped(groups["incoming_candidate"]).keys()&cg.keys()),
      "school_size_distribution":dict(collections.Counter(s["applicant_records"] for s in school_summaries)),
      "urban_town_support":townstats,
      "limitations":["No full-graduating-cohort denominator.","No national outgoing-Alba reconciliation.",
                     "Exact name and origin-school text after splitting printed county suffix; explicit county conflicts rejected; no persistent ID demonstrated.",
                     "Address-prefix town mapping covers explicitly urban directory addresses only.",
                     "Ranges for fewer than five records suppressed for reporting; five is not an analytical eligibility rule.",
                     "Min/max overlap is a support check, not evidence of common distributions or identification."]}
    final.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n")
    emit({"kind":"completed",**summary})
if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--run",action="store_true")
    parser.add_argument("--policy-reviewed",action="store_true",
                        help="Use only after reviewing the archive's published crawling guidance.")
    args=parser.parse_args()
    if args.run:
        try:main(args.policy_reviewed)
        except (RetrievalStopped,KeyboardInterrupt) as error:
            emit({"kind":"stopped","reason":str(error) or "Interrupted by user"})
            raise SystemExit(2)
    else:parser.print_help()
