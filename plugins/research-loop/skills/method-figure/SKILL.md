---
name: method-figure
description: Create or revise a research methodology overview figure with editable source and a rendered image, and attach it to Research Loop when requested. Use for mechanism, architecture or algorithm diagrams, not statistical plots or general page editing.
---

# Method figure

Make the mechanism understandable through structure and concise labels. No explanatory text, conclusions, commentary boxes or baked-in captions—even one sentence. Explanations belong in the external page caption. Honor the user's tools and scope. This skill renders locally; it does not call an image-generation API or grant project write access.

## Choose the content

- Read the actual method/code and the requested destination. Identify inputs, transformations, state, branches and outputs; do not invent missing mechanisms. Separate training/inference or overall/detail panels only when useful.
- For Research Loop, use the [Research Loop skill](../research-loop/SKILL.md) for identity and narrow source reads, then `get_visualization_guide(technique_id="method-overview")`. Reuse guides already read. Do not fetch unrelated project histories or rewrite the method merely to illustrate it.
- Use meaningful shapes for tokens, tensors, caches and operations. Arrows represent verified relationships. Keep labels short; explanatory prose and important caveats belong in the external caption, term notes or linked method page. A diagram is not evidence of performance.

## Render and inspect

1. Read [the input contract](references/input.md) and adapt the [synthetic example](examples/token-selection.json) only if needed. Preserve the method specification as JSON in the user's working directory, outside the installed plugin. Do not publish the example as real research.
2. Run [the renderer](scripts/render-method-figure.py): `python3 <skill-directory>/scripts/render-method-figure.py INPUT.json --output-dir OUTPUT`. Resolve the skill directory from this file's actual location; do not paste an unexpanded placeholder. Use an existing Python environment with Matplotlib. If missing, follow [local setup](references/setup.md); do not install globally or send content to an external service as a fallback.
3. The renderer saves PNG and source JSON by default; add `--formats png pdf svg` only when publication formats are needed. It runs one guarded worker with a 60-second wall timeout and single-thread settings for common numerical libraries. The input contract lists size limits; these are not OS CPU/memory quotas. It returns a small manifest with actual size and streamed SHA-256. Keep the files for later revisions. Reuse the source for local changes rather than recreating the entire figure. Do not load source code or image base64 into context when a file path suffices.
4. Open the actual PNG with the client's image-viewing tool. Check the mechanism, arrows, missing paths, overlap and page-width readability. Every text item must identify a component, operation, quantity or panel—not explain a finding. Move commentary to the external caption, including text disguised as a short title/label. Fix and inspect again, at most two additional renders. On size/time limits, simplify or report the limit; do not bypass it, launch parallel alternatives, or repeatedly raise the timeout. Successful rendering is not verification; report if image inspection is unavailable.

The bundled layout is a starting point, not a constraint on the research. If it cannot express the mechanism clearly, use an appropriate local vector tool with the same source-preservation and inspection requirements. Do not force a complex mechanism into a generic four-box flowchart. Missing source details may be left explicitly unresolved; they are not permission to fabricate a figure.

## Attach when requested

Use [the existing attachment workflow](../research-loop/references/operations.md#figures-and-attachments): prepare the PNG upload using the manifest, upload binary bytes, complete, reread the destination and attach the returned permanent media. Preserve unrelated blocks, caption/alt text and current page revision. SVG/PDF/source files are local deliverables; the image API does not accept them.

After a direct save, reread the page and confirm the intended attachment reference. If the server requires a proposal, report **awaiting review**, not saved. Do not bypass permissions, delete prior assets, or claim that an empty image block, generated code or uploaded-but-unattached file completes the requested page change.

Return the figure/page and any unresolved issue briefly. State a blocker instead of repeatedly uploading or silently changing methods.
