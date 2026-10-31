# CLAUDE.md

This is a **build123d starter project** for parametric, 3D-printable parts. The
scaffolding (uv, Makefile, exporter) is done. Your job is usually just to
write or edit a model in `models/`. Don't re-create the scaffolding.

## Quick start

```sh
make setup              # once: uv sync (Python 3.12 venv in .venv)
make                    # export all default models (power_switch_cover, cable_tie_plate): build/<slug>/<slug>.{stl,step,obj,png,svg}
make MODEL=<name>       # export models/<name>.py into build/<slug>/ (underscores become hyphens)
make list               # list models
make clean              # delete build/
make view MODEL=<name>  # push to OCP viewer (optional; needs viewer running)
```

Outputs land in `build/<slug>/` (gitignored), where `<slug>` is the model name with
underscores replaced by hyphens: `<slug>.stl` for slicers, `<slug>.svg` (underside outline, true 1:1 mm scale, print at 100%), `<slug>.step`
for CAD, `<slug>.obj` for mesh tools, `<slug>.png` an isometric render. Look at
the PNG to check the shape visually.

## Layout

```
models/<name>.py     one file per part; must define build() -> Part
scripts/export.py    generic exporter; imports models.<name>, calls build(), writes STL+STEP+OBJ+PNG+SVG
scripts/render.py    shaded isometric PNG render (numpy z-buffer, headless)
Makefile             thin wrapper around the exporter
pyproject.toml       deps managed by uv (build123d, numpy, pillow; ocp-vscode as dev dep)
```

## Making a new part

1. Copy `models/example.py` to `models/<name>.py` (or edit it in place for a one-off).
2. Keep **all dimensions as named constants at the top, in mm**. No magic numbers in geometry code.
3. Keep `build()` pure: no I/O, no `show()`, return the shape (`part.part` for `BuildPart`).
4. Run `make MODEL=<name>`. The exporter fails if the shape is invalid and prints
   volume and bounding box. Check those against what you intended.
5. To rename the project, edit `name` in `pyproject.toml`.

## build123d notes and gotchas

- Use the builder API (`with BuildPart() as p:`) and return `p.part`.
- Z is up. Use `Align.MIN` on Z to sit a box on the XY plane.
- `Mode.SUBTRACT` cuts holes; give cutters extra length so they pass fully through.
- Fillet/chamfer **early** (see models/power_switch_cover.py: select edges by position, cut pockets last), on simple geometry, before unioning more features.
  Filleting edges at junctions of merged solids often raises
  `Failed creating a fillet`; use a smaller radius, `max_fillet()`, or restructure.
- Docs: https://build123d.readthedocs.io
- Verify output programmatically (volume, `bounding_box()`, `is_valid`) rather than assuming.

## 3D-printing defaults to design for (FDM)

- Min wall ~1.2 mm; holes print slightly small, so add ~0.2 mm clearance for fits.
- Avoid overhangs > 45° or orient the part to avoid them; prefer a flat face on the bed.
- Export units are mm.

## Dependencies

Add with `uv add <pkg>`; never use bare `pip`. Python is pinned to 3.12 in
`.python-version` because the OCP (OpenCascade) wheels lag newer Pythons.
