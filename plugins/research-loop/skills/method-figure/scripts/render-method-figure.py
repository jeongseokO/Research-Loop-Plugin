#!/usr/bin/env python3
"""Render a bounded method diagram JSON to editable SVG/PDF and a 2x PNG."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import textwrap
import unicodedata
import warnings

VERSION = 1
KINDS = {"module", "tensor", "tokens", "cache", "operator", "input", "output"}
COLORS = {"blue": "#3973B9", "teal": "#25887E", "purple": "#8062AF",
          "orange": "#C67C33", "gray": "#697888"}
PORTS = {"north", "south", "east", "west"}
DX, DY, WIDTH, HEIGHT = 3.6, 2.5, 2.0, 1.16
OUTPUT_NAMES = {"sourceJson": "method-source.json", "svg": "method-overview.svg",
                "pdf": "method-overview.pdf", "png": "method-overview.png"}


class DiagramError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise DiagramError(message)


def fields(value, allowed, required, where):
    require(type(value) is dict, f"{where}: expected an object")
    require(not (set(value) - allowed), f"{where}: unknown fields {sorted(set(value) - allowed)}")
    require(required <= set(value), f"{where}: missing fields {sorted(required - set(value))}")


def short_text(value, limit, where, empty=False):
    require(type(value) is str, f"{where}: expected text")
    require((empty or bool(value.strip())) and len(value) <= limit,
            f"{where}: use {'0' if empty else '1'}–{limit} characters")
    require(not any(unicodedata.category(c).startswith("C") for c in value),
            f"{where}: control characters, line breaks, and hidden formatting are not allowed")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"JSON: duplicate key {key!r}")
        result[key] = value
    return result


def load_spec(path):
    require(path.stat().st_size <= 128_000, "JSON: maximum input size is 128 KB")
    raw = path.read_bytes()
    def nonfinite(value):
        raise DiagramError(f"JSON: non-finite number {value} is not allowed")
    try:
        spec = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object,
                          parse_constant=nonfinite)
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError) as error:
        raise DiagramError(f"JSON: invalid UTF-8 or malformed JSON: {error}") from error
    validate(spec)
    return spec, raw


def validate(spec):
    fields(spec, {"schemaVersion", "title", "layout", "panels"},
           {"schemaVersion", "panels"}, "diagram")
    require(type(spec["schemaVersion"]) is int and spec["schemaVersion"] == VERSION,
            "diagram.schemaVersion: expected integer 1")
    require(spec.get("layout", "horizontal") in ("horizontal", "vertical"),
            "diagram.layout: expected horizontal or vertical")
    short_text(spec.get("title", ""), 64, "diagram.title", empty=True)
    require(type(spec["panels"]) is list and 1 <= len(spec["panels"]) <= 4,
            "diagram.panels: use 1–4 panels")
    total = 0
    for pi, panel in enumerate(spec["panels"]):
        where = f"panel[{pi}]"
        fields(panel, {"title", "nodes", "edges"}, {"nodes", "edges"}, where)
        short_text(panel.get("title", ""), 48, f"{where}.title", empty=True)
        require(type(panel["nodes"]) is list and 1 <= len(panel["nodes"]) <= 20,
                f"{where}.nodes: use 1–20 nodes")
        require(type(panel["edges"]) is list and len(panel["edges"]) <= 32,
                f"{where}.edges: use at most 32 edges")
        ids, coordinates, links = set(), set(), set()
        total += len(panel["nodes"])
        for ni, node in enumerate(panel["nodes"]):
            loc = f"{where}.node[{ni}]"
            fields(node, {"id", "label", "kind", "row", "column", "accent"},
                   {"id", "label", "kind", "row", "column"}, loc)
            require(type(node["id"]) is str and re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{0,39}", node["id"]),
                    f"{loc}.id: use a letter followed by up to 39 letters, digits, _ or -")
            require(node["id"] not in ids, f"{loc}: duplicate node id {node['id']!r}")
            ids.add(node["id"])
            require(type(node["kind"]) is str and node["kind"] in KINDS, f"{loc}.kind: expected {sorted(KINDS)}")
            short_text(node["label"], 8 if node["kind"] == "operator" else 28, f"{loc}.label")
            require(type(node.get("accent", "blue")) is str and node.get("accent", "blue") in COLORS,
                    f"{loc}.accent: expected one of {sorted(COLORS)}")
            for coordinate in ("row", "column"):
                require(type(node[coordinate]) is int and 0 <= node[coordinate] <= 4,
                        f"{loc}.{coordinate}: expected an integer from 0 to 4")
            cell = (node["row"], node["column"])
            require(cell not in coordinates, f"{loc}: duplicate grid coordinate {cell}")
            coordinates.add(cell)
        for ei, edge in enumerate(panel["edges"]):
            loc = f"{where}.edge[{ei}]"
            fields(edge, {"source", "target", "label", "dashed", "route", "sourcePort", "targetPort"},
                   {"source", "target"}, loc)
            for end in ("source", "target"):
                require(type(edge[end]) is str and edge[end] in ids, f"{loc}.{end}: unknown node endpoint")
            pair = (edge["source"], edge["target"])
            require(pair[0] != pair[1], f"{loc}: self edges are unsupported; use a separate cache node")
            require(pair not in links, f"{loc}: duplicate directed edge {pair}")
            links.add(pair)
            short_text(edge.get("label", ""), 18, f"{loc}.label", empty=True)
            require(type(edge.get("dashed", False)) is bool, f"{loc}.dashed: expected a boolean")
            require(edge.get("route", "auto") in ("auto", "direct", "above", "below", "left", "right"),
                    f"{loc}.route: expected auto, direct, above, below, left, or right")
            for port in ("sourcePort", "targetPort"):
                require(type(edge.get(port, "east")) is str and edge.get(port, "east") in PORTS,
                        f"{loc}.{port}: expected north, south, east, or west")
    require(total <= 40, "diagram: use at most 40 nodes across all panels")


def position(node):
    return node["column"] * DX, -node["row"] * DY


def port_point(node, port):
    x, y = position(node)
    w, h = (.46, .46) if node["kind"] == "operator" else (WIDTH / 2, HEIGHT / 2)
    return {"north": (x, y + h + .05), "south": (x, y - h - .05),
            "east": (x + w + .05, y), "west": (x - w - .05, y)}[port]


def intersects(a, b, node, padding=.12):
    """Slab intersection with a padded node rectangle."""
    x, y = position(node)
    low, high = 0., 1.
    w, h = (.46, .46) if node["kind"] == "operator" else (WIDTH / 2, HEIGHT / 2)
    for start, finish, center, half in zip(a, b, (x, y), (w + padding, h + padding)):
        delta = finish - start
        if abs(delta) < 1e-10:
            if abs(start - center) > half:
                return False
        else:
            ends = sorted(((center - half - start) / delta, (center + half - start) / delta))
            low, high = max(low, ends[0]), min(high, ends[1])
            if low > high:
                return False
    return True


def panel_geometry(panel):
    nodes = {node["id"]: node for node in panel["nodes"]}
    xy = [position(n) for n in nodes.values()]
    xmin, xmax = min(p[0] for p in xy) - WIDTH / 2, max(p[0] for p in xy) + WIDTH / 2
    ymin, ymax = min(p[1] for p in xy) - HEIGHT / 2, max(p[1] for p in xy) + HEIGHT / 2
    paths, lanes = [], dict.fromkeys(("above", "below", "left", "right"), 0)
    for edge in panel["edges"]:
        source, target = nodes[edge["source"]], nodes[edge["target"]]
        sx, sy = position(source)
        tx, ty = position(target)
        default = ("east", "west") if tx > sx else ("west", "east")
        if abs(ty - sy) > abs(tx - sx):
            default = ("north", "south") if ty > sy else ("south", "north")
        a, b = port_point(source, edge.get("sourcePort", default[0])), port_point(target, edge.get("targetPort", default[1]))
        others = [n for n in nodes.values() if n["id"] not in (edge["source"], edge["target"])]
        blocked = any(intersects(a, b, n) for n in others)
        route = edge.get("route", "auto")
        require(not (blocked and route == "direct"),
                f"edge {edge['source']} → {edge['target']}: direct path crosses a node; use an outer route")
        if route == "auto":
            route = "above" if blocked else "direct"
        points = [a, b]
        if route == "direct":
            require(not any(intersects(a, b, n, padding=0) for n in (source, target)),
                    f"edge {edge['source']} → {edge['target']}: ports direct the edge through its endpoint; choose facing ports")
        if route != "direct":
            port = {"above": "north", "below": "south", "left": "west", "right": "east"}[route]
            require(edge.get("sourcePort", port) == port and edge.get("targetPort", port) == port,
                    f"edge {edge['source']} → {edge['target']}: {route} route requires {port} ports")
            a, b = port_point(source, port), port_point(target, port)
            require((a[0] != b[0]) if route in ("above", "below") else (a[1] != b[1]),
                    f"edge {edge['source']} → {edge['target']}: {route} route overlaps itself; choose a perpendicular outer route")
            offset = .6 + .32 * lanes[route]
            lanes[route] += 1
            outer = {"above": ymax + offset, "below": ymin - offset,
                     "left": xmin - offset, "right": xmax + offset}[route]
            points = ([a, (a[0], outer), (b[0], outer), b] if route in ("above", "below")
                      else [a, (outer, a[1]), (outer, b[1]), b])
            require(not any(intersects(p, q, n) for p, q in zip(points, points[1:]) for n in others),
                    f"edge {edge['source']} → {edge['target']}: {route} route is blocked; choose another route or grid position")
        paths.append((edge, points))
    all_points = xy + [point for _, points in paths for point in points]
    bounds = (min(xmin, min(p[0] for p in all_points)) - 1.15,
              max(xmax, max(p[0] for p in all_points)) + 1.15,
              min(ymin, min(p[1] for p in all_points)) - .8,
              max(ymax, max(p[1] for p in all_points)) + 1.15)
    return paths, bounds


def plan(spec):
    panels = [panel_geometry(p) for p in spec["panels"]]
    sizes = [(b[1] - b[0], b[3] - b[2]) for _, b in panels]
    horizontal = spec.get("layout", "horizontal") == "horizontal"
    width = sum(s[0] for s in sizes) if horizontal else max(s[0] for s in sizes)
    height = max(s[1] for s in sizes) if horizontal else sum(s[1] for s in sizes)
    height += .8 if spec.get("title") else 0
    inches = (max(4., width * .55), max(2., height * .55))
    require(inches[0] <= 32 and inches[1] <= 24,
            "diagram exceeds the 32 × 24 inch limit; use fewer grid cells or change panel layout")
    return panels, sizes, width, height, inches


def select_font(spec, requested, font_manager, ft2font):
    labels = [spec.get("title", "")]
    for panel in spec["panels"]:
        labels += [panel.get("title", "")] + [n["label"] for n in panel["nodes"]]
        labels += [e.get("label", "") for e in panel["edges"]]
    needed = {ord(c) for c in "".join(labels) if not c.isspace()}
    candidates = [requested] if requested else ["DejaVu Sans", "Noto Sans CJK KR", "Noto Sans CJK SC",
                  "Noto Sans CJK JP", "Apple SD Gothic Neo", "PingFang SC", "Malgun Gothic", "Arial Unicode MS"]
    for name in candidates:
        try:
            path = font_manager.findfont(font_manager.FontProperties(family=[name]), fallback_to_default=False)
        except ValueError:
            continue
        if needed <= set(ft2font.FT2Font(path).get_charmap()):
            return name
    raise DiagramError("No installed font covers all labels (including CJK/symbols). "
                       "Install a suitable font yourself or use --font with an installed font name.")


def fit_node_text(ax, artist, width, height, lines=2):
    """Wrap against real font metrics; reject text that cannot fit readably."""
    renderer = ax.figure.canvas.get_renderer()
    ax.apply_aspect()
    origin, extent = ax.transData.transform((0, 0)), ax.transData.transform((width, height))
    max_width, max_height = extent - origin
    def measure(value):
        return renderer.get_text_width_height_descent(value, artist.get_fontproperties(), ismath=False)[0]
    remaining, wrapped = artist.get_text(), []
    while remaining:
        end = len(remaining)
        while end and measure(remaining[:end]) > max_width:
            end -= 1
        require(end > 0, "Node label cannot fit the selected font; shorten it or choose another font")
        if end < len(remaining) and " " in remaining[:end]:
            end = remaining[:end].rfind(" ")
        wrapped.append(remaining[:end].rstrip())
        remaining = remaining[end:].lstrip()
    require(len(wrapped) <= lines, f"Node label {artist.get_text()!r} is too wide; shorten it")
    artist.set_text("\n".join(wrapped))
    require(artist.get_window_extent(renderer).height <= max_height,
            f"Node label {artist.get_text()!r} is too tall; shorten it")


def draw_node(ax, node, patches):
    x, y = position(node)
    color = COLORS[node.get("accent", "blue")]
    kind = node["kind"]
    if kind == "operator":
        ax.add_patch(patches.Circle((x, y), .46, fc="white", ec=color, lw=1.7, zorder=3))
        artist = ax.text(x, y, node["label"], ha="center", va="center", fontsize=10, weight="bold", zorder=4)
        fit_node_text(ax, artist, .70, .70, lines=1)
        return
    rounding = .25 if kind in ("input", "output") else .09
    ax.add_patch(patches.FancyBboxPatch((x - WIDTH / 2, y - HEIGHT / 2), WIDTH, HEIGHT,
                 boxstyle=f"round,pad=0,rounding_size={rounding}", fc="white", ec=color, lw=1.4, zorder=3))
    if kind == "module":
        ax.add_patch(patches.Rectangle((x - .99, y - .36), .045, .72, fc=color, ec="none", zorder=4))
    if kind == "output":
        ax.add_patch(patches.FancyBboxPatch((x - .91, y - .49), 1.82, .98,
                     boxstyle="round,pad=0,rounding_size=.21", fc="none", ec=color, lw=.65, zorder=4))
    label_y = y
    if kind in ("tensor", "tokens", "cache"):
        label_y = y - .30
        if kind == "tensor":
            for row in range(3):
                for col in range(6):
                    ax.add_patch(patches.Rectangle((x - .66 + col * .22, y + .04 + row * .13),
                                 .22, .13, fc=color, alpha=.10 + .055 * ((row + col) % 3), ec=color, lw=.5, zorder=4))
        elif kind == "tokens":
            for col in range(5):
                ax.add_patch(patches.FancyBboxPatch((x - .66 + col * .27, y + .02), .21, .40,
                             boxstyle="round,pad=0,rounding_size=.035", fc=color, alpha=.18 + .06 * (col % 2), ec=color, lw=.8, zorder=4))
        else:
            for layer in range(3):
                ax.add_patch(patches.FancyBboxPatch((x - .59 + layer * .06, y + .01 + layer * .12), 1.06, .20,
                             boxstyle="round,pad=0,rounding_size=.045", fc="white", ec=color, lw=.9, zorder=4 + layer))
    artist = ax.text(x, label_y, node["label"], ha="center", va="center", fontsize=9, color="#243247", linespacing=1.08, zorder=8)
    fit_node_text(ax, artist, WIDTH - .22, .50 if kind in ("tensor", "tokens", "cache") else .95)


def render(spec, geometry, font, staging):
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib import pyplot as plt, patches
    from matplotlib.path import Path as MplPath
    panels, sizes, width, height, inches = geometry
    settings = {"font.family": font, "svg.fonttype": "none", "pdf.fonttype": 42,
                "text.usetex": False, "text.parse_math": False, "figure.dpi": 100,
                "savefig.dpi": 200, "axes.unicode_minus": False}
    with matplotlib.rc_context(settings), warnings.catch_warnings():
        warnings.simplefilter("error", UserWarning)
        warnings.simplefilter("error", RuntimeWarning)
        fig = plt.figure(figsize=inches, facecolor="white")
        try:
            if spec.get("title"):
                fig.text(.025, 1 - .20 / height, spec["title"], va="top", fontsize=12, weight="bold", color="#243247")
            xoffset, yoffset = 0., height - (.8 if spec.get("title") else 0)
            for panel, (paths, bounds), (pw, ph) in zip(spec["panels"], panels, sizes):
                horizontal = spec.get("layout", "horizontal") == "horizontal"
                if not horizontal:
                    yoffset -= ph
                ax = fig.add_axes([xoffset / width, (yoffset - ph if horizontal else yoffset) / height,
                                   pw / width, ph / height])
                ax.set(xlim=bounds[:2], ylim=bounds[2:])
                ax.set_aspect("equal")
                ax.axis("off")
                if panel.get("title"):
                    ax.text(bounds[0] + .20, bounds[3] - .16, panel["title"], va="top", fontsize=10, weight="bold", color="#243247")
                for edge, points in paths:
                    path = MplPath(points, [MplPath.MOVETO] + [MplPath.LINETO] * (len(points) - 1))
                    ax.add_patch(patches.FancyArrowPatch(path=path, arrowstyle="-|>", mutation_scale=11,
                                 lw=1.1, linestyle="--" if edge.get("dashed") else "-", color="#627187", zorder=2))
                    if edge.get("label"):
                        a, b = (points[1], points[2]) if len(points) > 2 else (points[0], points[1])
                        vertical = abs(a[0] - b[0]) < .1
                        ax.text((a[0] + b[0]) / 2 + (.15 if vertical else 0), (a[1] + b[1]) / 2 + (0 if vertical else .18),
                                textwrap.fill(edge["label"], 14), fontsize=7.5, ha="left" if vertical else "center",
                                va="center" if vertical else "bottom", color="#536075", zorder=9,
                                bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.3})
                for node in panel["nodes"]:
                    draw_node(ax, node, patches)
                if horizontal:
                    xoffset += pw
            fig.canvas.draw()
            for ax in fig.axes:
                for artist in ax.texts:
                    box = artist.get_window_extent(fig.canvas.get_renderer())
                    require(ax.bbox.x0 <= box.x0 and box.x1 <= ax.bbox.x1 and ax.bbox.y0 <= box.y0 and box.y1 <= ax.bbox.y1,
                            f"Label {artist.get_text()!r} exceeds panel bounds; shorten it or adjust the grid")
            for artist in fig.texts:
                require(fig.bbox.contains(*artist.get_window_extent().get_points()[1]),
                        "Diagram title exceeds figure bounds; shorten it")
            for ext in ("svg", "pdf", "png"):
                fig.savefig(staging / OUTPUT_NAMES[ext], format=ext, dpi=200, facecolor="white")
            return [int(inches[0] * 200), int(inches[1] * 200)]
        finally:
            plt.close(fig)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--overwrite", action="store_true", help="explicitly replace the four renderer outputs")
    parser.add_argument("--font", help="installed font family covering every label")
    args = parser.parse_args(argv)
    try:
        spec, raw = load_spec(args.input)
        geometry = plan(spec)
        output = args.output_dir.resolve()
        targets = {key: output / name for key, name in OUTPUT_NAMES.items()}
        require(args.overwrite or not any(p.exists() or p.is_symlink() for p in targets.values()),
                "Output already exists; choose a new directory or explicitly pass --overwrite")
        import matplotlib.font_manager as font_manager
        import matplotlib.ft2font as ft2font
        font = select_font(spec, args.font, font_manager, ft2font)
        output.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix=".method-render-", dir=output) as temporary:
            staging = Path(temporary)
            dimensions = render(spec, geometry, font, staging)
            (staging / OUTPUT_NAMES["sourceJson"]).write_bytes(raw)
            published = []
            try:
                for key, target in targets.items():
                    if args.overwrite:
                        os.replace(staging / OUTPUT_NAMES[key], target)
                    else:
                        os.link(staging / OUTPUT_NAMES[key], target)
                        published.append(target)
            except OSError:
                for target in published:
                    target.unlink()
                raise
        outputs = {key: {"path": str(path), "byteSize": path.stat().st_size,
                         "sha256": hashlib.sha256(path.read_bytes()).hexdigest()} for key, path in targets.items()}
        outputs["png"].update(width=dimensions[0], height=dimensions[1])
        print(json.dumps({"schemaVersion": 1, "font": font, "outputs": outputs}, ensure_ascii=False))
        return 0
    except (DiagramError, OSError, ImportError, Warning) as error:
        print(f"method-figure: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
