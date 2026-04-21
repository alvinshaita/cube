"""Tests for rubik_toolkit.cube.Cube.

Covers construction, state/cube-array synchronisation, every face turn,
the rotate() notation parser, whole-cube rotations, invariants preserved
by all moves, and well-known algorithm identities (sexy move, sune,
T-perm, Y-perm) as higher-level behavioural guarantees.
"""
import re

import numpy as np
import pytest

from rubik_toolkit import Cube
from rubik_toolkit.cubelet import Cubelet

from .conftest import (
    SOLVED_STATE_3X3,
    SOLVED_STATE_2X2,
    FACES,
    EXPECTED_SINGLE_MOVE_STATES,
    cubelet_colors,
    invert_sequence,
)


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------

class TestCubeInit:
    def test_default_size_is_3(self):
        c = Cube()
        assert c.size == 3

    def test_default_state_is_solved_3x3(self):
        c = Cube()
        assert c.state == SOLVED_STATE_3X3

    def test_default_state_length_is_6NN(self):
        c = Cube()
        assert len(c.state) == 54

    def test_size_2_default_state(self):
        c = Cube(size=2)
        assert c.state == SOLVED_STATE_2X2
        assert len(c.state) == 24

    def test_initial_path_is_empty(self):
        assert Cube().path == []

    def test_lowercases_explicit_state(self):
        c = Cube(state=SOLVED_STATE_3X3.upper())
        assert c.state == SOLVED_STATE_3X3

    def test_default_state_exposed_on_instance(self):
        """The init stores a computed `default_state` attribute; callers
        occasionally read it to compare against a scrambled state."""
        c = Cube()
        assert c.default_state == SOLVED_STATE_3X3

    def test_wrong_length_state_raises(self):
        with pytest.raises(AssertionError):
            Cube(state="abc")

    def test_state_too_long_raises(self):
        with pytest.raises(AssertionError):
            Cube(state=SOLVED_STATE_3X3 + "y")

    def test_state_mismatched_size_raises(self):
        with pytest.raises(AssertionError):
            Cube(size=2, state=SOLVED_STATE_3X3)

    def test_cube_array_is_NxNxN(self):
        c = Cube()
        assert c.cube.shape == (3, 3, 3)

    def test_cube_2x2_array_shape(self):
        c = Cube(size=2)
        assert c.cube.shape == (2, 2, 2)

    def test_every_array_entry_is_cubelet(self):
        c = Cube()
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    assert isinstance(c.cube[i][j][k], Cubelet)


# ---------------------------------------------------------------------------
# state <-> cube array synchronisation
# ---------------------------------------------------------------------------

class TestStateCubeSync:
    def test_load_state_is_inverse_of_generate(self):
        """Building the array from the state and reading it back must round-trip."""
        scrambled = "yyryyryyrbbbbbbbbbrrwrrwrrwgggggggggyooyooyoowwowwowwo"
        c = Cube(state=scrambled)
        c.load_state()
        assert c.state == scrambled

    def test_solved_centers_on_3x3(self):
        """Face centres of a solved 3x3 are fixed, so the cube array must
        place each centre colour on the corresponding face of the centre cubelet."""
        c = Cube()
        assert c.cube[0][1][1].pos["f"] == "red"      # F centre
        assert c.cube[-1][1][1].pos["b"] == "orange"  # B centre
        assert c.cube[1][0][1].pos["u"] == "yellow"   # U centre
        assert c.cube[1][-1][1].pos["d"] == "white"   # D centre
        assert c.cube[1][1][0].pos["l"] == "blue"     # L centre
        assert c.cube[1][1][-1].pos["r"] == "green"   # R centre

    def test_interior_cubelet_has_no_exposed_faces(self):
        """The one truly interior cubelet on a 3x3 has no stickers."""
        c = Cube()
        inner = c.cube[1][1][1]
        assert all(v is None for v in inner.pos.values())

    def test_roundtrip_preserves_state(self):
        """Parse a state, run load_state, re-init from the new state — must match."""
        scrambled_state = "yyryyryyrbbbbbbbbbrrwrrwrrwgggggggggyooyooyoowwowwowwo"
        c = Cube(state=scrambled_state)
        assert c.state == scrambled_state
        c2 = Cube(state=c.state)
        assert c2.state == scrambled_state


# ---------------------------------------------------------------------------
# Every single face turn produces the expected state
# ---------------------------------------------------------------------------

class TestSingleMoveStates:
    @pytest.mark.parametrize("move,expected", list(EXPECTED_SINGLE_MOVE_STATES.items()))
    def test_exact_state_after_move(self, move, expected):
        c = Cube()
        c.rotate(move)
        assert c.state == expected


