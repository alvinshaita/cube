"""Two-phase IDA* solver on Kociemba's coordinate representation.

The search runs in two phases:

	Phase 1:  IDA* over (twist, flip, slice) using max of the two
	          phase-1 pruning tables as its admissible heuristic, over
	          all 18 HTM moves. Stops when (twist, flip, slice) = (0, 0, 0),
	          i.e. the cube has been reduced into the subgroup G1 =
	          <U, D, L2, R2, F2, B2>.

	Phase 2:  IDA* over (cp, ep_ud, sp) restricted to the 10 G1 moves,
	          using max of the two phase-2 pruning tables. Stops when
	          all three coords are 0 (fully solved).

The concatenation of the two phase move lists is the final solution.
This basic version does not iterate sub-optimal phase 1 solutions to
hunt for a shorter total length; it returns the first complete
solution it finds, which is typically correct but not globally
optimal. Solutions for random 3x3 scrambles generally land in the
20-30 HTM range.
"""
from __future__ import annotations

from ..base import BaseSolver
from . import coord as cd
from . import moves as mv
from . import pruning as pr
from .from_cube import from_cube


_FACE_OF_HTM = [m[0] for m in mv.HTM_MOVES]
_FACE_OF_PHASE2 = [m[0] for m in mv.PHASE2_MOVES]


def _phase1_search(twist: int, flip: int, slice_: int, max_depth: int) -> list[int] | None:
	tsp = pr.twist_slice_prun()
	fsp = pr.flip_slice_prun()
	tm = mv.twist_move()
	fm = mv.flip_move()
	sm = mv.slice_move()
	htm_count = mv.HTM_COUNT
	slice_count = cd.SLICE_COUNT
	face_of = _FACE_OF_HTM

	def recurse(t: int, f: int, s: int, last_face: str | None, depth: int, path: list[int]) -> bool:
		h = max(tsp[t * slice_count + s], fsp[f * slice_count + s])
		if h > depth:
			return False
		if h == 0:
			return True
		for mi in range(htm_count):
			face = face_of[mi]
			if face == last_face:
				continue
			path.append(mi)
			if recurse(tm[t][mi], fm[f][mi], sm[s][mi], face, depth - 1, path):
				return True
			path.pop()
		return False

	path: list[int] = []
	for d in range(max_depth + 1):
		if recurse(twist, flip, slice_, None, d, path):
			return path
	return None


def _phase2_search(cp: int, ep_ud: int, sp: int, max_depth: int) -> list[int] | None:
	csp = pr.cp_sp_prun()
	esp = pr.ep_ud_sp_prun()
	cm = mv.cp_move()
	em = mv.ep_ud_move()
	spm = mv.sp_move()
	phase2_count = mv.PHASE2_COUNT
	sp_count = cd.SP_COUNT
	face_of = _FACE_OF_PHASE2

	def recurse(c: int, e: int, s: int, last_face: str | None, depth: int, path: list[int]) -> bool:
		h = max(csp[c * sp_count + s], esp[e * sp_count + s])
		if h > depth:
			return False
		if h == 0:
			return True
		for mi in range(phase2_count):
			face = face_of[mi]
			if face == last_face:
				continue
			path.append(mi)
			if recurse(cm[c][mi], em[e][mi], spm[s][mi], face, depth - 1, path):
				return True
			path.pop()
		return False

	path: list[int] = []
	for d in range(max_depth + 1):
		if recurse(cp, ep_ud, sp, None, d, path):
			return path
	return None


class KociembaSolver(BaseSolver):
	"""Two-phase Kociemba solver for 3x3 cubes."""

	def solve(self, cube):
		if cube.size != 3:
			raise NotImplementedError(
				f"KociembaSolver supports 3x3 cubes only; got {cube.size}x{cube.size}. "
				f"Use method='brute_force' for 2x2 cubes."
			)

		cc = from_cube(cube)
		if cc.is_solved():
			return []

		# --- Phase 1 ---
		twist = cd.get_twist(cc)
		flip = cd.get_flip(cc)
		slice_ = cd.get_slice(cc)
		phase1_indices = _phase1_search(twist, flip, slice_, max_depth=12)
		if phase1_indices is None:
			raise RuntimeError("Kociemba phase 1 failed within depth 12")
		phase1_moves = [mv.HTM_MOVES[i] for i in phase1_indices]

		# Apply phase 1 to the cubie state to get the start of phase 2.
		for mname in phase1_moves:
			cc.apply(mname)

		# --- Phase 2 ---
		cp = cd.get_cp(cc)
		ep_ud = cd.get_ep_ud(cc)
		sp = cd.get_sp(cc)
		phase2_indices = _phase2_search(cp, ep_ud, sp, max_depth=18)
		if phase2_indices is None:
			raise RuntimeError("Kociemba phase 2 failed within depth 18")
		phase2_moves = [mv.PHASE2_MOVES[i] for i in phase2_indices]

		return [m.lower() for m in phase1_moves + phase2_moves]
