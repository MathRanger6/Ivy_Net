"""Canonical paths under re_entry/HEROs_and_PASSes/."""

from __future__ import annotations

from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
HERO_ROOT = _REPO / "3-Master_Plan" / "re_entry" / "HEROs_and_PASSes"

PASS_A = HERO_ROOT / "pass_a"
PASS_B = HERO_ROOT / "pass_b"
PASS_C_RHO = HERO_ROOT / "pass_c_rho"
SORT_CHOP_LAMBDA = HERO_ROOT / "sort_chop_lambda"
THETA = HERO_ROOT / "theta"
SLIDES = HERO_ROOT / "slides"
# Hand-edited masters (scripts never write these).
SLIDES_AUTO = SLIDES / "auto"
HAND_PHASE_B_DECK = SLIDES / "CHAR_Phase_B_characterization.pptx"
HAND_RHO_DECK = SLIDES / "CHAR_rho_characterization.pptx"
HAND_LAMBDA_DECK = SLIDES / "CHAR_lambda_characterization.pptx"
HAND_THETA_DECK = SLIDES / "CHAR_theta_characterization.pptx"
HAND_GAMMA_DECK = SLIDES / "CHAR_gamma_characterization.pptx"
# Disposable script output — always *_AUTO.pptx under SLIDES_AUTO/.
AUTO_RHO_DECK = SLIDES_AUTO / "CHAR_rho_characterization_AUTO.pptx"
AUTO_LAMBDA_DECK = SLIDES_AUTO / "CHAR_lambda_characterization_AUTO.pptx"
AUTO_THETA_DECK = SLIDES_AUTO / "CHAR_theta_characterization_AUTO.pptx"
AUTO_GAMMA_DECK = SLIDES_AUTO / "CHAR_gamma_characterization_AUTO.pptx"
AUTO_PHASE_B_DECK = SLIDES_AUTO / "CHAR_Phase_B_characterization_AUTO.pptx"

_ALL_DIRS = (PASS_A, PASS_B, PASS_C_RHO, SORT_CHOP_LAMBDA, THETA, SLIDES, SLIDES_AUTO)


def ensure_hero_dirs() -> None:
    for d in _ALL_DIRS:
        d.mkdir(parents=True, exist_ok=True)
