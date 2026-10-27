from pathlib import Path
import pandas as pd,numpy as np,json,hashlib
O=Path(__file__).parent;A=O/('archive_clipped_v1' if (O/'archive_clipped_v1').exists() else 'superseded_JN03_v1_scores_clipped_to_zero')
old=pd.read_csv(A/'gibbs_t_sweep_bin_rates.csv');new=pd.read_csv(O/'gibbs_t_sweep_bin_rates.csv')
audit=old.merge(new,on=['t_sel','bin','n','observed_rate','topK_rate'],suffixes=('_old_clipped','_corrected'),validate='one_to_one')
assert len(audit)==144
audit['change_percentage_points']=100*(audit.gibbs_mean_inclusion_corrected-audit.gibbs_mean_inclusion_old_clipped)
audit.to_csv(O/'correction_before_after_bin_rates.csv',index=False)
oldplayers=pd.read_csv(A/'player_gibbs_inclusion_by_t.csv.gz');newplayers=pd.read_csv(O/'player_gibbs_inclusion_by_t.csv.gz')
cols=['athlete_id','bin','perf','Y_draft','topK_selected']
pd.testing.assert_frame_equal(oldplayers[cols],newplayers[cols])
for t,g in new.groupby('t_sel'):assert np.isclose((g.n*g.gibbs_mean_inclusion).sum(),615,atol=1e-9)
for c in newplayers.columns.difference(cols):
 assert newplayers[c].between(0,1).all() and np.isclose(newplayers[c].sum(),615)
# Source hashes must still match old provenance; settings must match exactly.
p=json.loads((O/'provenance.json').read_text());q=json.loads((A/'provenance.json').read_text())
for k in ['source_hashes','N','K','score','n_replicates','seed_base','t_sweep','t_featured_on_plot']:assert p[k]==q[k],k
f=O/'validation.txt';f.write_text(f.read_text()+'PASS: original and corrected player identities, scores, outcomes, top-K indicators and bins are identical; all nine temperatures, seeds, counts and source hashes match v1. Each temperature has total mean inclusions 615. Before/after table has 144 matched bin-temperature rows.\n')
print(audit[audit.t_sel.isin([.25,.7,2.5])&audit.bin.isin([1,8,15,16])][['t_sel','bin','gibbs_mean_inclusion_old_clipped','gibbs_mean_inclusion_corrected','change_percentage_points']].to_string(index=False))
