import json
import pathlib

import importlib_resources

################################################################################
# Version Number
################################################################################

# The tree-sitter-talon version.
try:
    TREE_SITTER_TALON_VERSION: str = json.loads(
        importlib_resources.files("tree_sitter_talon")
        .joinpath("_tree_sitter_talon", "package.json")
        .read_text(encoding="utf-8")
    )["version"]
except ModuleNotFoundError:
    TREE_SITTER_TALON_VERSION: str = json.loads(  # type: ignore[no-redef]
        (
            pathlib.Path(__file__).parent / "_tree_sitter_talon" / "package.json"
        ).read_text(encoding="utf-8")
    )["version"]

VERSION: str = f"1!1.0.6+grammar{TREE_SITTER_TALON_VERSION}"
