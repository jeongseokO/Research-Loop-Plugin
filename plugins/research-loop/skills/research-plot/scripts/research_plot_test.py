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

    def test_presentation_profile_changes_legibility_not_data_and_restores_defaults(self):
        original = deepcopy(dict(matplotlib.rcParams))
        with plot.style_context(profile="presentation"):
            fig, ax = plt.subplots(layout="constrained")
            bars = plot.draw_delta_panel(ax, ["A", "B"], [1.2, -0.8])
            ax.set_xlabel("Delta (points)")
            self.assertEqual([bar.get_width() for bar in bars], [1.2, -0.8])
            self.assertEqual(ax.xaxis.label.get_fontsize(), 18)
            self.assertEqual(matplotlib.rcParams["legend.fontsize"], 16)
            self.assertEqual(list(fig.get_size_inches()), [10.5, 5.6])
            self.assert_labels_inside(ax)
            with tempfile.TemporaryDirectory() as temporary:
                plot.save_figure(fig, Path(temporary) / "presentation", formats=("png", "svg"))
            with plot.style_context():
                self.assertEqual(matplotlib.rcParams["font.size"], 12)
            self.assertEqual(matplotlib.rcParams["font.size"], 18)
        self.assertEqual(dict(matplotlib.rcParams), original)
        with self.assertRaisesRegex(ValueError, "profile"):
            with plot.style_context(profile="unknown"):
                self.fail("invalid profile accepted")
        self.assertEqual(dict(matplotlib.rcParams), original)

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


LOOKS_FILE = Path(plot.__file__).resolve().parent.parent / "assets" / "slide-looks.json"


