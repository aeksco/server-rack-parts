# build123d starter

Parametric 3D-printable parts in Python with [build123d](https://build123d.readthedocs.io), exported to STL, STEP and OBJ, plus an isometric PNG preview and a 1:1 SVG underside outline.

Requires [uv](https://docs.astral.sh/uv/) and make.

```sh
make setup              # install deps into .venv (run once)
make                    # export build/plate.{stl,step,obj,png,svg}
make MODEL=mypart       # export models/mypart.py
make png MODEL=mypart   # export only if build/mypart.png is stale
make list               # list available models
make help               # show all targets
```

Add a part by copying `models/example.py`; each model defines `build()`.
See `CLAUDE.md` for conventions (written for AI agents, useful for humans too).

To reuse as a template: copy this folder, delete `.git`, `build/` and `.venv/`, rename the project in `pyproject.toml`, and replace `models/example.py`.
