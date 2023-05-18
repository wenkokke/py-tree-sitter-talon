import json
import pathlib

import importlib_resources
import packaging.version

################################################################################
# Version Number
################################################################################

# The tree-sitter-talon version.
TREE_SITTER_TALON: packaging.version.Version
try:
    TREE_SITTER_TALON_VERSION = packaging.version.Version(
        json.loads(
            importlib_resources.files("tree_sitter_talon")
            .joinpath("_tree_sitter_talon", "package.json")
            .read_text(encoding="utf-8")
        )["version"]
    )
except ModuleNotFoundError:
    TREE_SITTER_TALON_VERSION = packaging.version.Version(
        json.loads(  # type: ignore[no-redef]
            (
                pathlib.Path(__file__).parent / "_tree_sitter_talon" / "package.json"
            ).read_text(encoding="utf-8")
        )["version"]
    )

VERSION: str = f"{TREE_SITTER_TALON_VERSION.major}!1.0"
