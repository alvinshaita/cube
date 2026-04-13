"""Convert a :class:`rubik_toolkit.cube.Cube` into a :class:`CubieCube`.

The ``Cube`` class stores each physical cubie as a dict mapping face
directions to color names. This module walks those cubies in a fixed
order and fills in the cubie-level ``(cp, co, ep, eo)`` arrays used
by the Kociemba solver.

Only 3x3 cubes are supported; callers should check ``cube.size == 3``
before invoking ``from_cube``.
"""
from __future__ import annotations

from .cubie import CubieCube


_UD_COLORS = frozenset({"yellow", "white"})
_FB_COLORS = frozenset({"red", "orange"})
_LR_COLORS = frozenset({"blue", "green"})


# For each corner position, the (x, y, z) coordinate in ``cube.cube``
# and the ordered tuple of face keys used to determine orientation.
# The face at index 0 is the U or D face of the position; orientation
# equals the index in this tuple where the U/D-color sticker sits.
_CORNER_DATA: list[tuple[tuple[int, int, int], tuple[str, str, str]]] = [
	((0, 0, 2), ("u", "r", "f")),  # 0 URF
	((0, 0, 0), ("u", "f", "l")),  # 1 UFL
	((2, 0, 0), ("u", "l", "b")),  # 2 ULB
	((2, 0, 2), ("u", "b", "r")),  # 3 UBR
	((0, 2, 2), ("d", "f", "r")),  # 4 DFR
	((0, 2, 0), ("d", "l", "f")),  # 5 DLF
	((2, 2, 0), ("d", "b", "l")),  # 6 DBL
	((2, 2, 2), ("d", "r", "b")),  # 7 DRB
]


# Color-set to corner index, matching the solved-cube color layout
# (yellow on top, white on bottom, red front, orange back, green right,
# blue left).
_CORNER_COLORS_TO_INDEX: dict[frozenset, int] = {
	frozenset({"yellow", "green", "red"}): 0,     # URF
	frozenset({"yellow", "red", "blue"}): 1,      # UFL
	frozenset({"yellow", "blue", "orange"}): 2,   # ULB
	frozenset({"yellow", "orange", "green"}): 3,  # UBR
	frozenset({"white", "red", "green"}): 4,      # DFR
	frozenset({"white", "blue", "red"}): 5,       # DLF
	frozenset({"white", "orange", "blue"}): 6,    # DBL
	frozenset({"white", "green", "orange"}): 7,   # DRB
}


# For each edge position, the (x, y, z) coordinate and the ordered
# pair (primary_face, secondary_face). The primary face is U or D for
# top/bottom edges and F or B for the four middle-slice edges.
_EDGE_DATA: list[tuple[tuple[int, int, int], tuple[str, str]]] = [
	((1, 0, 2), ("u", "r")),  # 0 UR
	((0, 0, 1), ("u", "f")),  # 1 UF
	((1, 0, 0), ("u", "l")),  # 2 UL
	((2, 0, 1), ("u", "b")),  # 3 UB
	((1, 2, 2), ("d", "r")),  # 4 DR
	((0, 2, 1), ("d", "f")),  # 5 DF
	((1, 2, 0), ("d", "l")),  # 6 DL
	((2, 2, 1), ("d", "b")),  # 7 DB
	((0, 1, 2), ("f", "r")),  # 8 FR
	((0, 1, 0), ("f", "l")),  # 9 FL
	((2, 1, 0), ("b", "l")),  # 10 BL
	((2, 1, 2), ("b", "r")),  # 11 BR
]


_EDGE_COLORS_TO_INDEX: dict[frozenset, int] = {
	frozenset({"yellow", "green"}): 0,   # UR
	frozenset({"yellow", "red"}): 1,     # UF
	frozenset({"yellow", "blue"}): 2,    # UL
	frozenset({"yellow", "orange"}): 3,  # UB
	frozenset({"white", "green"}): 4,    # DR
	frozenset({"white", "red"}): 5,      # DF
	frozenset({"white", "blue"}): 6,     # DL
	frozenset({"white", "orange"}): 7,   # DB
	frozenset({"red", "green"}): 8,      # FR
	frozenset({"red", "blue"}): 9,       # FL
	frozenset({"orange", "blue"}): 10,   # BL
	frozenset({"orange", "green"}): 11,  # BR
}


def _corner_at(cube, pos_index: int) -> tuple[int, int]:
	(x, y, z), faces = _CORNER_DATA[pos_index]
	cubelet = cube.cube[x, y, z]
	colors = [cubelet.pos[f] for f in faces]
	cp = _CORNER_COLORS_TO_INDEX[frozenset(colors)]
	# Orientation = index of U/D-color sticker in the position's face ordering.
	for i, c in enumerate(colors):
		if c in _UD_COLORS:
			return cp, i
	raise ValueError(f"corner position {pos_index} has no U/D sticker")


def _edge_at(cube, pos_index: int) -> tuple[int, int]:
	(x, y, z), (primary_face, secondary_face) = _EDGE_DATA[pos_index]
	cubelet = cube.cube[x, y, z]
	primary = cubelet.pos[primary_face]
	secondary = cubelet.pos[secondary_face]
	ep = _EDGE_COLORS_TO_INDEX[frozenset([primary, secondary])]

	# Kociemba edge orientation rule: eo = 0 iff the edge's "home sticker"
	# is on a "good face" of its current position.
	#
	#   home sticker = U/D-color sticker for U/D-layer edges (ep 0..7);
	#                  F/B-color sticker for middle-slice edges (ep 8..11).
	#   good face    = U or D face for U/D-layer positions;
	#                  F or B face for middle-slice positions.
	#
	# This is the only sticker-local rule that is preserved by every
	# non-F/B quarter turn (which is exactly the Kociemba invariant).
	if ep < 8:
		home_colors = _UD_COLORS
	else:
		home_colors = _FB_COLORS
	home_face = primary_face if primary in home_colors else secondary_face
	if primary_face in ("u", "d"):
		good_faces = ("u", "d")
	else:
		good_faces = ("f", "b")
	eo = 0 if home_face in good_faces else 1
	return ep, eo


def from_cube(cube) -> CubieCube:
	"""Build a :class:`CubieCube` from a (3x3) :class:`Cube` object."""
	if cube.size != 3:
		raise ValueError(f"from_cube only supports 3x3 cubes; got size {cube.size}")
	cc = CubieCube()
	for i in range(8):
		cc.cp[i], cc.co[i] = _corner_at(cube, i)
	for i in range(12):
		cc.ep[i], cc.eo[i] = _edge_at(cube, i)
	return cc
