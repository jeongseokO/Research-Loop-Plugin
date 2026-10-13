# Writing design — one canonical guide

The server's `get_page_writing_guide` owns writing design. Do not copy its full policy into skills or load every guide at startup. A technical report normally needs core, report, lists, annotations and evidence, followed by review. Reuse modules at the same revision within the task.

The guide's English is instruction language only. Follow core's output-language rule and annotations' naming/localization rules; reports, captions and clickable explanations follow the user's language unless explicitly requested otherwise.

| When | Read |
| --- | --- |
| Before substantive authoring | `get_page_writing_guide(section="core")`: shared rules and module index |
| Create or rename a plan/to-do | `section="tasks"`: concrete target/action, purpose-first description and observable completion criteria |
| Task/Main analysis, research report, PI/student report | `section="report"`: question/purpose → approach → findings → interpretation/limits → decision |
| Structured lists and indentation | `section="lists"`: parent claims, child evidence, Markdown versus block item syntax |
| First-use technical terms, metrics, datasets or conditions | `section="annotations"`: clickable explanations, definitions, escaping and reproduction details |
| Numbers, methods, examples, figures or sources | `section="evidence"`: comparisons, uncertainty, source records and external captions |
| A mechanism or experiment design to draw | `section="explainer"`: parts, links and steps the app lays out and steps through |
| Before saving substantive writing | `section="review"`: the request's explicit requirements first, then reader-path and evidence checks |
| Explicit instruction audit | `section="all"`; unnecessary for ordinary work |

Experiment, result and claim pages also carry a bottom line, `fields.summary`, which the app shows before the body and in every list; `get_research_properties(type)` has its contract. The body expands it rather than repeating it.

Then read only the relevant record/task/literature/meeting template. It supplies required content and storage semantics; it does not replace the writing guide. Existing project preferences, source preservation, author permissions, version checks, bounded computation and Main/Sub completion rules still apply.

Use the existing report request and page workflow. Do not rewrite old research records merely because the guide changed, claim that reading guidance proves writing quality, or hide material caveats in notes.
