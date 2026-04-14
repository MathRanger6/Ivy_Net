import pandas as pd
import numpy as np
from lifelines import CoxPHFitter
from lifelines.utils import to_long_format
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set random seed for reproducibility
np.random.seed(42)

def load_and_prepare_data(file_path='cox_data.csv'):
    """
    Load and prepare data for Cox proportional hazards analysis.
    
    Parameters:
    file_path (str): Path to the CSV file containing the data
    
    Returns:
    tuple: (long_format_data, original_data)
    """
    print("Loading and preparing data...")
    
    # Load the data
    df = pd.read_csv(file_path)
    
    # Clean the data - remove empty rows
    df = df.dropna(subset=['pid_pde', 'snpsht_dt'])
    
    # Convert snapshot date to datetime
    df['snpsht_dt'] = pd.to_datetime(df['snpsht_dt'])
    
    # Define study end date
    study_end = pd.to_datetime('2007-09-30')
    
    # Sort by pid_pde and snpsht_dt
    df = df.sort_values(['pid_pde', 'snpsht_dt']).reset_index(drop=True)
    
    return df

def create_survival_data(df):
    """
    Create survival analysis dataset with proper time-to-event structure.
    
    Parameters:
    df (DataFrame): Original data with snapshot information
    
    Returns:
    DataFrame: Survival analysis dataset
    """
    print("Creating survival analysis dataset...")
    
    # Define study end date
    study_end = pd.to_datetime('2007-09-30')
    
    # Initialize lists to store survival data
    survival_data = []
    
    # Process each person
    for pid in df['pid_pde'].unique():
        person_data = df[df['pid_pde'] == pid].copy()
        
        # Find first CPT snapshot (entry into study)
        first_cpt_idx = person_data[person_data['rank_pde'] == 'CPT'].index[0]
        first_cpt_date = person_data.loc[first_cpt_idx, 'snpsht_dt']
        
        # Check if person was promoted to MAJ
        maj_snapshots = person_data[person_data['rank_pde'] == 'MAJ']
        
        if len(maj_snapshots) > 0:
            # Person was promoted - find first MAJ date
            first_maj_date = maj_snapshots['snpsht_dt'].min()
            event_occurred = True
            time_to_event = (first_maj_date - first_cpt_date).days / 365.25  # Convert to years
        else:
            # Person was not promoted - check if they left early or stayed until end
            last_snapshot = person_data['snpsht_dt'].max()
            
            if last_snapshot < study_end:
                # Person left early
                time_to_event = (last_snapshot - first_cpt_date).days / 365.25
                event_occurred = False
            else:
                # Person stayed until end of study without promotion
                time_to_event = (study_end - first_cpt_date).days / 365.25
                event_occurred = False
        
        # Get baseline characteristics (from first CPT snapshot)
        baseline = person_data.loc[first_cpt_idx]
        
        # Create survival record
        survival_record = {
            'pid_pde': pid,
            'time': time_to_event,
            'event': event_occurred,
            'sex': baseline['sex'],
            'age_start': baseline['age'],
            'job_code_start': baseline['job_code'],
            'married_start': baseline['married']
        }
        
        survival_data.append(survival_record)
    
    return pd.DataFrame(survival_data)

