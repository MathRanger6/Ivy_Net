# LIBRARY and GLOBAL IMPORTS
import os, ray, sys, re, glob, csv
sys.path.append(".")
from functionsG import *

# === Core Libraries ===
# Import necessary libraries
import numpy as np
from collections import Counter
from collections import defaultdict, deque
import pandas as pd

# === Directories ===
var_dir = './running_vars'

# UIC Hierarchy Analysis Functions
def find_subordinate_uics_recursive(df_in, 
                                   top_uic, 
                                   uic_col = 'UIC', 
                                   parent_col = 'PARENTUIC',
                                   include_top = True,
                                   max_depth = None,
                                   show=False):
    """
    Recursively find all subordinate UICs for a given top-level UIC.
    
    Parameters:
    -----------
    df : pd.DataFrame
    DataFrame containing UIC hierarchy data
    top_uic : str, top-level UIC to get all subordinates for
    List of top-level UICs to start the search from
    uic_col : str, default 'UIC'
    Column name containing the unit identification codes
    parent_col : str, default 'PARENTUIC'
    Column name containing the parent/superior UIC for each unit
    include_top : bool, default True
    Whether to include the top-level UICs in the results
    max_depth : Optional[int], default None
    Maximum depth to search (None for unlimited depth)
    
    Returns:
    --------
    sub_uics : list
    list of all subordinate UICs
    """
    df=df_in.copy()
    uic_col = 'UIC'
    parent_col = 'PARENTUIC'
    include_top = True
    max_depth = None
    # Validate inputs
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")
    if uic_col not in df.columns:
        raise ValueError(f"Column '{uic_col}' not found in DataFrame")
    if parent_col not in df.columns:
        raise ValueError(f"Column '{parent_col}' not found in DataFrame")
    
    # Remove rows with null UICs or parent UICs for cleaner processing
    clean_df = df.dropna(subset=[uic_col, parent_col])
    
    # Create lookup dictionary for faster searching
    # Group by parent UIC to get all direct subordinates
    hierarchy_dict = defaultdict(set)
    
    # Build the hierarchy dictionary
    for _, row in clean_df.iterrows():
        parent = row[parent_col]
        child = row[uic_col]
        if pd.notna(parent) and pd.notna(child):
            hierarchy_dict[parent].add(child)
    
    if show:
        print(f"📊 Built hierarchy dictionary with {len(hierarchy_dict)} parent UICs")

    subordinates = set()
    
    if include_top:
        subordinates.add(top_uic)
    
    # Use BFS to find all subordinates
    queue = deque([(top_uic, 0)])  # (uic, depth)
    visited = set()
    
    while queue:
        # print('fy, queue',clean_df.FY.unique().tolist(),queue)
        current_uic, depth = queue.popleft()
        
        # Skip if we've already processed this UIC
        if current_uic in visited:
            continue
            
        visited.add(current_uic)

        # Check depth limit
        if max_depth is not None and depth >= max_depth:
            continue
        
        # Get direct subordinates
        direct_subordinates = hierarchy_dict.get(current_uic, set())
        
        # Add them to df_uic_hierarchy.sub_class.unique()results and queue
        for sub_uic in direct_subordinates:
            subordinates.add(sub_uic)
            queue.append((sub_uic, depth + 1))
    
    if show:
        print(f"🎯 Found {len(subordinates)} total subordinates for {top_uic} for FY {clean_df.FY.unique().tolist()}")
    return subordinates


