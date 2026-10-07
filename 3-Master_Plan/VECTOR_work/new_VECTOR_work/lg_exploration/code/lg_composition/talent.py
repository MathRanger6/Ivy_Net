"""Talent laws and theoretical scaling; never sample-standardize the players."""
from dataclasses import dataclass, fields
import hashlib
import math
from pathlib import Path
import numpy as np
from .experiment import Settings, code_digest, describe, draw_inputs, load_unit, run_id


@dataclass(frozen=True)
class TalentSettings(Settings):
    talent_distribution: str = "normal"
    weibull_shape: float = 2.0
    talent_scale: str = "theoretical_mean_sd"
    population_mode: str = "same"

    def validate(self):
        super().validate()
        if self.talent_distribution not in ("normal", "uniform", "beta", "weibull"):
            raise ValueError("Talent distribution must be normal, uniform, beta or weibull")
        if self.talent_scale not in ("theoretical_mean_sd", "original"):
            raise ValueError("Talent scale must be theoretical_mean_sd or original")
        if not np.isfinite(self.weibull_shape) or self.weibull_shape <= 0:
            raise ValueError("Weibull shape must be finite and positive")
        if self.population_mode not in ("same", "fresh"):
            raise ValueError("Population mode must be same or fresh")
        theoretical_moments(self)

    @property
    def legacy_compatible(self):
        return (self.population_mode == "same" and self.talent_distribution == "normal"
                and self.talent_scale == "theoretical_mean_sd")

    def scientific_dict(self):
        # Construct the original base class so normal IDs stay exactly compatible.
        base = Settings(**{f.name: getattr(self, f.name) for f in fields(Settings)})
        value = base.scientific_dict()
        if not self.legacy_compatible:
            value.update(distribution=self.talent_distribution,
                         distribution_parameters=({"alpha": 2., "beta": 2.}
                            if self.talent_distribution == "beta" else
                            {"low": 0., "high": 1.}
                            if self.talent_distribution == "uniform" else
                            {"shape": self.weibull_shape, "scale": 1.}
                            if self.talent_distribution == "weibull" else
                            {"mean": 0., "sd": 1.}),
                         transformation=self.talent_scale,
                         talent_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
        if self.population_mode == "fresh":
            value.update(population_repetitions=self.assignment_repetitions,
                         population_mode="fresh",
                         population_stream="SeedSequence([population_seed, 3, repetition])")
        return value


def theoretical_moments(settings):
    if settings.talent_distribution == "normal":
        return 0., 1.
    if settings.talent_distribution == "beta":
        return .5, math.sqrt(1 / 20)
    if settings.talent_distribution == "uniform":
        return .5, math.sqrt(1 / 12)
    try:
        mean = math.gamma(1 + 1 / settings.weibull_shape)
        variance = math.gamma(1 + 2 / settings.weibull_shape) - mean**2
    except (OverflowError, ValueError) as error:
        raise ValueError("Weibull shape has unrepresentable theoretical moments") from error
    if not math.isfinite(variance) or variance <= 0:
        raise ValueError("Weibull shape has unusable theoretical variance")
    return mean, math.sqrt(variance)


def draw_population(settings, repetition=0):
    settings.validate()
    if isinstance(repetition, bool) or not isinstance(repetition, int) or not 0 <= repetition < settings.assignment_repetitions:
        raise ValueError("Population repetition index is outside the selected run")
    seed = (settings.population_seed if settings.population_mode == "same" else
            np.random.SeedSequence([settings.population_seed, 3, repetition]))
    rng = np.random.default_rng(seed)
    if settings.talent_distribution == "normal":
        raw = rng.normal(size=settings.n_players)
    elif settings.talent_distribution == "uniform":
        raw = rng.uniform(0., 1., size=settings.n_players)
    elif settings.talent_distribution == "beta":
        raw = rng.beta(2., 2., size=settings.n_players)
    else:
        raw = rng.weibull(settings.weibull_shape, size=settings.n_players)
    mean, sd = theoretical_moments(settings)
    ability = (raw - mean) / sd if settings.talent_scale == "theoretical_mean_sd" else raw.copy()
    if not np.all(np.isfinite(ability)) or np.var(ability) <= 0:
        raise ValueError("Talent population must have finite, positive variance")
    return raw, ability


def load_talent_unit(path, settings, rho, repetition, rule, ability):
    if settings.legacy_compatible:
        return load_unit(path, settings, rho, repetition, rule, ability)
    raw, expected_ability = draw_population(settings, repetition)
    with np.load(path, allow_pickle=False) as archive:
        unit = {key: archive[key].copy() for key in archive.files}
    for key, expected in (("run_id", run_id(settings)), ("source_sha256", code_digest()),
                          ("rule", rule), ("rho", rho), ("repetition", repetition),
                          ("population_seed", settings.population_seed),
                          ("assignment_seed", settings.assignment_seed)):
        if unit[key].item() != expected:
            raise ValueError(f"Checkpoint metadata mismatch: {path.name}, {key}")
    for key, expected in (("original_draws", raw), ("ability", expected_ability),
                          ("player_id", np.arange(settings.n_players))):
        if not np.array_equal(unit[key], expected):
            raise ValueError(f"Checkpoint population mismatch: {key}")
    if not np.array_equal(ability, expected_ability):
        raise ValueError("Loaded population differs from configured talent")
    order, uniforms = draw_inputs(settings, repetition)
    for key, expected in (("arrival_order", order), ("choice_uniforms", uniforms)):
        if not np.array_equal(unit[key], expected):
            raise ValueError(f"Checkpoint random inputs mismatch: {key}")
    summary = describe(ability, unit["team_id"], settings.n_teams)
    if not np.all(summary["team_sizes"] == settings.roster_size):
        raise ValueError("Checkpoint roster sizes mismatch")
    for key, value in summary.items():
        if not np.allclose(unit[key], value, rtol=1e-12, atol=1e-12):
            raise ValueError(f"Checkpoint statistic mismatch: {key}")
    if not np.array_equal(unit["capacities"], summary["team_sizes"]):
        raise ValueError("Checkpoint capacities mismatch")
    return unit
