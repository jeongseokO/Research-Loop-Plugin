# Figures, plots and diagrams

Apply this reference when creating or substantially revising a visual. Reuse an unchanged, adequate figure. Read only the selected technique with `get_visualization_guide`; its `visual_quality` field carries the shared rules for MCP-only clients. Instructions are in English; write labels and captions in the user's language while preserving established names and notation.

## 1. Define the visual's job

- Name the question, source evidence, focal comparison and destination before drawing. Identify whether it is a measured result, mechanism, conceptual illustration or original source figure.
- Choose the form that answers the question: aligned points/intervals for comparisons, a line for a meaningful ordered trend, a distribution for variability, a heatmap for a matrix, a diagram for structure or flow. Keep exact lookup values in a table when that serves the reader better.
- For slides, give one visual the largest useful region. Use aligned panels only when the audience needs the comparison simultaneously. Separate an overview from a magnified detail when one view cannot explain both.
- Reuse a diagram's geometry through a sequence. Add or emphasize the changed operation in place; do not move unchanged components or recolor methods on every slide.

## 2. Compose deliberately

- Use a shared alignment grid. Align panel edges, axes, component centers and labels. Use consistent internal padding and inter-panel gaps; leave whitespace around distinct groups.
- Establish hierarchy through position, size and contrast. Use one primary accent for the focal intervention and quieter, still legible comparators. Do not turn every module into an emphasized card.
- Use a light neutral canvas, dark labels and restrained strokes by default. Remove shadows, ornamental gradients, generic AI/brain icons and decorative perspective unless the form explains the actual research.
- Use the same shapes for the same kinds of objects. Represent arrays, state, samples, operators and modules distinctly when that difference matters. Do not use an identical box for every scientific object.
- Use consistent panel identifiers such as (a) and (b), with short descriptive labels. Put the slide's claim in its separate headline; keep the reusable figure free of explanatory paragraphs and baked-in captions.

## 3. Make type and color survive the destination

- Use one font family covering every required glyph, with consistent mathematical notation. Check Korean, Greek letters, minus signs, subscripts and superscripts in the exported file.
- For a typical 16:9 slide, start with 18–24 pt essential figure labels **at final placement**, then inspect the slide. Effective size equals source font size × placed width / source canvas width, using the same width units. Export DPI changes sharpness, not the relative size of text.
- For local plots, use `style_context(profile="presentation")`; it starts at a 10.5 × 5.6 inch canvas with 18 pt labels, 16 pt ticks/legends and stronger lines/markers. For the method renderer use `--profile presentation`. These are starting points, not a fit guarantee. Split a crowded figure; do not silently shrink important text.
- For page/mobile viewing, inspect at the actual content width without relying on zoom. If labels become unreadable, provide separately readable panels or a focused companion figure while retaining the complete source. A high-resolution thumbnail can still be unreadable.
- Give each method/condition a stable color across figures. Pair color with direct labels, marker shapes or line styles. Inspect a grayscale preview; do not claim color-vision accessibility solely because a palette looks pleasant.
- Use perceptually ordered sequential maps for magnitude, diverging maps around a meaningful stated center for signed differences, and cyclic maps only for cyclic quantities. Keep the colorbar, units and normalization explicit. Do not add a rainbow palette to an unordered comparison.

## 4. Plot the evidence faithfully

- Establish metric, units, direction, baseline, scope and exclusions from verified inputs. Distinguish percentage points from relative percent. Separate incompatible units and opposite metric directions into clearly labeled panels.
- Absolute bars/areas start at zero. Delta plots include zero. Points/lines may use a labeled tighter range covering all relevant values and intervals with padding; disclose nonzero bounds in the external caption. Keep comparable panels on comparable scales.
- Show available uncertainty and define it in the caption. Distinguish SD, SE, confidence intervals and range. Do not infer intervals from a single number, imply significance with emphasis, smooth away inconvenient behavior or hide missing values.
- Prefer direct series names near their data when space permits. Otherwise use a compact legend in the same order as the series. Use sparse meaningful ticks and consistent numeric precision. Do not overlap labels with observations or error bars.
- Keep source data, units, transformations and rendering code. Check output values against the source after visual edits. Beauty is not a reason to change evidence.

## 5. Draw mechanisms that can be followed

- Verify inputs, operations, state, branches and outputs against the method/code. Show the proposed intervention with the neighboring computation needed to understand it.
- Keep one dominant flow direction. Route connectors around labels and components. Attach arrowheads to the intended endpoints; distinguish a crossing from a merge and show bypass routes unambiguously.
- Use solid/dashed lines only with a defined semantic distinction. Label a connection with a short quantity or operation when useful. Avoid unsupported arrows suggesting causality, training signals or information access.
- Align baseline and proposed mechanisms so unchanged components occupy corresponding positions. Use a detail panel for essential internals; use ellipsis and a verified count for repetitions.
- Distinguish schematic cell counts, dimensions and colors from measured quantities. Retain conceptual labeling in the external caption. A diagram explains structure; it does not demonstrate performance.

## 6. Export, inspect and deliver

1. Preserve regenerable source and verified data. Construct scientific structure with vector tools. Measured plots must come from data and code, never an image generator.
2. Export SVG/PDF for slides when supported and a sharp PNG for Research Loop page uploads. Preserve aspect ratio. Do not upscale a small screenshot as the final asset or crop away axes, legends, conditions or source credits.
3. Distinguish portable outlined SVG from editable text. Use `portable=False` for text-preserving plot SVG when matching fonts are available; the method renderer retains SVG text. Reopen the output in its intended consumer before promising editability.
4. Inspect the actual export and the assembled slide/page: glyphs, contrast, hierarchy, alignment, collisions, arrow paths, clipping, scale/uncertainty and source fidelity. Check a full-slide view and the intended narrow view. Successful rendering alone does not pass this check.
5. Fix observed defects and inspect again within the existing bounded rendering workflow (at most two additional visual revisions). Report any remaining or unchecked issue. Never waive source correctness or claim a visual check that did not occur.
6. Add a concise external caption explaining the comparison, material conditions and uncertainty. Add distinct alt text describing the essential structure/pattern. Preserve links to complete evidence. For synthetic examples, state clearly in the caption and surrounding document that they are demonstrations, not research results.

These are Research Loop production defaults informed by the user's preferences, not experimental proof of a universally best style. Project examples take priority where compatible with accurate evidence and readable output.

## Source basis

- [MIT Communication Lab: Figure Design](https://mitcommlab.mit.edu/be/commkit/figure-design/) informs figure purpose, simplification, emphasis and checking the intended message.
- [Matplotlib: Choosing Colormaps](https://matplotlib.org/stable/users/explain/colors/colormaps.html) informs sequential, diverging and cyclic encodings; the mapping depends on the data's meaning.
- [W3C: Use of Color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html) supports providing another visual cue besides color. This guidance is not a WCAG certification of an exported figure.

The numeric typography presets, file choices and bounded review workflow are Research Loop production defaults. The references do not experimentally establish those exact settings.
