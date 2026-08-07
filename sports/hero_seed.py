"""Canonical stochastic seed for Phase B gallery + tier1 playground.

Override at runtime:
  export GALLERY_HERO_SEED=99

Consumers: gallery_knobs.HERO_SEED, tier1_sim_config.RANDOM_SEED,
tier1_sim_config.MATCH_539_RANDOM_SEED, rebuild_hero_gallery.sh,
build_characterization_slides.sh.
"""

from __future__ import annotations

import os

DEFAULT_HERO_SEED = 42


def read_hero_seed(default: int = DEFAULT_HERO_SEED) -> int:
    val = os.environ.get("GALLERY_HERO_SEED")
    if val is None or val == "":
        return default
    return int(val)


HERO_SEED = read_hero_seed()
