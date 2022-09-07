import json
import pathlib

import pkg_resources  # type: ignore

__version_binding__: str = "v4.0"


def _get_package_json() -> pathlib.Path:
    package_json_relpath = pathlib.Path("data", "tree-sitter-talon", "package.json")
    package_json = pkg_resources.resource_filename(
        "tree_sitter_talon", str(package_json_relpath)
    )
    if package_json:
        package_json = pathlib.Path(package_json)
        if package_json.exists():
            return package_json
    package_json = (
        pathlib.Path(__file__).parent / "tree_sitter_talon" / package_json_relpath
    )
    if package_json:
        if package_json.exists():
            return package_json
    raise FileNotFoundError(str(package_json_relpath))


def _get_version_grammar() -> str:
    package_json = _get_package_json()
    return json.loads(package_json.read_text())["version"]


__version_grammar__: str = f"v{_get_version_grammar()}"


def _get_version() -> str:
    version_grammar_parts = _get_version_grammar().split(".")
    assert (
        2 <= len(version_grammar_parts) <= 3
    ), f"Version for tree-sitter-talon must contain at least a MAJOR and a MINOR component, found '{__version_grammar__}'."
    major_grammar, minor_grammar = version_grammar_parts[:2]
    major_binding, minor_binding = __version_binding__.split(".")
    if minor_binding == "0":
        return f"1!{major_grammar}.{minor_grammar}.{major_binding}"
    else:
        return f"1!{major_grammar}.{minor_grammar}.{major_binding}.post{minor_binding}"


__version__: str = f"v{_get_version()}"
