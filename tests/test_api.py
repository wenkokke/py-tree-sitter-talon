import typing

import pytest

from . import class_signatures, function_signatures, pyver


@pytest.mark.golden_test(f"data/api.{pyver()}.yml")
def test_talon_api(golden) -> None:
    assert golden["input"] is None

    import tree_sitter_talon

    globals().update(tree_sitter_talon.__dict__)

    output: typing.List[str] = []
    output.extend(function_signatures(tree_sitter_talon.__class__))
    output.extend(function_signatures(tree_sitter_talon))
    output.extend(class_signatures(tree_sitter_talon.__class__))
    output.extend(class_signatures(tree_sitter_talon))

    assert "\n".join(output) == golden.out["output"]
