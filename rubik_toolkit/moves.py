"""Move-sequence utilities.

Exports:

- ``summarize_moves(moves, compact=False, normalize=False)`` — reduce a
  move sequence to its shortest equivalent form.

  Adjacent same-face moves merge via signed sum (``u`` = +1, ``u2`` = +2,
  ``u'`` = −1). Cancellations and cascades resolve when the sum hits a
  multiple of 4. Output formatting depends on ``R = signed_sum mod 4``:

    R = 1 → ``x``                      (single positive)
    R = 3 → ``x'``                     (single inverse, shorter than ``x x x``)
    R = 2 → sign-preserving by default:
              ``x x``     if sum > 0
              ``x' x'``   if sum < 0
    R = 0 → dropped

  Flags:

  - ``compact`` — collapse R = 2 streaks into the half-turn shorthand
    (``x2``); the half-turn has no signed equivalent so direction is
    forgotten.
  - ``normalize`` — force positive output everywhere. R = 2 emits
    ``x x`` regardless of sign; R = 3 expands to ``x x x`` rather than
    ``x'``. ``compact`` still wins for R = 2 (gives ``x2``); ``normalize``
    still wins for R = 3.

  Different faces never merge (no commutativity assumed).
"""

_FACES = frozenset("udlrfb")


def _parse(token):
	"""Parse a move token into ``(face, signed_count)`` where ``signed_count``
	is +1 for ``x``, +2 for ``x2``, −1 for ``x'``."""
	token = token.lower().strip()
	if not token:
		raise ValueError("empty move token")
	if token.endswith("'"):
		face, count = token[:-1], -1
	elif token.endswith("2"):
		face, count = token[:-1], 2
	else:
		face, count = token, 1
	if face not in _FACES:
		raise ValueError(f"invalid move token: {token!r}")
	return face, count


def _emit(face, signed_sum, compact, normalize):
	"""Tokens for a single (face, signed_sum) stack entry."""
	R = signed_sum % 4
	if R == 0:
		return []
	if R == 1:
		return [face]
	if R == 3:
		return [face, face, face] if normalize else [face + "'"]
	# R == 2
	if compact:
		return [face + "2"]
	if normalize or signed_sum > 0:
		return [face, face]
	return [face + "'", face + "'"]


def summarize_moves(moves, compact=False, normalize=False):
	"""Reduce a move sequence to its shortest equivalent form.

	Adjacent same-face moves are merged via signed sum; cancellations
	(sum ≡ 0 mod 4) are dropped. By default the output preserves the
	sign of the merged streak for count-2 outputs:

	  ``"u u"``      → ``"u u"``      (count 2, positive)
	  ``"u' u'"``    → ``"u' u'"``    (count 2, negative)
	  ``"u u u"``    → ``"u'"``       (R = 3 default — single inverse)
	  ``"u' u' u'"`` → ``"u"``        (sum −3 ≡ +1 mod 4 — single positive)
	  ``"u u u u"``  → ``""``         (full cancel)

	Flags:

	- ``compact=True`` — count-2 streaks collapse to the half-turn
	  shorthand (``"u' u'"`` → ``"u2"``).
	- ``normalize=True`` — emit positive tokens only. Negative count-2
	  becomes positive (``"u' u'"`` → ``"u u"``); single inverses expand
	  (``"u'"`` → ``"u u u"``).

	Accepts either a space-separated string or an iterable of tokens.
	Returns the same type as the input.
	"""
	is_string = isinstance(moves, str)
	tokens = moves.split() if is_string else list(moves)

	# Stack entries are (face, signed_sum). Same-face moves merge by adding
	# their signed counts; an entry whose sum hits a multiple of 4 is dropped.
	stack = []
	for token in tokens:
		face, count = _parse(token)
		if stack and stack[-1][0] == face:
			new_sum = stack[-1][1] + count
			if new_sum % 4 == 0:
				stack.pop()
			else:
				stack[-1] = (face, new_sum)
		else:
			stack.append((face, count))

	out = []
	for face, signed_sum in stack:
		out.extend(_emit(face, signed_sum, compact, normalize))

	return " ".join(out) if is_string else out
