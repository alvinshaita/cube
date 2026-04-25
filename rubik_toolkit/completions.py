"""Generate possible valid states from a state with unknown stickers.

Exports:

- ``possible_states(state, size=None, limit=None)`` — generator yielding
  every state that matches the partial input AND is valid per
  ``is_state_valid`` (physical pieces, canonical centres on 3×3, corner
  chirality, and solvability parity). Yields state strings, not Cube
  instances. ``size`` is inferred from ``len(state)`` when omitted;
  ``limit`` caps the number of valid states yielded.
- ``count_possible_states(state, size=None)`` — count of valid states
  matching the partial input. Implemented by enumeration: O(N) where N
  is the colour-count-valid completion space, which can be huge for
  highly partial inputs.

Filtering is applied at the leaf of the enumeration: every '?' position
is filled in turn (respecting colour counts), and the resulting candidate
is checked with ``is_state_valid``. Candidates that fail are silently
skipped. For sparse inputs (many unknowns) the search may iterate many
internal candidates before yielding each valid one.

``Cube.possible_states`` and ``Cube.count_possible_states`` are thin
wrappers around these functions.
"""
from collections import Counter

from .validation import infer_size, is_state_valid


UNKNOWN_CHAR = "?"
_COLOR_CHARS = "ybrgow"


def possible_states(state, size=None, limit=None):
	"""Yield every valid state matching the partial ``state``.

	A "valid state" is one that passes :func:`is_state_valid` — colour
	counts balance, every cubelet is a real piece in canonical chirality,
	centres (3×3) are in their fixed positions, and parity invariants
	hold. The '?' positions in ``state`` are filled with colours; known
	stickers are preserved.

	``size`` is inferred from ``len(state)`` when omitted. ``limit`` caps
	the number of valid states yielded (not the number of candidates
	considered).
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


def count_possible_states(state, size=None):
	"""Count valid states matching the partial ``state``.

	Implemented by enumerating ``possible_states`` and counting — O(N)
	where N is the size of the colour-count-valid completion space.
	For inputs with many unknowns this can be expensive; consider
	whether the count is actually needed before calling.
	"""
	state = state.lower()
	if size is None:
		size = infer_size(state)
	if len(state) != 6 * size * size:
		raise ValueError(
			f"state length {len(state)} does not match size {size}"
		)
	return sum(1 for _ in possible_states(state, size))
