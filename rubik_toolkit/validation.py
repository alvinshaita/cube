"""State-level validity check for Rubik's cubes.

Exports:

- ``is_state_valid(state, size=None)`` — pure function: does the given
  state string represent a cube that's reachable from solved by legal
  face moves? ``size`` is optional; when omitted, it's inferred from
  ``len(state)``.
- ``infer_size(state)`` — helper that returns the cube size implied by a
  state string's length, or raises ``ValueError`` if the length doesn't
  correspond to any square cube.

``Cube.is_valid`` is a thin wrapper around ``is_state_valid``.

Validity layers (tightest → loosest rejections first):

1. Format — complete (no '?'), correct length, only colour chars
2. Colour counts — each of y/b/r/g/o/w appears exactly size² times
3. Physical pieces — 8 real corner triples (3×3 also: 12 edges, 6 centres)
4. Centres in canonical positions (3×3 only — they can't move)
5. Chirality — each corner's stickers in face order must be a cyclic
   rotation of the piece's canonical tuple (no mirror reflections)
6. Solvability parity:
   - 3×3: corner twist sum ≡ 0 (mod 3); edge flip sum ≡ 0 (mod 2);
     sgn(corner perm) = sgn(edge perm)
   - 2×2: corner twist sum ≡ 0 (mod 3) (no perm-parity constraint
     because every face move is a 4-cycle)
"""
import math

from .solver.kociemba.from_cube import from_cube as _to_cubie


UNKNOWN_CHAR = "?"
_COLOR_CHARS = frozenset("ybrgow")

# Opposite-face colour pairs on a standard cube.
_OPPOSITE_COLORS = {
	"yellow": "white", "white": "yellow",
	"blue": "green",   "green": "blue",
	"red": "orange",   "orange": "red",
}
_COLOR_NAMES = ("yellow", "blue", "red", "green", "orange", "white")

# 8 real corner pieces: one colour from each opposite pair.
_VALID_CORNERS = frozenset(
	frozenset((a, b, c))
	for a in ("yellow", "white")
	for b in ("blue", "green")
	for c in ("red", "orange")
)

# 12 real edge pieces: every pair of non-opposite colours.
_VALID_EDGES = frozenset(
	frozenset((a, b))
	for i, a in enumerate(_COLOR_NAMES)
	for b in _COLOR_NAMES[i + 1:]
	if _OPPOSITE_COLORS[a] != b
)

# Canonical centre positions on a 3×3 — (cube-array i, j, k, face) → colour.
# Centres can't move under legal play, so any deviation is unreachable.
_STANDARD_CENTERS_3X3 = {
	(1, 0, 1, "u"): "yellow",
	(1, 2, 1, "d"): "white",
	(1, 1, 0, "l"): "blue",
	(1, 1, 2, "r"): "green",
	(0, 1, 1, "f"): "red",
	(2, 1, 1, "b"): "orange",
}

# Corner positions (cube-array index, face ordering) on 2×2 / 3×3.
# Face ordering is clockwise-from-outside-the-corner, consistent with the
# kociemba solver's convention. Orientation index = position of the
# U/D-colour sticker in that ordering.
_CORNER_DATA_2X2 = (
	((0, 0, 1), ("u", "r", "f")),  # URF
	((0, 0, 0), ("u", "f", "l")),  # UFL
	((1, 0, 0), ("u", "l", "b")),  # ULB
	((1, 0, 1), ("u", "b", "r")),  # UBR
	((0, 1, 1), ("d", "f", "r")),  # DFR
	((0, 1, 0), ("d", "l", "f")),  # DLF
	((1, 1, 0), ("d", "b", "l")),  # DBL
	((1, 1, 1), ("d", "r", "b")),  # DRB
)
_CORNER_DATA_3X3 = (
	((0, 0, 2), ("u", "r", "f")),
	((0, 0, 0), ("u", "f", "l")),
	((2, 0, 0), ("u", "l", "b")),
	((2, 0, 2), ("u", "b", "r")),
	((0, 2, 2), ("d", "f", "r")),
	((0, 2, 0), ("d", "l", "f")),
	((2, 2, 0), ("d", "b", "l")),
	((2, 2, 2), ("d", "r", "b")),
)
_UD_COLORS = frozenset({"yellow", "white"})

# Canonical chirality tuples: the colour ordering a piece shows at its home
# position when solved, in the position's face order. Any other appearance
# must be a *cyclic rotation* of this tuple — a reversed order is a
# mirror-reflected corner, impossible without disassembling the cube.
_CORNER_CANONICAL = {
	frozenset({"yellow", "green", "red"}):    ("yellow", "green", "red"),    # URF
	frozenset({"yellow", "red", "blue"}):     ("yellow", "red", "blue"),     # UFL
	frozenset({"yellow", "blue", "orange"}):  ("yellow", "blue", "orange"),  # ULB
	frozenset({"yellow", "orange", "green"}): ("yellow", "orange", "green"), # UBR
	frozenset({"white", "red", "green"}):     ("white", "red", "green"),     # DFR
	frozenset({"white", "blue", "red"}):      ("white", "blue", "red"),      # DLF
	frozenset({"white", "orange", "blue"}):   ("white", "orange", "blue"),   # DBL
	frozenset({"white", "green", "orange"}):  ("white", "green", "orange"),  # DRB
}

