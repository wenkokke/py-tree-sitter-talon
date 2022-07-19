from collections.abc import Generator
import tree_sitter_talon as talon
import pytest
import inspect


def function_signatures(object: object) -> Generator[str, None, None]:
    for name, fun in inspect.getmembers(object, inspect.isfunction):
        if not name.startswith("_"):
            yield f"{name}{inspect.signature(fun)}"


def class_signatures(object: object) -> Generator[str, None, None]:
    for name, cls in inspect.getmembers(object, inspect.isclass):
        if not name.startswith("_"):
            yield f"{name}{inspect.signature(cls)}"
            for sig in function_signatures(cls):
                yield f"  {sig}"


@pytest.mark.golden_test("talon_api.yml")
def test_talon_api(golden):
    assert golden["input"] is None

    output: list[str] = []
    output.extend(function_signatures(talon.__class__))
    output.extend(function_signatures(talon))
    output.extend(class_signatures(talon.__class__))
    output.extend(class_signatures(talon))

    assert "\n".join(output) == golden.out["output"]
