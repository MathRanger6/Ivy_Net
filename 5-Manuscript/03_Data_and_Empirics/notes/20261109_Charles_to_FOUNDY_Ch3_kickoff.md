# Message to FOUNDY — Chapter 3 Army data answers (Charles, 2026-11-09)

**Attach:** [`20261109_FOUNDY_Response_Ch3_Army_data_questions.md`](20261109_FOUNDY_Response_Ch3_Army_data_questions.md) (full §1–8, answers the morning question list).  
**Supporting:** [`20261109_CODA_Response_Ch3_raw_to_dataframes.md`](20261109_CODA_Response_Ch3_raw_to_dataframes.md) (tables/IRB), [`_DISPOSABLE_Ch3_data_empirics_thread.md`](../../re_entry/_DISPOSABLE_Ch3_data_empirics_thread.md) (prose seed + placeholders).

---

**Subject:** Answers to the Army raw-data → dataframe questions (Ch.3)

FOUNDY,

Here are the answers you asked for this morning, in **`20261109_FOUNDY_Response_Ch3_Army_data_questions.md`**. It follows the eight headings in `20261109_Ch3_Questions_for_CODA_raw_to_dataframes.md` (raw sources, filters, events, top box, run of record, what to cite, quirks, print/IRB). I skimmed it against the notebooks; the disposable thread matches on component and on the peer variable.

**Settled for drafting (unless I tell you otherwise):**

- **Promotion outcome:** any promotion to major (`dor_maj`); attrition = exit from the extract before study end without major; open at study end counts as not promoted in the bar denominators.
- **Bars:** final promotion + final attrition by performance band—not a survival chapter. Optional **one footnote** on below-zone history (default yes); Alex does not want a long BZ sidebar.
- **Run of record for placeholder figures:** March 2026 export `20260320-1000`, Run 1 · `pipeline_config_17_1`, YG **2002–2011** on in that export’s base config, `noOER`, **N = 31,692** in eight bins. Captions note **Vantage TBD** until we rerun.
- **Horizontal axis on those March bars:** z-scored **`pool_minus_mean_snr_fwd`** (own top-box share **minus** LOO mean of peers’ shares)—**not** pond LOO mean alone (`pool_tb_ratio_mean_snr_fwd`). Wording like “standing relative to one’s senior-rater pool” fits; “peer quality alone” does not match this PNG.
- **YG + snapshot window:** include in methods—chosen to follow officers through realistic CPT→MAJ windows and limit unresolved open cases.
- **`compo`:** string **`R` = Regular Army**; we do **not** globally drop officers who ever had non-`R` rows. Chapter treats **leaving the Regular Army promotion pool** like attrition for this study; MAJ selection in another component is out of scope (annotation in the response + disposable).
- **Print:** PDE (AAG-RFL); OER methods OK under DUAs; no microdata release.

**Still TK (prose can say “to be updated from Vantage”):** filter flow table with counts at each step; per-band `event = 0`; count of mixed-component histories; exact snapshot end dates.

**Prose seed:** disposable § “Army — draft of the data section” (variable table updated today).

**Out of scope for Ch.3 figures:** sex/prestige/MOS exploratory panels; old screenshot decks.

If anything in the response conflicts with what you see in Word, flag it—I’d rather fix the doc than argue in the chapter.

Charles