class TestMoveIdentities:
    """Identities every quarter-turn move must satisfy on a solved cube."""

    @pytest.mark.parametrize("face", FACES)
    def test_four_quarter_turns_is_identity(self, face):
        c = Cube()
        for _ in range(4):
            c.rotate(face)
        assert c.solved()
        assert c.state == SOLVED_STATE_3X3

    @pytest.mark.parametrize("face", FACES)
    def test_inverse_cancels(self, face):
        c = Cube()
        c.rotate(f"{face} {face}'")
        assert c.state == SOLVED_STATE_3X3

    @pytest.mark.parametrize("face", FACES)
    def test_double_equals_two_quarter_turns(self, face):
        a, b = Cube(), Cube()
        a.rotate(f"{face}2")
        b.rotate(f"{face} {face}")
        assert a.state == b.state

    @pytest.mark.parametrize("face", FACES)
    def test_prime_equals_three_quarter_turns(self, face):
        a, b = Cube(), Cube()
        a.rotate(f"{face}'")
        b.rotate(f"{face} {face} {face}")
        assert a.state == b.state

    @pytest.mark.parametrize("face", FACES)
    def test_double_is_its_own_inverse(self, face):
        c = Cube()
        c.rotate(f"{face}2 {face}2")
        assert c.state == SOLVED_STATE_3X3


# ---------------------------------------------------------------------------
# rotate() string parser
# ---------------------------------------------------------------------------

class TestRotateParser:
    def test_single_move(self):
        c = Cube()
        c.rotate("u")
        assert c.state == EXPECTED_SINGLE_MOVE_STATES["u"]

    def test_uppercase_accepted(self):
        a, b = Cube(), Cube()
        a.rotate("U R F")
        b.rotate("u r f")
        assert a.state == b.state

    def test_mixed_case_accepted(self):
        a, b = Cube(), Cube()
        a.rotate("U r F'")
        b.rotate("u r f'")
        assert a.state == b.state

    def test_multi_move_sequence(self):
        c = Cube()
        c.rotate("u u")
        assert c.state == EXPECTED_SINGLE_MOVE_STATES["u2"]

    def test_sequence_with_all_notations(self):
        """u + r' + f2 composed step-by-step equals the same rotate() call."""
        a = Cube()
        a.rotate_u()
        a.rotate_r(times_to_move=-1)
        a.rotate_f(times_to_move=2)

        b = Cube()
        b.rotate("u r' f2")
        assert a.state == b.state

    def test_unknown_token_is_silently_ignored(self):
        """The parser's if/elif chain has no default branch — unknown tokens
        are dropped. Pin this behaviour so a future refactor stays explicit."""
        c = Cube()
        c.rotate("xyz")
        assert c.state == SOLVED_STATE_3X3

    def test_empty_string_is_noop(self):
        c = Cube()
        c.rotate("")
        assert c.state == SOLVED_STATE_3X3


class TestPathTracking:
    def test_path_starts_empty(self):
        assert Cube().path == []

    def test_quarter_turn_recorded_as_times_1(self):
        c = Cube()
        c.rotate("u")
        assert c.path == [("u", 1)]

    def test_prime_recorded_as_times_3(self):
        """rotate_X(times_to_move=-1) is normalised via `% 4` to 3."""
        c = Cube()
        c.rotate("u'")
        assert c.path == [("u", 3)]

    def test_double_recorded_as_times_2(self):
        c = Cube()
        c.rotate("u2")
        assert c.path == [("u", 2)]

    def test_multi_move_path(self):
        c = Cube()
        c.rotate("u r' f2")
        assert c.path == [("u", 1), ("r", 3), ("f", 2)]

    def test_four_turns_recorded_as_four_entries(self):
        """Four u turns bring state back to solved but the path records them."""
        c = Cube()
        for _ in range(4):
            c.rotate("u")
        assert c.path == [("u", 1)] * 4
        assert c.solved()


# ---------------------------------------------------------------------------
# Direct rotate_X method calls (bypassing the parser)
# ---------------------------------------------------------------------------

