from collections.abc import Generator
import inspect
import pytest
import re
import tree_sitter_talon
import typing


Context: typing.TypeAlias = typing.Union[None, typing.Mapping[str, typing.Any]]


def short(sig: inspect.Signature) -> str:
    out = str(sig)
    out = out.replace("tree_sitter_type_provider.node_types.", "")
    out = re.sub(r"ForwardRef\('(\w+)'\)", r"\1", out)
    out = out.replace("typing.", "")
    out = out.replace("NoneType", "None")
    out = out.replace("abc.", "")
    out = out.replace("~Result", "Result")
    return out


def function_signatures(
    object: object, ctx: Context = None
) -> Generator[str, None, None]:
    for name, fun in inspect.getmembers(object, inspect.isfunction):
        if not (name.startswith("_") or name in ["to_dict", "to_json"]):
            try:
                funsig = inspect.signature(fun, globals=ctx, eval_str=True)
                yield f"{name}{short(funsig)}"
            except ValueError:
                pass


def class_signatures(object: object, ctx: Context = None) -> Generator[str, None, None]:
    for name, cls in inspect.getmembers(object, inspect.isclass):
        if not name.startswith("_"):
            try:
                clssig = inspect.signature(cls, globals=ctx, eval_str=True)
                yield f"{name}{short(clssig)}"
                for funsigstr in function_signatures(cls, ctx=ctx):
                    yield f"  {funsigstr}"
            except ValueError:
                pass


@pytest.mark.golden_test("api.yml")
def test_talon_api(golden):
    assert golden["input"] is None

    ctx = globals() | tree_sitter_talon.__dict__

    output: list[str] = []
    output.extend(function_signatures(tree_sitter_talon.__class__, ctx=ctx))
    output.extend(function_signatures(tree_sitter_talon, ctx=ctx))
    output.extend(class_signatures(tree_sitter_talon.__class__, ctx=ctx))
    output.extend(class_signatures(tree_sitter_talon, ctx=ctx))

    assert "\n".join(output) == golden.out["output"]