class SlideTests(unittest.TestCase):
    """A slide figure wears its deck's look and fills its slot at the slide's own sizes."""

    def setUp(self):
        self.looks = json.loads(LOOKS_FILE.read_text(encoding="utf-8"))

    def tearDown(self):
        plt.close("all")

    def test_a_look_dresses_the_figure_and_everything_is_restored(self):
        original = deepcopy(dict(matplotlib.rcParams))
        fonts = list(font_manager.fontManager.ttflist)
        with plot.slide_context("stage", accent="5cc8ff") as style:
            self.assertEqual(style.background, "#0F1B2E")
            for key in ("figure.facecolor", "axes.facecolor", "savefig.facecolor"):
                self.assertEqual(to_rgba(matplotlib.rcParams[key]), to_rgba("#0F1B2E"), key)
            self.assertEqual(style.focus, "#5CC8FF")
            self.assertEqual(matplotlib.rcParams["axes.prop_cycle"].by_key()["color"][0], "#5CC8FF")
            self.assertEqual(matplotlib.rcParams["axes.prop_cycle"].by_key()["color"][1:], list(style.ramp))
            self.assertEqual(style.ramp, tuple(f"#{color}" for color in self.looks["looks"]["stage"]["ramp"]))
            self.assertEqual(style.categories, ("#5CC8FF", "#FFB547", "#7EE0A8", "#FF8A7A"))
            self.assertEqual(to_rgba(matplotlib.rcParams["axes.edgecolor"]), to_rgba("#2A3A56"))
            self.assertEqual(to_rgba(matplotlib.rcParams["axes.labelcolor"]), to_rgba(style.body))
            self.assertEqual(to_rgba(matplotlib.rcParams["xtick.labelcolor"]), to_rgba(style.muted))
            self.assertEqual(to_rgba(matplotlib.rcParams["grid.color"]), to_rgba(style.rule))
            self.assertFalse(matplotlib.rcParams["axes.spines.top"])
            self.assertFalse(matplotlib.rcParams["axes.spines.right"])
            self.assertTrue(matplotlib.rcParams["axes.spines.left"])
            self.assertEqual(matplotlib.rcParams["lines.linewidth"], 2.4)
            self.assertFalse(matplotlib.rcParams["legend.frameon"])
            # A sequential map runs from the ground to the accent.
            self.assertEqual(to_rgba(style.sequential(0.0)), to_rgba("#0F1B2E"))
            self.assertEqual(to_rgba(style.sequential(1.0)), to_rgba("#5CC8FF"))
        self.assertEqual(dict(matplotlib.rcParams), original)
        self.assertEqual(font_manager.fontManager.ttflist, fonts)

    def test_every_slot_takes_its_box_at_ninety_six_pixels_an_inch(self):
        for slot in ("claim-figure", "figure", "comparison", "big-number"):
            with self.subTest(slot=slot), plot.slide_context("vivid", slot=slot, purpose="progress") as style:
                box = self.looks["boxes"]["progress"][slot]
                self.assertEqual(style.figsize, (box["w"] / 96, box["h"] / 96))
                fig, _ = plt.subplots()
                self.assertEqual(tuple(fig.get_size_inches()), style.figsize)
                plt.close(fig)

    def test_axis_names_take_the_purpose_caption_size(self):
        with plot.slide_context("vivid", purpose="talk") as style:
            fig, ax = plt.subplots()
            ax.set_xlabel("Budget (%)")
            self.assertEqual(ax.xaxis.label.get_fontsize(), 16)
            self.assertEqual((style.label_size, style.tick_size), (16, 14))
            self.assertEqual(matplotlib.rcParams["legend.fontsize"], 14)
        with plot.slide_context("report", purpose="memo") as style:
            self.assertEqual((style.label_size, style.tick_size), (12, 12))

    def test_unknown_names_say_what_is_possible(self):
        cases = [({"look": "neon"}, "vivid, paper, stage, report"), ({"look": "vivid", "slot": "hero"}, "claim-figure, figure, comparison, big-number"),
                 ({"look": "vivid", "purpose": "keynote"}, "talk, progress, memo, journal"), ({"look": "vivid", "accent": "FFFFFF"}, "#2457D6")]
        for arguments, possible in cases:
            with self.subTest(arguments=arguments), self.assertRaisesRegex(ValueError, possible):
                with plot.slide_context(**arguments):
                    self.fail("an unknown name was accepted")

    def test_the_plugin_faces_are_the_ones_chosen(self):
        with plot.slide_context("vivid") as style:
            self.assertEqual(style.family, "Research Loop Sans")
            self.assertEqual(matplotlib.rcParams["font.family"][0], "Research Loop Sans")
            fig, ax = plt.subplots()
            label = ax.set_xlabel("Budget")
            self.assertEqual(font_manager.FontProperties(fname=font_manager.findfont(label.get_fontproperties())).get_name(), "Research Loop Sans")
        with plot.slide_context("paper") as style:
            self.assertEqual(style.family, "Research Loop Serif")
        names = {entry.name for entry in font_manager.fontManager.ttflist}
        self.assertNotIn("Research Loop Sans", names)

    def test_a_figure_without_a_hangul_face_warns(self):
        manager = font_manager.fontManager
        latin = [entry for entry in manager.ttflist if entry.name == "DejaVu Sans"]
        with patch.object(manager, "ttflist", list(latin)):
            manager._findfont_cached.cache_clear()
            with self.assertWarnsRegex(UserWarning, "Korean"):
                with plot.slide_context("vivid"):
                    pass
        manager._findfont_cached.cache_clear()

    def test_figure_record_hashes_repository_files_and_refuses_paths_outside(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "repo"
            (root / "results").mkdir(parents=True)
            (root / "figures").mkdir()
            (root / "results" / "kv.csv").write_text("budget,loss\n10,4.2\n", encoding="utf-8")
            (root / "figures" / "kv.py").write_text("print('plot')\n", encoding="utf-8")
            (Path(temporary) / "secret.csv").write_text("x\n", encoding="utf-8")
            record = plot.figure_record(["results/kv.csv"], "figures/kv.py", look="vivid", slot="claim-figure", commit="ABC1234", root=root)
            self.assertEqual(list(record), ["data", "code", "commit", "tool", "look", "slot", "date"])
            self.assertEqual(record["data"], [{"name": "results/kv.csv", "sha256": hashlib.sha256(b"budget,loss\n10,4.2\n").hexdigest()}])
            self.assertEqual(record["code"]["sha256"], hashlib.sha256(b"print('plot')\n").hexdigest())
            self.assertEqual((record["commit"], record["look"], record["slot"]), ("abc1234", "vivid", "claim-figure"))
            self.assertEqual(record["tool"], f"matplotlib {matplotlib.__version__}")
            self.assertRegex(record["date"], r"^\d{4}-\d{2}-\d{2}$")
            for name in ("../secret.csv", "/etc/hosts", "~/kv.csv", "C:\\data\\kv.csv", "results/../../secret.csv", ""):
                with self.subTest(name=name), self.assertRaises(ValueError):
                    plot.figure_record([name], look="vivid", slot="figure", root=root)
            for arguments in ({"look": "neon", "slot": "figure"}, {"look": "vivid", "slot": "hero"}, {"look": "vivid", "slot": "figure", "commit": "xyz"}):
                with self.subTest(arguments=arguments), self.assertRaises(ValueError):
                    plot.figure_record(["results/kv.csv"], root=root, **arguments)
            with self.assertRaises(FileNotFoundError):
                plot.figure_record(["results/missing.csv"], look="vivid", slot="figure", root=root)
            with self.assertRaisesRegex(ValueError, "8"):
                plot.figure_record(["results/kv.csv"] * 9, look="vivid", slot="figure", root=root)

    def test_a_slide_figure_is_saved_on_its_look_ground(self):
        with tempfile.TemporaryDirectory() as temporary, plot.slide_context("stage") as style:
            fig, ax = plt.subplots()
            ax.plot([0, 1, 2], [1, 3, 2])
            manifest = plot.save_figure(fig, Path(temporary) / "stage", background=style.background)
            pixels = plt.imread(Path(temporary) / manifest["outputs"]["png"]["path"])
            for corner in (pixels[0, 0], pixels[-1, -1]):
                self.assertTrue(all(abs(float(value) - expected) <= 1 / 255 for value, expected in zip(corner[:3], to_rgba("#0F1B2E")[:3])))
            with self.assertRaises(ValueError):
                plot.save_figure(plt.subplots()[0], Path(temporary) / "bad", background="not a colour")


if __name__ == "__main__":
    unittest.main()
