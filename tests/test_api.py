import pytest

from . import class_signatures, function_signatures


@pytest.mark.golden_test("data/api.yml")
def test_talon_api(golden):
    assert golden["input"] is None

    import tree_sitter_talon.ast as ast

    globals().update(ast.__dict__)

    output: list[str] = []
    output.extend(function_signatures(ast.__class__))
    output.extend(function_signatures(ast))
    output.extend(class_signatures(ast.__class__))
    output.extend(class_signatures(ast))

    assert "\n".join(output) == golden.out["output"]
