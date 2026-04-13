"""Cubie-level 3x3 cube representation for Kociemba's two-phase solver.

The cube is represented as 4 arrays:
	- cp[8]:  corner permutation. cp[i] is the corner currently at position i.
	- co[8]:  corner orientation. co[i] in {0, 1, 2}.
	- ep[12]: edge permutation. ep[i] is the edge currently at position i.
	- eo[12]: edge orientation. eo[i] in {0, 1}.

Position indices:
	Corners: URF=0, UFL=1, ULB=2, UBR=3, DFR=4, DLF=5, DBL=6, DRB=7
	Edges:   UR=0, UF=1, UL=2, UB=3, DR=4, DF=5, DL=6, DB=7,
	         FR=8, FL=9, BL=10, BR=11

Moves use the "source" convention: after applying move M,
	new.cp[i] = old.cp[M.cp[i]]
	new.co[i] = (old.co[M.cp[i]] + M.co[i]) % 3
so M.cp[i] names the position that feeds position i under the move, and
M.co[i] is the orientation delta applied at destination position i.
"""
from __future__ import annotations

# Corner positions
URF, UFL, ULB, UBR, DFR, DLF, DBL, DRB = range(8)

# Edge positions
UR, UF, UL, UB, DR, DF, DL, DB, FR, FL, BL, BR = range(12)

CORNER_COUNT = 8
EDGE_COUNT = 12

# HTM move names: 6 face moves, each with 3 variants (quarter, double, inverse).
FACE_MOVES = ["U", "R", "F", "D", "L", "B"]
ALL_MOVES = [f + suffix for f in FACE_MOVES for suffix in ("", "2", "'")]


class CubieCube:
	"""Cubie-level cube state with move composition."""

	__slots__ = ("cp", "co", "ep", "eo")

	def __init__(self, cp=None, co=None, ep=None, eo=None):
		self.cp = list(cp) if cp is not None else list(range(CORNER_COUNT))
		self.co = list(co) if co is not None else [0] * CORNER_COUNT
		self.ep = list(ep) if ep is not None else list(range(EDGE_COUNT))
		self.eo = list(eo) if eo is not None else [0] * EDGE_COUNT

	def copy(self):
		return CubieCube(self.cp, self.co, self.ep, self.eo)

	def is_solved(self):
		return (
			self.cp == list(range(CORNER_COUNT))
			and self.co == [0] * CORNER_COUNT
			and self.ep == list(range(EDGE_COUNT))
			and self.eo == [0] * EDGE_COUNT
		)

	def __eq__(self, other):
		if not isinstance(other, CubieCube):
			return NotImplemented
		return (
			self.cp == other.cp
			and self.co == other.co
			and self.ep == other.ep
			and self.eo == other.eo
		)

	def multiply(self, move):
		"""Apply ``move`` (a CubieCube generator) to self in place."""
		new_cp = [self.cp[move.cp[i]] for i in range(CORNER_COUNT)]
		new_co = [
			(self.co[move.cp[i]] + move.co[i]) % 3
			for i in range(CORNER_COUNT)
		]
		new_ep = [self.ep[move.ep[i]] for i in range(EDGE_COUNT)]
		new_eo = [
			(self.eo[move.ep[i]] + move.eo[i]) % 2
			for i in range(EDGE_COUNT)
		]
		self.cp = new_cp
		self.co = new_co
		self.ep = new_ep
		self.eo = new_eo

	def apply(self, move_name):
		"""Apply a named move (e.g. ``"U"``, ``"R2"``, ``"F'"``) in place."""
		move = MOVES[move_name]
		self.multiply(move)

	def apply_sequence(self, sequence):
		"""Apply a whitespace-separated move sequence in place."""
		for name in sequence.split():
			if name:
				self.apply(name)


def _make_move(cp, co, ep, eo):
	return CubieCube(cp=cp, co=co, ep=ep, eo=eo)


