"""Generate possible valid states from a state with unknown stickers.

Exports:

- ``possible_states(state, size=None, limit=None)`` — generator yielding
  every valid state matching the partial input. Filters each candidate
  through ``is_state_valid``.
- ``count_possible_states(state, size=None)`` — count of valid states
  matching the partial input. Implemented independently from
  ``possible_states``: enumerates piece placements (corner / edge
  permutation × orientation) consistent with the known stickers, then
  combines counts by parity. Significantly faster than iterating
  ``possible_states`` for inputs with many partially-known cubelets.

The two functions are internally decoupled but produce consistent
answers — ``count_possible_states(s)`` always equals
``sum(1 for _ in possible_states(s))``.

``Cube.possible_states`` and ``Cube.count_possible_states`` are thin
wrappers around these functions.
"""
import math
from collections import Counter

from .validation import (
	infer_size,
	is_state_valid,
	_CORNER_CANONICAL,
	_CORNER_DATA_2X2,
	_CORNER_DATA_3X3,
	_STANDARD_CENTERS_3X3,
	_UD_COLORS,
	_permutation_parity,
)


UNKNOWN_CHAR = "?"
_COLOR_CHARS = "ybrgow"

# 12 edge slots on a 3×3: cubelet array index, ordered face pair. The
# face ordering matches the convention used in the kociemba converter
# (primary face = U/D for the 8 U/D-layer slots, F/B for the 4 middle).
_EDGE_DATA_3X3 = (
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
)

# Canonical sticker order at each edge piece's home position.
_EDGE_CANONICAL = {
	frozenset({"yellow", "green"}):  ("yellow", "green"),
	frozenset({"yellow", "red"}):    ("yellow", "red"),
	frozenset({"yellow", "blue"}):   ("yellow", "blue"),
	frozenset({"yellow", "orange"}): ("yellow", "orange"),
	frozenset({"white", "green"}):   ("white", "green"),
	frozenset({"white", "red"}):     ("white", "red"),
	frozenset({"white", "blue"}):    ("white", "blue"),
	frozenset({"white", "orange"}):  ("white", "orange"),
	frozenset({"red", "green"}):     ("red", "green"),
	frozenset({"red", "blue"}):      ("red", "blue"),
	frozenset({"orange", "blue"}):   ("orange", "blue"),
	frozenset({"orange", "green"}):  ("orange", "green"),
}

_FB_COLORS = frozenset({"red", "orange"})

# Indexed piece lists — used as the integer "piece id" in the (cp, co)
# and (ep, eo) representations during counting.
_CORNER_PIECE_CANONICAL = list(_CORNER_CANONICAL.values())  # 8 items
_EDGE_PIECE_CANONICAL = list(_EDGE_CANONICAL.values())      # 12 items

# Closed-form fully-unconstrained counts.
#
# 3×3 corners: 8! × 3^7 (cp, co) tuples satisfy sum(co) ≡ 0 (mod 3).
# Both perm parities occur equally → divide by 2 for the per-parity count.
# 3×3 edges: 12! × 2^11 (ep, eo) tuples satisfy sum(eo) ≡ 0 (mod 2).
# Both perm parities occur equally → divide by 2 for the per-parity count.
# 2×2: no perm-parity constraint, so we use the unsplit count.
_FREE_CORNER_3X3_PER_PARITY = math.factorial(8) * 3**7 // 2   # 44_089_920
_FREE_EDGE_3X3_PER_PARITY = math.factorial(12) * 2**11 // 2   # 490_497_638_400
_FREE_CORNER_2X2_TOTAL = math.factorial(8) * 3**7              # 88_179_840


# ---------------------------------------------------------------------------
# possible_states (generator) — filters candidates through is_state_valid
# ---------------------------------------------------------------------------

