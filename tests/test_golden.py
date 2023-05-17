import io
import pickle

import pytest

import tree_sitter_talon

from . import node_dict_simplify


@pytest.mark.golden_test("data/golden/*.yml")
def test_golden_dict(golden) -> None:
    node = tree_sitter_talon.parse(golden["input"])
    node_dict = node.to_dict()
    node_dict_simplify(node_dict)
    assert node_dict == golden.out["output"]


@pytest.mark.golden_test("data/golden/*.yml")
def test_golden_pickle(golden) -> None:
    buffer_out = io.BytesIO()
    node_before = tree_sitter_talon.parse(golden["input"])
    pickle.dump(node_before, buffer_out)
    buffer_in = io.BytesIO(buffer_out.getvalue())
    node_after = pickle.load(buffer_in)
    assert node_before == node_after
    # NOTE: suppresses GoldenTestUsageWarning
    assert golden["output"] is not None


@pytest.mark.golden_test("data/golden/*.yml")
def test_golden_match(golden) -> None:
    source_file = tree_sitter_talon.parse(golden["input"])
    assert isinstance(source_file, tree_sitter_talon.TalonSourceFile)
    try:
        for command in golden["commands"]:
            assert isinstance(command, str)
            declaration = source_file.find_command(list(command.split()))
            assert isinstance(declaration, tree_sitter_talon.TalonCommandDeclaration)
    except KeyError:
        pass
    # NOTE: suppresses GoldenTestUsageWarning
    assert golden["output"] is not None
