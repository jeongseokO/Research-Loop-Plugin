---
description: Explain a method from this codebase (or a Research Loop method page) as a step-by-step explainer on its method page
argument-hint: "[method name, source files or page]"
---

Draw "$ARGUMENTS" as an explainer: the app lays it out and steps through it; you state only parts, links and steps. Follow the research-loop skill for identity, instructions and writes.

1. **Understand it from the source.** Read the implementation the user named, or find it with a narrow search, until you can name each component, what passes between them and in what order. Read the paper or method page when one exists. Mark what the code does not settle as unknown; never fill gaps with a typical design.
2. **Find the page.** The linked project (`.research-loop.json`) or ask; `query_research_objects` with `type:"method"`; `get_research_page` (outline, then the 작동 원리 section). Ask before creating a method page.
3. **Build the explainer** with `get_guide(topic:writing, section:explainer)`: 3–7 steps, each one change the reader should notice; labels use the names in the code and paper; cells only for real state (a cache, a mask, a selection), and the caption says when counts are schematic.
4. **Place it** under 작동 원리 with `patch_research_page`: one sentence before it saying what it answers, then the explainer with its caption. Report what each step shows in one line each and whether the save was applied or proposed.
