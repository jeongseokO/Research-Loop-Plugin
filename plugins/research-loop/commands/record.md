---
description: Record the experiment just run in this repository as a Research Loop experiment page — runs, settings, results table and bottom line
argument-hint: "[result files, run folder or experiment name]"
---

Record in Research Loop the experiment the user ran here: "$ARGUMENTS". Follow the research-loop skill for identity, project instructions and writes.

1. **Evidence from this repository only.** Read the result files, logs and configs named above (ask which if none are named), and the commands run in this session. Use the values as written in those files; never type numbers from memory. Do not start new runs, long jobs or recursive scans of large folders.
2. **Find the page.** Use the linked project (`.research-loop.json`) or ask. `query_research_objects` with `type:"experiment"` for a page testing the same question: prefer updating it. Ask before creating a new page. Read `get_research_record_template` (`type:"experiment"`), `get_research_properties` (`type:"experiment"`) and `get_page_writing_guide` core, then evidence.
3. **Write what a colleague needs to judge it.** The question it tests and what changed between conditions; a run inventory with every run, including failed, partial and excluded ones with reasons; a results table from the files, with `table.chart` for the comparison the reader should see; what it shows and what it does not yet. Put commands, paths, commits and seeds under a reproducibility heading. Set `fields.summary` (bottom line, verdict, evidence IDs) and link the question, method and dataset when they exist.
4. **Save the smallest change**: `patch_research_page` on an existing page at its read revision, or `create_research_object` then `save_research_page` for a new one. Report applied versus proposed, the page title and anything left unrecorded.
