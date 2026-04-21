"""Tests for rubik_toolkit.constants.

The SLICE helper builds numpy index tuples that pick out a single layer of
the NxNxN cube array. Getting this wrong silently corrupts every rotation,
so the tests pin the exact tuple shape and the near/far semantics.
"""
import numpy as np
import pytest

from rubik_toolkit.constants import (
    SLICE,
    SLICES,
    ORIENTATION_LAYOUT,
    colors,
    twotwo,
    DEFAULT_CUBE_2X2,
    DEFAULT_CUBE_3X3,
)
from rubik_toolkit.cubelet import Cubelet


ALL_NONE = slice(None, None, None)


class TestSlicesDict:
    def test_has_all_six_faces(self):
        assert set(SLICES.keys()) == {"U", "D", "L", "R", "F", "B"}

    @pytest.mark.parametrize(
        "face,axis",
        [("F", 0), ("B", 0), ("U", 1), ("D", 1), ("L", 2), ("R", 2)],
    )
    def test_axis_assignments(self, face, axis):
        """F/B run along axis 0, U/D along axis 1, L/R along axis 2."""
        assert SLICES[face]["slice_index_to_move"] == axis

    @pytest.mark.parametrize(
        "face,near_or_far",
        [("U", 0), ("L", 0), ("F", 0), ("D", -1), ("R", -1), ("B", -1)],
    )
    def test_near_far_assignments(self, face, near_or_far):
        """U/L/F are the 'near' end (slice 0); D/R/B are the 'far' end (-1)."""
        assert SLICES[face]["slice_to_move"] == near_or_far


class TestSliceIndexBuilder:
    """SLICE.X(i) returns a tuple suitable for numpy fancy indexing."""

    def test_u_index_0(self):
        assert SLICE.U(0) == (ALL_NONE, 0, ALL_NONE)

    def test_u_inner_layer(self):
        """U(1) indexes the second-from-top layer (equator-ish on a 3x3)."""
        assert SLICE.U(1) == (ALL_NONE, 1, ALL_NONE)

    def test_d_index_0_is_far_end(self):
        """D uses slice_to_move=-1, so passing index=0 resolves to -1 (last row)."""
        assert SLICE.D(0) == (ALL_NONE, -1, ALL_NONE)

    def test_d_index_1_is_second_from_far(self):
        """D(1) should map to -2 (second layer counted from the bottom)."""
        assert SLICE.D(1) == (ALL_NONE, -2, ALL_NONE)

    def test_l_index_0(self):
        assert SLICE.L(0) == (ALL_NONE, ALL_NONE, 0)

    def test_r_index_0(self):
        assert SLICE.R(0) == (ALL_NONE, ALL_NONE, -1)

    def test_f_index_0(self):
        assert SLICE.F(0) == (0, ALL_NONE, ALL_NONE)

    def test_b_index_0(self):
        assert SLICE.B(0) == (-1, ALL_NONE, ALL_NONE)

    @pytest.mark.parametrize("face", ["U", "D", "L", "R", "F", "B"])
    def test_returns_tuple_of_length_3(self, face):
        assert len(SLICE[face](0)) == 3


class TestSlicePicksCorrectLayer:
    """Use SLICE tuples against a real 3x3x3 array and verify the layer."""

    @pytest.fixture
    def arr(self):
        # Unique integer per cell so we can verify which cells are picked.
        return np.arange(27).reshape(3, 3, 3)

    def test_u_picks_top_layer(self, arr):
        # "Top" layer on this convention is the j=0 column across all i,k.
        picked = arr[SLICE.U(0)]
        assert picked.shape == (3, 3)
        np.testing.assert_array_equal(picked, arr[:, 0, :])

    def test_d_picks_bottom_layer(self, arr):
        picked = arr[SLICE.D(0)]
        np.testing.assert_array_equal(picked, arr[:, -1, :])

    def test_l_picks_left_layer(self, arr):
        picked = arr[SLICE.L(0)]
        np.testing.assert_array_equal(picked, arr[:, :, 0])

    def test_r_picks_right_layer(self, arr):
        picked = arr[SLICE.R(0)]
        np.testing.assert_array_equal(picked, arr[:, :, -1])

    def test_f_picks_front_layer(self, arr):
        picked = arr[SLICE.F(0)]
        np.testing.assert_array_equal(picked, arr[0, :, :])

    def test_b_picks_back_layer(self, arr):
        picked = arr[SLICE.B(0)]
        np.testing.assert_array_equal(picked, arr[-1, :, :])

    def test_opposite_faces_do_not_overlap(self, arr):
        """On a 3x3, U and D should pick disjoint cells."""
        u_cells = set(arr[SLICE.U(0)].flatten().tolist())
        d_cells = set(arr[SLICE.D(0)].flatten().tolist())
        assert u_cells.isdisjoint(d_cells)


