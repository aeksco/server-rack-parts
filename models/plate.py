"""PDU power-switch cover plate: flat plate with 2 slotted screw holes and a raised
hollow "bubble" over the switch. The underside (against the ear) stays flat with a
blind pocket for the switch; the top is flat except for the raised bubble.

Coordinates (viewed from the front of the PDU, mm):
  X = 0 at the RIGHT edge of the rack ear, +X to the right (plate extends to negative X)
  Y = 0 at the vertical centre of the 1U panel, +Y up
  Z = 0 at the plate underside (the face against the ear)
"""

from build123d import (
    Align,
    Axis,
    Box,
    BuildPart,
    BuildSketch,
    Cylinder,
    Locations,
    Mode,
    Part,
    Rectangle,
    RectangleRounded,
    SlotOverall,
    extrude,
    fillet,
)

# --- Rack / PDU geometry (mm) ---------------------------------------------------
RACK_U = 44.45  # 1U panel height
HOLE_PITCH_Y = 31.75  # outer pair of the EIA-310 hole trio (1.25")
HOLE_X_FROM_RIGHT_EDGE = 7.9  # ASSUMPTION: hole centre from ear's right edge; measure and adjust

# --- Switch (minimum clearance) --------------------------------------------------
SWITCH_W = 16.0
SWITCH_H = 35.0
SWITCH_D = 8.0  # how far the switch stands proud of the panel
SWITCH_RIGHT_FROM_EDGE = 35.0  # switch right edge to ear right edge

# --- Pocket (cut into the underside; bubble size and position follow) ---
POCKET_W = 17.0  # switch width + extra on the right
POCKET_EXTRA_RIGHT = 1.0  # of POCKET_W, how much extends right of the switch (toward the screws)
POCKET_H = 36.0  # 1 mm of play over the switch height
POCKET_D = 9.0  # 1 mm of play over the switch depth

# --- Plate -----------------------------------------------------------------------
THICKNESS = 2.5
PLATE_W = 65.0  # extends left from the ear's right edge
PLATE_H = RACK_U - 1.0  # a little under 1U so it doesn't foul neighbouring units
BUBBLE_WALL = 2.5  # wall and roof thickness of the bubble over the switch

# --- Light holes (through the bubble roof, in a column over the switch) ----------
LIGHT_HOLE_COUNT = 3
LIGHT_HOLE_DIA = 4.0
LIGHT_HOLE_PITCH = 10.0  # centre-to-centre along the switch height

# --- Edge rounding (mm) -----------------------------------------------------------
PLATE_CORNER_R = 3.0  # plan-view corners of the plate
BUBBLE_CORNER_R = 2.0  # plan-view corners of the bubble
PLATE_TOP_EDGE_R = 1.0  # outer top edge of the plate
BUBBLE_TOP_EDGE_R = 1.5  # top edge of the bubble
BUBBLE_BASE_R = 1.0  # concave fillet where the bubble meets the plate
BOTTOM_EDGE_R = 0.5  # outer edge of the underside (kept small for the print bed)

# --- Screw slots (M6 cage nut screws) --------------------------------------------
SCREW_DIA = 6.0
SLOT_WIDTH = SCREW_DIA + 0.5  # vertical clearance
SLOT_LENGTH = SLOT_WIDTH + 3.0  # overall length; extra is horizontal wiggle room

# --- Corner cut-out (top-right) ---------------------------------------------------
# Clears the upper screw entirely, so the plate is held by the lower screw alone and
# can be removed without touching the upper one.
CORNER_CUT_W = 16.0  # measured from the plate's right edge
CORNER_CUT_H = 14.0  # measured from the plate's top edge
CORNER_CUT_OUTER_R = 2.0  # rounding where the cut meets the plate's top / right edges
CORNER_CUT_INNER_R = 3.0  # rounding of the inside corner of the cut


