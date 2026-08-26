setopt INTERACTIVE_COMMENTS && \
# SLIDE 1 FIXED HERO
python sports/scripts/pass_a_empirical_bundle.py \
--y-draft-mode ever \
--panel-rows all-ps \
--n-bins 16 \
--poolq-binning quantile \
--roster-x poolq_loo \
--output-tag “_FIXED_HERO” \
--output-root 3-Master_Plan/re_entry/HEROs_and_PASSes/population_sandbox/hero && \
# SLIDE 2 – SLIDE 1 CHNG to poolq
python sports/scripts/pass_a_empirical_bundle.py \
--y-draft-mode ever \
--panel-rows all-ps \
--n-bins 16 \
--poolq-binning quantile \
--roster-x poolq \
--output-tag “_slide_2” \
--output-root 3-Master_Plan/re_entry/HEROs_and_PASSes/population_sandbox/hero && \
# SLIDE 3 – SLIDE 1 CHNG draft-mode to season
python sports/scripts/pass_a_empirical_bundle.py \
--y-draft-mode season \
--panel-rows all-ps \
--n-bins 16 \
--poolq-binning quantile \
--roster-x poolq_loo \
--output-tag “_slide_3” \
--output-root 3-Master_Plan/re_entry/HEROs_and_PASSes/population_sandbox/hero && \