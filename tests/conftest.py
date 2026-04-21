import pytest

from rubik_toolkit import Cube


SOLVED_STATE_3X3 = "yyyyyyyyybbbbbbbbbrrrrrrrrrgggggggggooooooooowwwwwwwww"
SOLVED_STATE_2X2 = "yyyybbbbrrrrggggoooowwww"

FACES = ("u", "d", "l", "r", "f", "b")

# Golden expected states for every single quarter/half turn applied to a solved 3x3.
# Captured by running the implementation and verified against cube identities
# (inverse, 4x = identity, 2x = double). See test_cube.py for the identity checks.
EXPECTED_SINGLE_MOVE_STATES = {
    "u":  "yyyyyyyyyrrrbbbbbbgggrrrrrroooggggggbbboooooowwwwwwwww",
    "u'": "yyyyyyyyyooobbbbbbbbbrrrrrrrrrgggggggggoooooowwwwwwwww",
    "u2": "yyyyyyyyygggbbbbbbooorrrrrrbbbggggggrrroooooowwwwwwwww",
    "d":  "yyyyyyyyybbbbbbooorrrrrrbbbggggggrrroooooogggwwwwwwwww",
    "d'": "yyyyyyyyybbbbbbrrrrrrrrrgggggggggooooooooobbbwwwwwwwww",
    "d2": "yyyyyyyyybbbbbbgggrrrrrroooggggggbbboooooorrrwwwwwwwww",
    "l":  "oyyoyyoyybbbbbbbbbyrryrryrrgggggggggoowoowoowrwwrwwrww",
    "l'": "ryyryyryybbbbbbbbbwrrwrrwrrgggggggggooyooyooyowwowwoww",
    "l2": "wyywyywyybbbbbbbbborrorrorrgggggggggoorooroorywwywwyww",
    "r":  "yyryyryyrbbbbbbbbbrrwrrwrrwgggggggggyooyooyoowwowwowwo",
    "r'": "yyoyyoyyobbbbbbbbbrryrryrrygggggggggwoowoowoowwrwwrwwr",
    "r2": "yywyywyywbbbbbbbbbrrorrorrogggggggggroorooroowwywwywwy",
    "f":  "yyyyyybbbbbwbbwbbwrrrrrrrrryggyggyggooooooooogggwwwwww",
    "f'": "yyyyyygggbbybbybbyrrrrrrrrrwggwggwggooooooooobbbwwwwww",
    "f2": "yyyyyywwwbbgbbgbbgrrrrrrrrrbggbggbggoooooooooyyywwwwww",
    "b":  "gggyyyyyyybbybbybbrrrrrrrrrggwggwggwooooooooowwwwwwbbb",
    "b'": "bbbyyyyyywbbwbbwbbrrrrrrrrrggyggyggyooooooooowwwwwwggg",
    "b2": "wwwyyyyyygbbgbbgbbrrrrrrrrrggbggbggbooooooooowwwwwwyyy",
}


@pytest.fixture
def solved():
    """A freshly-solved 3x3 cube."""
    return Cube()


@pytest.fixture
def solved_2x2():
    """A freshly-solved 2x2 cube."""
    return Cube(size=2)


def cubelet_colors(cube):
    """Multiset (sorted list) of every non-None sticker colour across all cubelets."""
    out = []
    for i in range(cube.size):
        for j in range(cube.size):
            for k in range(cube.size):
                for v in cube.cube[i][j][k].pos.values():
                    if v is not None:
                        out.append(v)
    return sorted(out)


def invert_move(m):
    """Return the inverse of a single WCA-ish move token."""
    if m.endswith("2"):
        return m
    if m.endswith("'"):
        return m[:-1]
    return m + "'"


def invert_sequence(seq):
    """Return the inverse of a space-separated move sequence."""
    return " ".join(invert_move(m) for m in reversed(seq.split()))
