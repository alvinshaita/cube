"""Move-sequence utilities.

Exports:

- ``summarize_moves(moves)`` — reduce a sequence of cube moves to its
  shortest equivalent by merging *adjacent* same-face moves mod 4:

      u u   →  u2
      u u u →  u'
      u u u u → (empty)
      u u'  →  (empty)
      u r r' u' → (empty)        # cascades resolve

  Different faces don't commute on a Rubik's cube, so ``u r u'`` stays
  ``u r u'`` — only adjacent same-face moves are merged. The reduction
  is greedy and iterative via a stack, so any cascade of cancellations
  resolves in a single pass.
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


def _format(face, count):
	if count == 1:
		return face
	if count == 2:
		return face + "2"
	if count == 3:
		return face + "'"
	raise ValueError(f"unexpected count: {count}")


def summarize_moves(moves):
	"""Reduce a move sequence to its shortest equivalent form.

	Accepts either a space-separated string (``"u r u'"``) or an iterable
	of tokens (``["u", "r", "u'"]``). Returns the same type as the input.

	The empty result (``""`` or ``[]``) represents the identity rotation.
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

	out = [_format(face, count) for face, count in stack]
	return " ".join(out) if is_string else out
