# Writing design — one canonical guide

The server's writing guide, `get_guide(topic:writing)`, owns writing design. Do not copy its full policy into skills or load every guide at startup. A technical report normally needs core, report, lists, annotations and evidence, followed by review. Reuse modules at the same revision within the task.

The guide's English is instruction language only. Follow core's output-language rule and annotations' naming/localization rules; reports, captions and clickable explanations follow the user's language unless explicitly requested otherwise.

| When | Read |
| --- | --- |
| Before substantive authoring | `get_guide(topic:writing)`: core, the shared rules and module index |
| Create or rename a plan/to-do | `section:tasks`: concrete target/action, purpose-first description and observable completion criteria |
| Task/Main analysis, research report, PI/student report | `section:report`: question/purpose → approach → findings → cause → conclusion/decision |
| Experiment results or an analysis, on a page or in chat | `section:results`, bundled as [Reporting results](results-reporting.md): experiment → observation → cause → conclusion, always concluding; run details of runs you started in `report_implementation` |
| Structured lists and indentation | `section:lists`: parent claims, child evidence, Markdown versus block item syntax |
| First-use technical terms, metrics, datasets or conditions | `section:annotations`: clickable explanations, definitions, escaping and reproduction details |
| Numbers, methods, examples, figures or sources | `section:evidence`: comparisons, uncertainty, source records and external captions |
| Explain with a visual | `section:visuals`, bundled as [Visual explanations](visual-explanations.md): question-led format, faithful interaction and explanation beside the visual and in the final reply |
| A mechanism or experiment design to draw | `section:explainer`: parts, links and steps the app lays out and steps through |
| An equation the reader must understand | `section:equation`: the LaTeX, each symbol named, the derivation as steps, values to try, and a plot when its shape is the point (a curve, a 3D surface, or level lines with constraint regions) — the app typesets, lights, steps and draws it |
| Before saving substantive writing | `section:review`: the request's explicit requirements first, then reader-path and evidence checks |
| Explicit instruction audit | `section:all`; unnecessary for ordinary work |

Experiment, result and claim pages also carry a bottom line, `fields.summary`, which the app shows before the body and in every list; `get_guide(topic:record, type)` has its contract. The body expands it rather than repeating it.

Then read only the relevant record/task/literature/meeting template. It supplies required content and storage semantics; it does not replace the writing guide. Existing project preferences, source preservation, author permissions, version checks, bounded computation and Main/Sub completion rules still apply.

Use the existing report request and page workflow. Do not rewrite old research records merely because the guide changed, claim that reading guidance proves writing quality, or hide material caveats in notes.
