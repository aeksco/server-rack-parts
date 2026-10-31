# build123d starter

Parametric 3D-printable parts in Python with [build123d](https://build123d.readthedocs.io), exported to STL and STEP.

Requires [uv](https://docs.astral.sh/uv/) and make.

```sh
make setup           # install deps
make                 # build/example.stl + build/example.step
make MODEL=myparm    # build models/myparm.py
```

Add a part by copying `models/example.py`; each model defines `build()`.
See `CLAUDE.md` for conventions (written for AI agents, useful for humans too).

To reuse as a template: copy this folder, delete `.git`, `build/` and `.venv/`, rename the project in `pyproject.toml`, and replace `models/example.py`.
