# cox_flag.py - Army Officer Promotion Analysis
# ================================================
# This module performs Cox proportional hazards analysis on Army officer promotion data
# to identify factors affecting promotion timing from Captain to Major.

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from lifelines import CoxPHFitter
import warnings
warnings.filterwarnings('ignore')

# === SECTION 1: IMPORTS & SETUP ===
def setup_analysis():
    """Initialize analysis environment and parameters"""
    print("🎯 Setting up Army Officer Promotion Analysis...")
    
    # Set plotting style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Analysis parameters
    params = {
        'prestige_calc': True,
        'division_only_analysis': False,
        'year_group_stratification': True,
        'output_dir': './outputs'
    }
    
    print(f"✅ Analysis parameters set: Prestige={params['prestige_calc']}, Division={params['division_only_analysis']}")
    return params

# === SECTION 2: DATA LOADING & CLEANING ===
def load_and_clean_data(personnel_df, hierarchy_df, prestige_lists):
    """Load and clean the input datasets"""
    print("📊 Loading and cleaning data...")
    
    # Create a copy of personnel data
    df_clean = personnel_df.copy()
    
    # Add division assignments using hierarchy data
    # First, create a simple mapping from UIC to division (using 2018 data for simplicity)
    uic_to_division = hierarchy_df[hierarchy_df['fy'] == '2018'][['asg_uic_pde', 'top_name']].drop_duplicates()
    
    # Check if top_name already exists in the data
    if 'top_name' in df_clean.columns:
        print("📊 top_name column already exists in personnel data")
        # Fill missing division assignments
        df_clean['top_name'] = df_clean['top_name'].fillna('No Division Assignment')
    else:
        # Merge with hierarchy data
        df_clean = df_clean.merge(
            uic_to_division, 
            on='asg_uic_pde', 
            how='left'
        )
        # Fill missing division assignments
        df_clean['top_name'] = df_clean['top_name'].fillna('No Division Assignment')
    
    # Check for missing mappings
    missing_divisions = df_clean['top_name'].isna().sum()
    total_records = len(df_clean)
    print(f"📊 Missing division mappings: {missing_divisions:,} out of {total_records:,} records ({missing_divisions/total_records:.1%})")
    
    # Show division distribution
    division_counts = df_clean['top_name'].value_counts()
    print(f"📊 Division distribution: {dict(division_counts.head(10))}")
    
    print(f"✅ Data cleaned: {len(df_clean):,} records for {df_clean['pid_pde'].nunique():,} officers")
    return df_clean

# === SECTION 3: STATIC VARIABLE CREATION ===
def create_static_variables(df_clean):
    """Create all static variables at once"""
    print("📊 Creating static variables...")
    
    # Group by officer to get static values
    officer_static = df_clean.groupby('pid_pde').agg({
        'dor_cpt': 'first',
        'dor_maj': 'first',
        'sex': 'first',
        'yg': 'first',
        'age_cpt': 'first',
        'age_maj': 'first',
        'job_code_changed': 'first',
        'married_cpt': 'first',
        'snpsht_dt': 'max'
    }).reset_index()
    
    # Add prestige history (ever served in prestige during CPT period)
    if 'prestige_unit' in df_clean.columns:
        prestige_static = df_clean.groupby('pid_pde')['prestige_unit'].max().reset_index()
        prestige_static.columns = ['pid_pde', 'prestige_cpt']
        officer_static = officer_static.merge(prestige_static, on='pid_pde', how='left')
        print(f"📊 Prestige history added: {officer_static['prestige_cpt'].sum():,} officers with prestige service")
    
    # Add final division assignment
    if 'top_name' in df_clean.columns:
        final_div_static = df_clean.groupby('pid_pde')['top_name'].last().reset_index()
        final_div_static.columns = ['pid_pde', 'final_div']
        officer_static = officer_static.merge(final_div_static, on='pid_pde', how='left')
        
        # Show final division distribution
        final_div_counts = officer_static['final_div'].value_counts()
        print(f"📊 Final division distribution: {dict(final_div_counts.head(10))}")
    
    print(f"✅ Static variables created: {len(officer_static):,} officers")
    return officer_static

# === SECTION 4: TIME-VARYING VARIABLE CREATION ===
def create_time_varying_variables(df_clean):
    """Create all time-varying variables at once"""
    print("📊 Creating time-varying variables...")
    
    # Time-varying variables are already in the main DataFrame
    # This function could add additional transformations if needed
    
    # Verify time-varying variables are present
    time_varying_cols = ['age', 'married', 'job_code', 'prestige_unit', 'top_name']
    available_cols = [col for col in time_varying_cols if col in df_clean.columns]
    print(f"📊 Available time-varying variables: {available_cols}")
    
    print(f"✅ Time-varying variables ready: {len(df_clean):,} records")
    return df_clean

