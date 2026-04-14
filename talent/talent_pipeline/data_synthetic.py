# data_synthetic.py - Synthetic Dataset Creation for Army Officer Promotion Analysis
# =============================================================================
# This module creates realistic synthetic datasets for testing the promotion analysis
# without requiring access to live Army data.

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# === SECTION 1: IMPORTS & SETUP ===
def setup_synthetic_analysis():
    """Initialize synthetic analysis environment and parameters"""
    print("🎯 Setting up Synthetic Army Officer Promotion Analysis...")
    
    # Set random seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # Analysis parameters
    params = {
        'start_year': 2000,
        'end_year': 2022,
        'year_groups': [1996, 1997, 1998, 1999, 2000, 2001, 2002],
        'prestige_units': ['Ranger', 'SOAR', 'SF', 'SFAB'],
        'divisions': ['1ID', '2ID', '3ID', '4ID', '10MTN', '25ID', '82ABN', '101ABN', '1CAV', '2CAV'],
        'job_codes': ['IN', 'AR', 'AV', 'EN', 'FI', 'MI', 'MP', 'OD', 'QM', 'SC'],
        'uic_codes': ['WFAAT0', 'WFAAT1', 'WFAAT2', 'WFAAT3', 'WFAAT4', 'WFAAT5', 'WFAAT6', 'WFAAT7', 'WFAAT8', 'WFAAT9']
    }
    
    print(f"✅ Analysis parameters set: {len(params['year_groups'])} year groups, {len(params['divisions'])} divisions")
    return params

# === SECTION 2: CREATE PERSONNEL DATASET ===
def create_personnel_dataset(params):
    """Create realistic synthetic personnel dataset"""
    print("📊 Creating synthetic personnel dataset...")
    
    # Create officers
    n_officers = 1000
    officers = []
    
    for i in range(n_officers):
        # Basic demographics
        yg = random.choice(params['year_groups'])
        sex = random.choice(['M', 'F'])
        
        # Career timeline
        commission_date = datetime(yg, 6, 1)  # June 1st of year group
        cpt_date = commission_date + timedelta(days=random.randint(1095, 1460))  # 3-4 years to CPT
        maj_date = cpt_date + timedelta(days=random.randint(2190, 2555)) if random.random() > 0.3 else None  # 6-7 years from CPT to MAJ (70% promote)
        
        # Create quarterly snapshots during CPT period
        if maj_date:
            end_date = maj_date
        else:
            end_date = cpt_date + timedelta(days=random.randint(1095, 2190))  # Censored
            
        current_date = cpt_date
        while current_date <= end_date:
            # Time-varying variables - realistic age calculation
            # Commission at 21, so age = 21 + years since commission
            age = 21 + (current_date - commission_date).days / 365.25
            married = random.choice([0, 1]) if random.random() > 0.7 else 0  # 30% chance of marriage change
            job_code = random.choice(params['job_codes'])
            
            # Unit assignments
            if random.random() < 0.1:  # 10% in prestige units
                asg_uic_pde = random.choice(['RANGER', 'SOAR', 'SF', 'SFAB'])
                prestige_unit = 1
                top_name = asg_uic_pde
            else:  # 90% in regular divisions
                asg_uic_pde = random.choice(params['uic_codes'])
                prestige_unit = 0
                top_name = random.choice(params['divisions'])
            
            officers.append({
                'pid_pde': f'OFF{i:04d}',
                'snpsht_dt': current_date,
                'yg': yg,
                'sex': sex,
                'age': age,
                'married': married,
                'job_code': job_code,
                'asg_uic_pde': asg_uic_pde,
                'prestige_unit': prestige_unit,
                'top_name': top_name,
                'dor_cpt': cpt_date,
                'dor_maj': maj_date
            })
            
            # Move to next quarter
            current_date += timedelta(days=90)
    
    # Create DataFrame
    df = pd.DataFrame(officers)
    
    # Add static variables
    df['job_code_changed'] = df.groupby('pid_pde')['job_code'].transform(lambda x: len(x.unique()) > 1).astype(int)
    df['married_cpt'] = df.groupby('pid_pde')['married'].transform('first')
    df['age_cpt'] = df.groupby('pid_pde')['age'].transform('first')
    df['age_maj'] = df.groupby('pid_pde')['age'].transform('last')
    
    print(f"✅ Personnel dataset created: {len(df):,} records for {df['pid_pde'].nunique():,} officers")
    return df

# === SECTION 3: CREATE UNIT HIERARCHY DATASET ===
def create_unit_hierarchy_dataset(params):
    """Create synthetic unit hierarchy dataset"""
    print("📊 Creating synthetic unit hierarchy dataset...")
    
    hierarchy_data = []
    
    for fy in range(2018, 2027):  # 2018-2026
        for uic in params['uic_codes']:
            # Assign each UIC to a division
            division = random.choice(params['divisions'])
            hierarchy_data.append({
                'asg_uic_pde': uic,
                'top_name': division,
                'fy': str(fy)
            })
    
    df_hierarchy = pd.DataFrame(hierarchy_data)
    
    print(f"✅ Unit hierarchy dataset created: {len(df_hierarchy):,} records")
    return df_hierarchy

# === SECTION 4: CREATE PRESTIGE UNIT LISTS ===
def create_prestige_unit_lists(params):
    """Create synthetic prestige unit lists"""
    print("📊 Creating synthetic prestige unit lists...")
    
    prestige_lists = {
        'Ranger': ['RANGER', 'RANGER1', 'RANGER2', 'RANGER3'],
        'SOAR': ['SOAR', 'SOAR1', 'SOAR2', 'SOAR3'],
        'SF': ['SF', 'SF1', 'SF2', 'SF3', 'SF4', 'SF5'],
        'SFAB': ['SFAB', 'SFAB1', 'SFAB2', 'SFAB3']
    }
    
    print(f"✅ Prestige unit lists created: {sum(len(units) for units in prestige_lists.values())} total units")
    return prestige_lists

# === SECTION 5: MAIN EXECUTION ===
def generate_all_synthetic_datasets():
    """Generate all synthetic datasets for testing"""
    print("🚀 Generating all synthetic datasets...")
    
    # Setup
    params = setup_synthetic_analysis()
    
    # Create datasets
    personnel_df = create_personnel_dataset(params)
    hierarchy_df = create_unit_hierarchy_dataset(params)
    prestige_lists = create_prestige_unit_lists(params)
    
    # Return all datasets
    datasets = {
        'personnel': personnel_df,
        'hierarchy': hierarchy_df,
        'prestige_lists': prestige_lists,
        'params': params
    }
    
    print("🎯 All synthetic datasets generated successfully!")
    return datasets

# === TESTING FUNCTION ===
if __name__ == "__main__":
    # Generate all synthetic datasets
    datasets = generate_all_synthetic_datasets()
    
    # Display summary
    print("\n📊 Dataset Summary:")
    print(f"Personnel: {len(datasets['personnel']):,} records")
    print(f"Hierarchy: {len(datasets['hierarchy']):,} records")
    print(f"Prestige units: {sum(len(units) for units in datasets['prestige_lists'].values())} units")
    
    # Show sample data
    print("\n📋 Sample Personnel Data:")
    print(datasets['personnel'].head())
    
    print("\n📋 Sample Hierarchy Data:")
    print(datasets['hierarchy'].head())
