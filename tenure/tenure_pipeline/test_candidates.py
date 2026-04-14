"""
test_candidates.py  —  Quick-test candidate R1 CS schools against live faculty pages.
Run:  python3 tenure_pipeline/test_candidates.py
Writes results to tenure_pipeline/candidate_test_results.json
"""
import sys, time, tempfile, json
from pathlib import Path

# Work from workspace root regardless of how the script is invoked
_WORKSPACE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_WORKSPACE))

from tenure_pipeline.html_parser import extract_faculty
import urllib.request

CANDIDATES = [
    # --- Large flagship R1s ---
    ("Arizona State University",             "https://scai.engineering.asu.edu/about/faculty/"),
    ("Washington University in St. Louis",   "https://cse.wustl.edu/people/faculty/Pages/default.aspx"),
    ("University of Georgia",                "https://www.cs.uga.edu/directory/faculty"),
    ("Georgia State University",             "https://cs.gsu.edu/faculty/"),
    ("University of Miami",                  "https://www.cs.miami.edu/people/faculty/"),
    ("Florida International University",     "https://www.cs.fiu.edu/faculty/"),
    ("Florida Atlantic University",          "https://www.cs.fau.edu/people/faculty/"),
    ("Virginia Commonwealth University",     "https://egr.vcu.edu/departments/computer-science/faculty-and-staff/"),
    ("University of Alabama Birmingham",     "https://www.uab.edu/engineering/cs/people/faculty"),
    ("University of Mississippi",            "https://cs.olemiss.edu/people/"),
    ("University of Memphis",                "https://www.cs.memphis.edu/about/faculty.php"),
    # --- Mid-size R1s ---
    ("Baylor University",                    "https://www.baylor.edu/cs/index.php?id=6"),
    ("University of Texas El Paso",          "https://www.cs.utep.edu/people/faculty/"),
    ("University of Texas Rio Grande Valley","https://www.utrgv.edu/csit/faculty/index.htm"),
    ("University of New Mexico",             "https://cs.unm.edu/people/faculty/"),
    ("University of Colorado Denver",        "https://cse.ucdenver.edu/people/faculty/"),
    ("Colorado School of Mines",             "https://cs.mines.edu/faculty/"),
    ("Utah State University",                "https://engineering.usu.edu/cs/faculty/"),
    ("Wichita State University",             "https://www.cs.wichita.edu/people/faculty/"),
    ("University of Missouri Kansas City",   "https://cs.umkc.edu/people/"),
    ("University of Nebraska Omaha",         "https://www.unomaha.edu/college-of-information-science-and-technology/computer-science/faculty-and-staff.php"),
    # --- Midwest / Northeast ---
    ("University of Cincinnati",             "https://eecs.ceas.uc.edu/people/faculty/"),
    ("Michigan Technological University",    "https://www.mtu.edu/cs/department/faculty-staff/"),
    ("University of Wisconsin Milwaukee",    "https://uwm.edu/engineering/ece/faculty/"),
    ("North Dakota State University",        "https://www.ndsu.edu/cs/people/faculty/"),
    ("University of New Hampshire",          "https://www.cs.unh.edu/people/faculty"),
    ("University of Rhode Island",           "https://web.uri.edu/cs/faculty/"),
    ("University of Massachusetts Lowell",   "https://www.uml.edu/sciences/computer-science/faculty/"),
    # --- Metro / private R1s ---
    ("New Jersey Institute of Technology",   "https://cs.njit.edu/faculty"),
    ("Stevens Institute of Technology",      "https://www.stevens.edu/school-engineering-science/departments/computer-science/faculty"),
    ("University of Louisville",             "https://engineering.louisville.edu/academics/departments/cse/faculty/"),
    ("Portland State University",            "https://www.pdx.edu/computer-science/faculty"),
    ("San Diego State University",           "https://www.cs.sdsu.edu/people/"),
]

OUT = _WORKSPACE / "tenure_pipeline" / "candidate_test_results.json"

print(f"Testing {len(CANDIDATES)} candidate schools ...\n")
print(f"  {'School':<50} {'N':>5}  {'Strategy':<35}  Status")
print("  " + "-"*100)

results = []
for name, url in CANDIDATES:
    try:
        req  = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh)'})
        html = urllib.request.urlopen(req, timeout=12).read()
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as f:
            f.write(html); tmp = f.name
        recs, meta = extract_faculty(tmp, return_meta=True)
        Path(tmp).unlink(missing_ok=True)
        n = len(recs)
        flag = "GOOD" if n >= 10 else ("MARGINAL" if n >= 3 else "LOW")
        icon = "✅" if flag == "GOOD" else ("⚠️ " if flag == "MARGINAL" else "❌")
        print(f"  {icon} {name:<48} {n:>5}  {meta['winner']:<35}  {flag}", flush=True)
        results.append({'university': name, 'url': url, 'n': n,
                        'strategy': meta['winner'], 'status': flag})
    except Exception as e:
        msg = str(e)[:60]
        print(f"  ❓  {name:<48} {'ERR':>5}  {'':35}  {msg}", flush=True)
        results.append({'university': name, 'url': url, 'n': -1,
                        'strategy': '', 'status': f'ERROR: {msg}'})
    time.sleep(0.8)

OUT.write_text(json.dumps(results, indent=2))

print(f"\n{'='*70}")
good     = [r for r in results if r['status'] == 'GOOD']
marginal = [r for r in results if r['status'] == 'MARGINAL']
errors   = [r for r in results if r['status'].startswith('ERROR')]

print(f"\n✅ GOOD (≥10 records) — {len(good)} schools:")
for r in sorted(good, key=lambda x: -x['n']):
    print(f"     {r['n']:>4}  {r['university']:<50}  {r['strategy']}")

print(f"\n⚠️  MARGINAL (3–9) — {len(marginal)} schools:")
for r in sorted(marginal, key=lambda x: -x['n']):
    print(f"     {r['n']:>4}  {r['university']:<50}  {r['strategy']}")

print(f"\n❓  ERRORS — {len(errors)} schools (blocked / 404 / timeout):")
for r in errors:
    print(f"          {r['university']}")

print(f"\nResults saved → {OUT}")
