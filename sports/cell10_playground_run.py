# Executed by 537 notebook Cell 10 via exec(..., globals()).
# Knob labels & dropdown options: cell10_knob_catalog.py (shared with faithful sweep PNG titles).

try:
    import html
    import io

    import ipywidgets as widgets
    import json
    from pathlib import Path

    from IPython.display import display

    import sys

    _repo = Path.cwd().resolve()
    for _add in (_repo, _repo / "sports"):
        if (_add / "cell10_knob_catalog.py").is_file():
            if str(_add) not in sys.path:
                sys.path.insert(0, str(_add))
            break
    import cell10_knob_catalog as knobs
except ImportError:
    print("Install ipywidgets (e.g. pip install ipywidgets or conda install ipywidgets), then restart the kernel.")
else:
    style = {"description_width": "160px"}
    lay = widgets.Layout(width="440px")

    PLAYGROUND_STATE_PATH = Path("sports/cell10_playground_state.json")

    def _playground_state_load():
        if not PLAYGROUND_STATE_PATH.is_file():
            return {}
        try:
            return json.loads(PLAYGROUND_STATE_PATH.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}

    _pk = _playground_state_load()
    _pbx0 = str(_pk.get("person_x_binning", "equal_count"))
    if _pbx0 not in ("equal_count", "equal_width"):
        _pbx0 = "equal_count"

    w_noise = widgets.FloatSlider(
        value=float(_pk.get("noise", SORTING_NOISE_SD)),
        min=0.0,
        max=float(INTERACTIVE_SORTING_NOISE_MAX),
        step=0.005,
        description="Sorting noise sd",
        continuous_update=False,
        style=style,
        layout=lay,
    )
    w_additive = widgets.FloatSlider(
        value=float(_pk.get("additive", ADDITIVE_LOCAL_RANK_WEIGHT)),
        min=0.0,
        max=1.0,
        step=0.01,
        description="ADDITIVE w (local-rank share)",
        continuous_update=False,
        readout_format=".2f",
        style=style,
        layout=lay,
    )
    w_runs = widgets.IntSlider(
        value=max(20, min(500, int(_pk.get("runs", INTERACTIVE_N_RUNS)))),
        min=20,
        max=500,
        step=10,
        description="Runs (playground)",
        continuous_update=False,
        style=style,
        layout=lay,
    )
    w_n = widgets.IntSlider(
        value=max(200, min(2000, int(_pk.get("n_indiv", INTERACTIVE_N_INDIVIDUALS)))),
        min=200,
        max=2000,
        step=100,
        description="N individuals",
        continuous_update=False,
        style=style,
        layout=lay,
    )
    w_k = widgets.IntSlider(
        value=max(1, min(200, int(_pk.get("n_winners", N_WINNERS)))),
        min=1,
        max=200,
        step=1,
        description="Promotions per run (K)",
        continuous_update=False,
        style=style,
        layout=lay,
    )
    w_n_pools = widgets.IntSlider(
        value=max(2, min(200, int(_pk.get("n_pools", N_POOLS)))),
        min=2,
        max=200,
        step=1,
        description="Pools (#)",
        continuous_update=False,
        style=style,
        layout=lay,
    )
    w_pool = widgets.Dropdown(
        options=knobs.POOL_ASSIGNMENT_OPTIONS,
        value=str(_pk.get("pool", "B")),
        description="Pool assignment",
        style=style,
        layout=lay,
    )
    w_score = widgets.Dropdown(
        options=knobs.SCORE_MODE_OPTIONS,
        value=str(_pk.get("score", "local_rank_plus_ability")),
        description="Promotion score",
        style=style,
        layout=lay,
    )
    w_bins = widgets.IntSlider(
        value=max(5, min(40, int(_pk.get("bins", INTERACTIVE_N_BINS)))),
        min=5,
        max=40,
        step=1,
        description="Person bins (#)",
        continuous_update=False,
        style=style,
        layout=lay,
    )
    w_person_x_binning = widgets.Dropdown(
        options=knobs.PERSON_X_BINNING_OPTIONS,
        value=_pbx0,
        description="Person x edges",
        style=style,
        layout=widgets.Layout(width="420px"),
    )
    w_pool_bins = widgets.IntSlider(
        value=max(2, min(40, int(_pk.get("pool_bins", globals().get("INTERACTIVE_N_POOL_AGG_BINS", 8))))),
        min=2,
        max=40,
        step=1,
        description="Pool–talent bins (#)",
        continuous_update=False,
        style=style,
        layout=lay,
    )
    w_binning_mode = widgets.Dropdown(
        options=knobs.BINNING_MODE_OPTIONS,
        value=str(_pk.get("binning_mode", "individual_qcut")),
        description="Binning",
        style=style,
        layout=widgets.Layout(width="560px"),
    )
    w_view = widgets.Dropdown(
        options=knobs.VIEW_MODE_OPTIONS,
        value=str(_pk.get("view", "pool_local")),
        description="Plot (x-axis)",
        style=style,
        layout=widgets.Layout(width="480px"),
    )
    w_ability = widgets.Dropdown(
        options=knobs.ABILITY_OPTIONS,
        value=str(_pk.get("ability", str(ABILITY_DISTRIBUTION_CHOICE))),
        description="A_i distribution",
        style=style,
        layout=lay,
    )
    w_winner = widgets.Dropdown(
        options=knobs.WINNER_OPTIONS,
        value=str(_pk.get("winner", str(WINNER_SELECTION_CHOICE))),
        description="Winner draw",
        style=style,
        layout=lay,
    )
    _ma0 = float(_pk.get("min_A_promote", globals().get("MIN_ABILITY_FOR_PROMOTION", 0.0)))
    w_min_A = widgets.FloatSlider(
        value=max(0.0, min(1.0, _ma0)),
        min=0.0,
        max=1.0,
        step=0.005,
        readout_format=".3f",
        description="Min A to promote",
        continuous_update=False,
        style=style,
        layout=lay,
    )

    btn_defaults = widgets.Button(
        description="Load defaults from sim_config.py",
        tooltip="Reload sim_config into the Python kernel and copy its scalars into the sliders/dropdowns.",
        layout=widgets.Layout(width="340px"),
    )

    def _sync_playground_controls():
        bmode = str(w_binning_mode.value)
        smode = str(w_score.value)
        w_additive.disabled = smode == "local_rank"
        w_bins.disabled = bmode != "individual_qcut"
        w_person_x_binning.disabled = bmode != "individual_qcut"
        w_pool_bins.disabled = bmode not in ("pool_equal_count", "pool_equal_width")

    eda_png = widgets.Image(
        format="png",
        layout=widgets.Layout(width="auto", max_height="960px"),
    )
    summary_lbl = widgets.HTML(value="", layout=widgets.Layout(width="100%"))
    _playground_ready = False
    _pg = {"busy": False, "listeners_on": False}

    def _persist_playground_knobs():
        try:
            PLAYGROUND_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
            PLAYGROUND_STATE_PATH.write_text(
                json.dumps(
                    {
                        "noise": float(w_noise.value),
                        "additive": float(w_additive.value),
                        "runs": int(w_runs.value),
                        "n_indiv": int(w_n.value),
                        "pool": str(w_pool.value),
                        "score": str(w_score.value),
                        "bins": int(w_bins.value),
                        "pool_bins": int(w_pool_bins.value),
                        "n_winners": int(w_k.value),
                        "n_pools": int(w_n_pools.value),
                        "binning_mode": str(w_binning_mode.value),
                        "view": str(w_view.value),
                        "ability": str(w_ability.value),
                        "winner": str(w_winner.value),
                        "person_x_binning": str(w_person_x_binning.value),
                        "min_A_promote": float(w_min_A.value),
                    },
                    indent=2,
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
            )
        except OSError:
            pass

    def redraw(_=None):
        if _pg["busy"]:
            return
        _pg["busy"] = True
        was_interactive = plt.isinteractive()
        plt.ioff()
        try:
            plt.close("all")
            summary_lbl.value = ""
            noise = float(w_noise.value)
            wgt = float(w_additive.value)
            min_a_cut = float(w_min_A.value)
            n_play = int(w_n.value)
            nruns = int(w_runs.value)
            ibins = int(w_bins.value)
            pbins = int(w_pool_bins.value)
            n_promo = int(w_k.value)
            n_pools_play = int(w_n_pools.value)
            pool = w_pool.value
            smode = w_score.value
            abil = str(w_ability.value)
            wchoice = str(w_winner.value)
            view = str(w_view.value)
            bmode = str(w_binning_mode.value)
            pxb = str(w_person_x_binning.value)

            if smode == "local_rank":
                lr_w = 0.5
                meta_lr_w = None
            else:
                lr_w = wgt
                meta_lr_w = wgt

            w_additive.disabled = smode == "local_rank"
            _sync_playground_controls()

            pg_extra = (
                "CELL 10 EDA · Widget values above are authoritative for this plot "
                "(faithful sweep PNG titles use the same knob phrases). "
                "FIG_PLAYGROUND_EDA_INCHES."
            )

            p_in = float(globals().get("FIG_PANEL_IN", 5.8))
            fig_wh = globals().get("FIG_PLAYGROUND_EDA_INCHES", (p_in * 1.4, p_in * 1.15))
            fig_w, fig_h = float(fig_wh[0]), float(fig_wh[1])
            fig, ax = plt.subplots(figsize=(fig_w, fig_h))

            seed_main = int(RANDOM_SEED + 7010)
            seed_nopool = int(RANDOM_SEED + 7000)

            if bmode in ("pool_equal_count", "pool_equal_width") and view == "nopool_global":
                summary_lbl.value = (
                    "<pre>Pool-level binning needs pools. "
                    "Pick a pooled Plot (x-axis) or set Binning to individuals.</pre>"
                )
                plt.close(fig)
                return

            if bmode == "pool_equal_count" and int(n_pools_play) < pbins:
                summary_lbl.value = (
                    f"<pre>Equal-count pool bins need Pools (#) ({int(n_pools_play)}) ≥ "
                    f"Pool–talent bins (#) ({pbins}). Raise Pools (#) or lower pool–talent bins.</pre>"
                )
                plt.close(fig)
                return

            use_pool_agg = bmode in ("pool_equal_count", "pool_equal_width")

            if view == "nopool_global":
                df = simulate_population_rows(
                    seed=seed_nopool,
                    n_runs=nruns,
                    n=n_play,
                    k=n_promo,
                    ability_choice=abil,
                    winner_choice=wchoice,
                    score_mode="global_rank",
                    include_random_pools=False,
                    min_ability_for_promotion=min_a_cut,
                )
                xcol = "global_rank_score"
                summ = summarize_by_bins(df, xcol, ibins, label=xcol, person_binning=pxb)
                summ = summ.sort_values("x_mean", kind="mergesort")
                title = "No pools: promotion vs global rank"
                xlab = "Global rank score"
                _pxtag = "equal-count" if pxb == "equal_count" else "equal-width"
                meta = build_plot_meta(
                    score_mode="global_rank",
                    x_binned=f"global_rank_score: {ibins} person bins ({_pxtag})",
                    seed=seed_nopool,
                    winner_choice=wchoice,
                    ability_choice=abil,
                    pool_assignment_choice=None,
                    n_pools=None,
                    sorting_noise_sd=None,
                    local_rank_weight=None,
                    min_ability_for_promotion=min_a_cut,
                    n_individuals=n_play,
                    n_winners=n_promo,
                    n_runs=nruns,
                    n_bins=ibins,
                    caption_extra=pg_extra,
                )
                plot_bin_summary(summ, title, xlab, ax=ax, plot_meta=meta)
            else:
                df = simulate_population_rows(
                    seed=seed_main,
                    n_runs=nruns,
                    n=n_play,
                    k=n_promo,
                    ability_choice=abil,
                    winner_choice=wchoice,
                    score_mode=smode,
                    include_random_pools=True,
                    n_pools=n_pools_play,
                    pool_assignment_choice=pool,
                    sorting_noise_sd=noise,
                    local_rank_weight=lr_w,
                    min_ability_for_promotion=min_a_cut,
                )
                if use_pool_agg:
                    pool_m = "equal_count" if bmode == "pool_equal_count" else "equal_width"
                    try:
                        summ = summarize_by_pool_mean_A_bins(df, pbins, method=pool_m)
                    except ValueError as e:
                        summary_lbl.value = f"<pre>{html.escape(str(e))}</pre>"
                        plt.close(fig)
                        return
                    per_pool = n_play // int(n_pools_play) if int(n_pools_play) else 0
                    title = "Promotion vs mean LOO peer A (pool–talent bins)"
                    if pool_m == "equal_count":
                        x_b = (
                            f"pools: equal COUNT / bin ({pbins}), sorted by mean A; "
                            f"~{float(summ['n_pools'].mean()):.1f} pools/bin; ~{per_pool} people/pool; "
                            f"x = mean leave-one-out peer A in bin (poolq_loo analog)"
                        )
                    else:
                        x_b = (
                            f"pools: equal WIDTH on mean A ({pbins} intervals per run, [min,max] of pool means); "
                            f"~{per_pool} people/pool; "
                            f"x = mean leave-one-out peer A in bin (poolq_loo analog)"
                        )
                    meta = build_plot_meta(
                        score_mode=smode,
                        x_binned=x_b,
                        seed=seed_main,
                        winner_choice=wchoice,
                        ability_choice=abil,
                        pool_assignment_choice=pool,
                        n_pools=n_pools_play,
                        sorting_noise_sd=noise,
                        local_rank_weight=meta_lr_w,
                        min_ability_for_promotion=min_a_cut,
                        n_individuals=n_play,
                        n_winners=n_promo,
                        n_runs=nruns,
                        n_bins=pbins,
                        caption_extra=pg_extra,
                    )
                    plot_pool_A_bin_summary(summ, title, ax=ax, plot_meta=meta)
                else:
                    if view == "pool_local":
                        xcol = "local_rank_score"
                        xlab = "Local rank score"
                        title = "With pools: promotion vs local rank"
                        x_b = (
                            f"local_rank_score: {ibins} person bins ("
                            f"{'equal-count' if pxb == 'equal_count' else 'equal-width'})"
                        )
                    elif view == "pool_global":
                        xcol = "global_rank_score"
                        xlab = "Global rank score"
                        title = "With pools: promotion vs global rank"
                        x_b = (
                            f"global_rank_score: {ibins} person bins ("
                            f"{'equal-count' if pxb == 'equal_count' else 'equal-width'})"
                        )
                    else:
                        xcol = "A"
                        xlab = "Ability A_i"
                        title = "With pools: promotion vs ability A_i"
                        x_b = (
                            f"A: {ibins} person bins ("
                            f"{'equal-count' if pxb == 'equal_count' else 'equal-width'})"
                        )
                    summ = summarize_by_bins(df, xcol, ibins, label=xcol, person_binning=pxb)
                    summ = summ.sort_values("x_mean", kind="mergesort")
                    meta = build_plot_meta(
                        score_mode=smode,
                        x_binned=x_b,
                        seed=seed_main,
                        winner_choice=wchoice,
                        ability_choice=abil,
                        pool_assignment_choice=pool,
                        n_pools=n_pools_play,
                        sorting_noise_sd=noise,
                        local_rank_weight=meta_lr_w,
                        min_ability_for_promotion=min_a_cut,
                        n_individuals=n_play,
                        n_winners=n_promo,
                        n_runs=nruns,
                        n_bins=ibins,
                        caption_extra=pg_extra,
                    )
                    plot_bin_summary(summ, title, xlab, ax=ax, plot_meta=meta)

            fig.subplots_adjust(bottom=0.40, top=0.94)
            buf = io.BytesIO()
            fig.savefig(
                buf,
                format="png",
                dpi=144,
                bbox_inches="tight",
                facecolor=fig.get_facecolor(),
                edgecolor="none",
            )
            buf.seek(0)
            eda_png.value = buf.getvalue()
            plt.close(fig)
            pm = float(df["promoted"].mean())
            extra = ""
            if use_pool_agg:
                extra = (
                    f"  x_loo_mean(bin) [{float(summ['x_loo_mean'].min()):.3f}, "
                    f"{float(summ['x_loo_mean'].max()):.3f}]"
                )
            line = (
                f"bmode={bmode} view={view}  mean promote={pm:.4f}  rows={len(df):,}  "
                f"summary_len={len(summ)}  n min/max={int(summ['n'].min())}/{int(summ['n'].max())}"
                f"{extra}"
            )
            summary_lbl.value = f"<pre>{html.escape(line)}</pre>"
        finally:
            _pg["busy"] = False
            if was_interactive:
                plt.ion()
            try:
                _persist_playground_knobs()
            except Exception:
                pass


    btn = widgets.Button(description="Run / refresh")
    btn.on_click(redraw)

    def _on_change(change):
        if not (_playground_ready and _pg["listeners_on"]):
            return
        if "old" in change and "new" in change and change["old"] == change["new"]:
            return
        redraw()

    def _on_binning_mode_change(change):
        if change.get("name") != "value":
            return
        if "old" in change and "new" in change and change["old"] == change["new"]:
            return
        _sync_playground_controls()
        if _playground_ready and _pg["listeners_on"]:
            redraw()

    def _apply_sim_config_defaults(_=None):
        if "reload_sim_config" in globals():
            reload_sim_config(verbose=False)
        w_noise.value = float(SORTING_NOISE_SD)
        w_additive.value = float(ADDITIVE_LOCAL_RANK_WEIGHT)
        w_runs.value = max(20, min(500, int(N_RUNS)))
        w_n.value = max(200, min(2000, int(N_INDIVIDUALS)))
        w_k.value = max(1, min(200, int(N_WINNERS)))
        w_n_pools.value = max(2, min(200, int(N_POOLS)))
        w_bins.value = max(5, min(40, int(N_BINS)))
        w_pool_bins.value = max(2, min(40, int(N_POOL_AGG_BINS)))
        w_min_A.value = float(MIN_ABILITY_FOR_PROMOTION)
        w_ability.value = str(ABILITY_DISTRIBUTION_CHOICE)
        w_winner.value = str(WINNER_SELECTION_CHOICE)
        choices = globals().get("LOCAL_POOL_ASSIGNMENT_CHOICES_SIM3", ("B",))
        w_pool.value = str(choices[0]) if choices else "B"
        _sync_playground_controls()
        redraw()

    btn_defaults.on_click(_apply_sim_config_defaults)


    for w_ctrl in (
        w_noise,
        w_additive,
        w_runs,
        w_n,
        w_k,
        w_n_pools,
        w_pool,
        w_score,
        w_bins,
        w_person_x_binning,
        w_pool_bins,
        w_view,
        w_ability,
        w_winner,
        w_min_A,
    ):
        w_ctrl.observe(_on_change, names="value")
    w_binning_mode.observe(_on_binning_mode_change, names="value")

    ui = widgets.VBox(
        [
            widgets.HTML(
                "<p><b>EDA:</b> one plot + caption under the axis. "
                "<b>All sliders and dropdowns on this panel drive the simulation</b> (they are authoritative for Cell 10). "
                "<code>sports/sim_config.py</code> is only the default snapshot: use <b>Load defaults from sim_config.py</b> "
                "after you edit that file (Cell 0 reload). Faithful 537 sweep candidate PNGs reuse the same knob wording. "
                "See <code>sports/documents/537_Manual.md</code>.</p>"
            ),
            widgets.HBox([btn_defaults]),
            w_binning_mode,
            w_view,
            widgets.HBox([w_ability, w_winner]),
            widgets.HBox([w_min_A]),
            widgets.HBox([w_noise, w_additive]),
            widgets.HBox([w_runs, w_n]),
            widgets.HBox([w_k, w_n_pools]),
            widgets.HBox([w_bins, w_person_x_binning, w_pool_bins]),
            widgets.HBox([w_pool, w_score]),
            widgets.HBox([btn]),
            eda_png,
            summary_lbl,
        ]
    )
    display(ui)
    _playground_ready = True
    _sync_playground_controls()
    redraw()
    _pg["listeners_on"] = True



