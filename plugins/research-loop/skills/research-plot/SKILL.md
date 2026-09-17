---
name: research-plot
description: Create or revise quantitative Research Loop plots with the shared Matplotlib house style and reusable helpers. Use for measured comparisons, trends, distributions and uncertainty, not methodology diagrams or styling the web app.
---

# Research plot

Make the research comparison easy to read. Use the shared style as a default, not as a restriction on the analytical form or the user's explicit choices. Render measurements from verified data with code, not an image generator.

## Choose and render

- For Research Loop sources or attachments, follow [Research Loop](../research-loop/SKILL.md). Read `get_visualization_guide` for the chosen technique, reusing a guide already loaded. Do not load the whole catalog or unrelated pages.
- Choose the chart from the question and evidence. Keep full inputs, units, missingness and available uncertainty; never invent bounds or claim significance from a highlighted maximum. Use stable entity colors across related figures. Signed blue/orange bars encode positive/negative change, not automatically good/bad.
- Read [usage](references/usage.md) when rendering. Import the bundled helper and use its isolated style context in a local script outside the installed plugin. Run that script through the bundled [render guard](../../scripts/render_guard.py), one figure job at a time. It limits wall time and common numerical-library threads; it is not an OS CPU/memory quota. It supplies typography, palette, restrained axes, delta panels and PNG export; request PDF/SVG explicitly only when needed for publication. Do not force everything into bars.
- White background, faint grid and generous margins are defaults. Prefer NanumSquare with a glyph-safe local fallback. Keep colors consistent and use markers/line styles too. Comparable panels share scales; limits come from data, not a template. Heatmaps retain an appropriate continuous color map.
- Include only data and necessary labels in the image. No explanatory prose, conclusions, commentary boxes or baked-in captions. Use the actual external caption for interpretation, conditions, uncertainty definitions and limits; alt text stays separate.

## Inspect and finish

Open the actual PNG at the intended page width. Check glyphs/math, label collisions, panel density, zeros, scales, missing data and uncertainty. Split dense panels or show fewer direct value labels without dropping evidence. A successful export is not a readability check.

Use the bounded helper limits described in usage. Validate input file size and row count before loading research data; do not load an entire dataset merely to inspect its shape. Large evidence stays in its source/table; create an explicitly described aggregate or smaller panels for the figure. A limit error means simplify or report the limit, not raise it or launch concurrent replacements. Do not start a render while another guarded render is running. Limit visual revision to two additional renders, then report the remaining layout issue.

Keep source data and rendering code beside the exports so the plot can be revised. The helper closes the figure by default, including failed exports. Attach only when requested using the [existing upload workflow](../research-loop/references/operations.md#figures-and-attachments); preserve the destination revision and unrelated blocks. Optional PDF/SVG remain local deliverables; the page image API accepts raster files. Confirm the saved media reference and distinguish approval-pending from applied.

If Python/Matplotlib is unavailable, use the existing [local setup](../method-figure/references/setup.md) only as needed. Do not silently install global dependencies, download fonts or send research to a third party. MCP-only clients do not have these local helpers: apply the returned style with available tools or report the missing execution capability.