class TestDirectRotateMethods:
    @pytest.mark.parametrize("face", FACES)
    def test_default_is_quarter_turn(self, face):
        c = Cube()
        getattr(c, f"rotate_{face}")()
        assert c.state == EXPECTED_SINGLE_MOVE_STATES[face]

    @pytest.mark.parametrize("face", FACES)
    def test_times_minus_one_is_prime(self, face):
        c = Cube()
        getattr(c, f"rotate_{face}")(times_to_move=-1)
        assert c.state == EXPECTED_SINGLE_MOVE_STATES[f"{face}'"]

    @pytest.mark.parametrize("face", FACES)
    def test_times_two_is_half_turn(self, face):
        c = Cube()
        getattr(c, f"rotate_{face}")(times_to_move=2)
        assert c.state == EXPECTED_SINGLE_MOVE_STATES[f"{face}2"]

    @pytest.mark.parametrize("face", FACES)
    def test_times_wraps_mod_4(self, face):
        """times_to_move=5 should behave like times_to_move=1."""
        a, b = Cube(), Cube()
        getattr(a, f"rotate_{face}")(times_to_move=5)
        getattr(b, f"rotate_{face}")(times_to_move=1)
        assert a.state == b.state


class TestInnerSliceMoves:
    """The rotate_X methods accept an `index_to_move` arg that picks an
    inner layer. On a 3x3, index=1 rotates only the middle slice (no
    effect on centres of that face but the E/M/S-slice edges move)."""

    def test_u_inner_slice_leaves_outer_layers_solved(self):
        """Rotating the middle U-slice doesn't disturb the U face itself."""
        c = Cube()
        c.rotate_u(index_to_move=1)
        # U face of the top layer remains all-yellow.
        assert c.state[:9] == "y" * 9
        # D face of the bottom layer remains all-white.
        assert c.state[-9:] == "w" * 9

    def test_u_inner_slice_x4_is_identity(self):
        c = Cube()
        s0 = c.state
        for _ in range(4):
            c.rotate_u(index_to_move=1)
        assert c.state == s0


# ---------------------------------------------------------------------------
# Whole-cube orientation rotations
# ---------------------------------------------------------------------------

class TestRotateAll:
    @pytest.mark.parametrize("face", FACES)
    def test_whole_cube_rotation_keeps_cube_solved(self, face):
        """A whole-cube rotation is just a reorientation; a solved cube stays solved."""
        c = Cube()
        getattr(c, f"rotate_all_{face}")()
        assert c.solved()

    @pytest.mark.parametrize("face", FACES)
    def test_whole_cube_rotation_x4_is_identity(self, face):
        c = Cube()
        s0 = c.state
        for _ in range(4):
            getattr(c, f"rotate_all_{face}")()
        assert c.state == s0

    def test_rotate_all_equals_rotating_every_layer(self):
        """rotate_all_u == rotate_u at every layer index."""
        a = Cube()
        a.rotate_all_u()

        b = Cube()
        for i in range(3):
            b.rotate_u(index_to_move=i)
        assert a.state == b.state

    def test_rotate_all_u_scrambled_cube(self):
        """Whole-cube rotation of a scrambled cube just relabels faces —
        the cube is still scrambled the same amount, but the state string
        differs because face labelling changed."""
        c = Cube()
        c.rotate("r u r' u'")
        before = c.state
        c.rotate_all_u()
        assert not c.solved()  # still scrambled
        assert c.state != before  # but state string changes


# ---------------------------------------------------------------------------
# solved() predicate
# ---------------------------------------------------------------------------

class TestSolved:
    def test_fresh_cube_is_solved(self):
        assert Cube().solved()

    def test_solved_from_solved_state(self):
        assert Cube(state=SOLVED_STATE_3X3).solved()

    @pytest.mark.parametrize("face", FACES)
    def test_one_move_makes_cube_unsolved(self, face):
        c = Cube()
        c.rotate(face)
        assert not c.solved()

    def test_rotated_but_still_uniform_faces_is_solved(self):
        """solved() checks each face is monochrome, not that colours are in
        their 'home' positions — so a whole-cube rotation keeps it solved."""
        c = Cube()
        c.rotate_all_u()
        assert c.solved()

    def test_2x2_solved(self):
        assert Cube(size=2).solved()

    def test_2x2_one_move_unsolved(self):
        c = Cube(size=2)
        c.rotate("r")
        assert not c.solved()


# ---------------------------------------------------------------------------
# Equality and copy
# ---------------------------------------------------------------------------

class TestEquality:
    def test_two_solved_cubes_are_equal(self):
        assert Cube() == Cube()

    def test_equality_ignores_path(self):
        """__eq__ only compares state; path history is ignored."""
        a = Cube()
        b = Cube()
        b.rotate("u u'")  # net no-op, but path is now [('u',1),('u',3)]
        assert a.state == b.state
        assert b.path != []
        assert a == b

    def test_different_states_not_equal(self):
        a = Cube()
        b = Cube()
        b.rotate("u")
        assert a != b


