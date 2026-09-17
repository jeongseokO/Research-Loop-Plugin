"""Small Matplotlib helpers; create and export figures inside ``style_context``.

Only Matplotlib is required. No backend is selected, fonts are never downloaded,
and importing this module does not change plotting defaults. As with Matplotlib's
own rc_context, the style context is intended for sequential use, not threads.
"""

from contextlib import contextmanager
import hashlib
import json
import math
from pathlib import Path
import tempfile
import warnings

import matplotlib as mpl
from matplotlib import font_manager
from matplotlib.text import Annotation
from matplotlib.transforms import nonsingular


BLUE = "#2563B9"
ORANGE = "#C97212"
GRAY = "#B5BFCB"
PURPLE = "#7652AF"
INK = "#223047"
TEXT = "#334155"
GRID = "#E7EDF4"
STYLE_PATH = Path(__file__).resolve().parent.parent / "assets" / "research-loop.mplstyle"


def _font_key(name):
    return "".join(character for character in name.casefold() if character.isalnum())


def _select_font(font_paths):
    """Register provided fonts and macOS user NanumSquare files temporarily."""
    manager = font_manager.fontManager
    explicit_families = []
    for filename in font_paths:
        path = Path(filename).expanduser()
        try:
            manager.addfont(str(path))
            explicit_families.append(manager.ttflist[-1].name)
        except (OSError, RuntimeError, ValueError) as error:
            warnings.warn(f"Cannot use font {path.name!r}; using installed fonts ({error}).", UserWarning, stacklevel=3)

    user_fonts = Path.home() / "Library" / "Fonts"
    known = {str(Path(entry.fname)) for entry in manager.ttflist}
    if user_fonts.is_dir():
        for path in sorted(user_fonts.iterdir()):
            if (_font_key(path.stem).startswith("nanumsquare")
                    and path.suffix.lower() in {".ttf", ".otf", ".ttc"}
                    and str(path) not in known):
                try:
                    manager.addfont(str(path))
                except (OSError, RuntimeError, ValueError):
                    continue

    installed = {entry.name for entry in manager.ttflist if Path(entry.fname).is_file()}
    nanum = sorted((name for name in installed if _font_key(name).startswith("nanumsquare")),
                   key=lambda name: (_font_key(name) != "nanumsquare", len(name), name))
    preferred = nanum + explicit_families + [
        "Noto Sans CJK KR", "Noto Sans KR", "Apple SD Gothic Neo",
        "Malgun Gothic", "NanumGothic", "DejaVu Sans",
    ]
    available = list(dict.fromkeys(name for name in preferred if name in installed))
    if not available:
        raise RuntimeError("No usable plotting font is installed; provide a local font through font_paths.")
    return available


@contextmanager
def style_context(*, font_paths=(), portable=True):
    """Apply house defaults, yielding the selected family name.

    NanumSquare is preferred when installed. Otherwise an available Korean font,
    then bundled DejaVu Sans, is used. Missing explicit font files warn and fall
    back; fonts lacking a requested glyph retain Matplotlib's glyph warnings.
    Optional ``font_paths`` is an iterable of local font files. Both rcParams and
    temporary font registrations are restored, including when rendering fails.
    ``portable=True`` outlines SVG text and embeds TrueType fonts in PDF.
    """
    manager = font_manager.fontManager
    original_fonts = list(manager.ttflist)
    original_afm = list(manager.afmlist)
    try:
        families = _select_font(font_paths)
        with mpl.rc_context(fname=str(STYLE_PATH), rc={
            "font.family": families,
            "font.sans-serif": families,
            "svg.fonttype": "path" if portable else "none",
        }):
            yield families[0]
    finally:
        manager.ttflist[:] = original_fonts
        manager.afmlist[:] = original_afm
        manager._findfont_cached.cache_clear()


def style_axes(ax, grid="y"):
    """Style an existing axes, with faint x/y major grids or no grid."""
    if grid not in ("x", "y", None):
        raise ValueError("grid must be 'x', 'y', or None")
    ax.set_facecolor("white")
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(axis="both", which="both", length=0, colors=TEXT, pad=7)
    ax.xaxis.label.set_color(TEXT)
    ax.yaxis.label.set_color(TEXT)
    ax.grid(False, which="both", axis="both")
    if grid is not None:
        ax.grid(True, which="major", axis=grid, color=GRID, linewidth=0.7, alpha=1.0)
    return ax


def _finite_values(values):
    try:
        original = list(values)
        if not original or any(isinstance(value, (str, bytes, bool)) for value in original):
            raise ValueError
        numbers = [float(value) for value in original]
    except (TypeError, ValueError, OverflowError) as error:
        raise ValueError("values must be a nonempty sequence of finite numbers") from error
    if not all(math.isfinite(value) for value in numbers):
        raise ValueError("values must contain only finite numbers")
    return numbers


def delta_limits(values):
    """Symmetric zero-centered limits; concatenate panel values to share a scale."""
    numbers = _finite_values(values)
    largest = max(abs(value) for value in numbers)
    bound = largest * 1.35 if largest else 1.0
    if not math.isfinite(bound * 2) or bound == 0:
        raise ValueError("value range is too large or small for a finite linear axis; rescale units")
    return _validate_limits((-bound, bound), numbers)


def _validate_limits(limits, numbers):
    try:
        lower, upper = limits
        lower, upper = float(lower), float(upper)
    except (TypeError, ValueError, OverflowError) as error:
        raise ValueError("limits must be two finite increasing numbers") from error
    if not all(math.isfinite(value) for value in (lower, upper, upper - lower)) or lower >= upper:
        raise ValueError("limits must have a finite, positive span")
    if lower > min(0, min(numbers)) or upper < max(0, max(numbers)):
        raise ValueError("limits must include zero and every value; values are never clipped")
    if nonsingular(lower, upper) != (lower, upper):
        raise ValueError("limits are too small for a stable linear axis; rescale units")
    return lower, upper