# let's define a uic_subordinate_dict dictionary
uic_subordinate_dict_raw = {
    'XXXXXX':{'top_name':'75RR','simplename':"75RR",'class':'RGR','sub_class':'rgr','uic_pde':None,'description': "75th Ranger Regiment",'sub_units_by_fy':dict()},
    'XXXXXX':{'top_name':'160SOAR','simplename':"160SOAR",'class':'SOAR','sub_class':'soar','uic_pde':None,'description': "160th SOAR Spec Opns Aviation Regiment",'sub_units_by_fy':dict()},
    'XXXXXX':{'top_name':'1SFG','simplename':"1SFG",'class':'SFG','sub_class':'sfg','uic_pde':None,'description': "1SFG - 1st Special Forces Group",'sub_units_by_fy':dict()},
    'XXXXXX':{'top_name':'3SFG','simplename':"3SFG",'class':'SFG','sub_class':'sfg','uic_pde':None,'description': "3SFG - 3rd Special Forces Group",'sub_units_by_fy':dict()},
    'XXXXXX':{'top_name':'5SFG','simplename':"5SFG",'class':'SFG','sub_class':'sfg','uic_pde':None,'description': "5SFG - 5th Special Forces Group",'sub_units_by_fy':dict()},
    'XXXXXX':{'top_name':'7SFG','simplename':"7SFG",'class':'SFG','sub_class':'sfg','uic_pde':None,'description': "7SFG - 7th Special Forces Group",'sub_units_by_fy':dict()},
    'XXXXXX':{'top_name':'10SFG','simplename':"10SFG",'class':'SFG','sub_class':'sfg','uic_pde':None,'description': "10SFG - 10th Special Forces Group",'sub_units_by_fy':dict()},
    'XXXXXX':{'top_name':'528SB','simplename':"528SB",'class':'SFG','sub_class':'sfg','uic_pde':None,'description': "528 SusBde - 528th Sustainment Brigade",'sub_units_by_fy':dict()},
    'XXXXXX':{'top_name':'1ID','simplename':"(HDIV) 1ID",'class':'HDIV','sub_class':'hdiv','uic_pde':'XXXXXXXXXX','description': "1ID - 1st Infantry Division",'sub_units_by_fy':dict()},
    'XXXXXX':{'top_name':'2ID','simplename':"(HDIV) 2ID",'class':'HDIV','sub_class':'hdiv','uic_pde':'XXXXXXXXXX','description': "2ID - 2nd Infantry Division",'sub_units_by_fy':dict()},
    'XXXXXX':{'top_name':'3ID','simplename':"(HDIV) 3ID",'class':'HDIV','sub_class':'hdiv','uic_pde':'XXXXXXXXXX','description': "3ID - 3rd Infantry Division",'sub_units_by_fy':dict()},
    'XXXXXX':{'top_name':'4ID','simplename':"(HDIV) 4ID",'class':'HDIV','sub_class':'hdiv','uic_pde':'XXXXXXXXXX','description': "4ID - 4th Infantry Division",'sub_units_by_fy':dict()},
    'XXXXXX':{'top_name':'7ID','simplename':"(HDIV) 7ID",'class':'HDIV','sub_class':'hdiv','uic_pde':'XXXXXXXXXX','description': "7ID - 7th Infantry Division",'sub_units_by_fy':dict()},
    'XXXXXX':{'top_name':'1AD','simplename':"(HDIV) 1AD",'class':'HDIV','sub_class':'hdiv','uic_pde':'XXXXXXXXXX','description': "1AD - 1st Armored Division",'sub_units_by_fy':dict()},
    'XXXXXX':{'top_name':'1CAV','simplename':"(HDIV) 1CD",'class':'HDIV','sub_class':'hdiv','uic_pde':'XXXXXXXXXX','description': "1CD - 1st Cavalry Division",'sub_units_by_fy':dict()},
    'XXXXXX':{'top_name':'82ABN','simplename':"(LHDIV) 82ABD",'class':'LDIV','sub_class':'ldiv','uic_pde':'XXXXXXXXXX','description': "82ABN - 82nd Airborne Division",'sub_units_by_fy':dict()},
    'XXXXXX':{'top_name':'101ABN','simplename':"(LHDIV) 101ABD",'class':'LDIV','sub_class':'ldiv','uic_pde':'XXXXXXXXXX','description': "101ABN - 101st Airborne Division",'sub_units_by_fy':dict()},
    'XXXXXX':{'top_name':'10MTN','simplename':"(LHDIV) 10MD",'class':'LDIV','sub_class':'ldiv','uic_pde':'XXXXXXXXXX','description': "10MTN - 10th Mountain Division",'sub_units_by_fy':dict()},
    'XXXXXX':{'top_name':'25ID','simplename':"(LHDIV) 25ID",'class':'LDIV','sub_class':'ldiv','uic_pde':'XXXXXXXXXX','description': "25ID - 25th Infantry Division",'sub_units_by_fy':dict()},
    'XXXXXX':{'top_name':'1SFAB','simplename':"(SFAB) 1 SFAB",'class':'SFAB','sub_class':'sfab','uic_pde':'','description': "1SFAB - 1st Security Force Assistance Bde",'sub_units_by_fy':dict()},
    'XXXXXX':{'top_name':'2SFAB','simplename':"(SFAB) 2 SFAB",'class':'SFAB','sub_class':'sfab','uic_pde':'','description': "2SFAB - 2nd Security Force Assistance Bde",'sub_units_by_fy':dict()},
    'XXXXXX':{'top_name':'3SFAB','simplename':"(SFAB) 3 SFAB",'class':'SFAB','sub_class':'sfab','uic_pde':'','description': "3SFAB - 3rd Security Force Assistance Bde",'sub_units_by_fy':dict()},
    'XXXXXX':{'top_name':'4SFAB','simplename':"(SFAB) 4 SFAB",'class':'SFAB','sub_class':'sfab','uic_pde':'','description': "4SFAB - 4th Security Force Assistance Bde",'sub_units_by_fy':dict()},
    'XXXXXX':{'top_name':'5SFAB','simplename':"(SFAB) 5 SFAB",'class':'SFAB','sub_class':'sfab','uic_pde':'2NCEEP5UHX','description': "5SFAB - 5th Security Force Assistance Bde",'sub_units_by_fy':dict()}
}
store_json(uic_subordinate_dict_raw, 'uic_subordinate_dict_raw',var_dir)
print("Storing 'uic_subordinate_dict_raw'... ")