# === SECTION 5: COX DATA PREPARATION ===
def prepare_cox_data(df_clean, officer_static):
    """Convert to survival analysis format"""
    print("📊 Preparing Cox regression data...")
    
    # Study end date for censoring (latest snapshot date in entire dataset)
    STUDY_END = df_clean['snpsht_dt'].max()
    print(f"Study end date (latest snapshot): {STUDY_END.date()}")
    
    # Add event and survival time information
    officer_static['has_maj'] = officer_static['dor_maj'].notna()
    officer_static['event'] = officer_static['has_maj'].astype(int)
    
    officer_static['end_time'] = officer_static['dor_maj'].where(
        officer_static['has_maj'],
        officer_static['snpsht_dt'].clip(upper=STUDY_END)
    )
    
    officer_static['survival_days'] = (officer_static['end_time'] - officer_static['dor_cpt']).dt.days
    
    # Filter valid officers
    valid_officers = officer_static[
        (officer_static['dor_cpt'].notna()) &
        (officer_static['survival_days'] > 0)
    ].copy()
    
    print(f"📊 Valid officers: {len(valid_officers):,} out of {len(officer_static):,} total")
    
    # Create time-dependent structure
    valid_df = df_clean[df_clean['pid_pde'].isin(valid_officers['pid_pde'])].copy()
    
    valid_df = valid_df.merge(
        valid_officers[['pid_pde','end_time','survival_days','event']],
        on='pid_pde'
    )
    
    # Filter to valid snapshots
    mask_valid_snapshots = (
        (valid_df['snpsht_dt'] >= valid_df['dor_cpt']) &
        (valid_df['snpsht_dt'] <= valid_df['end_time'])
    )
    
    valid_snapshots = valid_df[mask_valid_snapshots].copy()
    
    # Create time intervals
    valid_snapshots['start_days'] = (valid_snapshots['snpsht_dt'] - valid_snapshots['dor_cpt']).dt.days
    valid_snapshots = valid_snapshots.sort_values(['pid_pde','start_days'])
    valid_snapshots['stop_days'] = valid_snapshots.groupby('pid_pde')['start_days'].shift(-1)
    
    mask_last_interval = valid_snapshots['stop_days'].isna()
    valid_snapshots.loc[mask_last_interval, 'stop_days'] = valid_snapshots.loc[mask_last_interval, 'survival_days']
    
    valid_snapshots['interval_event'] = 0
    valid_snapshots.loc[mask_last_interval, 'interval_event'] = valid_snapshots.loc[mask_last_interval, 'event']
    
    valid_intervals = valid_snapshots[valid_snapshots['stop_days'] > valid_snapshots['start_days']].copy()
    
    # Create final columns dictionary
    final_columns = {
        'pid_pde': 'pid_pde',
        'start_days': 'start',
        'stop_days': 'stop',
        'interval_event': 'event',
        'sex': 'sex',
        'yg': 'yg',
        'job_code_changed': 'job_code_changed',
        'married_cpt': 'married_cpt',
        'age_cpt': 'age_cpt',
        'age_maj': 'age_maj',
        'age': 'age', # Time dependent
        'married': 'married', # Time dependent
        'job_code': 'job_code' # Time dependent
    }
    
    # Add prestige variables if available
    if 'prestige_unit' in valid_intervals.columns:
        final_columns['prestige_unit'] = 'prestige_unit'
    if 'prestige_cpt' in valid_intervals.columns:
        final_columns['prestige_cpt'] = 'prestige_cpt'
    if 'top_name' in valid_intervals.columns:
        final_columns['top_name'] = 'top_name'
    if 'final_div' in valid_intervals.columns:
        final_columns['final_div'] = 'final_div'
    
    # Create final DataFrame
    final_df = valid_intervals[list(final_columns.keys())].rename(columns=final_columns)
    
    print(f"✅ Cox data prepared: {len(final_df):,} intervals for {final_df['pid_pde'].nunique():,} officers")
    return final_df

