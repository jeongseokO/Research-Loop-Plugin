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
print(json.dumps(manifest))
```

Run the local script through `<plugin-root>/scripts/render_guard.py` using the
same Python environment: `python <plugin-root>/scripts/render_guard.py plot.py
<skill-directory> <output-directory>`. Resolve the actual paths from this
installed skill. The guard starts a single process, forces common numerical
library thread settings to one, and stops the job after 60 seconds. `--timeout`
before the script may choose a smaller limit or at most 120 seconds. A same-user
lock rejects overlapping guarded jobs instead of queuing them. On POSIX a timeout
kills the process group; on Windows it kills the Python worker. Do not spawn child
jobs from the plotting script. Use your server's scheduler/cgroup/container for
hard CPU and memory quotas; this launcher is not a sandbox.

The guard controls the whole script only when you launch through it. Importing
the helper directly does not add a timeout or prevent concurrent callers. A
stopped custom script may leave its own files: write exports into a dedicated
working directory and inspect failed output before reusing it. Do not wrap the
method-figure command in this guard; that command already starts a guarded worker.

The style applies to ordinary Matplotlib plots too: call `style_axes(ax, grid="y")` for curves or distributions, `grid="x"` for horizontal comparisons, or `grid=None` for a heatmap. The asset [research-loop.mplstyle](../assets/research-loop.mplstyle) is reusable without the helper, but font discovery, export handling and annotations then remain the caller's responsibility.

## Helper API

- `style_context(font_paths=(), portable=True)`: temporary plotting defaults; yields the selected font family. Prefer NanumSquare, otherwise an installed fallback. Optional local font paths are explicit inputs; no font download. Inspect Korean/math glyphs even if a fallback was selected. Custom font files should be trusted local assets.
- `style_axes(ax, grid="y")`: quiet grid and axes, without altering values or scale limits. `grid` accepts `"x"`, `"y"`, or `None`.
- `delta_limits(values)`: data-derived symmetric limits for deltas. For comparable panels, pass the combined values once and reuse the limits. Never reuse the illustrative `[-7, 7]` range blindly.
- `draw_delta_panel(ax, labels, values, title=None, limits=None)`: signed horizontal bars and endpoint values, preserving input order. Zero is neutral. Returns Matplotlib bars. Explicit limits must include zero and all values; labels move inward when those limits leave little room. A title, if used, is a short panel identifier, not an explanation. This helper does not compute averages, rank models, calculate uncertainty or know whether higher is better.
- `save_figure(fig, output_stem, dpi=300, portable=True, overwrite=False, formats=("png",), close=True)`: PNG and a small manifest containing actual byte sizes and streamed SHA-256. Use `formats=("png", "pdf", "svg")` only when publication formats are needed. Existing exports are preserved unless you explicitly choose `overwrite=True`. The figure closes on success or failure; use `close=False` only when the caller will close it in `finally`. Portable SVG uses glyph paths; `portable=False` keeps editable text where matching fonts exist. It does not upload or save research pages.

Bounds are checked before export: DPI 240–600, at most 16 × 12 inches and 12
megapixels (including the interactive canvas), 4 axes, 2,000 artists, 100,000
combined path/data points, and 2,000,000 image array values. Delta panels accept
at most 100 values and 200 characters per label/title. Iterable inputs stop at
their limit instead of consuming unbounded generators. Font paths are limited
to eight. Export keeps the fixed canvas; use constrained layout or explicit
margins rather than an unbounded tight bounding box. The limits apply to ordinary
Matplotlib objects and do not undo data/artist allocations already made by your
script or constrain arbitrary custom artist code. Inspect file sizes and load a
bounded subset/aggregate before constructing the plot; never allocate a huge
array and expect export validation to protect that earlier operation.

## Adapt deliberately

Use `BLUE`, `ORANGE`, `GRAY`, `PURPLE` from the helper. Keep each entity's color consistent across comparable figures; gray is context, not an excuse to hide a meaningful comparator. Purple can emphasize a declared criterion but is not an automatic best-model rule. Add markers or line styles when colors must be distinguishable.

Choose ranges from all relevant observations and available intervals. Absolute bars/areas start at zero; deltas include zero. To show small differences among high scores, use dots, a meaningful line plot or a separate delta panel instead of cropped bars. A tighter point/line range must be plainly labeled, include intervals and padding, and be disclosed in the external caption; retain absolute values and never imply significance from zoom. Comparable panels share scales. Heatmaps use a continuous sequential or zero-centered diverging map. Keep missing observations missing.

Decide what the reader should compare before choosing axes or a legend. Separate higher-is-better and lower-is-better metrics into distinct table groups/panels; do not mix incompatible units. Mark direction (↑/↓) and define deltas, distinguishing percentage points from relative percent. The helper colors signs, not benefits: do not call positive change an improvement without checking the metric. Never negate or complement values merely to harmonize a display. Any favorable counterpart requires a verified definition/denominator, explicit label and reproducible calculation; preserve raw values.

Prefer a few readable direct value labels over dense numbers. Retain the full data in the source/table and show material uncertainty when available. At narrow page widths, split a multi-panel figure rather than shrink its text. Keep prose outside the canvas, including explanations placed in a title or blank margin.

Keep inputs, units, aggregation code and figure source alongside the exports. Open the PNG before attaching; verify saved links with the Research Loop workflow. A valid manifest proves file bytes, not scientific correctness or legibility.
