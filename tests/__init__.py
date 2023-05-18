import inspect
import re
import sys
from types import ModuleType
from typing import Any, Dict, Iterator


def pyver() -> str:
    return f"py{sys.version_info.major}{sys.version_info.minor}"


def short(sig: inspect.Signature) -> str:
    out = str(sig)
    out = re.sub(r"ForwardRef\('([^']+)'\)", r"\1", out)
    out = out.replace("tree_sitter_type_provider.node_types.", "")
    out = out.replace("abc.Talon", "Talon")
    out = re.sub(r"'Talon([^']+)'", r"Talon\1", out)
    return out


def function_signatures(defns: Dict[str, Any]) -> Iterator[str]:
    for name, fun in defns.items():
        if inspect.isfunction(fun) and not name.startswith("_"):
            try:
                funsig = inspect.signature(fun)
                yield f"def {name}{short(funsig)}:"
                yield f"  pass"
            except ValueError:
                pass


def class_signatures(defns: Dict[str, Any]) -> Iterator[str]:
    for name, cls in defns.items():
        if inspect.isclass(cls) and not name.startswith("_"):
            try:
                parent = cls.__mro__[1].__name__
                init = short(inspect.signature(cls))
                yield f"class {name}({parent}):"
                yield f"  def __init__{init}:"
                yield f"    pass"
            except ValueError:
                pass


def node_dict_simplify(node_dict: Dict[str, Any]) -> None:
    if len(node_dict) > 4:
        del node_dict["text"]

    del node_dict["start_position"]
    del node_dict["end_position"]

    for key in node_dict.keys():
        if isinstance(node_dict[key], dict):
            node_dict_simplify(node_dict[key])
        if isinstance(node_dict[key], list):
            for val in node_dict[key]:
                if isinstance(val, dict):
                    node_dict_simplify(val)