def create_time_dependent_covariates(df):
    """
    Create time-dependent covariates for the analysis.
    
    Parameters:
    df (DataFrame): Original data with snapshot information
    
    Returns:
    DataFrame: Long format data with time-dependent covariates
    """
    print("Creating time-dependent covariates...")
    
    # Define study end date
    study_end = pd.to_datetime('2007-09-30')
    
    # Initialize lists for long format data
    long_data = []
    
    for pid in df['pid_pde'].unique():
        person_data = df[df['pid_pde'] == pid].copy()
        
        # Find first CPT snapshot
        first_cpt_idx = person_data[person_data['rank_pde'] == 'CPT'].index[0]
        first_cpt_date = person_data.loc[first_cpt_idx, 'snpsht_dt']
        
        # Get baseline characteristics
        baseline = person_data.loc[first_cpt_idx]
        
        # Track marriage status and job code changes
        current_married = baseline['married']
        current_job_code = baseline['job_code']
        job_changed = False
        
        # Process each snapshot after the first CPT
        for idx, row in person_data[person_data.index > first_cpt_idx].iterrows():
            # Check if this is still during CPT period
            if row['rank_pde'] != 'CPT':
                break
                
            # Calculate time since first CPT
            time_since_start = (row['snpsht_dt'] - first_cpt_date).days / 365.25
            
            # Check for marriage status change
            if row['married'] != current_married:
                current_married = row['married']
            
            # Check for job code change
            if row['job_code'] != current_job_code:
                current_job_code = row['job_code']
                job_changed = True
            
            # Add record to long format data
            long_record = {
                'pid_pde': pid,
                'start_time': time_since_start,
                'end_time': time_since_start + 0.25,  # Quarter length
                'married': current_married,
                'job_changed': job_changed,
                'sex': baseline['sex'],
                'age_start': baseline['age'],
                'job_code_start': baseline['job_code']
            }
            
            long_data.append(long_record)
            
            # Reset job_changed flag for next period
            job_changed = False
    
    return pd.DataFrame(long_data)

def run_cox_analysis(survival_data, long_data):
    """
    Run Cox proportional hazards analysis.
    
    Parameters:
    survival_data (DataFrame): Survival analysis dataset
    long_data (DataFrame): Long format data with time-dependent covariates
    
    Returns:
    CoxPHFitter: Fitted Cox model
    """
    print("Running Cox proportional hazards analysis...")
    
    # Merge survival data with long format data
    analysis_data = long_data.merge(survival_data[['pid_pde', 'time', 'event']], 
                                   on='pid_pde', how='left')
    
    # Create Cox model
    cph = CoxPHFitter()
    
    # Fit the model with time-dependent covariates
    cph.fit(analysis_data, 
            duration_col='time', 
            event_col='event',
            start_col='start_time',
            stop_col='end_time',
            id_col='pid_pde',
            covariates=['married', 'job_changed', 'sex', 'age_start'])
    
    return cph

def analyze_results(cph, survival_data):
    """
    Analyze and display results from the Cox model.
    
    Parameters:
    cph (CoxPHFitter): Fitted Cox model
    survival_data (DataFrame): Survival analysis dataset
    """
    print("\n" + "="*60)
    print("COX PROPORTIONAL HAZARDS ANALYSIS RESULTS")
    print("="*60)
    
    # Print model summary
    print("\nModel Summary:")
    print(cph.print_summary())
    
    # Print baseline hazard
    print(f"\nBaseline Hazard: {cph.baseline_hazard_:.4f}")
    
    # Print concordance index
    print(f"Concordance Index: {cph.concordance_index_:.4f}")
    
    # Print AIC
    print(f"AIC: {cph.AIC_:.4f}")
    
    # Create visualizations
    create_plots(cph, survival_data)

