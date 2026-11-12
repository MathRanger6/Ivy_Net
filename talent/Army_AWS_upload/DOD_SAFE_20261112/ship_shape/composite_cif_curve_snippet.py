def composite_cif_curve_and_bars(path_cr_plot, path_bar_plot, path_out, dpi=300):
    """
    Build a single image for slides: 2x2 layout from saved CIF curve plot and CIF bar plot.
    Left column: Promotion CIF curve (top), Promotion CIF bars (bottom).
    Right column: Attrition CIF curve (top), Attrition CIF bars (bottom).
    Both input PNGs are assumed to be two-panel figures (top=promo, bottom=attrition).
    """
    from matplotlib import image as mpl_image
    if not os.path.isfile(path_cr_plot) or not os.path.isfile(path_bar_plot):
        return None
    cr_img = mpl_image.imread(path_cr_plot)
    bar_img = mpl_image.imread(path_bar_plot)
    H_cr, W_cr = cr_img.shape[:2]
    H_bar, W_bar = bar_img.shape[:2]
    # Top half = promo, bottom half = attrition (both figures)
    promo_curve = cr_img[: H_cr // 2, :]
    attr_curve = cr_img[H_cr // 2 :, :]
    promo_bar = bar_img[: H_bar // 2, :]
    attr_bar = bar_img[H_bar // 2 :, :]
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes[0, 0].imshow(promo_curve)
    axes[0, 0].set_title("Promotion (CIF curve)", fontsize=11, fontweight="bold")
    axes[0, 0].axis("off")
    axes[0, 1].imshow(attr_curve)
    axes[0, 1].set_title("Attrition (CIF curve)", fontsize=11, fontweight="bold")
    axes[0, 1].axis("off")
    axes[1, 0].imshow(promo_bar)
    axes[1, 0].set_title("Promotion (CIF bars)", fontsize=11, fontweight="bold")
    axes[1, 0].axis("off")
    axes[1, 1].imshow(attr_bar)
    axes[1, 1].set_title("Attrition (CIF bars)", fontsize=11, fontweight="bold")
    axes[1, 1].axis("off")
    plt.tight_layout()
    fig.savefig(path_out, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    return path_out