---
description: Where a Research Loop project stands — its current answer, my work, reviews and questions waiting for me
argument-hint: "[project name or ID]"
---

Give a read-only briefing on the Research Loop project named in "$ARGUMENTS", or the project this repository is linked to (`.research-loop.json`, see the research-loop skill). If neither identifies one project, list the user's projects from `who_am_i` and ask which.

1. `who_am_i` once, then `get_project_instructions` for that project.
2. `get_research_brief` (first page only) and `get_my_research_tasks` for that project. If `who_am_i` reports questions for the user, `list_project_discussions` with `for_me:true`. Both are outside the tool list: call them with `call_tool_read`.
3. Reply in the user's language, at most 12 lines: the project's current answer and its main uncertainty; the user's assigned work, each with its next concrete step; pending reviews; questions waiting for them. Name pages by title. Mark what the records do not say as unknown.

Do not write anything, claim work or open more pages than the briefing needs.
