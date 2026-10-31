"""Rack ear: right-angle bracket that serves as one rack rail of a rack-mount case.

The front flange carries EIA-310 square holes for M6 cage nuts; the side flange is
screwed to the inside of the case wall with one countersunk screw, head facing the
equipment so it sits flush.

One part fits both sides: the hole pattern and the side screw are symmetric about
mid-height, so flipping the ear upside down (180 degrees about Y) turns a right
ear into a left ear.

Coordinates (right-hand ear, viewed from the front of the rack, mm):
  X = 0 at the rack opening edge (inner edge of the front flange), +X outward
  Y = 0 at the front face, +Y toward the back of the case
  Z = 0 at the bottom of the ear, +Z up
"""

from build123d import (
    Box,
    BuildPart,
    BuildSketch,
    CounterSinkHole,
    Locations,
    Mode,
    Part,
    Plane,
    Polygon,
    extrude,
)

# --- Size ------------------------------------------------------------------------
RACK_UNITS = 2  # height in U; any whole number

# --- EIA-310 rack geometry (mm) ----------------------------------------------------
RACK_U = 44.45
HOLE_Z_IN_U = (6.35, 22.225, 38.1)  # hole centres from the bottom of each U
SQUARE_HOLE = 9.5  # cage nut hole, 9.5 x 9.5
HOLE_X = (465.1 - 450.85) / 2  # 7.125: hole centre to rack opening edge

# --- Bracket -----------------------------------------------------------------------
THICKNESS = 2.0  # typical rack rail steel; M6 cage nuts clip 1.8-2.6 mm panels
FLANGE_W = 18.0  # front flange, opening edge to outer face of the side flange
SIDE_DEPTH = 20.0  # side flange, front face to back edge
CAGE_NUT_W = 13.5  # cage nut wings; checked against the side flange below

# --- Case screw (countersunk, ISO 10642 / DIN 7991 M3; M4 heads are deeper than 2 mm)
CASE_SCREW_CLEARANCE = 3.4
CASE_SCREW_HEAD_DIA = 6.3  # countersink diameter at the surface (head 6.0 + 0.3)
COUNTERSINK_ANGLE = 90


def build(units: int = RACK_UNITS) -> Part:
    height = units * RACK_U
    side_inner_x = FLANGE_W - THICKNESS
    assert HOLE_X + CAGE_NUT_W / 2 < side_inner_x, "cage nut would hit the side flange"

    with BuildPart() as part:
        # L-shaped profile in plan view, extruded to the full rack height
        with BuildSketch():
            Polygon(
                (0, 0),
                (FLANGE_W, 0),
                (FLANGE_W, SIDE_DEPTH),
                (side_inner_x, SIDE_DEPTH),
                (side_inner_x, THICKNESS),
                (0, THICKNESS),
                align=None,
            )
        extrude(amount=height)

        # Square cage nut holes through the front flange
        zs = [u * RACK_U + z for u in range(units) for z in HOLE_Z_IN_U]
        with Locations(*[(HOLE_X, THICKNESS / 2, z) for z in zs]):
            Box(SQUARE_HOLE, THICKNESS * 2, SQUARE_HOLE, mode=Mode.SUBTRACT)

        # One countersunk case screw at mid-height, head on the inner face of the side flange
        y = THICKNESS + (SIDE_DEPTH - THICKNESS) / 2
        with Locations(Plane(origin=(side_inner_x, y, height / 2), z_dir=(-1, 0, 0))):
            CounterSinkHole(
                radius=CASE_SCREW_CLEARANCE / 2,
                counter_sink_radius=CASE_SCREW_HEAD_DIA / 2,
                depth=THICKNESS,
                counter_sink_angle=COUNTERSINK_ANGLE,
            )
    return part.part