def possible_states(state, size=None, limit=None):
	"""Yield every valid state matching the partial ``state``.

	A "valid state" is one that passes :func:`is_state_valid`. Each '?'
	in ``state`` is filled with a colour; known stickers are preserved.

	``size`` is inferred from ``len(state)`` when omitted. ``limit`` caps
	the number of valid states yielded (not the number of candidates
	considered). For sparse inputs, the search may iterate many internal
	candidates before yielding each one.
	"""
	state = state.lower()
	if size is None:
		size = infer_size(state)
	if len(state) != 6 * size * size:
		raise ValueError(
			f"state length {len(state)} does not match size {size}"
		)

	if limit is not None and limit <= 0:
		return

	if UNKNOWN_CHAR not in state:
		if is_state_valid(state, size):
			yield state
		return

	target = size * size
	deficits = {c: target - state.count(c) for c in _COLOR_CHARS}
	if any(d < 0 for d in deficits.values()):
		return

	unknown_positions = [i for i, ch in enumerate(state) if ch == UNKNOWN_CHAR]
	if sum(deficits.values()) != len(unknown_positions):
		return

	state_chars = list(state)
	remaining = Counter({c: d for c, d in deficits.items() if d > 0})
	sorted_colors = sorted(remaining.keys())
	yielded = 0

	def recurse(pos_idx):
		nonlocal yielded
		if pos_idx == len(unknown_positions):
			candidate = "".join(state_chars)
			if is_state_valid(candidate, size):
				yield candidate
				yielded += 1
			return
		pos = unknown_positions[pos_idx]
		for c in sorted_colors:
			if remaining[c] <= 0:
				continue
			remaining[c] -= 1
			state_chars[pos] = c
			yield from recurse(pos_idx + 1)
			remaining[c] += 1
			if limit is not None and yielded >= limit:
				return
		state_chars[pos] = UNKNOWN_CHAR

	for completion in recurse(0):
		yield completion
		if limit is not None and yielded >= limit:
			return


# ---------------------------------------------------------------------------
# count_possible_states — independent piece-level enumeration
# ---------------------------------------------------------------------------

def _normalize_known(value):
	"""Cubelet `pos` stores 'unknown' for '?' stickers; map to None for clarity."""
	return None if value == "unknown" else value


def _build_corner_compat(cube, corner_data):
	"""Per-slot list of ``(piece_index, co)`` pairs compatible with known stickers.

	``co`` is the kociemba corner orientation: index of the U/D-colour
	sticker in the slot's face ordering. Only the 3 cyclic rotations of
	the canonical tuple are emitted, so chirality is enforced by construction.
	"""
	result = []
	for (i, j, k), faces in corner_data:
		cubelet_pos = cube.cube[i, j, k].pos
		known = [_normalize_known(cubelet_pos[f]) for f in faces]
		compat = []
		for piece_idx, canonical in enumerate(_CORNER_PIECE_CANONICAL):
			for k_rot in range(3):
				arrangement = canonical[k_rot:] + canonical[:k_rot]
				if not all(known[ix] is None or known[ix] == arrangement[ix]
				           for ix in range(3)):
					continue
				# co = position of U/D-colour sticker in this arrangement.
				co = next(ix for ix, c in enumerate(arrangement) if c in _UD_COLORS)
				compat.append((piece_idx, co))
		result.append(compat)
	return result


def _build_edge_compat(cube):
	"""Per-slot list of ``(piece_index, eo)`` pairs compatible with known stickers.

	``eo`` is the kociemba edge orientation: 0 iff the home-colour sticker
	(U/D for U/D-layer pieces, F/B for middle-slice pieces) sits on a
	"good face" (U/D for U/D-layer slots, F/B for middle-slice slots).
	Both arrangements per piece (canonical and swapped) are considered.
	"""
	result = []
	for slot_idx, ((i, j, k), (face_a, face_b)) in enumerate(_EDGE_DATA_3X3):
		cubelet_pos = cube.cube[i, j, k].pos
		known_a = _normalize_known(cubelet_pos[face_a])
		known_b = _normalize_known(cubelet_pos[face_b])
		good_faces = ("u", "d") if face_a in ("u", "d") else ("f", "b")
		compat = []
		for piece_idx, canonical in enumerate(_EDGE_PIECE_CANONICAL):
			# piece_idx 0..7 are U/D-layer pieces, 8..11 are middle-slice.
			home_colors = _UD_COLORS if piece_idx < 8 else _FB_COLORS
			for arrangement in (canonical, (canonical[1], canonical[0])):
				sa, sb = arrangement
				if known_a is not None and known_a != sa:
					continue
				if known_b is not None and known_b != sb:
					continue
				home_face = face_a if sa in home_colors else face_b
				eo = 0 if home_face in good_faces else 1
				compat.append((piece_idx, eo))
		result.append(compat)
	return result


def _count_corners_2x2(corner_compat):
	"""Count valid (cp, co) tuples for a 2×2 (no perm-parity constraint)."""
	n = 8
	used = [False] * n
	total = [0]

	def backtrack(pos, co_sum):
		if pos == n:
			if co_sum % 3 == 0:
				total[0] += 1
			return
		for piece_idx, co in corner_compat[pos]:
			if used[piece_idx]:
				continue
			used[piece_idx] = True
			backtrack(pos + 1, co_sum + co)
			used[piece_idx] = False

	backtrack(0, 0)
	return total[0]


