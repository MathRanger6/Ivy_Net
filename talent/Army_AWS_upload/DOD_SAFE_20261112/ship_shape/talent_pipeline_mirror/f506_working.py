# This Notebook Creates a Feeder DatFrame for 507 and 508
## 1. Load 'df_501_major'
## 2. Select a snapshot date with a substantial number of promotions to CPT
## 3. Filter the DataFrame to only include those pid_pde's who made CPT during that snapshot
## 4. Save the new DataFrame as '507_exact_base'

import os, ray, sys
sys.path.append(".")

# === Ray/Modin Environment Variables ===
from init_ray_cluster import init_ray_cluster
# init_ray_cluster()


# === Core Libraries ===
# import modin.pandas as mpd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys, glob, csv
import numpy as np
import networkx as nx
from datetime import timedelta, time
from time import gmtime, localtime, strftime, sleep
from lifelines import CoxPHFitter

# === SQL and Feather I/O ===
# import psycopg2
# from psycopg2 import sql, extras
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
from collections import Counter
from IPython.display import IFrame, display, HTML

from functionsG import *

# from functionsG import (
#     get_params, run_sql_script, store_feather, load_feather,
#     categorize, reduce_floats, add_fy_col, print_syntax,
#     time_start, time_stop, print_syntax, run_pp
# )

# === Secure PostgreSQL Connection String and Create Engine ===
pp = run_pp()
from urllib.parse import quote_plus
safe_pw = quote_plus(pp)
params_dict = get_params()
conn_str = XXXXXXXXXX


# === Directories ===
load_dir = './chapter_folder'
load_local = './zz_load_local'
store_dir = './chapter_folder'
store_local = './zz_store_local'
var_dir = './running_vars'

# === Control Flags ===
rank = 'CPT'
optimize = False
build_df_work = True
keep_crl = True

# === Other Stuff ===
df_store_name = 'df_u'
df_save_dir = '/projects/TALENT_NET/big_dfs'
sql_path = './winbucket_link/'
data_table_pde = "study_talent_net.mv_master_ad_army_qtr_v3a"
data_table = "study_talent_net.mv_fouo_uz_master_ad_army_v3a"
good_years = None
null_entry = "NA"

snapshots = sorted(load_pickle('snapshots',var_dir))
snap_dict = make_bidict({i:snap for i,snap in enumerate(snapshots)})
store_pickle(snap_dict,'snap_dict_506',var_dir)


## Boolean Control Flags

# =============================================
# Boolean Switches
# =============================================
ONEA      = True ## Part ONE A: Create df2, a DataFrame with only CPT and MAJ entries with column names adjusted for 507
ONEB      = True ## Part ONE B: Create a DataFrame (df_cpt_promo) of the number of officers promoted to Captain withn each snapshot
ONEC      = True ## Part ONE C: Visualize that data and get the top three CPT promo snapshots (top_cpt_idxs)



## Part ONE A:  Create df2 save as df_506_base_exact, a DataFrame with only CPT and MAJ entries with column names adjusted for 507

# df = load_feather('df_501_major')
# df = load_feather('df_with_cum_opm')
df = load_feather('df_with_met_20021231_20120930')

### I FOUND A BAD PID_PDE!!!!  - PROBABLY MULTIPLE PEOPLE SAME PID_PDE - LET'S ELIMINATE
df = df[df.pid_pde != 'XXXXXXXXXX']
##############################################

snapshots = sorted(load_pickle('snapshots',var_dir))

df.pn_age_qy.unique()
df[df.pn_age_qy != df.pn_age_qy]

df.mrtl_stat_cd.unique()
df.occ_crer_grp_cd.unique()

def drop_non_cpt_maj_rows(df_in):
    df = df_in.copy()
    df = df[df.rank_pde.isin(['CPT','MAJ'])]
    return df
def map_and_rename_cols(df_in):
    df = df_in.copy()
    def mar_sex_code_interpret(in_value):
        if in_value == 'M':
            return 1
        else:
            return 0 
    df['married'] = df['mrtl_stat_cd'].apply(mar_sex_code_interpret).astype(int)
    df['sex'] = df['pn_sex_cd'].apply(mar_sex_code_interpret).astype(int)
    
    # We can only map 'age' values these as integer if there are no nan's for age in any rows
    # How many pid_pde's have a row with a nan value for age?
    df.pn_age_qy.unique()
    nan_age_pids = df[df.pn_age_qy != df.pn_age_qy]['pid_pde'].unique()
    # print(f"There are {len(nan_age_pids):,} pid_pde's with a nan value in one of their rows for pn_age_qy")
    if len(nan_age_pids):
        df['age'] = df.pn_age_qy
    else:
        df['age'] = df.pn_age_qy.astype(int)
    df['job_code'] = df.occ_crer_grp_cd
    return df
df2 = drop_non_cpt_maj_rows(df)
df2 = map_and_rename_cols(df2)

store_feather(df2,'df_506_base_exact')
print("df_506_exact_base created and stored......!!!!")

## Part ONE B: Create dictionaries and a dataframe of officers promoted to Captain withn each snapshot

# --- a. Load the dor_cpt_dict dictionary and intitalize cpt_promo_dict and cpt_promo_num_dict to store our snapshot values 
dor_cpt_dict = load_pickle('dor_cpt_dict',var_dir)
cpt_promo_dict = dict() # Store the pid_pde's of the new Captains for this snapshot
cpt_promo_num_dict = {'snap_idx':[],'new_captains_num':[]} # Just store the number of new captains

# --- b. get a list of all know captain dates of rank
dors_cpt = sorted(list(set(dor_cpt_dict.values())))

# --- c. Loop through the snapshot dates and identify the target dates of rank that fall within that snapshot
for snap_idx in range(len(snapshots)):
    target_dors = [dor for dor in dors_cpt if dor > snapshots[snap_idx-1] and  dor <= snapshots[snap_idx]]
    # -- (1) Create a new DatFrame containing officers who made Captain during that snapshot index
    df_snap_cpt = df2[df2.dor_cpt.isin(target_dors)]
    # -- (2) Get the number of new Captains and store in cpt_promo_num_dict
    num_cpt_in_snapshot = df_snap_cpt.pid_pde.nunique()
    cpt_promo_num_dict['snap_idx'].append(snap_idx)
    cpt_promo_num_dict['new_captains_num'].append(num_cpt_in_snapshot)
    # -- (3) Get the pid_pde's of new Captains and store in cpt_promo_dict
    pids_in_snapshot = df_snap_cpt.pid_pde.unique().tolist()
    cpt_promo_dict[snap_idx] = pids_in_snapshot

# --- d. Save the dictionaries
store_pickle(cpt_promo_dict,'cpt_promo_dict',var_dir)
print("cpt_promo_dict created and stored......!!!!")
store_pickle(cpt_promo_num_dict,'cpt_promo_num_dict',var_dir)
print("cpt_promo_num_dict created and stored......!!!!")

# --- d. Create a DataFrame
df_cpt_promo_nums = pd.DataFrame(cpt_promo_num_dict)
# df_cpt_promo_nums.sort_values(by='new_captains_num').head(25)
