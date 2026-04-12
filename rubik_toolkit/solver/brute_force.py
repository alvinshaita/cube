from collections import deque

from .base import BaseSolver


# Full half-turn move set for a 3x3 cube.
MOVES_3X3 = [
	"u", "u'", "u2",
	"d", "d'", "d2",
	"l", "l'", "l2",
	"r", "r'", "r2",
	"f", "f'", "f2",
	"b", "b'", "b2",
]

# For a 2x2, fixing the DLB corner means only R, U, F are needed
# to reach every reachable state. This cuts the branching factor
# from 18 down to 9.
MOVES_2X2 = [
	"r", "r'", "r2",
	"u", "u'", "u2",
	"f", "f'", "f2",
]

# BFS depth caps. 2x2 God's number is 11 (HTM), so 11 is enough to
# solve any 2x2. For 3x3, naive BFS is only practical on near-solved
# cubes; 7 is the rough ceiling before memory and time blow up.
DEFAULT_MAX_DEPTH = {2: 11, 3: 7}


class BruteForceSolver(BaseSolver):
	"""Breadth-first search over the move space.

	Supports 2x2 and 3x3 cubes. For 2x2 this finds an optimal solution
	(in HTM) for any scramble. For 3x3 it only reaches cubes within
	``max_depth`` moves of solved; use a stronger strategy (e.g. Kociemba)
	for full scrambles once available.
	"""

	def __init__(self, max_depth=None):
		self.max_depth = max_depth

	def solve(self, cube):
		if cube.size not in (2, 3):
			raise NotImplementedError(
				f"BruteForceSolver supports 2x2 and 3x3 cubes only; "
				f"got {cube.size}x{cube.size}"
			)

		if cube.solved():
			return []

		moves = MOVES_2X2 if cube.size == 2 else MOVES_3X3
		max_depth = self.max_depth or DEFAULT_MAX_DEPTH[cube.size]

		start = cube.copy()
		visited = {start.state}
		queue = deque([(start, [])])

		while queue:
			current, path = queue.popleft()
			if len(path) >= max_depth:
				continue

			# Skip moves on the same face as the previous move
			# (e.g. don't follow "r" with "r'" or "r2").
			last_face = path[-1][0] if path else None

			for move in moves:
				if move[0] == last_face:
					continue

				nxt = current.copy()
				nxt.rotate(move)

				if nxt.state in visited:
					continue
				if nxt.solved():
					return path + [move]

				visited.add(nxt.state)
				queue.append((nxt, path + [move]))

		raise RuntimeError(
			f"No solution found within depth {max_depth}. "
			f"Increase max_depth or use a stronger solver."
		)