# Now populate uic_subordinate_dict_raw with data from FMS Web using the get_file_fy and 
# find_subordinate_uics_recursive functions to create uic_subordinate_dict
def get_file_fy(filename):
    pattern = 'ORGS3' + r'(\d{2})'
    match = re.search(pattern,filename)
    return int('20'+ match.group(1))

# Load the uic Lookup dictionary to populate the uic_pde columns for use with our tables
df_uic_lookup = load_feather('df_uic_lookup')

# Initiate the final uic subordinate dictionary
uic_subordinate_dict = uic_subordinate_dict_raw.copy()

# Identify the FMS Web data directory structure and loop through it
# directory by directory,  file by file
uic_data_dir = './data_imported/hierarchy_data/UICs2'
sub_dirs = ['HDIV','LDIV','SFAB','RGR','SOAR','SFG']
file_dict = dict()

action="Looping through data directories to build uic_subordinate_dict"
data_loop = time_start(action, nest=2)
for sub_dir in sub_dirs:
    sub_action=f"working sub-directory {sub_dir}"
    sub_loop = time_start(sub_action,nest=4)
    for file_name in os.listdir(os.path.join(uic_data_dir, sub_dir)):
        dfh = pd.read_csv(os.path.join(uic_data_dir,sub_dir,file_name))
        fy = get_file_fy(file_name)
        # Populate the SOF entries in uic_subordinate_dict
        for top_uic in uic_subordinate_dict:
            if uic_subordinate_dict[top_uic]['class'] == sub_dir:
                try:
                    uic_subordinate_dict[top_uic]['sub_units_by_fy'].update({fy:find_subordinate_uics_recursive(dfh,top_uic,show=False)})
                    # print(f" Updated uic_subordinate_dict[{top_uic}] ({sub_dir}) for fy {fy}, with subordinate units")
                except Exception as e:
                    print(f"Failed to find subordinate units for {top_uic} fy{fy} file: {file_name}: {e}")
    time_stop(sub_loop,action=sub_action,nest=4)
time_stop(data_loop,action=action,nest=2)
store_pickle(uic_subordinate_dict,'uic_subordinate_dict',var_dir)
print("Storing 'uic_subordinate_dict'... ")

# Now transform the uic_subordinate_dict into a lookup dataframe called df_uic_hierarchy
df_uic_hierarchy= pd.DataFrame.from_dict(uic_subordinate_dict, orient='index').reset_index()
df_uic_hierarchy = df_uic_hierarchy.rename(columns={'index':'top_uic', 'uic_pde':'top_uic_pde', 'description':'top_uic_description'})
df_uic_hierarchy = (df_uic_hierarchy.assign(sub_units_by_fy=df_uic_hierarchy['sub_units_by_fy'].map(dict.items))
         .explode('sub_units_by_fy')
         .assign(fy=lambda x: x['sub_units_by_fy'].str[0],
                 asg_uic=lambda x: x['sub_units_by_fy'].str[1])
         .explode('asg_uic')
         .drop(columns='sub_units_by_fy')
         .reset_index(drop=True)
        )
df_uic_hierarchy = df_uic_hierarchy.merge(df_uic_lookup, how='left', on=['asg_uic'])
df_uic_hierarchy = df_uic_hierarchy[[df_uic_hierarchy.columns.tolist()[-1]]+df_uic_hierarchy.columns.tolist()[:-1]]
df_uic_hierarchy = move_column_after(df_uic_hierarchy,'asg_uic','asg_uic_pde')
df_uic_hierarchy = move_column_after(df_uic_hierarchy,'top_uic_pde','asg_uic')
df_uic_hierarchy = move_column_after(df_uic_hierarchy,'top_uic','top_uic_pde')
df_uic_hierarchy = df_uic_hierarchy.sort_values(by=['asg_uic_pde','fy' ])
# Store df_uic_hierarchy
store_feather(df_uic_hierarchy,'df_uic_hierarchy')

# Now build and save uic_lookup_dict
df_dict = df_uic_hierarchy.copy().dropna(subset='asg_uic_pde')
df_dict = df_dict[['asg_uic','asg_uic_pde']].dropna(subset=['asg_uic','asg_uic_pde']).drop_duplicates()
uic_lookup_dict = dict(zip(df_dict.asg_uic, df_dict.asg_uic_pde))
store_json(uic_lookup_dict,'uic_lookup_dict',var_dir)
print("Storing 'uic_lookup_dict'... ")