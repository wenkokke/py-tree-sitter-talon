import pathlib

import pkg_resources  # type: ignore


def _get_node_types() -> pathlib.Path:
    node_types_relpath = pathlib.Path(
        "data", "tree-sitter-talon", "src", "node-types.json"
    )
    node_types = pkg_resources.resource_filename(
        "tree_sitter_talon", str(node_types_relpath)
    )
    if node_types:
        node_types = pathlib.Path(node_types)
        if node_types.exists():
            return node_types
    node_types = (
        pathlib.Path(__file__).parent / "tree_sitter_talon" / node_types_relpath
    )
    if node_types:
        if node_types.exists():
            return node_types
    raise FileNotFoundError(str(node_types_relpath))
