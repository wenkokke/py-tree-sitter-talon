import json
import pathlib

__version_binding__: str = "1000"


def _get_tree_sitter_package_json() -> pathlib.Path:
    pkg_path = pathlib.Path(__file__).parent / "tree_sitter_talon"
    package_json_relpath = pathlib.Path("data", "tree-sitter-talon", "package.json")
    package_json = pkg_path / package_json_relpath
    if package_json:
        if package_json.exists():
            return package_json
    raise FileNotFoundError(str(package_json_relpath))


def _get_version_grammar() -> str:
    package_json = _get_tree_sitter_package_json()
    version_grammar = json.loads(package_json.read_text())["version"]
    version_grammar = version_grammar.removeprefix("v")
    return version_grammar


__version_grammar__: str = _get_version_grammar()


def _get_version() -> str:
    return f"1!{__version_binding__}.{__version_grammar__}"


__version__: str = _get_version()


if __name__ == "__main__":
    print(__version__)