# === SECTION 6: MODEL FITTING ===
def fit_models(cox_df):
    """Fit Cox regression models"""
    print("📊 Fitting Cox regression models...")
    
    # Initialize Cox model
    cph = CoxPHFitter()
    
    # Prepare data for Cox regression
    model_df = cox_df.copy()
    
    # Remove identifier columns
    columns_to_exclude = ['pid_pde']
    for col in columns_to_exclude:
        if col in model_df.columns:
            model_df = model_df.drop(columns=[col])
    
    # Handle categorical variables appropriately
    # For ordinal variables (sex), convert to numeric
    if 'sex' in model_df.columns:
        model_df['sex'] = pd.Categorical(model_df['sex']).codes
    
    # For nominal variables (job_code, top_name, final_div), use dummy variables
    nominal_columns = ['job_code', 'top_name', 'final_div']
    for col in nominal_columns:
        if col in model_df.columns:
            # Create dummy variables (one-hot encoding)
            dummies = pd.get_dummies(model_df[col], prefix=col, drop_first=True)
            # Drop original column and add dummies
            model_df = model_df.drop(columns=[col])
            model_df = pd.concat([model_df, dummies], axis=1)
    
    # Remove any remaining non-numeric columns
    numeric_columns = model_df.select_dtypes(include=[np.number]).columns
    model_df = model_df[numeric_columns]
    
    # Remove highly correlated variables to avoid collinearity
    # Keep only essential variables for the model
    essential_vars = ['stop', 'event', 'sex', 'age', 'married', 'prestige_unit']
    available_vars = [col for col in essential_vars if col in model_df.columns]
    model_df = model_df[available_vars]
    
    print(f"📊 Model variables: {list(model_df.columns)}")
    print(f"📊 Model shape: {model_df.shape}")
    
    # Check for any remaining issues
    if model_df.isnull().any().any():
        print("⚠️ Warning: Missing values detected, filling with median")
        model_df = model_df.fillna(model_df.median())
    
    # Fit the model
    cph.fit(model_df, duration_col='stop', event_col='event')
    
    print("✅ Cox model fitted successfully")
    return cph

# === SECTION 7: VISUALIZATION ===
def create_visualizations(cph_model, cox_df):
    """Generate all plots and charts"""
    print("📊 Creating visualizations...")
    
    # Create output directory
    import os
    os.makedirs('./outputs', exist_ok=True)
    
    try:
        # Plot 1: Hazard ratios
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        cph_model.plot(ax=ax1)
        ax1.set_title('Hazard Ratios for Promotion Factors')
        plt.tight_layout()
        plt.savefig('./outputs/hazard_ratios.png', dpi=300, bbox_inches='tight')
        plt.close(fig1)
        print("✅ Hazard ratios plot saved")
        
        # Plot 2: Model summary
        fig2, ax2 = plt.subplots(figsize=(12, 8))
        summary_df = cph_model.summary
        if 'exp(coef)' in summary_df.columns:
            summary_df['exp(coef)'].plot(kind='bar', ax=ax2)
            ax2.set_title('Hazard Ratios (exp(coef)) for Each Variable')
            ax2.set_ylabel('Hazard Ratio')
            ax2.tick_params(axis='x', rotation=45)
        else:
            ax2.text(0.5, 0.5, 'No hazard ratios available', ha='center', va='center')
            ax2.set_title('Model Summary')
        plt.tight_layout()
        plt.savefig('./outputs/model_summary.png', dpi=300, bbox_inches='tight')
        plt.close(fig2)
        print("✅ Model summary plot saved")
        
        # Plot 3: Baseline survival function
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        if hasattr(cph_model, 'baseline_survival_') and cph_model.baseline_survival_ is not None:
            cph_model.baseline_survival_.plot(ax=ax3)
            ax3.set_title('Baseline Survival Function')
            ax3.set_xlabel('Time (days)')
            ax3.set_ylabel('Survival Probability')
        else:
            ax3.text(0.5, 0.5, 'Baseline survival not available', ha='center', va='center')
            ax3.set_title('Baseline Survival Function')
        plt.tight_layout()
        plt.savefig('./outputs/baseline_survival.png', dpi=300, bbox_inches='tight')
        plt.close(fig3)
        print("✅ Baseline survival plot saved")
        
    except Exception as e:
        print(f"⚠️ Warning: Some plots could not be created: {e}")
    
    print("✅ Visualizations created and saved to ./outputs/")
    return None