class TestCopy:
    def test_copy_produces_equal_cube(self):
        a = Cube()
        a.rotate("r u r' u'")
        b = a.copy()
        assert a == b
        assert a.state == b.state

    def test_copy_is_independent_state(self):
        a = Cube()
        b = a.copy()
        b.rotate("u")
        assert a.solved()
        assert not b.solved()

    def test_copy_is_independent_path(self):
        a = Cube()
        a.rotate("u")
        b = a.copy()
        b.rotate("r")
        assert a.path == [("u", 1)]
        assert b.path == [("u", 1), ("r", 1)]

    def test_copy_is_independent_cube_array(self):
        a = Cube()
        b = a.copy()
        # Mutating b's array should not touch a's.
        b.cube[0][0][0].pos["u"] = "MUTATED"
        assert a.cube[0][0][0].pos["u"] != "MUTATED"


# ---------------------------------------------------------------------------
# Invariants preserved by every rotation
# ---------------------------------------------------------------------------

class TestInvariants:
    @pytest.mark.parametrize(
        "sequence",
        [
            "u",
            "r u r' u'",
            "r u r' u r u2 r'",  # sune
            "r u r' u' r' f r2 u' r' u' r u r' f'",  # t-perm
            "f r u' r' u' r u r' f' r u r' u' r' f r f'",  # y-perm
        ],
    )
    def test_color_multiset_preserved(self, sequence):
        """Every rotation is a permutation of stickers — never adds or removes
        colour. The multiset of all exposed colours must stay constant."""
        c = Cube()
        before = cubelet_colors(c)
        c.rotate(sequence)
        after = cubelet_colors(c)
        assert before == after

    @pytest.mark.parametrize(
        "sequence",
        [
            "u",
            "r u r' u'",
            "r u r' u r u2 r'",
            "r u r' u' r' f r2 u' r' u' r u r' f'",
        ],
    )
    def test_state_is_valid_length_and_chars(self, sequence):
        c = Cube()
        c.rotate(sequence)
        assert len(c.state) == 54
        assert set(c.state) <= set("ybrgow")

    @pytest.mark.parametrize(
        "sequence",
        [
            "u",
            "r u r' u'",
            "r u r' u r u2 r'",
            "r u r' u' r' f r2 u' r' u' r u r' f'",
        ],
    )
    def test_each_color_appears_9_times_on_3x3(self, sequence):
        c = Cube()
        c.rotate(sequence)
        for colour in "ybrgow":
            assert c.state.count(colour) == 9

    def test_face_centers_never_move_with_face_turns(self):
        """Face centres are fixed on a real 3x3 — they can only rotate in place."""
        c = Cube()
        c.rotate("r u r' u' r u' r' f' u' f r u r'")  # random face-turn sequence
        assert c.cube[0][1][1].pos["f"] == "red"
        assert c.cube[-1][1][1].pos["b"] == "orange"
        assert c.cube[1][0][1].pos["u"] == "yellow"
        assert c.cube[1][-1][1].pos["d"] == "white"
        assert c.cube[1][1][0].pos["l"] == "blue"
        assert c.cube[1][1][-1].pos["r"] == "green"


class TestRoundTrip:
    @pytest.mark.parametrize(
        "sequence",
        [
            "u r f",
            "r u r' u'",
            "r u r' u r u2 r'",
            "r u r' u' r' f r2 u' r' u' r u r' f'",
            "f r u' r' u' r u r' f' r u r' u' r' f r f'",
            "u d l r f b u' d' l' r' f' b'",
        ],
    )
    def test_sequence_then_inverse_restores_solved(self, sequence):
        c = Cube()
        c.rotate(sequence)
        c.rotate(invert_sequence(sequence))
        assert c.solved()


# ---------------------------------------------------------------------------
# Well-known algorithm identities
# ---------------------------------------------------------------------------