# Quarter-turn move generators in source convention.
#
# U: corner cycle URF->UBR->ULB->UFL->URF; edge cycle UR->UB->UL->UF->UR.
#    No orientation change (U/D turns preserve both co and eo).
_MOVE_U = _make_move(
	cp=[UFL, ULB, UBR, URF, DFR, DLF, DBL, DRB],
	co=[0, 0, 0, 0, 0, 0, 0, 0],
	ep=[UF, UL, UB, UR, DR, DF, DL, DB, FR, FL, BL, BR],
	eo=[0] * 12,
)

# R: corner cycle URF->UBR->DRB->DFR->URF; edge cycle UR->BR->DR->FR->UR.
#    Twists the 4 R-face corners. eo preserved (standard Kociemba convention).
_MOVE_R = _make_move(
	cp=[DFR, UFL, ULB, URF, DRB, DLF, DBL, UBR],
	co=[2, 0, 0, 1, 1, 0, 0, 2],
	ep=[FR, UF, UL, UB, BR, DF, DL, DB, DR, FL, BL, UR],
	eo=[0] * 12,
)

# F: corner cycle URF->DFR->DLF->UFL->URF; edge cycle UF->FR->DF->FL->UF.
#    Twists the 4 F-face corners. Flips the 4 F-face edges.
_MOVE_F = _make_move(
	cp=[UFL, DLF, ULB, UBR, URF, DFR, DBL, DRB],
	co=[1, 2, 0, 0, 2, 1, 0, 0],
	ep=[UR, FL, UL, UB, DR, FR, DL, DB, UF, DF, BL, BR],
	eo=[0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
)

# D: corner cycle DFR->DLF->DBL->DRB->DFR; edge cycle DR->DF->DL->DB->DR.
#    No orientation change.
_MOVE_D = _make_move(
	cp=[URF, UFL, ULB, UBR, DRB, DFR, DLF, DBL],
	co=[0, 0, 0, 0, 0, 0, 0, 0],
	ep=[UR, UF, UL, UB, DB, DR, DF, DL, FR, FL, BL, BR],
	eo=[0] * 12,
)

# L: corner cycle UFL->DLF->DBL->ULB->UFL; edge cycle UL->FL->DL->BL->UL.
#    Twists the 4 L-face corners. eo preserved.
_MOVE_L = _make_move(
	cp=[URF, ULB, DBL, UBR, DFR, UFL, DLF, DRB],
	co=[0, 1, 2, 0, 0, 2, 1, 0],
	ep=[UR, UF, BL, UB, DR, DF, FL, DB, FR, UL, DL, BR],
	eo=[0] * 12,
)

# B: corner cycle ULB->DBL->DRB->UBR->ULB; edge cycle UB->BL->DB->BR->UB.
#    Twists the 4 B-face corners. Flips the 4 B-face edges.
_MOVE_B = _make_move(
	cp=[URF, UFL, UBR, DRB, DFR, DLF, ULB, DBL],
	co=[0, 0, 1, 2, 0, 0, 2, 1],
	ep=[UR, UF, UL, BR, DR, DF, DL, BL, FR, FL, UB, DB],
	eo=[0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1],
)


_QUARTER_MOVES = {
	"U": _MOVE_U,
	"R": _MOVE_R,
	"F": _MOVE_F,
	"D": _MOVE_D,
	"L": _MOVE_L,
	"B": _MOVE_B,
}


def _double(move):
	result = CubieCube()
	result.multiply(move)
	result.multiply(move)
	return result


def _inverse(move):
	result = CubieCube()
	result.multiply(move)
	result.multiply(move)
	result.multiply(move)
	return result


MOVES = {}
for _name, _move in _QUARTER_MOVES.items():
	MOVES[_name] = _move
	MOVES[_name + "2"] = _double(_move)
	MOVES[_name + "'"] = _inverse(_move)
