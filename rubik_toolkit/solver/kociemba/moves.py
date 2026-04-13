"""Coordinate-level move tables for Kociemba's two-phase solver.

Each move table is a 2D list ``table[coord][move_index] = new_coord`` that
gives the result of applying a named HTM move to a cube in the given
coordinate class. Tables are generated once (lazily) per Python process.

The tables are built by the straightforward method:
	for every value of the coordinate,
	    instantiate a CubieCube with that coord and everything else at
	    identity, apply the move, and read the new coord.

Correctness relies on each coordinate depending only on the part of the
cube state that is preserved across this instantiation (e.g. ``twist``
only looks at corner orientations, which evolve under moves without
reference to the corner permutation).
"""
from __future__ import annotations

from .cubie import CubieCube, MOVES
from . import coord as cd


# All 18 half-turn-metric moves in a fixed canonical order.
HTM_MOVES = [
	"U", "U2", "U'",
	"R", "R2", "R'",
	"F", "F2", "F'",
	"D", "D2", "D'",
	"L", "L2", "L'",
	"B", "B2", "B'",
]
HTM_COUNT = len(HTM_MOVES)  # 18

# Phase 2 moves (G1 generators): the 10 moves that preserve the
# phase-1 invariants (twist=0, flip=0, slice=0).
PHASE2_MOVES = [
	"U", "U2", "U'",
	"D", "D2", "D'",
	"R2", "L2", "F2", "B2",
]
PHASE2_COUNT = len(PHASE2_MOVES)  # 10

# Index mapping so we can convert a phase 2 move index (0..9) to its
# HTM move index (0..17).
PHASE2_TO_HTM = [HTM_MOVES.index(m) for m in PHASE2_MOVES]

# Group moves by face — used for "don't repeat the same face back-to-back"
# pruning during search.
MOVE_FACE = {m: m[0] for m in HTM_MOVES}
# Axis groupings so we also prune e.g. "U then D" in favour of a canonical
# order. (U and D share an axis; R and L; F and B.)
MOVE_AXIS = {
	"U": 0, "D": 0,
	"R": 1, "L": 1,
	"F": 2, "B": 2,
}


def _gen_single_move_table(coord_count, get_fn, set_fn, moves):
	"""Build a move table for a single coordinate class."""
	table = [[0] * len(moves) for _ in range(coord_count)]
	for c in range(coord_count):
		base = CubieCube()
		set_fn(base, c)
		for mi, mname in enumerate(moves):
			d = base.copy()
			d.apply(mname)
			table[c][mi] = get_fn(d)
	return table


# --- Lazy singleton tables ---
# Generation is deferred to first access because building them all up
# front costs several seconds and not every solve needs every table.

_twist_move = None
_flip_move = None
_slice_move = None
_cp_move = None
_ep_ud_move = None
_sp_move = None


def twist_move():
	global _twist_move
	if _twist_move is None:
		_twist_move = _gen_single_move_table(
			cd.TWIST_COUNT, cd.get_twist, cd.set_twist, HTM_MOVES
		)
	return _twist_move


def flip_move():
	global _flip_move
	if _flip_move is None:
		_flip_move = _gen_single_move_table(
			cd.FLIP_COUNT, cd.get_flip, cd.set_flip, HTM_MOVES
		)
	return _flip_move


def slice_move():
	global _slice_move
	if _slice_move is None:
		_slice_move = _gen_single_move_table(
			cd.SLICE_COUNT, cd.get_slice, cd.set_slice, HTM_MOVES
		)
	return _slice_move


def cp_move():
	global _cp_move
	if _cp_move is None:
		_cp_move = _gen_single_move_table(
			cd.CP_COUNT, cd.get_cp, cd.set_cp, PHASE2_MOVES
		)
	return _cp_move


def ep_ud_move():
	global _ep_ud_move
	if _ep_ud_move is None:
		_ep_ud_move = _gen_single_move_table(
			cd.EP_UD_COUNT, cd.get_ep_ud, cd.set_ep_ud, PHASE2_MOVES
		)
	return _ep_ud_move


def sp_move():
	global _sp_move
	if _sp_move is None:
		_sp_move = _gen_single_move_table(
			cd.SP_COUNT, cd.get_sp, cd.set_sp, PHASE2_MOVES
		)
	return _sp_move