class TestTwoTwo:
    """twotwo is the underlying builder behind SLICE.X."""

    def test_u_near_end(self):
        assert twotwo(0, "U") == (ALL_NONE, 0, ALL_NONE)

    def test_d_flips_index(self):
        """For 'far end' faces the index is negated as -(i+1) — so index 0 maps to -1."""
        assert twotwo(0, "D") == (ALL_NONE, -1, ALL_NONE)
        assert twotwo(1, "D") == (ALL_NONE, -2, ALL_NONE)
        assert twotwo(2, "D") == (ALL_NONE, -3, ALL_NONE)


class TestOrientationLayout:
    def test_contains_all_six_faces(self):
        assert set(ORIENTATION_LAYOUT) == {"U", "D", "L", "R", "F", "B"}

    def test_length(self):
        assert len(ORIENTATION_LAYOUT) == 6


class TestColors:
    @pytest.mark.parametrize(
        "name,expected",
        [
            ("w", [255, 255, 255]),
            ("y", [255, 255, 0]),
            ("r", [255, 0, 0]),
            ("o", [255, 121, 0]),
            ("b", [0, 0, 255]),
            ("g", [0, 255, 0]),
            ("black", [0, 0, 0]),
        ],
    )
    def test_rgb_triples(self, name, expected):
        assert colors[name] == expected

    def test_attribute_access(self):
        assert colors.w == [255, 255, 255]

    @pytest.mark.parametrize("name", ["w", "y", "r", "o", "b", "g", "black"])
    def test_is_valid_rgb(self, name):
        rgb = colors[name]
        assert len(rgb) == 3
        assert all(0 <= c <= 255 for c in rgb)


class TestDefaultCubes:
    """The DEFAULT_CUBE_* arrays are pre-built solved-state Cubelet grids.
    They aren't imported by Cube itself, but they're part of the public
    constants surface, so we lock down their shape and contents."""

    def test_2x2_shape(self):
        assert len(DEFAULT_CUBE_2X2) == 2
        assert all(len(layer) == 2 for layer in DEFAULT_CUBE_2X2)
        assert all(len(row) == 2 for layer in DEFAULT_CUBE_2X2 for row in layer)

    def test_3x3_shape(self):
        assert len(DEFAULT_CUBE_3X3) == 3
        assert all(len(layer) == 3 for layer in DEFAULT_CUBE_3X3)
        assert all(len(row) == 3 for layer in DEFAULT_CUBE_3X3 for row in layer)

    def test_2x2_all_entries_are_cubelets(self):
        for layer in DEFAULT_CUBE_2X2:
            for row in layer:
                for cell in row:
                    assert isinstance(cell, Cubelet)

    def test_3x3_all_entries_are_cubelets(self):
        for layer in DEFAULT_CUBE_3X3:
            for row in layer:
                for cell in row:
                    assert isinstance(cell, Cubelet)

    def test_2x2_corner_pieces_have_three_colors(self):
        """On a 2x2, every piece is a corner with exactly 3 exposed faces."""
        for layer in DEFAULT_CUBE_2X2:
            for row in layer:
                for cell in row:
                    exposed = [v for v in cell.pos.values() if v is not None]
                    assert len(exposed) == 3

    def test_3x3_center_has_one_color(self):
        """The very centre of a solved 3x3 is fully interior — no exposed faces."""
        center = DEFAULT_CUBE_3X3[1][1][1]
        assert all(v is None for v in center.pos.values())

    def test_3x3_face_centers_have_one_color(self):
        """A face-center on a 3x3 has exactly one exposed sticker."""
        # Front face centre: layer 0 (F), middle row, middle column.
        fc = DEFAULT_CUBE_3X3[0][1][1]
        exposed = [v for v in fc.pos.values() if v is not None]
        assert exposed == ["red"]
