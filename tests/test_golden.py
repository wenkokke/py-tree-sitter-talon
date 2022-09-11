import io
import pickle

import pytest

import tree_sitter_talon

from . import node_dict_simplify


@pytest.mark.golden_test("data/golden/*.yml")
def test_golden(golden):
    node_dict = tree_sitter_talon.parse(golden["input"]).to_dict()
    node_dict_simplify(node_dict)
    assert node_dict == golden.out["output"]


@pytest.mark.golden_test("data/golden/*.yml")
def test_golden_pickle(golden):
    buffer_out = io.BytesIO()
    node_before = tree_sitter_talon.parse(golden["input"])
    pickle.dump(node_before, buffer_out)
    buffer_in = io.BytesIO(buffer_out.getvalue())
    node_after = pickle.load(buffer_in)
    assert node_before == node_after
