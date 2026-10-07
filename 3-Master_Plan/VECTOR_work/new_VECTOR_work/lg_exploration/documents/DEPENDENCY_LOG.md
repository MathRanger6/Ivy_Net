# Composition demonstration dependencies

Prepared 6 October 2026 by Leo. Project root is lg_exploration/.

Scientific source: the supplied, untouched
reference_snapshot/sports/541_grandchild_homophily_assign.py. Its package manifest
SHA-256 is b6983d0b0a0cedfe3ca439ff830113824dc0f101fe2707f2b042532e745df666.
The local adaptation preserves sequential random seating, evolving actual-member
centroids and remaining-seat opportunity probabilities. It introduces a paired
inverse-CDF sampler, stable log normalization, and the explicitly distinct
one-opportunity-per-open-team comparison.

Third-party libraries checked in the existing sports_net environment:
NumPy 2.4.6 and Matplotlib 3.11.0. Remaining computation/storage uses the Python
standard library. There are no imports from other research folders, no empirical
datasets, and no missing scientific supporting modules for this first stage.

Jupyter support, nbformat and ipykernel are also available. The registered
python3 kernel points to the sports_net Python executable. A notebook interface
itself was not installed or launched by Leo.
The same computation is available from the CLI. No packages were installed.

Run metadata records a SHA-256 of the local scientific implementation. Each
checkpoint records that digest, scientific run ID, seeds and explicit random
inputs. Code changes produce a new run directory rather than reusing divisions
from a different implementation.

Later SCORE, mosaic and MLE adapters may need further supplied modules; audit
those stages when requested, report exact missing imports, and keep folder-only
scope.

Talent-law extension: NumPy Generator.normal/beta/weibull supplies local random
draws; Python standard-library math.gamma supplies theoretical Weibull moments.
No external data, new packages or original source modifications are required.