class TestAlgorithmIdentities:
    def test_sexy_move_order_6(self):
        """(R U R' U') repeated 6 times restores a solved cube."""
        c = Cube()
        for _ in range(6):
            c.rotate("r u r' u'")
        assert c.solved()

    def test_sexy_move_order_lt_6(self):
        """The sexy move has order 6; fewer reps should not solve it."""
        c = Cube()
        for _ in range(5):
            c.rotate("r u r' u'")
        assert not c.solved()

    def test_sune_order_6(self):
        """Sune has order 6."""
        c = Cube()
        for _ in range(6):
            c.rotate("r u r' u r u2 r'")
        assert c.solved()

    def test_t_perm_order_2(self):
        """T-perm is a 3-cycle... no wait, T-perm swaps two pairs — it's an involution."""
        alg = "r u r' u' r' f r2 u' r' u' r u r' f'"
        c = Cube()
        c.rotate(alg)
        assert not c.solved()
        c.rotate(alg)
        assert c.solved()

    def test_y_perm_order_2(self):
        """Y-perm swaps two adjacent corner/edge pairs; applying it twice restores."""
        alg = "f r u' r' u' r u r' f' r u r' u' r' f r f'"
        c = Cube()
        c.rotate(alg)
        assert not c.solved()
        c.rotate(alg)
        assert c.solved()

    def test_superflip_candidate_is_unsolved(self):
        """Just a sanity check that a long scramble produces an unsolved cube."""
        c = Cube()
        c.rotate("r u r' u r u2 r' l' u' l u' l' u2 l")
        assert not c.solved()


# ---------------------------------------------------------------------------
# Rendering: to_string / __repr__ / group_sides
# ---------------------------------------------------------------------------

class TestToString:
    def test_to_string_returns_str(self):
        assert isinstance(Cube().to_string(), str)

    def test_repr_returns_to_string(self):
        c = Cube()
        assert repr(c) == c.to_string()

    def test_rendering_has_expected_line_count(self):
        """Net view is 3 U-rows + 3 middle rows + 3 D-rows = 9 lines (plus trailing newline)."""
        c = Cube()
        # trailing newline means splitlines() gives 9, split('\n') gives 10.
        assert len(c.to_string().splitlines()) == 9

    def test_rendering_2x2_line_count(self):
        c = Cube(size=2)
        assert len(c.to_string().splitlines()) == 6

    def test_rendering_contains_all_colors_of_solved_cube(self):
        rep = Cube().to_string()
        for colour in "ybrgow":
            assert colour in rep

    def test_rendering_changes_after_move(self):
        a = Cube().to_string()
        c = Cube()
        c.rotate("u")
        assert a != c.to_string()


class TestGroupSides:
    def test_returns_all_six_faces(self):
        gs = Cube().group_sides()
        assert set(gs.keys()) == {"u", "d", "l", "r", "f", "b"}

    def test_each_face_is_NxN(self):
        c = Cube()
        gs = c.group_sides()
        for face, grid in gs.items():
            assert len(grid) == 3
            for row in grid:
                assert len(row) == 3

    def test_solved_cube_each_face_is_monochrome(self):
        gs = Cube().group_sides()
        for face, grid in gs.items():
            flat = {cell for row in grid for cell in row}
            assert len(flat) == 1

    def test_solved_face_colors_match_convention(self):
        """yellow=U, blue=L, red=F, green=R, orange=B, white=D."""
        gs = Cube().group_sides()
        assert gs["u"][0][0] == "y"
        assert gs["l"][0][0] == "b"
        assert gs["f"][0][0] == "r"
        assert gs["r"][0][0] == "g"
        assert gs["b"][0][0] == "o"
        assert gs["d"][0][0] == "w"

    def test_2x2_group_sides_shape(self):
        gs = Cube(size=2).group_sides()
        for face, grid in gs.items():
            assert len(grid) == 2
            assert all(len(row) == 2 for row in grid)


# ---------------------------------------------------------------------------
# 2x2 specific behaviour
# ---------------------------------------------------------------------------

class TestCube2x2:
    def test_solved_default(self):
        assert Cube(size=2).solved()

    def test_state_length(self):
        assert len(Cube(size=2).state) == 24

    @pytest.mark.parametrize("face", FACES)
    def test_four_turns_identity(self, face):
        c = Cube(size=2)
        for _ in range(4):
            c.rotate(face)
        assert c.solved()
        assert c.state == SOLVED_STATE_2X2

    @pytest.mark.parametrize("face", FACES)
    def test_inverse_cancels(self, face):
        c = Cube(size=2)
        c.rotate(f"{face} {face}'")
        assert c.state == SOLVED_STATE_2X2

    def test_sexy_move_order_6(self):
        c = Cube(size=2)
        for _ in range(6):
            c.rotate("r u r' u'")
        assert c.solved()

    def test_color_multiset_preserved(self):
        c = Cube(size=2)
        before = cubelet_colors(c)
        c.rotate("r u r' f' u r u'")
        after = cubelet_colors(c)
        assert before == after

    def test_each_color_appears_4_times_on_2x2(self):
        c = Cube(size=2)
        c.rotate("r u r' f'")
        for colour in "ybrgow":
            assert c.state.count(colour) == 4