def _count_corners_3x3_by_parity(corner_compat):
	"""Count valid (cp, co) tuples for a 3×3, returned as (even, odd) by perm parity."""
	n = 8
	cp = [0] * n
	used = [False] * n
	by_parity = [0, 0]

	def backtrack(pos, co_sum):
		if pos == n:
			if co_sum % 3 != 0:
				return
			by_parity[_permutation_parity(cp)] += 1
			return
		for piece_idx, co in corner_compat[pos]:
			if used[piece_idx]:
				continue
			used[piece_idx] = True
			cp[pos] = piece_idx
			backtrack(pos + 1, co_sum + co)
			used[piece_idx] = False

	backtrack(0, 0)
	return by_parity[0], by_parity[1]


def _count_edges_3x3_by_parity(edge_compat):
	"""Count valid (ep, eo) tuples returned as (even, odd) by perm parity."""
	n = 12
	ep = [0] * n
	used = [False] * n
	by_parity = [0, 0]

	def backtrack(pos, eo_sum):
		if pos == n:
			if eo_sum % 2 != 0:
				return
			by_parity[_permutation_parity(ep)] += 1
			return
		for piece_idx, eo in edge_compat[pos]:
			if used[piece_idx]:
				continue
			used[piece_idx] = True
			ep[pos] = piece_idx
			backtrack(pos + 1, eo_sum + eo)
			used[piece_idx] = False

	backtrack(0, 0)
	return by_parity[0], by_parity[1]


def _all_unconstrained(cube, slots_data):
	"""True iff every sticker at every (slot, face) listed is unknown."""
	for entry in slots_data:
		(i, j, k), faces = entry
		pos = cube.cube[i, j, k].pos
		for face in faces:
			if pos[face] != "unknown":
				return False
	return True


def count_possible_states(state, size=None):
	"""Count valid states matching the partial ``state``.

	Independent of :func:`possible_states`. Enumerates piece placements
	(per-slot ``(piece, orientation)`` options consistent with known
	stickers), then combines corner and edge counts by perm parity:
	``corner_even × edge_even + corner_odd × edge_odd`` for 3×3, and a
	plain twist-sum count for 2×2 (no perm-parity constraint).

	When all corner (or edge) slots are fully unknown, the corresponding
	count uses a closed-form constant rather than backtracking, so the
	all-unknown 3×3 / 2×2 cases evaluate immediately.
	"""
	state = state.lower()
	if size is None:
		size = infer_size(state)
	if len(state) != 6 * size * size:
		raise ValueError(
			f"state length {len(state)} does not match size {size}"
		)
	if size not in (2, 3):
		raise NotImplementedError(
			f"count_possible_states only supports 2x2 and 3x3 cubes "
			f"(got {size}x{size})"
		)
	if not (set(state) - {UNKNOWN_CHAR}) <= set(_COLOR_CHARS):
		return 0

	# Quick reject: any colour over the per-face quota is unfixable.
	target = size * size
	for c in _COLOR_CHARS:
		if state.count(c) > target:
			return 0

	# Build the cubelet array so we can reason about per-slot known stickers.
	from .cube import Cube
	cube = Cube(size=size, state=state)

	# 3×3 centres are fixed by the state convention; any non-canonical
	# centre is unreachable.
	if size == 3:
		for (i, j, k, face), expected in _STANDARD_CENTERS_3X3.items():
			actual = _normalize_known(cube.cube[i, j, k].pos[face])
			if actual is not None and actual != expected:
				return 0

	corner_data = _CORNER_DATA_3X3 if size == 3 else _CORNER_DATA_2X2

	if size == 2:
		if _all_unconstrained(cube, corner_data):
			return _FREE_CORNER_2X2_TOTAL
		corner_compat = _build_corner_compat(cube, corner_data)
		if any(not c for c in corner_compat):
			return 0
		return _count_corners_2x2(corner_compat)

	# 3×3
	if _all_unconstrained(cube, corner_data):
		c_even = c_odd = _FREE_CORNER_3X3_PER_PARITY
	else:
		corner_compat = _build_corner_compat(cube, corner_data)
		if any(not c for c in corner_compat):
			return 0
		c_even, c_odd = _count_corners_3x3_by_parity(corner_compat)

	if _all_unconstrained(cube, _EDGE_DATA_3X3):
		e_even = e_odd = _FREE_EDGE_3X3_PER_PARITY
	else:
		edge_compat = _build_edge_compat(cube)
		if any(not c for c in edge_compat):
			return 0
		e_even, e_odd = _count_edges_3x3_by_parity(edge_compat)

	return c_even * e_even + c_odd * e_odd