def create_plots(cph, survival_data):
    """
    Create visualizations for the Cox analysis.
    
    Parameters:
    cph (CoxPHFitter): Fitted Cox model
    survival_data (DataFrame): Survival analysis dataset
    """
    print("\nCreating visualizations...")
    
    # Set up the plotting style
    plt.style.use('default')
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. Survival function plot
    cph.plot_survival_function(ax=axes[0,0])
    axes[0,0].set_title('Survival Function')
    axes[0,0].set_xlabel('Time (years)')
    axes[0,0].set_ylabel('Survival Probability')
    
    # 2. Hazard function plot
    cph.plot_hazard(ax=axes[0,1])
    axes[0,1].set_title('Hazard Function')
    axes[0,1].set_xlabel('Time (years)')
    axes[0,1].set_ylabel('Hazard Rate')
    
    # 3. Partial effects plot
    cph.plot_partial_effects('married', ax=axes[1,0])
    axes[1,0].set_title('Partial Effect of Marriage Status')
    
    # 4. Event distribution
    event_counts = survival_data['event'].value_counts()
    axes[1,1].pie(event_counts.values, labels=['Censored', 'Promoted'], autopct='%1.1f%%')
    axes[1,1].set_title('Event Distribution')
    
    plt.tight_layout()
    plt.savefig('cox_analysis_results.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Create additional plots
    create_additional_plots(cph, survival_data)

def create_additional_plots(cph, survival_data):
    """
    Create additional diagnostic plots.
    
    Parameters:
    cph (CoxPHFitter): Fitted Cox model
    survival_data (DataFrame): Survival analysis dataset
    """
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. Schoenfeld residuals plot
    cph.plot_partial_effects_on_outcome('married', ax=axes[0,0])
    axes[0,0].set_title('Partial Effects on Outcome - Marriage')
    
    # 2. Age distribution by event status
    axes[0,1].hist(survival_data[survival_data['event']==True]['age_start'], 
                   alpha=0.7, label='Promoted', bins=10)
    axes[0,1].hist(survival_data[survival_data['event']==False]['age_start'], 
                   alpha=0.7, label='Censored', bins=10)
    axes[0,1].set_xlabel('Age at Start')
    axes[0,1].set_ylabel('Frequency')
    axes[0,1].set_title('Age Distribution by Event Status')
    axes[0,1].legend()
    
    # 3. Time to event distribution
    axes[1,0].hist(survival_data['time'], bins=15, alpha=0.7)
    axes[1,0].set_xlabel('Time to Event (years)')
    axes[1,0].set_ylabel('Frequency')
    axes[1,0].set_title('Distribution of Time to Event')
    
    # 4. Sex distribution by event status
    sex_event = pd.crosstab(survival_data['sex'], survival_data['event'], 
                           margins=True, normalize='index')
    sex_event.plot(kind='bar', ax=axes[1,1])
    axes[1,1].set_title('Event Status by Sex')
    axes[1,1].set_xlabel('Sex (1=Male, 0=Female)')
    axes[1,1].set_ylabel('Proportion')
    
    plt.tight_layout()
    plt.savefig('cox_diagnostic_plots.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """
    Main function to run the complete Cox analysis.
    """
    print("Starting Cox Proportional Hazards Analysis")
    print("="*50)
    
    # Load and prepare data
    df = load_and_prepare_data()
    
    # Create survival dataset
    survival_data = create_survival_data(df)
    
    # Create time-dependent covariates
    long_data = create_time_dependent_covariates(df)
    
    # Print data summary
    print(f"\nData Summary:")
    print(f"Total individuals: {len(survival_data)}")
    print(f"Events (promotions): {survival_data['event'].sum()}")
    print(f"Censored: {(~survival_data['event']).sum()}")
    print(f"Event rate: {survival_data['event'].mean():.2%}")
    
    print(f"\nTime Summary:")
    print(f"Mean time to event: {survival_data['time'].mean():.2f} years")
    print(f"Median time to event: {survival_data['time'].median():.2f} years")
    print(f"Min time: {survival_data['time'].min():.2f} years")
    print(f"Max time: {survival_data['time'].max():.2f} years")
    
    # Run Cox analysis
    cph = run_cox_analysis(survival_data, long_data)
    
    # Analyze results
    analyze_results(cph, survival_data)
    
    # Save results
    save_results(cph, survival_data, long_data)
    
    print("\nAnalysis complete! Results saved to files.")

def save_results(cph, survival_data, long_data):
    """
    Save analysis results to files.
    
    Parameters:
    cph (CoxPHFitter): Fitted Cox model
    survival_data (DataFrame): Survival analysis dataset
    long_data (DataFrame): Long format data
    """
    # Save survival data
    survival_data.to_csv('survival_data.csv', index=False)
    
    # Save long format data
    long_data.to_csv('long_format_data.csv', index=False)
    
    # Save model summary
    with open('cox_model_summary.txt', 'w') as f:
        f.write("COX PROPORTIONAL HAZARDS MODEL SUMMARY\n")
        f.write("="*50 + "\n\n")
        f.write(cph.print_summary().to_string())
        f.write(f"\n\nConcordance Index: {cph.concordance_index_:.4f}")
        f.write(f"\nAIC: {cph.AIC_:.4f}")
        f.write(f"\nBaseline Hazard: {cph.baseline_hazard_:.4f}")

if __name__ == "__main__":
    main()