class _DeltaLabel(Annotation):
    """Fit end labels to the current axes size on every render, including export."""

    def _fit(self, renderer):
        width, _, _ = renderer.get_text_width_height_descent(
            self.get_text(), self.get_fontproperties(), ismath=False)
        padding = renderer.points_to_pixels(5)
        bounds = self.axes.bbox
        if width + 2 * padding > bounds.width:
            raise ValueError("delta label does not fit the axes; increase the figure width or split panels")
        endpoint = self.axes.transData.transform(self.xy)[0]
        zero = self.axes.transData.transform((0, self.xy[1]))[0]
        desired = endpoint + padding if self.xy[0] >= 0 else endpoint - padding - width
        left = min(max(desired, bounds.x0 + padding), bounds.x1 - padding - width)
        self.set_position(((left - endpoint) / renderer.points_to_pixels(1), 0))
        inside = min(zero, endpoint) <= left and left + width <= max(zero, endpoint)
        overlaps = left < max(zero, endpoint) and left + width > min(zero, endpoint)
        self.set_color("white" if inside else TEXT)
        self.set_bbox(dict(facecolor="white", edgecolor="none", pad=0.5) if overlaps and not inside else None)

    def draw(self, renderer):
        self._fit(renderer)
        super().draw(renderer)

    def get_window_extent(self, renderer=None):
        if renderer is not None:
            self._fit(renderer)
        return super().get_window_extent(renderer)


def draw_delta_panel(ax, labels, values, title=None, limits=None):
    """Draw horizontal deltas in input order and return the BarContainer.

    Positive values are blue, negative values orange, and zero gray. End labels
    use signed four-significant-digit display (plain ``0`` for zero); bar widths retain
    the input values. Limits default to ``delta_limits(values)``. Supply shared
    limits explicitly for comparisons; insufficient limits raise before drawing.
    """
    numbers = _finite_values(values)
    if isinstance(labels, (str, bytes)):
        raise ValueError("labels must be a sequence with one label per value")
    names = list(labels)
    if len(names) != len(numbers):
        raise ValueError("labels and values must have the same length")
    if ax.get_xscale() != "linear":
        raise ValueError("delta panels require a linear x axis")
    bounds = delta_limits(numbers) if limits is None else _validate_limits(limits, numbers)

    style_axes(ax, grid="x")
    colors = [BLUE if value > 0 else ORANGE if value < 0 else GRAY for value in numbers]
    bars = ax.barh(range(len(numbers)), numbers, height=0.62, color=colors, edgecolor="none", zorder=3)
    ax.set_yticks(range(len(names)), labels=names)
    ax.set_ylim(len(names) - 0.5, -0.5)
    ax.set_xlim(*bounds)
    ax.axvline(0, color="#64748B", linewidth=0.9, zorder=2)
    if title is not None:
        ax.set_title(title, loc="left", color=INK)
    for row, value in enumerate(numbers):
        sign = "−" if value < 0 else "+"
        label = _DeltaLabel(
            "0" if value == 0 else f"{sign} {abs(value):.4g}", xy=(value, row), xytext=(0, 0),
            textcoords="offset points", ha="left", va="center", color=TEXT,
            fontweight="bold", annotation_clip=False, clip_on=False, zorder=4,
        )
        ax.add_artist(label)
    return bars


def save_figure(fig, output_stem, *, dpi=300, portable=True, overwrite=False):
    """Export PNG (at least 240 dpi), PDF, SVG, and a small integrity manifest.

    Returns the same dictionary saved to ``<stem>.manifest.json``. Manifest paths
    are filenames relative to that file. Portable SVG outlines text; ``False``
    retains editable SVG text requiring the selected font on the viewing system.
    PDF embeds fonts in either mode. Existing outputs require ``overwrite=True``.
    """
    if isinstance(dpi, bool) or not isinstance(dpi, (int, float)) or not math.isfinite(dpi) or dpi < 240:
        raise ValueError("PNG export dpi must be a finite number of at least 240")
    stem = Path(output_stem).expanduser()
    outputs = {extension: Path(f"{stem}.{extension}") for extension in ("png", "pdf", "svg")}
    manifest_path = Path(f"{stem}.manifest.json")
    targets = list(outputs.values()) + [manifest_path]
    if not overwrite:
        occupied = [path.name for path in targets if path.exists()]
        if occupied:
            raise FileExistsError(f"Output already exists: {', '.join(occupied)}; use overwrite=True to replace")
    stem.parent.mkdir(parents=True, exist_ok=True)
    manifest = {"pngDpi": dpi, "svgText": "paths" if portable else "editable", "outputs": {}}
    with tempfile.TemporaryDirectory(prefix=".research-plot-", dir=stem.parent) as temporary:
        staged = Path(temporary)
        with mpl.rc_context(rc={"svg.fonttype": "path" if portable else "none", "pdf.fonttype": 42}):
            for extension, target in outputs.items():
                output = staged / target.name
                fig.savefig(output, format=extension, dpi=dpi, bbox_inches="tight", pad_inches=0.12,
                            facecolor="white", edgecolor="white", transparent=False)
                content = output.read_bytes()
                manifest["outputs"][extension] = {
                    "path": target.name, "byteSize": len(content),
                    "sha256": hashlib.sha256(content).hexdigest(),
                }
        (staged / manifest_path.name).write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        for target in targets:
            (staged / target.name).replace(target)
    return manifest
