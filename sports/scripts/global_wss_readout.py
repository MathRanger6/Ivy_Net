"""Shared readout lines for global WSS on LG slides."""

from __future__ import annotations


def global_wss_definition_bullet() -> str:
    return (
        r"global\_wss = \sum_j \sum_{i \in j} (\hat{A}_i - \hat{T}_j)^2 — "
        r"global within-team SS; $\hat{T}_j$ = realized roster mean."
    )


def global_wss_h_sort_link_bullet() -> str:
    return (
        r"$H_{sort} = 1 - \mathrm{global\_wss}/\mathrm{SS}_{total}$ on the same partition — "
        r"global\_wss is raw magnitude; $H_{sort}$ is scale-free explained variance."
    )


def global_wss_note_bullet() -> str:
    return (
        r"$\rho \uparrow$ sorting $\Rightarrow$ global\_wss $\downarrow$, $H_{sort} \uparrow$ "
        r"(monotone mirror on a fixed ability pool)."
    )
