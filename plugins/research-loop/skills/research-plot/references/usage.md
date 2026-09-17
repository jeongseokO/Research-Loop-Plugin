# Shared Matplotlib style

Use Python with Matplotlib in an existing environment. The helper has no network, research-data access or upload side effects. Resolve the skill directory from this reference's location, not a machine-specific path. Write data/scripts/exports in the user's working directory, never in the installed plugin.

## Import and export

For this **synthetic example only**, save the code as a local script and pass the absolute skill directory and output directory as its two arguments. Replace the inputs with verified data for research. If sharing the unchanged example, identify it as synthetic in the external caption.

```python
import json
import sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(sys.argv[1]).resolve() / "scripts"))
from research_plot import style_context, draw_delta_panel, save_figure

with style_context():
    fig, ax = plt.subplots(figsize=(7, 4), layout="constrained")
    draw_delta_panel(ax, ["Condition A", "Condition B", "Condition C"], [1.2, -0.8, 0])
    ax.set(xlabel="Δ score (points)")
    manifest = save_figure(fig, Path(sys.argv[2]) / "comparison")
    plt.close(fig)
print(json.dumps(manifest))
```

The style applies to ordinary Matplotlib plots too: call `style_axes(ax, grid="y")` for curves or distributions, `grid="x"` for horizontal comparisons, or `grid=None` for a heatmap. The asset [research-loop.mplstyle](../assets/research-loop.mplstyle) is reusable without the helper, but font discovery, export handling and annotations then remain the caller's responsibility.

## Helper API

- `style_context(font_paths=(), portable=True)`: temporary plotting defaults; yields the selected font family. Prefer NanumSquare, otherwise an installed fallback. Optional local font paths are explicit inputs; no font download. Inspect Korean/math glyphs even if a fallback was selected. Custom font files should be trusted local assets.
- `style_axes(ax, grid="y")`: quiet grid and axes, without altering values or scale limits. `grid` accepts `"x"`, `"y"`, or `None`.
- `delta_limits(values)`: data-derived symmetric limits for deltas. For comparable panels, pass the combined values once and reuse the limits. Never reuse the illustrative `[-7, 7]` range blindly.
- `draw_delta_panel(ax, labels, values, title=None, limits=None)`: signed horizontal bars and endpoint values, preserving input order. Zero is neutral. Returns Matplotlib bars. Explicit limits must include zero and all values; labels move inward when those limits leave little room. A title, if used, is a short panel identifier, not an explanation. This helper does not compute averages, rank models, calculate uncertainty or know whether higher is better.
- `save_figure(fig, output_stem, dpi=300, portable=True, overwrite=False)`: PNG, PDF and SVG plus a small manifest containing actual byte sizes and SHA-256. Existing exports are preserved unless you explicitly choose `overwrite=True`. Default portable SVG uses glyph paths to avoid relying on the reader's font installation; preserve the Python source for edits. `portable=False` keeps SVG text for editing where matching fonts exist. It does not upload or save research pages.

## Adapt deliberately

Use `BLUE`, `ORANGE`, `GRAY`, `PURPLE` from the helper. Keep each entity's color consistent across comparable figures; gray is context, not an excuse to hide a meaningful comparator. Purple can emphasize a declared criterion but is not an automatic best-model rule. Add markers or line styles when colors must be distinguishable.

Choose ranges from all observations and available intervals. Absolute bars start at zero; deltas include zero. Heatmaps use a continuous sequential or zero-centered diverging map. Do not apply blue/orange categories to continuous intensity. Keep missing observations missing.

Prefer a few readable direct value labels over dense numbers. Retain the full data in the source/table and show material uncertainty when available. At narrow page widths, split a multi-panel figure rather than shrink its text. Keep prose outside the canvas, including explanations placed in a title or blank margin.

Keep inputs, units, aggregation code and figure source alongside the exports. Open the PNG before attaching; verify saved links with the Research Loop workflow. A valid manifest proves file bytes, not scientific correctness or legibility.
