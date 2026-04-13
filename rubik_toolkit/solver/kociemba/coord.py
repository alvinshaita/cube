"""Coordinate encoding for Kociemba's two-phase algorithm.

Six integer coordinates fully describe a cube state for the purposes
of the two-phase search:

	Phase 1 (reduce to G1 = <U, D, L2, R2, F2, B2>):
		twist: corner orientation, [0, 2187)
		flip:  edge orientation,   [0, 2048)
		slice: positions of the 4 UD-slice edges (FR, FL, BL, BR)
		       in the 12 edge slots, ignoring their order.
		       C(12, 4) = 495 possibilities.

	Phase 2 (solve within G1):
		cp:      corner permutation,        [0, 40320)
		ep_ud:   U/D-layer edge permutation, [0, 40320)
		sp:      UD-slice edge permutation,  [0, 24)

The phase 1 goal is (twist, flip, slice) == (0, 0, 0).
The phase 2 goal is (cp, ep_ud, sp) == (0, 0, 0) (i.e. fully solved).
"""
from __future__ import annotations

from itertools import combinations
from math import factorial

from .cubie import (
	CORNER_COUNT,
	EDGE_COUNT,
	CubieCube,
	FR,
	BR,
)

TWIST_COUNT = 2187     # 3^7
FLIP_COUNT = 2048      # 2^11
SLICE_COUNT = 495      # C(12, 4)
CP_COUNT = 40320       # 8!
EP_UD_COUNT = 40320    # 8!
SP_COUNT = 24          # 4!


# --- Corner orientation (twist) ---

def get_twist(cc: CubieCube) -> int:
	s = 0
	for i in range(CORNER_COUNT - 1):
		s = 3 * s + cc.co[i]
	return s


def set_twist(cc: CubieCube, twist: int) -> None:
	total = 0
	for i in range(CORNER_COUNT - 2, -1, -1):
		v = twist % 3
		cc.co[i] = v
		total += v
		twist //= 3
	cc.co[CORNER_COUNT - 1] = (-total) % 3


# --- Edge orientation (flip) ---

def get_flip(cc: CubieCube) -> int:
	s = 0
	for i in range(EDGE_COUNT - 1):
		s = 2 * s + cc.eo[i]
	return s


def set_flip(cc: CubieCube, flip: int) -> None:
	total = 0
	for i in range(EDGE_COUNT - 2, -1, -1):
		v = flip % 2
		cc.eo[i] = v
		total += v
		flip //= 2
	cc.eo[EDGE_COUNT - 1] = (-total) % 2


# --- UD slice position (unordered) ---
# 4 UD-slice edges occupy some 4-element subset of the 12 edge slots.
# We rank these subsets in colex order using a lookup table.

_SLICE_TO_POS: list[tuple[int, ...]] = []
_POS_TO_SLICE: dict[tuple[int, ...], int] = {}
# Enumerated in reverse so (8, 9, 10, 11) — the solved-cube slice-edge
# positions — gets index 0, matching the phase 1 goal convention.
for _idx, _combo in enumerate(
	reversed(list(combinations(range(EDGE_COUNT), 4)))
):
	_SLICE_TO_POS.append(_combo)
	_POS_TO_SLICE[_combo] = _idx


def get_slice(cc: CubieCube) -> int:
	positions = tuple(
		sorted(j for j in range(EDGE_COUNT) if FR <= cc.ep[j] <= BR)
	)
	return _POS_TO_SLICE[positions]


def set_slice(cc: CubieCube, slice_coord: int) -> None:
	"""Set the cube to have the 4 UD-slice edges at the positions encoded
	by ``slice_coord``. Used only for move-table seeding; the specific
	assignment to each slot is canonical (FR, FL, BL, BR in order)."""
	positions = _SLICE_TO_POS[slice_coord]
	# Wipe edges to a distinguishable marker, then fill.
	# We use the invariant: non-slice edges get placed in the non-slice
	# slots in their natural order; slice edges in slice slots in order.
	non_slice_slots = [j for j in range(EDGE_COUNT) if j not in positions]
	# Canonical filler (non-slice edges 0..7 fill non-slice slots in order).
	non_slice_edges = [e for e in range(EDGE_COUNT) if not (FR <= e <= BR)]
	slice_edges = [FR, FR + 1, FR + 2, FR + 3]  # FR, FL, BL, BR
	for slot, edge in zip(non_slice_slots, non_slice_edges):
		cc.ep[slot] = edge
	for slot, edge in zip(positions, slice_edges):
		cc.ep[slot] = edge


# --- Permutation ranking ---

def _perm_rank(perm: list[int], n: int) -> int:
	"""Factorial-base Lehmer-code rank of a permutation of [0..n-1]."""
	rank = 0
	for i in range(n - 1):
		r = 0
		for j in range(i + 1, n):
			if perm[j] < perm[i]:
				r += 1
		rank += r * factorial(n - 1 - i)
	return rank


def _perm_unrank(rank: int, n: int) -> list[int]:
	"""Return the permutation whose Lehmer rank equals ``rank``.

	Inverse of ``_perm_rank``. The Lehmer code digit at position ``i`` is
	``#{j > i : perm[j] < perm[i]}``; when reconstructing left-to-right
	with the still-unused values in sorted ascending order, the digit
	equals the index into that unused list.
	"""
	unused = list(range(n))
	perm = [0] * n
	for i in range(n - 1):
		f = factorial(n - 1 - i)
		d = rank // f
		rank %= f
		perm[i] = unused.pop(d)
	perm[n - 1] = unused[0]
	return perm


def get_cp(cc: CubieCube) -> int:
	return _perm_rank(cc.cp, CORNER_COUNT)


def set_cp(cc: CubieCube, cp: int) -> None:
	cc.cp = _perm_unrank(cp, CORNER_COUNT)


def get_ep_ud(cc: CubieCube) -> int:
	"""Permutation rank of the 8 U/D-layer edges (only valid in G1)."""
	return _perm_rank(cc.ep[:8], 8)


def set_ep_ud(cc: CubieCube, ep_ud: int) -> None:
	cc.ep[:8] = _perm_unrank(ep_ud, 8)


def get_sp(cc: CubieCube) -> int:
	"""Permutation rank of the 4 UD-slice edges (only valid in G1)."""
	return _perm_rank([e - FR for e in cc.ep[8:12]], 4)


def set_sp(cc: CubieCube, sp: int) -> None:
	cc.ep[8:12] = [e + FR for e in _perm_unrank(sp, 4)]


# --- Phase predicates ---

def is_in_g1(cc: CubieCube) -> bool:
	"""True if the cube is in the phase 1 target subgroup."""
	return get_twist(cc) == 0 and get_flip(cc) == 0 and get_slice(cc) == 0


def is_solved(cc: CubieCube) -> bool:
	return cc.is_solved()
