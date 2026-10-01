# Presentation studio and editable PowerPoint

Use **페이지 도구 → 발표 제작 · PPTX** on a saved research page. Converting an ordinary page produces an unsaved, independent deck; Save creates a note in `미팅 발표`. Saved decks reopen for editing; Save uses their captured page revision and the existing human permission/review flow. Web and the full plugin workspace use the same editor. The legacy compact panel does not contain the studio.

## Authoring

Read the presentation writing guide, project examples and exact evidence first. Choose a headline argument; place one claim/question and its evidence on each slide. Use a neutral 16:9 canvas, readable text, aligned comparisons and restrained colors. The editor supports draggable/resizable text, images, tables, native charts, labeled shapes and arrows, slide ordering/duplication, undo/redo, notes, source links and explicit page imports. Keep scientific figures and source data intact. Images keep their aspect ratio. Lines use the input category order at equal spacing, not a continuous numerical X scale. Use an imported research plot when error bars, log scales, unequal X spacing or other scientific encodings are needed. Never fabricate values to fill a chart.

## Document contract for AI edits

Use existing page read/patch/save tools with their actual revision. Read the complete document before changing layout or membership. A deck is an ordinary version-1 ResearchDocument:

- The first block is `{id:"presentation-manifest",type:"code",language:"research-loop-deck",text:JSON.stringify(manifest)}`.
- `manifest` is `{version:1,slides:[{id,notes,source,elements:[{blockId,kind,x,y,w,h,fontSize,color,fill,bold,align,chartType}]}]}`.
- Every slide `id` references a unique ordinary level-2 heading block containing its headline.
- Every `blockId` references a unique ordinary content block. Keep all referenced blocks in document order. Every block other than the manifest must be used exactly once; no hidden or orphan blocks.
- `kind`: `text`, `image`, `table`, `chart`, `shape`, `arrow`. Image uses an image/plot block; table/chart uses a table block. Shape/arrow/text normally use paragraph blocks. A chart uses column 0 as categories and columns 1–4 as numerical series of the same unit; no missing-value interpolation or uncertainty parsing occurs.
- Geometry is in a 1280×720 canvas: x/y ≥0, width ≥24, height ≥12, within bounds. Reserve x=72…1208, y=184…634 for body content; the headline and footer have fixed slots. Text sizes are 12–60 pt; use 24–28 pt for main text. Colors are six hex digits without `#`; align is left/center/right; chartType is bar/line. Title ≤300 characters, notes ≤12000, source ≤4000; at most 80 slides and 250 total page blocks within the existing 512 KiB limit.
- For wording-only edits, patch the referenced content block; preserve its ID. For slide/element additions, removals or order changes, update the manifest and blocks together in one revision-checked write. Never leave new blocks outside the manifest or silently discard another author's slide.
- Put a short readable citation label on the first line of `source`; it appears in the slide footer. Keep full source URLs/revisions on following lines and speaker notes in `notes`. Content and uploaded media remain ordinary page blocks so existing media scope, ownership and audit checks apply. Files copied from a different page must be uploaded for the new page before saving; never reuse foreign private storage paths or short-lived signed URLs.

## Delivery

PPTX exports contain native text, shapes, tables and charts with their embedded workbook; imported images are individual raster images. Notes and sources are exported as speaker notes. Text, table cells or image captions that exceed their box, and overlapping chart labels, block export rather than silently clipping evidence. Use a brief image caption and keep the full explanation in notes. Check the rendered output before calling it ready. Font substitution and native Office chart layout may differ; native editable equations, arbitrary PPTX layout import and animation/timing authoring are not implemented. Existing PPT/PPTX/PDF example uploads are references, not an import of their complete editable layout.

For ChatGPT collaboration, save first and choose **ChatGPT와 다듬기**. This opens the explicit request composer for that saved page; the person still chooses what to send. Do not imply that opening the composer runs AI work or saves its result.