def build() -> Part:
    switch_cx = -(SWITCH_RIGHT_FROM_EDGE + SWITCH_W / 2)
    pocket_w, pocket_h, pocket_d = POCKET_W, POCKET_H, POCKET_D
    # Pocket is centred vertically on the switch; horizontally it spans the switch
    # plus POCKET_EXTRA_RIGHT on the right-hand side.
    pocket_cx = switch_cx + (POCKET_EXTRA_RIGHT - (POCKET_W - SWITCH_W - POCKET_EXTRA_RIGHT)) / 2
    bubble_w = pocket_w + 2 * BUBBLE_WALL
    bubble_h = pocket_h + 2 * BUBBLE_WALL
    bubble_top = pocket_d + BUBBLE_WALL
    eps = 1e-3

    slot_cx, slot_cy = -HOLE_X_FROM_RIGHT_EDGE, -HOLE_PITCH_Y / 2

    def on_plate_perimeter(e) -> bool:
        # Any plate-outline edge, i.e. not the screw slot and not the bubble
        c = e.center()
        in_slot = abs(c.X - slot_cx) < SLOT_LENGTH / 2 + eps and abs(c.Y - slot_cy) < SLOT_WIDTH / 2 + eps
        in_bubble = abs(c.X - pocket_cx) < bubble_w / 2 + eps and abs(c.Y) < bubble_h / 2 + eps
        return not in_slot and not in_bubble

    with BuildPart() as part:
        # Flat base plate with slotted screw holes
        with BuildSketch() as sk:
            top = PLATE_H / 2
            with Locations((-PLATE_W / 2, 0)):
                RectangleRounded(PLATE_W, PLATE_H, PLATE_CORNER_R)
            with Locations((slot_cx, slot_cy)):
                SlotOverall(SLOT_LENGTH, SLOT_WIDTH, mode=Mode.SUBTRACT)
            # Square cut-out in the top-right corner, with rounded edges
            with Locations(((-CORNER_CUT_W + 1.0) / 2, top - CORNER_CUT_H / 2 + 0.5)):
                Rectangle(CORNER_CUT_W + 1.0, CORNER_CUT_H + 1.0, mode=Mode.SUBTRACT)

            def vertex_at(x, y):
                return [v for v in sk.vertices() if abs(v.X - x) < eps and abs(v.Y - y) < eps]

            fillet(vertex_at(-CORNER_CUT_W, top) + vertex_at(0, top - CORNER_CUT_H), CORNER_CUT_OUTER_R)
            fillet(vertex_at(-CORNER_CUT_W, top - CORNER_CUT_H), CORNER_CUT_INNER_R)
        extrude(amount=THICKNESS)

        # Raised bubble block over the switch
        with Locations((pocket_cx, 0, 0)):
            Box(bubble_w, bubble_h, bubble_top, align=(Align.CENTER, Align.CENTER, Align.MIN))

        # Round everything while the geometry is still simple; pocket is cut last
        edges = part.edges()
        in_bubble = lambda e: abs(e.center().X - pocket_cx) < bubble_w / 2 + eps and abs(e.center().Y) < bubble_h / 2 + eps
        fillet(
            [e for e in edges.filter_by(Axis.Z) if in_bubble(e) and e.center().Z > THICKNESS],
            radius=BUBBLE_CORNER_R,
        )
        fillet(part.edges().filter_by_position(Axis.Z, bubble_top - eps, bubble_top + eps), radius=BUBBLE_TOP_EDGE_R)
        fillet(
            [e for e in part.edges().filter_by_position(Axis.Z, THICKNESS - eps, THICKNESS + eps) if in_bubble(e)],
            radius=BUBBLE_BASE_R,
        )
        fillet(
            [e for e in part.edges().filter_by_position(Axis.Z, THICKNESS - eps, THICKNESS + eps) if on_plate_perimeter(e)],
            radius=PLATE_TOP_EDGE_R,
        )
        fillet(
            [e for e in part.edges().filter_by_position(Axis.Z, -eps, eps) if on_plate_perimeter(e)],
            radius=BOTTOM_EDGE_R,
        )

        # Blind pocket cut from the underside for the switch
        with Locations((pocket_cx, 0, 0)):
            Box(
                pocket_w,
                pocket_h,
                pocket_d,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
                mode=Mode.SUBTRACT,
            )

        # Light holes through the bubble roof
        ys = [(i - (LIGHT_HOLE_COUNT - 1) / 2) * LIGHT_HOLE_PITCH for i in range(LIGHT_HOLE_COUNT)]
        with Locations(*[(switch_cx, y, bubble_top) for y in ys]):
            Cylinder(
                LIGHT_HOLE_DIA / 2,
                BUBBLE_WALL * 2,
                align=(Align.CENTER, Align.CENTER, Align.CENTER),
                mode=Mode.SUBTRACT,
            )
    return part.part
