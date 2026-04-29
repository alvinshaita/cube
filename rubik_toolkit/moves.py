"""Move-sequence utilities.

Exports:

- ``summarize_moves(moves, compact=False)`` — drop cancelling moves from
  a sequence.

  - Default behaviour: preserve every input token unchanged unless a
    contiguous same-face streak sums to identity (count mod 4 == 0), in
    which case the whole streak is dropped. ``"u u"`` stays ``"u u"``
    because it isn't identity; ``"u u u u"`` and ``"u u'"`` cancel.
  - ``compact=True``: additionally merge adjacent same-face moves into
    shorthand notation. ``"u u"`` → ``"u2"``; ``"u u u"`` → ``"u'"``.

  Different faces never merge (no commutativity assumed), but cascades
  of cancellations resolve naturally — ``"u r r' u'"`` → ``""``.
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


def _format_compact(face, count):
	if count == 1:
		return face
	if count == 2:
		return face + "2"
	if count == 3:
		return face + "'"
	raise ValueError(f"unexpected count: {count}")


def summarize_moves(moves, compact=False):
	"""Drop cancelling moves from a sequence.

	By default, every input token is preserved unchanged unless a
	contiguous same-face streak sums to identity (count mod 4 == 0), in
	which case the whole streak is dropped. ``"u u"`` stays ``"u u"``;
	``"u u u u"`` and ``"u u'"`` cancel completely.

	With ``compact=True``, adjacent same-face moves are additionally
	merged into shorthand notation: ``"u u"`` → ``"u2"``, ``"u u u"`` →
	``"u'"``.

	Accepts either a space-separated string or an iterable of tokens.
	Returns the same type as the input.
	"""
	is_string = isinstance(moves, str)
	tokens = moves.split() if is_string else list(moves)

	# Stack entries are (face, count, original_token_or_None). The third
	# field lets default mode emit the token exactly as the caller wrote
	# it; compact mode synthesises tokens from (face, count) and stores
	# None for the original.
	stack = []
	for token in tokens:
		face, count = _parse(token)
		stack.append((face, count, token.lower().strip()))

		# Find the longest contiguous same-face suffix.
		i = len(stack) - 1
		while i > 0 and stack[i - 1][0] == face:
			i -= 1
		streak_total = sum(entry[1] for entry in stack[i:]) % 4

		if streak_total == 0:
			del stack[i:]
		elif compact:
			stack[i:] = [(face, streak_total, None)]

	if compact:
		out = [_format_compact(face, count) for face, count, _ in stack]
	else:
		out = [entry[2] for entry in stack]

	return " ".join(out) if is_string else out
