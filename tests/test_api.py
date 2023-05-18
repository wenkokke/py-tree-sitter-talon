from typing import List

from pytest import mark
from pytest_golden.plugin import GoldenTestFixture

from . import class_signatures, function_signatures, pyver


@mark.golden_test(f"data/api.{pyver()}.yml")  # type: ignore[misc]
def test_talon_api(golden: GoldenTestFixture) -> None:
    assert golden["input"] is None

    import tree_sitter_talon

    defns = {
        name: defn
        for name, defn in tree_sitter_talon.__dict__.items()
        if name in tree_sitter_talon.__all__
    }
    globals().update(defns)

    output: List[str] = []
    output.extend(function_signatures(defns))
    output.extend(class_signatures(defns))

    assert "\n".join(output) == golden.out["output"]