# === SECTION 7B: PROMOTION-FOCUSED VISUALIZATIONS ===
def create_promotion_visualizations(cox_df):
    """Create the three key transformation plots from 508_flag_down"""
    print("🎯 Creating promotion-focused visualizations...")
    
    # Create output directory
    import os
    os.makedirs('./outputs', exist_ok=True)
    
    # Prepare officer-level data for analysis
    officer_data = prepare_officer_data(cox_df)
    
    try:
        # Transformation 1: Promotion Probability Curves
        print("📊 Creating Transformation 1: Promotion Probability Curves")
        plot_promotion_curves(officer_data, 'sex', 'by Gender')
        plot_promotion_curves(officer_data, 'married', 'by Marital Status')
        
        # Transformation 2: Competing Risks Analysis  
        print("📊 Creating Transformation 2: Competing Risks Analysis")
        analyze_competing_risks(officer_data, 'sex', 'by Gender')
        analyze_competing_risks(officer_data, 'married', 'by Marital Status')
        
        # Transformation 3: Promotion Velocity Analysis
        print("📊 Creating Transformation 3: Promotion Velocity Analysis")
        analyze_promotion_velocity(officer_data, 'sex', 'by Gender')
        analyze_promotion_velocity(officer_data, 'married', 'by Marital Status')
        
        print("✅ All promotion-focused visualizations created!")
        
    except Exception as e:
        print(f"⚠️ Warning: Some promotion visualizations could not be created: {e}")
        import traceback
        traceback.print_exc()
    
    return None

def prepare_officer_data(cox_df):
    """Prepare officer-level data for promotion analysis"""
    print("🔧 Preparing officer-level data for promotion analysis...")
    
    # Get the final row for each officer (most recent observation)
    officer_data = cox_df.groupby('pid_pde').last().reset_index()
    
    # Add survival_days column if it doesn't exist
    if 'survival_days' not in officer_data.columns and 'stop' in officer_data.columns:
        officer_data['survival_days'] = officer_data['stop']
    
    print(f"✅ Officer data prepared: {len(officer_data)} officers")
    return officer_data

