# Local method figure renderer

`render-method-figure.py INPUT.json --output-dir DIR [--overwrite] [--font "Installed Font"]`

The renderer requires Python 3.9+ and matplotlib. Tested with Python 3.9.13 and
matplotlib 3.9.4. It uses no model API, network fetch, browser, raw SVG input,
HTML input, shell execution, or source-code evaluation. Run it locally; uploading
is a separate existing Research Loop workflow.

The example is a **synthetic demonstration**, not a depiction or measurement of
an actual paper or experiment. It shows token selection and gated fusion solely
to exercise the visual grammar. Do not present it as research evidence.

## JSON grammar

Only these fields are accepted. Unknown fields are rejected.

- Root: `schemaVersion` (integer `1`), `panels`, optional `title` and `layout`.
- `layout`: `horizontal` (default) or `vertical` controls panel arrangement.
- Panel: `nodes`, `edges`, optional short `title`.
- Node: `id`, `label`, `kind`, `row`, `column`, optional `accent`.
- `kind`: `module`, `tensor`, `tokens`, `cache`, `operator`, `input`, `output`.
- `row` and `column`: integers 0–4. Rows increase downward; columns rightward.
- `accent`: `blue` (default), `teal`, `purple`, `orange`, `gray`.
- Edge: `source`, `target`, optional `label`, `dashed`, `route`, `sourcePort`,
  `targetPort`.
- `route`: `auto` (default), `direct`, `above`, `below`, `left`, `right`.
- Ports: `north`, `south`, `east`, `west`.
- `dashed`: a JSON boolean.

Node IDs begin with an ASCII letter and contain up to 40 letters, digits,
underscores, or hyphens. IDs are local to each panel. Root titles allow 64
characters, panel titles 48, node labels 28 (operators 8), and edge labels 18.
All labels are literal text; `$` does not enable math, and XML metacharacters
remain text. Line breaks, controls, and hidden formatting are rejected. Node
labels wrap to at most two lines using actual font metrics. Oversized labels
fail with an explanation instead of overflowing; operator labels should be
short symbols such as `+` or `×`.

These are size limits, not permission to put explanation in a short label.
Titles identify panels; labels identify components, operations or quantities.
No interpretive sentences, conclusions or captions belong in any JSON text
field. Write them in the external page caption instead. The renderer checks
length and layout, not meaning: inspect the rendered image before attaching it.

Limits: 128 KB UTF-8 JSON; 1–4 panels; 1–20 nodes and at most 32 edges per panel;
at most 40 total nodes; exported page at most 32 × 24 inches. The grammar does
not accept explicit canvas or object sizes. NaN, Infinity, duplicate JSON keys,
duplicate node IDs or grid cells, unknown endpoints, duplicate directed edges,
and self edges are rejected.

## Layout and edges

Grid spacing is automatic. Modules use rounded boxes; tensors use cell grids;
tokens use token tiles; caches use stacked layers; operators use circles.
These glyphs are symbolic: tile counts do not encode actual token counts or
tensor dimensions. Add concise quantities such as N or k when relevant.

Default direct edges use facing ports. A direct path that crosses another node
automatically tries an outer route above the panel. Specify an explicit outer
route for residuals or to resolve a blocked automatic route. Above/below routes
use north/south ports on both ends; left/right routes use west/east ports.
Explicit incompatible ports, routes through other nodes, or routes that retrace
themselves are rejected. Reposition the nodes or choose another route when this
occurs. General edge crossings are not prohibited; use sparse layouts and
inspect the figure when several flows meet.

The renderer checks label bounds before publishing. It does not infer scientific
meaning or correct an incorrect mechanism. Review node types, arrows, retained
versus discarded data, and residual direction against the source method.

## Files and manifest

Four files are written: `method-source.json`, `method-overview.svg`,
`method-overview.pdf`, and `method-overview.png`. The source JSON is preserved
byte-for-byte. SVG keeps selectable text (`svg.fonttype=none`); PDF embeds
TrueType fonts (`pdf.fonttype=42`); PNG uses 200 dpi, twice the 100 dpi design
canvas. The vector outputs retain shapes and text for editing. SVG portability
still depends on a viewer having the selected font installed.

Successful stdout is a single JSON object with `schemaVersion`, `font`, and
`outputs`. Each of `outputs.sourceJson`, `.svg`, `.pdf`, `.png` contains an
absolute `path`, `byteSize`, and hexadecimal `sha256`. PNG also has integer
`width` and `height`. There is no base64. Use PNG's path/byte count/hash with the
existing signed uploader; this renderer does not upload or publish anything.

Input/schema/route validation happens before importing matplotlib or creating
the output directory. Font and final layout errors publish no output files.
Existing target files are refused unless `--overwrite` is explicit. Files are
rendered in a temporary staging directory before publication. An error prints a
brief explanation to stderr, leaves stdout empty, and exits with status 2.

The default font selection checks actual glyph coverage. It tries DejaVu Sans
and installed CJK families, including Noto Sans CJK, Apple SD Gothic Neo,
PingFang, Malgun Gothic, and Arial Unicode MS. Missing glyph coverage fails
clearly rather than producing replacement boxes. `--font` selects an installed
family; the renderer does not download or install fonts.

## Verification

From the skill directory: `python3 -m unittest discover -s scripts -p '*_test.py' -v`

Tests cover invalid input, route validation, dependency-free validation imports,
output refusal and explicit overwrite, preserved source bytes, PNG dimensions,
manifest hashes, selectable SVG text, XML safety, literal dollar signs, vertical
panels, absent fonts, unsupported CJK glyphs, and clipping failures. Render tests
are explicitly skipped if matplotlib is unavailable; validation tests still run.
