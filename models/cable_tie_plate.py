"""Cable-tie plate: flat plate held by both 1U rack screws, with two tie slots so a
cable tie or Velcro wrap can strap a wire bundle (running vertically) to its face.
Both faces are flat.

Coordinates (viewed from the front of the rack, mm):
  X = 0 at the RIGHT edge of the rack ear, +X to the right (plate extends to negative X)
  Y = 0 at the vertical centre of the 1U panel, +Y up
  Z = 0 at the plate underside (the face against the ear)
"""

from build123d import (
    Axis,
    BuildPart,
    BuildSketch,
    Locations,
    Mode,
    Part,
    RectangleRounded,
    SlotOverall,
    extrude,
    fillet,
)

# --- Rack geometry (mm), same as power_switch_cover ----------------------------
RACK_U = 44.45  # 1U panel height
HOLE_PITCH_Y = 31.75  # outer pair of the EIA-310 hole trio (1.25")
HOLE_X_FROM_RIGHT_EDGE = 7.9  # ASSUMPTION: hole centre from ear's right edge; measure and adjust

# --- Screw slots (M6 cage nut screws) --------------------------------------------
SCREW_DIA = 6.0
SLOT_WIDTH = SCREW_DIA + 0.5  # vertical clearance
SLOT_LENGTH = SLOT_WIDTH + 3.0  # overall length; extra is horizontal wiggle room
SCREW_HEAD_DIA = 12.0  # keep the tie slots clear of the screw heads

# --- Tie slots (vertical, either side of the bundle) -----------------------------
TIE_SLOT_LENGTH = 15.0  # vertical; fits 1/2" (12.7 mm) Velcro and standard cable ties
TIE_SLOT_WIDTH = 10.0
TIE_SLOT_SPACING = 20.0  # centre-to-centre; roughly the bundle width
TIE_SLOT_GAP_FROM_HEAD = 3.0  # clearance from the screw head to the first tie slot

# --- Plate -----------------------------------------------------------------------
THICKNESS = 4.0
PLATE_H = RACK_U - 1.0  # a little under 1U so it doesn't foul neighbouring units
EDGE_MARGIN = 6.0  # from the far tie slot to the plate's left edge

# --- Edge rounding (mm) -----------------------------------------------------------
PLATE_CORNER_R = 3.0  # plan-view corners of the plate
PLATE_TOP_EDGE_R = 1.0  # outer top edge of the plate
BOTTOM_EDGE_R = 0.5  # outer edge of the underside (kept small for the print bed)


def build(tie_slots: int = 2, edge_margin: float = EDGE_MARGIN) -> Part:
    screw_x = -HOLE_X_FROM_RIGHT_EDGE
    # Worst case the screw sits at the left end of its slot
    head_left = screw_x - (SLOT_LENGTH - SLOT_WIDTH) / 2 - SCREW_HEAD_DIA / 2
    tie_x1 = head_left - TIE_SLOT_GAP_FROM_HEAD - TIE_SLOT_WIDTH / 2
    tie_xs = [tie_x1 - i * TIE_SLOT_SPACING for i in range(tie_slots)]
    plate_w = -(tie_xs[-1] - TIE_SLOT_WIDTH / 2) + edge_margin
    eps = 1e-3

    with BuildPart() as part:
        with BuildSketch():
            with Locations((-plate_w / 2, 0)):
                RectangleRounded(plate_w, PLATE_H, PLATE_CORNER_R)
        extrude(amount=THICKNESS)

        # Round the outer edges while the plate is still a simple slab; cut holes last
        fillet(part.edges().filter_by_position(Axis.Z, THICKNESS - eps, THICKNESS + eps), radius=PLATE_TOP_EDGE_R)
        fillet(part.edges().filter_by_position(Axis.Z, -eps, eps), radius=BOTTOM_EDGE_R)

        # Slotted holes for both rack screws
        with BuildSketch() as holes:
            with Locations((screw_x, HOLE_PITCH_Y / 2), (screw_x, -HOLE_PITCH_Y / 2)):
                SlotOverall(SLOT_LENGTH, SLOT_WIDTH)
            # Tie slots run vertically, parallel to the bundle
            with Locations(*[(x, 0) for x in tie_xs]):
                SlotOverall(TIE_SLOT_LENGTH, TIE_SLOT_WIDTH, rotation=90)
        extrude(holes.sketch, amount=THICKNESS, mode=Mode.SUBTRACT)
    return part.part
