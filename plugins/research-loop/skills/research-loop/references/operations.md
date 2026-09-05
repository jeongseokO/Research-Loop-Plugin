# Research Loop operating contract

Read this reference for writes, rich research pages, AI task transitions, protected changes, review work, or conflict recovery. MCP tool schemas remain authoritative for exact fields and limits.

## Intent to tool map

| Intent | Read first | Action |
| --- | --- | --- |
| Identify agent and access | — | `who_am_i` |
| Find a project | `list_projects` | — |
| Reconstruct current project | `sync_project` or `get_project_context` | — |
| Read or edit detailed research content | `get_research_page` | `save_research_page` |
| Inspect an uploaded page attachment | `get_research_page` | `get_research_media` using the attachment block ID |
| Add a generated figure | `get_research_page` | prepare/upload/complete media, then `save_research_page` |
| Create a project | `who_am_i` | `create_project` with revision `0` |
| Capture an unstructured note | project sync | `capture_inbox` |
| Add a question, paper, method, experiment, result, decision, or claim | project sync | `create_research_object` |
| Add scheduled work | project sync | `create_plan` |
| Add a conference or internal due date | project sync | `create_deadline` |
| Replace a weekly plan | project sync | `set_week_plan` |
| Change existing project or object state | project sync | the matching update/status/link/archive tool |
| Inspect protected proposals | project sync | `list_change_requests` |
| Approve or reject a proposal | project sync | `review_change_request` |
| Process queued AI work | `list_ai_tasks`, then `get_ai_task` | claim/update/complete tools |
| Inspect AI provenance | `who_am_i` | `get_agent_activity` |

## Revision and idempotency rules

- Project mutations use the project stream revision returned by a complete sync.
- Rich-page replacement uses the page revision from `get_research_page`, never the project revision.
- Task transitions use the task's `currentRevision`; the task may use a project or private workspace stream.
- One logical mutation gets one stable idempotency key. A network retry with unknown outcome reuses it.
- A returned conflict is a stored receipt. Reload state, revalidate intent, and use a new key only for the revised attempt.
- Dependent changes require a fresh sync after the preceding mutation.

## Direct changes and proposals

Safe creation actions—new inbox entries, research objects, plans, and deadlines—can apply directly for Owner and Editor agents with write scope.

Protected actions include:

- replacing a rich research page;
- replacing a weekly plan;
- updating existing research objects or statuses;
- linking existing objects;
- changing project metadata;
- archiving a project.

An Owner agent with the required scope applies these directly. An Editor agent with propose scope receives a change request. A Viewer cannot write. Only an Owner with review scope can approve or reject. Never report a proposal as committed.

## Rich pages

`save_research_page` replaces the complete document snapshot. Preserve untouched blocks and unique block IDs. The document uses version `1`, at most 250 blocks, and at most 512 KiB.

Available blocks include paragraphs, headings, bulleted and numbered lists, quotes, callouts, code, tables, images, plots, files, and dividers. Storage media must already exist under the exact target project/object folder. External media must use HTTP(S).

If `hasPageSnapshot` is false, retain the returned legacy-summary paragraph unless the user explicitly replaces it.

Private storage attachments can be inspected with `get_research_media` after reading the containing page. The returned download URL expires in 60 seconds. Never persist or publish that URL; retain the original storage reference and block ID instead. This read tool does not upload or generate media.

## Generate and attach figures

1. Use the real experiment data and your available rendering tools to generate a local PNG/JPEG/WebP/GIF. Include units, legible axes, and captions. Do not fabricate missing results; label synthetic examples.
2. Prefer `prepare_research_media_upload` with the file name, byte size and SHA-256 (up to 10 MiB). Reuse its idempotency key for the same file after uncertain responses; use a new key when bytes or metadata change.
3. PUT the exact binary bytes to the returned private `uploadUrl` with its Content-Type. Do not add the Research Loop API key or other Authorization header. The bundled [upload helper](../../../scripts/upload-image.mjs) accepts the prepare result JSON through stdin and the local file path as its argument, keeping the URL out of command-line arguments. It only uploads to Research Loop’s fixed Storage host and object path.
4. Call `complete_research_media_upload` with `upload_id`. It verifies the image signature, size, SHA-256 and fresh permissions. Retry completion after an uncertain PUT before preparing a new file.
5. Use the returned permanent `media` reference in an image/plot block. Read the latest page, preserve existing blocks, append the figure with caption and alt, and call `save_research_page`. Upload success alone is not a page save; Editor saves still require Owner review.

For images up to 384 KiB decoded, `upload_research_media` accepts standard base64 directly. Prefer binary PUT when shell/file tools are available, to avoid large model-context payloads. The server permits 64 new uploads per human per 24 hours. SVG/PDF figures should be exported as PNG for inline display.

Upload URLs are private two-hour capabilities, unlike 60-second download URLs. Never store either in research content or expose them in final answers. A revoked user can no longer complete or attach an upload, although an already-issued URL can upload to its reserved path until expiry. Files are private to project members, not uploader-only drafts. Unattached uploads are retained; never delete historical or pending-review assets as cleanup.

## AI task lifecycle

Follow `list_ai_tasks` pagination even when a filtered page is empty but has `nextCursor`.

Normal flow:

1. `queued → claimed`
2. `claimed → running`
3. `running → review_required` for proposal or review work
4. requester or Owner review

Direct `running → completed` is only valid for create-mode work with real result references. Only the claiming agent may update the task. Failed tasks require an error reason.

## Result reporting

After actions, report only what helps the researcher continue:

- project and affected objects;
- what was applied;
- what is pending Owner review;
- conflicts that changed the requested action;
- the smallest unresolved user decision.

Avoid connection tutorials, generic prompt suggestions, and repeated MCP explanations when the connection is healthy.
