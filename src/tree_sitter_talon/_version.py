import json
import pathlib

import importlib_resources

################################################################################
# Version Number
################################################################################

# The build number.
__build__: int = 1007

# The tree-sitter-talon version.
try:
    __tree_sitter_talon_version__: str = json.loads(
        importlib_resources.files("tree_sitter_talon")
        .joinpath("_tree_sitter_talon", "package.json")
        .read_text(encoding="utf-8")
    )["version"]
except ModuleNotFoundError:
    __tree_sitter_talon_version__: str = json.loads(  # type: ignore[no-redef]
        (
            pathlib.Path(__file__).parent / "_tree_sitter_talon" / "package.json"
        ).read_text(encoding="utf-8")
    )["version"]

# The py-tree-sitter-talon version.
VERSION: str = f"{__build__}.{__tree_sitter_talon_version__}"
