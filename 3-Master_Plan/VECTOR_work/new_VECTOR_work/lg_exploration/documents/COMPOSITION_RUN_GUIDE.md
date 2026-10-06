# Run the first composition demonstration

Open notebooks/01_composition_opportunity_rules.ipynb from this exploration
folder. Choose the Python 3 kernel using sports_net. Review the settings cell,
set RUN_EXPERIMENT = True, then run all cells. The notebook uses the approved
2,000 players, 100 teams of 20, five rho values and 30 paired assignments.

The current notebook has no saved scientific outputs. Small validation outputs
are explicitly separate in results/validation/ and are not the demonstration.

After completion, leave RUN_EXPERIMENT = False for later figure review. Turning
it back on with the same settings verifies and reuses complete divisions.
Interruptions preserve completed units; use the same settings to resume.
Do not run a notebook and CLI concurrently against the same run.

The runner reports progress after every division. It saves a population file,
300 division checkpoints, a CSV of division summaries, metadata and a progress
log under results/composition_first/<scientific-run-id>/.
The notebook then saves five scientific figures as PNG and SVG in plots/:
team means, team variances, division summaries, paired sorting differences, and
the first paired repetition's actual roster compositions.

Distribution figures use consistent colors for rho. Error bars and distribution
shading show assignment SD, conditional on the single normal population.
They do not represent fresh-population uncertainty or pooled-player uncertainty.

## The same implementation from the CLI

From lg_exploration/ in an environment with NumPy and Matplotlib:

~~~sh
PYTHONPATH=code python -B -m lg_composition.experiment
~~~

This previews settings without executing. To explicitly run and plot:

~~~sh
PYTHONPATH=code python -B -m lg_composition.experiment --run --plots
~~~

To choose a project-local settings file, add --settings settings/<filename>.json.
Results paths must stay beneath this folder's results/ directory.

## Small checks

~~~sh
PYTHONPATH=code MPLBACKEND=Agg python -B code/test_composition.py -v
~~~

These validate probabilities, centroids, roster counts, variance decomposition,
random-grouping expectations, reproducibility, resume, damaged-checkpoint
handling and figure creation on a tiny population.

Code, settings, notebook and these documents are suitable for Git. Generated
results and notebook checkpoints are excluded by the existing local .gitignore;
ignore behavior was checked. Configure an explicit rsync scope before larger
runs. No synchronization, HPC submission or larger sweep was prepared here.