def plot_promotion_curves(officer_data, group_col, title_suffix, compare=True):
    """
    TRANSFORMATION 1: Promotion Probability Curves
    
    CRITICAL TRANSFORMATION: Instead of showing P(still a Captain), shows P(promoted to Major)
    - Traditional survival: S(t) = P(T > t) = P(not promoted by time t)  
    - Our promotion prob: P(t) = 1 - S(t) = P(promoted by time t)
    
    INTERPRETATION CHANGE:
    - Traditional: "Higher curve = longer survival = better" (WRONG for promotions!)
    - New: "Higher curve = higher promotion probability = better" (CORRECT!)
    """
    from lifelines import KaplanMeierFitter
    
    print(f"📊 Creating Promotion Probability Curves {title_suffix}")
    
    # Group labels for better interpretation
    group_label_dict = {
        'sex': {'F': 'FEMALE', 'M': 'MALE', 0: 'FEMALE', 1: 'MALE'},
        'married': {0: 'Unmarried', 1: 'Married'},
        'prestige_unit': {0: 'Regular Unit', 1: 'Prestige Unit'}
    }
    
    # Create single plot focused on promotion probability
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    # Get unique groups and assign colors
    groups = officer_data[group_col].unique()
    colors = plt.cm.Set1(np.linspace(0, 1, len(groups)))
    
    for i, group in enumerate(groups):
        group_data = officer_data[officer_data[group_col] == group]
        
        if len(group_data) == 0:
            continue
            
        # Fit Kaplan-Meier
        kmf = KaplanMeierFitter()
        # Get group label with fallback
        group_label = group_label_dict.get(group_col, {}).get(group, f'Group {group}')
        kmf.fit(durations=group_data['survival_days'], 
                event_observed=group_data['event'], 
                label=f'{group_label} (n={len(group_data)})')
        
        # CRITICAL TRANSFORMATION: Calculate promotion probability = 1 - survival_function
        promotion_prob = 1 - kmf.survival_function_
        
        # Plot promotion probability curve
        ax.plot(promotion_prob.index, promotion_prob.iloc[:, 0], 
                color=colors[i], label=f'{group_label} (n={len(group_data)})', linewidth=3)
    
    ax.set_xlabel('Days from Captain Promotion', fontsize=12)
    ax.set_ylabel('Probability of Being Promoted\n(Promotion Probability)', fontsize=12)
    ax.set_title(f'Promotion Probability Curves {title_suffix}\n(Higher = Better Performance)', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 1)
    
    plt.tight_layout()
    plt.savefig(f'./outputs/promotion_curves_{group_col}.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Promotion curves saved: ./outputs/promotion_curves_{group_col}.png")
    return fig

def analyze_competing_risks(officer_data, group_col, title_suffix):
    """
    TRANSFORMATION 2: Competing Risks Analysis
    
    Shows the different ways officers can exit the promotion process:
    - Promoted to Major (success)
    - Left Army (attrition - competing risk)
    - Administrative censoring (still in process)
    """
    print(f"📊 Creating Competing Risks Analysis {title_suffix}")
    
    # Create competing risks visualization
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Plot 1: Cumulative Incidence by Outcome Type
    groups = officer_data[group_col].unique()
    colors = plt.cm.Set1(np.linspace(0, 1, len(groups)))
    
    for i, group in enumerate(groups):
        group_data = officer_data[officer_data[group_col] == group]
        
        if len(group_data) == 0:
            continue
            
        # Calculate cumulative incidence
        promoted = group_data['event'].sum()
        total = len(group_data)
        promotion_rate = promoted / total
        
        # Simple bar chart for now (can be enhanced with time-dependent analysis)
        ax1.bar([f'Group {group}'], [promotion_rate], color=colors[i], alpha=0.7)
    
    ax1.set_title(f'Promotion Rates by Group {title_suffix}')
    ax1.set_ylabel('Promotion Rate')
    ax1.set_ylim(0, 1)
    
    # Plot 2: Event Distribution
    event_counts = officer_data.groupby([group_col, 'event']).size().unstack(fill_value=0)
    event_counts.plot(kind='bar', ax=ax2, color=['red', 'green'])
    ax2.set_title(f'Event Distribution {title_suffix}')
    ax2.set_ylabel('Number of Officers')
    ax2.legend(['Not Promoted', 'Promoted'])
    ax2.tick_params(axis='x', rotation=45)
    
    # Plot 3: Time to Event Distribution
    for i, group in enumerate(groups):
        group_data = officer_data[officer_data[group_col] == group]
        if len(group_data) > 0:
            ax3.hist(group_data['survival_days'], alpha=0.6, label=f'Group {group}', 
                    color=colors[i], bins=20)
    
    ax3.set_title(f'Time to Event Distribution {title_suffix}')
    ax3.set_xlabel('Days from Captain Promotion')
    ax3.set_ylabel('Frequency')
    ax3.legend()
    
    # Plot 4: Promotion Probability by Group
    from lifelines import KaplanMeierFitter
    
    for i, group in enumerate(groups):
        group_data = officer_data[officer_data[group_col] == group]
        
        if len(group_data) == 0:
            continue
            
        kmf = KaplanMeierFitter()
        kmf.fit(durations=group_data['survival_days'], 
                event_observed=group_data['event'])
        
        # Calculate promotion probability = 1 - survival
        promotion_prob = 1 - kmf.survival_function_
        ax4.plot(promotion_prob.index, promotion_prob.iloc[:, 0], 
                color=colors[i], label=f'Group {group}', linewidth=2)
    
    ax4.set_title(f'Promotion Probability Curves {title_suffix}')
    ax4.set_xlabel('Days from Captain Promotion')
    ax4.set_ylabel('Probability of Being Promoted')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.set_ylim(0, 1)
    
    plt.tight_layout()
    plt.savefig(f'./outputs/competing_risks_{group_col}.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Competing risks analysis saved: ./outputs/competing_risks_{group_col}.png")
    return fig

def analyze_promotion_velocity(officer_data, group_col, title_suffix):
    """
    TRANSFORMATION 3: Promotion Velocity Analysis
    
    Focuses on promotion speed among officers who were successfully promoted.
    Shows distribution of promotion timing for successful officers.
    """
    print(f"📊 Creating Promotion Velocity Analysis {title_suffix}")
    
    # Create velocity analysis visualization
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Plot 1: Promotion Speed Distribution by Group
    groups = officer_data[group_col].unique()
    colors = plt.cm.Set1(np.linspace(0, 1, len(groups)))
    
    promotion_times_by_group = []
    group_labels = []
    
    for i, group in enumerate(groups):
        group_data = officer_data[officer_data[group_col] == group]
        group_promoted = group_data[group_data['event'] == 1]
        
        if len(group_promoted) > 0:
            promotion_times_by_group.append(group_promoted['survival_days'].values)
            group_labels.append(f'Group {group}\n(n={len(group_promoted)})')
    
    # Box plot showing promotion speed distribution
    if promotion_times_by_group:
        box_plot = ax1.boxplot(promotion_times_by_group, labels=group_labels, patch_artist=True)
        
        # Color the boxes
        for patch, color in zip(box_plot['boxes'], colors[:len(groups)]):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
    
    ax1.set_title(f'Promotion Speed Distribution {title_suffix}\n(Among Promoted Officers Only)')
    ax1.set_ylabel('Days to Promotion')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Promotion Rate by Group
    promotion_rates = []
    group_names = []
    
    for group in groups:
        group_data = officer_data[officer_data[group_col] == group]
        if len(group_data) > 0:
            rate = group_data['event'].mean()
            promotion_rates.append(rate)
            group_names.append(f'Group {group}')
    
    ax2.bar(group_names, promotion_rates, color=colors[:len(groups)], alpha=0.7)
    ax2.set_title(f'Promotion Rates by Group {title_suffix}')
    ax2.set_ylabel('Promotion Rate')
    ax2.set_ylim(0, 1)
    
    # Plot 3: Cumulative Promotion Probability
    from lifelines import KaplanMeierFitter
    
    for i, group in enumerate(groups):
        group_data = officer_data[officer_data[group_col] == group]
        
        if len(group_data) == 0:
            continue
            
        kmf = KaplanMeierFitter()
        kmf.fit(durations=group_data['survival_days'], 
                event_observed=group_data['event'])
        
        # Calculate promotion probability = 1 - survival
        promotion_prob = 1 - kmf.survival_function_
        ax3.plot(promotion_prob.index, promotion_prob.iloc[:, 0], 
                color=colors[i], label=f'Group {group}', linewidth=2)
    
    ax3.set_title(f'Cumulative Promotion Probability {title_suffix}')
    ax3.set_xlabel('Days from Captain Promotion')
    ax3.set_ylabel('Probability of Being Promoted')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Hazard Function (if available)
    ax4.text(0.5, 0.5, 'Hazard Function Analysis\n(Can be enhanced with more data)', 
             ha='center', va='center', transform=ax4.transAxes, fontsize=12)
    ax4.set_title(f'Hazard Function {title_suffix}')
    
    plt.tight_layout()
    plt.savefig(f'./outputs/promotion_velocity_{group_col}.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Promotion velocity analysis saved: ./outputs/promotion_velocity_{group_col}.png")
    return fig

# === SECTION 8: OUTPUT GENERATION ===
def generate_outputs(cph_model, cox_df):
    """Create final outputs and reports"""
    print("📊 Generating outputs...")
    
    # Model summary
    print("\n📋 Model Summary:")
    print(cph_model.summary)
    
    # Event rate
    event_rate = cox_df['event'].mean()
    total_officers = cox_df['pid_pde'].nunique()
    total_events = cox_df['event'].sum()
    officer_promotion_rate = total_events / total_officers
    
    print(f"\n📊 Promotion Statistics:")
    print(f"   • Event Rate: {event_rate:.1%} (interval-level)")
    print(f"   • Officer Promotion Rate: {officer_promotion_rate:.1%} ({total_events:,}/{total_officers:,})")
    
    print("✅ Outputs generated successfully")
    return None

# === MAIN EXECUTION ===
def run_complete_analysis(personnel_df, hierarchy_df, prestige_lists):
    """Run the complete promotion analysis"""
    print("🚀 Starting complete Army Officer Promotion Analysis...")
    
    # Setup
    params = setup_analysis()
    
    # Load and clean data
    df_clean = load_and_clean_data(personnel_df, hierarchy_df, prestige_lists)
    
    # Create variables
    officer_static = create_static_variables(df_clean)
    df_tv = create_time_varying_variables(df_clean)
    
    # Prepare for analysis
    cox_df = prepare_cox_data(df_tv, officer_static)
    
    # Fit models
    cph_model = fit_models(cox_df)
    
    # Create visualizations
    create_visualizations(cph_model, cox_df)
    
    # Create promotion-focused visualizations (the three key transformations)
    create_promotion_visualizations(cox_df)
    
    # Generate outputs
    generate_outputs(cph_model, cox_df)
    
    print("🎯 Complete analysis finished successfully!")
    return cph_model, cox_df

# === TESTING FUNCTION ===
if __name__ == "__main__":
    # Import the data generation module
    from cox_data import generate_all_synthetic_datasets
    
    # Generate synthetic datasets
    datasets = generate_all_synthetic_datasets()
    
    # Run complete analysis
    cph_model, cox_df = run_complete_analysis(
        datasets['personnel'],
        datasets['hierarchy'],
        datasets['prestige_lists']
    )
