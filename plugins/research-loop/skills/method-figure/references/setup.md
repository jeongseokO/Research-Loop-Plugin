# Local rendering environment

The renderer needs Python 3.9+ and Matplotlib. Reuse an available environment first; an import check is sufficient. No image-model key is required. AI planning and image inspection still consume the client's normal usage allowance.

If the dependency is missing and installation is authorized, create a dedicated virtual environment in the user's working directory (not the plugin cache), then install the pinned requirement from [requirements.txt](../scripts/requirements.txt):

```sh
python3 -m venv .research-loop-figures
.research-loop-figures/bin/python -m pip install -r <skill-directory>/scripts/requirements.txt
.research-loop-figures/bin/python <skill-directory>/scripts/render-method-figure.py INPUT.json --output-dir OUTPUT
```

Resolve `<skill-directory>` to the installed skill's actual path. On Windows the environment interpreter is `.research-loop-figures\Scripts\python.exe`.

Do not modify the user's system Python, weaken client permissions, install a separate AI service, or put credentials in scripts. If installation is unavailable, report the missing dependency and retain the source specification.

Short English technical labels are usually suitable for paper figures. For other scripts, use an installed font covering those characters and inspect the actual output; do not accept missing-glyph boxes. SVG keeps text elements and therefore needs the corresponding font when opened elsewhere. PDF embeds font subsets for portable viewing. Inspect the exported form used for publication too.
