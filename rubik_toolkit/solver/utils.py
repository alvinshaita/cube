import math

from .registry import get_solver


def solve(state, method="brute_force"):
	"""Solve a cube given its state string.

	Returns a list of move strings. Kept as a thin entry point so
	``Cube.solve`` can delegate here without importing solver internals.
	"""
	# Lazy import to avoid a circular import with ``rubik_toolkit.cube``.
	from ..cube import Cube

	size = math.isqrt(len(state) // 6)
	cube = Cube(size=size, state=state)
	solver = get_solver(method)
	return solver.solve(cube)
