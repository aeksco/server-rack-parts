"""Narrow cable-tie plate: the cable_tie_plate with only the tie slot nearest the
screws, trimmed to just past it. The strap goes through the slot and around the
plate's cut edge.
"""

from build123d import Part

from models import cable_tie_plate

EDGE_MARGIN = 4.0  # wall left beyond the tie slot; carries the strap around the cut edge


def build() -> Part:
    return cable_tie_plate.build(tie_slots=1, edge_margin=EDGE_MARGIN)
