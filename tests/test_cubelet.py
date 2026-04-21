"""Tests for rubik_toolkit.cubelet.Cubelet.

Cubelet is a tiny value-wrapper around a dict of six face-to-colour entries.
These tests pin down the contract: construction, repr, mutation, and the
fact that the class holds its dict by reference (used by Cube.orient_cubelets).
"""
import copy

import pytest

from rubik_toolkit.cubelet import Cubelet


FULL_POS = {"u": "yellow", "d": None, "l": "blue", "r": None, "f": "red", "b": None}


class TestCubeletConstruction:
    def test_stores_pos_dict(self):
        cb = Cubelet(FULL_POS)
        assert cb.pos == FULL_POS

    def test_stores_pos_by_reference(self):
        """Cube.orient_cubelets mutates cubelet.pos in place, so Cubelet must
        not deep-copy the dict on construction."""
        pos = dict(FULL_POS)
        cb = Cubelet(pos)
        assert cb.pos is pos

    def test_accepts_all_none_pos(self):
        """Interior cubelet of a cube >=3: every face is None."""
        pos = {k: None for k in "udlrfb"}
        cb = Cubelet(pos)
        assert cb.pos == pos

    def test_accepts_empty_dict(self):
        """Constructor imposes no schema — an empty dict is accepted."""
        cb = Cubelet({})
        assert cb.pos == {}

    def test_accepts_extra_keys(self):
        """Constructor imposes no schema — extra keys pass through."""
        cb = Cubelet({"u": "yellow", "extra": "ignored"})
        assert cb.pos["extra"] == "ignored"


class TestCubeletRepr:
    def test_repr_is_dict_str(self):
        cb = Cubelet(FULL_POS)
        assert repr(cb) == str(FULL_POS)

    def test_repr_returns_str(self):
        cb = Cubelet(FULL_POS)
        assert isinstance(repr(cb), str)

    def test_repr_reflects_mutation(self):
        cb = Cubelet(dict(FULL_POS))
        cb.pos["u"] = "green"
        assert "'u': 'green'" in repr(cb)


class TestCubeletMutation:
    def test_pos_is_mutable(self):
        cb = Cubelet(dict(FULL_POS))
        cb.pos["u"] = "green"
        assert cb.pos["u"] == "green"

    def test_can_swap_faces_in_place(self):
        """Simulates what Cube.orient_cubelets does when rotating a layer."""
        cb = Cubelet({"u": "yellow", "l": "blue", "f": "red", "r": None, "d": None, "b": None})
        cb.pos["u"], cb.pos["l"], cb.pos["f"] = cb.pos["l"], cb.pos["f"], cb.pos["u"]
        assert cb.pos["u"] == "blue"
        assert cb.pos["l"] == "red"
        assert cb.pos["f"] == "yellow"


class TestCubeletCopy:
    def test_deepcopy_is_independent(self):
        """Cube.copy() relies on deepcopy producing independent cubelets."""
        cb = Cubelet(dict(FULL_POS))
        other = copy.deepcopy(cb)
        other.pos["u"] = "green"
        assert cb.pos["u"] == "yellow"

    def test_shallow_copy_shares_dict(self):
        """Sanity check — documents that shallow copy.copy would share state."""
        cb = Cubelet(dict(FULL_POS))
        other = copy.copy(cb)
        other.pos["u"] = "green"
        # Pure shallow copy of the object would share the same dict reference.
        assert cb.pos["u"] == "green"
