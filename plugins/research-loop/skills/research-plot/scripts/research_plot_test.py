"""Run: python -m unittest discover -s <this directory> -p '*_test.py' -v"""

from copy import deepcopy
import hashlib
import json
from itertools import count, repeat
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch
import warnings
import xml.etree.ElementTree as ET

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import to_rgba

import research_plot as plot


class PlotTests(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def assert_labels_inside(self, ax):
        ax.figure.canvas.draw()
        renderer = ax.figure.canvas.get_renderer()
        for text in ax.texts:
            bounds = text.get_window_extent(renderer)
            self.assertGreaterEqual(bounds.x0, ax.bbox.x0 - 0.5, text.get_text())
            self.assertLessEqual(bounds.x1, ax.bbox.x1 + 0.5, text.get_text())
            self.assertGreaterEqual(bounds.y0, ax.bbox.y0 - 0.5, text.get_text())
            self.assertLessEqual(bounds.y1, ax.bbox.y1 + 0.5, text.get_text())

    def test_context_isolated_even_after_error(self):
        original = deepcopy(dict(matplotlib.rcParams))
        fonts = list(font_manager.fontManager.ttflist)
        font_file = font_manager.findfont("DejaVu Sans")
        with self.assertRaisesRegex(RuntimeError, "intentional"):
            with plot.style_context(font_paths=[font_file]) as family:
                self.assertTrue(family)
                self.assertEqual(matplotlib.rcParams["axes.facecolor"], "white")
                self.assertEqual(matplotlib.rcParams["svg.fonttype"], "path")
                self.assertEqual(matplotlib.rcParams["axes.prop_cycle"].by_key()["color"],
                                 [plot.BLUE, plot.ORANGE, plot.GRAY, plot.PURPLE])
                with plot.style_context(portable=False):
                    self.assertEqual(matplotlib.rcParams["svg.fonttype"], "none")
                self.assertEqual(matplotlib.rcParams["svg.fonttype"], "path")
                raise RuntimeError("intentional")
        self.assertEqual(dict(matplotlib.rcParams), original)
        self.assertEqual(font_manager.fontManager.ttflist, fonts)

    def test_missing_font_deliberately_falls_back(self):
        manager = font_manager.fontManager
        entries = [entry for entry in manager.ttflist if entry.name == "DejaVu Sans"]
        with tempfile.TemporaryDirectory() as temporary:
            with patch.object(manager, "ttflist", list(entries)), patch.object(Path, "home", return_value=Path(temporary)):
                manager._findfont_cached.cache_clear()
                with self.assertWarnsRegex(UserWarning, "Cannot use font"):
                    with plot.style_context(font_paths=[Path(temporary) / "missing.ttf"]) as family:
                        self.assertEqual(family, "DejaVu Sans")
                        fig, ax = plt.subplots()
                        plot.draw_delta_panel(ax, ["Sample"], [1])
                        fig.canvas.draw()

    def test_math_font_fallback_renders_symbols(self):
        with warnings.catch_warnings(record=True) as emitted, plot.style_context():
            warnings.simplefilter("always", UserWarning)
            self.assertEqual(matplotlib.rcParams["mathtext.fontset"], "dejavusans")
            self.assertEqual(matplotlib.rcParams["mathtext.fallback"], "stix")
            fig, ax = plt.subplots(figsize=(5, 2.5))
            plot.draw_delta_panel(ax, [r"$\Delta \mu \pm \sigma$"], [1])
            fig.canvas.draw()
        self.assertFalse([warning for warning in emitted if "glyph" in str(warning.message).lower()])

    def test_style_axes_grid_modes(self):
        with plot.style_context():
            fig, axes = plt.subplots(1, 3)
            for ax, grid in zip(axes, ("x", "y", None)):
                plot.style_axes(ax, grid)
                self.assertEqual(ax.get_facecolor(), to_rgba("white"))
                self.assertFalse(any(spine.get_visible() for spine in ax.spines.values()))
                self.assertEqual(any(line.get_visible() for line in ax.get_xgridlines()), grid == "x")
                self.assertEqual(any(line.get_visible() for line in ax.get_ygridlines()), grid == "y")
            with self.assertRaises(ValueError):
                plot.style_axes(axes[0], "both")

    def test_delta_preserves_order_values_and_sign_colors(self):
        labels = ["small", "negative", "zero", "large"]
        values = [0.2, -3.75, 0.0, 2.5]
        original = (list(labels), list(values))
        with plot.style_context():
            fig, ax = plt.subplots(figsize=(6, 3))
            bars = plot.draw_delta_panel(ax, labels, values, title="Metric change")
            self.assertEqual([bar.get_width() for bar in bars], values)
            self.assertEqual([tick.get_text() for tick in ax.get_yticklabels()], labels)
            self.assertEqual([bar.get_facecolor() for bar in bars],
                             list(map(to_rgba, [plot.BLUE, plot.ORANGE, plot.GRAY, plot.BLUE])))
            self.assertEqual([text.get_text() for text in ax.texts], ["+ 0.2", "− 3.75", "0", "+ 2.5"])
            self.assertEqual(ax.lines[0].get_xdata(), [0, 0])
            self.assertEqual(ax.get_title(loc="left"), "Metric change")
            self.assert_labels_inside(ax)
        self.assertEqual((labels, values), original)

    def test_zero_negative_positive_mixed_and_extreme_ranges(self):
        cases = [[0, 0, -0.0], [-1, -5], [0, 4], [-7, 9], [-1e-250, 1e-250], [-1e250, 1e250]]
        with plot.style_context():
            for values in cases:
                with self.subTest(values=values):
                    fig, ax = plt.subplots(figsize=(6, 2.5))
                    plot.draw_delta_panel(ax, [str(index) for index in range(len(values))], values)
                    self.assertLess(ax.get_xlim()[0], 0)
                    self.assertGreater(ax.get_xlim()[1], 0)
                    self.assert_labels_inside(ax)
                    plt.close(fig)
        self.assertEqual(plot.delta_limits([0, 0]), (-1, 1))

    def test_shared_limits_and_tight_limits_keep_labels_visible_after_resize(self):
        shared = plot.delta_limits([-100, 3, 10])
        cases = [([-100, 3], shared), ([0, 10], shared), ([-100, 100], (-100, 100)),
                 ([0, 1], (0, 1)), ([-1, 0], (-1, 0)), ([0, 0], (0, 1))]
        with plot.style_context():
            for values, limits in cases:
                with self.subTest(values=values, limits=limits):
                    fig, ax = plt.subplots(figsize=(6, 2.5))
                    plot.draw_delta_panel(ax, ["a", "b"], values, limits=limits)
                    self.assertEqual(ax.get_xlim(), limits)
                    self.assert_labels_inside(ax)
                    fig.set_size_inches(3, 2.5)
                    self.assert_labels_inside(ax)
                    self.assertEqual(ax.get_xlim(), limits)
                    plt.close(fig)

    def test_invalid_data_and_overflow_rejected_before_drawing(self):
        bad_values = [[], [float("nan")], [float("inf")], [-float("inf")], ["1"], [True], [None]]
        bad_limits = [(1, 2), (-1, 0), (0, 0), (2, -2), (float("nan"), 2),
                      (-float("inf"), 2), (-1e308, 1e308), (0,)]
        fig, ax = plt.subplots()
        for values in bad_values:
            with self.subTest(values=values), self.assertRaises(ValueError):
                plot.draw_delta_panel(ax, ["a"] * len(values), values)
        for limits in bad_limits:
            with self.subTest(limits=limits), self.assertRaises(ValueError):
                plot.draw_delta_panel(ax, ["a"], [1], limits=limits)
        for labels in ([], ["a", "b"], "a"):
            with self.subTest(labels=labels), self.assertRaises(ValueError):
                plot.draw_delta_panel(ax, labels, [1])
        with self.assertRaisesRegex(ValueError, "rescale units"):
            plot.draw_delta_panel(ax, ["a"], [1e308])
        with self.assertRaisesRegex(ValueError, "rescale units"):
            plot.draw_delta_panel(ax, ["a"], [1e-300])
        with self.assertRaisesRegex(ValueError, "rescale units"):
            plot.draw_delta_panel(ax, ["a"], [1e-300], limits=(-1e-300, 1e-300))
        self.assertEqual(len(ax.patches), 0)
        self.assertEqual(len(ax.texts), 0)
        ax.set_xscale("log")
        with self.assertRaisesRegex(ValueError, "linear"):
            plot.draw_delta_panel(ax, ["a"], [1])

    def test_label_fit_reports_unreadably_narrow_axis(self):
        with plot.style_context():
            fig, ax = plt.subplots(figsize=(0.3, 2))
            plot.draw_delta_panel(ax, ["a"], [123456789])
            with self.assertRaisesRegex(ValueError, "increase the figure width"):
                fig.canvas.draw()

    def test_exports_manifest_portability_dpi_and_overwrite(self):
        with tempfile.TemporaryDirectory() as temporary, plot.style_context():
            stem = Path(temporary) / "result.v2"
            fig, ax = plt.subplots(figsize=(5, 2.5))
            plot.draw_delta_panel(ax, ["A", "B", "C"], [-3, 0, 2], limits=(-3, 2))
            original = deepcopy(dict(matplotlib.rcParams))
            manifest = plot.save_figure(fig, stem, formats=("png", "pdf", "svg"), close=False)
            self.assertEqual(dict(matplotlib.rcParams), original)
            self.assertEqual(manifest, json.loads(Path(f"{stem}.manifest.json").read_text()))
            self.assertEqual(set(manifest["outputs"]), {"png", "pdf", "svg"})
            for extension, item in manifest["outputs"].items():
                output = stem.parent / item["path"]
                content = output.read_bytes()
                self.assertEqual(output.name, f"result.v2.{extension}")
                self.assertEqual(item["byteSize"], len(content))
                self.assertEqual(item["sha256"], hashlib.sha256(content).hexdigest())
            png = Path(f"{stem}.png").read_bytes()
            self.assertEqual(png[:8], b"\x89PNG\r\n\x1a\n")
            offset = png.index(b"pHYs") + 4
            x_ppm, y_ppm, unit = struct.unpack(">IIB", png[offset:offset + 9])
            self.assertEqual(unit, 1)
            self.assertAlmostEqual(x_ppm * 0.0254, 300, delta=0.02)
            self.assertEqual(x_ppm, y_ppm)
            self.assertTrue(Path(f"{stem}.pdf").read_bytes().startswith(b"%PDF"))
            root = ET.parse(Path(f"{stem}.svg")).getroot()
            self.assertEqual(root.findall(".//{http://www.w3.org/2000/svg}text"), [])
            self.assertGreater(len(root.findall(".//{http://www.w3.org/2000/svg}path")), 5)
            snapshot = {path.name: path.read_bytes() for path in stem.parent.iterdir()}
            with self.assertRaises(FileExistsError):
                plot.save_figure(fig, stem, close=False)
            self.assertEqual(snapshot, {path.name: path.read_bytes() for path in stem.parent.iterdir()})
            editable = plot.save_figure(fig, stem, dpi=240, portable=False, overwrite=True,
                                        formats=("png", "pdf", "svg"), close=False)
            self.assertEqual(editable["svgText"], "editable")
            self.assertTrue(ET.parse(Path(f"{stem}.svg")).findall(".//{http://www.w3.org/2000/svg}text"))
            self.assert_labels_inside(ax)

    def test_failed_export_publishes_no_partial_files(self):
        with tempfile.TemporaryDirectory() as temporary, plot.style_context():
            stem = Path(temporary) / "failure"
            fig, ax = plt.subplots(figsize=(0.3, 2))
            plot.draw_delta_panel(ax, ["a"], [123456789])
            with self.assertRaises(ValueError):
                plot.save_figure(fig, stem)
            self.assertEqual(list(Path(temporary).iterdir()), [])
            for dpi in (239, 601, -1, True, float("inf"), float("nan"), "300"):
                with self.subTest(dpi=dpi), self.assertRaises(ValueError):
                    plot.save_figure(fig, stem, dpi=dpi)
            self.assertEqual(list(Path(temporary).iterdir()), [])

    def test_default_is_png_and_closes_figure(self):
        with tempfile.TemporaryDirectory() as temporary:
            fig, ax = plt.subplots(figsize=(3, 2))
            ax.plot([0, 1], [0, 1])
            with patch.object(Path, "read_bytes", side_effect=AssertionError("hash must stream")):
                manifest = plot.save_figure(fig, Path(temporary) / "single")
            self.assertEqual(set(manifest["outputs"]), {"png"})
            self.assertFalse(plt.fignum_exists(fig.number))
            self.assertEqual(len(list(Path(temporary).iterdir())), 2)

    def test_input_limits_stop_infinite_iterators_before_drawing(self):
        fig, ax = plt.subplots()
        consumed = []
        def values():
            for value in count():
                consumed.append(value)
                yield value
        with self.assertRaisesRegex(ValueError, "100 item limit"):
            plot.draw_delta_panel(ax, repeat("a"), values())
        self.assertEqual(len(consumed), 101)
        for labels, title in [(["a" * 201], None), (["a"], "x" * 201)]:
            with self.assertRaises(ValueError):
                plot.draw_delta_panel(ax, labels, [1], title=title)
        self.assertEqual(len(ax.patches), 0)

    def test_resource_limits_reject_before_savefig_and_close(self):
        with tempfile.TemporaryDirectory() as temporary:
            for figsize, dpi in [((17, 2), 300), ((16, 12), 300), ((5, 3), 601)]:
                fig, ax = plt.subplots(figsize=figsize)
                with patch.object(fig, "savefig") as save, self.assertRaises(ValueError):
                    plot.save_figure(fig, Path(temporary) / "too-large", dpi=dpi)
                save.assert_not_called()
                self.assertFalse(plt.fignum_exists(fig.number))
            fig, axes = plt.subplots(1, 5, figsize=(5, 2))
            with patch.object(fig, "savefig") as save, self.assertRaisesRegex(ValueError, "4 axes"):
                plot.save_figure(fig, Path(temporary) / "axes")
            save.assert_not_called()
            fig, ax = plt.subplots(figsize=(3, 2))
            ax.plot([0, 1], [0, 1])
            # Lower the threshold to exercise the limit without constructing heavy data.
            with patch.object(plot, "MAX_POINTS", 1), patch.object(fig, "savefig") as save:
                with self.assertRaisesRegex(ValueError, "path/data points"):
                    plot.save_figure(fig, Path(temporary) / "points")
                save.assert_not_called()
            fig, ax = plt.subplots(figsize=(3, 2))
            with patch.object(plot, "MAX_ARTISTS", 1), patch.object(fig, "savefig") as save:
                with self.assertRaisesRegex(ValueError, "artists"):
                    plot.save_figure(fig, Path(temporary) / "artists")
                save.assert_not_called()
            self.assertEqual(list(Path(temporary).iterdir()), [])

    def test_fixed_canvas_cannot_expand_for_far_away_text(self):
        with tempfile.TemporaryDirectory() as temporary:
            fig, ax = plt.subplots(figsize=(3, 2))
            ax.text(1e20, 1e20, "outside")
            manifest = plot.save_figure(fig, Path(temporary) / "bounded")
            png = (Path(temporary) / manifest["outputs"]["png"]["path"]).read_bytes()
            self.assertEqual(struct.unpack(">II", png[16:24]), (900, 600))


if __name__ == "__main__":
    unittest.main()
