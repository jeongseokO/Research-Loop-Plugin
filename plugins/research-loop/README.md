# Research Loop

[Research Loop](https://airesearchloop.com) keeps a research team's work in one place: questions, methods, experiments and what their results mean, papers and their readings, to-dos and plans. This plugin brings it into Claude. Claude reads and edits your projects through the Research Loop connector, and the plugin's skills tell it how a good record is written.

## In Claude chat and Cowork

Add the marketplace `jeongseokO/Research-Loop-Plugin` in **Customize → Plugins → Add → Add marketplace** and install Research Loop. Then connect Research Loop in the plugin's Connectors tab and sign in with your Research Loop account. If you already added the connector at `https://airesearchloop.com/mcp`, it is the same one. Ask in your own words:

- "Where does the KV cache project stand?"
- "Record this run as an experiment page: here are the logs."
- "Read this paper with me and add the key sentences."

## In Claude Code

Claude Code signed in to the same Claude account picks up the plugin the next time it starts (if a running session says `Plugins changed`, run `/reload-plugins`). Claude Code that runs on an API key installs it from the terminal:

```sh
claude plugin marketplace add jeongseokO/Research-Loop-Plugin
claude plugin install research-loop@research-loop
```

Either way, open `/mcp` once, choose `plugin:research-loop:research` and sign in. The commands:

| Command | What it does |
| --- | --- |
| `/research-loop:brief` | Where a project stands: its current answer, your work, reviews and questions waiting for you. Reads only. |
| `/research-loop:record` | Records the experiment you just ran in this repository: runs, settings, results table and bottom line, with the values from your result files. |
| `/research-loop:explain` | Reads a method in your code and draws it step by step on its method page. |
| `/research-loop:task` | Takes one AI request your team queued for this connection and carries it to review. |

The `research-plot` and `method-figure` skills draw charts and method diagrams as image files on your computer, in Python, when a page's own table chart or diagram is not enough.

## What it sends

The connector talks to `https://airesearchloop.com/mcp` over OAuth. It carries what Claude asks for, such as a page to read or an edit to save, and brings back what your account may see. The plugin keeps no credentials. Three helpers run on your computer: a script that reads changed code lines from git so an implementation report quotes them exactly (those lines go into the report), a script that uploads an image you asked to put on a page, and the figure scripts, which draw locally and send nothing.

## What it may do

Claude acts for the person who connected it, with that person's role in each project: at once where they are Owner or Semi-Owner, and elsewhere once the project's owner approves. It reads the current revision and saves only the change you asked for. A Viewer's AI reads only. An Editor's AI edits the notes, literature, experiments, datasets and results its person created; other changes become review requests that wait for a person's approval. A Semi-Owner's AI edits research content directly, and deleting a project or changing who can see it stays with the owner. Reading tools are marked read-only; Claude asks before the others run unless you allowed them.

## License

The plugin's files (skills, commands, references, scripts and manifests) are licensed under the [Apache License 2.0](LICENSE). The license does not cover the Research Loop name and logo (its section 6), and using the Research Loop service is governed by its [Terms](https://airesearchloop.com/terms).

[Privacy policy](https://airesearchloop.com/privacy) · [Terms](https://airesearchloop.com/terms) · [Connection guide](https://airesearchloop.com/guide/ai)
