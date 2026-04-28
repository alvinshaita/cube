"""Normalize a cube state to a canonical whole-cube orientation.

Two states that represent the same physical cube oriented differently
will produce the same string after normalization, so cubes can be
compared by string equality regardless of how they're oriented.

The canonical orientation places the {yellow, red, blue} corner piece
at the UFL slot with yellow on U, red on F, blue on L. This anchors
the cube against all 24 whole-cube rotations.

Exports:

- ``normalize_state(state, size=None)`` — returns the state string of
  the cube rotated into canonical orientation. Raises ``ValueError`` if
  the state is incomplete or doesn't contain the anchor corner.

``Cube.normalize`` is a thin wrapper that returns a new ``Cube``.
"""
from collections import deque

from .validation import infer_size


UNKNOWN_CHAR = "?"

# The corner piece used as the orientation anchor and where it must end up.
_ANCHOR_FACE_COLORS = {"u": "yellow", "f": "red", "l": "blue"}

# Whole-cube rotation generators (operate in place on a Cube).
_GENERATORS = ("rotate_all_u", "rotate_all_r", "rotate_all_f")


def _anchor_at_ufl(cube):
	"""True iff the cubelet at array position (0, 0, 0) holds the anchor piece
	with the canonical sticker arrangement."""
	pos = cube.cube[0, 0, 0].pos
	return all(pos.get(face) == colour for face, colour in _ANCHOR_FACE_COLORS.items())


def normalize_state(state, size=None):
	"""Return the state string of ``state`` rotated to canonical orientation.

	The canonical orientation places the {yellow, red, blue} corner piece
	at the UFL slot with yellow on U, red on F, blue on L — uniquely
	determining the cube's orientation in space.

	Raises ``ValueError`` if the state is incomplete (contains '?'), has
	the wrong length, or doesn't contain a placeable {y, r, b} corner.
	"""
	state = state.lower()
	if size is None:
		size = infer_size(state)
	if len(state) != 6 * size * size:
		raise ValueError(
			f"state length {len(state)} does not match size {size}"
		)
	if UNKNOWN_CHAR in state:
		raise ValueError("cannot normalize a state with unknown stickers")

	from .cube import Cube
	start = Cube(size=size, state=state)

	if _anchor_at_ufl(start):
		return start.state

	# BFS through whole-cube rotations. The cube rotation group has order 24,
	# so the search visits at most 24 states.
	seen = {start.state}
	queue = deque([start])
	while queue:
		current = queue.popleft()
		for gen in _GENERATORS:
			candidate = current.copy()
			getattr(candidate, gen)(1)
			if candidate.state in seen:
				continue
			if _anchor_at_ufl(candidate):
				return candidate.state
			seen.add(candidate.state)
			queue.append(candidate)

	raise ValueError(
		"no rotation places the {yellow, red, blue} corner at UFL — "
		"state may not contain that corner piece"
	)
