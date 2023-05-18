import io
import pickle

from pytest import mark
from pytest_golden.plugin import GoldenTestFixture, GoldenTestUsageWarning

from tree_sitter_talon import (  # type: ignore[attr-defined]
    TalonCommandDeclaration,
    TalonSourceFile,
    parse,
)

from . import node_dict_simplify


@mark.golden_test("data/golden/*.yml")  # type: ignore[misc]
def test_golden_dict(golden: GoldenTestFixture) -> None:
    try:
        node = parse(golden["input"])
        node_dict = node.to_dict()
        node_dict_simplify(node_dict)
        assert node_dict == golden.out["output"]
    except GoldenTestUsageWarning:
        pass


@mark.golden_test("data/golden/*.yml")  # type: ignore[misc]
def test_golden_pickle(golden: GoldenTestFixture) -> None:
    try:
        node_before = parse(golden["input"])
        node_pickled = pickle.dumps(node_before)
        node_after = pickle.loads(node_pickled)
        assert node_before == node_after
    except GoldenTestUsageWarning:
        pass


@mark.golden_test("data/golden/*.yml")  # type: ignore[misc]
def test_golden_match(golden: GoldenTestFixture) -> None:
    source_file = parse(golden["input"])
    assert isinstance(source_file, TalonSourceFile)
    try:
        for command in golden["commands"]:
            assert isinstance(command, str)
            declaration = source_file.find_command(list(command.split()))
            assert isinstance(declaration, TalonCommandDeclaration)
    except KeyError:
        pass
    except GoldenTestUsageWarning:
        pass
