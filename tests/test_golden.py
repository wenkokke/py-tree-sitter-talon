import pytest

import tree_sitter_talon.ast as ast

from . import node_dict_simplify


@pytest.mark.golden_test("data/golden/*.yml")
def test_golden(golden):
    node_dict = ast.parse(golden["input"]).to_dict()
    node_dict_simplify(node_dict)
    assert node_dict == golden.out["output"]