# Precompute valid cyclic rotations per piece for O(1) membership check.
_CORNER_VALID_ORIENTATIONS = {
	color_set: frozenset(canonical[i:] + canonical[:i] for i in range(3))
	for color_set, canonical in _CORNER_CANONICAL.items()
}


def infer_size(state):
	"""Return the cube size implied by a state string's length.

	A size-N cube has 6·N² stickers. Raises ``ValueError`` if the length
	doesn't satisfy that relation (e.g. 23, 25, empty string).
	"""
	n = len(state)
	if n == 0 or n % 6 != 0:
		raise ValueError(f"state length {n} is not a multiple of 6")
	stickers_per_face = n // 6
	size = math.isqrt(stickers_per_face)
	if size * size != stickers_per_face:
		raise ValueError(
			f"state length {n} implies {stickers_per_face} stickers/face, "
			f"which is not a square number"
		)
	return size


def _permutation_parity(perm):
	"""0 (even) or 1 (odd) for a permutation. Parity = (n - cycles) % 2."""
	n = len(perm)
	visited = [False] * n
	cycles = 0
	for i in range(n):
		if visited[i]:
			continue
		cycles += 1
		j = i
		while not visited[j]:
			visited[j] = True
			j = perm[j]
	return (n - cycles) % 2


def _corner_twist_sum_2x2(cube):
	"""Sum (mod 3) of corner orientation indices on a 2×2 cube."""
	total = 0
	for (i, j, k), faces in _CORNER_DATA_2X2:
		cubelet = cube.cube[i, j, k]
		for idx, face in enumerate(faces):
			if cubelet.pos[face] in _UD_COLORS:
				total += idx
				break
	return total % 3


def _has_valid_chirality(cube, corner_data):
	"""True iff every corner's colours in face order are a cyclic rotation
	of the piece's canonical tuple. Assumes physical validity already ran."""
	for (i, j, k), faces in corner_data:
		cubelet = cube.cube[i, j, k]
		colors = tuple(cubelet.pos[f] for f in faces)
		if colors not in _CORNER_VALID_ORIENTATIONS[frozenset(colors)]:
			return False
	return True


def is_state_valid(state, size=None):
	"""True iff ``state`` is reachable from solved by legal face moves.

	``size`` is inferred from ``len(state)`` when omitted. Returns ``False``
	for incomplete (``?``), malformed, or unsolvable states. Raises
	``NotImplementedError`` for sizes other than 2 or 3.
	"""
	state = state.lower()

	if size is None:
		try:
			size = infer_size(state)
		except ValueError:
			return False

	if size not in (2, 3):
		raise NotImplementedError(
			f"is_state_valid only supports 2x2 and 3x3 cubes (got {size}x{size})"
		)

	# Format
	if len(state) != 6 * size * size:
		return False
	if UNKNOWN_CHAR in state:
		return False  # incomplete
	if not set(state) <= _COLOR_CHARS:
		return False

	# Colour counts
	target = size * size
	for c in "ybrgow":
		if state.count(c) != target:
			return False

	# Build an internal Cube to reuse the cubelet-array representation.
	# Lazy import avoids a cube.py ↔ validation.py cycle at module load.
	from .cube import Cube
	cube = Cube(size=size, state=state)

	# Physical pieces
	corners, edges, centers = [], [], []
	for i in range(size):
		for j in range(size):
			for k in range(size):
				exposed = [v for v in cube.cube[i][j][k].pos.values() if v is not None]
				if len(exposed) == 3:
					corners.append(frozenset(exposed))
				elif len(exposed) == 2:
					edges.append(frozenset(exposed))
				elif len(exposed) == 1:
					centers.append(exposed[0])

	if len(corners) != 8:
		return False
	for corner in corners:
		if len(corner) != 3 or corner not in _VALID_CORNERS:
			return False
	if len(set(corners)) != 8:
		return False

	corner_data = _CORNER_DATA_3X3 if size == 3 else _CORNER_DATA_2X2

	if size == 3:
		if len(edges) != 12:
			return False
		for edge in edges:
			if len(edge) != 2 or edge not in _VALID_EDGES:
				return False
		if len(set(edges)) != 12:
			return False
		if len(centers) != 6 or len(set(centers)) != 6:
			return False
		for (i, j, k, face), expected in _STANDARD_CENTERS_3X3.items():
			if cube.cube[i, j, k].pos[face] != expected:
				return False

	# Chirality (both sizes)
	if not _has_valid_chirality(cube, corner_data):
		return False

	# Solvability parity
	if size == 3:
		cc = _to_cubie(cube)
		if sum(cc.co) % 3 != 0:
			return False
		if sum(cc.eo) % 2 != 0:
			return False
		if _permutation_parity(cc.cp) != _permutation_parity(cc.ep):
			return False
	else:  # size == 2
		if _corner_twist_sum_2x2(cube) != 0:
			return False

	return True
