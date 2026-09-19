## Figures and attachments

For literature, first inspect and reuse informative original paper figures/tables following `get_literature_review_template`: authorized source, faithful extraction, readable labels, attribution and explanation nearby. Preserve original embedded text; do not redraw a paper figure just to remove it. If access, reuse or extraction is unavailable, identify the missing visual and give its source and grounded explanation.

For newly authored figures, read `get_visualization_guide` for the relevant technique; methodology overviews use the bundled [method-figure skill](../../method-figure/SKILL.md). Generate from verified data/structure. In either case, visually inspect the actual local image before uploading. Research Loop stores images, not rendered plots from arbitrary code. Never fabricate measurements or report a placeholder as completed.

Before upload, keep only essential labels, axes, units, legends, data values or mechanism symbols in a new figure. Move all explanatory sentences, conclusions and commentary boxes to the real page block `caption`. Text in canvas margins, titles or annotations is still inside the image; do not bake in a caption. Alt text is separate, not a replacement for the visible caption. This does not authorize erasing text from original paper figures.

1. Call `prepare_research_media_upload` with the file name, actual size and SHA-256, within current server limits.
2. PUT the exact bytes to its private `uploadUrl` with Content-Type and **no additional Authorization header**. The bundled [upload helper](../../../scripts/upload-image.mjs) takes the prepare response through stdin and the local file path as its argument, keeping the URL out of command-line arguments. It validates the fixed Research Loop Storage destination.
3. Call `complete_research_media_upload` with `upload_id`. After an uncertain PUT, try completion before preparing a duplicate upload. Reuse the prepare key only for the same file and metadata.
4. Attach the returned permanent `media` reference with caption and alt text after rereading the target page. Upload success alone is not a page save; protected saves may still require review.

Prefer binary upload to base64 in model context. `upload_research_media` is a fallback only for files within its smaller limit. Export unsupported figure formats to PNG. To inspect an existing attachment, read its page, then use `get_research_media` with its attachment block ID. Upload and download URLs are temporary credentials: never save them in content, logs or final responses. Do not delete historical, unattached or pending-review assets as cleanup.
