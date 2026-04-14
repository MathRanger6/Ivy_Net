# Cox Proportional Hazards Analysis for Military Promotion

This project analyzes time to promotion from Captain to Major using Cox proportional hazards regression.

## Overview

The analysis predicts how long it takes for military officers to be promoted from Captain (CPT) to Major (MAJ) based on various covariates.

### Key Features:
- **Event**: Promotion to Major (MAJ)
- **Time Start**: First Captain (CPT) snapshot
- **Time End**: Promotion to Major, leaving early, or study end (9/30/2007)
- **Covariates**: 
  - Time-invariant: Sex, Age at start
  - Time-dependent: Marriage status, Job code changes

### Censoring:
- **Right censoring**: Never promoted, left before study end
- **Study end**: 9/30/2007

## Data Structure

The data contains quarterly snapshots for each officer:
- `snpsht_dt`: Snapshot date
- `pid_pde`: Unique officer identifier
- `rank_pde`: Rank (CPT = Captain, MAJ = Major)
- `sex`: Sex (1 = Male, 0 = Female)
- `age`: Age at snapshot
- `job_code`: Military Occupational Specialty (MOS)
- `married`: Marriage status (1 = Married, 0 = Unmarried)

## Setup Instructions

### Option 1: Using Jupyter Notebook (Recommended)

1. Install Python and Jupyter:
   ```bash
   # Install Python from python.org or use Anaconda
   pip install jupyter
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Start Jupyter:
   ```bash
   jupyter notebook
   ```

4. Open `cox_analysis_notebook.ipynb` and run all cells

### Option 2: Using Python Script

1. Install Python and required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the analysis:
   ```bash
   python cox_work.py
   ```

## Files

- `cox_data.csv`: Input data with officer snapshots
- `cox_work.py`: Python script for analysis
- `cox_analysis_notebook.ipynb`: Jupyter notebook version
- `requirements.txt`: Required Python packages
- `README.md`: This file

## Output Files

After running the analysis, the following files will be created:
- `survival_data.csv`: Survival analysis dataset
- `long_format_data.csv`: Long format data with time-dependent covariates
- `cox_model_summary.txt`: Model results and summary
- `cox_analysis_results.png`: Main visualization plots
- `cox_diagnostic_plots.png`: Diagnostic plots

## Model Interpretation

The Cox proportional hazards model provides:
- **Hazard ratios**: Relative risk of promotion for different covariate values
- **P-values**: Statistical significance of each covariate
- **Concordance index**: Model discrimination ability
- **Survival curves**: Probability of remaining unpromoted over time

## Key Results

The analysis will show:
1. Which factors significantly affect promotion timing
2. How marriage status changes impact promotion probability
3. Whether job code changes affect promotion rates
4. Age and sex effects on promotion timing
5. Overall model fit and predictive ability

## Troubleshooting

If you encounter issues:

1. **Python not found**: Install Python from python.org or use Anaconda
2. **Package installation errors**: Try updating pip: `pip install --upgrade pip`
3. **Jupyter not starting**: Install with conda: `conda install jupyter`
4. **Data loading errors**: Ensure `cox_data.csv` is in the same directory

## Contact

For questions about the analysis or methodology, please refer to the code comments and documentation.

