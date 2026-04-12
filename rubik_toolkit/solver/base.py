from abc import ABC, abstractmethod


class BaseSolver(ABC):
	"""Abstract base class for all cube solvers.

	Subclasses implement :meth:`solve` and return a list of move strings
	(e.g. ``["r", "u'", "f2"]``) that, when applied in order to the input
	cube, leave it in a solved state. An empty list means the cube is
	already solved.
	"""

	@abstractmethod
	def solve(self, cube):
		"""Solve ``cube`` and return the move list."""
