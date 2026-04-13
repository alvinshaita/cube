from .brute_force import BruteForceSolver
from .kociemba import KociembaSolver


# Registry of available solving strategies. Adding a new strategy is
# just a matter of implementing BaseSolver and listing it here.
SOLVERS = {
	"brute_force": BruteForceSolver,
	"kociemba": KociembaSolver,
}


def get_solver(method):
	"""Return an instance of the solver registered under ``method``."""
	if method not in SOLVERS:
		available = ", ".join(sorted(SOLVERS))
		raise ValueError(
			f"Unknown solver method '{method}'. Available methods: {available}"
		)
	return SOLVERS[method]()
