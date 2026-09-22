---
name: method-figure
description: Create or revise a research methodology overview figure with editable source and a rendered image, and attach it to Research Loop when requested. Use for mechanism, architecture or algorithm diagrams, not statistical plots or general page editing.
---

# Method figure

Make the mechanism understandable through structure and concise labels. **Default to code-authored vectors**: Matplotlib shapes, grids, lines, text and formulas, or another suitable vector tool. Image generation is a last resort, never a source of scientific structure. No explanatory text, conclusions, commentary boxes or baked-in captions—even one sentence. Explanations belong in the external page caption. Honor the user's tools and scope; rendering does not grant project write access.

## Choose the content

- Read the actual method/code and the requested destination. Identify inputs, transformations, state, branches and outputs; do not invent missing mechanisms. Separate training/inference or overall/detail panels only when useful.
- For Research Loop, use the [Research Loop skill](../research-loop/SKILL.md) for identity and narrow source reads, then `get_visualization_guide(technique_id="method-overview")`. Reuse guides already read. Do not fetch unrelated project histories or rewrite the method merely to illustrate it.
- Let forms carry meaning: data as arrays/tables/samples, space as maps/coordinates, relations as graphs, devices as parts, software as actual components. Show algorithm states/transforms, system interactions, or apparatus/conditions/observation points. Do not put everything in identical boxes.
- Use stacking, alignment and grouping only for real repetition, hierarchy, parallelism, storage or sharing. Connect overview and magnified detail when useful; never invent internals. Emphasize the proposed intervention and its neighbors. Main flow is left→right or bottom→top; arrow types identify data, control, physical action or time. Make branches, merges and bypass junctions unambiguous.
- White background, whitespace, thin crisp lines and pale fills. Blue/teal baseline components, orange intervention; extra colors only for distinct meanings. Keep meanings stable across figures and add labels/symbols/line styles. Use size, placement and contrast for hierarchy; shallow depth only for meaningful overlap/internals, not decorative perspective, shadows or gradients.
- Inside: component names, operations, variables, essential formulas, units/dimensions. Match document language and consistent technical symbols. Represent repeats with selected instances, ellipsis and verified counts; distinguish schematic size/color/cell counts from measurements. Prose, limitations and omissions go outside. A diagram is not performance evidence.

## Render and inspect

1. Read [the input contract](references/input.md) and adapt the [synthetic example](examples/token-selection.json) only if needed. Preserve the method specification as JSON in the user's working directory, outside the installed plugin. Do not publish the example as real research.
2. Run [the renderer](scripts/render-method-figure.py): `python3 <skill-directory>/scripts/render-method-figure.py INPUT.json --output-dir OUTPUT --formats png svg pdf`. Resolve the actual skill directory. Use an existing Python environment with Matplotlib; if missing, follow [local setup](references/setup.md). Do not install globally or send private research to external services as a fallback.
3. Keep PNG, editable SVG/vector PDF and regenerable source together; request the vector formats explicitly (the bare CLI defaults to PNG/source JSON). Check exported text/formulas remain editable where required; this renderer's labels are literal, so use a suitable vector tool for actual typeset formulas. It runs one guarded worker with a 60-second wall timeout and single-thread settings. These are not OS CPU/memory quotas. Reuse source for revisions; do not load code or image base64 into context when a file path suffices.
4. Open the actual PNG with the client's image-viewing tool. Check the mechanism, arrows, missing paths, overlap and page-width readability. Every text item must identify a component, operation, quantity or panel—not explain a finding. Move commentary to the external caption, including text disguised as a short title/label. Fix and inspect again, at most two additional renders. On size/time limits, simplify or report the limit; do not bypass it, launch parallel alternatives, or repeatedly raise the timeout. Successful rendering is not verification; report if image inspection is unavailable.

Reuse style, not a previous figure's layout, components or numbers. If the bundled grammar cannot express the verified mechanism, use a suitable local vector tool with the same source-preservation and inspection requirements, not a generic four-box flowchart. Image generation is a last resort only when vector options cannot meet the need: explain why, obtain authorization before sending private sources, and verify every generated component/connection against evidence. Missing source details stay unresolved, never hallucinated; do not claim a generated raster is an editable vector.

## Attach when requested

Use [the existing attachment workflow](../research-loop/references/media.md): prepare the PNG upload using the manifest, upload binary bytes, complete, reread the destination and attach the returned permanent media. Preserve unrelated blocks, caption/alt text and current page revision. SVG/PDF/source files are local deliverables; the image API does not accept them.

After a direct save, reread the page and confirm the intended attachment reference. If the server requires a proposal, report **awaiting review**, not saved. Do not bypass permissions, delete prior assets, or claim that an empty image block, generated code or uploaded-but-unattached file completes the requested page change.

Return the figure/page and any unresolved issue briefly. State a blocker instead of repeatedly uploading or silently changing methods.
