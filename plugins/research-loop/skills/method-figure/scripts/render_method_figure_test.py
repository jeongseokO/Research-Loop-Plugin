"""Run with: python -m unittest discover -s . -p '*_test.py' -v"""

from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / "render-method-figure.py"
EXAMPLE = ROOT.parent / "examples" / "token-selection.json"
MODULE_SPEC = importlib.util.spec_from_file_location("method_figure", SCRIPT)
renderer = importlib.util.module_from_spec(MODULE_SPEC)
MODULE_SPEC.loader.exec_module(renderer)


def minimal():
    return {"schemaVersion": 1, "panels": [{"nodes": [
        {"id": "input", "label": "Input", "kind": "input", "row": 0, "column": 0},
        {"id": "output", "label": "Output", "kind": "output", "row": 0, "column": 1}],
        "edges": [{"source": "input", "target": "output"}]}]}


class ValidationTests(unittest.TestCase):
    def test_import_is_dependency_free(self):
        code = "import importlib.util,sys; s=importlib.util.spec_from_file_location('r',sys.argv[1]); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); assert 'matplotlib' not in sys.modules"
        subprocess.run([sys.executable, "-c", code, str(SCRIPT)], check=True)

    def test_malformed_fields(self):
        mutations = [
            lambda s: s.update(schemaVersion=True),
            lambda s: s.update(width=1e99),
            lambda s: s.update(layout=[]),
            lambda s: s.update(panels=[]),
            lambda s: s["panels"][0]["nodes"][0].update(row=float("nan")),
            lambda s: s["panels"][0]["nodes"][0].update(column=999),
            lambda s: s["panels"][0]["nodes"][0].update(column=True),
            lambda s: s["panels"][0]["nodes"][0].update(kind=[]),
            lambda s: s["panels"][0]["nodes"][0].update(label="A" * 29),
            lambda s: s["panels"][0]["nodes"][0].update(label="line\nbreak"),
            lambda s: s["panels"][0]["nodes"][0].update(svg="<script>oops</script>"),
            lambda s: s["panels"][0]["nodes"][1].update(column=0),
            lambda s: s["panels"][0]["nodes"][1].update(id="input"),
            lambda s: s["panels"][0]["edges"][0].update(target="missing"),
            lambda s: s["panels"][0]["edges"][0].update(source=[]),
            lambda s: s["panels"][0]["edges"][0].update(dashed="yes"),
            lambda s: s["panels"][0]["edges"][0].update(sourcePort="outside"),
            lambda s: s["panels"][0]["edges"].append({"source": "input", "target": "output"}),
        ]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                spec = minimal()
                mutation(spec)
                with self.assertRaises(renderer.DiagramError):
                    renderer.validate(spec)

    def test_geometry_rejects_wrong_ports_and_crossings(self):
        spec = minimal()
        spec["panels"][0]["edges"][0]["sourcePort"] = "west"
        with self.assertRaisesRegex(renderer.DiagramError, "ports"):
            renderer.plan(spec)
        spec = minimal()
        spec["panels"][0]["nodes"][1]["column"] = 2
        spec["panels"][0]["nodes"].append({"id": "blocker", "label": "Blocker", "kind": "module", "row": 0, "column": 1})
        spec["panels"][0]["edges"][0]["route"] = "direct"
        with self.assertRaisesRegex(renderer.DiagramError, "crosses a node"):
            renderer.plan(spec)
        spec["panels"][0]["edges"][0]["route"] = "auto"
        self.assertEqual(len(renderer.plan(spec)[0][0][0][0][1]), 4)

    def test_invalid_input_never_creates_output(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            source, output = base / "bad.json", base / "must-not-exist"
            for contents in ('{"schemaVersion": NaN}', '{"schemaVersion":1,"schemaVersion":1}', '[]', '[', '{"panels":' + '[' * 1500):
                source.write_text(contents)
                result = subprocess.run([sys.executable, str(SCRIPT), str(source), "--output-dir", str(output)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertEqual(result.stdout, "")
                self.assertFalse(output.exists())

    def test_route_points_stay_inside_bounds(self):
        spec, _ = renderer.load_spec(EXAMPLE)
        for paths, (xmin, xmax, ymin, ymax) in renderer.plan(spec)[0]:
            for _, points in paths:
                for x, y in points:
                    self.assertLess(xmin + .3, x)
                    self.assertLess(x, xmax - .3)
                    self.assertLess(ymin + .3, y)
                    self.assertLess(y, ymax - .3)


class RenderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            import matplotlib  # noqa: F401
        except ImportError:
            raise unittest.SkipTest("matplotlib is not installed in this interpreter")

    def run_renderer(self, source, output, *options):
        return subprocess.run([sys.executable, str(SCRIPT), str(source), "--output-dir", str(output), *options], capture_output=True, text=True)

    def test_example_exports_and_overwrite(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "export"
            result = self.run_renderer(EXAMPLE, output)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stderr, "", "Rendering must not emit font or layout warnings")
            manifest = json.loads(result.stdout)
            self.assertEqual(set(manifest["outputs"]), {"sourceJson", "svg", "pdf", "png"})
            for key, item in manifest["outputs"].items():
                data = Path(item["path"]).read_bytes()
                self.assertEqual(item["byteSize"], len(data))
                self.assertEqual(item["sha256"], hashlib.sha256(data).hexdigest())
                if key == "sourceJson":
                    self.assertEqual(data, EXAMPLE.read_bytes())
            png = manifest["outputs"]["png"]
            data = Path(png["path"]).read_bytes()
            self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
            width, height = struct.unpack(">II", data[16:24])
            self.assertEqual((width, height), (png["width"], png["height"]))
            self.assertGreater(width, 1600)
            self.assertGreater(height, 600)
            svg = ET.parse(output / "method-overview.svg")
            self.assertGreater(len(svg.findall(".//{http://www.w3.org/2000/svg}text")), 15)
            self.assertTrue((output / "method-overview.pdf").read_bytes().startswith(b"%PDF"))
            snapshot = {p.name: p.read_bytes() for p in output.iterdir()}
            repeat = self.run_renderer(EXAMPLE, output)
            self.assertEqual(repeat.returncode, 2)
            self.assertIn("--overwrite", repeat.stderr)
            self.assertEqual(snapshot, {p.name: p.read_bytes() for p in output.iterdir()})
            self.assertEqual(self.run_renderer(EXAMPLE, output, "--overwrite").returncode, 0)

    def test_literal_text_and_svg_safety(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            spec = minimal()
            spec["panels"][0]["nodes"][0]["label"] = "<script> & $x$"
            source = base / "literal.json"
            source.write_text(json.dumps(spec))
            result = self.run_renderer(source, base / "output")
            self.assertEqual(result.returncode, 0, result.stderr)
            root = ET.parse(base / "output" / "method-overview.svg").getroot()
            texts = ["".join(node.itertext()) for node in root.findall(".//{http://www.w3.org/2000/svg}text")]
            self.assertIn("<script> & $x$", texts)
            for element in root.iter():
                self.assertNotIn(element.tag.split("}")[-1], ("script", "image", "foreignObject", "a"))
                self.assertFalse(any(key.split("}")[-1].startswith("on") for key in element.attrib))

    def test_vertical_layout_and_font_failure(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            spec = minimal()
            spec["layout"] = "vertical"
            spec["panels"].append(deepcopy(spec["panels"][0]))
            source = base / "vertical.json"
            source.write_text(json.dumps(spec))
            result = self.run_renderer(source, base / "vertical")
            self.assertEqual(result.returncode, 0, result.stderr)
            fail = self.run_renderer(source, base / "missing-font", "--font", "Definitely Not An Installed Font 987")
            self.assertEqual(fail.returncode, 2)
            self.assertIn("font", fail.stderr)
            self.assertFalse((base / "missing-font").exists())
            spec["panels"][0]["nodes"][0]["label"] = "한글 입력"
            source.write_text(json.dumps(spec))
            cjk = self.run_renderer(source, base / "cjk-font", "--font", "DejaVu Sans")
            self.assertEqual(cjk.returncode, 2)
            self.assertIn("CJK", cjk.stderr)
            self.assertFalse((base / "cjk-font").exists())

    def test_clipping_fails_without_publishing(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            spec = minimal()
            spec["panels"][0]["nodes"][0].update(kind="operator", label="WWWWWWWW")
            source = base / "oversize-label.json"
            source.write_text(json.dumps(spec))
            result = self.run_renderer(source, base / "output")
            self.assertEqual(result.returncode, 2)
            self.assertIn("too wide", result.stderr)
            self.assertEqual(list((base / "output").iterdir()), [])


if __name__ == "__main__":
    unittest.main()
