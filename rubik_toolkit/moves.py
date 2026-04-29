"""Move-sequence utilities.

Exports:

- ``summarize_moves(moves, compact=False)`` — reduce a move sequence to
  its shortest equivalent form.

  Adjacent same-face moves are always merged mod 4. Cancellations and
  cascades (``"u r r' u'"`` → ``""``) resolve through the same merging
  logic. The output formatting differs by mode:

    count 1 → ``x``
    count 2 → ``x x`` (default) / ``x2`` (compact)
    count 3 → ``x'`` (always — natural inverse)

  Different faces never merge (no commutativity assumed).
"""

_FACES = frozenset("udlrfb")


def _parse(token):
	"""Parse a move token like ``u``, ``u'``, ``u2`` into ``(face, count)``
	with count in ``{1, 2, 3}``."""
	token = token.lower().strip()
	if not token:
		raise ValueError("empty move token")
	if token.endswith("'"):
		face, count = token[:-1], 3
	elif token.endswith("2"):
		face, count = token[:-1], 2
	else:
		face, count = token, 1
	if face not in _FACES:
		raise ValueError(f"invalid move token: {token!r}")
	return face, count


def _emit(face, count, compact):
	"""Return the list of tokens representing ``count`` quarter-turns of ``face``."""
	if count == 1:
		return [face]
	if count == 2:
		return [face + "2"] if compact else [face, face]
	if count == 3:
		return [face + "'"]
	raise ValueError(f"unexpected count: {count}")


def summarize_moves(moves, compact=False):
	"""Reduce a move sequence to its shortest equivalent form.

	Adjacent same-face moves are merged mod 4; cancellations are dropped.
	By default, count-of-2 streaks emit as two separate quarter-turn
	tokens (``"u u"``); count-of-3 streaks always emit as the inverse
	(``"u'"``). With ``compact=True``, count-of-2 streaks collapse into
	the half-turn shorthand (``"u2"``).

	Accepts either a space-separated string or an iterable of tokens.
	Returns the same type as the input.
	"""
	is_string = isinstance(moves, str)
	tokens = moves.split() if is_string else list(moves)

	stack = []
	for token in tokens:
		face, count = _parse(token)
		if stack and stack[-1][0] == face:
			new_count = (stack[-1][1] + count) % 4
			if new_count == 0:
				stack.pop()
			else:
				stack[-1] = (face, new_count)
		else:
			stack.append((face, count))

	out = []
	for face, count in stack:
		out.extend(_emit(face, count, compact))

	return " ".join(out) if is_string else out
