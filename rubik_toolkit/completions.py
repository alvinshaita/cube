"""Generate possible complete states from a state with unknown stickers.

Exports:

- ``possible_states(state, size=None, limit=None)`` — pure generator that
  yields every colour-count-valid completion of ``state`` (each '?' filled
  with a colour such that every face colour appears exactly size² times).
  Yields state strings, not Cube instances. ``size`` is inferred from
  ``len(state)`` when omitted; ``limit`` caps the number yielded.
- ``count_possible_states(state, size=None)`` — O(1) multinomial count
  without enumerating; returns 0 if the state is over-counted in any
  colour.

A "colour-count-valid" completion does NOT guarantee physical validity or
solvability — wrap with ``is_state_valid`` to filter further. The all-
unknown 3×3 has ~10³³ completions, so ``limit`` is essential for any
state with many unknowns.

``Cube.possible_states`` is a thin wrapper around ``possible_states``.
"""
import math
from collections import Counter

from .validation import infer_size


UNKNOWN_CHAR = "?"
_COLOR_CHARS = "ybrgow"


def count_possible_states(state, size=None):
	"""Number of colour-count-valid completions of ``state``.

	Computed in O(1) via the multinomial coefficient
	N! / (d_y! d_b! d_r! d_g! d_o! d_w!), where d_c is the deficit
	(target − current count) of each colour. Returns 0 if any colour is
	already over-counted.
	"""
	state = state.lower()
	if size is None:
		size = infer_size(state)
	if len(state) != 6 * size * size:
		raise ValueError(
			f"state length {len(state)} does not match size {size}"
		)

	if UNKNOWN_CHAR not in state:
		# Already complete — itself is the only completion (we don't
		# validate colour counts here; that's is_state_valid's job).
		return 1

	target = size * size
	deficits = [target - state.count(c) for c in _COLOR_CHARS]
	if any(d < 0 for d in deficits):
		return 0
	n = sum(deficits)
	result = math.factorial(n)
	for d in deficits:
		result //= math.factorial(d)
	return result


def possible_states(state, size=None, limit=None):
	"""Yield every colour-count-valid completion of ``state``.

	Each yielded value is a complete state string with the '?' positions
	filled so that every colour appears exactly size² times. Order is
	deterministic (lexicographic over the unknown positions).

	``size`` is inferred from ``len(state)`` when omitted. ``limit`` caps
	the number yielded — set it whenever the deficit-sum is large; an
	all-unknown 3×3 has ~10³³ completions.
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
		yield state
		return

	target = size * size
	deficits = {c: target - state.count(c) for c in _COLOR_CHARS}
	if any(d < 0 for d in deficits.values()):
		return  # over-counted — no completion can balance

	unknown_positions = [i for i, ch in enumerate(state) if ch == UNKNOWN_CHAR]
	if sum(deficits.values()) != len(unknown_positions):
		return  # defensive: length invariant broken

	state_chars = list(state)
	remaining = Counter({c: d for c, d in deficits.items() if d > 0})
	sorted_colors = sorted(remaining.keys())
	yielded = 0

	def recurse(pos_idx):
		nonlocal yielded
		if pos_idx == len(unknown_positions):
			yield "".join(state_chars)
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
